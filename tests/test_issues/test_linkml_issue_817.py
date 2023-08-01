from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders import yaml_loader

from linkml.generators.pythongen import PythonGenerator


def _roundtrip(obj, tc):
    v = yaml_dumper.dumps(obj)
    obj2 = yaml_loader.loads(v, target_class=tc)
    assert obj == obj2
    return obj2


def test_inline(input_path):
    """
    Tests https://github.com/linkml/linkml/issues/817
    """
    name = "linkml_issue_817"
    infile = input_path(f"{name}.yaml")
    pygen = PythonGenerator(infile)
    mod = pygen.compile_module()
    p = mod.Person(id="x", name="x", vital_status=mod.VitalStatusEnum("LIVING"))
    c = mod.Container()
    c.persons_as_list = [p]
    # c.persons_as_dict = {p.id: p}
    _roundtrip(c, mod.Container)
    c = mod.Container(persons_as_list=[p], persons_as_dict=[p])
    assert c.persons_as_dict[p.id].name == p.name
    c2 = _roundtrip(c, mod.Container)
    assert c2.persons_as_dict[p.id].name == p.name
