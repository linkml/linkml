import os
import unittest
from contextlib import redirect_stdout

from linkml.generators.docgen import DocGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
MD_DIR = env.expected_path('kitchen_sink_md')

def assert_mdfile_contains(filename, text, after=None, description=None) -> None:
    found = False
    is_after = False  ## have we reached the after mark?
    with open(os.path.join(MD_DIR, filename)) as stream:
        for line in stream.readlines():
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
            if after is not None and after in line:
                is_after = True
    assert found

class DocGeneratorTestCase(unittest.TestCase):

    def test_docdowngen(self):
        """ DDL  """
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True)
        md = gen.serialize(directory=MD_DIR)
        assert_mdfile_contains('Organization.md', 'Organization', after='Inheritance')
        # TODO: add more tests




if __name__ == '__main__':
    unittest.main()
