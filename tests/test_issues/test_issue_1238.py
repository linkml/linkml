import unittest

from linkml_runtime import SchemaView

META_URL = "https://raw.githubusercontent.com/linkml/linkml-model/main/linkml_model/model/schema/meta.yaml"
SCRUTINIZED_CLASS = "schema_definition"

EXPECTED_INDUCED_ATTRIBS = ['aliases',
                            'alt_descriptions',
                            'annotations',
                            'broad mappings',
                            'categories',
                            'classes',
                            'close mappings',
                            'comments',
                            'conforms_to',
                            'default_curi_maps',
                            'default_prefix',
                            'default_range',
                            'definition_uri',
                            'deprecated',
                            'deprecated element has exact replacement',
                            'deprecated element has possible replacement',
                            'description',
                            'emit_prefixes',
                            'enums',
                            'exact mappings',
                            'examples',
                            'extensions',
                            'from_schema',
                            'generation_date',
                            'id',
                            'id_prefixes',
                            'imported_from',
                            'imports',
                            'in_language',
                            'in_subset',
                            'keywords',
                            'license',
                            'local_names',
                            'mappings',
                            'metamodel_version',
                            'name',
                            'narrow mappings',
                            'notes',
                            'prefixes',
                            'rank',
                            'related mappings',
                            'see_also',
                            'settings',
                            'slot_definitions',
                            'slot_names_unique',
                            'source',
                            'source_file',
                            'source_file_date',
                            'source_file_size',
                            'structured_aliases',
                            'subsets',
                            'title',
                            'todos',
                            'types',
                            'version']


class SchemaDefInducedAttribsCase(unittest.TestCase):
    def test_induced_attrib_list(self):
        meta_view = SchemaView(META_URL)

        induced_schema_def = meta_view.induced_class(SCRUTINIZED_CLASS)
        induced_schema_def_attribs = induced_schema_def.attributes
        induced_schema_def_attrib_names = [v.name for k, v in induced_schema_def_attribs.items()]
        induced_schema_def_attrib_names.sort()

        self.assertEqual(induced_schema_def_attrib_names, EXPECTED_INDUCED_ATTRIBS)


if __name__ == "__main__":
    unittest.main()
