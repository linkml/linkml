import unittest

from linkml_runtime.dumpers import rdf_dumper, json_dumper
from linkml_runtime.loaders import yaml_loader
from pyshex.evaluate import evaluate

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.shexgen import ShExGenerator
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path('kitchen_sink.yaml')
JSONSCHEMA_OUT = env.expected_path('kitchen_sink.schema.json')
DATA = env.input_path('kitchen_sink_inst_01.yaml')
FAILDATA = env.input_path('kitchen_sink_failtest_inst_01.yaml')
DATA_JSON = env.expected_path('kitchen_sink_inst_01.json')


class ShExTestCase(unittest.TestCase):
    def test_shex(self):
        """ shex  """
        kitchen_module = make_python(False)
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        shexstr = ShExGenerator(SCHEMA, mergeimports=True).serialize(collections=False)
        #print(shexstr)
        ctxt = ContextGenerator(SCHEMA, mergeimports=True).serialize()
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        print(json_dumper.dumps(element=inst, contexts=ctxt))
        g = rdf_dumper.as_rdf_graph(element=inst, contexts=ctxt)
        #print(g)
        nodes = set()
        for (s,p,o) in g.triples((None, None, None)):
            #print(f'{s} {p} {o}')
            nodes.add(s)
        for node in nodes:
            r = evaluate(g, shexstr,
                         focus=node)
            print(f'Eval {node} = {r}')
        #               start="http://example.org/model/FriendlyPerson",
        #            focus="http://example.org/people/42")





if __name__ == '__main__':
    unittest.main()
