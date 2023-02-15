from linkml_runtime.dumpers import yaml_dumper
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.books_normalized_pydantic import Book, BookSeries, Author


class PydanticDumpersTestCase(LoaderDumperTestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        """ Generate a small sample Books instance for testing purposes """
        LoaderDumperTestCase.setUpClass()
        b1 = Book(name='The Fellowship of the Ring', id="S001.1", price="5.99", summary="Hobbits")
        b2 = Book(name='The Two Towers', id="S001.2", price="5.99", summary="More hobbits")
        b3 = Book(name='The Return of the King', id="S001.3", price="5.99", summary="Yet more hobbits")
        jrr = Author(name='JRR Tolkien', from_country='England')
        cls.books = BookSeries(name='The Lord of the Rings', id="S001", genres=["fantasy"], creator=jrr, books=[b1, b2, b3])

    def test_yaml_dumper(self):
        """ Test the yaml emitter """
        self.dump_test('book_series_lotr.yaml', lambda out_fname: yaml_dumper.dump(self.books, out_fname))
        self.dumps_test('book_series_lotr.yaml', lambda: yaml_dumper.dumps(self.books))
