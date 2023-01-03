import os.path
import unittest

from linkml_runtime.loaders import YAMLLoader
from linkml_runtime.utils.compile_python import compile_python

from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env


nesting_string = """id: https://examples.r.us/manifest
name: manifest

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://examples.r.us/manifest/

imports:
  - linkml:types

classes:
    TestEntry:
        attributes:
            name:
            description:
            stuff:
    Module:
        attributes:
            id:
                identifier: True
            description:
    TestSet:
        attributes:
            module:
                range: Module
                identifier: True
            tests:
                range: TestEntry
                multivalued: True
                inlined: True
    Manifest:
        attributes:
            modules:
                description: Testing modules
                range: Module
                inlined: true
                multivalued: true
            tests:
                description: Actual test sets
                range: TestSet
                inlined: true
                multivalued: true
"""

manifest = """
tests:
    module_1:
        - name: test_1
          description: first test
          stuff: stuff 1
        - description: second test
          stuff: stuff 2
    module_2:
        - name: test_3
"""

testset1 = """
module: module_1
tests:
    - name: test_1
      description: first test
      stuff: stuff 1
    - description: second test
      stuff: stuff 2
"""

testset2 = """
module_1:
    - name: test_1
      description: first test
      stuff: stuff 1
    - description: second test
      stuff: stuff 2
"""

UPDATE_PYTHON = True


# If you need to debug, you can uncomment this line and switch from self.mod to issue_1188 for imports
# Example
#     from .output.issue_1188 import issue_1188a
#     instance = YAMLLoader().load_any(manifest, issue_1188a.Manifest, base_dir=env.cwd)

class InlineListTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        gen = PythonGenerator(nesting_string, metadata=False)
        output = gen.serialize()
        if UPDATE_PYTHON:
            # Create a readable image of the output for debugging purposes
            issue_1188_directory = os.path.join(env.outdir, 'issue_1188')
            init_file = os.path.join(issue_1188_directory, '__init__.py')
            python_file = os.path.join(issue_1188_directory, 'issue_1188a.py')
            os.makedirs(issue_1188_directory, exist_ok=True)
            if not os.path.exists(init_file):
                with open(init_file, 'w'):
                    pass
            with open(python_file, 'w') as pyfile:
                pyfile.write(output)
            print(f"{os.path.relpath(python_file, env.cwd)} created")
        cls.mod = compile_python(output)

    def test_manifest(self):
        """ Test a list of strings as a root node """
        instance = YAMLLoader().load_any(manifest, self.mod.Manifest, base_dir=env.cwd)
        self.assertEqual(['module_1', 'module_2'], list(instance.tests.keys()))
        self.assertEqual(instance.tests['module_1'].tests[0].name, 'test_1')
        self.assertIsNone(instance.tests['module_1'].tests[1].name)
        self.assertEqual('second test', instance.tests['module_1'].tests[1].description)
        self.assertEqual('test_3', instance.tests['module_2'].tests[0].name)

    def test_testset(self):
        instance1 = YAMLLoader().load_any(testset1, self.mod.TestSet, base_dir=env.cwd)
        self.assertEqual("TestSet(module='module_1', "
                         "tests=[TestEntry(name='test_1', description='first test', stuff='stuff 1'), "
                         "TestEntry(name=None, description='second test', stuff='stuff 2')])", repr(instance1))
        instance2 = YAMLLoader().load_any(testset2, self.mod.TestSet, base_dir=env.cwd)
        self.assertEqual("TestSet(module='module_1', "
                         "tests=[TestEntry(name='test_1', description='first test', stuff='stuff 1'), "
                         "TestEntry(name=None, description='second test', stuff='stuff 2')])", repr(instance2))


if __name__ == '__main__':
    unittest.main()
