import json
import unittest

import jsonschema
import yaml
from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path('kitchen_sink.yaml')
JSONSCHEMA_OUT = env.expected_path('kitchen_sink.schema.json')
PYTHON = env.expected_path('kitchen_sink.py')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
FAILDATA = env.input_path('kitchen_sink_failtest_inst_01.yaml')
DATA_JSON = env.expected_path('kitchen_sink_inst_01.json')


class JsonSchemaTestCase(unittest.TestCase):
    def test_jsonschema(self):
        """ json schema """
        kitchen_module = make_python(False)
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
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
            is_skip = failobj.get('skip', False)
            #print(f'[{is_skip}] Testing {failobj["description"]} {dataset}')
            is_fail = False
            try:
                jsonschema.validate(dataset, schema=jsonschema_obj)
                is_fail = False
            except:
                is_fail = True
            #print(f'Detected error: {is_fail}')
            if not is_skip:
                assert is_fail





if __name__ == '__main__':
    unittest.main()
