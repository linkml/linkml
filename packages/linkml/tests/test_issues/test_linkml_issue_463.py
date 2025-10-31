from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator

data_str = """
contains:
 - label: n1
   type:
     label: n1 label
     system: n1 system
 - label: n2
   type:
     label: n2 label
     system: n2 system
"""


def test_inlined(input_path):
    """Ensure that inlined lists without identifiers work"""
    gen = PythonGenerator(input_path("linkml_issue_463.yaml"))
    pystr = gen.serialize()
    module = compile_python(pystr)

    # Uncomment these two lines for debugging
    # from tests.test_issues.output.linkml_issue_463 import Container
    # obj = yaml_loader.loads(data_str, target_class=Container)
    # TODO: this currently yields "TypeError: unhashable type: 'TypeObj'"
    obj = yaml_loader.loads(data_str, target_class=module.Container)
    ok1 = False
    ok2 = False
    for c in obj.contains:
        if c.label == "n1" and c.type.label == "n1 label":
            ok1 = True
        if c.label == "n2" and c.type.label == "n2 label":
            ok2 = True
    assert ok1
    assert ok2
