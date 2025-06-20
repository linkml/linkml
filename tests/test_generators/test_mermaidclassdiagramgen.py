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
