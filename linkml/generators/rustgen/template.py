from typing import ClassVar, Optional, List

from jinja2 import Environment, PackageLoader
from linkml_runtime.utils.formatutils import underscore
from pydantic import Field, computed_field, field_validator, BaseModel

from linkml.generators.common.template import Import as Import_
from linkml.generators.common.template import Imports as Imports_
from linkml.generators.common.template import TemplateModel, _render


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
    name: str
    type_: str # might be a union type, so list length > 1
    required: bool
    multivalued: bool = False
    is_key_value: bool = False

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
    class_module : Optional[RustClassModule] = None

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
        return [(p.name, p.type_) for p in self.properties]

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
