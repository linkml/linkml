from linkml.generators.javagen import JavaGenerator
from linkml.generators.oocodegen import OOEnum, OOEnumValue
from tests.linkml.utils.fileutils import assert_file_contains

PACKAGE = "org.sink.kitchen"


def test_javagen_records(kitchen_sink_path, tmp_path):
    """Generate java records"""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE)
    gen.serialize(directory=str(tmp_path), template_variant="records")
    assert_file_contains(
        tmp_path / "Address.java",
        "public record Address(String street, String city, BigDecimal altitude)",
        after="package org.sink.kitchen",
    )


def test_javagen_with_custom_template(kitchen_sink_path, tmp_path):
    """Generate java records with a custom template.

    This should yield the same code as the test above, but by forcefully
    specifying the class-records template, instead of specifying the "records"
    variant and letting the generator pick the corresponding template.
    """

    gen = JavaGenerator(
        kitchen_sink_path,
        package=PACKAGE,
        template_file="packages/linkml/src/linkml/generators/javagen/class-records.jinja2",
    )
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


def test_javagen_classes_and_enums(kitchen_sink_path, tmp_path):
    """Generate both Java classes and enums."""
    gen = JavaGenerator(kitchen_sink_path, package=PACKAGE, true_enums=True)
    gen.serialize(directory=str(tmp_path))
    assert_file_contains(
        tmp_path / "CordialnessEnum.java", "public enum CordialnessEnum", after="package org.sink.kitchen"
    )
    assert_file_contains(
        tmp_path / "Relationship.java", "private CordialnessEnum cordialness;", after="package org.sink.kitchen"
    )


def test_generate_enum_objects(kitchen_sink_path):
    """Generate object representation of enums.

    Note that this is really a feature of OOCodeGenerator and not of
    JavaGenerator, but since OOCodeGenerator is abstract it has to be
    tested through a derived concrete class.
    """
    gen = JavaGenerator(kitchen_sink_path)
    enum_definitions = gen.schemaview.all_enums()
    enum_objects = gen.generate_enum_objects(enum_definitions)

    # Check that all enums are present
    for name in enum_definitions.keys():
        assert name in enum_objects

    # Check that one enum is complete
    expected_enum = OOEnum(name="FamilialRelationshipType")
    expected_enum.values = [
        OOEnumValue(label="SIBLING_OF", text="SIBLING_OF"),
        OOEnumValue(label="PARENT_OF", text="PARENT_OF"),
        OOEnumValue(label="CHILD_OF", text="CHILD_OF"),
    ]
    assert expected_enum == enum_objects["FamilialRelationshipType"]

    # Same, but with an enum with names that must be transformed
    expected_enum = OOEnum(name="OtherCodes")
    expected_enum.values = [OOEnumValue(label="a_b", text="a b")]
    assert expected_enum == enum_objects["other codes"]


def test_create_documents_includes_enums(kitchen_sink_path):
    """Check that the code generator generates documents for enums."""
    # Default mode: enums should not be included
    gen = JavaGenerator(kitchen_sink_path, true_enums=False)
    docs = gen.create_documents()
    assert not [doc for doc in docs if doc.enums]

    # "True enums" mode: one document per enum
    gen = JavaGenerator(kitchen_sink_path, true_enums=True)
    docs = gen.create_documents()
    enum_docs = [doc for doc in docs if doc.enums]
    assert len(enum_docs) == 7  # 6 enums in kitchen sink + 1 in core

    # A document contains either a class or an enum, but not both
    assert not [doc for doc in docs if doc.classes and doc.enums]
