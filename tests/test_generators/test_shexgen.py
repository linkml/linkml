import sys

import pytest
from linkml_runtime.dumpers import json_dumper, rdf_dumper
from linkml_runtime.loaders import yaml_loader
from pyshex.evaluate import evaluate

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.shexgen import ShExGenerator
from tests.test_generators.test_pythongen import make_python


@pytest.mark.skipif(sys.version_info < (3, 8), reason="ShEx has issues with python 3.7 at the moment")
def test_shex(kitchen_sink_path, input_path, tmp_path):
    """tests generation of shex and subsequent evaluation"""
    kitchen_module = make_python(kitchen_sink_path)
    data = input_path("kitchen_sink_inst_01.yaml")
    inst = yaml_loader.load(data, target_class=kitchen_module.Dataset)
    shexstr = ShExGenerator(kitchen_sink_path, mergeimports=True).serialize(collections=False)
    assert "<Person> CLOSED {" in shexstr
    assert "<has_familial_relationships> @<FamilialRelationship> * ;" in shexstr
    # re-enable below test when linkml/linkml#1914 is fixed
    # assert "<type> [ bizcodes:001 bizcodes:002 bizcodes:003 bizcodes:004 ] ?" in shexstr
    # validation
    # TODO: provide starting shape
    ctxt = ContextGenerator(kitchen_sink_path, mergeimports=True).serialize()
    inst = yaml_loader.load(data, target_class=kitchen_module.Dataset)

    # TODO: turn this into an actual test
    with open(tmp_path / "shexgen_log.txt", "w") as log:
        log.write(json_dumper.dumps(element=inst, contexts=ctxt))
        try:
            g = rdf_dumper.as_rdf_graph(element=inst, contexts=ctxt)
        except Exception as e:
            if "URL could not be dereferenced" in str(e):
                print("WARNING: non-modified version of pyld detected. RDF dumping test skipped")
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
