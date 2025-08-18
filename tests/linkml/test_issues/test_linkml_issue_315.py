from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


# Tests: https://github.com/linkml/linkml/issues/314
def test_keyval(input_path):
    name = "linkml_issue_315"
    inpath = input_path(f"{name}.yaml")
    gen = PythonGenerator(inpath, mergeimports=True)
    pstr = str(gen.serialize())
    mod = compile_python(pstr)
    d1 = mod.Container(word_mappings={"hand": "manus"})
    assert d1.word_mappings["hand"] == mod.WordMapping(src="hand", tgt="manus")
    obj = yaml_loader.load(input_path(f"{name}_data.yaml"), target_class=mod.Container)
    assert obj.word_mappings["foot"] == mod.WordMapping(src="foot", tgt="pes")
