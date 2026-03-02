import pytest

from linkml.generators.pythongen import PythonGenerator


@pytest.mark.pythongen
def test_enum_import(input_path, snapshot):
    """Enum reference isn't getting merged on module import"""
    # env.generate_single_file('file1.py',
    #                          lambda: PythonGenerator(env.input_path(self.directory, 'file1.yaml'),
    #                                                  mergeimports=True).serialize(),
    #                          comparator=lambda exp,
    #                          act: compare_python(exp, act, env.expected_path(self.directory, 'file1.py')),
    #                          value_is_returned=True)
    output = PythonGenerator(input_path("issue_enum_import/file2.yaml"), mergeimports=True).serialize()
    assert output == snapshot("issue_enum_import/file2.py")
