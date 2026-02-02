from linkml.generators.markdowngen import MarkdownGenerator


def test_issue_62(input_path, tmp_path, snapshot):
    """Make sure that types are generated as part of the output"""
    MarkdownGenerator(input_path("issue_62.yaml")).serialize(directory=tmp_path)
    assert tmp_path == snapshot("issue62")
