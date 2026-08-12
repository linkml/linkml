"""Generate OpenAPI v3.0.3 Specification YAML files."""

import json
import os
import re
import textwrap
from dataclasses import dataclass, field
from typing import cast

import click
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator
from openapi_spec_validator import validate as openapi_validate
from openapi_spec_validator.validation.validators import SpecValidator as OaSpecValidator
from yaml import MappingNode, ScalarNode

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator, json_schema_types
from linkml.utils.generator import Generator, shared_arguments

openapi_generic_template = """openapi: 3.0.3
# This is a valid OpenAPI template to be used by the LinkML OpenAPI generator.
# It adds one (random) class or type of the LinkML schema as an example.
# Please adapt it to your needs.
# See more information in the online documentation:
#   https://linkml.io/linkml/generators/openapi.html
info:
  title: Generic example referring in LinkML-modelled resources
  version: 0.1.0
servers:
  - url: https://example.org/
security:
  - PayloadSignature: []
paths:
  /api/endpoint:
    get:
      responses:
        '200':
          description: Endpoint example involving random data schema
          content:
            application/json:
              schema:
                # any broken reference will cause template instantiation to fail
                # OpenAPI editors typically also report them
                $ref: '#/components/schemas/{data_schema}'
components:
  # any data schema provided here that is not used by at least
  # one endpoint will be eliminated from the template instantiation
  # OpenAPI editors typically also report them
  schemas:
    # this resource name can differ from the name in the LinkML schema
    # it must only match the corresponding endpoint `$ref` references
    # it creates a mapping between names in OpenAPI and LinkML
    {data_schema}:
      type: object
      description: Resource schema to be generated from the LinkML data model.
      # schema ID mismatching with provided schema will cause template
      # instantiation to fail
      x-linkml-schema: {linkml_schema_id}
      x-linkml-source: {data_schema}
"""


