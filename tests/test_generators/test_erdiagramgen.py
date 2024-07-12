"""
Tests generation of mermaidfrom LinkML schemas
"""

from linkml.generators.erdiagramgen import ERDiagramGenerator


def remove_whitespace(string: str):
    return string.replace(" ", "")


MARKDOWN_HEADER = remove_whitespace(
    """```mermaid
erDiagram
"""
)

PERSON = remove_whitespace(
    """
Person {
    string id
    string name
    integer age_in_years
    string species_name
    integer stomach_count
    LifeStatusEnum is_living
    stringList aliases
}
"""
)

PERSON2MEDICALEVENT = remove_whitespace(
    """
Person ||--}o MedicalEvent : "has medical history"
"""
)

FAMILIALRELATIONSHIP2PERSON = remove_whitespace(
    """
FamilialRelationship ||--|| Person : "related to"
"""
)

DATASET2PERSON = remove_whitespace(
    """
Dataset ||--}o Person : "persons"
"""
)


def test_serialize(kitchen_sink_path):
    """Test default serialization (structural)"""
    gen = ERDiagramGenerator(kitchen_sink_path)
    mermaid = remove_whitespace(gen.serialize())
    assert MARKDOWN_HEADER in mermaid, "default format should be markdown"
    assert PERSON in mermaid
    assert PERSON2MEDICALEVENT in mermaid
    assert FAMILIALRELATIONSHIP2PERSON in mermaid
    assert "FakeClass" not in mermaid, "FakeClass should not be reachable from root"


def test_serialize_direct(kitchen_sink_path):
    """Test default serialization (structural), no markdown block"""
    gen = ERDiagramGenerator(kitchen_sink_path, format="mermaid")
    mermaid = remove_whitespace(gen.serialize())
    assert "```" not in mermaid, "markdown header should not be present"
    assert PERSON in mermaid
    assert PERSON2MEDICALEVENT in mermaid
    assert "FakeClass" not in mermaid, "FakeClass should not be reachable from root"


def test_serialize_exclude_attributes(kitchen_sink_path):
    """Test default serialization (structural), excluding attributes"""
    gen = ERDiagramGenerator(kitchen_sink_path, exclude_attributes=True)
    mermaid = remove_whitespace(gen.serialize())
    assert "string" not in mermaid, "attributes should be excluded"
    assert PERSON2MEDICALEVENT in mermaid
    assert FAMILIALRELATIONSHIP2PERSON in mermaid


def test_serialize_all(kitchen_sink_path):
    """Test serialization of all elements"""
    gen = ERDiagramGenerator(kitchen_sink_path, structural=False)
    mermaid = remove_whitespace(gen.serialize())
    assert PERSON in mermaid
    assert PERSON2MEDICALEVENT in mermaid
    assert "FakeClass" in mermaid, "FakeClass be included even if not reachable"


def test_serialize_selected(kitchen_sink_path):
    """Test serialization of selected elements"""
    gen = ERDiagramGenerator(kitchen_sink_path)
    mermaid = remove_whitespace(gen.serialize_classes(["FamilialRelationship"]))
    assert "Person{" not in mermaid, "Person not reachable from selected"
    assert FAMILIALRELATIONSHIP2PERSON in mermaid, "dangling references should be included"


def test_serialize_selected_with_neighbors(kitchen_sink_path):
    """Test serialization of selected elements"""
    gen = ERDiagramGenerator(kitchen_sink_path)
    mermaid = remove_whitespace(
        gen.serialize_classes(
            ["MedicalEvent"],
            max_hops=0,
            include_upstream=True,
        )
    )
    assert "Person{" in mermaid, "Person is directly upstream from selected"
    assert "MedicalEvent{" in mermaid, "Medical Event is selected"
    assert "ProcedureConcept:" in mermaid, "Procedure is directly downstream from Medical Event"
    assert "DiagnosisConcept:" in mermaid, "Diagnosis is directly downstream from Medical Event"
    assert "CodeSystem" not in mermaid, "Place is too many hops away downstream from selected"
    assert "Organization" not in mermaid, "Organization is not reachable either way from selected"


def test_follow_references(kitchen_sink_path):
    """Test serialization of selected elements following non-inlined references"""
    gen = ERDiagramGenerator(kitchen_sink_path)
    mermaid = remove_whitespace(gen.serialize_classes(["FamilialRelationship"], follow_references=True))
    assert PERSON in mermaid
    assert FAMILIALRELATIONSHIP2PERSON in mermaid


def test_max_hops(kitchen_sink_path):
    """Test truncation at depth"""
    gen = ERDiagramGenerator(kitchen_sink_path)
    mermaid = remove_whitespace(gen.serialize_classes(["Dataset"], max_hops=0))
    assert "Person{" not in mermaid, "Person not reachable from selected in zero hops"
    assert DATASET2PERSON in mermaid, "dangling references should be included"

    mermaid = remove_whitespace(gen.serialize_classes(["Dataset"], max_hops=1))
    assert PERSON in mermaid, "Person reachable from selected in one hop"
    assert "FamilialRelationship{" not in mermaid, "FamilialRelationship not reachable from selected in zero hops"
