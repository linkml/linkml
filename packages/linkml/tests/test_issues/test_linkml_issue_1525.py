from linkml.generators.javagen import JavaGenerator
from tests.utils.fileutils import assert_file_contains

schema_str = """
id: http://example.com/person
name: datetest
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types

classes:
  SomethingWithDate:
    slots:
      - date_and_time
      - date_only
      - time_only

slots:
  date_and_time:
    range: datetime
  date_only:
    range: date
  time_only:
    range: time
"""


def test_javagen_with_date_slots(tmp_path):
    """
    Check that date and time slots are rendered with the correct types in Java code.

    See https://github.com/linkml/linkml/issues/1525.
    """
    JavaGenerator(schema_str).serialize(directory=str(tmp_path))
    assert_file_contains(tmp_path / "SomethingWithDate.java", "ZonedDateTime dateAndTime")
    assert_file_contains(tmp_path / "SomethingWithDate.java", "LocalDate dateOnly")
    assert_file_contains(tmp_path / "SomethingWithDate.java", "Instant timeOnly")
