import logging
import unittest


from linkml.generators.pythongen import PythonGenerator
from tests.test_issues.environment import env

SCHEMA = env.input_path("linkml_issue_1168.yaml")


class TestForwardReferences(unittest.TestCase):

    def test_compile(self):
        generator = PythonGenerator(SCHEMA)
        mod = generator.compile_module()