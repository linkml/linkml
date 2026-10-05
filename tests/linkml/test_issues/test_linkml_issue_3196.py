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
    # Assert that our abstract class is not in the type union for the Qux.foo_object slot
    assert mod.Foo not in typing.get_args(annotation)


def test_concrete_descendants_are_in_range_union():
    mod = PydanticGenerator(test_schema).compile_module()
    annotation = mod.Qux.model_fields["foo_object"].annotation
    args = typing.get_args(annotation)
    assert mod.Bar in args
    assert mod.Baz in args


nested_abstract_schema = """
id: https://w3id.org/test
name: TestNested
imports:
  - linkml:types
classes:
  Foo:
    abstract: true
    attributes:
      type: {range: string, designates_type: true}
  Mid:
    is_a: Foo
    abstract: true
  Leaf1:
    is_a: Mid
    attributes: {f1: {range: string}}
  Leaf2:
    is_a: Foo
    attributes: {f2: {range: string}}
  Qux:
    attributes:
      foo_object: {range: Foo, required: true}
"""


def test_nested_abstract_intermediates_excluded():
    mod = PydanticGenerator(nested_abstract_schema).compile_module()
    args = typing.get_args(mod.Qux.model_fields["foo_object"].annotation)
    assert mod.Foo not in args
    assert mod.Mid not in args
    assert mod.Leaf1 in args
    assert mod.Leaf2 in args


mixin_schema = """
id: https://w3id.org/test
name: TestMixin
imports:
  - linkml:types
classes:
  Foo:
    abstract: true
    attributes:
      type: {range: string, designates_type: true}
  Bar:
    is_a: Foo
    attributes: {bar_field: {range: string}}
  MixinChild:
    mixins: [Foo]
    attributes: {mc_field: {range: string}}
  Qux:
    attributes:
      foo_object: {range: Foo, required: true}
"""


def test_mixin_descendant_included_in_union():
    mod = PydanticGenerator(mixin_schema).compile_module()
    args = typing.get_args(mod.Qux.model_fields["foo_object"].annotation)
    assert mod.Foo not in args
    assert mod.Bar in args
    assert mod.MixinChild in args


all_abstract_schema = """
id: https://w3id.org/test
name: TestAllAbstract
imports:
  - linkml:types
classes:
  Foo:
    abstract: true
    attributes:
      type: {range: string, designates_type: true}
  MidAbstract:
    is_a: Foo
    abstract: true
  Qux:
    attributes:
      foo_object: {range: Foo, required: true}
"""


def test_all_descendants_abstract_raises():
    """Abstract range with no concrete descendants is a schema error."""
    import pytest

    with pytest.raises(ValueError, match="no concrete descendants"):
        PydanticGenerator(all_abstract_schema).compile_module()
