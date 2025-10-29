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
from linkml_runtime.utils.formatutils import camelcase, uncamelcase, underscore
from linkml_runtime.utils.schemaview import OrderedBy, SchemaView

from linkml.generators.common.lifecycle import LifecycleMixin
from linkml.generators.common.template import ObjectImport
from linkml.generators.common.type_designators import get_accepted_type_designator_values
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
    AsKeyValue,
    ContainerType,
    Import,
    Imports,
    PolyContainersFile,
    PolyFile,
    PolyTrait,
    PolyTraitImpl,
    PolyTraitImplForSubtypeEnum,
    PolyTraitProperty,
    PolyTraitPropertyImpl,
    PolyTraitPropertyMatch,
    RustCargo,
    RustClassModule,
    RustEnum,
    RustEnumItem,
    RustFile,
    RustLibShim,
    RustProperty,
    RustPyProject,
    RustRange,
    RustStruct,
    RustStructOrSubtypeEnum,
    RustTemplateModel,
    RustTypeAlias,
    SerdeUtilsFile,
    SlotRangeAsUnion,
    StubGenBin,
    StubUtilsFile,
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
    "NaiveDate": Import(
        module="chrono", features=["serde"], version="0.4.41", objects=[ObjectImport(name="NaiveDate")]
    ),
    "NaiveDateTime": Import(
        module="chrono", features=["serde"], version="0.4.41", objects=[ObjectImport(name="NaiveDateTime")]
    ),
}

MERGE_ANNOTATION = "rust.linkml.io/generate/merge"

MERGE_IMPORTS = Imports(
    imports=[Import(module="merge", version="0.2.0", objects=[ObjectImport(name="Merge")])],
)

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
            objects=[
                ObjectImport(name="Serialize"),
                ObjectImport(name="Deserialize"),
                ObjectImport(name="de::IntoDeserializer"),
            ],
            feature_flag="serde",
        ),
        Import(module="serde-value", version="0.7.0", objects=[ObjectImport(name="Value")]),
        Import(module="serde_yml", version="0.0.12", feature_flag="serde", alias="_"),
        Import(module="serde_path_to_error", version="0.1.17", objects=[], feature_flag="serde"),
    ]
)

PYTHON_IMPORTS = Imports(
    imports=[
        Import(
            module="pyo3",
            version="0.25.0",
            objects=[ObjectImport(name="prelude::*"), ObjectImport(name="FromPyObject")],
            feature_flag="pyo3",
            features=["chrono"],
        ),
        # Import(module="serde_pyobject", version="0.6.1", objects=[], feature_flag="pyo3", features=[]),
    ]
)

STUBGEN_IMPORTS = Imports(
    imports=[
        Import(
            module="pyo3-stub-gen",
            version="0.13.1",
            objects=[
                ObjectImport(name="define_stub_info_gatherer"),
                ObjectImport(name="derive::gen_stub_pyclass"),
                ObjectImport(name="derive::gen_stub_pymethods"),
            ],
            feature_flag="stubgen",
            feature_dependencies=["pyo3"],
        ),
    ]
)


class SlotContainerMode(Enum):
    SINGLE_VALUE = "single_value"
    MAPPING = "mapping"
    LIST = "list"


class SlotInlineMode(Enum):
    INLINE = "inline"
    PRIMITIVE = "primitive"
    REFERENCE = "reference"


def get_key_or_identifier_slot(cls: ClassDefinition, sv: SchemaView) -> Optional[SlotDefinition]:
    induced_slots = sv.class_induced_slots(cls.name)
    for slot in induced_slots:
        if slot.identifier or slot.key:
            return slot
    return None


def get_identifier_slot(cls: ClassDefinition, sv: SchemaView) -> Optional[SlotDefinition]:
    induced_slots = sv.class_induced_slots(cls.name)
    for slot in induced_slots:
        if slot.identifier:
            return slot
    return None


