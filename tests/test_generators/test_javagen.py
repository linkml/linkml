import os
import unittest
from contextlib import redirect_stdout

from linkml.generators.javagen import JavaGenerator
from tests.test_generators.environment import env

SCHEMA = env.input_path("kitchen_sink.yaml")
JAVA_DIR = env.expected_path("kitchen_sink_java")
PACKAGE = "org.sink.kitchen"


# TODO: move this somewhere reusable
def assert_file_contains(filename, text, after=None, description=None) -> None:
    found = False
    is_after = False  ## have we reached the after mark?
    with open(os.path.join(JAVA_DIR, filename)) as stream:
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
    def test_javagen_records(self):
        """Generate java records"""
        gen = JavaGenerator(SCHEMA, package=PACKAGE, generate_records=True)
        gen.serialize(directory=JAVA_DIR)
        assert_file_contains(
            "Address.java",
            "public record Address(String street, String city)",
            after="package org.sink.kitchen",
        )

    def test_javagen_classes(self):
        """Generate java classes"""
        gen = JavaGenerator(SCHEMA, package=PACKAGE)
        gen.serialize(directory=JAVA_DIR)
        assert_file_contains(
            "Address.java", "public class Address", after="package org.sink.kitchen"
        )


if __name__ == "__main__":
    unittest.main()
