import yaml
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.utils.compile_python import compile_python
from io import StringIO

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
    mixins:
      - HasAliases

  Interface:
    mixin: true
    attributes:
      aliases: {}

  HasAliases:
    mixin: true
    is_a: Interface
"""

# Generate Python classes from the YAML schema
gen = PythonGenerator(schema_yaml)
output = gen.serialize()
print(output)
mod = compile_python(output, "testschema")


# Now define the pytest tests
def test_mixin_inheritance_interface():
    """Test if Person1 inherits attributes from Interface"""
    assert hasattr(mod.Person1, 'aliases'), "Person1 should inherit 'aliases' attribute from Interface"

def test_mixin_inheritance_has_aliases():
    """Test if HasAliases inherits attributes from Interface"""
    assert hasattr(mod.HasAliases, 'aliases'), "HasAliases should inherit 'aliases' attribute from Interface"

def test_mixin_inheritance_person2():
    """Test if Person2 inherits attributes from HasAliases"""
    assert hasattr(mod.Person2, 'aliases'), "Person2 should inherit 'aliases' attribute from HasAliases"
