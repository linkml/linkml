"""Validate the same instance against the JSON Schema and the SHACL shapes generated for a schema."""

import json
from typing import Any

import yaml
from jsonschema import Draft201909Validator
from pyshacl import validate
from rdflib import Graph

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from linkml_runtime import SchemaView


def as_json_ld(sv: SchemaView, obj: dict[str, Any], class_name: str) -> dict[str, Any]:
    """*obj* with an ``@type`` on it and on each inlined object: the range of its slot, unless it states one."""
    class_name = obj.get("@type", class_name)
    typed = {**obj, "@type": class_name}
    for slot in sv.class_induced_slots(class_name):
        value = obj.get(slot.name)
        if slot.range in sv.all_classes() and value is not None:
            values = [as_json_ld(sv, v, slot.range) for v in (value if isinstance(value, list) else [value])]
            typed[slot.name] = values if isinstance(value, list) else values[0]
    return typed


def without_types(obj: Any) -> Any:
    """*obj* without its ``@type`` keys."""
    if isinstance(obj, dict):
        return {k: without_types(v) for k, v in obj.items() if k != "@type"}
    if isinstance(obj, list):
        return [without_types(v) for v in obj]
    return obj


def verdicts(schema: dict[str, Any], instance: dict[str, Any], target: str) -> tuple[bool, bool]:
    """Whether the JSON Schema and the SHACL shapes generated for *schema* accept *instance* of *target*.

    For SHACL, *instance* is loaded as RDF through the generated JSON-LD context,
    and the shapes must pass meta-SHACL.
    """
    text = yaml.safe_dump(schema)
    json_schema = json.loads(JsonSchemaGenerator(text, top_class=target).serialize())
    context = json.loads(ContextGenerator(text).serialize())["@context"]
    data = {"@context": context, **as_json_ld(SchemaView(text), instance, target)}
    shapes = ShaclGenerator(text, closed=False).serialize()
    conforms, _, _ = validate(
        Graph().parse(data=json.dumps(data), format="json-ld"),
        shacl_graph=Graph().parse(data=shapes, format="turtle"),
        meta_shacl=True,
    )
    return Draft201909Validator(json_schema).is_valid(without_types(instance)), conforms
