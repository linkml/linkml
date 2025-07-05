from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.yamlutils import from_yaml

model_txt = """
id: http://x.org
name: test

default_range: string
types:
  string:
    base: str
    uri: xsd:string

slots:
  name:
"""


def test_read_dangling_name() -> None:
    """Dangling name should not throw a type error."""
    error_thrown = False
    try:
        from_yaml(model_txt, SchemaDefinition)
    except TypeError:
        error_thrown = True
    assert error_thrown is False
