import sys
import unittest

from linkml_runtime.dumpers import rdf_dumper, json_dumper
from linkml_runtime.loaders import yaml_loader
#from pyshacl.evaluate import evaluate

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.shaclgen import ShaclGenerator
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path('kitchen_sink.yaml')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
LOG = env.expected_path('ShaclGen_log.txt')
OUT = env.expected_path('kitchen_sink.shacl.ttl')


class ShaclTestCase(unittest.TestCase):

    def test_shacl(self):
        """ shacl  """
        shaclstr = ShaclGenerator(SCHEMA, mergeimports=True).serialize()
        with open(OUT, 'w') as stream:
            stream.write(shaclstr)
        # TODO: test shacl validation; pyshacl requires rdflib6



if __name__ == '__main__':
    unittest.main()