@dataclass
class OpenApiGenerator(Generator):
    """
    Generates OpenAPI v3.0.3 specification YAML from a LinkML schema.

    The generator composes a user-provided OpenAPI template (containing the API header,
    paths/endpoints, and security schemes) with JSON Schema components generated from
    the LinkML schema via :class:`.JsonSchemaGenerator`. Only data schemas referenced
    by the template's endpoints (and their transitive dependencies) are included in
    the ``components/schemas`` section.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["openapi303"]
    file_extension = "yaml"
    uses_schemaloader = False

    _template: dict = field(default_factory=dict, init=False, repr=False)
    # Mapping of valid_formats entries to OpenAPI version strings.
    # Extend this dict when adding support for additional OpenAPI versions.
    _openapi_versions: dict[str, str] = field(
        default_factory=lambda: {"openapi303": "3.0.3"},
        init=False,
        repr=False,
    )
    # Mapping of OpenAPI version strings to validators from openapi-spec-validator.
    # Extend this dict when adding support for additional OpenAPI versions.
    _openapi_validators: dict[str, type[OaSpecValidator]] = field(
        default_factory=lambda: {"3.0.3": OpenAPIV30SpecValidator},
        init=False,
        repr=False,
    )

    def _validate_oad_template(
        self, oad_validator_class: type[OaSpecValidator], expected_version: str, format_name: str
    ):
        """Validate the OpenAPI template"""
        # Validate that the template declares the expected OpenAPI version
        declared_version = self._template.get("openapi")
        if declared_version != expected_version:
            raise ValueError(
                f"Template OpenAPI version is '{declared_version}', "
                f"but format '{format_name}' requires version '{expected_version}'"
            )
        # Validate the input template against the OpenAPI specification.
        # This also catches dangling $ref targets in endpoints.
        openapi_validate(self._template, cls=oad_validator_class)
        # Validation: every template schema must declare this LinkML schema.
        if "components" in self._template and "schemas" in self._template["components"]:
            for name, schema in self._template["components"]["schemas"].items():
                if "x-linkml-schema" not in schema:
                    raise KeyError(f"Template data schema '{name}' is missing required 'x-linkml-schema'")
                if schema["x-linkml-schema"] != self.schemaview.schema.id:
                    raise ValueError(
                        f"Template data schema '{name}' declares "
                        f"x-linkml-schema '{schema['x-linkml-schema']}' "
                        f"but the loaded schema has id '{self.schemaview.schema.id}'"
                    )

    def _find_referenced_schemas(self) -> set[str]:
        """Return the set of resource names referenced by the template's endpoints."""
        result = set()
        for endp_spec in self._template["paths"].values():
            for req_spec in endp_spec.values():
                if "requestBody" in req_spec and "content" in req_spec["requestBody"]:
                    for content_spec in req_spec["requestBody"]["content"].values():
                        if "$ref" in content_spec["schema"]:
                            resource_name = content_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                            result.add(resource_name)
                if "parameters" in req_spec:
                    for param_spec in req_spec["parameters"]:
                        if "$ref" in param_spec["schema"]:
                            resource_name = param_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                            result.add(resource_name)
                if "responses" in req_spec:
                    for response in req_spec["responses"].values():
                        if "content" in response:
                            for content_spec in response["content"].values():
                                if "$ref" in content_spec["schema"]:
                                    resource_name = content_spec["schema"]["$ref"].removeprefix("#/components/schemas/")
                                    result.add(resource_name)
        return result

    def _generate_type_schema(self, type_name: str) -> dict:
        """Build an OpenAPI-compatible JSON Schema for a LinkML TypeDefinition."""
        type_def = self.schemaview.get_type(type_name)
        typ, fmt = json_schema_types.get(type_def.base.lower(), ("string", None))
        schema: dict = {}
        if typ:
            schema["type"] = str(typ)
        if fmt:
            schema["format"] = str(fmt)
        if type_def.pattern:
            schema["pattern"] = str(type_def.pattern)
        if type_def.minimum_value is not None:
            schema["minimum"] = str(type_def.minimum_value)
        if type_def.maximum_value is not None:
            schema["maximum"] = str(type_def.maximum_value)
        if type_def.equals_string is not None:
            schema["const"] = str(type_def.equals_string)
        if type_def.equals_number is not None:
            schema["const"] = str(type_def.equals_number)
        if type_def.description:
            schema["description"] = str(type_def.description)
        return schema

    def _find_references(self, element: dict | list, referenced_data_schemas: set[str]) -> None:
        """Recursively collect all ``$ref`` target names from ``element`` into ``referenced_data_schemas``."""
        if isinstance(element, dict):
            if "$ref" in element:
                referenced_data_schemas.add(element["$ref"].replace("#/$defs/", ""))
            for value in element.values():
                self._find_references(value, referenced_data_schemas)
        elif isinstance(element, list):
            for item in element:
                self._find_references(item, referenced_data_schemas)

    def _fix_openapi_spec(self, element: dict | list) -> dict | list:
        """
        Transform JSON Schema constructs into OpenAPI v3.0.3 compatible forms:

        - ``const`` becomes ``enum`` with a single value (OpenAPI 3.0 doesn't support ``const``)
        - ``type`` as a list (e.g. nullable ``["string", "null"]``) becomes ``anyOf``
        - ``$ref`` paths are rewritten from ``#/$defs/`` to ``#/components/schemas/``
        """
        fixed_element = None
        if isinstance(element, dict):
            fixed_element = {}
            for key, value in element.items():
                if key == "const":
                    fixed_element["enum"] = [value]
                elif key == "type" and isinstance(value, list):
                    fixed_element["anyOf"] = [{"type": item} for item in value if item != "null"]
                else:
                    if isinstance(value, dict | list):
                        value = self._fix_openapi_spec(value)
                    elif isinstance(value, str) and value.startswith("#/$defs/"):
                        value = value.replace("#/$defs/", "#/components/schemas/")
                    fixed_element[key] = value
        elif isinstance(element, list):
            fixed_element = []
            for item in element:
                if isinstance(item, dict | list):
                    item = self._fix_openapi_spec(item)
                elif isinstance(item, str) and item.startswith("#/$defs/"):
                    item = item.replace("#/$defs/", "#/components/schemas/")
                fixed_element.append(item)
        return fixed_element

    def _rename(self, name_map: dict[str, str], element: dict | list) -> dict | list:
        """
        If the resource names do not correspond the data schema names,
        then some renaming is needed so that OpenAPI resource names
        are properly referenced throughout the whole OpenAPI file.
        """
        if isinstance(element, dict):
            renamed_element: dict | list = {}
            for key, value in element.items():
                if key in name_map:
                    key = name_map[key]
                if isinstance(value, dict | list):
                    value = self._rename(name_map, value)
                elif isinstance(value, str) and value.startswith("#/components/schemas/"):
                    data_schema_name = value[len("#/components/schemas/") :]
                    if data_schema_name in name_map:
                        value = value.replace(data_schema_name, name_map[data_schema_name])
                renamed_element[key] = value
        elif isinstance(element, list):
            renamed_element: dict | list = []
            for item in element:
                if isinstance(item, dict | list):
                    item = self._rename(name_map, item)
                elif isinstance(item, str) and item.startswith("#/components/schemas/"):
                    data_schema_name = item[len("#/components/schemas/") :]
                    if data_schema_name in name_map:
                        item = item.replace(data_schema_name, name_map[data_schema_name])
                renamed_element.append(item)
        else:
            raise TypeError(f"Unexpected type '{type(element)}', only 'dict' and 'list' supported.")
        return renamed_element

    def _sanitize_schemas(
        self, name_map: dict[str, str], openapi_schemas: dict, endpoint_ref_linkml_names: set[str]
    ) -> dict:
        """
        Prune unreachable schemas, remove redundant metadata, convert JSON Schema constructs
        to OpenAPI 3.0.3 compat, and apply any OpenAPI↔LinkML name renames.
        """
        referenced_schemas = endpoint_ref_linkml_names.copy()
        for openapi_schema in openapi_schemas.values():
            self._find_references(openapi_schema, referenced_schemas)
        while set(openapi_schemas.keys()).difference(referenced_schemas):
            openapi_schema_names = list(openapi_schemas.keys())
            for openapi_schema_name in openapi_schema_names:
                if openapi_schema_name not in referenced_schemas:
                    del openapi_schemas[openapi_schema_name]
            referenced_schemas = endpoint_ref_linkml_names.copy()
            for openapi_schema in openapi_schemas.values():
                self._find_references(openapi_schema, referenced_schemas)
        # title always duplicates the schema dict key, so it is redundant in components/schemas
        for openapi_schema in openapi_schemas.values():
            openapi_schema.pop("title", None)
        openapi_schemas = cast(dict, self._fix_openapi_spec(openapi_schemas))
        if name_map:
            openapi_schemas = cast(dict, self._rename(name_map, openapi_schemas))
        return openapi_schemas

    def _find_schemas_line(self, template_text: str) -> int:
        """Return the 0-indexed line number of the ``schemas`` key under ``components``."""
        doc = yaml.compose(template_text)
        if not isinstance(doc, MappingNode):
            raise ValueError("OpenAPI template is not a YAML mapping")
        components_node = None
        for key, value in doc.value:
            if isinstance(key, ScalarNode) and key.value == "components":
                components_node = value
                break
        if not isinstance(components_node, MappingNode):
            raise ValueError("OpenAPI template is missing a valid 'components' section")
        for key, _ in components_node.value:
            if isinstance(key, ScalarNode) and key.value == "schemas":
                return key.start_mark.line
        raise ValueError("OpenAPI template is missing 'schemas' section under 'components'")

    def serialize(self, template_file: str = "", **kwargs) -> str:
        """Generate an OpenAPI v3.0.3 spec from ``template_file`` and the loaded LinkML schema."""
        # load the template
        if not template_file:
            raise ValueError("An OpenAPI template file is required")
        with open(template_file) as tf:
            template_text = tf.read()
            self._template = yaml.safe_load(template_text)
        # determine the expected OpenAPI version from the active output format
        format_name = getattr(self, "format", self.valid_formats[0]) or self.valid_formats[0]
        expected_version = self._openapi_versions.get(format_name)
        if expected_version is None:
            raise ValueError(f"Unsupported output format '{format_name}'")

        # get the corresponding OpenAPI validator
        oad_validator_class = self._openapi_validators.get(expected_version)
        if oad_validator_class is None:
            raise ValueError(f"No validator available for OpenAPI version {expected_version}")
        # validate the OpenAPI template before further processing
        self._validate_oad_template(oad_validator_class, expected_version, format_name)
        # if no schemas to instantiate, return the template itself
        if (
            "components" not in self._template
            or "schemas" not in self._template["components"]
            or not self._template["components"]["schemas"]
        ):
            return template_text

        # Two namespaces exist: OpenAPI schema names (from the template's
        # components/schemas keys) and LinkML element names (from the LinkML schema).
        # Every schema has a name in both namespaces and the template declares the
        # mapping between them in the x-linkml-schema values; they may be identical or differ.
        # When they differ, name_map records the synonym (LinkML element name -> OpenAPI schema name).
        endpoint_ref_openapi_names = self._find_referenced_schemas()  # OpenAPI names referenced by endpoints
        openapi_schemas = self._template["components"]["schemas"]  # schemas provided by the OpenAPI template
        # collect the LinkML names referenced by endpoints (seed for sanitizing below)
        endpoint_ref_linkml_names: set[str] = {
            openapi_schemas[n]["x-linkml-source"] for n in endpoint_ref_openapi_names
        }
        # when OpenAPI and LinkML names differ, record the synonym for later renaming
        name_map: dict[str, str] = {
            openapi_schemas[n]["x-linkml-source"]: n
            for n in endpoint_ref_openapi_names
            if n != openapi_schemas[n]["x-linkml-source"]
        }

        # JsonSchemaGenerator.generate() emits every class/enum of the LinkML schema into
        # $defs. LinkML types are not part of $defs and are generated separately.
        # all_req_schemas contains all directly or transitively required schemas from
        # LinkML classes and types
        json_schema = JsonSchemaGenerator(self.schemaview.schema, include_null=False).generate()
        all_req_schemas: dict[str, dict] = json.loads(json_schema.to_json())["$defs"]
        for linkml_name in endpoint_ref_linkml_names:
            if linkml_name in self.schemaview.all_types():
                all_req_schemas[linkml_name] = self._generate_type_schema(linkml_name)

        # sanitize schemas not transitively reachable from any endpoint-referenced schema
        sanitized_data_schemas = self._sanitize_schemas(name_map, all_req_schemas, endpoint_ref_linkml_names)

        # instantiate the real OpenAPI YAML replacing the schema placeholders
        lines = template_text.splitlines(keepends=True)
        schemas_line_idx = self._find_schemas_line(template_text)
        text_before_schemas = "".join(lines[:schemas_line_idx])
        schemas_yaml = yaml.dump(sanitized_data_schemas, sort_keys=False)
        indented_schemas = textwrap.indent(schemas_yaml, "    ")
        result = text_before_schemas + "  schemas:\n" + indented_schemas

        # validate the generated output against the OpenAPI specification before returning
        openapi_validate(yaml.safe_load(result), cls=oad_validator_class)
        return result

    def printout_template(self) -> str:
        """Return a generic OpenAPI template pre-filled with the first class/type of the LinkML schema."""
        element_names = self.schemaview.all_classes().keys()
        if not element_names:
            element_names = self.schemaview.all_types().keys()
        if not element_names:
            # if no realistic schema and data can be used, put some placeholders
            return openapi_generic_template.format(
                linkml_schema_id="<LinkML Schema ID>", data_schema="<data schema name>"
            )
        first_element = next(iter(element_names))
        if re.search(r"[ :\d]", first_element):
            first_element = f'"{first_element}"'
        return openapi_generic_template.format(linkml_schema_id=self.schemaview.schema.id, data_schema=first_element)


@shared_arguments(OpenApiGenerator)
@click.command(name="openapi")
@click.option(
    "--template",
    "-t",
    help="OpenAPI v3.0.3 template - includes the header, the endpoints and the security schemes",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, template, **args):
    """Generate an OpenAPI v3.0.3 spec with resources modelled with LinkML.
    If no OpenAPI template is provided,
    a generic one with one exemplary class/type schema is printed out."""
    # if no template provided, print out a generic one
    if not template:
        print(OpenApiGenerator(yamlfile, **args).printout_template())
        return
    print(
        OpenApiGenerator(yamlfile, **args).serialize(template_file=template, **args),
        end="",
    )


if __name__ == "__main__":
    cli()
