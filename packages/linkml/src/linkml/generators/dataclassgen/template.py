"""
Template models for dataclassgen.

These are the intermediate representation between SchemaView queries and the
jinja templates in :mod:`linkml.generators.dataclassgen.templates`, following
the architecture established by pydanticgen (see
:mod:`linkml.generators.common.template`).
"""

from typing import ClassVar

from jinja2 import Environment, PackageLoader

from linkml.generators.common.template import TemplateModel


class DataclassTemplateModel(TemplateModel):
    """Base class binding dataclassgen's template directory."""

    _environment: ClassVar[Environment] = Environment(
        loader=PackageLoader("linkml.generators.dataclassgen", "templates"), trim_blocks=True, lstrip_blocks=True
    )


class TypeClass(DataclassTemplateModel):
    """A LinkML type rendered as a python class with type_* ClassVars."""

    template: ClassVar[str] = "type.py.jinja"

    name: str
    base: str
    type_class_uri: str
    type_class_curie: str
    type_name_value: str
    type_model_uri: str


class NameClass(DataclassTemplateModel):
    """A class reference (identifier/key) type, e.g. ``PersonId(extended_str)``."""

    template: ClassVar[str] = "name_class.py.jinja"

    name: str
    base: str


class DataclassClass(DataclassTemplateModel):
    """A YAMLRoot dataclass definition."""

    template: ClassVar[str] = "class.py.jinja"

    name: str
    base: str = "YAMLRoot"
    description: str | None = None
    inherited_slots: str = ""
    class_class_uri: str
    class_class_curie: str
    class_name_value: str
    class_model_uri: str
    attributes: list[str] = []
    post_init_lines: list[str] = []


class EnumClass(DataclassTemplateModel):
    """An EnumDefinitionImpl with PermissibleValue members."""

    template: ClassVar[str] = "enum.py.jinja"

    name: str
    description: str | None = None
    permissible_values: list[str] = []


class SlotEntry(DataclassTemplateModel):
    """One entry in the module-level ``slots`` registry."""

    template: ClassVar[str] = "slot_entry.py.jinja"

    pyname: str
    uri: str
    slot_name: str
    curie: str
    model_uri: str
    domain: str
    range: str


class DataclassModule(DataclassTemplateModel):
    """The full generated module."""

    template: ClassVar[str] = "module.py.jinja"

    source_file: str
    generator_version: str
    generation_date: str | None = None
    schema_name: str
    schema_id: str
    schema_description: str = ""
    schema_license: str = ""
    metamodel_version: str
    version: str = "None"
    namespaces: list[str] = []
    default_namespace: str
    types: list[TypeClass] = []
    name_classes: list[NameClass] = []
    classes: list[DataclassClass] = []
    enums: list[EnumClass] = []
    slot_entries: list[SlotEntry] = []
