import json
from collections.abc import Callable, Mapping

import pytest
import rdflib
from rdflib.compare import to_canonical_graph


@pytest.fixture
def personinfo_path(input_path):
    return str(input_path("personinfo.yaml"))


@pytest.fixture
def type_hierarchy_schema_str():
    return """
id: http://example.org
name: inline-dict-test
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test

classes:
  NamedThing:
    slots:
      - id
      - category
  Person:
    is_a: NamedThing

types:
  category type:
    typeof: uriorcurie
    description: >-
      see biolink model

slots:
  id:
    identifier: true
    range: string
    required: true
  type:
    slot_uri: rdf:type
    multivalued: true
  category:
    is_a: type
    range: category type
    designates_type: true
    is_class_field: true
    multivalued: true
"""


@pytest.fixture
def schema_str():
    return """
id: http://example.org
name: inline-dict-test
imports:
  - https://w3id.org/linkml/types
prefixes:
  x: http://example.org/
default_prefix: x
default_range: string
description: test

classes:
  NamedThing:
    slots:
      - id
      - full_name
      - thingtype
  Person:
    is_a: NamedThing
    #class_uri: "http://testbreaker/not-the-uri-you-expect"
    slots:
      - height
  Organisation:
    is_a: NamedThing
    slots:
      - number_of_employees
  NonProfit:
    is_a: Organisation
  ForProfit:
    is_a: Organisation
    slots:
      - target_profit_margin
  Container:
    tree_root: true
    slots:
      - things
  ContainerWithOneSibling:
    slots:
      - persons
slots:
  id:
    identifier: true
    range: string
    required: true
  thingtype:
    designates_type: true
    range: uriorcurie
  full_name:
    range: string
  height:
    range: integer
  number_of_employees:
    range: integer
  things:
    range: NamedThing
    multivalued: true
    inlined_as_list: true
  persons:
    range: Person
    multivalued: true
    inlined_as_list: true
  target_profit_margin:
    range: float
"""


@pytest.fixture
def data_str():
    return """
{
  "things": [
    {
      "id": "1",
      "thingtype": "x:Person",
      "full_name": "phoebe",
      "height": 10
    },
    {
      "id": "2",
      "thingtype": "x:Organisation",
      "full_name": "University of Earth",
      "number_of_employees": 2
    }
  ]
}
"""


def _normalize_snapshot_bundle_output(name: str, output: str) -> str:
    """Normalize bundle sections that would otherwise vary in serialization order."""
    if name.endswith((".ttl", ".owl")):
        graph = rdflib.Graph()
        graph.parse(data=output, format="turtle")
        normalized = to_canonical_graph(graph).serialize(format="nt")
        return "\n".join(sorted(line for line in normalized.splitlines() if line)) + "\n"
    if name.endswith((".json", ".schema.json", ".context.jsonld")):
        return json.dumps(json.loads(output), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    return output if output.endswith("\n") else f"{output}\n"


def render_snapshot_bundle(outputs: Mapping[str, str]) -> str:
    """Render multiple named outputs into one deterministic snapshot string."""
    parts: list[str] = []
    for name, output in outputs.items():
        parts.append(f"# --- {name} ---\n")
        parts.append(_normalize_snapshot_bundle_output(name, output))
        parts.append("\n")
    return "".join(parts)


@pytest.fixture
def bundled_snapshot_text() -> Callable[[Mapping[str, str]], str]:
    """Build a labeled single-file snapshot from multiple related outputs."""

    return render_snapshot_bundle
