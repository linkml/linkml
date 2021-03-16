import unittest

from linkml import META_BASE_URI
from linkml.generators.jsonldcontextgen import ContextGenerator
from tests.test_base.environment import env
from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.filters import ldcontext_metadata_filter


class ContextTestCase(GeneratorTestCase):
    """ Generate the context.jsonld for all of the models and compare them against what has been published """
    env = env

    def test_types_context(self):
        """ Build includes/types.context.jsonld """
        self.model_name = 'types'
        self.single_file_generator('context.jsonld', ContextGenerator, subdir='includes',
                                   serialize_args=dict(base=META_BASE_URI), filtr=ldcontext_metadata_filter)

    def test_mappings_context(self):
        """ Build includes/mappings.context.jsonld """
        self.model_name = 'mappings'
        self.single_file_generator('context.jsonld', ContextGenerator, subdir='includes',
                                   serialize_args=dict(base=META_BASE_URI), filtr=ldcontext_metadata_filter)

    def test_extensions_context(self):
        """ Build includes/extensions.context.jsonld """
        self.model_name = 'extensions'
        self.single_file_generator('context.jsonld', ContextGenerator, subdir='includes',
                                   serialize_args=dict(base=META_BASE_URI), filtr=ldcontext_metadata_filter)

    def test_annotations_context(self):
        """ Build includes/annotations.context.jsonld """
        self.model_name = 'annotations'
        self.single_file_generator('context.jsonld', ContextGenerator, subdir='includes',
                                   serialize_args=dict(base=META_BASE_URI), filtr=ldcontext_metadata_filter)

    def test_metamodel_context(self):
        """ Build meta.context.jsonld """
        self.model_name = 'meta'
        self.single_file_generator('jsonld', ContextGenerator, serialize_args=dict(base=META_BASE_URI),
                                   filtr=ldcontext_metadata_filter, output_name='context')


if __name__ == '__main__':
    unittest.main()