def class_real_descendants(sv: SchemaView, class_name: str) -> list[str]:
    """Return true descendants of a class, excluding the class itself.

    Some SchemaView implementations include the class in `class_descendants`.
    We normalize here to avoid off-by-one errors when deciding if a class has
    subtypes (for OrSubtype generation and trait typing decisions).
    """
    try:
        descs = list(sv.class_descendants(class_name))
    except Exception:
        descs = []
    return [d for d in descs if d != class_name]


def has_real_subtypes(sv: SchemaView, class_name: str) -> bool:
    """True when the class has at least one real subtype (excluding itself)."""
    return len(class_real_descendants(sv, class_name)) > 0


def determine_slot_mode(s: SlotDefinition, sv: SchemaView) -> tuple[SlotContainerMode, SlotInlineMode]:
    """Return container and inline modes for a slot."""

    class_range = s.range in sv.all_classes()
    if not class_range:
        return (
            SlotContainerMode.LIST if s.multivalued else SlotContainerMode.SINGLE_VALUE,
            SlotInlineMode.PRIMITIVE,
        )

    if s.multivalued and s.inlined_as_list:
        return (SlotContainerMode.LIST, SlotInlineMode.INLINE)

    key_slot = get_key_or_identifier_slot(sv.get_class(s.range), sv)
    identifier_slot = get_identifier_slot(sv.get_class(s.range), sv)
    inlined = s.inlined
    if identifier_slot is None:
        # can only inline if identifier slot is none
        inlined = True

    if not s.multivalued:
        return (
            SlotContainerMode.SINGLE_VALUE,
            SlotInlineMode.INLINE if inlined else SlotInlineMode.REFERENCE,
        )

    if not inlined:
        return (SlotContainerMode.LIST, SlotInlineMode.REFERENCE)

    if key_slot is not None:
        return (SlotContainerMode.MAPPING, SlotInlineMode.INLINE)
    else:
        return (SlotContainerMode.LIST, SlotInlineMode.INLINE)


def can_contain_reference_to_class(s: SlotDefinition, cls: ClassDefinition, sv: SchemaView) -> bool:
    ref_name = cls.name
    seen_classes = set()
    classes_to_check = [s.range]
    while len(classes_to_check) > 0:
        a_class = classes_to_check.pop()
        seen_classes.add(a_class)
        if a_class not in sv.all_classes():
            continue
        if a_class == ref_name:
            return True
        induced_class = sv.induced_class(a_class)
        for attr in induced_class.attributes.values():
            if attr.range not in seen_classes:
                classes_to_check.append(attr.range)
    return False


def get_rust_type(
    t: Union[TypeDefinition, type, str], sv: SchemaView, pyo3: bool = False, crate_ref: Optional[str] = None
) -> str:
    """
    Get the rust type from a given linkml type
    """
    rsrange = None
    no_add_crate = False

    if isinstance(t, TypeDefinition):
        rsrange = t.base
        if rsrange is not None and rsrange not in PYTHON_TO_RUST:
            # A type like URIorCURIE which is an alias for a rust type
            rsrange = get_name(t)

        elif rsrange is None and t.typeof is not None:
            # A type with no base type,
            no_add_crate = True
            rsrange = get_rust_type(sv.get_type(t.typeof), sv, pyo3)

    elif isinstance(t, str):
        if tdef := sv.all_types().get(t, None):
            rsrange = get_rust_type(tdef, sv, pyo3)
            no_add_crate = True
        elif t in sv.all_enums():
            # Map LinkML enums to generated Rust enums rather than collapsing to String
            e = sv.get_enum(t)
            rsrange = get_name(e)
            no_add_crate = True
        elif t in sv.all_classes():
            c = sv.get_class(t)
            rsrange = get_name(c)

    # FIXME: Raise here once we have implemented all base types
    if rsrange is None:
        rsrange = PYTHON_TO_RUST[str]
    elif rsrange in PYTHON_TO_RUST:
        rsrange = PYTHON_TO_RUST[rsrange]
    elif crate_ref is not None and not no_add_crate:
        rsrange = f"{crate_ref}::{rsrange}"
    return rsrange


