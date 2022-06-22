import logging
import os
import unittest
from contextlib import redirect_stdout
from copy import copy
from typing import List

from linkml.generators.docgen import DocGenerator
from linkml.generators.markdowngen import MarkdownGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
LATEX_DIR = env.expected_path('kitchen_sink_tex')
MD_DIR = env.expected_path('kitchen_sink_md')
MD_DIR2 = env.expected_path('kitchen_sink_md2')
HTML_DIR = env.expected_path('kitchen_sink_html')

def assert_mdfile_contains(filename, text, after:str =None, followed_by: List[str]=None,
                           outdir=MD_DIR) -> None:
    found = False
    is_after = False  ## have we reached the after mark?
    with open(os.path.join(outdir, filename)) as stream:
        lines = stream.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
                if found and followed_by:
                    todo = copy(followed_by)
                    for j in range(i+1, len(lines)):
                        subsequent_line = lines[j]
                        if len(todo) > 0 and todo[0] in subsequent_line:
                            todo = todo[1:]
                    if len(todo) > 0:
                        logging.error(f'Did not find: {todo}')
                        assert False
                    else:
                        return
            if after is not None and after in line:
                is_after = True
    if not found:
        logging.error(f'Failed to find {text} in {filename}')
    assert found

class DocGeneratorTestCase(unittest.TestCase):

    def test_latex_generation(self):
        """ Tests minimal latex generation  """
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, format='latex')
        md = gen.serialize(directory=LATEX_DIR)

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
        # test mermaid
        assert_mdfile_contains('Organization.md',
                               '```mermaid',
                               after='# Class',
                               followed_by=['```', '## Inheritance', '## Slots'])
        assert_mdfile_contains('Organization.md',
                               'HasAliases <|-- Organization',
                               after='```mermaid',
                               followed_by=['Organization : name', '```'])

        # test yaml
        assert_mdfile_contains('Organization.md',
                               '<details>',
                               after='### Direct',
                               followed_by=['```yaml',
                                            'name: Organization',
                                            'mixins:',
                                            '- HasAliases',
                                            '```', '</details>', '### Induced'])
        assert_mdfile_contains('Organization.md',
                               '<details>',
                               after='### Induced',
                               followed_by=['```yaml',
                                            'name: Organization',
                                            'attributes:',
                                            'aliases:',
                                            'multivalued: true',
                                            '```', '</details>'])

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
        assert_mdfile_contains('index.md',
                               '# Kitchen Sink Schema',
                               followed_by=['URI:', 'Name:', '## Classes', '## Slots', '## Enumerations'])
        assert_mdfile_contains('index.md',
                               '[EmploymentEventType](EmploymentEventType.md)',
                               after='Enumerations')
        assert_mdfile_contains('index.md',
                               'a provence-generating activity',
                               after='Classes')
        # test internal links
        assert_mdfile_contains('ceo.md',
                               'Range: [Person](Person.md)',
                               after='Properties')
        # TODO: external links

    def test_myst_dialect(self):
        """
        Tests mermaid in myst.

        See <https://github.com/linkml/linkml/issues/835>_
        """
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, dialect='myst')
        md = gen.serialize(directory=MD_DIR)
        assert_mdfile_contains('Organization.md',
                               '```{mermaid}',
                               after='# Class',
                               followed_by=['```', '## Inheritance', '## Slots'])


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

    def test_class_hierarchy_as_tuples(self):
        """Test for method that seeks to generate hierarchically indented
        list of classes and subclasses
        """
        tdir = env.input_path('docgen_html_templates')
        gen = DocGenerator(SCHEMA, mergeimports=True, no_types_dir=True, template_directory=tdir, format='html')

        actual_result = gen.class_hierarchy_as_tuples()
        actual_result = list(actual_result)

        # assertion to make sure that children are listed after parents
        # parent: class with spaces
        # child at depth 1: subclass test
        # child at depth 2: sub subclass test

        # classes related by is_a relationship
        # sub subclass test is_a subclass test is_a class with spaces

        parent_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "class with spaces"][0])
        sub_class_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "subclass test"][0])
        sub_sub_class_order = actual_result.index([(dep, cls) for dep, cls in actual_result if cls == "sub subclass test"][0])
        
        self.assertGreater(sub_sub_class_order, sub_class_order, parent_order)

        expected_result = [(0, 'agent'), (0, 'activity'), (0, 'AnyObject'), (0, 'class with spaces'), 
                           (1, 'subclass test'), (2, 'sub subclass test'), (0, 'FakeClass'), 
                           (0, 'Dataset'), (0, 'CodeSystem'), (0, 'WithLocation'), (0, 'Relationship'), 
                           (1, 'FamilialRelationship'), (0, 'Event'), (1, 'MarriageEvent'), (1, 'MedicalEvent'), 
                           (1, 'EmploymentEvent'), (1, 'BirthEvent'), (0, 'Concept'), (1, 'ProcedureConcept'), 
                           (1, 'DiagnosisConcept'), (0, 'Address'), (0, 'Place'), (0, 'Organization'), 
                           (1, 'Company'), (0, 'Person'), (0, 'Friend'), (0, 'HasAliases')]
                           
        self.assertCountEqual(actual_result, expected_result)
        



if __name__ == '__main__':
    unittest.main()
