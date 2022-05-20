import unittest


class ParserErrorTestCase(unittest.TestCase):
    """Test case to make sure ParserError exception
        type is present in the python dateutil 
        dependency specified in the Pipfile."""
    def test_missing_exception_type(self):
        try:
            from dateutil.parser import ParserError
        except ImportError:
            self.fail("ParserError() cannot be found in python-dateutil<2.8.1")


if __name__ == "__main__":
    unittest.main()
