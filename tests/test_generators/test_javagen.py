import os
import unittest
from contextlib import redirect_stdout


from linkml.generators.javagen import JavaGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path('kitchen_sink.yaml')
JAVA_DIR = env.expected_path('kitchen_sink_java')
PACKAGE = 'org.sink.kitchen'

def assert_file_contains(filename, text, after=None, description=None) -> None:
    found = False
    is_after = False  ## have we reached the after mark?
    with open(os.path.join(MD_DIR, filename)) as stream:
        for line in stream.readlines():
            if text in line:
                if after is None:
                    found = True
                else:
                    if is_after:
                        found = True
            if after is not None and after in line:
                is_after = True
    assert found

class JavaGeneratorTestCase(unittest.TestCase):

    def test_javagen(self):
        """ Generate java classes  """
        gen = JavaGenerator(SCHEMA, package=PACKAGE)
        md = gen.serialize(directory=JAVA_DIR)




if __name__ == '__main__':
    unittest.main()
