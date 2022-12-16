import unittest

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


class IsolatedNameTestCase(unittest.TestCase):
    def test_it(self):
        """ Dangling name should not throw a type error """
        error_thrown = False
        try:
            from_yaml(model_txt, SchemaDefinition)
        except TypeError as e:
            error_thrown = True
        self.assertFalse(error_thrown, msg="Type error should not be thrown")

if __name__ == '__main__':
    unittest.main()
