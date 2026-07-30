"""Generate OpenAPI YAML files."""

import json
import os
import re
import textwrap
from dataclasses import dataclass, field
from typing import cast

import click
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, OpenAPIV31SpecValidator
from openapi_spec_validator import validate as openapi_validate
from openapi_spec_validator.validation.validators import SpecValidator as OaSpecValidator
from pydantic import BaseModel
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT4
from yaml import MappingNode, ScalarNode

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator, json_schema_types
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.generator import Generator, shared_arguments

SUPPORTED_OPENAPI_VERSIONS = ["3.0.3", "3.1.0"]

openapi_generic_template = """# TODO: remove this whole comment block after processing
# This is a valid OpenAPI template to be used by the LinkML OpenAPI generator.
# Make sure to set the right OpenAPI version in the `openapi` top-level attribute.
# These are the supported OpenAPI versions: {openapi_version_list}
# It adds one (random) class or type of the LinkML schema as an example.
# Please adapt it to your needs.
# See more information in the online documentation:
#   https://linkml.io/linkml/generators/openapi.html
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
          description: Endpoint example involving random data schema
          content:
            application/json:
              schema:
                # TODO: remove this whole comment block after processing
                # any broken reference will cause template instantiation to fail
                # OpenAPI editors typically also report them
                $ref: '#/components/schemas/{data_schema}'
components:
  # TODO: remove this whole comment block after processing
  # any data schema provided here that is not used by at least
  # one endpoint will be eliminated from the template instantiation
  # OpenAPI editors typically also report them
  schemas:
    # TODO: remove this whole comment block after processing
    # this resource name can differ from the name in the LinkML schema
    # it must only match the corresponding endpoint `$ref` references
    # it creates a mapping between names in OpenAPI and LinkML
    {data_schema}:
      type: object
      description: Resource schema to be generated from the LinkML data model.
      # TODO: remove this whole comment block after processing
      # schema ID mismatching with provided schema will cause template
      # instantiation to fail
      x-linkml-schema: {linkml_schema_id}
      x-linkml-source: {data_schema}
"""


