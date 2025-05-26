from dataclasses import dataclass
from enum import Enum
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
from linkml_runtime.utils.formatutils import camelcase, underscore, uncamelcase
from linkml_runtime.utils.schemaview import OrderedBy, SchemaView

from linkml.generators.common.lifecycle import LifecycleMixin
from linkml.generators.common.template import ObjectImport
from linkml.generators.common.type_designators import get_accepted_type_designator_values, get_type_designator_value
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
    PolyFile,
    PolyTrait,
    PolyTraitImpl,
    SerdeUtilsFile,
    RustProperty,
    AsKeyValue,
    RustPyProject,
    RustStruct,
    RustTemplateModel,
    RustTypeAlias,
    RustStructOrSubtypeEnum,
    SlotRangeAsUnion,
    RustClassModule,
    PolyTraitProperty,
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
    "String": "String",
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
        Import(module="serde_yml", version="0.0.12", feature_flag="serde", alias="_"),
        Import(module="serde_path_to_error", version = "0.1.17", objects=[], feature_flag="serde"),

    ]
)

PYTHON_IMPORTS = Imports(
    imports = [
        Import(module="pyo3", version="0.25.0", objects=[ObjectImport(name="prelude::*"), ObjectImport(name="FromPyObject")], feature_flag="pyo3", features=["chrono"]),
        # Import(module="serde_pyobject", version="0.6.1", objects=[], feature_flag="pyo3", features=[]),
    ]
)

class SlotInlineMode(Enum):
    IDENTIFIER = "identifier" ## not inlined at all, just has the identifier
    SINGLE_VALUE = "single_value"
    MAPPING = "mapping"
    LIST = "list"


def get_key_or_identifier_slot(cls: ClassDefinition, sv: SchemaView) -> Optional[SlotDefinition]:
    induced_slots = sv.class_induced_slots(cls.name)
    for slot in induced_slots:
        if slot.identifier or slot.key:
            return slot
    return None

def get_inline_mode(s: SlotDefinition, sv: SchemaView) -> SlotInlineMode:
    class_range = s.range in sv.all_classes()
    multivalued = s.multivalued
    if not class_range:
        return SlotInlineMode.LIST if multivalued else SlotInlineMode.SINGLE_VALUE
    if s.inlined_as_list:
        return SlotInlineMode.LIST
    key_slot = get_key_or_identifier_slot(sv.get_class(s.range), sv)
    if key_slot is None:
        return SlotInlineMode.SINGLE_VALUE if not multivalued else SlotInlineMode.LIST
    elif s.inlined:
        return SlotInlineMode.MAPPING
    else:
        return SlotInlineMode.IDENTIFIER


def can_contain_reference_to_class(s: SlotDefinition, cls: ClassDefinition, sv: SchemaView) -> bool:
    ref_name = cls.name
    seen_classes = set()
    classes_to_check = [s.range]
    while len(classes_to_check) > 0:
        a_class = classes_to_check.pop()
        seen_classes.add(a_class)
        if not a_class in sv.all_classes():
            continue
        if a_class == ref_name:
            return True
        induced_class = sv.induced_class(a_class)
        for attr in induced_class.attributes.values():
            if attr.range not in seen_classes:
                classes_to_check.append(attr.range)
    return False


def get_rust_type(t: Union[TypeDefinition, type, str], sv: SchemaView, pyo3: bool = False, crate_ref: Optional[str] = None) -> str:
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
            c = sv.get_class(t)
            rsrange = get_name(c)
            descendants = sv.class_descendants(t)
            if len(descendants) > 1:
                rsrange += "OrSubtype"

    # FIXME: Raise here once we have implemented all base types
    if rsrange is None:
        rsrange = PYTHON_TO_RUST[str]
    elif rsrange in PYTHON_TO_RUST:
        rsrange = PYTHON_TO_RUST[rsrange]
    elif crate_ref is not None:
        rsrange = f"{crate_ref}::{rsrange}"
    return rsrange


