import os
import unittest
from contextlib import redirect_stdout


from linkml.generators.markdowngen import MarkdownGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
MD_DIR = env.expected_path('kitchen_sink_docs')

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

class MarkdownGeneratorTestCase(unittest.TestCase):

    def test_markdowngen(self):
        """ DDL  """
        gen = MarkdownGenerator(SCHEMA, mergeimports=True, no_types_dir=True)
        md = gen.serialize(directory=MD_DIR)

        assert_mdfile_contains('index.md', 'Address', after='Classes')
        assert_mdfile_contains('index.md', 'HasAliases', after='Mixins')
        assert_mdfile_contains('index.md', 'acted on behalf of', after='Slots')
        assert_mdfile_contains('index.md', 'DiagnosisType', after='Enums')
        assert_mdfile_contains('index.md', 'test subset A', after='Subsets')

        assert_mdfile_contains('SubsetA.md', '* [Person](Person.md)',
                               description="person class is declared to be in subset A")

        assert_mdfile_contains('Person.md', 'has medical history', after='Own')
        assert_mdfile_contains('Person.md', 'aliases', after='Mixed in from HasAliases')

        assert_mdfile_contains('has_medical_history.md', 'MedicalEvent', after='Domain and Range')
        assert_mdfile_contains('has_medical_history.md', 'subset B', after='Other properties')


if __name__ == '__main__':
    unittest.main()
