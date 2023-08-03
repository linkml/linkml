from linkml.generators.pythongen import PythonGenerator


def test_issue_84(input_path, snapshot):
    output = PythonGenerator(input_path("issue_50.yaml")).serialize()
    assert output == snapshot("issue_50.py")


def test_issue_50(input_path, snapshot):
    output = PythonGenerator(input_path("issue_84.yaml")).serialize()
    assert output == snapshot("issue_84.py")
