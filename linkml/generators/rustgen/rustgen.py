from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Optional, Union, overload

from jinja2 import Environment
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    EnumDefinition,
    PermissibleValue,
    SlotDefinition,
    TypeDefinition,
)
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import OrderedBy, SchemaView

from linkml.generators.common.lifecycle import LifecycleMixin
from linkml.generators.common.template import ObjectImport
from linkml.generators.rustgen.build import (
    AttributeResult,
    ClassResult,
    CrateResult,
    EnumResult,
    FileResult,
    SlotResult,
    TypeResult,
)
from linkml.generators.rustgen.template import (
    Import,
    Imports,
    RustCargo,
    RustEnum,
    RustFile,
    SerdeUtilsFile,
    RustProperty,
    AsKeyValue,
    RustPyProject,
    RustStruct,
    RustTemplateModel,
    RustTypeAlias,
)
from linkml.utils.generator import Generator

RUST_MODES = Literal["crate", "file"]

PYTHON_TO_RUST = {
    int: "isize",
    float: "f64",
    str: "String",
    bool: "bool",
    "int": "isize",
    "float": "f64",
    "str": "String",
    "bool": "bool",
    "Bool": "bool",
    "XSDDate": "NaiveDate",
    "date": "NaiveDate",
    "XSDDateTime": "NaiveDateTime",
    "datetime": "NaiveDateTime",
    # "Decimal": "dec",
    "Decimal": "f64",
}
"""
Mapping from python types to rust types.

.. todo::

    - Add numpy types
    - make an enum wrapper for naivedatetime and datetime<fixedoffset> that can represent both of them

"""

PROTECTED_NAMES = ("type", "typeof", "abstract")

RUST_IMPORTS = {
    "dec": Import(module="rust_decimal", version="1.36", objects=[ObjectImport(name="dec")]),
    "NaiveDate": Import(module="chrono", features=["serde"], version="0.4.41", objects= [ObjectImport(name="NaiveDate")]),
    "NaiveDateTime": Import(module="chrono", features=["serde"], version="0.4.41", objects= [ObjectImport(name="NaiveDateTime")]),
}

DEFAULT_IMPORTS = Imports(
    imports=[
        Import(module="std::collections", objects=[ObjectImport(name="HashMap")]),
        # Import(module="std::fmt", objects=[ObjectImport(name="Display")]),
    ]
)

SERDE_IMPORTS = Imports(
    imports=[
        Import(
            module="serde",
            version="1.0",
            features=["derive"],
            objects=[ObjectImport(name="Serialize"), ObjectImport(name="Deserialize"), ObjectImport(name="de::IntoDeserializer")],
            feature_flag="serde",
        ),
        Import(module="serde-value", version="0.7.0", objects=[ObjectImport(name="Value")]),
        Import(module="serde_yml", version="0.0.12", feature_flag="serde"),
    ]
)

PYTHON_IMPORTS = Imports(
    imports = [
        Import(module="pyo3", version="0.25.0", objects=[ObjectImport(name="prelude::*"), ObjectImport(name="FromPyObject")], feature_flag="pyo3", features=["chrono"]),
        # Import(module="serde_pyobject", version="0.6.1", objects=[], feature_flag="pyo3", features=[]),
    ]
)


def get_rust_type(t: Union[TypeDefinition, type, str], sv: SchemaView, pyo3: bool = False) -> str:
    """
    Get the rust type from a given linkml type
    """
    rsrange = None

    if isinstance(t, TypeDefinition):
        rsrange = t.base
        if rsrange is not None and rsrange not in PYTHON_TO_RUST:
            # A type like URIorCURIE which is an alias for a rust type
            rsrange = get_name(t)

        elif rsrange is None and t.typeof is not None:
            # A type with no base type,
            rsrange = get_rust_type(sv.get_type(t.typeof), sv, pyo3)

    elif isinstance(t, str):
        if tdef := sv.all_types().get(t, None):
            rsrange = get_rust_type(tdef, sv, pyo3)
        elif t in sv.all_classes():
            rsrange = get_name(sv.get_class(t))

    # FIXME: Raise here once we have implemented all base types
    if rsrange is None:
        rsrange = PYTHON_TO_RUST[str]
    elif rsrange in PYTHON_TO_RUST:
        rsrange = PYTHON_TO_RUST[rsrange]
    return rsrange


