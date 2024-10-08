import pytest
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_inheritance(input_path, snapshot, snapshot_path):
    output = PythonGenerator(input_path("issue_14.yaml")).serialize()
    assert output == snapshot("issue_14.py")

    # Added test for issue #183, where sex_qualifier disappeared from MixinOwner class
    module = compile_python(str(snapshot_path("issue_14.py")))
    module.SubjectRange1(id="sr1", name="SubjectRange1", subject="thing1", object="thing2")
    module.MixinOwner(
        id="mo1",
        subject="sr1",
        name="MixinOwner1",
        object="thing2",
        sex_qualifier="ntx",
    )
