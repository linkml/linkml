import pytest
import unittest

from linkml_runtime.utils.csvutils import _get_key_config, get_configmap
from linkml_runtime.utils.schemaview import SchemaView
from tests.support.test_environment import TestEnvironmentTestCase
from tests.test_utils.environment import env


class CsvUtilTestCase(TestEnvironmentTestCase):
    env = env

    def test_null_configmap(self):
        get_configmap(None, "unknown")
        # TODO: with pytest, use captlog to verify the output
        # assert 'Index slot or schema not specified' in caplog.text

    def test_get_configmap(self):
        fname = env.input_path('kitchen_sink.yaml')
        schema = SchemaView(fname)
        get_configmap(schema, "unknown")


if __name__ == '__main__':
    unittest.main()
