import unittest

from linkml_runtime.loaders import yaml_loader, json_loader
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.books_normalized_pydantic import BookSeries
from tests.test_loaders_dumpers.models.kitchen_sink_pydantic import Dataset


class PydanticLoadersUnitTest(LoaderDumperTestCase):
    env = env

    def test_yaml_loader_single(self):
        """ Load obo_sample.yaml, emit obo_sample_yaml.yaml and compare to obo_sample_output.yaml """
        self.loader_test('book_series_lotr.yaml', BookSeries, yaml_loader)

    def test_json_loader(self):
        """ Load obo_sample.json, emit obo_sample_json.yaml and check the results """
        self.loader_test('book_series_lotr.json', BookSeries, json_loader)

    def test_yaml_loader_kitchen_sink(self):
        self.loader_test('kitchen_sink_normalized_inst_01.yaml', Dataset, yaml_loader)

    def test_json_loader_kitchen_sink(self):
        self.loader_test('kitchen_sink_normalized_inst_01.json', Dataset, json_loader)

if __name__ == '__main__':
    unittest.main()
