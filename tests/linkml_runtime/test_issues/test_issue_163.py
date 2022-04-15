import os
import unittest

from linkml_runtime.utils.context_utils import parse_import_map


class Issue163TestCase(unittest.TestCase):
    def test_trailing_sep(self):
        """ Test the importmap namespace """
        importmap = parse_import_map('{ "base:": "base/" }', os.path.dirname(__file__))
        # TODO: see how this works in a windows environment
        self.assertTrue(importmap['base:'].endswith('/'), msg="Trailing separator stripped in import map parsing")


if __name__ == '__main__':
    unittest.main()
