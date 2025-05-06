from typing import ClassVar, Optional

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


class Imports(Imports_, RustTemplateModel):
    template: ClassVar[str] = "imports.rs.jinja"


class RustProperty(RustTemplateModel):
    """
    A property within a rust struct
    """

    template: ClassVar[str] = "property.rs.jinja"

    name: str
    type_: str
    required: bool
    multivalued: Optional[bool] = False
    class_range: bool = False
    recursive: bool = False
    inlined: bool = False
    is_key_value: bool = False

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
    

class RustStruct(RustTemplateModel):
    """
    A struct!
    """

    template: ClassVar[str] = "struct.rs.jinja"

    name: str
    bases: Optional[list[str]] = None
    """
    Base classes to inherit from - must have entire MRO, just just immediate ancestor
    """
    properties: list[RustProperty] = Field(default_factory=list)
    unsendable: bool = False
    as_key_value: Optional[AsKeyValue] = None

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

    @field_validator("name", mode="after")
    @classmethod
    def snake_case_name(cls, value: str) -> str:
        return underscore(value)

    @field_validator("imports", mode="after")
    @classmethod
    def remove_pyo3(cls, v: Imports) -> Imports:
        """Remove pyo3, it's handled separately"""
        return Imports(imports=[i for i in v.imports if not i.module.startswith("pyo3")])

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
