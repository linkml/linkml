import json
from collections.abc import Callable
from datetime import UTC, date, datetime
from typing import Any

import pytest
import yaml
from pydantic import BaseModel

from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.utils.formatutils import remove_empty_items
from tests.linkml_runtime.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.linkml_runtime.test_loaders_dumpers.models.books_normalized_pydantic import Author, Book, BookSeries
from tests.linkml_runtime.test_loaders_dumpers.models.kitchen_sink_pydantic import BirthEvent, Person


class PydanticDumpersTestCase(LoaderDumperTestCase):
    pass

    @classmethod
    def setUpClass(cls) -> None:
        """Generate a small sample Books instance for testing purposes"""
        LoaderDumperTestCase.setUpClass()
        b1 = Book(name="Fellowship of the Ring", id="S001.1", price="5.99", summary="Hobbits")
        b2 = Book(name="The Two Towers", id="S001.2", price="5.99", summary="More hobbits")
        b3 = Book(name="Return of the King", id="S001.3", price="6.99", summary="Yet more hobbits")
        jrr = Author(name="JRR Tolkien", from_country="England")
        cls.bookseries = BookSeries(
            name="Lord of the Rings", id="S001", genres=["fantasy"], creator=jrr, books=[b1, b2, b3]
        )

    def test_yaml_dumper(self):
        """Test the yaml emitter"""
        self.dump_test("book_series_lotr.yaml", lambda out_fname: yaml_dumper.dump(self.bookseries, out_fname))
        self.dumps_test("book_series_lotr.yaml", lambda: yaml_dumper.dumps(self.bookseries))

        # test contents of yaml file with cleaned dict made from bookseries instance in setup
        with open(self.env.input_path("book_series_lotr.yaml")) as f:
            data = yaml.safe_load(f)
            # explicitly confirm that unset fields aren't written to the file
            for i in range(3):
                "genres" not in data["books"][i].keys()
                "inStock" not in data["books"][i].keys()
                "creator" not in data["books"][i].keys()
            self.assertEqual(data, remove_empty_items(self.bookseries.model_dump()))

    def test_json_dumper(self):
        """Test the json emitter"""
        self.dump_test("book_series_lotr.json", lambda out_fname: json_dumper.dump(self.bookseries, out_fname))
        self.dumps_test("book_series_lotr.json", lambda: json_dumper.dumps(self.bookseries))

        # test contents of json file with cleaned dict made from bookseries instance in setup
        with open(self.env.input_path("book_series_lotr.json")) as f:
            data = json.load(f)
            # explicitly confirm that unset fields aren't written to the file
            for i in range(3):
                "genres" not in data["books"][i].keys()
                "inStock" not in data["books"][i].keys()
                "creator" not in data["books"][i].keys()
            self.assertEqual(data, remove_empty_items(self.bookseries.model_dump()))

        # test @type is added to the top level and is assigned correct type when inject_type is True
        bookseries_with_type = json.loads(json_dumper.dumps(self.bookseries, inject_type=True))
        self.assertIn("@type", bookseries_with_type)
        self.assertEqual("BookSeries", bookseries_with_type.get("@type"))

        # test @type is not added to the top level when inject_type is False
        bookseries_without_type = json.loads(json_dumper.dumps(self.bookseries, inject_type=False))
        self.assertNotIn("@type", bookseries_without_type)
        self.assertEqual(None, bookseries_without_type.get("@type"))


class PydanticDumpersDateTestCase(LoaderDumperTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Generate an example with a date for testing purposes"""
        LoaderDumperTestCase.setUpClass()
        b1 = BirthEvent(started_at_time="2021-01-01", ended_at_time="2021-01-02")

        cls.person = Person(id="P01", name="John Doe", has_birth_event=b1)

    def test_yaml_dumper(self):
        """Test the yaml emitter"""
        # with open(self.env.input_path('kitchen_sink_person_01.yaml'), 'w', encoding='utf-8') as f:
        #     # write the yaml file
        #     f.write(yaml_dumper.dumps(self.person))
        # with open(self.env.input_path('kitchen_sink_person_01.json'), 'w', encoding='utf-8') as f:
        #     # write the json file
        #     f.write(json_dumper.dumps(self.person, inject_type=False))

        self.dump_test("kitchen_sink_person_01.yaml", lambda out_fname: yaml_dumper.dump(self.person, out_fname))
        self.dumps_test("kitchen_sink_person_01.yaml", lambda: yaml_dumper.dumps(self.person))

    def test_json_dumper(self):
        """Test the json emitter"""
        self.dump_test("kitchen_sink_person_01.json", lambda out_fname: json_dumper.dump(self.person, out_fname))
        self.dumps_test("kitchen_sink_person_01.json", lambda: json_dumper.dumps(self.person))


class Event(BaseModel):
    """Pydantic model with date and datetime fields, the Python types of the LinkML date and datetime ranges."""

    day: date
    at: datetime


@pytest.mark.parametrize(
    "dumps,loads",
    [
        (lambda e: json_dumper.dumps(e, inject_type=False), json.loads),
        (yaml_dumper.dumps, yaml.safe_load),
    ],
    ids=["json", "yaml"],
)
def test_dumper_writes_dates_as_iso_8601_strings(
    dumps: Callable[[BaseModel], str], loads: Callable[[str], Any]
) -> None:
    """Dates and datetimes are written as xsd:date and xsd:dateTime strings, not as native YAML timestamps."""
    event = Event(day=date(2021, 1, 1), at=datetime(2024, 5, 15, 15, 51, 15, tzinfo=UTC))
    assert loads(dumps(event)) == {"day": "2021-01-01", "at": "2024-05-15T15:51:15+00:00"}
