"""Tests for the markdown data dictionary generator."""

from unittest.mock import MagicMock, patch

import pytest

from linkml.generators.markdowndatadictgen import DiagramRenderer, MarkdownDataDictGen, MarkdownTable, SvgCache


def test_markdown_table_empty():
    """Test that MarkdownTable returns empty string for empty data."""
    table = MarkdownTable([])
    assert table.get_markdown() == ""


def test_svg_cache_short_hash():
    """Test SvgCache handles short hashes with fallback logic."""
    cache = SvgCache("/tmp/test")
    # Short hash (less than 4 chars) triggers fallback
    result = cache.get_cache_path("abc")
    assert result is not None
    abs_path, rel_path = result
    assert "abc/00/abc.svg" in abs_path
    assert rel_path == ".kroki-cache/abc/00/abc.svg"


def test_diagram_renderer_kroki_failure():
    """Test DiagramRenderer falls back to mermaid code block when Kroki fails."""
    renderer = DiagramRenderer(kroki_server="http://invalid.server.test:12345")
    result = renderer.render("classDiagram\nA --> B", diagram_name="test")
    # Should fall back to mermaid code block
    assert result.startswith("```mermaid")
    assert "classDiagram" in result
    assert "A --> B" in result


def test_diagram_renderer_large_diagram_post(tmp_path):
    """Test DiagramRenderer uses POST for large diagrams (>1KB)."""
    # Create a diagram source larger than 1KB
    large_source = "classDiagram\n" + "\n".join([f"Class{i} --> Class{i+1}" for i in range(200)])
    assert len(large_source.encode("utf-8")) > 1024  # Verify it's > 1KB

    # Mock the urlopen to avoid network call
    mock_response = MagicMock()
    mock_response.read.return_value = b"<svg>mocked</svg>"
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)

    # Use tmp_path to ensure no cache interference
    with patch("urllib.request.urlopen", return_value=mock_response) as mock_urlopen:
        renderer = DiagramRenderer(kroki_server="https://kroki.io", diagram_dir=str(tmp_path))
        result = renderer.render(large_source, diagram_name="large_test")

        # Verify POST was used (check the request method)
        mock_urlopen.assert_called_once()
        request = mock_urlopen.call_args[0][0]
        assert request.method == "POST"
        assert "large_test" in result  # Returns image reference when diagram_dir is set


def test_datadict_personinfo(input_path, snapshot):
    """Test generating data dictionary for personinfo schema."""
    schema = str(input_path("personinfo.yaml"))
    figs_dir =snapshot("markdowndatadict_personinfo.md").path.parent / "figs"

    try:
      (
          figs_dir / ".kroki-cache/71/4f" / 
          "89dfe883b5f4071e149747a2fd1be257cd2bd6962ee62f7e07ab7202d299.svg").unlink()
    except FileNotFoundError:
        pass
    

    gen = MarkdownDataDictGen(
        schema, 
        debug=True, 
        pretty_format_svg=True, 
        add_svg_links="https://example.com/schema",
        kroki_server="https://kroki.r4.v-lad.org",
        diagram_dir=figs_dir
        )
    generated = gen.serialize()
    assert generated == snapshot("markdowndatadict_personinfo.md")

    try:
      (
          figs_dir / ".kroki-cache/71/4f" / 
          "89dfe883b5f4071e149747a2fd1be257cd2bd6962ee62f7e07ab7202d299.svg").unlink()
    except FileNotFoundError:
        pass
   

def test_datadict_kitchensink(kitchen_sink_path, snapshot):
    """Test generating data dictionary for kitchen sink schema."""
    gen = MarkdownDataDictGen(kitchen_sink_path)
    generated = gen.serialize()
    assert generated == snapshot("markdowndatadict_kitchen_sink.md")


def test_connected_components_detection(input_path):
    """Test detection of connected components for ERD diagrams.

    Connected components are groups of non-abstract classes connected through
    slot relationships (range references to other classes).
    """
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)

    # Test the private method directly
    connected_components, base_classes, standalone_classes = gen._detect_erd_connected_components()

    # Convert components to sets for easier comparison
    component_sets = [set(comp) for comp in connected_components]

    # Component 1: Person-related classes connected via slot ranges
    person_component = {"Person", "Address", "Employment", "Company"}
    assert person_component in component_sets, f"Person component {person_component} not found in {component_sets}"

    # Component 2: Medical-related classes (separate connected component)
    medical_component = {"Patient", "MedicalRecord", "Diagnosis"}
    assert medical_component in component_sets, f"Medical component {medical_component} not found in {component_sets}"

    # Component 3: PersonWithBase-related - Dog connects via owner->PersonWithBase->contact->ContactInfo
    dog_component = {"PersonWithBase", "ContactInfo", "Dog"}
    assert dog_component in component_sets, f"Dog component {dog_component} not found in {component_sets}"

    # Should have exactly 3 connected components
    assert len(connected_components) == 3, f"Expected 3 connected components, got {len(connected_components)}"


