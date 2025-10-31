import json

import pytest
from rdflib import RDFS, Graph, Literal, URIRef


@pytest.mark.parametrize(
    "prefix,version,expected",
    [
        (False, "1.1", True),
        (True, "1.1", True),
        (False, "1.0", False),
        (True, "1.0", False),
    ],
)
def test_jsonld_prefix(prefix, version, expected):
    """
    Test JSON-LD prefix serialization.

    Original: `<https://github.com/biolink/biolinkml/issues/414>`_
    Moved to: `<https://github.com/linkml/linkml/issues/25>`_

    See also: `<https://github.com/RDFLib/rdflib/issues/2606>`_

    :param prefix: Whether to include prefixes in the JSON-LD serialization (seems to have no effect)
    :param version: JSON-LD version
    :param expected: Whether it is expected that the CHEBI prefix is expanded correctly
    """
    test_json = """
    {
        "@context": {
            "CHEBI": {
                "@id": "http://purl.obolibrary.org/obo/CHEBI_",
                "@prefix": true
            },
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "owl": "http://www.w3.org/2002/07/owl#",
            "@vocab": "http://example.org/"
        },
        "terms": [
            {
                "@id": "CHEBI:33709",
                "@type": "owl:Class",
                "rdfs:label": "Amino Acid"
            }
        ]
    }
    """
    context = json.loads(test_json)["@context"]
    g = Graph().parse(data=test_json, format="json-ld", version=version, prefix=prefix)
    bindings = list(g.namespace_manager.namespaces())
    for prefix, expansion in bindings:
        # rdflib is not guaranteed to preserve bindings
        if prefix == "CHEBI":
            assert expansion == URIRef("http://purl.obolibrary.org/obo/CHEBI_")

    if expected:
        assert (URIRef("http://purl.obolibrary.org/obo/CHEBI_33709"), RDFS.label, Literal("Amino Acid")) in g
    g.bind("CHEBI", "http://purl.obolibrary.org/obo/CHEBI_")
    jsonld = g.serialize(format="json-ld", version=version, prefix=prefix, context=context)
    if expected:
        # TODO: determine if it's possible to do this
        # assert '"CHEBI:33709"' in jsonld
        assert '"CHEBI:33709"' in jsonld or '"http://purl.obolibrary.org/obo/CHEBI_33709"' in jsonld
