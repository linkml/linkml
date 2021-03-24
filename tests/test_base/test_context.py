import unittest

from linkml import LOCAL_TYPES_YAML_FILE, METATYPE_NAMESPACE, METAMAPPING_NAMESPACE, \
    LOCAL_MAPPINGS_YAML_FILE, LOCAL_EXTENSIONS_YAML_FILE, LOCAL_ANNOTATIONS_YAML_FILE, LOCAL_METAMODEL_YAML_FILE, \
    METAMODEL_NAMESPACE, METAEXTENSIONS_NAMESPACE, METAANNOTATIONS_NAMESPACE
from linkml.generators.jsonldcontextgen import ContextGenerator
from tests.test_base.environment import env
from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.filters import ldcontext_metadata_filter


class ContextTestCase(GeneratorTestCase):
    """ Generate the context.jsonld for all of the models and compare them against what has been published """
    env = env

    def test_types_context(self):
        """ Build types.context.jsonld """
        self.model_name = 'types'
        self.single_file_generator('context.jsonld', ContextGenerator, yaml_file=LOCAL_TYPES_YAML_FILE,
                                   serialize_args=dict(base=str(METATYPE_NAMESPACE)), filtr=ldcontext_metadata_filter)

    def test_mappings_context(self):
        """ Build mappings.context.jsonld """
        self.model_name = 'mappings'
        self.single_file_generator('context.jsonld', ContextGenerator, yaml_file=LOCAL_MAPPINGS_YAML_FILE,
                                   serialize_args=dict(base=METAMAPPING_NAMESPACE), filtr=ldcontext_metadata_filter)

    def test_extensions_context(self):
        """ Build includes/extensions.context.jsonld """
        self.model_name = 'extensions'
        self.single_file_generator('context.jsonld', ContextGenerator, yaml_file=LOCAL_EXTENSIONS_YAML_FILE,
                                   serialize_args=dict(base=METAEXTENSIONS_NAMESPACE), filtr=ldcontext_metadata_filter)

    def test_annotations_context(self):
        """ Build includes/annotations.context.jsonld """
        self.model_name = 'annotations'
        self.single_file_generator('context.jsonld', ContextGenerator, yaml_file=LOCAL_ANNOTATIONS_YAML_FILE,
                                   serialize_args=dict(base=METAANNOTATIONS_NAMESPACE), filtr=ldcontext_metadata_filter)

    def test_metamodel_context(self):
        """ Build meta.context.jsonld """
        self.model_name = 'meta'
        self.single_file_generator('context.jsonld', ContextGenerator, yaml_file=LOCAL_METAMODEL_YAML_FILE,
                                   serialize_args=dict(base=METAMODEL_NAMESPACE), filtr=ldcontext_metadata_filter)


if __name__ == '__main__':
    unittest.main()
