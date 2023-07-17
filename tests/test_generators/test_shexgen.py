import sys
import unittest

from linkml_runtime.dumpers import json_dumper, rdf_dumper
from linkml_runtime.loaders import yaml_loader
from pyshex.evaluate import evaluate

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.shexgen import ShExGenerator
from tests.test_generators.environment import env
from tests.test_generators.test_pythongen import make_python

SCHEMA = env.input_path("kitchen_sink.yaml")
PYTHON = env.expected_path("kitchen_sink.py")
DATA = env.input_path("kitchen_sink_inst_01.yaml")
SHEXLOG = env.expected_path("shexgen_log.txt")


class ShExTestCase(unittest.TestCase):
    unittest.skipIf(sys.version_info < (3, 8), "ShEx has issues with python 3.7 at the moment")

    def test_shex(self):
        """tests generation of shex and subsequent evaluation"""
        kitchen_module = make_python(SCHEMA, PYTHON, False)
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        shexstr = ShExGenerator(SCHEMA, mergeimports=True).serialize(collections=False)
        self.assertIn("<Person> CLOSED {", shexstr)
        self.assertIn(
            "<has_familial_relationships> @<FamilialRelationship> * ;", shexstr
        )
        self.assertIn("<EmploymentEvent> CLOSED {", shexstr)
        self.assertIn("<type> [ bizcodes:001 bizcodes:002 bizcodes:003 bizcodes:004 ] ?", shexstr)

        # validation
        # TODO: provide starting shape
        ctxt = ContextGenerator(SCHEMA, mergeimports=True).serialize()
        inst = yaml_loader.load(DATA, target_class=kitchen_module.Dataset)
        with open(SHEXLOG, "w") as log:
            log.write(json_dumper.dumps(element=inst, contexts=ctxt))
            try:
                g = rdf_dumper.as_rdf_graph(element=inst, contexts=ctxt)
            except Exception as e:
                if "URL could not be dereferenced" in str(e):
                    print(
                        "WARNING: non-modified version of pyld detected. RDF dumping test skipped"
                    )
                    return
                raise e
            nodes = set()
            for s, p, o in g.triples((None, None, None)):
                nodes.add(s)
            for node in nodes:
                r = evaluate(g, shexstr, focus=node)

                log.write(f"Eval {node} = {r}\n")
                #               start="http://example.org/model/FriendlyPerson",
                #            focus="http://example.org/people/42")


if __name__ == "__main__":
    unittest.main()
