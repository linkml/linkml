import json
import unittest
from typing import Type

import jsonschema
import yaml
import jsonasobj2
from linkml_runtime.linkml_model import SchemaDefinition

from linkml_runtime.utils.yamlutils import as_dict, YAMLRoot
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.dumpers import rdf_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.utils.validation import validate_object
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path('kitchen_sink.yaml')
CONTEXT_OUT = env.expected_path('kitchen_sink.context.jsonld')
PYTHON = env.expected_path('kitchen_sink.py')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
FAILDATA = env.input_path('kitchen_sink_failtest_inst_01.yaml')
DATA_JSON = env.expected_path('kitchen_sink_inst_01.json')
DATA_RDF = env.expected_path('kitchen_sink_inst_01.rdf')
FAILLOG = env.expected_path('kitchen_sink_failtest_log.txt')



class ContextTestCase(unittest.TestCase):
    def test_context(self):
        """ json schema """
        kitchen_module = make_python(False)
        inst: Dataset
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        json_dumper.dump(element=inst, to_file=DATA_JSON)
        with open(CONTEXT_OUT, 'w') as stream:
            stream.write(ContextGenerator(SCHEMA).serialize())
        print(rdf_dumper.dumps(inst, CONTEXT_OUT))


if __name__ == '__main__':
    unittest.main()
