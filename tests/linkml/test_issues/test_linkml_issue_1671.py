from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator

# Define the schema as a YAML string
schema_yaml = """
id: https://w3id.org/linkml/examples/personinfo
imports:
  - https://w3id.org/linkml/types
default_range: string

classes:
  Person1:
    mixins:
      - Interface

  Person2:
    slots:
        - test_slot
    mixins:
      - HasAliases

  Person3:
    is_a: Person2

  Interface:
    mixin: true
    slots:
      - test_aliases

  HasAliases:
    mixin: true
    is_a: Interface

slots:
    test_slot:
        description: "Test slot"
        range: string

    test_aliases:
        description: "Test aliases"
        range: string
"""


# Now define the pytest tests
def test_mixin_inheritance_interface():
    gen = PythonGenerator(schema_yaml)
    output = gen.serialize()
    mod = compile_python(output, "testschema")
    """Test if Person1 inherits attributes from Interface"""
    assert hasattr(mod.Person1, "test_aliases"), "Person1 should inherit 'aliases' attribute from Interface"
    assert hasattr(mod.HasAliases, "test_aliases"), "HasAliases should inherit 'aliases' attribute from Interface"
    assert hasattr(mod.Person2, "test_aliases"), "Person2 should inherit 'aliases' attribute from HasAliases"
    assert hasattr(mod.Person3, "test_aliases"), "Person2 should inherit 'aliases' attribute from HasAliases"