def test_erd_diagram_sections(input_path):
    """Test that ERD diagrams are properly sectioned by component type."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema, separate_erd_components=True, omit_standalone_classes=False)

    output = gen.serialize()

    # Should have multiple ERD diagram sections
    assert "## ERD Diagrams" in output, "Should have multiple ERD diagram sections"
    assert "### Component 1" in output, "Should have Component 1 section"
    assert "### Component 2" in output, "Should have Component 2 section"
    assert "### Component 3" in output, "Should have Component 3 section"

    # Should have base classes section (the implementation includes many classes here)
    assert "## Base Classes" in output, "Should have Base Classes section"

    # Check that some expected class documentation is present
    assert "### Person" in output, "Should have Person class section"
    assert "### Dog" in output, "Should have Dog class section"


def test_omit_standalone_classes_option(input_path):
    """Test that --omit-standalone-classes hides both base and standalone classes."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema, separate_erd_components=True, omit_standalone_classes=True)

    output = gen.serialize()

    # Should have ERD diagrams for components
    assert "## ERD Diagrams" in output or "## ERD Diagram" in output, "Should have ERD diagram sections"

    # Should NOT have base classes or standalone classes sections
    assert "## Base Classes" not in output, "Should not have Base Classes section when omitted"
    assert "## Standalone Classes" not in output, "Should not have Standalone Classes section when omitted"


def test_single_erd_option(input_path):
    """Test that --single-erd produces one large ERD diagram."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema, separate_erd_components=False)

    output = gen.serialize()

    # Should have single ERD diagram section
    assert "## ERD Diagram" in output, "Should have single ERD Diagram section"
    assert "## ERD Diagrams" not in output, "Should not have multiple ERD Diagrams section"
    assert "### Component" not in output, "Should not have component subsections"


def test_class_descendants_have_relationships(input_path):
    """Test the helper method for checking if descendants have relationships."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)

    # Get classes with relationships first
    connected_components, _, _ = gen._detect_erd_connected_components()
    classes_with_relationships = set()
    for component in connected_components:
        classes_with_relationships.update(component)

    # Test that Animal's descendants have relationships (Dog connects to PersonWithBase)
    assert gen._class_descendants_have_relationships("Animal", classes_with_relationships), (
        "Animal descendants should have relationships through Dog"
    )

    # Test that BaseEntity's descendants have relationships (ContactInfo is in a component)
    assert gen._class_descendants_have_relationships("BaseEntity", classes_with_relationships), (
        "BaseEntity descendants should have relationships through ContactInfo"
    )

    # Test a class with no descendants
    assert not gen._class_descendants_have_relationships("ConfigSettings", classes_with_relationships), (
        "ConfigSettings should have no descendants with relationships"
    )


def test_dog_in_connected_component(input_path):
    """Test that Dog is in a connected component with PersonWithBase."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)

    connected_components, _, _ = gen._detect_erd_connected_components()
    component_sets = [set(comp) for comp in connected_components]

    # Find which component contains Dog
    dog_component = None
    for comp_set in component_sets:
        if "Dog" in comp_set:
            dog_component = comp_set
            break

    assert dog_component is not None, "Dog should be in a connected component"
    # Dog should be with PersonWithBase (via owner slot) and ContactInfo (via PersonWithBase.contact)
    assert "PersonWithBase" in dog_component, (
        "Dog should be in same component as PersonWithBase (its relationship target)"
    )
    assert "ContactInfo" in dog_component, "ContactInfo should be in same component via PersonWithBase"


def test_basic_output_structure(input_path):
    """Test that generated output has expected basic structure."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)

    output = gen.serialize()

    # Should have main sections
    assert "# CONNECTED-COMPONENTS-TEST" in output, "Should have title"
    assert "## Class Diagram" in output, "Should have class diagram section"
    assert "## Classes" in output, "Should have classes section"
    assert "## Slots" in output, "Should have slots section"
    assert "## Enums" in output, "Should have enums section"

    # Check for mermaid diagram
    assert "```mermaid" in output, "Should have mermaid code blocks"
    assert "classDiagram" in output, "Should have class diagram"


def test_class_attributes_table(input_path):
    """Test that class attributes are rendered as tables."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)

    output = gen.serialize()

    # Person class should have attributes table with name, address, employment
    assert "| Name |" in output, "Should have Name column in attributes table"
    # Check for some expected attributes
    assert "address" in output.lower(), "Should mention address attribute"
    assert "employment" in output.lower(), "Should mention employment attribute"


def test_enum_values_table(input_path):
    """Test that enum values are rendered as tables."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)

    output = gen.serialize()

    # StatusEnum should have permissible values
    assert "StatusEnum" in output, "Should have StatusEnum section"
    assert "active" in output, "Should have 'active' enum value"
    assert "inactive" in output, "Should have 'inactive' enum value"
