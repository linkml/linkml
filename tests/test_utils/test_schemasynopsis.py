import unittest
from typing import Union, List, Optional

from linkml.utils.schemaloader import SchemaLoader
from tests.test_utils.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class SchemaSynopsisTestCase(TestEnvironmentTestCase):
    env = env

    """ Tests for various parts of the schema synopsis file """
    def eval_synopsis(self, base_name: str, source: Optional[str]=None) -> None:
        schema = SchemaLoader(source if source else env.input_path(base_name + '.yaml'), importmap=env.import_map)
        schema.resolve()
        self.summary = schema.synopsis.summary()

        self.env.generate_single_file(base_name + '.errs', lambda: '\n'.join(schema.synopsis.errors()),
                                      value_is_returned=True)
        self.env.generate_single_file(base_name + '.synopsis', lambda: self.summary,
                                      value_is_returned=True)

    def test_meta_synopsis(self):
        """ Raise a flag if the number of classes, slots, types or other elements change in the model  """
        self.eval_synopsis('meta', source=env.meta_yaml)

    def test_unitialized_domain(self):
        self.eval_synopsis('synopsis1')
        # Double check because it is easy to lose the target in the file updates
        self.assertIn("Domain unspecified: 1", self.summary)

    def test_applyto(self):
        self.eval_synopsis('synopsis2')
        self.assertIn("* Unowned slots: s1, s2", self.summary)


if __name__ == '__main__':
    unittest.main()
