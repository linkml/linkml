import unittest

from linkml_runtime import LINKML
from linkml_runtime.utils.compile_python import compile_python
from pydantic import ValidationError
from rdflib import OWL, RDF, RDFS, SKOS, XSD, Literal, Namespace, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator
from linkml.generators.pydanticgen import PydanticGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase

SCHEMA = env.input_path("personinfo.yaml")

PERSONINFO = Namespace("https://w3id.org/linkml/examples/personinfo/")
SCHEMA_HTTP = Namespace("http://schema.org/")


class Issue1463ConstCase(TestEnvironmentTestCase):
    env = env

    def test_owlgen_personinfo(self):
        """
        Test for https://github.com/linkml/linkml/issues/1463

        Ensures that OWL export is valid for personinfo
        """
        for opts in [{}, {"type_objects": False, "metaclasses": False}]:
            gen = OwlSchemaGenerator(SCHEMA, **opts)
            _ = gen.serialize()
            g = gen.graph
            # container metaslots are intentionally excluded from OWL export
            for metaslot in [LINKML.classes, LINKML.enums, LINKML.types]:
                self.assertEqual([], list(g.triples((None, metaslot, None))))
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
                self.assertIn(t, g)
            for t in g.triples((PERSONINFO.age_in_years, None, None)):
                print(t)


if __name__ == "__main__":
    unittest.main()
