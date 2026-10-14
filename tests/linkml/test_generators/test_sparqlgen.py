from linkml.generators.sparqlgen import SparqlGenerator
from linkml_runtime import SchemaView


def test_sparqlgen(kitchen_sink_path):
    """Generate java classes"""
    gen = SparqlGenerator(kitchen_sink_path)
    sparql = gen.serialize()
    # TODO: add more checks
    assert "?subject rdf:type ks:Person" in sparql


def test_sparqlgen_does_not_mutate_input_schemaview(kitchen_sink_path):
    """
    Materialization must not mutate a caller-supplied schema.

    Regression for #3770: sparqlgen moved ``attributes`` into ``slots`` on the shared schema, so a
    later generator reusing the same SchemaView (e.g. under gen-project) saw its attributes gone.
    """
    sv = SchemaView(kitchen_sink_path)
    before = {cn: len(c.attributes) for cn, c in sv.all_classes().items()}

    SparqlGenerator(sv.schema).serialize()

    after = {cn: len(c.attributes) for cn, c in sv.all_classes().items()}
    assert before == after
    assert any(count > 0 for count in before.values()), "fixture must have attributes to be meaningful"


def test_sparqlgen_path_and_object_inputs_match(kitchen_sink_path):
    """
    Path and pre-parsed-object inputs must produce identical output.

    Regression for #3770: the base ``__post_init__`` rebuilt the SchemaView after materialization,
    so path inputs silently dropped the prefixes materialization adds, yielding SPARQL that
    referenced undeclared prefixes.
    """
    from_path = SparqlGenerator(kitchen_sink_path).serialize()
    from_object = SparqlGenerator(SchemaView(kitchen_sink_path).schema).serialize()
    assert from_path == from_object
    assert "PREFIX rdf:" in from_path
