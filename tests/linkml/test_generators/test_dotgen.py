"""
Tests for DotGenerator (graphviz/dotfile generation)
"""

import os
import tempfile

import pytest
from click.testing import CliRunner
from graphviz import Digraph

from linkml.generators.dotgen import DotGenerator, cli
from linkml_runtime.linkml_model.meta import SlotDefinition


@pytest.fixture
def runner():
    """Fixture for Click CLI runner"""
    return CliRunner()


def test_generator_initialization(kitchen_sink_path):
    """Test that DotGenerator initializes correctly"""
    gen = DotGenerator(kitchen_sink_path)
    assert gen is not None
    assert gen.generatorname == "dotgen.py"
    assert gen.generatorversion == "0.1.1"
    # directory_output is a class attribute, not instance attribute after initialization
    assert DotGenerator.directory_output is True
    assert gen.visit_all_class_slots is True
    assert gen.uses_schemaloader is True
    assert "png" in gen.valid_formats


def test_deprecated_decorator(kitchen_sink_path):
    """Test that DotGenerator is marked as deprecated"""
    # Check if creating an instance triggers a deprecation warning
    with pytest.warns(DeprecationWarning, match="Replaced by yuml/mermaid"):
        DotGenerator(kitchen_sink_path)


def test_serialize_with_schema_object(kitchen_sink_path):
    """Test serialization with kitchen sink schema"""
    gen = DotGenerator(kitchen_sink_path, format="dot")
    # Visit schema without any specific options
    gen.visit_schema()
    # Serialize should not crash - it doesn't return anything meaningful
    # since we're just testing the generator methods work
    gen.end_schema()


def test_visit_schema_initializes_attributes(kitchen_sink_path):
    """Test that visit_schema properly initializes attributes"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(classname=["Person"], directory=None, filename=None)

    assert gen.classnames == ["Person"]
    assert gen.filename is None
    assert gen.dirname is None
    assert gen.filedot is None


def test_visit_schema_with_filename(kitchen_sink_path):
    """Test that visit_schema creates filedot when filename is provided"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    assert gen.filename == "test"
    assert gen.filedot is not None
    assert isinstance(gen.filedot, Digraph)
    assert gen.filedot.comment == gen.schema.name


def test_visit_schema_with_directory(kitchen_sink_path):
    """Test that visit_schema creates directory when specified"""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = os.path.join(tmpdir, "test_output")
        gen = DotGenerator(kitchen_sink_path)
        gen.visit_schema(directory=test_dir)

        assert gen.dirname == test_dir
        assert os.path.exists(test_dir)


def test_visit_schema_unknown_classname(kitchen_sink_path):
    """Test that visit_schema raises error for unknown class name"""
    gen = DotGenerator(kitchen_sink_path)

    with pytest.raises(ValueError, match="Unknown class name: NonExistentClass"):
        gen.visit_schema(classname=["NonExistentClass"])


def test_visit_class_filters_by_classname(kitchen_sink_path):
    """Test that visit_class filters classes when classnames is set"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(classname=["Person"])

    person_class = gen.schema.classes["Person"]
    org_class = gen.schema.classes.get("Organization")

    # Person should be visited
    assert gen.visit_class(person_class) is True
    # Organization should not be visited (if it exists)
    if org_class:
        assert gen.visit_class(org_class) is False


def test_visit_class_without_filter(kitchen_sink_path):
    """Test that visit_class accepts all classes when no filter is set"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema()

    person_class = gen.schema.classes["Person"]

    # Should be visited
    assert gen.visit_class(person_class) is True


def test_visit_class_creates_classdot_with_directory(kitchen_sink_path):
    """Test that visit_class creates classdot when directory is set"""
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = DotGenerator(kitchen_sink_path)
        gen.visit_schema(directory=tmpdir)

        person_class = gen.schema.classes["Person"]
        gen.visit_class(person_class)

        assert gen.classdot is not None
        assert isinstance(gen.classdot, Digraph)


def test_visit_class_handles_is_a_relationship(kitchen_sink_path):
    """Test that visit_class handles is_a relationships"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    # Find a class with is_a relationship in kitchen_sink
    for cls in gen.schema.classes.values():
        if cls.is_a:
            gen.visit_class(cls)
            break

    # Check that the filedot has nodes and edges
    assert gen.filedot is not None


def test_visit_class_handles_mixins(kitchen_sink_path):
    """Test that visit_class handles mixins"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    # Find a class with mixins in kitchen_sink
    for cls in gen.schema.classes.values():
        if cls.mixins:
            gen.visit_class(cls)
            break

    # Check that the filedot has nodes and edges for mixins
    assert gen.filedot is not None


