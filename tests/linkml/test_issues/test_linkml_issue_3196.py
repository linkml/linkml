import typing

from linkml.generators.pydanticgen import PydanticGenerator

test_schema = """
id: https://w3id.org/test
name: Test

imports:
  - linkml:types

classes:
  Foo:
    abstract: true
    attributes:
      foo_field:
        range: string
        required: true
      type:
        range: string
        designates_type: true

  Bar:
    is_a: Foo
    attributes:
      bar_field:
        range: string
        required: true
  Baz:
    is_a: Foo
    attributes:
      baz_field:
        range: string
        required: true

  Qux:
    attributes:
      foo_object:
        range: Foo
        required: true
"""


def test_pydantic_abstract_class_not_in_range_union():
    mod = PydanticGenerator(test_schema).compile_module()
    annotation = mod.Qux.model_fields["foo_object"].annotation

    # Assert that our abstract class is not in the type union for the Qux.foo_object slot
    assert mod.Foo not in typing.get_args(annotation)
