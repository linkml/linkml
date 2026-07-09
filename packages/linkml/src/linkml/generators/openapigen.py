"""Generate OpenAPI YAML files."""

import json
import os
import re
from dataclasses import dataclass, field

import click
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, validate

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.generator import Generator, shared_arguments

SUPPORTED_OPENAPI_VERSIONS = ["3.0.3"]

openapi_generic_template = """# TODO: remove this whole comment block after processing
# This is a valid OpenAPI template to be used by the LinkML OpenAPI generator.
# Make sure to set the right OpenAPI version in the `openapi` top-level attribute.
# These are the supported OpenAPI versions: {openapi_version_list}
# It adds one (random) class of the schema as an example.
# Please adapt it to your needs and then.
# See more information in the online documentation:
#   https://linkml.io/linkml/generators/openapi.template
openapi: x.y.z
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
          description: Endpoint example involving random schema class
          content:
            application/json:
              schema:
                # TODO: remove this whole comment block after processing
                # any broken reference will cause template instantiation to fail
                # OpenAPI editors typically also report them
                $ref: '#/components/schemas/{schema_class}'
components:
  # TODO: remove this whole comment block after processing
  # any class schema provided here that is not used by at least
  # one endpoint will be eliminated from the template instantiation
  # OpenAPI editors typically also report them
  schemas:
    # TODO: remove this whole comment block after processing
    # this resource name can differ from the name in the LinkML schema
    # it must only match the corresponding endpoint `$ref` references
    {schema_class}:
      type: object
      description: Resource schema to be generated from the LinkML data model.
      # TODO: remove this whole comment block after processing
      # schema ID mismatching with provided schema will cause template
      # instantiation to fail
      x-linkml-schema: {schema_id}
      x-linkml-source: {schema_class}
"""


