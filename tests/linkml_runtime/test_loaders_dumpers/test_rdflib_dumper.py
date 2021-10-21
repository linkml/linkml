import json
import os
import unittest
import logging

from rdflib import Graph

from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinitionName
from linkml_runtime.loaders import json_loader
from linkml_runtime.dumpers.rdflib_dumper import RDFLibDumper
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.schemaops import roll_up, roll_down
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.personinfo import Container

SCHEMA = os.path.join(INPUT_DIR, 'personinfo.yaml')
DATA = os.path.join(INPUT_DIR, 'example_personinfo_data.yaml')
OUT = os.path.join(OUTPUT_DIR, 'example_personinfo_data.ttl')

yaml_loader = YAMLLoader()


class RdfLibDumperTestCase(unittest.TestCase):

    def test_rdflib_dumper(self):
        view = SchemaView(SCHEMA)
        dataset = yaml_loader.load(DATA, target_class=Container)
        pm = {
            'CODE': 'http://example.org/code/',
            'ROR': 'http://example.org/ror/',
            'P': 'http://example.org/P/',
            'GEO': 'http://example.org/GEO/',
        }
        rdflib_dumper = RDFLibDumper()
        rdflib_dumper.dump(dataset, schemaview=view, to_file=OUT, prefix_map=pm)
        g = Graph()
        g.parse(OUT, format='ttl')


if __name__ == '__main__':
    unittest.main()
