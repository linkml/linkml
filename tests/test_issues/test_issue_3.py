import unittest

from rdflib import Graph, XSD

from linkml.generators.rdfgen import RDFGenerator
from linkml.meta import META
from includes.types import METATYPE
from tests.test_issues.environment import env


class DateTestCase(unittest.TestCase):
    def test_date_time(self):
        """ date datatype should be rdf:date and datetime rdf:datetime """
        rdf = RDFGenerator(env.types_yaml).serialize()
        g = Graph()
        g.parse(data=rdf, format="turtle")
        self.assertEqual(XSD.date, g.value(METATYPE.date, META.uri))
        self.assertEqual(XSD.dateTime, g.value(METATYPE.datetime, META.uri))


if __name__ == '__main__':
    unittest.main()