def protect_name(v: str) -> str:
    """
    append an underscore to a protected name
    """
    if v in PROTECTED_NAMES:
        v = f"{v}_"
    return v


def get_name(e: Union[ClassDefinition, SlotDefinition, EnumDefinition, PermissibleValue, TypeDefinition]) -> str:
    if isinstance(e, (ClassDefinition, EnumDefinition)):
        name = camelcase(e.name)
    elif isinstance(e, PermissibleValue):
        name = camelcase(e.text)
    elif isinstance(e, (SlotDefinition, TypeDefinition)):
        name = underscore(e.name)
    else:
        raise ValueError("Can only get the name from a slot or class!")

    name = protect_name(name)
    return name


@dataclass
class RustGenerator(Generator, LifecycleMixin):
    """
    Generate rust types from a linkml schema
    """

    generatorname = "rustgenerator"
    generatorversion = "0.0.2"
    valid_formats = ["rust"]
    file_extension = "rs"
    crate_name: Optional[str] = None

    pyo3: bool = True
    """Generate pyO3 bindings for the rust defs"""
    pyo3_version: str = ">=0.21.1"
    serde: bool = True
    """Generate serde derive serialization/deserialization attributes"""
    mode: RUST_MODES = "crate"
    """Generate a cargo.toml file"""
    output: Optional[Path] = None
    """
    * If ``mode == "crate"`` , a directory to contain the generated crate
    * If ``mode == "file"`` , a file with a ``.rs`` extension
    
    If output is not provided at object instantiation,
    it must be provided on a call to :meth:`.serialize`
    """

    _environment: Optional[Environment] = None

    def __post_init__(self):
        # TODO: consider moving up a level
        self.schemaview: SchemaView = SchemaView(self.schema)
        super().__post_init__()

    def generate_type(self, type_: TypeDefinition) -> TypeResult:
        type_ = self.before_generate_type(type_, self.schemaview)
        res = TypeResult(
            source=type_,
            type_=RustTypeAlias(
                name=get_name(type_), type_=[get_rust_type(type_.base, self.schemaview, self.pyo3)], pyo3=self.pyo3
            ),
            imports=self.get_imports(type_),
        )
        slot = self.after_generate_type(res, self.schemaview)
        return slot

    def generate_enum(self, enum: EnumDefinition) -> EnumResult:
        # TODO: this
        enum = self.before_generate_enum(enum, self.schemaview)
        res = EnumResult(
            source=enum,
            enum=RustEnum(
                name=get_name(enum),
                items=[get_name(i) for i in enum.permissible_values.values()],
                pyo3=self.pyo3,
                serde=self.serde,
            ),
        )
        res = self.after_generate_enum(res, self.schemaview)
        return res

    def generate_slot(self, slot: SlotDefinition) -> SlotResult:
        """
        Generate a slot as a struct field
        """
        slot = self.before_generate_slot(slot, self.schemaview)
        class_range = slot.range in self.schemaview.all_classes()
        type_ = [get_rust_type(slot.range, self.schemaview, self.pyo3)]
        if class_range:
            descendants = self.schemaview.class_descendants(slot.range)
            type_ = [get_rust_type(d, self.schemaview, self.pyo3) for d in descendants]
            
        slot = SlotResult(
            source=slot,
            slot=RustTypeAlias(
                name=get_name(slot),
                type_=type_,
                multivalued=slot.multivalued,
                pyo3=self.pyo3,
                class_range=class_range,
            ),
            imports=self.get_imports(slot),
        )
        slot = self.after_generate_slot(slot, self.schemaview)
        return slot

    def generate_class(self, cls: ClassDefinition) -> ClassResult:
        """
        Generate a class as a struct!
        """
        cls = self.before_generate_class(cls, self.schemaview)
        induced_attrs = [self.schemaview.induced_slot(sn, cls.name) for sn in self.schemaview.class_slots(cls.name)]
        induced_attrs = self.before_generate_slots(induced_attrs, self.schemaview)
        attributes = [self.generate_attribute(attr, cls) for attr in induced_attrs]
        attributes = self.after_generate_slots(attributes, self.schemaview)

        unsendable = any([a.range in self.schemaview.all_classes() for a in induced_attrs])

        res = ClassResult(
            source=cls,
            cls=RustStruct(
                name=get_name(cls),
                properties=[a.attribute for a in attributes],
                unsendable=unsendable,
                pyo3=self.pyo3,
                serde=self.serde,
                as_key_value=self.generate_class_as_key_value(cls),
            ),
        )
        # merge imports
        for attr in attributes:
            res = res.merge(attr)

        res = self.after_generate_class(res, self.schemaview)
        return res
    
    def generate_class_as_key_value(self, cls: ClassDefinition) -> Optional[AsKeyValue]:
        induced_attrs = [self.schemaview.induced_slot(sn, cls.name) for sn in self.schemaview.class_slots(cls.name)]
        key_attr = None
        identifier_attr = None
        value_attrs = []
        for attr in induced_attrs:
            if attr.identifier:
                if identifier_attr is not None:
                    ## multiple identifiers --> don't know what to do!
                    return None
                identifier_attr = attr
            if attr.key:
                if key_attr is not None:
                    ## multiple keys --> don't know what to do!
                    return None
                key_attr = attr
            else:
                value_attrs.append(attr)
        if key_attr is not None and len(value_attrs) == 1:
            return AsKeyValue(
                    name=get_name(cls),
                    key_property_name=get_name(key_attr),
                    key_property_type=get_rust_type(key_attr.range, self.schemaview, self.pyo3),
                    value_property_name=get_name(value_attrs[0]),
                    value_property_type=get_rust_type(value_attrs[0].range, self.schemaview, self.pyo3),
                    serde=self.serde,
                    pyo3=self.pyo3,
            )
        if identifier_attr is not None and len(value_attrs) > 1:
            key_attr = identifier_attr
            return AsKeyValue(
                    name=get_name(cls),
                    key_property_name=get_name(key_attr),
                    key_property_type=get_rust_type(key_attr.range, self.schemaview, self.pyo3),
                    value_property_name=None,
                    key_attrib_in_value=get_name(key_attr),
                    value_property_type="Value",
                    serde=self.serde,
                    pyo3=self.pyo3,
            )
        return None
                

    def generate_attribute(self, attr: SlotDefinition, cls: ClassDefinition) -> AttributeResult:
        """
        Generate an attribute as a struct property
        """
        attr = self.before_generate_slot(attr, self.schemaview)
        is_class_range = attr.range in self.schemaview.all_classes()

        # -------
        # check for circular class -> slot -> class -> slot -> class recursion
        # FIXME: split this up lol

        reference_recursive = False
        is_key_value = False
        if is_class_range:
            induced_range = self.schemaview.induced_class(attr.range)
            is_key_value = (attr.inlined is True) and (self.generate_class_as_key_value(induced_range) is not None)
            attr_ranges = [attr.range for attr in induced_range.attributes.values()]
            reference_recursive = cls.name in attr_ranges

        is_recursive = attr.range == cls.name or reference_recursive

        type_=[get_rust_type(attr.range, self.schemaview, self.pyo3)]
        if is_class_range:
            descendants = self.schemaview.class_descendants(attr.range)
            type_ = [get_rust_type(d, self.schemaview, self.pyo3) for d in descendants]
        

        res = AttributeResult(
            source=attr,
            attribute=RustProperty(
                name=get_name(attr),
                type_=type_,
                required=bool(attr.required),
                multivalued=attr.multivalued,
                class_range=is_class_range,
                pyo3=self.pyo3,
                serde=self.serde,
                recursive=is_recursive,
                inlined=bool(attr.inlined and not attr.inlined_as_list),
                inlined_as_list=bool(attr.inlined_as_list),
                is_key_value=is_key_value,
                has_slot_usage=attr.name in cls.slot_usage.keys(),
                class_name=get_name(cls),
            ),
            imports=self.get_imports(attr),
        )
        res = self.after_generate_slot(res, self.schemaview)
        return res

    def generate_cargo(self, imports: Imports) -> RustCargo:
        """
        Generate a Cargo.toml file
        """
        version = self.schemaview.schema.version if self.schemaview.schema.version is not None else "0.0.0"
        return RustCargo(
            name=self.crate_name if self.crate_name is not None else self.schemaview.schema.name,
            version=version,
            imports=imports,
            pyo3_version=self.pyo3_version,
            pyo3=self.pyo3,
            serde=self.serde,
        )

    def generate_pyproject(self) -> RustPyProject:
        """
        Generate a pyproject.toml file for a pyo3 rust crate
        """
        version = self.schemaview.schema.version if self.schemaview.schema.version is not None else "0.0.0"
        return RustPyProject(name=self.schemaview.schema.name, version=version)

    def get_imports(self, element: Union[SlotDefinition, TypeDefinition]) -> Imports:
        if isinstance(element, SlotDefinition):
            type_ = get_rust_type(element.range, self.schemaview, self.pyo3)
        elif isinstance(element, TypeDefinition):
            type_ = get_rust_type(element.base, self.schemaview, self.pyo3)
        else:
            raise TypeError("Must be a slot or type definition")

        if type_ in RUST_IMPORTS:
            return Imports(imports=[RUST_IMPORTS[type_]])
        else:
            return Imports()

    @overload
    def render(self, mode: Literal["file"] = "file") -> FileResult: ...

    @overload
    def render(self, mode: Literal["crate"] = "crate") -> CrateResult: ...

    def render(self, mode: Optional[RUST_MODES] = None) -> Union[FileResult, CrateResult]:
        """
        Render the template model of a rust file before serializing

        Args:
            mode (:class:`.RUST_MODES`, optional): Override the instance-level generation mode
        """
        if mode is None:
            mode = self.mode

        sv = self.schemaview

        types = list(sv.all_types(imports=True).values())
        types = self.before_generate_types(types, sv)
        types = [self.generate_type(t) for t in types]
        types = self.after_generate_types(types, sv)

        enums = list(sv.all_enums(imports=True).values())
        enums = self.before_generate_enums(enums, sv)
        enums = [self.generate_enum(e) for e in enums]
        enums = self.after_generate_enums(enums, sv)

        slots = list(sv.induced_slot(s) for s in sv.all_slots())
        slots = self.before_generate_slots(slots, sv)
        slots = [self.generate_slot(s) for s in slots]
        slots = self.after_generate_slots(slots, sv)

        classes = list(sv.induced_class(c) for c in sv.all_classes(ordered_by=OrderedBy.INHERITANCE))
        classes = self.before_generate_classes(classes, sv)
        classes = [self.generate_class(c) for c in classes]
        classes = self.after_generate_classes(classes, sv)

        imports = DEFAULT_IMPORTS.model_copy()
        imports += PYTHON_IMPORTS
        imports += SERDE_IMPORTS
        for result in [*enums, *slots, *classes]:
            imports += result.imports

        # TODO: get imports from all results

        file = RustFile(
            name=sv.schema.name,
            imports=imports,
            slots=[t.slot for t in slots],
            types=[t.type_ for t in types],
            enums=[e.enum for e in enums],
            structs=[c.cls for c in classes],
            pyo3=self.pyo3,
            serde=self.serde,
        )

        if mode == "crate":
            extra_files = {}
            extra_files["serde_utils"] = SerdeUtilsFile()
            cargo = self.generate_cargo(imports)
            pyproject = self.generate_pyproject()
            res = CrateResult(cargo=cargo, file=file, pyproject=pyproject, source=sv.schema, extra_files=extra_files)
            return res
        else:
            res = FileResult(file=file, source=sv.schema)
            return res

    def serialize(self, output: Optional[Path] = None, mode: Optional[RUST_MODES] = None, force: bool = False) -> str:
        """
        Serialize a schema to a rust crate or file.

        Args:
            output (Path, optional): A ``.rs`` file if in ``file`` mode,
                directory otherwise.
            force (bool): If the output already exists, overwrite it.
                Otherwise raise a :class:`FileExistsError`
        """
        if mode is None:
            mode = self.mode

        output = self._validate_output(output, mode, force)
        rendered = self.render(mode=mode)
        if mode == "crate":
            serialized = self.write_crate(output, rendered, force)
        else:
            serialized = rendered.file.render(self.template_environment)
            with open(output, "w") as f:
                f.write(serialized)

        return serialized

    def write_crate(
        self, output: Optional[Path] = None, rendered: Union[FileResult, CrateResult] = None, force: bool = False
    ) -> str:
        output = self._validate_output(output, mode="crate", force=force)
        if rendered is None:
            rendered = self.render(mode="crate")

        cargo = rendered.cargo.render(self.template_environment)
        cargo_file = output / "Cargo.toml"
        with open(cargo_file, "w") as cfile:
            cfile.write(cargo)

        pyproject = rendered.pyproject.render(self.template_environment)
        pyproject_file = output / "pyproject.toml"
        with open(pyproject_file, "w") as pyfile:
            pyfile.write(pyproject)

        rust_file = rendered.file.render(self.template_environment)
        src_dir = output / "src"
        src_dir.mkdir(exist_ok=True)
        lib_file = src_dir / "lib.rs"
        with open(lib_file, "w") as lfile:
            lfile.write(rust_file)

        for (k,f) in rendered.extra_files.items():
            extra_file = f.render(self.template_environment)
            extra_file_name = f"{k}.rs"
            extra_file_path = src_dir / extra_file_name
            with open(extra_file_path, "w") as ef:
                ef.write(extra_file)

        return rust_file

    def _validate_output(
        self, output: Optional[Path] = None, mode: Optional[RUST_MODES] = None, force: bool = False
    ) -> Path:
        """Raise a ValueError if given a dir when in file mode or vice versa"""
        if output is None:
            if self.output is None:
                raise ValueError("Must provide an output if generator doesn't already have one")
            else:
                output = Path(self.output)
        else:
            output = Path(output)

        if mode == "file":
            assert output.suffix == ".rs", "Output must be a rust file in file mode"
            if not force and output.exists():
                raise FileExistsError(f"{output} already exists and force is False! pass force=True to overwrite")
            output.parent.mkdir(exist_ok=True, parents=True)
        elif mode == "crate":
            if not force and len([d for d in output.iterdir()]) != 0:
                raise FileExistsError(
                    f"{output} already exists, is not empty,  and force is False! pass force=True to overwrite"
                )
            output.mkdir(exist_ok=True, parents=True)
        else:
            raise ValueError(f"Invalid generation mode: {mode}")

        return output

    @property
    def template_environment(self) -> Environment:
        if self._environment is None:
            self._environment = RustTemplateModel.environment()
        # if self.template_dir is not None:
        #     loader = ChoiceLoader([FileSystemLoader(self.template_dir), env.loader])
        #     env.loader = loader
        return self._environment
