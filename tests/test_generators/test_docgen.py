import os
import unittest
from contextlib import redirect_stdout

from linkml.generators.docgen import DocGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
MD_DIR = env.expected_path('kitchen_sink_md')
MD_DIR2 = env.expected_path('kitchen_sink_md2')
HTML_DIR = env.expected_path('kitchen_sink_html')

def assert_mdfile_contains(filename, text, after=None, description=None, outdir=MD_DIR) -> None:
    found = False
    is_after = False  ## have we reached the after mark?
    with open(os.path.join(outdir, filename)) as stream:
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

    def test_docgen(self):
        """ Tests basic document generator functionality  """
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True)
        md = gen.serialize(directory=MD_DIR)
        # test class docs
        assert_mdfile_contains('Organization.md', 'Organization', after='Inheritance')
        assert_mdfile_contains('Organization.md', '[aliases](aliases.md)', after='Slots')
        assert_mdfile_contains('Organization.md',
                               'URI: [ks:Organization](https://w3id.org/linkml/tests/kitchen_sink/Organization)',
                               after='Class: Organization')
        assert_mdfile_contains('Organization.md',
                               'from_schema: https://w3id.org/linkml/tests/kitchen_sink',
                               after='Class: Organization')
        assert_mdfile_contains('Organization.md',
                               'slot_uri: skos:altLabel',
                               after='Induced')
        # test type docs
        assert_mdfile_contains('PhoneNumberType.md',
                               'URI: http://www.w3.org/2001/XMLSchema#string',
                               after='PhoneNumberType')
        # test enum docs
        assert_mdfile_contains('EmploymentEventType.md',
                               'codes for different kinds of employment/HR related events',
                               after='EmploymentEventType')
        assert_mdfile_contains('EmploymentEventType.md',
                               'PROMOTION | bizcodes:003 | promotion event',
                               after='Permissible Values')
        # test slot docs
        assert_mdfile_contains('aliases.md',
                               'http://www.w3.org/2004/02/skos/core#altLabel',
                               after='aliases')
        # test index docs
        assert_mdfile_contains('aliases.md',
                               'http://www.w3.org/2004/02/skos/core#altLabel',
                               after='aliases')


    def test_custom_directory(self):
        """
        tests ability to specify a custom folder of templates;
        these act as overrides, if no template is found the default is used
        """
        tdir = env.input_path('docgen_md_templates')
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, template_directory=tdir)
        md = gen.serialize(directory=MD_DIR2)
        #assert_mdfile_contains('Organization.md', 'Organization', after='Inheritance')
        assert_mdfile_contains('Organization.md', 'FAKE TEMPLATE', outdir=MD_DIR2)

    def test_html(self):
        """
        Tests ability to specify a complete new set of templates in a different format
        """
        tdir = env.input_path('docgen_html_templates')
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, template_directory=tdir, format='html')
        assert gen._file_suffix() == 'html'
        md = gen.serialize(directory=HTML_DIR)
        assert_mdfile_contains('Organization.html', 'Fake example Organization', outdir=HTML_DIR)




if __name__ == '__main__':
    unittest.main()
