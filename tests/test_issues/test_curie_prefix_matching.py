import unittest
from logging import INFO

from linkml.generators.jsonldcontextgen import ContextGenerator
from linkml.generators.yamlgen import YAMLGenerator
from tests.test_issues.environment import env
from tests.utils.filters import yaml_filter, ldcontext_metadata_filter
from tests.utils.test_environment import TestEnvironmentTestCase


class CuriePrefixTestCase(TestEnvironmentTestCase):
    env = env

    def test_multi_curies(self):
        self._do_test('curie_prefix_matching')

    def test_curie_case(self):
        self._do_test('curie_case')

    def _do_test(self, tfn):
        env.generate_single_file(f'{tfn}.yaml',
                                 lambda: YAMLGenerator(env.input_path(f'{tfn}.yaml'), log_level=INFO).serialize(),
                                 filtr=yaml_filter, value_is_returned=True)
        env.generate_single_file(f'{tfn}.context.jsonld',
                                 lambda: ContextGenerator(env.input_path(f'{tfn}.yaml')).serialize(),
                                 filtr=ldcontext_metadata_filter, value_is_returned=True)



if __name__ == '__main__':
    unittest.main()
