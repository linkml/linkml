import unittest

import linkml_runtime

class TestPackageVersion(unittest.TestCase):
    def test_package_version(self):
        self.assertIsNotNone(linkml_runtime.__version__)
