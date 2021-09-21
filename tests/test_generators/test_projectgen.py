import os
import unittest
from contextlib import redirect_stdout


from linkml.generators.projectgen import ProjectGenerator, ProjectConfiguration
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
PROJECT_DIR = env.expected_path('ks')

class ProjectGeneratorTestCase(unittest.TestCase):

    def test_projectgen(self):
        """ Generate whole project  """
        config = ProjectConfiguration()
        config.directory = PROJECT_DIR
        config.generator_args['jsonschema'] = {"top_class": "Container"}
        gen = ProjectGenerator()
        gen.generate(SCHEMA, config)

if __name__ == '__main__':
    unittest.main()
