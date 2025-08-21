from linkml.generators.markdowngen import MarkdownGenerator


def test_issue_179(input_path, snapshot, tmp_path):
    """Make sure that inheritance isn't implied by reference slots"""

    MarkdownGenerator(input_path("issue_179.yaml")).serialize(directory=tmp_path)
    assert tmp_path == snapshot("issue179")
