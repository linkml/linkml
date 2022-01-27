import unittest


class BasicExample(unittest.TestCase):
    """An illustration of failed java generation will go here.
    Right now I'm just getting used to unittest"""

    def test_valid_math(self):
        self.assertEqual(1, 2 / 2)

    def test_bogus_math(self):
        self.assertEqual(1, 0.5 + 0.501)


if __name__ == "__main__":
    unittest.main()
