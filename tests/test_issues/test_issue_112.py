import unittest

import requests

from linkml.generators.yumlgen import YumlGenerator
from tests.test_issues.environment import env
from tests.utils.test_environment import TestEnvironmentTestCase


class EmptyClassTestCase(TestEnvironmentTestCase):
    env = env

    def test_prefix(self):
        env.generate_single_file(
            "issue112.yuml",
            lambda: YumlGenerator(env.input_path("issue_112.yaml")).serialize(),
            value_is_returned=True,
        )
        with open(env.expected_path("issue112.yuml")) as f:
            url = f.read()
        resp = requests.get(url)
        self.assertTrue(resp.ok)


if __name__ == "__main__":
    unittest.main()
