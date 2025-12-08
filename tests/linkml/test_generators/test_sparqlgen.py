from linkml.generators.sparqlgen import SparqlGenerator


def test_sparqlgen(kitchen_sink_path):
    """Generate java classes"""
    gen = SparqlGenerator(kitchen_sink_path)
    sparql = gen.serialize()
    # TODO: add more checks
    assert "?subject rdf:type ks:Person" in sparql
