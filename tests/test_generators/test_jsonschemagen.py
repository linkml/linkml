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
FAILLOG = env.expected_path('kitchen_sink_failtest_log.txt')


class JsonSchemaTestCase(unittest.TestCase):
    def test_jsonschema(self):
        """ json schema """
        kitchen_module = make_python(False)
        inst: Dataset
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        #p = [p for p in persons if p.id == 'P:002'][0]
        for p in inst.persons:
            for a in p.addresses:
                print(f'{p.id} address = {a.street}')
        json_dumper.dump(element=inst, to_file=DATA_JSON)
        inst_dict = json.loads(json_dumper.dumps(element=inst))
        jsonschemastr = JsonSchemaGenerator(SCHEMA, mergeimports=True, top_class='Dataset').serialize()
        with open(JSONSCHEMA_OUT, 'w') as io:
            io.write(jsonschemastr)
        jsonschema_obj = json.loads(jsonschemastr)
        jsonschema.validate(inst_dict, schema=jsonschema_obj)
        #print(f'S={jsonschema}')

        # test for expected failures
        # FAILDATA contains a set of json objects each of which
        # violates the schema in some way
        with open(FAILDATA, 'r') as io:
            failobjs = yaml.load(io, Loader=yaml.loader.SafeLoader)

        with open(FAILLOG, 'w') as log:
            for failobj in failobjs:
                dataset = failobj['dataset']
                is_skip = failobj.get('skip', False)
                log.write('-' * 20)
                log.write(f"\n{failobj['description']}:\n")
                log.write(f"\n{failobj['dataset']}:\n")
                if not is_skip:
                    with self.assertRaises(Exception) as e:
                        jsonschema.validate(dataset, schema=jsonschema_obj)
                    log.write(f"\nEXPECTED FAILURE: {type(e.exception)}:\n\t{e.exception}\n\n")
                else:
                    log.write(" SKIPPED\n")


if __name__ == '__main__':
    unittest.main()
