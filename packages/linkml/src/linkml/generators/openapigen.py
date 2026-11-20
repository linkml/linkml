"""Generate OpenAPI YAML files."""

import copy
import difflib
import json
import logging
import os
import re
import textwrap
from collections.abc import Mapping
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, cast

import click
import yaml
from openapi_spec_validator import OpenAPIV30SpecValidator, OpenAPIV31SpecValidator
from openapi_spec_validator import validate as openapi_validate
from openapi_spec_validator.validation.validators import SpecValidator as OaSpecValidator
from pydantic import BaseModel
from yaml import MappingNode, ScalarNode

from linkml._version import __version__
from linkml.generators.jsonschemagen import JsonSchemaGenerator, json_schema_types
from linkml.generators.pydanticgen import PydanticGenerator
from linkml.utils.generator import (
    Generator,
    apply_config_defaults,
    config_mapping,
    read_generator_config,
    shared_arguments,
)
from linkml_runtime.linkml_model.meta import SlotDefinition

logger = logging.getLogger(__name__)

SUPPORTED_OPENAPI_VERSIONS = ["3.0.3", "3.1.0"]

# The generator reads these settings of the ``generator_args.openapi`` section itself. They are
# not options of the command, so :func:`cli` takes them out of the section before
# :func:`apply_config_defaults` applies the rest to the options.
EXPOSURE_CONFIG_KEYS = ("expose", "exclude")

# The keys that ``expose`` may hold.
EXPOSE_KEYS = frozenset({"subset", "classes"})

# The keys of one ``expose.classes`` entry that the generator reads, with the type each must
# have. The generator leaves any other key alone, because it belongs to another tool that reads
# the same file, such as a server that keeps its routing settings beside the class it serves. A
# key that looks like a misspelling of one of these, such as ``operationId``, is an error,
# because ignoring it would change the API without a message.
EXPOSE_CLASS_KEYS: dict[str, type] = {
    "path": str,
    "operation_id": str,
    "summary": str,
    "description": str,
    "crud": bool,
}

# The source that an error message names when the exposure settings have the wrong shape.
EXPOSURE_SOURCE = "generator_args.openapi"

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

# OpenAPI Schema Object keys a template placeholder is allowed to override.
#
# Various annotations can describe a schema without constraining it, so an override can
# change what a reader sees but never alter structural aspects of the schema, and never affect
# whether a payload is accepted. So any JSON body the generated schema accepted before
# an override is still accepted after it, and a body it rejected is still rejected.
#
# Structural keys (`type`, `properties`, `enum`, `required`, ...) are deliberately left
# out. Every placeholder is written `type: object` by convention, but LinkML enums and
# types generate as `type: string` -- allowing `type` through would corrupt the output
# document, still valid OpenAPI, but clients would fail on it.
OVERRIDABLE_SCHEMA_KEYS = frozenset({"description", "title", "example", "externalDocs", "deprecated"})

# Prefix of the keys that map a template placeholder onto its LinkML element
# (`x-linkml-schema`, `x-linkml-source`, and any future `x-linkml-*` key). They are
# meaningless to an API consumer, so they are stripped rather than published.
LINKML_BOOKKEEPING_PREFIX = "x-linkml-"


def _misspelt_class_key(key: str) -> str | None:
    """Return the ``expose.classes`` key that ``key`` looks like a misspelling of, or None.

    The comparison first converts ``key`` to lower case with underscores, so that
    ``operationId`` and ``operation-id`` both become ``operation_id``. It then accepts a close
    misspelling.

    >>> _misspelt_class_key("operationId")
    'operation_id'
    >>> _misspelt_class_key("summry")
    'summary'
    >>> _misspelt_class_key("descripton")  # codespell:ignore descripton
    'description'
    >>> _misspelt_class_key("related") is None
    True
    """
    spelling = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", key).replace("-", "_").lower()
    matches = difflib.get_close_matches(spelling, EXPOSE_CLASS_KEYS, n=1, cutoff=0.8)
    return matches[0] if matches else None