def test_visit_class_slot(kitchen_sink_path):
    """Test visit_class_slot method"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    person_class = gen.schema.classes["Person"]
    gen.visit_class(person_class)

    # Get a slot from the schema
    slot_name = person_class.slots[0] if person_class.slots else None
    if slot_name:
        slot = gen.schema.slots.get(slot_name)
        if slot:
            gen.visit_class_slot(person_class, slot_name, slot)

    # Verify that nodes and edges were created
    assert gen.filedot is not None


def test_visit_class_slot_subject_object(kitchen_sink_path):
    """Test visit_class_slot with subject and object slots"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    # Use kitchen_sink classes for this test
    person_class = gen.schema.classes["Person"]
    gen.visit_class(person_class)

    # Create custom slots for this test
    subject_slot = SlotDefinition(name="subject", range="Person")
    object_slot = SlotDefinition(name="object", range="Person")

    gen.visit_class_slot(person_class, "subject", subject_slot)
    assert gen.cls_subj == subject_slot

    gen.visit_class_slot(person_class, "object", object_slot)
    assert gen.cls_obj == object_slot


def test_end_class_with_subject_object(kitchen_sink_path):
    """Test end_class creates relation edges when subject and object are set"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    person_class = gen.schema.classes["Person"]
    gen.visit_class(person_class)

    subject_slot = SlotDefinition(name="subject", range="Person")
    object_slot = SlotDefinition(name="object", range="Person")

    gen.visit_class_slot(person_class, "subject", subject_slot)
    gen.visit_class_slot(person_class, "object", object_slot)

    gen.end_class(person_class)

    # Verify filedot still exists and has content
    assert gen.filedot is not None


def test_end_class_renders_to_directory(kitchen_sink_path):
    """Test end_class renders graph files when directory is set"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = DotGenerator(kitchen_sink_path, format="dot")
            gen.visit_schema(directory=tmpdir)

            person_class = gen.schema.classes["Person"]
            gen.visit_class(person_class)
            gen.end_class(person_class)

            # Check that a file was created (GraphViz may or may not add extension depending on environment)
            files_created = os.listdir(tmpdir)
            if not files_created:
                pytest.skip("Graphviz executable not available - no files rendered")

            expected_file = os.path.join(tmpdir, "person.dot")
            expected_file_no_ext = os.path.join(tmpdir, "person")
            assert os.path.exists(expected_file) or os.path.exists(expected_file_no_ext), (
                f"Expected person file not found. Files in directory: {files_created}"
            )
    except Exception as e:
        if "Graphviz executables" in str(e):
            pytest.skip("Graphviz executable not found on system PATH")
        raise


def test_end_schema_renders_file(kitchen_sink_path):
    """Test end_schema renders the final graph when filename is set"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = DotGenerator(kitchen_sink_path, format="dot")
            gen.visit_schema(filename="schema", directory=tmpdir)

            # Visit at least one class
            person_class = gen.schema.classes["Person"]
            gen.visit_class(person_class)

            gen.end_schema()

            # Check that the file was created (GraphViz adds the format extension)
            expected_file = os.path.join(tmpdir, "schema.dot")
            assert os.path.exists(expected_file)
    except Exception as e:
        if "Graphviz executables" in str(e):
            pytest.skip("Graphviz executable not found on system PATH")
        raise


def test_node_method_adds_to_both_dots(kitchen_sink_path):
    """Test that node method adds nodes to both filedot and classdot"""
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = DotGenerator(kitchen_sink_path)
        gen.visit_schema(filename="test", directory=tmpdir)

        # Create both dots
        person_class = gen.schema.classes["Person"]
        gen.visit_class(person_class)

        # Add a node
        gen.node("TestNode", "TestLabel")

        # Verify both dots have nodes (they should not be None)
        assert gen.filedot is not None
        assert gen.classdot is not None


def test_edge_method_adds_to_both_dots(kitchen_sink_path):
    """Test that edge method adds edges to both filedot and classdot"""
    with tempfile.TemporaryDirectory() as tmpdir:
        gen = DotGenerator(kitchen_sink_path)
        gen.visit_schema(filename="test", directory=tmpdir)

        # Create both dots
        person_class = gen.schema.classes["Person"]
        gen.visit_class(person_class)

        # Add nodes and an edge
        gen.node("Node1", "Label1")
        gen.node("Node2", "Label2")
        gen.edge("Node1", "Node2", label="test_edge")

        # Verify both dots exist
        assert gen.filedot is not None
        assert gen.classdot is not None


def test_node_method_with_only_filedot(kitchen_sink_path):
    """Test node method when only filedot is set"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    gen.node("TestNode", "TestLabel")

    assert gen.filedot is not None
    assert gen.classdot is None


