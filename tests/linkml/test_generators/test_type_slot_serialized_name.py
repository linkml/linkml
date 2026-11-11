"""Cross-generator tests for serializing RDF type slots under their alias."""

import json

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from linkml.generators.golanggen.golanggen import GolangGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.jsonschemagen import JsonSchemaGenerator


@pytest.mark.parametrize(
    ("rdf_prefix", "rdf_slot_uri"),
    [
        ("rdf", "rdf:type"),
        ("r", "r:type"),
        ("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
    ],
)
@pytest.mark.parametrize(("alias", "serialized_name"), [("kind", "kind"), ("kebab-case", "kebab_case")])
@pytest.mark.parametrize("use_curies", [False, True])
@pytest.mark.parametrize("required", [False, True])
def test_rdf_type_slot_uses_aliased_serialized_name(
    tmp_path,
    rdf_prefix: str,
    rdf_slot_uri: str,
    alias: str,
    serialized_name: str,
    use_curies: bool,
    required: bool,
):
    """RDF type uses its normalized alias across context, schema, and Go tags."""
    schema_path = tmp_path / "rdf_type_alias.yaml"
    schema_path.write_text(
        f"""
id: https://example.org/rdf-type-alias
name: rdf_type_alias
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/vocab/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  {rdf_prefix}: http://www.w3.org/1999/02/22-rdf-syntax-ns#
  bx: https://example.org/business/
classes:
  Entity:
    class_uri: ex:Entity
    slots: [id, membership, label, business_type, business_id]
slots:
  id:
    identifier: true
    required: true
    range: uriorcurie
    slot_uri: bx:id
  membership:
    alias: {alias}
    slot_uri: {rdf_slot_uri}
    required: {str(required).lower()}
    range: uriorcurie
  label:
    required: true
    range: string
    slot_uri: http://www.w3.org/2000/01/rdf-schema#label
  business_type:
    alias: businessType
    slot_uri: bx:type
    designates_type: true
    range: string
  business_id:
    alias: businessId
    slot_uri: bx:id
    range: string
""",
        encoding="utf-8",
    )

    # --- JSON-LD Context ---
    context = json.loads(ContextGenerator(str(schema_path), use_curies=use_curies).serialize())
    assert context["@context"][serialized_name] == {"@id": "@type"}
    assert context["@context"]["id"] == "@id"
    business_type_name = "bx:type" if use_curies else "businessType"
    business_id_name = "bx:id" if use_curies else "businessId"
    assert business_type_name in context["@context"]
    assert business_id_name in context["@context"]

    serialized_label_name = "rdfs:label" if use_curies else "label"
    compacted = {
        "@context": context["@context"],
        "@id": "ex:subject",
        serialized_name: "ex:Entity",
        serialized_label_name: "Source entity",
    }
    actual_graph = Graph().parse(data=json.dumps(compacted), format="json-ld")
    reference_graph = Graph().parse(
        data="""
@prefix ex: <https://example.org/vocab/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
ex:subject a ex:Entity ; rdfs:label "Source entity" .
""",
        format="turtle",
    )
    assert isomorphic(actual_graph, reference_graph)

    # --- JSON Schema ---
    json_schema = json.loads(JsonSchemaGenerator(str(schema_path), use_curies=use_curies).serialize())
    entity_schema = next(value for key, value in json_schema["$defs"].items() if key.endswith("Entity"))
    assert serialized_name in entity_schema["properties"]
    assert (serialized_name in entity_schema.get("required", [])) is required
    assert "id" in entity_schema["properties"]
    assert business_id_name in entity_schema["properties"]
    assert business_type_name in entity_schema["properties"]

    # --- Go ---
    go_source = GolangGenerator(str(schema_path), package="fixture").serialize()
    omitempty = "" if required else ",omitempty"
    go_tag = f'json:"{serialized_name}{omitempty}"'
    assert go_tag in go_source
    assert 'json:"id"' in go_source

    go_curie_source = GolangGenerator(str(schema_path), package="fixture", use_curies=True).serialize()
    assert go_tag in go_curie_source
    assert 'json:"id"' in go_curie_source
    assert 'json:"bx:id,omitempty"' in go_curie_source
    assert 'json:"bx:type,omitempty"' in go_curie_source


def test_designates_type_does_not_make_business_predicate_a_keyword(tmp_path):
    """A non-RDF slot URI stays an ordinary CURIE even when designates_type is set."""
    schema_path = tmp_path / "business_type.yaml"
    schema_path.write_text(
        """
id: https://example.org/business-type
name: business_type
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/vocab/
  rdfs: http://www.w3.org/2000/01/rdf-schema#
  bx: https://example.org/business/
classes:
  Entity:
    class_uri: ex:Entity
    slots: [id, classification]
slots:
  id:
    identifier: true
    range: uriorcurie
  classification:
    alias: kind
    slot_uri: bx:type
    designates_type: true
    range: string
""",
        encoding="utf-8",
    )

    # --- JSON-LD Context ---
    context = json.loads(ContextGenerator(str(schema_path), use_curies=True).serialize())
    assert "bx:type" in context["@context"]
    assert context["@context"]["bx:type"]["@id"] != "@type"

    # --- JSON Schema ---
    json_schema = json.loads(JsonSchemaGenerator(str(schema_path), use_curies=True).serialize())
    entity_schema = next(value for key, value in json_schema["$defs"].items() if key.endswith("Entity"))
    assert "bx:type" in entity_schema["properties"]
    assert "kind" not in entity_schema["properties"]


@pytest.mark.parametrize("use_curies", [False, True])
def test_rdf_type_alias_collision_is_reported(tmp_path, use_curies: bool):
    """Only report a collision when the selected key policy maps both slots to one key."""
    schema_path = tmp_path / "type_key_collision.yaml"
    schema_path.write_text(
        """
id: https://example.org/type-key-collision
name: type_key_collision
default_prefix: ex
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/vocab/
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
classes:
  Entity:
    slots: [membership, kind_value]
slots:
  membership:
    alias: kind
    slot_uri: rdf:type
    range: uriorcurie
  kind_value:
    alias: kind
    slot_uri: ex:kindValue
    range: string
""",
        encoding="utf-8",
    )

    if not use_curies:
        # Both slots use their alias, so the ordinary property conflicts with
        # the alias for the JSON-LD @type keyword.

        # --- JSON-LD Context ---
        with pytest.raises(ValueError, match="collision"):
            ContextGenerator(str(schema_path)).serialize()
        # --- JSON Schema ---
        with pytest.raises(ValueError, match="collision"):
            JsonSchemaGenerator(str(schema_path)).serialize()
    else:
        # With CURIEs, the RDF type keyword still uses its alias, while the
        # ordinary predicate gets its CURIE and no longer collides.

        # --- JSON-LD Context ---
        context = json.loads(ContextGenerator(str(schema_path), use_curies=True).serialize())
        assert context["@context"]["kind"] == {"@id": "@type"}
        assert "ex:kindValue" in context["@context"]

        # --- JSON Schema ---
        json_schema = json.loads(JsonSchemaGenerator(str(schema_path), use_curies=True).serialize())
        entity_schema = next(value for key, value in json_schema["$defs"].items() if key.endswith("Entity"))
        assert {"kind", "ex:kindValue"} <= entity_schema["properties"].keys()
