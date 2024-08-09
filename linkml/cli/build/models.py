from __future__ import annotations

from enum import Enum
from typing import Any, ClassVar, Dict, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, ValidationInfo, field_validator

metamodel_version = "None"
version = "None"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="allow",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )

    @field_validator("*", mode="before")
    @classmethod
    def _unnest_identifier(cls, val: Any, info: ValidationInfo):
        """
        If a slot is inlined as a dict/simple dict, and is being passed to us with without the value
        of that slot set, fill it in from the key (field name)

        eg if we have a field like

        ``field_name: Dict[str, IDClass]``

        and are given

        ``{'id_value': {'some_other_value': 'who_knows'}}``

        and there is some required identifier/key slot ``id_slot``, we return

        ``{'id_value': {'id_slot': 'id_value', 'some_other_value': 'who_knows'}}``
        """
        if (
            identifier_slot := getattr(cls.model_fields[info.field_name], "json_schema_extra")
            .get("linkml_meta", {})
            .get("identifier_slot", None)
        ) is not None:
            if isinstance(val, dict):
                for key, inner_val in val.items():
                    if not isinstance(inner_val, dict):
                        continue
                    if identifier_slot not in inner_val:
                        inner_val[identifier_slot] = key
        return val


class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_prefix": "linkml-build-schema/",
        "default_range": "string",
        "description": 'schema for the tables in pyproject.toml under "tool.linkml" '
        "that\n"
        "are used by the build commands\n",
        "id": "linkml-build-schema",
        "imports": ["linkml:types"],
        "name": "linkml-build-schema",
        "source_file": "./build_schema.yaml",
    }
)


class HookTypes(str, Enum):
    # python.module:function
    module = "module"
    # python code literal
    python = "python"
    # shell script
    shell = "shell"


class LinkmlConfig(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    schema_: Optional[Dict[str, Union[str, Schema]]] = Field(
        None,
        alias="schema",
        json_schema_extra={
            "linkml_meta": {"domain_of": ["Linkml"], "identifier_slot": "schema_name", "inlined_as": "simple_dict"}
        },
    )
    generate: Optional[Generate] = Field(
        None, alias="generate", json_schema_extra={"linkml_meta": {"domain_of": ["Linkml"]}}
    )
    build: Optional[Dict[str, SchemaBuildConfig]] = Field(
        None,
        alias="build",
        json_schema_extra={
            "linkml_meta": {"domain_of": ["Linkml"], "identifier_slot": "schema_name", "inlined_as": "dict"}
        },
    )


class Schema(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    schema_name: str = Field(
        ...,
        alias="schema_name",
        json_schema_extra={"linkml_meta": {"domain_of": ["Schema", "SchemaBuildConfig"], "key": True}},
    )
    schema_path: Optional[str] = Field(
        None, alias="schema_path", json_schema_extra={"linkml_meta": {"domain_of": ["Schema"]}}
    )


class SchemaBuildConfig(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    schema_name: str = Field(
        ...,
        alias="schema_name",
        json_schema_extra={"linkml_meta": {"domain_of": ["Schema", "SchemaBuildConfig"], "key": True}},
    )
    global_: Optional[AnonymousGeneratorConfig] = Field(
        None, alias="global", json_schema_extra={"linkml_meta": {"domain_of": ["SchemaBuildConfig", "Generate"]}}
    )
    generator_config: Optional[Dict[str, GeneratorConfig]] = Field(
        None,
        alias="generator_config",
        json_schema_extra={
            "linkml_meta": {
                "domain_of": ["SchemaBuildConfig"],
                "identifier_slot": "generator_name",
                "inlined_as": "dict",
            }
        },
    )


class Generate(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    global_: Optional[AnonymousGeneratorConfig] = Field(
        None, alias="global", json_schema_extra={"linkml_meta": {"domain_of": ["SchemaBuildConfig", "Generate"]}}
    )


class AnonymousGeneratorConfig(ConfiguredBaseModel):
    """
    Settings for a general generator without one being specified,
    used for global configs

    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    enable: Optional[bool] = Field(
        False,
        alias="enable",
        json_schema_extra={"linkml_meta": {"domain_of": ["AnonymousGeneratorConfig"], "ifabsent": "false"}},
    )
    output_path: Optional[str] = Field(
        None, alias="output_path", json_schema_extra={"linkml_meta": {"domain_of": ["AnonymousGeneratorConfig"]}}
    )
    pre_build: Optional[str] = Field(
        None,
        alias="pre_build",
        json_schema_extra={
            "linkml_meta": {
                "any_of": [{"range": "string"}, {"range": "BuildHook"}],
                "domain_of": ["AnonymousGeneratorConfig"],
            }
        },
    )
    post_build: Optional[str] = Field(
        None,
        alias="post_build",
        json_schema_extra={
            "linkml_meta": {
                "any_of": [{"range": "string"}, {"range": "BuildHook"}],
                "domain_of": ["AnonymousGeneratorConfig"],
            }
        },
    )


class GeneratorConfig(AnonymousGeneratorConfig):
    """
    Settings for an individual generator, either global or per schema.
    Individual settings are variable and depending on the specific generator,
    so this is intended to be an \"open\" schema where generator-specific
    options are ass passed as \"extra\" values.

    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    generator_name: str = Field(
        ...,
        alias="generator_name",
        json_schema_extra={"linkml_meta": {"domain_of": ["GeneratorConfig"], "identifier": True}},
    )
    enable: Optional[bool] = Field(
        False,
        alias="enable",
        json_schema_extra={"linkml_meta": {"domain_of": ["AnonymousGeneratorConfig"], "ifabsent": "false"}},
    )
    output_path: Optional[str] = Field(
        None, alias="output_path", json_schema_extra={"linkml_meta": {"domain_of": ["AnonymousGeneratorConfig"]}}
    )
    pre_build: Optional[str] = Field(
        None,
        alias="pre_build",
        json_schema_extra={
            "linkml_meta": {
                "any_of": [{"range": "string"}, {"range": "BuildHook"}],
                "domain_of": ["AnonymousGeneratorConfig"],
            }
        },
    )
    post_build: Optional[str] = Field(
        None,
        alias="post_build",
        json_schema_extra={
            "linkml_meta": {
                "any_of": [{"range": "string"}, {"range": "BuildHook"}],
                "domain_of": ["AnonymousGeneratorConfig"],
            }
        },
    )


class BuildHook(ConfiguredBaseModel):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "linkml-build-schema"})

    hook_type: HookTypes = Field(
        "module",
        alias="hook_type",
        json_schema_extra={"linkml_meta": {"domain_of": ["BuildHook"], "ifabsent": "string(module)", "key": True}},
    )
    hook_value: Optional[str] = Field(
        None, alias="hook_value", json_schema_extra={"linkml_meta": {"domain_of": ["BuildHook"]}}
    )


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Linkml.model_rebuild()
Schema.model_rebuild()
SchemaBuildConfig.model_rebuild()
Generate.model_rebuild()
AnonymousGeneratorConfig.model_rebuild()
GeneratorConfig.model_rebuild()
BuildHook.model_rebuild()
