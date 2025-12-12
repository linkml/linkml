import pytest
import rdflib
from rdflib import RDF, SH

from linkml.generators.shaclgen import ShaclGenerator


@pytest.mark.xfail(reason="Known bug: shapes with same class_uri incorrectly merged")
def test_shacl_distinct_shapes_with_native_names():
    """
    Expected correct behavior:
    When using native names (use_class_uri_names=False), shapes SHOULD be created per LinkML class
    even if class_uri is identical.

    This test documents the intended future behavior and currently fails.
    """

    test_schema = """
id: http://example.org/nonmerge
name: distinct_shape_test
prefixes:
  prov: http://www.w3.org/ns/prov#
default_prefix: http://example.org/test#

imports:
  - linkml:types

classes:
  Entity:
    description: Base entity
    class_uri: prov:Entity
    slots: [a]

  EvaluatedEntity:
    description: Evaluated version
    class_uri: prov:Entity
    slots: [b]

  ThirdEntity:
    description: Third class
    class_uri: prov:Entity
    slots: [c]

slots:
  a:
    range: string
  b:
    range: string
  c:
    range: string
"""

    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(test_schema)
        tmp = f.name

    try:
        shaclstr = ShaclGenerator(
            tmp,
            mergeimports=True,
            use_class_uri_names=False,  # <-- native names → expected behavior: NO MERGE
        ).serialize()

        g = rdflib.Graph()
        g.parse(data=shaclstr, format="turtle")

        shapes = list(g.subjects(RDF.type, SH.NodeShape))

        # EXPECTED: 3 distinct shapes (1 per LinkML class)
        assert len(shapes) == 3, f"Expected 3 separate shapes but found {len(shapes)}"

        # Check that each class name appears in exactly one shape URI
        for cname in ["Entity", "EvaluatedEntity", "ThirdEntity"]:
            matching = [s for s in shapes if cname in str(s)]
            assert len(matching) == 1, f"{cname}: expected 1 shape, found {matching}"

    finally:
        os.unlink(tmp)
