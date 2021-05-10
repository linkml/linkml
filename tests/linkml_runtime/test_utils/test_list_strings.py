import unittest

from linkml_runtime.loaders import yaml_loader
from linkml_runtime.linkml_model.meta import SchemaDefinition

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


class ListStringsTestCase(unittest.TestCase):
    def test_strings_in_list_slot(self):
        rslt = yaml_loader.loads(sample, SchemaDefinition)
        self.assertEqual(1, len(rslt.classes['AClass'].slots))
        self.assertEqual('a_slot', rslt.classes['AClass'].slots[0])
        self.assertEqual(1, len(rslt.classes['BClass'].mixins))
        self.assertEqual('AClass', rslt.classes['BClass'].mixins[0])


if __name__ == '__main__':
    unittest.main()
