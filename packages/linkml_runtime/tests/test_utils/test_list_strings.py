from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

sample = """id: http://examples.org/test
name: test
license: https://creativecommons.org/publicdomain/zero/1.0/

prefixes:
  test: http://examples.org/test/
  xsd: http://www.w3.org/2001/XMLSchema#

default_prefix: test
default_range: string

types:
  string:
    uri: xsd:string
    base: str
    description: A character string

slots:
  a_slot:
    description: A single slot

classes:
  AClass:
    description: class 1
    slots:
        a_slot

  BClass:
    mixins:
        AClass
"""


def test_strings_in_list_slot():
    rslt = yaml_loader.loads(sample, SchemaDefinition)
    assert len(rslt.classes["AClass"].slots) == 1
    assert rslt.classes["AClass"].slots[0] == "a_slot"
    assert len(rslt.classes["BClass"].mixins) == 1
    assert rslt.classes["BClass"].mixins[0] == "AClass"
