"""Generate OpenAPI YAML files."""

import json
import os
from dataclasses import dataclass, field
from typing import Literal

import click
import yaml
from pydantic import BaseModel

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.generator import Generator, shared_arguments

_OPENAPI_VERSIONS = ("3.0.3", "3.1.0")


@dataclass
class OpenApiGenerator(Generator):
    """
    Generates OpenAPI specification YAML from a LinkML schema.

    The generator composes a user-provided OpenAPI template (containing the API header,
    paths/endpoints, and security schemes) with schema components generated from
    the LinkML schema. Only classes referenced by the template's endpoints (and their
    transitive dependencies) are included in the ``components/schemas`` section.

    Two generation paths are supported:

    * **v3.0.3** — uses :class:`.JsonSchemaGenerator` and applies post-processing
      transforms (``const`` → ``enum``, nullable ``type`` lists → ``anyOf``,
      ``$defs`` → ``components/schemas``) required by OpenAPI 3.0.3.
    * **v3.1.0** — uses :class:`.PydanticGenerator` to compile a Python module,
      then calls :meth:`pydantic.BaseModel.model_json_schema` on each class.
      Because OpenAPI 3.1.0 is fully aligned with JSON Schema 2020-12, no
      post-processing transforms are needed beyond rewriting ``$defs`` references
      and stripping ``linkml_meta`` annotations.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["openapi"]
    file_extension = "yaml"
    uses_schemaloader = False

    openapi_version: Literal["3.0.3", "3.1.0"] = field(default="3.0.3")

    def _find_referenced_classes(self) -> set[str]:
        """Return the set of class names referenced by the template's endpoints."""
        result = set()
        for endp_spec in self._template["paths"].values():
            for req_spec in endp_spec.values():
                if "requestBody" in req_spec and "content" in req_spec["requestBody"]:
                    for content_spec in req_spec["requestBody"]["content"].values():
                        if "$ref" in content_spec["schema"]:
                            class_name = content_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                            result.add(class_name)
                if "responses" in req_spec:
                    for response in req_spec["responses"].values():
                        if "content" in response:
                            for content_spec in response["content"].values():
                                if "$ref" in content_spec["schema"]:
                                    class_name = content_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                                    result.add(class_name)
        return result

    def _fix_openapi_spec_v303(self, element: dict | list) -> dict | list | None:
        """
        Transform JSON Schema constructs into OpenAPI v3.0.3 compatible forms:

        - ``const`` becomes ``enum`` with a single value
        - ``type`` as a list (e.g. nullable ``["string", "null"]``) becomes ``anyOf``
        - ``$ref`` paths are rewritten from ``#/$defs/`` to ``#/components/schemas/``
        """
        new_element = None
        if isinstance(element, dict):
            new_element = {}
            for key, value in element.items():
                if key == "const":
                    new_element["enum"] = [value]
                elif key == "type" and isinstance(value, list):
                    new_element["anyOf"] = [{"type": item} for item in value if item != "null"]
                else:
                    if isinstance(value, dict) or isinstance(value, list):
                        value = self._fix_openapi_spec_v303(value)
                    elif isinstance(value, str) and value.startswith("#/$defs/"):
                        value = value.replace("#/$defs/", "#/components/schemas/")
                    new_element[key] = value
        elif isinstance(element, list):
            new_element = []
            for item in element:
                if isinstance(item, dict) or isinstance(item, list):
                    item = self._fix_openapi_spec_v303(item)
                elif isinstance(item, str) and item.startswith("#/$defs/"):
                    item = item.replace("#/$defs/", "#/components/schemas/")
                new_element.append(item)
        return new_element

    def _find_references(self, element: dict | list, referenced_classes: set[str]) -> None:
        """Populate *referenced_classes* with all ``$ref`` targets found in *element*."""
        if isinstance(element, dict):
            if "$ref" in element:
                referenced_classes.add(element["$ref"].replace("#/$defs/", ""))
            for value in element.values():
                self._find_references(value, referenced_classes)
        elif isinstance(element, list):
            for item in element:
                self._find_references(item, referenced_classes)

    def _sanitize_schemas(self, class_schemas: dict, endpoint_referenced_classes: set[str]) -> dict:
        """Remove class schemas not reachable from *endpoint_referenced_classes*."""
        referenced_classes = endpoint_referenced_classes.copy()
        for class_schema in class_schemas.values():
            self._find_references(class_schema, referenced_classes)
        while set(class_schemas.keys()).difference(referenced_classes):
            class_schema_names = list(class_schemas.keys())
            for class_name in class_schema_names:
                if class_name not in referenced_classes:
                    del class_schemas[class_name]
            referenced_classes = endpoint_referenced_classes.copy()
            for class_schema in class_schemas.values():
                self._find_references(class_schema, referenced_classes)
        return class_schemas

    def _rewrite_defs_refs(self, element: dict | list) -> None:
        """
        Rewrite ``#/$defs/`` references to ``#/components/schemas/`` in-place.

        This is the only structural transformation needed for OpenAPI 3.1.0,
        since it is fully aligned with JSON Schema 2020-12.
        """
        if isinstance(element, dict):
            keys_to_update = []
            for key, value in element.items():
                if isinstance(value, str) and value.startswith("#/$defs/"):
                    keys_to_update.append((key, value.replace("#/$defs/", "#/components/schemas/")))
                elif isinstance(value, dict) or isinstance(value, list):
                    self._rewrite_defs_refs(value)
            for key, new_value in keys_to_update:
                element[key] = new_value
        elif isinstance(element, list):
            for i, item in enumerate(element):
                if isinstance(item, str) and item.startswith("#/$defs/"):
                    element[i] = item.replace("#/$defs/", "#/components/schemas/")
                elif isinstance(item, dict) or isinstance(item, list):
                    self._rewrite_defs_refs(item)

    @staticmethod
    def _strip_linkml_meta(element: dict | list) -> None:
        """Remove ``linkml_meta`` annotations recursively from Pydantic JSON Schema output."""
        if isinstance(element, dict):
            element.pop("linkml_meta", None)
            for value in element.values():
                if isinstance(value, dict) or isinstance(value, list):
                    OpenApiGenerator._strip_linkml_meta(value)
        elif isinstance(element, list):
            for item in element:
                if isinstance(item, dict) or isinstance(item, list):
                    OpenApiGenerator._strip_linkml_meta(item)

    def _validate_template(self) -> None:
        """Validate that the loaded template has the required structure."""
        if not isinstance(self._template.get("paths"), dict):
            raise ValueError("OpenAPI template is missing required 'paths' section")
        if not isinstance(self._template.get("components"), dict):
            raise ValueError("OpenAPI template is missing required 'components' section")
        if self._template["components"].get("schemas"):
            raise ValueError(
                "OpenAPI template must not contain pre-existing 'components/schemas' — "
                "they would be overwritten during generation"
            )

    def _generate_schemas_v303(self, referenced_classes: set[str]) -> dict:
        """Generate component schemas for OpenAPI v3.0.3 via :class:`.JsonSchemaGenerator`."""
        class_schemas: dict = {}
        for class_name in referenced_classes:
            json_schema = JsonSchemaGenerator(self.schema, include_null=False, top_class=class_name).generate()
            json_schema_classes = json.loads(json_schema.to_json())["$defs"]
            class_schemas = class_schemas | json_schema_classes
        class_schemas = self._sanitize_schemas(class_schemas, referenced_classes)
        for class_schema in class_schemas.values():
            class_schema.pop("title", None)
        class_schemas = self._fix_openapi_spec_v303(class_schemas)
        return class_schemas

    def _generate_schemas_v310(self, referenced_classes: set[str]) -> dict:
        """Generate component schemas for OpenAPI v3.1.0 via :class:`.PydanticGenerator`."""
        if not referenced_classes:
            return {}
        module = PydanticGenerator(self.schema).compile_module()
        pydantic_classes = {
            name: obj
            for name, obj in vars(module).items()
            if isinstance(obj, type)
            and issubclass(obj, BaseModel)
            and obj is not BaseModel
            and name in referenced_classes
        }
        top_class_name = next(iter(referenced_classes))
        top_class = pydantic_classes[top_class_name]
        full_schema = top_class.model_json_schema()
        class_schemas = full_schema.get("$defs", {})
        for name, cls in pydantic_classes.items():
            if name not in class_schemas:
                cls_schema = cls.model_json_schema()
                if "$defs" in cls_schema:
                    class_schemas.update(cls_schema["$defs"])
                cls_schema.pop("$defs", None)
                class_schemas[name] = cls_schema
        class_schemas = self._sanitize_schemas(class_schemas, referenced_classes)
        for class_schema in class_schemas.values():
            class_schema.pop("title", None)
        self._strip_linkml_meta(class_schemas)
        self._rewrite_defs_refs(class_schemas)
        return class_schemas

    def serialize(self, template_file: str = "", **kwargs) -> str:
        """
        Generate an OpenAPI specification and return it as a YAML string.

        :param template_file: Path to the OpenAPI template YAML file.
        :raises ValueError: If *template_file* is empty or the template is invalid.
        """
        if not template_file:
            raise ValueError("An OpenAPI template file is required")
        with open(template_file) as tf:
            self._template = yaml.safe_load(tf)
        self._validate_template()
        referenced_classes = self._find_referenced_classes()
        if self.openapi_version == "3.1.0":
            self._template["openapi"] = "3.1.0"
            class_schemas = self._generate_schemas_v310(referenced_classes)
        else:
            class_schemas = self._generate_schemas_v303(referenced_classes)
        self._template["components"]["schemas"] = class_schemas
        return yaml.dump(self._template, sort_keys=False)


@shared_arguments(OpenApiGenerator)
@click.command(name="openapi")
@click.option(
    "--template",
    "-t",
    required=True,
    help="OpenAPI template - includes the header, the endpoints and the security schemes",
)
@click.option(
    "--openapi-version",
    type=click.Choice(_OPENAPI_VERSIONS),
    default="3.0.3",
    show_default=True,
    help="OpenAPI specification version to generate",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, template, openapi_version, **args):
    """Generate an OpenAPI spec with resources modelled with LinkML"""
    print(
        OpenApiGenerator(yamlfile, openapi_version=openapi_version, **args).serialize(template_file=template, **args),
        end="",
    )


if __name__ == "__main__":
    cli()
