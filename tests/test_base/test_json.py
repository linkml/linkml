import unittest

from linkml import LOCAL_TYPES_YAML_FILE, METATYPE_NAMESPACE, METAMAPPING_NAMESPACE, \
    LOCAL_MAPPINGS_YAML_FILE, LOCAL_EXTENSIONS_YAML_FILE, LOCAL_ANNOTATIONS_YAML_FILE, LOCAL_METAMODEL_YAML_FILE, \
    METAMODEL_NAMESPACE, METAEXTENSIONS_NAMESPACE, METAANNOTATIONS_NAMESPACE
from linkml.generators.jsonldgen import JSONLDGenerator
from tests.test_base.environment import env
from tests.utils.generatortestcase import GeneratorTestCase
from tests.utils.filters import json_metadata_filter


class JsonLDTestCase(GeneratorTestCase):
    """ Generate the JSON for all of the models and compare them against what has been published """
    env = env

    def test_types_jsonld(self):
        """ Build includes/types.jsonld """
        self.model_name = 'types'
        self.single_file_generator('json', JSONLDGenerator, yaml_file=LOCAL_TYPES_YAML_FILE,
                                   serialize_args=dict(base=METATYPE_NAMESPACE), filtr=json_metadata_filter)

    def test_mappings_jsonld(self):
        """ Build includes/mappings.jsonld """
        self.model_name = 'mappings'
        self.single_file_generator('json', JSONLDGenerator, yaml_file=LOCAL_MAPPINGS_YAML_FILE,
                                   serialize_args=dict(base=METAMAPPING_NAMESPACE), filtr=json_metadata_filter)

    def test_extensions_jsonld(self):
        """ Build includes/extensions.jsonld """
        self.model_name = 'extensions'
        self.single_file_generator('json', JSONLDGenerator, yaml_file=LOCAL_EXTENSIONS_YAML_FILE,
                                   serialize_args=dict(base=METAEXTENSIONS_NAMESPACE), filtr=json_metadata_filter)

    def test_annotations_jsonld(self):
        """ Build includes/annotations.jsonld """
        self.model_name = 'annotations'
        self.single_file_generator('json', JSONLDGenerator, yaml_file=LOCAL_ANNOTATIONS_YAML_FILE,
                                   serialize_args=dict(base=METAANNOTATIONS_NAMESPACE), filtr=json_metadata_filter)

    def test_metamodel_jsonld(self):
        """ Build meta.jsonld """
        self.model_name = 'meta'
        self.single_file_generator('json', JSONLDGenerator, yaml_file=LOCAL_METAMODEL_YAML_FILE,
                                   serialize_args=dict(base=METAMODEL_NAMESPACE), filtr=json_metadata_filter)


if __name__ == '__main__':
    unittest.main()