def exposure_settings(expose: Any, exclude: Any) -> tuple[dict[str, Any], list[str]]:
    """Check the shape of the ``expose`` and ``exclude`` settings, and return them normalised.

    This checks the shape only. It runs before any schema is loaded, so the names are checked
    against the schema later, when the template is created. It raises ``ValueError`` rather
    than a click error, so that a library caller gets the same checks, and
    :meth:`OpenApiGenerator.validate_generator_args` turns the error into a usage error.

    >>> exposure_settings({"classes": {"Risk": {"path": "/risks"}, "Hazard": None}}, "Entity")
    ({'classes': {'Risk': {'path': '/risks'}, 'Hazard': {}}}, ['Entity'])
    >>> exposure_settings({"subsets": "core"}, None)
    Traceback (most recent call last):
    ...
    ValueError: expose: unknown key 'subsets'; the keys are classes, subset

    :param expose: The ``expose`` mapping, or None when absent.
    :param exclude: The ``exclude`` list. A bare class name counts as a list of one.
    :return: ``expose`` with every class entry a mapping, and ``exclude`` as a list.
    :raises ValueError: if either has the wrong shape.
    """
    expose = dict(config_mapping(expose, "'expose'", EXPOSURE_SOURCE))
    for key in sorted(set(expose) - EXPOSE_KEYS):
        raise ValueError(f"expose: unknown key {key!r}; the keys are {', '.join(sorted(EXPOSE_KEYS))}")
    subset = expose.get("subset")
    if subset is not None and not isinstance(subset, str):
        raise ValueError(f"expose.subset: expected a subset name, found {type(subset).__name__}")
    if "classes" in expose:
        classes = {}
        for name, entry in config_mapping(expose["classes"], "'expose.classes'", EXPOSURE_SOURCE).items():
            entry = config_mapping(entry, f"'expose.classes.{name}'", EXPOSURE_SOURCE)
            for key, expected in EXPOSE_CLASS_KEYS.items():
                if key in entry and not isinstance(entry[key], expected):
                    raise ValueError(
                        f"expose.classes.{name}.{key}: expected {expected.__name__}, found {type(entry[key]).__name__}"
                    )
            if "path" in entry and not entry["path"].startswith("/"):
                raise ValueError(f"expose.classes.{name}.path: a path starts with '/', found {entry['path']!r}")
            for key in entry:
                if key in EXPOSE_CLASS_KEYS:
                    continue
                if meant := _misspelt_class_key(str(key)):
                    raise ValueError(
                        f"expose.classes.{name}.{key}: did you mean {meant!r}? gen-openapi reads "
                        f"{', '.join(EXPOSE_CLASS_KEYS)} in a class entry and leaves other keys alone"
                    )
                logger.debug(f"expose.classes.{name}.{key}: not read by gen-openapi, left for other tools")
            classes[name] = entry
        expose["classes"] = classes
    if exclude is None:
        exclude = []
    elif isinstance(exclude, str):
        # Read a YAML scalar as a list of one, as apply_config_defaults does for a repeatable option.
        exclude = [exclude]
    if not isinstance(exclude, list) or not all(isinstance(name, str) for name in exclude):
        raise ValueError(f"exclude: expected a list of class names, found {type(exclude).__name__}")
    return expose, exclude


