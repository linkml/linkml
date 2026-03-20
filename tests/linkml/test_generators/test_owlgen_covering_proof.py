"""Standalone proof that the single-child covering axiom bug reverses OWL class hierarchies.

This module demonstrates the bug independently of any domain ontology (Gaia-X, harbour, etc.)
using a minimal 3-class schema and RDFS inference.

Bug summary
-----------
When an abstract class has exactly **one** direct ``is_a`` child, the OWL generator's
covering axiom code path calls ``_union_of([single_child])``.  The ``_boolean_expression``
helper optimises single-element lists by returning the URI directly instead of wrapping it
in ``owl:unionOf``.  The result is an unqualified triple::

    AbstractParent  rdfs:subClassOf  OnlyChild

Combined with the already-present ``OnlyChild rdfs:subClassOf AbstractParent`` (from the
``is_a`` declaration), this creates a **bidirectional** ``rdfs:subClassOf`` — which, per
the W3C OWL 2 Primer §4.2, is semantically identical to ``owl:equivalentClass``::

    "Stating that Person and Human are equivalent amounts exactly to the same as
     stating that both Person is a subclass of Human and Human is a subclass of
     Person."
    — https://www.w3.org/TR/owl2-primer/#Class_Hierarchies

This unintended equivalence means that **any** class later added as a second child of the
abstract parent will, via RDFS transitivity, become a subclass of the first child — inheriting
all of its constraints.

The fix is to skip the covering axiom when ``len(children) == 1``, because:

1.  A single-element union is semantically identical to the element itself
    (``A ⊑ unionOf(B)`` ≡ ``A ⊑ B``), so the axiom degenerates to equivalence.
2.  OWL 2 provides ``DisjointUnion`` (§9.1.4) as the proper construct for covering
    constraints; using ``rdfs:subClassOf`` + ``owl:unionOf`` is an approximation that
    only adds information when there are ≥ 2 children.
3.  An abstract class with one child is typically an incomplete ontology awaiting extension;
    asserting equivalence precludes safe extension.

References
----------
- W3C OWL 2 Primer §4.2 (Class Hierarchies):
  https://www.w3.org/TR/owl2-primer/#Class_Hierarchies
- W3C OWL 2 Structural Specification §9.1.1 (Subclass Axioms):
  https://www.w3.org/TR/owl2-syntax/#Subclass_Axioms
- W3C OWL 2 Structural Specification §9.1.4 (Disjoint Union):
  https://www.w3.org/TR/owl2-syntax/#Disjoint_Union_of_Class_Expressions
- W3C OWL 2 New Features §2.1.1 (F1: DisjointUnion):
  https://www.w3.org/TR/owl2-new-features/#F1:_DisjointUnion
"""

from rdflib import RDFS, Graph, Namespace, URIRef
from rdflib.collection import Collection
from rdflib.namespace import OWL, RDF

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.utils.schema_builder import SchemaBuilder

# SchemaBuilder.add_defaults() sets id/prefix to http://example.org/test-schema/
EX = Namespace("http://example.org/test-schema/")


# ---------------------------------------------------------------------------
# Helper: build a SchemaBuilder with a 3-level hierarchy
# ---------------------------------------------------------------------------


def _build_single_child_schema() -> SchemaBuilder:
    """GrandParent → Parent (abstract) → Child.

    Only one ``is_a`` child of ``Parent``, which triggers the bug.
    """
    sb = SchemaBuilder()
    sb.add_class("GrandParent")
    sb.add_class("Parent", is_a="GrandParent", abstract=True)
    sb.add_class("Child", is_a="Parent")
    sb.add_defaults()
    return sb


def _build_two_child_schema() -> SchemaBuilder:
    """GrandParent → Parent (abstract) → {ChildA, ChildB}.

    Two children — the covering axiom is valid here.
    """
    sb = SchemaBuilder()
    sb.add_class("GrandParent")
    sb.add_class("Parent", is_a="GrandParent", abstract=True)
    sb.add_class("ChildA", is_a="Parent")
    sb.add_class("ChildB", is_a="Parent")
    sb.add_defaults()
    return sb


def _owl_graph(sb: SchemaBuilder, **kwargs) -> Graph:
    gen = OwlSchemaGenerator(sb.schema, mergeimports=True, **kwargs)
    ttl = gen.serialize()
    g = Graph()
    g.parse(data=ttl, format="turtle")
    return g


def _union_members(g: Graph, cls_uri: URIRef):
    """Return the set of URIs in the owl:unionOf list for a covering axiom, or None."""
    for obj in g.objects(cls_uri, RDFS.subClassOf):
        for union_list in g.objects(obj, OWL.unionOf):
            return set(Collection(g, union_list))
    return None


# ---------------------------------------------------------------------------
# Test 1: The bug — single child must NOT produce a reversed subClassOf
# ---------------------------------------------------------------------------


