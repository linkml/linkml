import json

import yaml

from linkml_runtime.dumpers import yaml_dumper, json_dumper
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.books_normalized_pydantic import Book, BookSeries, Author
from tests.test_loaders_dumpers.models.kitchen_sink_pydantic import BirthEvent, Person
from linkml_runtime.utils.formatutils import remove_empty_items


class PydanticDumpersTestCase(LoaderDumperTestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        """ Generate a small sample Books instance for testing purposes """
        LoaderDumperTestCase.setUpClass()
        b1 = Book(name='Fellowship of the Ring', id="S001.1", price="5.99", summary="Hobbits")
        b2 = Book(name='The Two Towers', id="S001.2", price="5.99", summary="More hobbits")
        b3 = Book(name='Return of the King', id="S001.3", price="6.99", summary="Yet more hobbits")
        jrr = Author(name='JRR Tolkein', from_country='England')
        cls.bookseries = BookSeries(name='Lord of the Rings', id="S001", genres=["fantasy"], creator=jrr, books=[b1, b2, b3])

    def test_yaml_dumper(self):
        """ Test the yaml emitter """
        self.dump_test('book_series_lotr.yaml', lambda out_fname: yaml_dumper.dump(self.bookseries, out_fname))
        self.dumps_test('book_series_lotr.yaml', lambda: yaml_dumper.dumps(self.bookseries))

        # test contents of yaml file with cleaned dict made from bookseries instance in setup
        with open(self.env.input_path('book_series_lotr.yaml')) as f:
            data = yaml.safe_load(f)
            # explicitly confirm that unset fields aren't written to the file
            for i in range(3):
                'genres' not in data['books'][i].keys()
                'inStock' not in data['books'][i].keys()
                'creator' not in data['books'][i].keys()
            self.assertEqual(data, remove_empty_items(self.bookseries.model_dump()))


    def test_json_dumper(self):
        """ Test the json emitter """
        self.dump_test('book_series_lotr.json', lambda out_fname: json_dumper.dump(self.bookseries, out_fname))
        self.dumps_test('book_series_lotr.json', lambda: json_dumper.dumps(self.bookseries))

        # test contents of json file with cleaned dict made from bookseries instance in setup
        with open(self.env.input_path('book_series_lotr.json')) as f:
            data = json.load(f)
            # explicitly confirm that unset fields aren't written to the file
            for i in range(3):
                'genres' not in data['books'][i].keys()
                'inStock' not in data['books'][i].keys()
                'creator' not in data['books'][i].keys()
            self.assertEqual(data, remove_empty_items(self.bookseries.model_dump()))
  

class PydanticDumpersDateTestCase(LoaderDumperTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """ Generate an example with a date for testing purposes """
        LoaderDumperTestCase.setUpClass()
        b1 = BirthEvent(started_at_time="2021-01-01", ended_at_time="2021-01-02")
        
        cls.person = Person(
            id="P01", 
            name='John Doe', 
            has_birth_event=b1
        )

    def test_yaml_dumper(self):
        """ Test the yaml emitter """
        # with open(self.env.input_path('kitchen_sink_person_01.yaml'), 'w', encoding='utf-8') as f:
        #     # write the yaml file
        #     f.write(yaml_dumper.dumps(self.person))
        # with open(self.env.input_path('kitchen_sink_person_01.json'), 'w', encoding='utf-8') as f:
        #     # write the json file
        #     f.write(json_dumper.dumps(self.person, inject_type=False))

        self.dump_test('kitchen_sink_person_01.yaml', lambda out_fname: yaml_dumper.dump(self.person, out_fname))
        self.dumps_test('kitchen_sink_person_01.yaml', lambda: yaml_dumper.dumps(self.person))

    def test_json_dumper(self):
        """ Test the json emitter """
        self.dump_test('kitchen_sink_person_01.json', lambda out_fname: json_dumper.dump(self.person, out_fname))
        self.dumps_test('kitchen_sink_person_01.json', lambda: json_dumper.dumps(self.person))