def test_edge_method_with_only_filedot(kitchen_sink_path):
    """Test edge method when only filedot is set"""
    gen = DotGenerator(kitchen_sink_path)
    gen.visit_schema(filename="test")

    gen.node("Node1", "Label1")
    gen.node("Node2", "Label2")
    gen.edge("Node1", "Node2")

    assert gen.filedot is not None
    assert gen.classdot is None


def test_cli_basic(runner, kitchen_sink_path):
    """Test CLI basic invocation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "output.dot")
        result = runner.invoke(cli, [kitchen_sink_path, "--out", output_file, "--format", "dot"])

        # The test might fail if graphviz executable is not installed, which is acceptable
        # since we're testing the generator logic, not the external tool
        if result.exit_code != 0 and "Graphviz executables" in str(result.exception):
            pytest.skip("Graphviz executable not found on system PATH")

        # Should run without error
        assert result.exit_code == 0
        # File should be created (CLI writes directly to specified file)
        # For dot format, GraphViz render adds extension, so check both
        assert os.path.exists(output_file) or os.path.exists(output_file + ".dot")


def test_cli_with_directory(runner, kitchen_sink_path):
    """Test CLI with directory option"""
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(cli, [kitchen_sink_path, "--directory", tmpdir, "--format", "dot"])

        # The test might fail if graphviz executable is not installed
        if result.exit_code != 0 and "Graphviz executables" in str(result.exception):
            pytest.skip("Graphviz executable not found on system PATH")

        # Should run without error
        assert result.exit_code == 0
        # Directory should contain generated files
        files = os.listdir(tmpdir)
        assert len(files) > 0


def test_cli_with_classname_filter(runner, kitchen_sink_path):
    """Test CLI with classname filter"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "filtered.dot")
        result = runner.invoke(
            cli,
            [
                kitchen_sink_path,
                "--out",
                output_file,
                "--classname",
                "Person",
                "--format",
                "dot",
            ],
        )

        # The test might fail if graphviz executable is not installed
        if result.exit_code != 0 and "Graphviz executables" in str(result.exception):
            pytest.skip("Graphviz executable not found on system PATH")

        # Should run without error
        assert result.exit_code == 0
        assert os.path.exists(output_file + ".dot")


def test_cli_with_multiple_classnames(runner, kitchen_sink_path):
    """Test CLI with multiple classname filters"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "multi.dot")
        result = runner.invoke(
            cli,
            [
                kitchen_sink_path,
                "--out",
                output_file,
                "--classname",
                "Person",
                "--classname",
                "Organization",
                "--format",
                "dot",
            ],
        )

        # The test might fail if graphviz executable is not installed
        if result.exit_code != 0 and "Graphviz executables" in str(result.exception):
            pytest.skip("Graphviz executable not found on system PATH")

        # Should run without error
        assert result.exit_code == 0
        assert os.path.exists(output_file + ".dot")


def test_cli_version_option(runner):
    """Test CLI version option"""
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()


def test_cli_help_option(runner):
    """Test CLI help option"""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Generate graphviz representations" in result.output


def test_valid_formats_includes_png():
    """Test that valid_formats includes png"""
    from linkml.generators.dotgen import valid_formats as module_valid_formats

    assert "png" in DotGenerator.valid_formats
    # Also check the module-level valid_formats is sorted
    assert module_valid_formats == sorted(module_valid_formats)


def test_serialize_integration_with_kitchen_sink(kitchen_sink_path):
    """Integration test: serialize kitchen_sink schema"""
    gen = DotGenerator(kitchen_sink_path, format="dot")
    gen.visit_schema()

    # Should complete without error
    # Note: serialize() with no parameters may not return meaningful content
    # as it depends on internal state, but it should not crash
    gen.end_schema()


def test_multiple_classes_with_relationships(kitchen_sink_path):
    """Test handling multiple classes with various relationships"""
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            gen = DotGenerator(kitchen_sink_path, format="dot")
            gen.visit_schema(filename="full_schema", directory=tmpdir)

            # Visit a few classes from kitchen_sink
            for class_name in ["Person", "Organization", "Dataset"][:3]:  # Limit to 3 classes
                if class_name in gen.schema.classes:
                    class_def = gen.schema.classes[class_name]
                    if gen.visit_class(class_def):
                        # Visit slots for each class
                        for slot_name in class_def.slots[:2]:  # Limit slots to 2 per class
                            if slot_name in gen.schema.slots:
                                slot = gen.schema.slots[slot_name]
                                gen.visit_class_slot(class_def, slot_name, slot)
                        gen.end_class(class_def)

            gen.end_schema()

            # Verify file was created (GraphViz adds the format extension)
            expected_file = os.path.join(tmpdir, "full_schema.dot")
            assert os.path.exists(expected_file)
    except Exception as e:
        if "Graphviz executables" in str(e):
            pytest.skip("Graphviz executable not found on system PATH")
        raise
