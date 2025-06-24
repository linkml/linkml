from enum import Enum
from typing import ClassVar, List, Optional

from jinja2 import Environment, PackageLoader
from linkml_runtime.utils.formatutils import underscore
from pydantic import BaseModel, Field, computed_field, field_validator

from linkml.generators.common.template import Import as Import_
from linkml.generators.common.template import Imports as Imports_
from linkml.generators.common.template import TemplateModel, _render


class ContainerType(Enum):
    LIST = "list"
    MAPPING = "mapping"


class RustRange(BaseModel):
    optional: bool = False
    containerType: Optional[ContainerType] = None
    has_default: bool = False
    is_class_range: bool = False
    is_reference: bool = False
    box_needed: bool = False
    has_class_subtypes: bool = False
    child_ranges: Optional[List["RustRange"]] = None
    type_: str

    def type_for_field(self):
        tp = self.type_
        if self.has_class_subtypes:
            if not self.is_reference:
                tp = f"{tp}OrSubtype"
        if self.box_needed:
            tp = f"Box<{tp}>"
        if self.containerType == ContainerType.LIST:
            tp = f"Vec<{tp}>"
        elif self.containerType == ContainerType.MAPPING:
            tp = f"HashMap<String, {tp}>"
        if self.optional and self.containerType is None:
            tp = f"Option<{tp}>"
        return tp

    def type_for_trait(self, crateref: Optional[str], setter: bool = False):
        tp = self.type_
        if self.is_class_range and not self.has_class_subtypes and not setter:
            if crateref and not self.is_reference:
                tp = f"{crateref}::{tp}"
        if self.has_class_subtypes and not self.is_reference:
            tp = f"{tp}OrSubtype"
        if self.is_class_range and setter and not self.is_reference:
            tp = "E"
        convert_ref = False
        if self.containerType == ContainerType.LIST:
            if not setter:
                # tp = f"poly_containers::ListView<{tp}>"
                tp = f"impl poly_containers::SeqRef<{tp}>"
            else:
                tp = f"&Vec<{tp}>"
        elif self.containerType == ContainerType.MAPPING:
            if not setter:
                tp = f"impl poly_containers::MapRef<String,{tp}>"
            else:
                tp = f"&HashMap<String, {tp}>"
        else:
            convert_ref = True
        if not setter and convert_ref and (not self.optional or (self.is_class_range and not self.is_reference)):
            tp = f"&{tp}"
        if self.optional and self.containerType is None:
            if self.is_class_range and not self.is_reference:
                tp = f"Option<{tp}>"
            else:
                if tp == 'String':
                    tp = "Option<&str>"
                else:
                    tp = f"Option<&{tp}>"
        if tp == '&String':
            tp = '&str'
        return tp

    def type_bound_for_setter(self, crateref: Optional[str]) -> Optional[str]:
        if self.is_class_range:
            tp = self.type_
            return f"Into<{tp}>"
        return None


class RustTemplateModel(TemplateModel):
    """
    Parent class for rust template models :)
    """

    template: ClassVar[str]
    _environment: ClassVar[Environment] = Environment(
        loader=PackageLoader("linkml.generators.rustgen", "templates"), trim_blocks=True, lstrip_blocks=True
    )
    meta_exclude: ClassVar[list[str]] = None

    pyo3: bool = True
    """
    Whether pyO3 annotations should be added to generated items :)
    """
    serde: bool = False
    """
    Whether serde serialization/deserialization annotations should be added.
    """
    attributes: dict[str, str] = Field(default_factory=dict)


class PolyContainersFile(RustTemplateModel):

    template: ClassVar[str] = "poly_containers.rs.jinja"


class Import(Import_, RustTemplateModel):
    template: ClassVar[str] = "import.rs.jinja"

    version: Optional[str] = None
    """Version specifier to use in Cargo.toml"""
    features: Optional[list[str]] = None
    """Features to require in Cargo.toml"""
    ## whether this import should be behind a feature flag
    feature_flag: Optional[str] = None


class Imports(Imports_, RustTemplateModel):
    template: ClassVar[str] = "imports.rs.jinja"


class RustProperty(RustTemplateModel):
    """
    A property within a rust struct
    """

    template: ClassVar[str] = "property.rs.jinja"
    inline_mode: str
    container_mode: str
    name: str
    type_: RustRange  # might be a union type, so list length > 1
    required: bool
    multivalued: bool = False
    is_key_value: bool = False

    @computed_field
    def type_for_field(self) -> str:
        """
        The type of this field, as it would be used in a struct definition
        """
        return self.type_.type_for_field()

    @computed_field
    def hasdefault(self) -> bool:
        return self.multivalued or not self.required


