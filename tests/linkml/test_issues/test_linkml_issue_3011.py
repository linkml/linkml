"""
Tests for issue #3011: SHACL class merging with shared class_uri.

These tests verify that the use_class_uri_names parameter works correctly
to prevent unintentional shape merging when multiple LinkML classes share
the same class_uri.
"""

import rdflib
from rdflib import RDF, SH

from linkml.generators.shaclgen import ShaclGenerator


def test_shacl_distinct_shapes_with_native_names(tmp_path):
    """
    Test for issue #3011: Distinct shapes with native names.

    When using native names (use_class_uri_names=False), shapes are created per LinkML class
    even if class_uri is identical.
    """
    test_schema = """
id: http://example.org/nonmerge
name: distinct_shape_test
prefixes:
  prov: http://www.w3.org/ns/prov#
  linkml: https://w3id.org/linkml/
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
    schema_path = tmp_path / "test_schema.yaml"
    schema_path.write_text(test_schema)

    shaclstr = ShaclGenerator(
        str(schema_path),
        mergeimports=True,
        use_class_uri_names=False,
    ).serialize()

    g = rdflib.Graph()
    g.parse(data=shaclstr, format="turtle")

    shapes = list(g.subjects(RDF.type, SH.NodeShape))

    # EXPECTED: 3 distinct shapes (1 per LinkML class)
    assert len(shapes) == 3, f"Expected 3 separate shapes but found {len(shapes)}"

    # Check that each class name appears as the shape URI suffix (after the colon)
    for cname in ["Entity", "EvaluatedEntity", "ThirdEntity"]:
        matching = [s for s in shapes if str(s).endswith(f":{cname}")]
        assert len(matching) == 1, f"{cname}: expected 1 shape, found {matching}"


def test_shacl_target_class_correct_with_native_names(tmp_path):
    """
    Test that sh:targetClass is correctly set to the class_uri even when using native names.

    This ensures that shapes are named by the LinkML class name but still correctly
    target the appropriate RDF class (class_uri).
    """
    test_schema = """
id: http://example.org/targettest
name: target_class_test
prefixes:
  prov: http://www.w3.org/ns/prov#
  linkml: https://w3id.org/linkml/
default_prefix: http://example.org/test#

imports:
  - linkml:types

classes:
  Entity:
    class_uri: prov:Entity
    slots: [name]

  EvaluatedEntity:
    class_uri: prov:Entity
    slots: [score]

slots:
  name:
    range: string
  score:
    range: string
"""
    schema_path = tmp_path / "test_schema.yaml"
    schema_path.write_text(test_schema)

    shaclstr = ShaclGenerator(
        str(schema_path),
        mergeimports=True,
        use_class_uri_names=False,
    ).serialize()

    g = rdflib.Graph()
    g.parse(data=shaclstr, format="turtle")

    prov_entity = rdflib.URIRef("http://www.w3.org/ns/prov#Entity")

    # Both shapes should have sh:targetClass pointing to prov:Entity
    shapes_targeting_prov = list(g.subjects(SH.targetClass, prov_entity))
    assert len(shapes_targeting_prov) == 2, (
        f"Expected 2 shapes targeting prov:Entity, found {len(shapes_targeting_prov)}"
    )

    # Verify shape names are based on LinkML class names
    shape_names = {str(s) for s in shapes_targeting_prov}
    assert any(s.endswith(":Entity") for s in shape_names)
    assert any(s.endswith(":EvaluatedEntity") for s in shape_names)


def test_shacl_inheritance_with_shared_class_uri(tmp_path):
    """
    Test that inheritance (is_a) works correctly with shared class_uri.

    When a child class inherits from a parent with a shared class_uri,
    native names mode should still produce distinct shapes.
    """
    test_schema = """
id: http://example.org/inheritance
name: inheritance_test
prefixes:
  schema: http://schema.org/
  linkml: https://w3id.org/linkml/
default_prefix: http://example.org/test#

imports:
  - linkml:types

classes:
  BaseThing:
    class_uri: schema:Thing
    slots: [name]

  ExtendedThing:
    class_uri: schema:Thing
    is_a: BaseThing
    slots: [description]

  DerivedFromExtended:
    is_a: ExtendedThing
    slots: [extra]

slots:
  name:
    range: string
  description:
    range: string
  extra:
    range: string
"""
    schema_path = tmp_path / "test_schema.yaml"
    schema_path.write_text(test_schema)

    shaclstr = ShaclGenerator(
        str(schema_path),
        mergeimports=True,
        use_class_uri_names=False,
    ).serialize()

    g = rdflib.Graph()
    g.parse(data=shaclstr, format="turtle")

    shapes = list(g.subjects(RDF.type, SH.NodeShape))

    # Should have 3 distinct shapes
    assert len(shapes) == 3, f"Expected 3 shapes, found {len(shapes)}"

    # Verify each LinkML class has its own shape
    shape_names = {str(s) for s in shapes}
    assert any(s.endswith(":BaseThing") for s in shape_names)
    assert any(s.endswith(":ExtendedThing") for s in shape_names)
    assert any(s.endswith(":DerivedFromExtended") for s in shape_names)


def test_shacl_mixin_with_shared_class_uri(tmp_path):
    """
    Test that mixins work correctly with shared class_uri.

    Mixins that share a class_uri should still produce distinct shapes
    when using native names mode.
    """
    test_schema = """
id: http://example.org/mixin
name: mixin_test
prefixes:
  schema: http://schema.org/
  linkml: https://w3id.org/linkml/
default_prefix: http://example.org/test#

imports:
  - linkml:types

classes:
  Identifiable:
    mixin: true
    class_uri: schema:Thing
    slots: [id]

  Named:
    mixin: true
    class_uri: schema:Thing
    slots: [name]

  ConcreteEntity:
    mixins:
      - Identifiable
      - Named
    slots: [data]

slots:
  id:
    range: string
  name:
    range: string
  data:
    range: string
"""
    schema_path = tmp_path / "test_schema.yaml"
    schema_path.write_text(test_schema)

    shaclstr = ShaclGenerator(
        str(schema_path),
        mergeimports=True,
        use_class_uri_names=False,
    ).serialize()

    g = rdflib.Graph()
    g.parse(data=shaclstr, format="turtle")

    shapes = list(g.subjects(RDF.type, SH.NodeShape))

    # Should have 3 distinct shapes (2 mixins + 1 concrete)
    assert len(shapes) == 3, f"Expected 3 shapes, found {len(shapes)}"

    # Verify each LinkML class has its own shape
    shape_names = {str(s) for s in shapes}
    assert any(s.endswith(":Identifiable") for s in shape_names)
    assert any(s.endswith(":Named") for s in shape_names)
    assert any(s.endswith(":ConcreteEntity") for s in shape_names)

    # Verify mixin shapes are marked as not closed (sh:closed false)
    for shape in shapes:
        shape_name = str(shape)
        closed_values = list(g.objects(shape, SH.closed))
        if ":Identifiable" in shape_name or ":Named" in shape_name:
            assert any(v.toPython() is False for v in closed_values), (
                f"Mixin shape {shape_name} should have sh:closed false"
            )