def get_rust_range(cls: ClassDefinition, s: SlotDefinition, sv: SchemaView, range: Optional[str] = None) -> str:
    range = range if range is not None else s.range
    boxing_needed = False
    inline_mode = get_inline_mode(s, sv)
    base_type = get_rust_type(range, sv, True)
    all_ranges = sv.slot_range_as_union(s)
    if len(all_ranges) > 1:
        base_type = underscore(uncamelcase(cls.name)) + "_utl::" + get_name(s) + "_range"


    if inline_mode == SlotInlineMode.IDENTIFIER:
        base_type = "String"
    else:
        if can_contain_reference_to_class(s, cls, sv):
            boxing_needed = True

    if boxing_needed:
        base_type = f"Box<{base_type}>"
    
    if inline_mode == SlotInlineMode.MAPPING:
        base_type = f"HashMap<String, {base_type}>"
    elif inline_mode == SlotInlineMode.LIST or s.multivalued:
        base_type = f"Vec<{base_type}>"

    if not s.required and not s.multivalued:
        base_type = f"Option<{base_type}>"

    return base_type


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
                name=get_name(type_), type_=get_rust_type(type_.base, self.schemaview, self.pyo3), pyo3=self.pyo3
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
        type_ = get_rust_type(slot.range, self.schemaview, self.pyo3)
            
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
        slot_range_unions = []
        for a in induced_attrs:
            ranges = self.schemaview.slot_range_as_union(a)
            if len(ranges) > 1:
                slot_range_unions.append(SlotRangeAsUnion(slot_name=get_name(a), ranges=[get_rust_type(r, self.schemaview, True) for r in ranges]))
                
        cls_mod = RustClassModule(
            class_name=get_name(cls),
            class_name_snakecase= underscore(uncamelcase(cls.name)),
            slot_ranges=slot_range_unions,
        )

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
                struct_or_subtype_enum=self.gen_struct_or_subtype_enum(cls),
                class_module=cls_mod,
            ),
        )
        # merge imports
        for attr in attributes:
            res = res.merge(attr)

        res = self.after_generate_class(res, self.schemaview)
        return res
    
    def gen_struct_or_subtype_enum(self, cls: ClassDefinition) -> Optional[RustStructOrSubtypeEnum]:
        descendants = self.schemaview.class_descendants(cls.name)
        td = self.schemaview.get_type_designator_slot(cls.name)
        td_mapping = {}
        if td is not None:
            for d in descendants:
                d_class = self.schemaview.get_class(d)
                values = get_accepted_type_designator_values(self.schemaview, td, d_class)
                td_mapping[d] = values
        if len(descendants) > 1:
            return RustStructOrSubtypeEnum(
                enum_name=get_name(cls) + "OrSubtype",
                struct_names=[get_name(self.schemaview.get_class(d)) for d in descendants],
                type_designator_name=get_name(td) if td else None,
                as_key_value=get_key_or_identifier_slot(cls, self.schemaview) is not None,
                type_designators = td_mapping,
            )
        return None



    def generate_class_as_key_value(self, cls: ClassDefinition) -> Optional[AsKeyValue]:
        induced_attrs = [self.schemaview.induced_slot(sn, cls.name) for sn in self.schemaview.class_slots(cls.name)]
        key_attr = None
        value_attrs = []
        value_args_no_default = []

        for attr in induced_attrs:
            if attr.identifier:
                if key_attr is not None:
                    ## multiple identifiers --> don't know what to do!
                    return None
                key_attr = attr
            elif attr.key:
                if key_attr is not None:
                    ## multiple keys --> don't know what to do!
                    return None
                key_attr = attr
            else:
                value_attrs.append(attr)
                if attr.required and not attr.multivalued:
                    value_args_no_default.append(attr)
        if key_attr is not None:
            return AsKeyValue(
                    name=get_name(cls),
                    key_property_name=get_name(key_attr),
                    key_property_type=get_rust_type(key_attr.range, self.schemaview, self.pyo3),
                    value_property_name=get_name(value_attrs[0]),
                    value_property_type=get_rust_type(value_attrs[0].range, self.schemaview, self.pyo3),
                    can_convert_from_primitive = len(value_args_no_default) <= 1,
                    can_convert_from_empty = len(value_args_no_default) == 0,
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
        inline_mode = get_inline_mode(attr, self.schemaview)
        range = get_rust_range(cls, attr, self.schemaview)
        res = AttributeResult(
            source=attr,
            attribute=RustProperty(
                name=get_name(attr),
                inline_mode=inline_mode.value,
                type_=range,
                required=bool(attr.required),
                multivalued=True if attr.multivalued else False,
                is_key_value=is_class_range and self.generate_class_as_key_value(self.schemaview.get_class(attr.range)) is not None,
                pyo3=self.pyo3,
                serde=self.serde,
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

        poly_traits = [self.gen_poly_trait(sv.get_class(c)) for c in sv.all_classes(ordered_by=OrderedBy.INHERITANCE)]

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
            extra_files["poly"] = PolyFile(imports=imports, traits=poly_traits)
            cargo = self.generate_cargo(imports)
            pyproject = self.generate_pyproject()
            res = CrateResult(cargo=cargo, file=file, pyproject=pyproject, source=sv.schema, extra_files=extra_files)
            return res
        else:
            res = FileResult(file=file, source=sv.schema)
            return res

    def gen_poly_trait(self, cls: ClassDefinition) -> PolyTrait:
        impls = []
        class_name = get_name(cls)
        attribs = self.schemaview.class_induced_slots(cls.name)
        superclass_name = cls.is_a
        superclass = self.schemaview.get_class(superclass_name) if superclass_name is not None else None
        if superclass is not None:
            attribs_sc = self.schemaview.class_induced_slots(superclass_name)
            attribs = [a for a in attribs if a.name not in [sc.name for sc in attribs_sc]]
        
        rust_attribs = []
        for a in attribs:
            n = get_name(a)
            tp = get_rust_type(a.range, self.schemaview, self.pyo3, crate_ref="crate")
            srau = self.schemaview.slot_range_as_union(a)
            class_range = False
            has_subclasses = False
            if len(srau) == 1:
                if srau[0] in self.schemaview.all_classes():
                    has_subclasses = len(self.schemaview.class_descendants(srau[0])) > 1
                    class_range = True
                    tp = get_name(self.schemaview.get_class(srau[0]))
            rust_attribs.append(PolyTraitProperty(name=n, type_=tp, class_range=class_range and has_subclasses))
            
        for sc in self.schemaview.class_descendants(cls.name):
            impls.append(PolyTraitImpl(name=class_name, struct_name=get_name(self.schemaview.get_class(sc))))
        return PolyTrait(name=class_name, impls=impls, attrs=rust_attribs, superclass_name = get_name(superclass) if superclass is not None else None)


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