class AsKeyValue(RustTemplateModel):
    """
    A key-value representation for this struct
    """

    template: ClassVar[str] = "as_key_value.rs.jinja"
    name: str
    key_property_name: str
    key_property_type: str
    value_property_name: str
    value_property_type: str
    can_convert_from_primitive: bool = False
    can_convert_from_empty: bool = False


class RustStructOrSubtypeEnum(RustTemplateModel):
    template: ClassVar[str] = "struct_or_subtype_enum.rs.jinja"
    enum_name: str
    struct_names: list[str]
    as_key_value: bool = False
    type_designator_field: Optional[str] = None
    type_designators: dict[str, str]


class SlotRangeAsUnion(RustTemplateModel):
    """
    A union of ranges!
    """

    template: ClassVar[str] = "slot_range_as_union.rs.jinja"
    slot_name: str
    ranges: list[str]


class RustClassModule(RustTemplateModel):
    class_name: str
    class_name_snakecase: str
    template: ClassVar[str] = "class_module.rs.jinja"
    slot_ranges: List[SlotRangeAsUnion]


class RustStruct(RustTemplateModel):
    """
    A struct!
    """

    template: ClassVar[str] = "struct.rs.jinja"
    class_module: Optional[RustClassModule] = None

    name: str
    bases: Optional[list[str]] = None
    """
    Base classes to inherit from - must have entire MRO, just just immediate ancestor
    """
    properties: list[RustProperty] = Field(default_factory=list)
    unsendable: bool = False
    as_key_value: Optional[AsKeyValue] = None
    struct_or_subtype_enum: Optional[RustStructOrSubtypeEnum] = None

    @computed_field()
    def property_names_and_types(self) -> dict[str, str]:
        return [(p.name, p.type_.type_for_field()) for p in self.properties]

    @computed_field()
    def property_names(self) -> list[str]:
        return [p.name for p in self.properties]


class RustEnum(RustTemplateModel):
    """
    A rust enum!
    """

    template: ClassVar[str] = "enum.rs.jinja"

    name: str
    items: list[str]


class RustTypeAlias(RustTemplateModel):
    """
    A type alias used to represent slots
    """

    template: ClassVar[str] = "typealias.rs.jinja"

    name: str
    type_: str
    description: Optional[str] = None
    multivalued: Optional[bool] = False
    class_range: bool = False
    slot_range_as_union: Optional[SlotRangeAsUnion] = None

    @field_validator("attributes", mode="before")
    @classmethod
    def attr_values_as_strings(cls, value: dict[str, any]) -> dict[str, str]:
        return {k: str(v) for k, v in value.items()}


class SerdeUtilsFile(RustTemplateModel):
    """
    A file containing utility functions for serde serialization/deserialization
    """

    template: ClassVar[str] = "serde_utils.rs.jinja"


class PolyTraitProperty(RustTemplateModel):
    template: ClassVar[str] = "poly_trait_property.rs.jinja"
    name: str
    range: RustRange

    @computed_field
    def class_range(self) -> bool:
        """
        Whether this range is a class range
        """
        return self.range.is_class_range

    @computed_field
    def type_getter(self) -> str:
        return self.range.type_for_trait(setter=False, crateref="crate")

    @computed_field
    def type_setter(self) -> str:
        return self.range.type_for_trait(setter=True, crateref="crate")

    @computed_field
    def type_bound(self) -> Optional[str]:
        """
        The type bound for the setter method
        """
        return self.range.type_bound_for_setter(crateref="crate")


class PolyTraitPropertyImpl(RustTemplateModel):
    template: ClassVar[str] = "poly_trait_property_impl.rs.jinja"
    name: str
    range: RustRange
    struct_name: str
    definition_range: RustRange

    @computed_field
    def need_option_wrap(self) -> bool:
        return self.definition_range.optional and not self.range.optional

    @computed_field
    def class_range(self) -> bool:
        """
        Whether this range is a class range
        """
        return self.range.is_class_range

    @computed_field
    def ct(self) -> str:
        """
        The container type for this range, if any
        """
        return self.range.containerType.value if self.range.containerType else "None"

    @computed_field
    def type_getter(self) -> str:
        return self.definition_range.type_for_trait(setter=False, crateref="crate")

    @computed_field
    def type_setter(self) -> str:
        return self.definition_range.type_for_trait(setter=True, crateref="crate")

    @computed_field
    def type_bound(self) -> Optional[str]:
        """
        The type bound for the setter method
        """
        return self.definition_range.type_bound_for_setter(crateref="crate")