class TestSingleChildCoveringAxiomBug:
    """Prove that the single-child covering axiom creates an unintended equivalence."""

    def test_no_reversed_subclassof(self):
        """Parent must NOT be a subclass of Child."""
        g = _owl_graph(_build_single_child_schema())

        assert (EX.Parent, RDFS.subClassOf, EX.Child) not in g, (
            "BUG: Abstract class with single child got a covering axiom that "
            "reverses the hierarchy (Parent rdfs:subClassOf Child). "
            "See W3C OWL 2 Primer §4.2: bidirectional SubClassOf = EquivalentClasses."
        )

    def test_correct_hierarchy_preserved(self):
        """The intended is_a hierarchy must still be present."""
        g = _owl_graph(_build_single_child_schema())

        assert (EX.Child, RDFS.subClassOf, EX.Parent) in g, "Child rdfs:subClassOf Parent must be present (from is_a)"
        assert (EX.Parent, RDFS.subClassOf, EX.GrandParent) in g, (
            "Parent rdfs:subClassOf GrandParent must be present (from is_a)"
        )

    def test_no_union_of_for_single_child(self):
        """No owl:unionOf wrapper should exist for a single-element covering axiom."""
        g = _owl_graph(_build_single_child_schema())
        assert _union_members(g, EX.Parent) is None

    def test_equivalence_proof_via_rdfs_transitivity(self):
        """Demonstrate the real-world impact: a second child inherits constraints
        of the first child via the unintended equivalence.

        Schema under test (simulating extensible ontology):
            GrandParent
            └── Parent (abstract)    ← if bug: Parent ≡ Child
                └── Child            ← has slot 'registration_number' (required)
                └── Child2           ← added by downstream schema; should NOT need registration_number

        With the bug:
            Child2 ⊆ Parent ≡ Child  ⟹  Child2 ⊆ Child  (WRONG)

        Without the bug:
            Child2 ⊆ Parent ⊆ GrandParent  (CORRECT — no relation to Child)
        """
        g = _owl_graph(_build_single_child_schema())

        # Simulate a downstream extension adding Child2 is_a Parent
        g.add((EX.Child2, RDF.type, OWL.Class))
        g.add((EX.Child2, RDFS.subClassOf, EX.Parent))

        # Check RDFS transitivity: does Child2 end up as subclass of Child?
        child2_supers = set()
        # Walk 2 levels of rdfs:subClassOf (sufficient for this test)
        for mid in g.objects(EX.Child2, RDFS.subClassOf):
            child2_supers.add(mid)
            for top in g.objects(mid, RDFS.subClassOf):
                child2_supers.add(top)

        assert EX.Child not in child2_supers, (
            "BUG: Child2 (added by downstream schema) became a subclass of Child "
            "via the unintended equivalence Parent ≡ Child. "
            "This means Child2 would inherit all of Child's constraints."
        )
        # Correct: Child2 should only reach Parent and GrandParent
        assert EX.Parent in child2_supers
        assert EX.GrandParent in child2_supers


# ---------------------------------------------------------------------------
# Test 2: Multi-child covering axiom still works correctly
# ---------------------------------------------------------------------------


class TestMultiChildCoveringAxiom:
    """Covering axiom with ≥ 2 children is valid and must still be emitted."""

    def test_union_of_emitted(self):
        """Abstract class with 2 children gets a proper owl:unionOf covering axiom."""
        g = _owl_graph(_build_two_child_schema())
        members = _union_members(g, EX.Parent)
        assert members is not None, "Covering axiom missing for abstract class with 2 children"
        assert members == {EX.ChildA, EX.ChildB}

    def test_no_direct_subclassof_to_individual_child(self):
        """The covering axiom must be a union, not a direct subClassOf to any single child."""
        g = _owl_graph(_build_two_child_schema())
        assert (EX.Parent, RDFS.subClassOf, EX.ChildA) not in g
        assert (EX.Parent, RDFS.subClassOf, EX.ChildB) not in g

    def test_correct_hierarchy_preserved(self):
        g = _owl_graph(_build_two_child_schema())
        assert (EX.ChildA, RDFS.subClassOf, EX.Parent) in g
        assert (EX.ChildB, RDFS.subClassOf, EX.Parent) in g
        assert (EX.Parent, RDFS.subClassOf, EX.GrandParent) in g


# ---------------------------------------------------------------------------
# Test 3: Skip flag suppresses all covering axioms
# ---------------------------------------------------------------------------


class TestSkipFlag:
    """The skip_abstract_class_as_unionof_subclasses flag must suppress all cases."""

    def test_skip_single_child(self):
        g = _owl_graph(_build_single_child_schema(), skip_abstract_class_as_unionof_subclasses=True)
        assert (EX.Parent, RDFS.subClassOf, EX.Child) not in g
        assert _union_members(g, EX.Parent) is None

    def test_skip_multi_child(self):
        g = _owl_graph(_build_two_child_schema(), skip_abstract_class_as_unionof_subclasses=True)
        assert _union_members(g, EX.Parent) is None
        assert (EX.Parent, RDFS.subClassOf, EX.ChildA) not in g
        assert (EX.Parent, RDFS.subClassOf, EX.ChildB) not in g
