from linkml_runtime import LINKML
from rdflib import OWL, RDF, RDFS, SKOS, XSD, Literal, Namespace, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator

PERSONINFO = Namespace("https://w3id.org/linkml/examples/personinfo/")
SCHEMA_HTTP = Namespace("http://schema.org/")


def test_owlgen_personinfo(input_path):
    """
    Test for https://github.com/linkml/linkml/issues/1463

    Ensures that OWL export is valid for personinfo
    """
    SCHEMA = input_path("personinfo.yaml")
    for opts in [{}, {"type_objects": False, "metaclasses": False}]:
        gen = OwlSchemaGenerator(SCHEMA, **opts)
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
        if opts.get("type_objects", True):
            expected.extend(
                [
                    (PERSONINFO.age_in_years, RDF.type, OWL.ObjectProperty),
                    (PERSONINFO.age_in_years, RDFS.range, LINKML.Integer),
                ]
            )
        else:
            expected.extend(
                [
                    (PERSONINFO.age_in_years, RDF.type, OWL.DatatypeProperty),
                    (PERSONINFO.age_in_years, RDFS.range, XSD.integer),
                ]
            )
        for t in expected:
            assert t in g
