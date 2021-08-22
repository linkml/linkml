import os
import unittest
import json

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.dumpers import csv_dumper
from linkml_runtime.loaders import csv_loader
from tests.test_loaders_dumpers.models.books_normalized import Shop


ROOT = os.path.abspath(os.path.dirname(__file__))
INPUT_DIR = os.path.join(ROOT, 'input')
OUTPUT_DIR = os.path.join(ROOT, 'output')
MODEL_DIR = os.path.join(ROOT, 'models')

SCHEMA = os.path.join(MODEL_DIR, 'books_normalized.yaml')
DATA = os.path.join(INPUT_DIR, 'books_normalized_01.yaml')
DATA2 = os.path.join(INPUT_DIR, 'books_normalized_02.yaml')
OUTPUT = os.path.join(OUTPUT_DIR, 'books_flattened.tsv')
OUTPUT2 = os.path.join(OUTPUT_DIR, 'books_flattened_02.tsv')

def _json(obj) -> str:
    return json.dumps(obj, indent=' ', sort_keys=True)


class CSVGenTestCase(unittest.TestCase):

    def test_csvgen_roundtrip(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA, target_class=Shop)
        csv_dumper.dump(data, to_file=OUTPUT, index_slot='all_book_series', schemaview=schemaview)
        roundtrip = csv_loader.load(OUTPUT, target_class=Shop, index_slot='all_book_series', schemaview=schemaview)
        print(json_dumper.dumps(roundtrip))
        assert roundtrip == data

    def test_csvgen_unroundtrippable(self):
        schemaview = SchemaView(SCHEMA)
        #schema = YAMLGenerator(SCHEMA).schema
        data = yaml_loader.load(DATA2, target_class=Shop)
        #print(json_dumper.dumps(data))
        #print(csv_dumper.dumps(data, index_slot='all_book_series', schema=schema))
        csv_dumper.dump(data, to_file=OUTPUT2, index_slot='all_book_series', schemaview=schemaview)
        roundtrip = csv_loader.load(OUTPUT2, target_class=Shop, index_slot='all_book_series', schemaview=schemaview)
        print(json_dumper.dumps(roundtrip))
        #assert roundtrip == data







if __name__ == '__main__':
    unittest.main()
