import os
from xml.dom import minidom

import pytest

from linkml.generators.plantumlgen import PlantumlGenerator

MARKDOWN_HEADER = """@startuml
skinparam nodesep 10
hide circle
hide empty members
"""

MARKDOWN_FOOTER = """
@enduml
"""

PERSON = """
class "Person" [[{A person, living or dead}]] {
    {field} id : string  
    {field} name : string  
    {field} age_in_years : integer  
    {field} species_name : string  
    {field} stomach_count : integer  
    {field} is_living : LifeStatusEnum  
    {field} aliases : string  [0..*]
}
"""

PERSON2MEDICALEVENT = """
"Person" *--> "0..*" "MedicalEvent" : "has medical history"
"""

FAMILIALRELATIONSHIP2PERSON = """
"FamilialRelationship" --> "1" "Person" : "related to"
"""

DATASET2PERSON = """
"Dataset" *--> "0..*" "Person" : "persons"
"""


@pytest.mark.parametrize(
    "input_class,expected",
    [
        # check that expected plantUML class diagram blocks are present
        # when diagrams are generated for different classes
        ("Person", PERSON),
        ("Dataset", DATASET2PERSON),
        ("MedicalEvent", PERSON2MEDICALEVENT),
        ("FamilialRelationship", FAMILIALRELATIONSHIP2PERSON),
    ],
)
def test_serialize_selected(input_class, expected, kitchen_sink_path):
    """Test serialization of select plantUML class diagrams from schema."""
    generator = PlantumlGenerator(kitchen_sink_path)
    plantuml = generator.serialize(classes=[input_class])

    # check that the expected block/relationships are present
    # in class-selected diagrams
    assert expected in plantuml

    # make sure that random classes like `MarriageEvent` which
    # have no defined relationships with classes like `FamilialRelationship`
    # have crept into class-selected diagrams
    if input_class == "FamilialRelationship":
        assert 'class "MarriageEvent"' not in plantuml, f"MarriageEvent not reachable from {input_class}"


def test_serialize(kitchen_sink_path):
    """Test serialization of complete plantUML class diagram from schema."""
    generator = PlantumlGenerator(kitchen_sink_path)
    plantuml = generator.serialize()

    # check that plantUML start and end blocks are present
    assert MARKDOWN_HEADER in plantuml
    assert MARKDOWN_FOOTER in plantuml

    # check that Markdown code blocks are not present
    assert "```" not in plantuml, "Markdown code block should not be present"

    # check that classes like `MarriageEvent` are present
    # in complete UML class diagram
    assert 'class "MarriageEvent"' in plantuml


def test_generate_svg(tmp_path, kitchen_sink_path):
    """Test the correctness of SVG rendering of plantUML diagram."""
    generator = PlantumlGenerator(kitchen_sink_path)
    generator.serialize(directory=tmp_path)

    # name of SVG file will be inferred from schema name because
    # we are passing a value to the directory argument
    svg_file = tmp_path / "KitchenSink.svg"

    # check that SVG file is generated correctly
    assert svg_file.is_file()

    svg_dom = minidom.parse(os.fspath(tmp_path / "KitchenSink.svg"))

    classes_list = []  # list of all classes in schema
    relationships_list = []  # list of all links/relationships in schema
    groups = svg_dom.getElementsByTagName("g")
    for group in groups:
        id = group.getAttribute("id")
        if id.startswith("elem_"):
            class_name = id[len("elem_") :]
            classes_list.append(class_name)
        if id.startswith("link_"):
            link_name = id[len("link_") :]
            relationships_list.append(link_name)

    assert "Person" in classes_list
    assert "Dataset" in classes_list
    assert "FamilialRelationship" in classes_list
    assert "MedicalEvent" in classes_list

    assert "Person_MedicalEvent" in relationships_list
    assert "FamilialRelationship_Person" in relationships_list
    assert "Dataset_Person" in relationships_list
    assert "Dataset_MarriageEvent" not in relationships_list
