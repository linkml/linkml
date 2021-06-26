import unittest

from linkml_runtime.loaders import yaml_loader, json_loader, rdf_loader
from linkml_runtime.dumpers import json_dumper
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.pythongen import PythonGenerator
from tests.test_generators.environment import env
from importlib import import_module
import jsonschema
import json
import yaml
#from kitchen_sink import *
from output.kitchen_sink import *

SCHEMA = env.input_path('kitchen_sink.yaml')
JSONSCHEMA_OUT = env.expected_path('kitchen_sink.schema.json')
PYTHON = env.expected_path('kitchen_sink.py')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
FAILDATA = env.input_path('kitchen_sink_failtest_inst_01.yaml')
DATA_JSON = env.expected_path('kitchen_sink_inst_01.json')

def make_python() -> None:
    """
    Note: if you change the yaml schema and associated test instance objects,
    you may need to run this test twice
    """
    pstr = str(PythonGenerator(SCHEMA, mergeimports=True).serialize())
    #eval(compile(pstr))
    with open(PYTHON, 'w') as io:
        io.write(pstr)
    c = Company('ROR:1')
    h = EmploymentEvent(employed_at=c.id)
    p = Person('P:1', has_employment_history=[h])

class JsonSchemaTestCase(unittest.TestCase):
    def test_jsonschem(self):
        """ json schema """
        make_python()
        inst = yaml_loader.load(DATA, target_class=Dataset)
        json_dumper.dump(element=inst, to_file=DATA_JSON)
        inst_dict = json.loads(json_dumper.dumps(element=inst))
        jsonschemastr = JsonSchemaGenerator(SCHEMA, mergeimports=True, top_class='Dataset').serialize()
        with open(JSONSCHEMA_OUT, 'w') as io:
            io.write(jsonschemastr)
        jsonschema_obj = json.loads(jsonschemastr)
        jsonschema.validate(inst_dict, schema=jsonschema_obj)
        #print(f'S={jsonschema}')

        with open(FAILDATA, 'r') as io:
            failobjs = yaml.load(io)
        for failobj in failobjs:
            dataset = failobj['dataset']
            print(f'Testing {failobj["description"]} {dataset}')
            is_fail = False
            try:
                jsonschema.validate(dataset, schema=jsonschema_obj)
                is_fail = False
            except:
                is_fail = True
            assert is_fail





if __name__ == '__main__':
    unittest.main()