@dataclass
class OpenApiGenerator(Generator):
    """
    Generates OpenAPI YAML from a LinkML schema.

    The generator composes a user-provided OpenAPI template (containing the API header,
    paths/endpoints, and security schemes) with JSON Schema components generated from
    the LinkML schema via :class:`.JsonSchemaGenerator`. Only data schemas referenced
    by the template's endpoints (and their transitive dependencies) are included in
    the ``components/schemas`` section.

    Currently following generation paths are supported (others might follow):

    * **v3.0.3** — uses :class:`.JsonSchemaGenerator` and applies post-processing
      transforms (``const`` → ``enum``, nullable ``type`` lists → ``anyOf``,
      ``$defs`` → ``components/schemas``) required by OpenAPI 3.0.3.
    * **v3.1.0** — uses :class:`.PydanticGenerator` to compile a Python module,
      then calls :meth:`pydantic.BaseModel.model_json_schema` on each class.
      Because OpenAPI 3.1.0 is fully aligned with JSON Schema 2020-12, no
      post-processing transforms are needed beyond rewriting ``$defs`` references
      and stripping ``linkml_meta`` annotations.

    The OpenAPI version to be generated is obtained from the template's top-level
    attribute `openapi`.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["openapi"]
    file_extension = "yaml"
    uses_schemaloader = False

    _template: dict = field(default_factory=dict, init=False, repr=False)
    keep_unreferenced: bool = False
    inline_enums: bool = False
    # Mapping of valid_formats entries to OpenAPI version strings.
    # Extend this dict when adding support for additional OpenAPI versions.
    _openapi_versions: list[str] = field(
        default_factory=lambda: SUPPORTED_OPENAPI_VERSIONS,
        init=False,
        repr=False,
    )
    # Mapping of OpenAPI version strings to validators from openapi-spec-validator.
    # Extend this dict when adding support for additional OpenAPI versions.
    _openapi_validators: dict[str, type[OaSpecValidator]] = field(
        default_factory=lambda: {"3.0.3": OpenAPIV30SpecValidator, "3.1.0": OpenAPIV31SpecValidator},
        init=False,
        repr=False,
    )

    _openapi_version = ""  # OpenAPI version declared in the template

    def _validate_oa_template(self, oa_validator_class: type[OaSpecValidator], expected_version: str):
        """Validate the OpenAPI template"""
        # Validate the input template against the OpenAPI specification.
        # This also catches dangling $ref targets in endpoints.
        openapi_validate(self._template, cls=oa_validator_class)
        # Validation: every template schema must declare this LinkML schema.
        if "components" in self._template and "schemas" in self._template["components"]:
            for name, schema in self._template["components"]["schemas"].items():
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

    def _find_references(self, element: dict | list, referenced_schemas: set[str]) -> set[str]:
        """Recursively collect all ``$ref`` target names from ``element`` into ``referenced_data_schemas``."""
        refd_schemas = referenced_schemas.copy()
        if isinstance(element, dict):
            if "$ref" in element:
                refd_schemas.add(element["$ref"].replace("#/$defs/", ""))
            for value in element.values():
                refd_schemas = self._find_references(value, refd_schemas)
        elif isinstance(element, list):
            for item in element:
                refd_schemas = self._find_references(item, refd_schemas)
        return refd_schemas

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

    def _strip_linkml_meta(self, element: dict | list) -> dict | list:
        """Remove ``linkml_meta`` annotations recursively from Pydantic JSON Schema output."""
        if isinstance(element, dict):
            element.pop("linkml_meta", None)
            for value in element.values():
                if isinstance(value, dict) or isinstance(value, list):
                    self._strip_linkml_meta(value)
        elif isinstance(element, list):
            for item in element:
                if isinstance(item, dict) or isinstance(item, list):
                    self._strip_linkml_meta(item)
        return element

    def _rewrite_defs_refs(self, element: dict | list) -> dict | list:
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
        return element

    def _sanitize_schemas(self, name_map: dict[str, str], openapi_schemas: dict, req_linkml_names: set[str]) -> dict:
        """
        Prune unreachable schemas, remove redundant metadata, convert JSON Schema constructs
        to OpenAPI 3.0.3 compat, and apply any OpenAPI<->LinkML name renames.
        """

        referenced_schemas = req_linkml_names.copy()
        for openapi_schema in openapi_schemas.values():
            referenced_schemas = self._find_references(openapi_schema, referenced_schemas)
        if not self.keep_unreferenced:
            openapi_schema_names = list(openapi_schemas.keys())
            for openapi_schema_name in openapi_schema_names:
                if openapi_schema_name not in referenced_schemas:
                    del openapi_schemas[openapi_schema_name]
        # title always duplicates the schema dict key, so it is redundant in components/schemas
        for openapi_schema in openapi_schemas.values():
            openapi_schema.pop("title", None)
        if self._openapi_version == "3.0.3":
            openapi_schemas = cast(dict, self._fix_openapi_spec_v303(openapi_schemas))
        elif self._openapi_version == "3.1.0":
            openapi_schemas = cast(dict, self._strip_linkml_meta(openapi_schemas))
            openapi_schemas = cast(dict, self._rewrite_defs_refs(openapi_schemas))
            # OpenAPI 3.1 restricts components/schemas keys to ^[a-zA-Z0-9._-]+$
            # (no spaces). Sanitize offending schema names and rewrite every $ref.
            sanitize_map = self._sanitize_schema_names(openapi_schemas, reserved=set(name_map.values()))
            if sanitize_map:
                openapi_schemas = cast(dict, self._rename(sanitize_map, openapi_schemas))
        else:
            raise ValueError(f"OpenAPI version '{self._openapi_version}' is not supported")
        if name_map:
            openapi_schemas = cast(dict, self._rename(name_map, openapi_schemas))
        if self.inline_enums:
            openapi_schemas = self._inline_enum_schemas(openapi_schemas)
        return openapi_schemas

    # OpenAPI 3.1 schema-name pattern; keys under components/schemas must match it.
    _OPENAPI_31_NAME_RE = re.compile(r"^[a-zA-Z0-9._-]+$")

    def _sanitize_schema_names(self, openapi_schemas: dict, reserved: set[str]) -> dict[str, str]:
        """Return a map of schema names invalid under OpenAPI 3.1 to sanitized equivalents.

        OpenAPI 3.1 constrains ``components/schemas`` keys to ``^[a-zA-Z0-9._-]+$``,
        so LinkML names containing spaces (or other disallowed characters) must be
        rewritten. Any run of invalid characters collapses to a single underscore;
        uniqueness is ensured against existing and already-reserved names.
        """
        existing = set(openapi_schemas.keys()) | reserved
        name_map: dict[str, str] = {}
        for name in openapi_schemas:
            if self._OPENAPI_31_NAME_RE.match(name):
                continue
            base = re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_") or "schema"
            candidate = base
            suffix = 1
            while candidate in existing or candidate in name_map.values():
                candidate = f"{base}_{suffix}"
                suffix += 1
            name_map[name] = candidate
            existing.add(candidate)
        return name_map

    def _inline_enum_schemas(self, data_schemas: dict) -> dict:
        """Inline enum subschemas into their parents instead of separate entries."""
        enum_schemas = {
            name: schema
            for name, schema in data_schemas.items()
            if isinstance(schema, dict) and "enum" in schema and "properties" not in schema
        }
        if not enum_schemas:
            return data_schemas

        def _replace_refs(obj):
            if isinstance(obj, dict):
                if "$ref" in obj:
                    ref_name = obj["$ref"].split("/")[-1]
                    if ref_name in enum_schemas:
                        return enum_schemas[ref_name]
                return {k: _replace_refs(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_replace_refs(item) for item in obj]
            return obj

        return {k: _replace_refs(v) for k, v in data_schemas.items() if k not in enum_schemas}

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

    def _generate_schemas_v303(self, endpoint_ref_schema_names: set[str]) -> dict:
        """Generate component schemas for OpenAPI v3.0.3 via :class:`.JsonSchemaGenerator`."""
        # JsonSchemaGenerator.generate() emits every class/enum of the LinkML schema into
        # $defs. LinkML types are not part of $defs and are generated separately.
        # all_req_schemas contains all directly or transitively required schemas from
        # LinkML classes and types
        json_schema = JsonSchemaGenerator(self.schemaview.schema, include_null=False, preserve_names=True).generate()
        all_req_schemas: dict[str, dict] = json.loads(json_schema.to_json())["$defs"]
        for linkml_name in endpoint_ref_schema_names:
            if linkml_name in self.schemaview.all_types():
                all_req_schemas[linkml_name] = self._generate_type_schema(linkml_name)
        return all_req_schemas

    def _generate_schemas_v310(self, endpoint_ref_schema_names: set[str]) -> dict:
        """Generate component schemas for OpenAPI v3.1.0 via :class:`.PydanticGenerator`."""
        if not endpoint_ref_schema_names:
            return {}
        materialized_schema = self.schemaview.materialize_derived_schema()
        module = PydanticGenerator(materialized_schema, extra_fields="allow").compile_module()
        pydantic_classes = {
            name: obj
            for name, obj in vars(module).items()
            if isinstance(obj, type) and issubclass(obj, BaseModel) and obj is not BaseModel
        }
        defined_types = {name: obj for name, obj in vars(module)["linkml_meta"]["types"].items()}

        all_schemas = {}
        for name, cls in pydantic_classes.items():
            schema = cls.model_json_schema()
            if "$defs" in schema:
                all_schemas |= cls.model_json_schema()["$defs"]
        if defined_types:
            json_schema = JsonSchemaGenerator(
                self.schemaview.schema, include_null=False, preserve_names=True
            ).generate()
            all_schemas |= json.loads(json_schema.to_json())["$defs"]

        # LinkML types are not emitted as standalone Pydantic classes nor reliably as
        # JSON Schema $defs (their constraints are inlined into referencing slots).
        # Endpoint-referenced types must therefore be generated explicitly, mirroring
        # the v3.0.3 path.
        for linkml_name in endpoint_ref_schema_names:
            if linkml_name not in all_schemas and linkml_name in self.schemaview.all_types():
                all_schemas[linkml_name] = self._generate_type_schema(linkml_name)

        return all_schemas

    def _generate_schemas(self, endpoint_ref_schema_names: set[str]) -> dict:
        if self._openapi_version == "3.1.0":
            all_req_schemas = self._generate_schemas_v310(endpoint_ref_schema_names)
        else:
            all_req_schemas = self._generate_schemas_v303(endpoint_ref_schema_names)
        return all_req_schemas

    def serialize(self, template_file: str = "", **kwargs) -> str:
        """Generate OpenAPI YAML from ``template_file`` and the loaded LinkML schema."""
        # load the template
        if not template_file:
            raise ValueError("An OpenAPI template file is required")
        with open(template_file) as tf:
            template_text = tf.read()
            self._template = yaml.safe_load(template_text)
        # determine the OpenAPI version from the provided template
        self._openapi_version = self._template["openapi"]
        if self._openapi_version not in SUPPORTED_OPENAPI_VERSIONS:
            raise ValueError(
                f"Unsupported OpenAPI version {self._openapi_version}. "
                + f"Only supported versions are {','.join(self._openapi_versions)}"
            )

        # get the corresponding OpenAPI validator
        oa_validator_class = self._openapi_validators.get(self._openapi_version)
        if oa_validator_class is None:
            raise ValueError(f"No validator available for OpenAPI version {self._openapi_version}")
        # validate the OpenAPI template before further processing
        self._validate_oa_template(oa_validator_class, self._openapi_version)
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
        if self.keep_unreferenced:
            req_linkml_names: set[str] = {openapi_schemas[n]["x-linkml-source"] for n in openapi_schemas.keys()}
        else:
            req_linkml_names: set[str] = {openapi_schemas[n]["x-linkml-source"] for n in endpoint_ref_openapi_names}
        # when OpenAPI and LinkML names differ, record the synonym for later renaming.
        # The template may declare a resource name (x-linkml-source mapping) for schemas
        # referenced only by other schemas, not just those referenced directly by
        # endpoints; every declared mapping must be honoured throughout the spec.
        name_map: dict[str, str] = {
            openapi_schemas[n]["x-linkml-source"]: n
            for n in openapi_schemas
            if n != openapi_schemas[n]["x-linkml-source"]
        }

        all_req_schemas = self._generate_schemas(req_linkml_names)

        # sanitize schemas not transitively reachable from any endpoint-referenced schema
        sanitized_data_schemas = self._sanitize_schemas(name_map, all_req_schemas, req_linkml_names)

        # instantiate the real OpenAPI YAML replacing the schema placeholders
        lines = template_text.splitlines(keepends=True)
        schemas_line_idx = self._find_schemas_line(template_text)
        text_before_schemas = "".join(lines[:schemas_line_idx])
        schemas_yaml = yaml.dump(sanitized_data_schemas, sort_keys=False)
        indented_schemas = textwrap.indent(schemas_yaml, "    ")
        result = text_before_schemas + "  schemas:\n" + indented_schemas

        # Check for dangling $ref references using the referencing library
        result_obj = yaml.safe_load(result)
        schemas = result_obj.get("components", {}).get("schemas", {})
        registry = Registry().with_resources(
            (
                f"#/components/schemas/{name}",
                Resource.from_contents(schema, default_specification=DRAFT4),
            )
            for name, schema in schemas.items()
        )

        def _collect_refs(obj, refs):
            if isinstance(obj, dict):
                if "$ref" in obj and isinstance(obj["$ref"], str) and obj["$ref"].startswith("#/"):
                    refs.append(obj["$ref"])
                for v in obj.values():
                    _collect_refs(v, refs)
            elif isinstance(obj, list):
                for item in obj:
                    _collect_refs(item, refs)

        all_refs = []
        _collect_refs(result_obj, all_refs)
        dangling = []
        for ref in all_refs:
            try:
                registry.get_or_retrieve(ref)
            except Exception:
                dangling.append(ref)
        if dangling:
            raise ValueError(f"Dangling $ref in generated OpenAPI spec: {','.join(dangling)}")

        # validate the generated output against the OpenAPI specification before returning
        openapi_validate(yaml.safe_load(result), cls=oa_validator_class)
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
        return openapi_generic_template.format(
            linkml_schema_id=self.schemaview.schema.id,
            data_schema=first_element,
            openapi_version_list=",".join(self._openapi_versions),
        )


@shared_arguments(OpenApiGenerator)
@click.command(name="openapi")
@click.option(
    "--template",
    "-t",
    help="OpenAPI template - includes the header, the endpoints and the security schemes",
)
@click.option(
    "--keep-unreferenced",
    "-k",
    is_flag=True,
    default=False,
    help="Keep schemas listed in the template even if not referenced by any endpoint",
)
@click.option(
    "--inline-enums",
    "-e",
    is_flag=True,
    default=False,
    help="Inline enum subschemas into their parent schemas instead of generating separate schema entries",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, template, keep_unreferenced, inline_enums, **args):
    """Generate an OpenAPI YAML with resources modelled with LinkML.
    If no OpenAPI template is provided,
    a generic one with one exemplary class/type schema is printed out."""
    # if no template provided, print out a generic one
    if not template:
        print(OpenApiGenerator(yamlfile, **args).printout_template())
        return
    print(
        OpenApiGenerator(
            yamlfile,
            keep_unreferenced=keep_unreferenced,
            inline_enums=inline_enums,
            **args,
        ).serialize(template_file=template, **args),
        end="",
    )


if __name__ == "__main__":
    cli()