def get_rust_range_info(
    cls: ClassDefinition, s: SlotDefinition, sv: SchemaView, crate_ref: Optional[str] = None
) -> RustRange:
    (container_mode, inline_mode) = determine_slot_mode(s, sv)
    all_ranges = sv.slot_range_as_union(s)
    sub_ranges = [
        RustRange(
            type_="String" if inline_mode == SlotInlineMode.REFERENCE else get_rust_type(r, sv, True, crate_ref),
            is_class_range=r in sv.all_classes(),
            has_class_subtypes=has_real_subtypes(sv, r) if r in sv.all_classes() else False,
        )
        for r in all_ranges
    ]

    res = RustRange(
        optional=not s.required,
        has_default=not (s.required or False) or (s.multivalued or False),
        containerType=(
            ContainerType.LIST
            if container_mode == SlotContainerMode.LIST
            else ContainerType.MAPPING
            if container_mode == SlotContainerMode.MAPPING
            else None
        ),
        child_ranges=sub_ranges if len(sub_ranges) > 1 else None,
        box_needed=inline_mode == SlotInlineMode.INLINE and can_contain_reference_to_class(s, cls, sv),
        is_class_range=all_ranges[0] in sv.all_classes() if len(all_ranges) == 1 else False,
        is_reference=inline_mode == SlotInlineMode.REFERENCE,
        has_class_subtypes=(
            has_real_subtypes(sv, all_ranges[0])
            if (len(all_ranges) == 1 and all_ranges[0] in sv.all_classes())
            else False
        ),
        type_=(
            underscore(uncamelcase(cls.name)) + "_utl::" + get_name(s) + "_range"
            if len(sub_ranges) > 1
            else ("String" if inline_mode == SlotInlineMode.REFERENCE else get_rust_type(s.range, sv, True, crate_ref))
        ),
    )
    return res


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
    stubgen: bool = True
    """Generate pyo3-stub-gen instrumentation alongside PyO3 bindings"""
    handwritten_lib: bool = False
    """Place generated sources under src/generated and leave src/lib.rs for user code"""
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
        self.schemaview: SchemaView = SchemaView(self.schema)
        super().__post_init__()

    def _select_root_class(self, class_defs: list[ClassDefinition]) -> Optional[ClassDefinition]:
        """Return the schema-local class marked ``tree_root`` if present."""

        schema_id = getattr(self.schemaview.schema, "id", None)

        def is_local(cls: ClassDefinition) -> bool:
            if schema_id is None:
                return cls.from_schema is None
            return cls.from_schema == schema_id

        local_classes = [cls for cls in class_defs if is_local(cls) and not getattr(cls, "mixin", False)]

        for cls in local_classes:
            if getattr(cls, "tree_root", False):
                return cls

        return None

    def generate_type(self, type_: TypeDefinition) -> TypeResult:
        type_ = self.before_generate_type(type_, self.schemaview)
        res = TypeResult(
            source=type_,
            type_=RustTypeAlias(
                name=get_name(type_),
                type_=get_rust_type(type_.base, self.schemaview, self.pyo3),
                pyo3=self.pyo3,
                stubgen=self.stubgen,
            ),
            imports=self.get_imports(type_),
        )
        slot = self.after_generate_type(res, self.schemaview)
        return slot

    def generate_enum(self, enum: EnumDefinition) -> EnumResult:
        enum = self.before_generate_enum(enum, self.schemaview)
        items = [
            RustEnumItem(
                variant=get_name(pv),
                text=pv.text or name,
            )
            for name, pv in enum.permissible_values.items()
        ]
        res = EnumResult(
            source=enum,
            enum=RustEnum(
                name=get_name(enum),
                items=items,
                pyo3=self.pyo3,
                serde=self.serde,
                stubgen=self.stubgen,
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
                stubgen=self.stubgen,
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
            # Promote union across descendants for canonical union enum in base module
            ranges = []
            for r in self.schemaview.slot_range_as_union(a):
                ranges.append(r)
            for d in self.schemaview.class_descendants(cls.name):
                sdesc = self.schemaview.induced_slot(a.name, d)
                if sdesc is None:
                    continue
                for r in self.schemaview.slot_range_as_union(sdesc):
                    if r not in ranges:
                        ranges.append(r)
            if len(ranges) > 1:
                slot_range_unions.append(
                    SlotRangeAsUnion(
                        slot_name=get_name(a),
                        ranges=[get_rust_type(r, self.schemaview, True) for r in ranges],
                        stubgen=self.stubgen,
                    )
                )

        cls_mod = RustClassModule(
            class_name=get_name(cls),
            class_name_snakecase=underscore(uncamelcase(cls.name)),
            slot_ranges=slot_range_unions,
            stubgen=self.stubgen,
        )

        attributes = [self.generate_attribute(attr, cls) for attr in induced_attrs]
        attributes = self.after_generate_slots(attributes, self.schemaview)

        unsendable = any([a.range in self.schemaview.all_classes() for a in induced_attrs])
        res = ClassResult(
            source=cls,
            cls=RustStruct(
                name=get_name(cls),
                properties=[a.attribute for a in attributes],
                special_case_enabled=self.schemaview.get_uri(cls, expand=True).startswith("https://w3id.org/linkml"),
                generate_merge=MERGE_ANNOTATION in cls.annotations,
                unsendable=unsendable,
                pyo3=self.pyo3,
                serde=self.serde,
                stubgen=self.stubgen,
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
        descendants = class_real_descendants(self.schemaview, cls.name)
        td = self.schemaview.get_type_designator_slot(cls.name)
        td_mapping = {}
        if td is not None:
            for d in descendants:
                d_class = self.schemaview.get_class(d)
                values = get_accepted_type_designator_values(self.schemaview, td, d_class)
                td_mapping[d] = values
        if len(descendants) > 0:
            key_type = "String"
            key_slot = get_key_or_identifier_slot(cls, self.schemaview)
            if key_slot is not None:
                key_type = get_rust_type(key_slot.range, self.schemaview, self.pyo3)
            return RustStructOrSubtypeEnum(
                enum_name=get_name(cls) + "OrSubtype",
                struct_names=[get_name(self.schemaview.get_class(d)) for d in descendants],
                type_designator_name=get_name(td) if td else None,
                as_key_value=get_key_or_identifier_slot(cls, self.schemaview) is not None,
                type_designators=td_mapping,
                key_property_type=key_type,
            )
        return None

    def generate_class_as_key_value(self, cls: ClassDefinition) -> Optional[AsKeyValue]:
        induced_attrs = [self.schemaview.induced_slot(sn, cls.name) for sn in self.schemaview.class_slots(cls.name)]
        key_attr = None
        value_attrs = []
        value_args_no_default = []
        non_key_attrs = []

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
                non_key_attrs.append(attr)
                if not attr.multivalued:
                    value_attrs.append(attr)
                    if attr.required:
                        value_args_no_default.append(attr)
        if key_attr is not None:
            # If there is a key/identifier but no single-valued non-multivalued
            # attribute to serve as the value, do not treat this as a key/value class.
            if len(value_attrs) == 0:
                return None
            value_attr = value_attrs[0]
            simple_dict_possible = (
                len(non_key_attrs) == 1
                and not value_attr.multivalued
                and (
                    value_attr.range not in self.schemaview.all_classes()
                    or not bool(getattr(value_attr, "inlined", False))
                )
            )
            return AsKeyValue(
                name=get_name(cls),
                key_property_name=get_name(key_attr),
                key_property_type=get_rust_type(key_attr.range, self.schemaview, self.pyo3),
                value_property_name=get_name(value_attr),
                value_property_type=get_rust_type(value_attr.range, self.schemaview, self.pyo3),
                can_convert_from_primitive=simple_dict_possible,
                can_convert_from_empty=len(value_args_no_default) == 0,
                value_property_optional=not bool(value_attr.required),
                serde=self.serde,
                pyo3=self.pyo3,
                stubgen=self.stubgen,
            )
        return None

    def generate_attribute(self, attr: SlotDefinition, cls: ClassDefinition) -> AttributeResult:
        """
        Generate an attribute as a struct property
        """
        attr = self.before_generate_slot(attr, self.schemaview)
        is_class_range = attr.range in self.schemaview.all_classes()
        (container_mode, inline_mode) = determine_slot_mode(attr, self.schemaview)
        range = get_rust_range_info(cls, attr, self.schemaview)
        res = AttributeResult(
            source=attr,
            attribute=RustProperty(
                name=get_name(attr),
                inline_mode=inline_mode.value,
                alias=attr.alias if attr.alias is not None and attr.alias != get_name(attr) else None,
                generate_merge=MERGE_ANNOTATION in cls.annotations,
                container_mode=container_mode.value,
                type_=range,
                required=bool(attr.required),
                multivalued=True if attr.multivalued else False,
                is_key_value=is_class_range
                and self.generate_class_as_key_value(self.schemaview.get_class(attr.range)) is not None,
                pyo3=self.pyo3,
                serde=self.serde,
                stubgen=self.stubgen,
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
            stubgen=self.stubgen,
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

        need_merge_crate = False
        class_defs = [sv.induced_class(c) for c in sv.all_classes(ordered_by=OrderedBy.INHERITANCE)]
        root_class_def = self._select_root_class(class_defs)
        root_struct_name = get_name(root_class_def) if root_class_def is not None else None
        classes = class_defs
        for c in classes:
            if MERGE_ANNOTATION in c.annotations:
                need_merge_crate = True
                break

        classes = self.before_generate_classes(classes, sv)
        classes = [self.generate_class(c) for c in classes]
        classes = self.after_generate_classes(classes, sv)

        poly_traits = [self.gen_poly_trait(sv.get_class(c)) for c in sv.all_classes(ordered_by=OrderedBy.INHERITANCE)]

        imports = DEFAULT_IMPORTS.model_copy()
        imports += PYTHON_IMPORTS
        imports += SERDE_IMPORTS
        if self.stubgen:
            imports += STUBGEN_IMPORTS
        if need_merge_crate:
            imports += MERGE_IMPORTS
        for result in [*enums, *slots, *classes]:
            imports += result.imports

        file = RustFile(
            name=sv.schema.name,
            imports=imports,
            slots=[t.slot for t in slots],
            types=[t.type_ for t in types],
            enums=[e.enum for e in enums],
            structs=[c.cls for c in classes],
            pyo3=self.pyo3,
            serde=self.serde,
            stubgen=self.stubgen,
            handwritten_lib=self.handwritten_lib,
            root_struct_name=root_struct_name,
        )

        if mode == "crate":
            extra_files = {}
            extra_files["serde_utils"] = SerdeUtilsFile()
            extra_files["poly"] = PolyFile(imports=imports, traits=poly_traits)
            extra_files["poly_containers"] = PolyContainersFile()
            if self.stubgen:
                extra_files["stub_utils"] = StubUtilsFile()
            cargo = self.generate_cargo(imports)
            pyproject = self.generate_pyproject()
            bin_files = {}
            if self.stubgen:
                bin_files["bin/stub_gen"] = StubGenBin(crate_name=cargo.name, stubgen=self.stubgen)
            res = CrateResult(
                cargo=cargo,
                file=file,
                pyproject=pyproject,
                source=sv.schema,
                extra_files=extra_files,
                bin_files=bin_files,
            )
            return res
        else:
            # Single file: inline serde utils, and skip poly modules
            file.inline_serde_utils = True
            file.emit_poly = False
            file.serde_utils = SerdeUtilsFile()
            res = FileResult(file=file, source=sv.schema)
            return res

    def gen_poly_trait(self, cls: ClassDefinition) -> PolyTrait:
        impls = []
        class_name = get_name(cls)
        attribs = self.schemaview.class_induced_slots(cls.name)
        superclass_names = []
        if cls.is_a is not None:
            superclass_names.append(cls.is_a)
        for m in cls.mixins:
            superclass_names.append(m)

        superclasses = [self.schemaview.get_class(sn) for sn in superclass_names if sn is not None]
        for superclass in superclasses:
            attribs_sc = self.schemaview.class_induced_slots(superclass.name)
            attribs = [a for a in attribs if a.name not in [sc.name for sc in attribs_sc]]

        rust_attribs = []
        for a in attribs:
            n = get_name(a)
            base_ri = get_rust_range_info(cls, a, self.schemaview)
            promoted_ri = self.get_rust_range_info_across_descendants(cls, a)
            rust_attribs.append(PolyTraitProperty(name=n, range=base_ri, promoted_range=promoted_ri))

        subtype_impls = []
        for sc in self.schemaview.class_descendants(cls.name):
            sco = self.schemaview.get_class(sc)
            induced_slots = self.schemaview.class_induced_slots(sco.name)

            def find_slot(n: str):
                for s in induced_slots:
                    if s.name == n:
                        return s
                return None

            ptis = [
                PolyTraitPropertyImpl(
                    name=get_name(a),
                    range=get_rust_range_info(sco, find_slot(a.name), self.schemaview),
                    definition_range=self.get_rust_range_info_across_descendants(cls, a),
                    trait_range=self.get_rust_range_info_across_descendants(cls, a),
                    struct_name=get_name(sco),
                )
                for a in attribs
            ]
            impls.append(PolyTraitImpl(name=class_name, struct_name=get_name(sco), attrs=ptis))
            has_subtypes = has_real_subtypes(self.schemaview, sc)
            if has_subtypes:
                cases = [get_name(self.schemaview.get_class(x)) for x in class_real_descendants(self.schemaview, sc)]
                matches = [
                    PolyTraitPropertyMatch(
                        name=get_name(a),
                        range=self.get_rust_range_info_across_descendants(cls, a),
                        cases=cases,
                        struct_name=f"{get_name(sco)}OrSubtype",
                    )
                    for a in attribs
                ]
                subtype_impls.append(
                    PolyTraitImplForSubtypeEnum(name=class_name, enum_name=f"{get_name(sco)}OrSubtype", attrs=matches)
                )
        return PolyTrait(
            name=class_name,
            impls=impls,
            attrs=rust_attribs,
            superclass_names=[get_name(scla) for scla in superclasses],
            subtypes=subtype_impls,
        )

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
            serialized = serialized.rstrip("\n") + "\n"
            with open(output, "w") as f:
                f.write(serialized)

        return serialized

    def get_rust_range_info_across_descendants(self, cls: ClassDefinition, s: SlotDefinition) -> RustRange:
        """Compute a RustRange representing the union of a slot's ranges across a class and all its descendants.

        Container and optionality are taken from the base class slot.
        """
        sv = self.schemaview
        # Collect rust type names for all ranges across base + descendants, and remember
        # the source class name (if any) responsible for each rust type so we can
        # correctly determine subtype presence against the metamodel (using class names,
        # not rust type identifiers).
        type_names: list[str] = []
        rust_to_class: dict[str, Optional[str]] = {}

        def add_for_slot(slot_def: SlotDefinition):
            for r in sv.slot_range_as_union(slot_def):
                if r in sv.all_classes():
                    # Special-case: treat Anything/AnyValue as inline to ensure
                    # promoted unions include the corresponding variant.
                    if r in {"Anything", "AnyValue"}:
                        tname = get_rust_type(r, sv, True)
                        rust_to_class[tname] = r
                        if tname not in type_names:
                            type_names.append(tname)
                        continue
                    # Prefer concrete observations: only add String if explicitly non-inlined
                    inl = slot_def.inlined
                    inl_list = slot_def.inlined_as_list
                    if inl is True or inl_list is True:
                        tname = get_rust_type(r, sv, True)
                        rust_to_class[tname] = r
                    elif inl is False and (inl_list is False or inl_list is None):
                        tname = "String"
                        rust_to_class[tname] = None
                    else:
                        # Unknown inlining at this definition; skip adding a guess
                        continue
                else:
                    tname = get_rust_type(r, sv, True)
                    rust_to_class[tname] = None
                if tname not in type_names:
                    type_names.append(tname)

        base_slot = sv.induced_slot(s.name, cls.name)
        if base_slot is not None:
            add_for_slot(base_slot)

        # Include descendants in the class inheritance tree
        for d in sv.class_descendants(cls.name):
            ds = sv.induced_slot(s.name, d)
            if ds is not None:
                add_for_slot(ds)

        # If this is a mixin, include classes that use the mixin and their descendants
        try:
            all_classes = list(sv.all_classes())
        except Exception:
            all_classes = []
        for cname in all_classes:
            cdef = sv.get_class(cname)
            if cdef is None:
                continue
            if cls.name in (cdef.mixins or []):
                ds = sv.induced_slot(s.name, cname)
                if ds is not None:
                    add_for_slot(ds)
                for dd in sv.class_descendants(cname):
                    dslot = sv.induced_slot(s.name, dd)
                    if dslot is not None:
                        add_for_slot(dslot)

        container_mode, _ = determine_slot_mode(s, sv)
        # Optionality across descendants/mixin users: optional if not all are required
        all_required = True

        def consider_required(slot_def: SlotDefinition):
            nonlocal all_required
            if not bool(slot_def.required):
                all_required = False

        if base_slot is not None:
            consider_required(base_slot)
        for d in sv.class_descendants(cls.name):
            ds = sv.induced_slot(s.name, d)
            if ds is not None:
                consider_required(ds)
        try:
            all_classes = list(sv.all_classes())
        except Exception:
            all_classes = []
        for cname in all_classes:
            cdef = sv.get_class(cname)
            if cdef is None:
                continue
            if cls.name in (cdef.mixins or []):
                ds = sv.induced_slot(s.name, cname)
                if ds is not None:
                    consider_required(ds)
                for dd in sv.class_descendants(cname):
                    dslot = sv.induced_slot(s.name, dd)
                    if dslot is not None:
                        consider_required(dslot)
        base_optional = not all_required

        if len(type_names) > 1:
            child_ranges = [
                RustRange(
                    type_=t,
                    is_class_range=t not in ("String", "bool", "f64", "isize"),
                )
                for t in type_names
            ]
            return RustRange(
                optional=base_optional,
                has_default=base_optional or (s.multivalued or False),
                containerType=(
                    ContainerType.LIST
                    if container_mode == SlotContainerMode.LIST
                    else ContainerType.MAPPING
                    if container_mode == SlotContainerMode.MAPPING
                    else None
                ),
                child_ranges=child_ranges,
                is_class_range=False,
                is_reference=False,
                type_=underscore(uncamelcase(cls.name)) + "_utl::" + get_name(s) + "_range",
            )
        else:
            # Fall back to base definition only if nothing was observed concretely
            if len(type_names) == 0 and base_slot is not None:
                for r in sv.slot_range_as_union(base_slot):
                    if r in sv.all_classes():
                        inl = base_slot.inlined
                        inl_list = base_slot.inlined_as_list
                        if inl is True or inl_list is True:
                            tname = get_rust_type(r, sv, True)
                            if tname not in type_names:
                                type_names.append(tname)
                                rust_to_class[tname] = r
                    else:
                        tname = get_rust_type(r, sv, True)
                        if tname not in type_names:
                            type_names.append(tname)
                            rust_to_class[tname] = None
            # If still empty, fall back to original per-class range info
            if len(type_names) == 0:
                return get_rust_range_info(cls, s, sv)
            single = type_names[0]
            single_src_class = rust_to_class.get(single, None)
            return RustRange(
                optional=base_optional,
                has_default=base_optional or (s.multivalued or False),
                containerType=(
                    ContainerType.LIST
                    if container_mode == SlotContainerMode.LIST
                    else ContainerType.MAPPING
                    if container_mode == SlotContainerMode.MAPPING
                    else None
                ),
                child_ranges=None,
                is_class_range=single not in ("String", "bool", "f64", "isize"),
                is_reference=False,
                has_class_subtypes=(
                    has_real_subtypes(self.schemaview, single_src_class) if single_src_class is not None else False
                ),
                type_=single,
            )

    def write_crate(
        self, output: Optional[Path] = None, rendered: Union[FileResult, CrateResult] = None, force: bool = False
    ) -> str:
        output = self._validate_output(output, mode="crate", force=force)
        if rendered is None:
            rendered = self.render(mode="crate")

        cargo = rendered.cargo.render(self.template_environment)
        cargo_file = output / "Cargo.toml"
        self._write_text_file(cargo_file, cargo, crate_root=output)

        pyproject = rendered.pyproject.render(self.template_environment)
        pyproject_file = output / "pyproject.toml"
        self._write_text_file(pyproject_file, pyproject, crate_root=output)

        rust_file = rendered.file.render(self.template_environment)
        src_dir = output / "src"
        src_dir.mkdir(exist_ok=True)
        if self.handwritten_lib:
            generated_dir = src_dir / "generated"
            generated_dir.mkdir(exist_ok=True)
            lib_file = generated_dir / "mod.rs"
        else:
            generated_dir = src_dir
            lib_file = src_dir / "lib.rs"
        self._write_text_file(lib_file, rust_file, crate_root=output)

        for k, f in rendered.extra_files.items():
            extra_file = f.render(self.template_environment)
            extra_file_name = f"{k}.rs"
            extra_file_path = self._safe_subpath(generated_dir, extra_file_name)
            self._write_text_file(extra_file_path, extra_file, crate_root=output)

        if getattr(rendered, "bin_files", None):
            for rel_path, template in rendered.bin_files.items():
                rendered_bin = template.render(self.template_environment)
                safe_bin_base = self._safe_subpath(src_dir, rel_path)
                bin_path = safe_bin_base.with_suffix(".rs")
                self._write_text_file(bin_path, rendered_bin, crate_root=output)

        if self.handwritten_lib:
            shim_path = src_dir / "lib.rs"
            if not shim_path.exists():
                root_struct_name = getattr(rendered.file, "root_struct_name", None)
                root_struct_fn_snake = underscore(uncamelcase(root_struct_name)) if root_struct_name else None
                shim_template = RustLibShim(
                    module_name=rendered.file.name,
                    pyo3=self.pyo3,
                    serde=self.serde,
                    stubgen=self.stubgen,
                    handwritten_lib=self.handwritten_lib,
                    root_struct_name=root_struct_name,
                    root_struct_fn_snake=root_struct_fn_snake,
                )
                shim = shim_template.render(self.template_environment)
                self._write_text_file(shim_path, shim, crate_root=output)

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

    def _safe_subpath(self, base: Path, relative: Union[str, Path]) -> Path:
        """Return a path nested under base, validating it does not escape."""

        rel_path = Path(relative)
        if rel_path.is_absolute():
            raise ValueError(f"Relative path expected, got absolute path: {relative}")

        if not rel_path.parts:
            raise ValueError("Relative path must contain at least one segment")

        for part in rel_path.parts:
            if part in (".", ".."):
                raise ValueError(f"Invalid path segment: {part}")
            if "/" in part or "\\" in part:
                raise ValueError(f"Path segment must not contain separators: {part}")

        candidate = base / rel_path
        base_resolved = base.resolve()
        try:
            candidate.resolve().relative_to(base_resolved)
        except ValueError as exc:  # pragma: no cover - defensive
            raise ValueError(f"Path {candidate} escapes base directory {base}") from exc

        return candidate

    def _write_text_file(self, path: Path, content: str, *, crate_root: Path) -> None:
        """Normalize trailing newline, ensure parent dirs, and write text."""

        base_resolved = crate_root.resolve()
        try:
            path.resolve().relative_to(base_resolved)
        except ValueError as exc:
            raise ValueError(f"Path {path} escapes crate root {crate_root}") from exc

        normalized = content.rstrip("\n") + "\n"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(normalized)

    @property
    def template_environment(self) -> Environment:
        if self._environment is None:
            self._environment = RustTemplateModel.environment()
        return self._environment
