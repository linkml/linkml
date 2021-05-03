import unittest

from linkml_runtime.utils.yamlutils import YAMLRoot, as_yaml
from tests.test_issues.environment import env
from tests.test_issues.input.issue_355 import Container, Containee


class ContainedObjectTestCase(unittest.TestCase):
    env = env

    def test_contained_constructor(self):
        """ Make sure the containee remains intact (test of YAMLRoot load section)"""
        c = Container(Containee('11111', "Glaubner's disease"))
        self.assertEqual('''entry:
  '11111':
    id: '11111'
    value: Glaubner's disease''', as_yaml(c).strip())

        c = Container({'22222': dict(id='22222', value='Phrenooscopy')})
        self.assertEqual('''entry:
  '22222':
    id: '22222'
    value: Phrenooscopy''', as_yaml(c).strip())
        alt_object = YAMLRoot()
        alt_object.id = '33333'
        alt_object.value = 'test'
        c = Container(alt_object)
        self.assertEqual('''entry:
  '33333':
    id: '33333'
    value: test''', as_yaml(c).strip())
        c = Container([dict(id='44444', value="Gracken's curse")])
        self.assertEqual('''entry:
  '44444':
    id: '44444'
    value: Gracken's curse''', as_yaml(c).strip())


if __name__ == '__main__':
    unittest.main()