@dataclass
class ExposedClass:
    """One class that the exposure settings expose, resolved against the schema."""

    name: str
    """The LinkML class name, which ``x-linkml-source`` carries."""
    openapi_name: str
    """The key in ``components/schemas``: the class name, changed to match the OpenAPI name pattern."""
    path: str
    """The path of the list ``GET``."""
    operation_id: str
    summary: str
    description: str | None
    """The operation's ``description``, written only when the class entry sets one."""
    crud: bool
    """False puts the class in ``components/schemas`` without a path."""
    slots: list[SlotDefinition]
    """The induced slots that become query parameters, in rank order."""


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

    A person can write the template by hand, or :meth:`create_template` can create it from
    the schema. It exposes the classes that the ``expose`` and ``exclude`` settings name.
    """

    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["openapi"]
    file_extension = "yaml"
    uses_schemaloader = False
    config_section_name = "openapi"

    _template: dict = field(default_factory=dict, init=False, repr=False)
    keep_unreferenced: bool = False
    inline_enums: bool = False
    expose: dict[str, Any] = field(default_factory=dict)
    """The classes that :meth:`create_template` exposes, as a ``subset`` and per-class ``classes`` entries."""
    exclude: list[str] = field(default_factory=list)
    """Classes :meth:`create_template` leaves out of the exposed set."""
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

    @classmethod
    def validate_generator_args(cls, args: Mapping[str, Any]) -> None:
        """Check the shape of ``expose`` and ``exclude`` before any generator is built from them.

        :param args: The merged ``generator_args.openapi`` settings.
        :raises click.UsageError: if a value has the wrong shape.
        """
        try:
            exposure_settings(args.get("expose"), args.get("exclude"))
        except ValueError as e:
            raise click.UsageError(str(e)) from e

    def _validate_oad_template(self, oad_validator_class: type[OaSpecValidator], expected_version: str):
        """Validate the OpenAPI template"""
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
                if "x-linkml-source" not in schema:
                    raise KeyError(f"Template data schema '{name}' is missing required 'x-linkml-source'")

    @staticmethod
    def _schema_refs(schema: dict | list | None) -> set[str]:
        """Return the component schema names a schema object refers to, at any depth.

        A list endpoint wraps its resource as ``type: array`` with the ``$ref`` under
        ``items``; a polymorphic one puts it under ``oneOf``, ``anyOf`` or ``allOf``.
        Those references seed generation like a top-level ``$ref`` does. References
        into other component sections (parameters, responses, ...) are not schemas
        and are left out.
        """
        prefix = "#/components/schemas/"
        if not schema:
            return set()
        return {ref.removeprefix(prefix) for ref in OpenApiGenerator._collect_refs(schema) if ref.startswith(prefix)}

    def _find_referenced_schemas(self) -> set[str]:
        """Return the set of resource names referenced by the template's endpoints."""
        result = set()
        for endp_spec in self._template["paths"].values():
            for req_spec in endp_spec.values():
                if "requestBody" in req_spec and "content" in req_spec["requestBody"]:
                    for content_spec in req_spec["requestBody"]["content"].values():
                        result |= self._schema_refs(content_spec.get("schema"))
                if "parameters" in req_spec:
                    for param_spec in req_spec["parameters"]:
                        # a $ref parameter directly references a reusable parameter object
                        # (whose schema lives inside components/parameters), so it cannot
                        # reference a component schema on its own
                        if "$ref" in param_spec:
                            continue
                        result |= self._schema_refs(param_spec.get("schema"))
                if "responses" in req_spec:
                    for response in req_spec["responses"].values():
                        if "content" in response:
                            for content_spec in response["content"].values():
                                result |= self._schema_refs(content_spec.get("schema"))
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

    def _build_reference_map(self, elem_schemas: dict) -> dict[str, set[str]]:
        """Map each schema name to the set of LinkML schema names it directly references (forward adjacency)."""
        ref_map: dict[str, set[str]] = {}
        for name, schema in elem_schemas.items():
            refs: set[str] = set()
            self._find_references(schema, refs)
            ref_map[name] = refs
        return ref_map

    def _reachable_from_seeds(self, ref_map: dict[str, set[str]], seeds: set[str]) -> set[str]:
        """Return the transitive closure of ``seeds`` over the ``$ref`` edges in ``ref_map``.

        A schema is reachable when it can be traced back, through a chain of references, to a schema referenced by the
        template endpoints. Computed in a single flood-fill pass (O(nodes + edges)); cycles are handled by the
        ``seen`` guard.
        """
        seen = set(seeds)
        stack = list(seeds)
        while stack:
            for ref in ref_map.get(stack.pop(), ()):
                if ref not in seen:
                    seen.add(ref)
                    stack.append(ref)
        return seen

    def _fix_openapi_spec_v303(self, element: dict | list) -> dict | list | None:
        """
        Transform JSON Schema constructs into OpenAPI v3.0.3 compatible forms:

        - ``const`` becomes ``enum`` with a single value
        - ``type`` as a list (e.g. nullable ``["string", "null"]``) becomes ``anyOf``
        - ``examples`` (a list) becomes ``example`` (its first element); OpenAPI 3.0 has
          no plural ``examples`` keyword on the Schema Object, only singular ``example``
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
                elif key == "examples" and isinstance(value, list):
                    if value:
                        # lossy by necessity: OpenAPI 3.0 allows only one example.
                        # assigned rather than recursed into, since an example is data,
                        # not schema -- recursing could rewrite a `const`/`type` key
                        # that happens to appear inside the example value itself
                        fixed_element["example"] = value[0]
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

    def _sanitize_schemas(self, name_map: dict[str, str], elem_schemas: dict, req_linkml_names: set[str]) -> dict:
        """
        Prune unreachable schemas, remove redundant metadata, convert JSON Schema constructs
        to OpenAPI 3.0.3 compat, and apply any OpenAPI<->LinkML name renames.
        """
        # Keep only schemas transitively reachable from the endpoint-referenced seeds.
        # The reference graph is built once and traversed in a single pass; no fixpoint
        # iteration is needed because the closure is grown outward from the seeds directly.
        ref_map = self._build_reference_map(elem_schemas)
        reachable = self._reachable_from_seeds(ref_map, req_linkml_names)
        for elem_schema_name in list(elem_schemas.keys()):
            if elem_schema_name not in reachable:
                del elem_schemas[elem_schema_name]
        # title always duplicates the schema dict key, so it is redundant in components/schemas
        for elem_schema in elem_schemas.values():
            elem_schema.pop("title", None)
        if self._openapi_version == "3.0.3":
            elem_schemas = cast(dict, self._fix_openapi_spec_v303(elem_schemas))
        elif self._openapi_version == "3.1.0":
            elem_schemas = cast(dict, self._strip_linkml_meta(elem_schemas))
            elem_schemas = cast(dict, self._rewrite_defs_refs(elem_schemas))
            # OpenAPI 3.1 restricts components/schemas keys to ^[a-zA-Z0-9._-]+$
            # (no spaces). Sanitize offending schema names and rewrite every $ref.
            sanitize_map = self._sanitize_schema_names(elem_schemas, reserved=set(name_map.values()))
            if sanitize_map:
                elem_schemas = cast(dict, self._rename(sanitize_map, elem_schemas))
        else:
            raise ValueError(f"OpenAPI version '{self._openapi_version}' is not supported")
        if self.inline_enums:
            # inline before renaming so the enum/type guard matches LinkML names,
            # not the (possibly renamed) OpenAPI schema names
            elem_schemas = self._inline_enum_schemas(elem_schemas, req_linkml_names)
        if name_map:
            elem_schemas = cast(dict, self._rename(name_map, elem_schemas))
        return elem_schemas

    # OpenAPI 3.1 schema-name pattern; keys under components/schemas must match it.
    _OPENAPI_31_NAME_RE = re.compile(r"^[a-zA-Z0-9._-]+$")

    @classmethod
    def _openapi_name(cls, name: str) -> str:
        """Change a LinkML name to match the pattern of an OpenAPI ``components/schemas`` key.

        Each run of characters outside the pattern becomes one underscore.

        >>> OpenApiGenerator._openapi_name("Foo Bar")
        'Foo_Bar'
        """
        return re.sub(r"[^a-zA-Z0-9._-]+", "_", name).strip("_") or "schema"

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
            base = self._openapi_name(name)
            candidate = base
            suffix = 1
            while candidate in existing or candidate in name_map.values():
                candidate = f"{base}_{suffix}"
                suffix += 1
            name_map[name] = candidate
            existing.add(candidate)
        return name_map

    def _inline_enum_schemas(self, data_schemas: dict, endpoint_schemas: set[str] | None = None) -> dict:
        """Inline enum subschemas into their parents instead of separate entries.

        ``endpoint_schemas`` holds the LinkML names referenced by the template's endpoints;
        those enums keep their standalone entry because removing it would leave a dangling
        endpoint ``$ref``.
        """
        endpoint_schemas = endpoint_schemas or set()
        enum_schemas = {
            name: schema
            for name, schema in data_schemas.items()
            if isinstance(schema, dict)
            and "enum" in schema
            and "properties" not in schema
            and name not in self.schemaview.all_types()
            and name not in endpoint_schemas
        }
        if not enum_schemas:
            return data_schemas

        def _replace_refs(obj):
            if isinstance(obj, dict):
                if "$ref" in obj:
                    ref_name = obj["$ref"].split("/")[-1]
                    if ref_name in enum_schemas:
                        # inline the enum definition, but preserve any sibling keywords
                        # placed next to the ``$ref`` (e.g. a slot-level ``description``).
                        # A sibling value overrides the enum's own only when it carries
                        # information: an empty/blank value must not eclipse a meaningful
                        # one from either side.
                        inlined = deepcopy(enum_schemas[ref_name])
                        for key, value in obj.items():
                            if key == "$ref":
                                continue
                            value = _replace_refs(value)
                            if value or key not in inlined or not inlined[key]:
                                inlined[key] = value
                        return inlined
                return {k: _replace_refs(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_replace_refs(item) for item in obj]
            return obj

        return {k: _replace_refs(v) for k, v in data_schemas.items() if k not in enum_schemas}

    def _apply_template_overrides(self, elem_schemas: dict, openapi_schemas: dict) -> None:
        """Overlay template-declared annotations onto the generated schemas, in place.

        The LinkML-derived value is the default; where a template placeholder explicitly
        declares an annotation key, that value takes precedence. Only the keys in
        :data:`OVERRIDABLE_SCHEMA_KEYS` and ``x-`` vendor extensions are overlaid, so a
        placeholder can annotate a resource but never alter its generated structure.

        Both mappings are keyed by OpenAPI name, so this must run after
        :meth:`_sanitize_schemas` has applied any OpenAPI<->LinkML renames. Template
        entries whose schema was pruned are simply absent from ``elem_schemas`` and are
        skipped.
        """
        for name, elem_schema in elem_schemas.items():
            template_schema = openapi_schemas.get(name)
            if not isinstance(template_schema, dict):
                continue
            for key, value in template_schema.items():
                if key.startswith(LINKML_BOOKKEEPING_PREFIX):
                    continue
                if key in OVERRIDABLE_SCHEMA_KEYS or key.startswith("x-"):
                    # copy: a template may share one value between placeholders via a
                    # YAML anchor, and yaml.dump would re-emit a shared object as an anchor
                    elem_schema[key] = copy.deepcopy(value)

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

    @staticmethod
    def _collect_refs(obj: dict | list) -> list[str]:
        """Recursively collect every internal ``$ref`` target string found in ``obj``."""
        refs: list[str] = []
        if isinstance(obj, dict):
            ref = obj.get("$ref")
            if isinstance(ref, str) and ref.startswith("#/"):
                refs.append(ref)
            for value in obj.values():
                refs.extend(OpenApiGenerator._collect_refs(value))
        elif isinstance(obj, list):
            for item in obj:
                refs.extend(OpenApiGenerator._collect_refs(item))
        return refs

    def _generate_schemas_v303(self, endpoint_ref_schema_names: set[str]) -> dict:
        """Generate component schemas for OpenAPI v3.0.3 via :class:`.JsonSchemaGenerator`."""
        # JsonSchemaGenerator.generate() emits every class/enum of the LinkML schema into
        # $defs. LinkML types are not part of $defs and are generated separately.
        # all_req_schemas contains all directly or transitively required schemas from
        # LinkML classes and types
        # not_closed=True is deliberate: APIs are extended backwards-compatibly by
        # adding attributes to existing objects, which additionalProperties=False
        # blocks. Stated explicitly rather than inherited from the generator default,
        # which follows the metamodel and closes classes with no `extra_slots`.
        json_schema = JsonSchemaGenerator(
            self.schemaview.schema, include_null=False, preserve_names=True, not_closed=True
        ).generate()
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
            # not_closed=True is deliberate, mirroring the v3.0.3 path: APIs are extended
            # backwards-compatibly by adding attributes to existing objects, which
            # additionalProperties=False blocks. The generated class schemas above are open
            # (extra_fields="allow"); this JsonSchema merge must not clobber them with the
            # metamodel-default closed class schemas.
            json_schema = JsonSchemaGenerator(
                self.schemaview.schema, include_null=False, preserve_names=True, not_closed=True
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
        oad_validator_class = self._openapi_validators.get(self._openapi_version)
        if oad_validator_class is None:
            raise ValueError(f"No validator available for OpenAPI version {self._openapi_version}")
        # validate the OpenAPI template before further processing
        self._validate_oad_template(oad_validator_class, self._openapi_version)
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

        # template-declared annotations override the LinkML-derived ones, where given
        self._apply_template_overrides(sanitized_data_schemas, openapi_schemas)

        # instantiate the real OpenAPI YAML replacing the schema placeholders
        lines = template_text.splitlines(keepends=True)
        schemas_line_idx = self._find_schemas_line(template_text)
        text_before_schemas = "".join(lines[:schemas_line_idx])
        schemas_yaml = yaml.dump(sanitized_data_schemas, sort_keys=False)
        indented_schemas = textwrap.indent(schemas_yaml, "    ")
        result = text_before_schemas + "  schemas:\n" + indented_schemas

        # detect and report dangling references
        result_obj = yaml.safe_load(result)
        # resolve every internal $ref against its own section: a ref of the form
        # #/components/<section>/<name> must point at an existing <name> in that section
        all_refs: list[str] = []
        components = result_obj.get("components", {})
        for ref in self._collect_refs(result_obj):
            if not ref.startswith("#/components/"):
                continue
            try:
                _, __, section_name, target = ref.split("/", 3)
            except ValueError:
                all_refs.append(ref)
                continue
            section = components.get(section_name, {})
            if not isinstance(section, dict) or target not in section:
                all_refs.append(ref)
        if all_refs:
            raise ValueError(f"Dangling $ref in generated OpenAPI spec: {','.join(sorted(set(all_refs)))}")

        # validate the generated output against the OpenAPI specification before returning
        openapi_validate(result_obj, cls=oad_validator_class)
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

    def _subset_members(self, subset_name: str) -> tuple[set[str], set[str]]:
        """Return the names of the classes and of the slots tagged ``in_subset`` with ``subset_name``.

        This method reads ``in_subset`` on every class and slot. ``SchemaView.get_elements_by_subset``,
        which #4103 proposes for #2432, does the same, and this method is the one place to call it
        from once it is merged.

        :raises ValueError: if the schema declares no subset of that name.
        """
        sv = self.schemaview
        if subset_name not in sv.all_subsets():
            declared = ", ".join(sorted(sv.all_subsets())) or "none"
            raise ValueError(f"expose.subset: the schema declares no subset {subset_name!r}; it declares {declared}")
        classes = {name for name, cls in sv.all_classes().items() if subset_name in cls.in_subset}
        slots = {name for name, slot in sv.all_slots().items() if subset_name in slot.in_subset}
        return classes, slots

    def _exposed_classes(self) -> list[ExposedClass]:
        """Resolve the exposed set from ``expose`` and ``exclude`` against the schema.

        The set is the subset's classes, plus the classes named under ``expose.classes``, minus
        ``exclude``, minus abstract and mixin classes. The abstract and mixin filter applies to
        what the subset contributes. A class named under ``expose.classes`` is exposed even when
        it is abstract or a mixin, because a person chose it by name: a listing of an abstract
        class returns the records of its subclasses, and a schema may give a mixin records of its
        own. With neither ``subset`` nor ``classes``, every class that is neither abstract nor a
        mixin is exposed. The subset's members come first, in schema order, and then the classes
        named under ``expose.classes``, in the order the settings give them. When the subset tags
        slots, the parameters of the subset's classes narrow to those slots, and a class named
        from outside the subset keeps all its slots.

        :raises ValueError: if a name is not in the schema, a class is both exposed and excluded,
            or two classes share a path.
        """
        expose, exclude = exposure_settings(self.expose, self.exclude)
        all_classes = self.schemaview.all_classes()
        explicit: dict[str, dict] = expose.get("classes", {})
        for name in [*explicit, *exclude]:
            if name not in all_classes:
                raise ValueError(f"expose: the schema has no class {name!r}")
        if contradictory := [name for name in explicit if name in exclude]:
            raise ValueError(f"expose: {', '.join(contradictory)} named both in expose.classes and in exclude")
        subset_name = expose.get("subset")
        if subset_name is not None:
            candidates, subset_slots = self._subset_members(subset_name)
        else:
            candidates, subset_slots = (set(all_classes) if not explicit else set()), set()
        entries: dict[str, dict] = {}
        for name, cls in all_classes.items():
            if name in candidates and name not in exclude and not cls.abstract and not cls.mixin:
                entries[name] = {}
        for name, entry in explicit.items():
            entries[name] = {**entries.get(name, {}), **entry}
        # When the subset tags at least one slot, narrow the parameters of the subset's classes to
        # those slots. A class named from outside the subset keeps all its slots, because the
        # subset says nothing about them.
        narrow_to = subset_name if subset_slots else None
        exposed = [
            self._exposed_class(name, entry, narrow_to if name in candidates else None)
            for name, entry in entries.items()
        ]
        paths: dict[str, str] = {}
        for cls in exposed:
            if cls.crud and cls.path in paths:
                raise ValueError(f"expose: {paths[cls.path]} and {cls.name} share the path {cls.path}")
            paths[cls.path] = cls.name
        return exposed

    def _exposed_class(self, name: str, entry: Mapping[str, Any], narrow_to: str | None) -> ExposedClass:
        """Resolve one exposed class, with each value from its entry, or else from the derived default.

        The derived defaults are the path ``/<lowercase class>``, the operation id
        ``list_<lowercase class>`` and the summary ``Get <Class>``. The description has no
        default, because the class's description in the schema would drift once copied into a
        template. The slots are the class's induced slots. When ``narrow_to`` is given, only the
        slots it tags through ``in_subset`` are kept. They come in ``rank`` order, and slots
        without a rank follow in schema order.
        """
        # Convert the name to a plain str, because yaml.dump writes the metamodel's name classes
        # as Python tags.
        name = str(name)
        openapi_name = self._openapi_name(name)
        slots = self.schemaview.class_induced_slots(name)
        if narrow_to is not None:
            slots = [slot for slot in slots if narrow_to in slot.in_subset]
        slots.sort(key=lambda slot: (slot.rank is None, slot.rank or 0))
        return ExposedClass(
            name=name,
            openapi_name=openapi_name,
            path=entry.get("path", f"/{openapi_name.lower()}"),
            operation_id=entry.get("operation_id", f"list_{openapi_name.lower()}"),
            summary=entry.get("summary", f"Get {name}"),
            description=entry.get("description"),
            crud=entry.get("crud", True),
            slots=slots,
        )

    def _parameter_type(self, slot: SlotDefinition) -> str:
        """Return the ``schema.type`` of the query parameter for ``slot``.

        A reference to a class is passed as the identifier, and an enum as the text of a
        permissible value, so both are strings. A type maps through its base type, as the JSON
        Schema generator maps it. A multivalued slot takes one value per request.
        """
        if slot.range in self.schemaview.all_types():
            base = self.schemaview.induced_type(slot.range).base or ""
            return json_schema_types.get(base.lower(), ("string", None))[0]
        return "string"

    def _class_parameters(self, exposed: ExposedClass) -> list[dict]:
        """Return the query parameters of the class's list ``GET``, one per slot.

        A parameter holds structure only: ``in``, ``name``, ``required``, ``schema.type`` and
        ``x-linkml-source: <Class>.<slot>``. The ``name`` is the slot's ``alias`` when it has
        one, and the slot name otherwise, because the generated schema names the property the
        same way. The template copies no description, enum value or default from the schema,
        because a copy would drift from it. ``x-linkml-source`` says where a later pass at
        instantiation can find them.
        """
        return [
            {
                "in": "query",
                "name": str(slot.alias or slot.name),
                "required": False,
                "schema": {"type": self._parameter_type(slot)},
                "x-linkml-source": f"{exposed.name}.{slot.name}",
            }
            for slot in exposed.slots
        ]

    def _template_info(self) -> dict[str, str]:
        """Return the ``info`` object from the schema's metadata."""
        schema = self.schemaview.schema
        info = {"title": str(schema.title or schema.name), "version": str(schema.version or "0.1.0")}
        if schema.description:
            info["description"] = str(schema.description)
        return info

    def create_template(self, openapi_version: str = SUPPORTED_OPENAPI_VERSIONS[0]) -> str:
        """Return an OpenAPI template that exposes the classes ``expose`` and ``exclude`` resolve to.

        The template holds structure only:

        * ``info``, from the schema's metadata;
        * one list ``GET`` for each exposed class with ``crud`` on, with a query parameter for
          each of the class's slots, typed from the slot's range;
        * one placeholder in ``components/schemas`` for each exposed class.

        :meth:`serialize` generates the component schemas, with their descriptions, enum values
        and defaults, from the schema when the template is instantiated, so the template cannot
        drift from the schema. The template is validated before it is returned, so it
        instantiates without further editing.

        :param openapi_version: The OpenAPI version the template declares.
        """
        if openapi_version not in SUPPORTED_OPENAPI_VERSIONS:
            raise ValueError(
                f"Unsupported OpenAPI version {openapi_version}. "
                + f"Only supported versions are {','.join(self._openapi_versions)}"
            )
        schema_id = str(self.schemaview.schema.id)
        paths: dict[str, dict] = {}
        schemas: dict[str, dict] = {}
        for cls in self._exposed_classes():
            schemas[cls.openapi_name] = {"type": "object", "x-linkml-schema": schema_id, "x-linkml-source": cls.name}
            if not cls.crud:
                continue
            operation: dict[str, Any] = {"summary": cls.summary}
            if cls.description is not None:
                operation["description"] = cls.description
            operation["operationId"] = cls.operation_id
            if parameters := self._class_parameters(cls):
                operation["parameters"] = parameters
            operation["responses"] = {
                "200": {
                    "description": f"A list of {cls.name}",
                    "content": {
                        "application/json": {
                            "schema": {"type": "array", "items": {"$ref": f"#/components/schemas/{cls.openapi_name}"}}
                        }
                    },
                }
            }
            paths[cls.path] = {"get": operation}
        document = {
            "openapi": openapi_version,
            "info": self._template_info(),
            "paths": paths,
            "components": {"schemas": schemas},
        }
        self._template = document
        self._validate_oad_template(self._openapi_validators[openapi_version], openapi_version)
        header = f"# OpenAPI template created by gen-openapi --create-template from {schema_id}\n"
        return header + yaml.dump(document, sort_keys=False)


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
@click.option(
    "--create-template",
    is_flag=True,
    default=False,
    help="Print an OpenAPI template that exposes the classes named under "
    "'generator_args: {openapi: {expose: ..., exclude: ...}}' in the config file, instead of "
    "instantiating a template. Without a config file, every class that is neither abstract nor "
    "a mixin is exposed. It cannot be given with --template.",
)
@click.option(
    "--openapi-version",
    type=click.Choice(SUPPORTED_OPENAPI_VERSIONS),
    default=SUPPORTED_OPENAPI_VERSIONS[0],
    show_default=True,
    help="The OpenAPI version that a created template declares",
)
@click.option(
    "--config-file",
    "-C",
    type=click.File("rb"),
    help="Path to a YAML config file supplying defaults under "
    "'generator_args: {openapi: {template: ...}}'. Keys are this command's own option "
    "names with dashes as underscores; explicit command-line options always take "
    "precedence over the config file. The same section carries the nested 'expose' and "
    "'exclude' settings that --create-template reads.",
)
@click.version_option(__version__, "-V", "--version")
@click.pass_context
def cli(
    ctx,
    yamlfile,
    template,
    keep_unreferenced,
    inline_enums,
    create_template=False,
    openapi_version=SUPPORTED_OPENAPI_VERSIONS[0],
    config_file=None,
    **args,
):
    """Generate an OpenAPI YAML with resources modelled with LinkML.
    If no OpenAPI template is provided,
    a generic one with one exemplary class/type schema is printed out.
    With --create-template, it prints a template for the classes that the config file exposes."""
    config = read_generator_config(config_file, OpenApiGenerator.config_section_name)
    # The generator reads the settings in EXPOSURE_CONFIG_KEYS itself. They are not options of
    # this command, so apply_config_defaults would warn that each is an unknown key. Take them
    # out of the config before it is applied, and add them to args after.
    exposure = {key: value for key, value in config.items() if key in EXPOSURE_CONFIG_KEYS}
    config = {key: value for key, value in config.items() if key not in EXPOSURE_CONFIG_KEYS}
    apply_config_defaults(ctx, config, args)
    args.update(exposure)
    OpenApiGenerator.validate_generator_args(args)
    # apply_config_defaults writes each option the config file sets into args, even an option
    # that this function names as a parameter. Move those values to the parameters, so that the
    # code below reads them there and passes no option to the generator twice.
    template = args.pop("template", template)
    keep_unreferenced = args.pop("keep_unreferenced", keep_unreferenced)
    inline_enums = args.pop("inline_enums", inline_enums)
    create_template = args.pop("create_template", create_template)
    openapi_version = args.pop("openapi_version", openapi_version)
    # Refuse a --template given on the command line, which asks this run to instantiate it. A
    # template named in the config file is allowed, because it names the template that a later
    # run instantiates, which is often the file this run creates.
    if create_template and ctx.get_parameter_source("template") is click.ParameterSource.COMMANDLINE:
        raise click.UsageError("--template and --create-template cannot be given together")
    if create_template:
        print(OpenApiGenerator(yamlfile, **args).create_template(openapi_version), end="")
        return
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
