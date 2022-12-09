import os
import unittest
from typing import Union, TextIO, Type, Optional

from hbreader import FileInfo

from linkml_runtime.loaders import yaml_loader, json_loader
from tests.test_loaders_dumpers.environment import env
from tests.test_loaders_dumpers.loaderdumpertestcase import LoaderDumperTestCase
from tests.test_loaders_dumpers.models.books_normalized_pydantic import BookSeries
from typing import List

class LoadersUnitTest(LoaderDumperTestCase):
    env = env

    def test_yaml_loader_single(self):
        """ Load obo_sample.yaml, emit obo_sample_yaml.yaml and compare to obo_sample_output.yaml """
        self.loader_test('book_series_lotr.yaml', BookSeries, yaml_loader)

    # def test_json_loader(self):
    #     """ Load obo_sample.json, emit obo_sample_json.yaml and check the results """
    #     self.loader_test('obo_sample.json', Package, json_loader)



if __name__ == '__main__':
    unittest.main()
