from linkml.generators.javagen import JavaGenerator
from tests.utils.fileutils import assert_file_contains

PACKAGE = "org.sink.kitchen"


def test_javagen_records(kitchen_sink_path, tmp_path):
    """Generate java records"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE, generate_records=True)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(
        tmp_path / "Address.java",
        "public record Address(String street, String city, BigDecimal altitude)",
        after="package org.sink.kitchen",
    )


def test_javagen_classes(kitchen_sink_path, tmp_path):
    """Generate java classes"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(tmp_path / "Address.java", "public class Address", after="package org.sink.kitchen")
