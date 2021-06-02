import os
import unittest

from linkml import LOCAL_METAMODEL_YAML_FILE, LOCAL_METAMODEL_JSONLD_FILE, LOCAL_METAMODEL_LDCONTEXT_FILE, \
    LOCAL_MAPPINGS_YAML_FILE, LOCAL_MAPPINGS_JSONLD_FILE, LOCAL_MAPPINGS_LDCONTEXT_FILE, \
    LOCAL_TYPES_YAML_FILE, LOCAL_TYPES_JSONLD_FILE, LOCAL_TYPES_LDCONTEXT_FILE, \
    LOCAL_SHEXC_FILE_NAME, LOCAL_SHEXJ_FILE_NAME, LOCAL_RDF_FILE_NAME, \
    METAMODEL_URI, METAMODEL_NAMESPACE_NAME, METAMODEL_NAMESPACE, METATYPE_NAMESPACE_NAME, METATYPE_URI, \
    METATYPE_NAMESPACE, METAMAPPING_URI, METAMAPPING_NAMESPACE_NAME, METAMAPPING_NAMESPACE, METAMODEL_NAME, \
    METATYPE_NAME, METAMAPPING_NAME
from linkml.utils.rawloader import load_raw_schema


class ModelURITestCase(unittest.TestCase):
    """ Make sure that the URI's in the include files match what is actually in the output"""

    def validate_yaml_content(self, uri, name, namespace_name, namespace, source) -> None:
        def check_yaml(source_file):
            model_yaml = load_raw_schema(source_file)
            # The model yaml id no longer mirrors the model uri
            # self.assertEqual(uri, model_yaml.id)
            self.assertEqual(name, model_yaml.name)
            self.assertEqual(namespace_name, model_yaml.default_prefix)
            self.assertEqual(namespace, model_yaml.prefixes[model_yaml.default_prefix].prefix_reference)
            self.assertEqual(source_file, model_yaml.source_file)

        check_yaml(source)

    @unittest.skip("TODO: decide which local files are still needed")
    def test_model_uris(self):
        """ Test that the variables in meta.yaml match the contents of linkml/__init__.py """
        for filename in [LOCAL_RDF_FILE_NAME, LOCAL_SHEXJ_FILE_NAME, LOCAL_SHEXC_FILE_NAME, LOCAL_TYPES_LDCONTEXT_FILE,
                         LOCAL_SHEXC_FILE_NAME, LOCAL_SHEXJ_FILE_NAME, LOCAL_RDF_FILE_NAME, LOCAL_TYPES_LDCONTEXT_FILE,
                         LOCAL_MAPPINGS_YAML_FILE, LOCAL_MAPPINGS_LDCONTEXT_FILE, LOCAL_MAPPINGS_JSONLD_FILE,
                         LOCAL_TYPES_LDCONTEXT_FILE, LOCAL_TYPES_JSONLD_FILE, LOCAL_TYPES_YAML_FILE,
                         LOCAL_MAPPINGS_JSONLD_FILE, LOCAL_METAMODEL_JSONLD_FILE, LOCAL_METAMODEL_LDCONTEXT_FILE]:
            self.assertTrue(os.path.exists(filename), msg=f"{filename} does not exist")
        self.validate_yaml_content(METAMODEL_URI, METAMODEL_NAME, METAMODEL_NAMESPACE_NAME, METAMODEL_NAMESPACE,
                                   LOCAL_METAMODEL_YAML_FILE)
        self.validate_yaml_content(METATYPE_URI, METATYPE_NAME, METATYPE_NAMESPACE_NAME, METATYPE_NAMESPACE,
                                   LOCAL_TYPES_YAML_FILE)
        self.validate_yaml_content(METAMAPPING_URI, METAMAPPING_NAME, METAMAPPING_NAMESPACE_NAME, METAMAPPING_NAMESPACE,
                                   LOCAL_MAPPINGS_YAML_FILE)


if __name__ == '__main__':
    unittest.main()
