from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    EnumDefinition,
    SchemaDefinition,
    SlotDefinition,
    TypeDefinition,
)

from linkml.generators.mermaidclassdiagramgen import MermaidClassDiagramGenerator


def test_generate_class_diagrams(kitchen_sink_path, tmp_path):
    gen = MermaidClassDiagramGenerator(kitchen_sink_path, mergeimports=True, directory=tmp_path)
    gen.generate_class_diagrams()

    # subset of classes from the kitchen sink schema
    expected_classes = ["Person", "Place", "Organization"]

    for cls_name in expected_classes:
        md_file = tmp_path / f"{cls_name}.md"
        # ensure that the file exists
        assert md_file.exists(), f"Expected {md_file} to be generated but it was not found."

        # check file contents for basic markers
        contents = md_file.read_text()
        assert "classDiagram" in contents, f"'classDiagram' not found in {md_file}"
        assert f"class {cls_name}" in contents, f"Class '{cls_name}' not found in {md_file}"

        if cls_name == "Person":
            # Check for enum usage in Person class
            assert 'click LifeStatusEnum href "../LifeStatusEnum"' in contents, (
                f"'LifeStatusEnum' not found in {md_file}"
            )


def test_preserve_names():
    """Test preserve_names option preserves original LinkML names in Mermaid class diagram output"""
    schema = SchemaDefinition(
        id="https://example.com/test_schema",
        name="test_underscore_schema",
        imports=["linkml:types"],
        prefixes={"linkml": "https://w3id.org/linkml/"},
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
    gen_default = MermaidClassDiagramGenerator(schema=schema, directory="/tmp/test_default")

    # Test name method directly
    my_class = schema.classes["My_Class"]
    my_slot = schema.slots["my_slot"]

    assert gen_default.name(my_class) == "MyClass"
    assert gen_default.name(my_slot) == "my_slot"

    # Test preserve_names behavior (names are preserved)
    gen_preserve = MermaidClassDiagramGenerator(schema=schema, directory="/tmp/test_preserve", preserve_names=True)

    assert gen_preserve.name(my_class) == "My_Class"
    assert gen_preserve.name(my_slot) == "my_slot"

    # Test edge cases and different element types for coverage
    assert gen_preserve.name(None) == ""

    enum_def = EnumDefinition(name="Test_Enum")
    type_def = TypeDefinition(name="Custom_Type", typeof="string")

    assert gen_preserve.name(enum_def) == "Test_Enum"
    assert gen_preserve.name(type_def) == "Custom_Type"
    assert gen_default.name(enum_def) == "TestEnum"
    assert gen_default.name(type_def) == "CustomType"

    # Test generate_class_diagrams method for coverage
    gen_preserve.generate_class_diagrams()