class PolyTraitImpl(RustTemplateModel):
    """Implementation of a :class:`PolyTrait` for a particular struct."""

    template: ClassVar[str] = "poly_trait_impl.rs.jinja"
    name: str
    struct_name: str
    attrs: List[PolyTraitPropertyImpl]


class PolyTraitPropertyMatch(RustTemplateModel):
    template: ClassVar[str] = "poly_trait_property_match.rs.jinja"
    name: str
    range: RustRange
    struct_name: str
    cases: List[str]

    @computed_field
    def is_container(self) -> bool:
        """
        Whether this property is a container type
        """
        return self.range.containerType is not None

    @computed_field
    def type_getter(self) -> str:
        return self.range.type_for_trait(setter=False, crateref="crate")


class PolyTraitImplForSubtypeEnum(RustTemplateModel):
    """Trait implementation that dispatches based on subtype enums."""

    template: ClassVar[str] = "poly_trait_impl_orsubtype.rs.jinja"
    enum_name: str
    name: str
    attrs: List[PolyTraitPropertyMatch]


class PolyTrait(RustTemplateModel):
    """Definition of a polymorphic trait generated from a class hierarchy."""

    template: ClassVar[str] = "poly_trait.rs.jinja"
    name: str
    attrs: List[PolyTraitProperty]
    superclass_names: List[str]
    impls: List[PolyTraitImpl]
    subtypes: List[PolyTraitImplForSubtypeEnum]


class PolyFile(RustTemplateModel):
    """Rust file aggregating polymorphic traits."""

    template: ClassVar[str] = "poly.rs.jinja"
    imports: Imports = Imports()
    traits: List[PolyTrait]


class RustFile(RustTemplateModel):
    """
    A whole rust file!
    """

    template: ClassVar[str] = "file.rs.jinja"

    name: str
    imports: Imports = Imports()
    types: list[RustTypeAlias] = Field(default_factory=list)
    structs: list[RustStruct] = Field(default_factory=list)
    enums: list[RustEnum] = Field(default_factory=list)
    slots: list[RustTypeAlias] = Field(default_factory=list)

    @computed_field
    def struct_names(self) -> list[str]:
        """Names of all the structs we have!"""
        return [c.name for c in self.structs]


class RangeEnum(RustTemplateModel):
    """
    A range enum!
    """

    template: ClassVar[str] = "range_enum.rs.jinja"
    name: str
    type_: List[str]


class RustCargo(RustTemplateModel):
    """
    A Cargo.toml file
    """

    template: ClassVar[str] = "Cargo.toml.jinja"

    name: str
    version: str = "0.0.0"
    edition: str = "2021"
    pyo3_version: str = "0.21.1"
    imports: Imports = Imports()

    @computed_field
    def cratefeatures(self) -> dict[str, list[str]]:
        feature_flags = {}
        for i in self.imports.imports:
            assert isinstance(i, Import)
            if i.feature_flag is not None:
                if i.feature_flag not in feature_flags:
                    feature_flags[i.feature_flag] = [i.module]
                else:
                    feature_flags[i.feature_flag].append(i.module)
        return feature_flags

    @field_validator("name", mode="after")
    @classmethod
    def snake_case_name(cls, value: str) -> str:
        return underscore(value)

    def render(self, environment: Optional[Environment] = None, **kwargs) -> str:
        if environment is None:
            environment = RustTemplateModel.environment()

        fields = {**self.model_fields, **self.model_computed_fields}
        data = {k: getattr(self, k, None) for k in fields}
        # don't render the template
        imports = []
        for i in data.get("imports", []):
            imp = i.model_dump()
            imp["module"] = imp["module"].split("::")[0]
            imports.append(imp)
        data["imports"] = imports

        data = {k: _render(v, environment) for k, v in data.items()}
        template = environment.get_template(self.template)
        rendered = template.render(**data)
        return rendered


class RustPyProject(RustTemplateModel):
    """
    A pyproject.toml file to go with a maturin/pyo3 package
    """

    template: ClassVar[str] = "pyproject.toml.jinja"

    name: str
    version: str = "0.0.0"

    @field_validator("name", mode="after")
    @classmethod
    def snake_case_name(cls, value: str) -> str:
        return underscore(value)