@dataclass
class OpenApiGenerator(Generator):
    """
    Generates OpenAPI specification YAML from a LinkML schema.

    The generator composes a user-provided OpenAPI template (containing the API header,
    paths/endpoints, and security schemes) with JSON Schema components generated from
    the LinkML schema via :class:`.JsonSchemaGenerator`. Only classes referenced by the
    template's endpoints (and their transitive dependencies) are included in the
    ``components/schemas`` section.

    Currently only one generation path is supported (others might follow):

    * **v3.0.3** — uses :class:`.JsonSchemaGenerator` and applies post-processing
      transforms (``const`` → ``enum``, nullable ``type`` lists → ``anyOf``,
      ``$defs`` → ``components/schemas``) required by OpenAPI 3.0.3.

    The OpenAPI version to be generated is obtained from the template's top-level
    attribute `openapi`.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["openapi"]
    file_extension = "yaml"
    uses_schemaloader = False

    _template: dict = field(default_factory=dict, init=False, repr=False)
    _renaming: dict[str, str] = field(default_factory=dict, init=False, repr=False)
    # Mapping of valid_formats entries to OpenAPI version strings.
    # Extend this dict when adding support for additional OpenAPI versions.
    _openapi_versions: list[str] = field(
        default_factory=lambda: SUPPORTED_OPENAPI_VERSIONS,
        init=False,
        repr=False,
    )
    # Mapping of OpenAPI version strings to validators from openapi-spec-validator.
    # Extend this dict when adding support for additional OpenAPI versions.
    _openapi_validators: dict[str, type] = field(
        default_factory=lambda: {"3.0.3": OpenAPIV30SpecValidator},
        init=False,
        repr=False,
    )

    def _find_referenced_resources(self) -> set[str]:
        """Return the set of resource names referenced by the template's endpoints."""
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
                        value = self._fix_openapi_spec_v303(value)
                    elif isinstance(value, str) and value.startswith("#/$defs/"):
                        value = value.replace("#/$defs/", "#/components/schemas/")
                    fixed_element[key] = value
        elif isinstance(element, list):
            fixed_element = []
            for item in element:
                if isinstance(item, dict | list):
                    item = self._fix_openapi_spec_v303(item)
                elif isinstance(item, str) and item.startswith("#/$defs/"):
                    item = item.replace("#/$defs/", "#/components/schemas/")
                fixed_element.append(item)
        return fixed_element

    def _rename(self, element: dict | list) -> dict | list | None:
        """
        If the resource names do not correspond the schema class names,
        then some renaming is needed so that OpenAPI resource names
        are properly referenced throughout the whole OpenAPI file.
        """
        renamed_element = None
        if isinstance(element, dict):
            renamed_element = {}
            for key, value in element.items():
                if key in self._renaming:
                    key = self._renaming[key]
                if isinstance(value, dict | list):
                    value = self._rename(value)
                elif isinstance(value, str) and value.startswith("#/components/schemas/"):
                    class_name = value[len("#/components/schemas/") :]
                    if class_name in self._renaming:
                        value = value.replace(class_name, self._renaming[class_name])
                renamed_element[key] = value
        elif isinstance(element, list):
            renamed_element = []
            for item in element:
                if isinstance(item, dict | list):
                    item = self._rename(item)
                elif isinstance(item, str) and item.startswith("#/components/schemas/"):
                    class_name = item[len("#/components/schemas/") :]
                    if class_name in self._renaming:
                        item = item.replace(class_name, self._renaming[class_name])
                renamed_element.append(item)
        return renamed_element

    def _find_references(self, element: dict | list, referenced_classes: set[str]) -> None:
        """Recursively collect all ``$ref`` target names from ``element`` into ``referenced_classes``."""
        if isinstance(element, dict):
            if "$ref" in element:
                referenced_classes.add(element["$ref"].replace("#/$defs/", ""))
            for value in element.values():
                self._find_references(value, referenced_classes)
        elif isinstance(element, list):
            for item in element:
                self._find_references(item, referenced_classes)

    def _sanitize_schemas(self, class_schemas: dict, endpoint_referenced_classes: set[str]) -> dict:
        """Remove schemas not transitively reachable from any endpoint-referenced class."""
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

    def _generate_schemas_v303(self, referenced_resource_names: set[str]) -> dict:
        """Generate component schemas for OpenAPI v3.0.3 via :class:`.JsonSchemaGenerator`."""
        resource_schemas = self._template["components"]["schemas"]
        class_schemas: dict = {}
        self._renaming = {}
        referenced_class_names = set()
        # get only the resource schemas that are really referenced from an endpoint
        for referenced_resource_name in referenced_resource_names:
            if referenced_resource_name not in resource_schemas:
                raise KeyError(
                    f"resource '{referenced_resource_name}' referenced in one of the endpoints "
                    "does not have a schema declaration"
                )
            resource_schema = resource_schemas[referenced_resource_name]
            # validate that linkml schema id is correct
            if resource_schema["x-linkml-schema"] != self.schema.id:
                raise ValueError(
                    f"Template resource '{referenced_resource_name}' declares "
                    f"x-linkml-schema '{resource_schema['x-linkml-schema']}' "
                    f"but the loaded schema has id '{self.schema.id}'"
                )
            # if resource name differs from schema class name, keep mapping
            class_name = resource_schema["x-linkml-source"]
            if referenced_resource_name != class_name:
                self._renaming[class_name] = referenced_resource_name
            referenced_class_names.add(class_name)
            json_schema = JsonSchemaGenerator(self.schema, include_null=False, top_class=class_name).generate()
            json_schema_classes = json.loads(json_schema.to_json())["$defs"]
            class_schemas = class_schemas | json_schema_classes
        if self._renaming:
            class_schemas = self._rename(class_schemas)
        class_schemas = self._sanitize_schemas(class_schemas, referenced_resource_names)
        for class_schema in class_schemas.values():
            class_schema.pop("title", None)
        class_schemas = self._fix_openapi_spec_v303(class_schemas)
        return class_schemas

    def serialize(self, template_file: str = "", **kwargs) -> str:
        """Generate an OpenAPI spec from ``template_file`` and the loaded LinkML schema."""
        if not template_file:
            raise ValueError("An OpenAPI template file is required")
        with open(template_file) as tf:
            self._template = yaml.safe_load(tf)
        # Determine the expected OpenAPI version from the provided template
        openapi_version = self._template["openapi"]
        if openapi_version not in SUPPORTED_OPENAPI_VERSIONS:
            raise ValueError(
                f"Unsupported OpenAPI version {openapi_version}. "
                + f"Only supported versions are: {','.join(self._openapi_versions)}"
            )
        validator_class = self._openapi_validators.get(openapi_version)
        if validator_class is None:
            raise ValueError(f"No validator available for OpenAPI version {openapi_version}.")
        # Validate the input template against the OpenAPI specification
        validate(self._template, cls=validator_class)
        referenced_resource_names = self._find_referenced_resources()
        if openapi_version == "3.0.3":
            class_schemas = self._generate_schemas_v303(referenced_resource_names)
        # instantiate the right resources in the OpenAPI template
        openapi_spec = self._template
        openapi_spec["components"]["schemas"] = class_schemas
        # Validate the generated output against the OpenAPI specification
        validate(openapi_spec, cls=validator_class)
        return yaml.dump(openapi_spec, sort_keys=False)

    def printout_template(self) -> str:
        """Return a generic OpenAPI template pre-filled with the first class of the schema."""
        first_class = next(iter(self.schema.classes.keys()))
        if re.search(r"[ :\d]", first_class):
            first_class = f'"{first_class}"'
        return openapi_generic_template.format(
            schema_id=self.schema.id,
            schema_class=first_class,
            openapi_version_list=",".join(self._openapi_versions),
        )


@shared_arguments(OpenApiGenerator)
@click.command(name="openapi")
@click.option(
    "--template",
    "-t",
    help="OpenAPI template - includes the header, the endpoints and the security schemes",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, template, **args):
    """Generate an OpenAPI spec with resources modelled with LinkML.
    If no OpenAPI template is provided,
    a generic one with placeholders for all the classes in the schema is printed out."""
    # if no template provided, print out a generic one with all the classes of the schema
    if not template:
        print(OpenApiGenerator(yamlfile, **args).printout_template())
        return
    print(OpenApiGenerator(yamlfile, **args).serialize(template_file=template, **args), end="")


if __name__ == "__main__":
    cli()
