import json
import os
import unittest

from linkml.generators.jsonldcontextgen import ContextGenerator
from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env


class Issue344TestCase(TestEnvironmentTestCase):
    env = env

    def test_issue_344(self):
        """ Test to check if prefixes of CURIEs from granular mappings show up in the json-ld context """
        x = env.generate_single_file('issue_344_context.json',
                                 lambda: ContextGenerator(env.input_path('issue_344.yaml'),
                                 importmap=env.import_map, emit_metadata=False).serialize(), value_is_returned=True)
        with open(os.path.join(env.outdir, 'issue_344_context.json')) as f:
            context = json.load(f)
        self.assertIn('PCO', context['@context'])
        self.assertIn('PATO', context['@context'])
        self.assertIn('GO', context['@context'])


if __name__ == '__main__':
    unittest.main()
