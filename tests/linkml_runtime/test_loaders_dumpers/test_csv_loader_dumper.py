import os
import unittest
import json
import logging

from jsonasobj2 import as_json_obj, JsonObj

from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.formatutils import remove_empty_items, is_empty
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.dumpers import csv_dumper
from linkml_runtime.loaders import csv_loader
from linkml_runtime.utils.yamlutils import as_json_object
from tests.test_loaders_dumpers.models.books_normalized import Shop, Book, GenreEnum, BookSeries


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

    def test_object_model(self):
        book = Book(id='B1', genres=['fantasy'], creator={})
        print(book.genres)
        print(type(book.genres[0]))
        logging.debug(as_json_obj(book.genres[0]))
        assert str(book.genres[0]) == 'fantasy'
        assert book.genres[0].code.text == 'fantasy'
        processed = remove_empty_items(book.genres)
        print(f'PR={processed}')
        assert processed[0] == 'fantasy'
        series = BookSeries(id='S1')
        series.books.append(book)
        schemaview = SchemaView(SCHEMA)
        shop = Shop()
        shop.all_book_series.append(book)
        #csvstr = csv_dumper.dumps(shop, index_slot='all_book_series', schemaview=schemaview)
        #logging.debug(csvstr)

    def test_csvgen_roundtrip(self):
        schemaview = SchemaView(SCHEMA)
        data = yaml_loader.load(DATA, target_class=Shop)
        csv_dumper.dump(data, to_file=OUTPUT, index_slot='all_book_series', schemaview=schemaview)
        roundtrip = csv_loader.load(OUTPUT, target_class=Shop, index_slot='all_book_series', schemaview=schemaview)
        logging.debug(json_dumper.dumps(roundtrip))
        logging.debug(f'COMPARE 1: {roundtrip}')
        logging.debug(f'COMPARE 2: {data}')
        assert roundtrip == data

    def test_csvgen_unroundtrippable(self):
        schemaview = SchemaView(SCHEMA)
        #schema = YAMLGenerator(SCHEMA).schema
        data = yaml_loader.load(DATA2, target_class=Shop)
        logging.debug(data.all_book_series[0])
        logging.debug(data.all_book_series[0].genres[0])
        assert str(data.all_book_series[0].genres[0]) == 'fantasy'
        logging.debug(yaml_dumper.dumps(data))
        logging.debug(json_dumper.dumps(data))
        processed = remove_empty_items(data)
        logging.debug(f'PROC {processed["all_book_series"]}')
        asj = as_json_object(processed, None)
        logging.debug(f'ASJ {asj["all_book_series"]}')
        reconstituted_json = json.loads(json_dumper.dumps(data))
        s0 = reconstituted_json['all_book_series'][0]
        logging.debug(s0)
        logging.debug(json_dumper.dumps(data))
        #logging.debug(csv_dumper.dumps(data, index_slot='all_book_series', schema=schema))
        csv_dumper.dump(data, to_file=OUTPUT2, index_slot='all_book_series', schemaview=schemaview)
        #assert False
        roundtrip = csv_loader.load(OUTPUT2, target_class=Shop, index_slot='all_book_series', schemaview=schemaview)
        logging.debug(json_dumper.dumps(roundtrip))
        assert roundtrip == data









if __name__ == '__main__':
    unittest.main()
