from linkml.generators.javagen import JavaGenerator

PACKAGE = "org.sink.kitchen"


# TODO: move this somewhere reusable
def assert_file_contains(filename, text, after=None, description=None) -> None:
    found = False
    is_after = False  # have we reached the after mark?
    with open(filename) as stream:
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


def test_javagen_records(kitchen_sink_path, tmp_path):
    """Generate java records"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE, generate_records=True)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(
        tmp_path / "Address.java",
        "public record Address(String street, String city)",
        after="package org.sink.kitchen",
    )


def test_javagen_classes(kitchen_sink_path, tmp_path):
    """Generate java classes"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(tmp_path / "Address.java", "public class Address", after="package org.sink.kitchen")
