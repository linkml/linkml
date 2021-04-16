import os
import unittest

from linkml.generators import markdowngen
from tests.test_scripts.environment import env
from tests.utils.clicktestcase import ClickTestCase


class GenMarkdownTestCase(ClickTestCase):
    testdir = "genmarkdown"
    click_ep = markdowngen.cli
    prog_name = "gen-markdown"
    env = env

    def test_help(self):
        self.do_test("--help", 'help')

    def test_meta(self):
        self.do_test([], 'meta', is_directory=True)

    def _exists(self, *path: str) -> None:
        expected = self.expected_file_path(*path)
        self.assertTrue(os.path.exists(expected), f"Failed to create {expected}")

    def test_issue_2(self):
        self.do_test(f'-c example -i ', 'issue2', is_directory=True)
        self._exists('issue2', 'images', 'Example.svg')

    def test_no_types(self):
        """ Test the no types directory setting """
        self.do_test(f'--notypesdir --warnonexist --log_level WARNING', 'meta_no_types', is_directory=True)

    @unittest.expectedFailure
    def test_issue_2_excerpt(self):
        # This was a part of the unit tests for a while.  We have NO idea why we thought that markdown should NOT
        # have been generated for the abstract slot in meta.yaml, but that is definitely not the case now.
        self.assertFalse(os.path.exists(self.expected_file_path('issue2', 'abstract.md')))


if __name__ == '__main__':
    unittest.main()
