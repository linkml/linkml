import unittest

from rdflib import Graph, XSD

from linkml.generators.rdfgen import RDFGenerator
from linkml_runtime.linkml_model.meta import LINKML
from tests.test_issues.environment import env


class DateTestCase(unittest.TestCase):
    def test_date_time(self):
        """ date datatype should be rdf:date and datetime rdf:datetime """
        rdf = RDFGenerator(env.types_yaml).serialize()
        g = Graph()
        g.parse(data=rdf, format="turtle")
        self.assertEqual(XSD.date, g.value(LINKML.date, LINKML.uri))
        self.assertEqual(XSD.dateTime, g.value(LINKML.datetime, LINKML.uri))


if __name__ == '__main__':
    unittest.main()
