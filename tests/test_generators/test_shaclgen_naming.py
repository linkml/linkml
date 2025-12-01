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

    - non_native_names=True  (default)  => shape URIs based on class_uri
    - non_native_names=False             => shape URIs based on LinkML class name

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
