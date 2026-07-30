"""
Tests for SHACL Generator naming behavior and class-URI-based shape merging.

This extends the existing test_shaclgen.py module with:

1. Shape naming mode tests
2. Default merging behavior for classes sharing class_uri
3. Correct (non-merged) behavior when using native LinkML class names
"""

import rdflib
from rdflib import RDF, SH

from linkml.generators.shaclgen import ShaclGenerator


# ---------------------------------------------------------------------------
# 1. SHAPE NAMING MODES: class_uri (default) vs native LinkML class names
# ---------------------------------------------------------------------------
def test_shacl_shape_naming_modes(tmp_path):
    """
    Validate naming modes using a minimal deterministic schema:

    - use_class_uri_names=True  (default)  => shape URIs based on class_uri
    - use_class_uri_names=False             => shape URIs based on LinkML class name

    A custom schema is used to guarantee differences.
    """

    test_schema = """
id: http://example.org/test
name: naming_test
prefixes:
  ex: http://example.org/
  linkml: https://w3id.org/linkml/
default_prefix: http://example.org/test#

imports:
  - linkml:types

classes:
  Foo:
    description: Test class Foo
    class_uri: ex:ExternalFoo
    slots:
      - a

  Bar:
    description: Test class Bar
    class_uri: ex:ExternalBar
    slots:
      - b

slots:
  a:
    range: string

  b:
    range: string
"""

    schema_path = tmp_path / "naming_test.yaml"
    schema_path.write_text(test_schema)

    # --- Mode 1: default mode = class_uri naming ---
    shacl_default = ShaclGenerator(str(schema_path), mergeimports=True, use_class_uri_names=True).serialize()

    g_default = rdflib.Graph()
    g_default.parse(data=shacl_default, format="turtle")
    default_shapes = {str(s) for s in g_default.subjects(RDF.type, SH.NodeShape)}

    # --- Mode 2: native names (LinkML class names) ---
    shacl_native = ShaclGenerator(str(schema_path), mergeimports=True, use_class_uri_names=False).serialize()

    g_native = rdflib.Graph()
    g_native.parse(data=shacl_native, format="turtle")
    native_shapes = {str(s) for s in g_native.subjects(RDF.type, SH.NodeShape)}

    # They must produce the same number of shapes
    assert len(default_shapes) == len(native_shapes) == 2

    # Default mode: shapes must come from class_uri
    assert any("ExternalFoo" in s for s in default_shapes)
    assert any("ExternalBar" in s for s in default_shapes)

    # Native mode: shapes must come from class names Foo and Bar
    assert any(s.endswith("Foo") for s in native_shapes)
    assert any(s.endswith("Bar") for s in native_shapes)

    # And finally: All default URIs MUST differ from all native URIs
    assert default_shapes.isdisjoint(native_shapes), (
        f"Expected naming modes to produce different URIs:\n{default_shapes}\nvs\n{native_shapes}"
    )


# ---------------------------------------------------------------------------
# 2. PROPERTY SHAPE CONSTRAINTS: sh:class (default) vs sh:node (native names)
# ---------------------------------------------------------------------------
def test_shacl_property_class_constraint_modes(tmp_path):
    """
    In default mode, property shapes with a class range emit sh:class <class_uri>.
    In native names mode, property shapes with a class range emit sh:node <native_shape_uri>.

    This tests the fix for the bug where --use-native-names incorrectly emitted
    sh:class <native_shape_uri> — a URI that data nodes are never typed as.
    """
    test_schema = """
id: http://example.org/test
name: range_class_test
prefixes:
  ex: http://example.org/
  linkml: https://w3id.org/linkml/
default_prefix: ex

imports:
  - linkml:types

classes:
  Target:
    description: The class used as a range
    class_uri: ex:ExternalTarget
    slots:
      - label

  Container:
    description: Has a slot whose range is Target
    slots:
      - has_target

slots:
  label:
    range: string

  has_target:
    range: Target
"""

    schema_path = tmp_path / "range_class_test.yaml"
    schema_path.write_text(test_schema)

    EX = "http://example.org/"
    CONTAINER_URI = rdflib.term.URIRef(EX + "Container")
    HAS_TARGET_URI = rdflib.term.URIRef(EX + "has_target")
    EXTERNAL_TARGET_URI = rdflib.term.URIRef(EX + "ExternalTarget")
    NATIVE_TARGET_URI = rdflib.term.URIRef(EX + "Target")

    def get_has_target_prop_node(g, container_uri):
        for prop in g.objects(container_uri, SH.property):
            paths = list(g.objects(prop, SH.path))
            if HAS_TARGET_URI in paths:
                return prop
        return None

    # --- Default mode: sh:class should use the class_uri (ExternalTarget) ---
    g_default = rdflib.Graph()
    g_default.parse(
        data=ShaclGenerator(str(schema_path), mergeimports=True, use_class_uri_names=True).serialize(),
        format="turtle",
    )
    prop_node = get_has_target_prop_node(g_default, CONTAINER_URI)
    assert prop_node is not None, "Container shape missing has_target property"

    class_objects = list(g_default.objects(prop_node, SH["class"]))
    node_objects = list(g_default.objects(prop_node, SH["node"]))

    assert EXTERNAL_TARGET_URI in class_objects, (
        f"Default mode: expected sh:class ex:ExternalTarget (class_uri), got {class_objects}"
    )
    assert node_objects == [], f"Default mode: sh:node must not be emitted, got {node_objects}"

    # --- Native names mode: sh:node should use the LinkML class name (Target) ---
    g_native = rdflib.Graph()
    g_native.parse(
        data=ShaclGenerator(str(schema_path), mergeimports=True, use_class_uri_names=False).serialize(),
        format="turtle",
    )
    prop_node_native = get_has_target_prop_node(g_native, CONTAINER_URI)
    assert prop_node_native is not None, "Container shape missing has_target property in native mode"

    class_objects_native = list(g_native.objects(prop_node_native, SH["class"]))
    node_objects_native = list(g_native.objects(prop_node_native, SH["node"]))

    assert NATIVE_TARGET_URI in node_objects_native, (
        f"Native mode: expected sh:node ex:Target (native shape name), got {node_objects_native}"
    )
    assert class_objects_native == [], (
        f"Native mode: sh:class must not be emitted (was the old bug), got {class_objects_native}"
    )
    # Also verify the wrong value (the old bug) is absent
    assert EXTERNAL_TARGET_URI not in node_objects_native, (
        "Native mode: sh:node must not use the class_uri (ExternalTarget)"
    )
