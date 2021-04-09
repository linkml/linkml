import os
import unittest

from rdflib import URIRef, Graph
from rdflib.namespace import OWL, RDFS, RDF

from linkml.generators.flattener import Flattener
from linkml.generators.sqlddlgen import SQLDDLGenerator
from linkml.generators.yamlgen import YAMLGenerator
from linkml.generators.yamlgen import YAMLGenerator
#from linkml.utils.sqlutils import SqlTransformer
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class IssueSQLGenTestCase(TestEnvironmentTestCase):
    env = env


    def test_sqlddlgen(self):
        PATH = env.input_path('issue_288.yaml')
        ddl = SQLDDLGenerator(PATH, dialect='mssql+pyodbc').serialize()
        with open(env.input_path('issue_288.sql'), "w") as io:
            io.write(ddl)
        print(ddl)





if __name__ == '__main__':
    unittest.main()
