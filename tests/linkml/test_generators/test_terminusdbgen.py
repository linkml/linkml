import json

import pytest
from click.testing import CliRunner

from linkml.generators.terminusdbgen import XSD_TRANSLATE, TerminusdbGenerator, cli
from linkml.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import SlotDefinition

SIMPLE_SCHEMA = """\
id: https://example.org/test
name: test_schema
title: Test Schema
description: A test schema for TerminusDB generation

prefixes:
  linkml: https://w3id.org/linkml/
  xsd: http://www.w3.org/2001/XMLSchema#

types:
  string:
    base: str
    uri: xsd:string
  integer:
    base: int
    uri: xsd:integer
  boolean:
    base: Bool
    uri: xsd:boolean

classes:
  Person:
    description: A human being
    slots:
      - name
      - age

  Employee:
    is_a: Person
    description: A person with a job
    slots:
      - employer

slots:
  name:
    range: string
    required: true
    description: The name of the entity
  age:
    range: integer
  employer:
    range: string
"""


def _generate(schema) -> list[dict]:
    """Serialize a schema with the TerminusDB generator and return parsed JSON."""
    return json.loads(TerminusdbGenerator(schema).serialize())


def test_context_document():
    """First document must be a valid TerminusDB @context."""
    docs = _generate(SIMPLE_SCHEMA)
    ctx = docs[0]
    assert ctx["@type"] == "@context"
    assert ctx["@schema"].endswith("#")
    assert ctx["@base"].endswith("/")
    assert ctx["@documentation"]["@title"] == "Test Schema"
    assert "test schema" in ctx["@documentation"]["@description"].lower()


def test_class_type_and_id():
    docs = _generate(SIMPLE_SCHEMA)
    person = next(d for d in docs if d.get("@id") == "Person")
    assert person["@type"] == "Class"


def test_class_description():
    docs = _generate(SIMPLE_SCHEMA)
    person = next(d for d in docs if d.get("@id") == "Person")
    assert person["@documentation"]["@comment"] == "A human being"


def test_inheritance():
    docs = _generate(SIMPLE_SCHEMA)
    employee = next(d for d in docs if d.get("@id") == "Employee")
    assert "Person" in employee["@inherits"]


def test_abstract_class():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Thing", slots=[])
    sb.schema.classes["Thing"].abstract = True
    docs = _generate(sb.schema)
    thing = next(d for d in docs if d.get("@id") == "Thing")
    assert "@abstract" in thing


def test_required_slot_is_plain_range():
    docs = _generate(SIMPLE_SCHEMA)
    person = next(d for d in docs if d.get("@id") == "Person")
    assert person["name"] == "xsd:string"


def test_optional_slot_has_optional_wrapper():
    docs = _generate(SIMPLE_SCHEMA)
    person = next(d for d in docs if d.get("@id") == "Person")
    assert person["age"] == {"@type": "Optional", "@class": "xsd:integer"}


def test_multivalued_set():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    tags = SlotDefinition(name="tags", range="string", multivalued=True)
    sb.add_class("Item", slots=[tags])
    docs = _generate(sb.schema)
    item = next(d for d in docs if d.get("@id") == "Item")
    assert item["tags"]["@type"] == "Set"


def test_multivalued_list():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    items = SlotDefinition(name="items", range="string", multivalued=True, inlined_as_list=True)
    sb.add_class("Container", slots=[items])
    docs = _generate(sb.schema)
    container = next(d for d in docs if d.get("@id") == "Container")
    assert container["items"]["@type"] == "List"


def test_slot_description_in_documentation():
    docs = _generate(SIMPLE_SCHEMA)
    person = next(d for d in docs if d.get("@id") == "Person")
    assert person["@documentation"]["@properties"]["name"] == "The name of the entity"


@pytest.mark.parametrize(
    "xsd_uri,expected",
    [
        ("xsd:int", "xsd:integer"),
        ("xsd:float", "xsd:double"),
        ("xsd:language", "xsd:string"),
        ("xsd:date", "xsd:dateTime"),
        ("xsd:time", "xsd:dateTime"),
    ],
)
def test_xsd_translation(xsd_uri, expected):
    assert XSD_TRANSLATE[xsd_uri] == expected


def test_class_range_uses_camelcase():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_class("Address", slots=[])
    ref = SlotDefinition(name="home_address", range="Address", required=True)
    sb.add_class("Person", slots=[ref])
    docs = _generate(sb.schema)
    person = next(d for d in docs if d.get("@id") == "Person")
    assert person["home_address"] == "Address"


def test_unsupported_xsd_falls_back_to_string():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_type("token_type", typeof="string")
    sb.schema.types["token_type"].uri = "xsd:token"
    slot = SlotDefinition(name="tok", range="token_type", required=True)
    sb.add_class("Thing", slots=[slot])
    docs = _generate(sb.schema)
    thing = next(d for d in docs if d.get("@id") == "Thing")
    assert thing["tok"] == "xsd:string"


def test_enum_emitted():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_enum("Color", ["RED", "GREEN", "BLUE"])
    docs = _generate(sb.schema)
    color = next(d for d in docs if d.get("@id") == "Color")
    assert color["@type"] == "Enum"
    assert set(color["@value"]) == {"RED", "GREEN", "BLUE"}


def test_enum_as_slot_range():
    sb = SchemaBuilder("test")
    sb.add_defaults()
    sb.add_enum("Status", ["ACTIVE", "INACTIVE"])
    slot = SlotDefinition(name="status", range="Status", required=True)
    sb.add_class("Record", slots=[slot])
    docs = _generate(sb.schema)
    record = next(d for d in docs if d.get("@id") == "Record")
    assert record["status"] == "Status"


def test_organization_schema(input_path):
    """The organization example schema should produce valid TerminusDB output."""
    docs = _generate(str(input_path("organization.yaml")))
    assert docs[0]["@type"] == "@context"
    class_ids = {d["@id"] for d in docs if d.get("@type") == "Class"}
    assert "Organization" in class_ids
    assert "Employee" in class_ids
    assert "Manager" in class_ids

    manager = next(d for d in docs if d.get("@id") == "Manager")
    assert "Employee" in manager["@inherits"]
    assert manager["has_employees"]["@type"] == "List"


def test_cli(input_path):
    """The gen-terminusdb CLI should emit valid JSON to stdout."""
    runner = CliRunner()
    result = runner.invoke(cli, [str(input_path("organization.yaml"))])
    assert result.exit_code == 0
    docs = json.loads(result.output)
    assert docs[0]["@type"] == "@context"
    assert any(d.get("@type") == "Class" for d in docs)
