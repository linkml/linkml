from linkml.generators.markdowndatadictgen import MarkdownDataDictGen
from linkml.generators.markdowngen import MarkdownGenerator


def test_datadict_gen(kitchen_sink_path, tmp_path):
    gen = MarkdownGenerator(kitchen_sink_path)
    gen.serialize(directory=tmp_path)


def test_datadict_personinfo(input_path, snapshot):
    schema = str(input_path("personinfo.yaml"))
    gen = MarkdownDataDictGen(schema)
    generated = gen.serialize()
    assert generated == snapshot("personinfo.md")


def test_datadict_kitchensink(kitchen_sink_path, snapshot):
    gen = MarkdownDataDictGen(kitchen_sink_path)
    generated = gen.serialize()
    assert generated == snapshot("kitchen_sink.md")


def test_connected_components_detection(input_path):
    """Test detection of connected components, base classes, and standalone classes."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)
    
    # Test the private method directly
    connected_components, base_classes, truly_standalone_classes = gen._detect_erd_connected_components()
    
    # Expected results:
    # Component 1: Person, Address, Employment, Company (4 classes connected via relationships)
    # Component 2: Patient, MedicalRecord, Diagnosis (3 classes connected via relationships)  
    # Component 3: PersonWithBase, ContactInfo, Dog (connected through relationships, inheritance parents are base classes)
    # Base classes: IdentifiedThing, Animal, Mammal (used as parents but no direct relationships)  
    # Standalone: ConfigSettings, UtilityClass (no relationships, not used as parents)
    # Note: BaseEntity is abstract so excluded from ERD analysis
    
    # Check we have the right number of components
    assert len(connected_components) == 3, f"Expected 3 connected components, got {len(connected_components)}"
    
    # Convert components to sets of sets for easier comparison
    component_sets = [set(comp) for comp in connected_components]
    
    # Check Component 1 (Person-related)
    person_component = {"Person", "Address", "Employment", "Company"}
    assert person_component in component_sets, f"Person component {person_component} not found in {component_sets}"
    
    # Check Component 2 (Medical-related) 
    medical_component = {"Patient", "MedicalRecord", "Diagnosis"}
    assert medical_component in component_sets, f"Medical component {medical_component} not found in {component_sets}"
    
    # Check Component 3 (PersonWithBase-related with relationships but not inheritance parents)
    inheritance_component = {"PersonWithBase", "ContactInfo", "Dog"}
    assert inheritance_component in component_sets, f"Inheritance component {inheritance_component} not found in {component_sets}"
    
    # Check base classes (inheritance parents that don't have direct relationships)
    expected_base_classes = {"IdentifiedThing", "Animal", "Mammal"}
    assert base_classes == expected_base_classes, f"Expected base classes {expected_base_classes}, got {base_classes}"
    
    # Check truly standalone classes
    expected_standalone_classes = {"ConfigSettings", "UtilityClass"}
    assert truly_standalone_classes == expected_standalone_classes, f"Expected standalone classes {expected_standalone_classes}, got {truly_standalone_classes}"


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
    
    # Should have base classes section
    assert "## Base Classes" in output, "Should have Base Classes section"
    assert "These classes have no direct relationships but serve as base classes" in output
    
    # Should have standalone classes section
    assert "## Standalone Classes" in output, "Should have Standalone Classes section"
    assert "These classes are completely isolated with no relationships" in output


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
    assert gen._class_descendants_have_relationships("Animal", classes_with_relationships), "Animal descendants should have relationships through Dog"
    
    # Test that BaseEntity's descendants have relationships (ContactInfo is in a component)
    assert gen._class_descendants_have_relationships("BaseEntity", classes_with_relationships), "BaseEntity descendants should have relationships through ContactInfo"
    
    # Test a class with no descendants
    assert not gen._class_descendants_have_relationships("ConfigSettings", classes_with_relationships), "ConfigSettings should have no descendants with relationships"


def test_inheritance_chain_classification(input_path):
    """Test that inheritance chains are properly classified."""
    schema = str(input_path("connected_components_test.yaml"))
    gen = MarkdownDataDictGen(schema)
    
    connected_components, base_classes, truly_standalone_classes = gen._detect_erd_connected_components()
    
    # Animal and Mammal should be classified as base classes because Dog (descendant) has relationships
    assert "Animal" in base_classes, "Animal should be a base class - its descendant Dog has relationships"
    assert "Mammal" in base_classes, "Mammal should be a base class - its descendant Dog has relationships"
    assert "Animal" not in truly_standalone_classes, "Animal should not be standalone"
    assert "Mammal" not in truly_standalone_classes, "Mammal should not be standalone"
    
    # Check that Dog (the descendant with actual relationships) is in a connected component
    component_sets = [set(comp) for comp in connected_components]
    
    # Find which component contains Dog
    dog_component = None
    for comp_set in component_sets:
        if "Dog" in comp_set:
            dog_component = comp_set
            break
    
    assert dog_component is not None, "Dog should be in a connected component"
    # Dog should be with PersonWithBase and ContactInfo (the classes it actually has relationships with)
    assert "PersonWithBase" in dog_component, "Dog should be in same component as PersonWithBase (its relationship target)"
    assert "ContactInfo" in dog_component, "ContactInfo should be in same component via PersonWithBase"
    
    # But Animal and Mammal should NOT be in the connected component (they're base classes)
    assert "Animal" not in dog_component, "Animal should be a base class, not in connected component"
    assert "Mammal" not in dog_component, "Mammal should be a base class, not in connected component"
