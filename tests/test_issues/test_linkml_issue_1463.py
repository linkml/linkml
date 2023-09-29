import pytest
from linkml_runtime import LINKML
from rdflib import OWL, RDF, RDFS, SKOS, Literal, Namespace, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator

PERSONINFO = Namespace("https://w3id.org/linkml/examples/personinfo/")
SCHEMA_HTTP = Namespace("http://schema.org/")


@pytest.mark.parametrize("type_objects,metaclasses", [(True, True), (False, False)])
def test_owlgen_personinfo(input_path, type_objects, metaclasses):
    """
    Test for https://github.com/linkml/linkml/issues/1463

    Ensures that OWL export is valid for personinfo
    """
    SCHEMA = input_path("personinfo.yaml")
    gen = OwlSchemaGenerator(SCHEMA, type_objects=type_objects, metaclasses=metaclasses)
    _ = gen.serialize()
    g = gen.graph
    # container metaslots are intentionally excluded from OWL export
    for metaslot in [LINKML.classes, LINKML.enums, LINKML.types]:
        assert [] == list(g.triples((None, metaslot, None)))
    expected = [
        (PERSONINFO.Address, RDFS.label, Literal("Address")),
        (PERSONINFO.Address, SKOS.exactMatch, SCHEMA_HTTP.PostalAddress),
        (
            PERSONINFO.FamilialRelationshipType,
            LINKML.permissible_values,
            URIRef("https://example.org/FamilialRelations#03"),
        ),
        (PERSONINFO.FamilialRelationshipType, RDF.type, OWL.Class),
        (PERSONINFO.employed_at, RDF.type, OWL.ObjectProperty),
        (
            PERSONINFO.current_address,
            SKOS.definition,
            Literal("The address at which a person currently lives"),
        ),
    ]
    # TODO: check expressions
    if type_objects:
        expected.extend(
            [
                (PERSONINFO.age_in_years, RDF.type, OWL.ObjectProperty),
                # (PERSONINFO.age_in_years, RDFS.range, LINKML.Integer),
            ]
        )
    else:
        expected.extend(
            [
                (PERSONINFO.age_in_years, RDF.type, OWL.DatatypeProperty),
                # (PERSONINFO.age_in_years, RDFS.range, XSD.integer),
            ]
        )
    for t in expected:
        assert t in g
