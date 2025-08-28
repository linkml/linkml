"""
Tests generation of mermaidfrom LinkML schemas
"""

import pytest
from click.testing import CliRunner
from linkml_runtime.linkml_model.meta import ClassDefinition, SchemaDefinition, SlotDefinition

from linkml.generators.erdiagramgen import ERDiagram, ERDiagramGenerator, cli


@pytest.fixture
def runner():
    return CliRunner()


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


def test_format_option_markdown(runner, kitchen_sink_path):
    """Test the --format option with 'markdown'."""
    result = runner.invoke(cli, [kitchen_sink_path, "--format", "markdown"])
    print(result.output)
    assert result.output.startswith("```mermaid")
    assert result.output.endswith("```\n\n")


def test_format_option_no_markdown(runner, kitchen_sink_path):
    """Test the --format option with 'mermaid'."""
    result = runner.invoke(cli, [kitchen_sink_path, "--format", "mermaid"])
    print(result.output)
    assert not result.output.startswith("```mermaid")
    assert result.output.endswith("\n\n")


def test_exclude_abstract_classes(kitchen_sink_path):
    """Test exclusion of abstract classes"""
    # Test with abstract classes included (default)
    gen = ERDiagramGenerator(kitchen_sink_path, structural=False)
    mermaid = remove_whitespace(gen.serialize())
    assert "Friend{" in mermaid, "Friend abstract class should be included by default"

    # Test with abstract classes excluded
    gen = ERDiagramGenerator(kitchen_sink_path, structural=False, exclude_abstract_classes=True)
    mermaid = remove_whitespace(gen.serialize())
    assert "Friend{" not in mermaid, "Friend abstract class should be excluded"
    assert "Person{" in mermaid, "Person concrete class should still be included"
    assert "Agent{" in mermaid, "Agent concrete class should still be included"


def test_preserve_names():
    """Test preserve_names option preserves original LinkML names in ER diagram output"""

    schema = SchemaDefinition(
        id="https://example.com/test_schema",
        name="test_underscore_schema",
        classes={
            "My_Class": ClassDefinition(name="My_Class", slots=["my_slot", "related_object"]),
            "Another_Class_Name": ClassDefinition(name="Another_Class_Name", slots=["class_specific_slot"]),
        },
        slots={
            "my_slot": SlotDefinition(name="my_slot", range="string"),
            "class_specific_slot": SlotDefinition(name="class_specific_slot", range="string"),
            "related_object": SlotDefinition(name="related_object", range="Another_Class_Name"),
        },
    )

    # Test default behavior (names are normalized)
    gen_default = ERDiagramGenerator(schema=schema)
    diagram_default = gen_default.serialize()

    assert "MyClass {" in diagram_default
    assert "AnotherClassName {" in diagram_default
    assert "string my_slot" in diagram_default
    assert "MyClass ||--" in diagram_default and 'AnotherClassName : "related_object"' in diagram_default

    # Test preserve_names behavior (names are preserved)
    gen_preserve = ERDiagramGenerator(schema=schema, preserve_names=True)
    diagram_preserve = gen_preserve.serialize()

    assert "My_Class {" in diagram_preserve
    assert "Another_Class_Name {" in diagram_preserve
    assert "string my_slot" in diagram_preserve
    assert "My_Class ||--" in diagram_preserve and 'Another_Class_Name : "related_object"' in diagram_preserve

    # Test add_upstream_class method for branch coverage
    gen_test = ERDiagramGenerator(schema=schema, preserve_names=True)
    diagram = ERDiagram()
    gen_test.add_upstream_class("My_Class", set(), diagram)
    assert any(e.name == "My_Class" for e in diagram.entities)
