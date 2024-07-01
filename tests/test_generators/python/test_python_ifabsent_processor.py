import pytest
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinitionName, SlotDefinitionName

from linkml.generators.python.python_ifabsent_processor import PythonIfAbsentProcessor

base_schema = """
id: ifabsent_tests
name: ifabsent_tests

prefixes:
  ex: https://example.org/
default_prefix: ex

classes:
  Student:
    attributes:
"""


@pytest.mark.parametrize("default_value", PythonIfAbsentProcessor.UNIMPLEMENTED_DEFAULT_VALUES)
def test_unimplemented_default_value(default_value):
    schema = (
        base_schema
        + f"""
      - name: unimplemented
        ifabsent: {default_value}
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplemented")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        is None
    )


def test_string_default_value():
    schema = (
        base_schema
        + """
      - name: studentName
        range: string
        ifabsent: string(N/A)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("studentName")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == '"N/A"'
    )


def test_boolean_default_value():
    schema = (
        base_schema
        + """
      - name: didHomework
        range: boolean
        ifabsent: boolean(True)
      - name: wasLate
        range: boolean
        ifabsent: boolean(False)
      - name: invalidBoolean
        range: boolean
        ifabsent: boolean(invalid)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("didHomework")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "True"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("wasLate")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "False"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidBoolean")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `boolean(invalid)` of the `invalidBoolean` slot does not match a valid boolean value"
    )


def test_numeric_default_value():
    schema = (
        base_schema
        + """
      - name: age
        range: integer
        ifabsent: integer(17)
      - name: averageScore
        range: float
        ifabsent: float(13.52)
      - name: minimalScore
        range: double
        ifabsent: double(8.453)
      - name: maximalScore
        range: decimal
        ifabsent: decimal(18.9)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("age")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "17"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("averageScore")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "13.52"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("minimalScore")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "8.453"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("maximalScore")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "18.9"
    )


def test_time_default_value():
    schema = (
        base_schema
        + """
      - name: arrivalTime
        range: time
        ifabsent: time(08:13:04)
      - name: departureTime
        range: time
        ifabsent: time(17:32:22.5)
      - name: invalidTime
        range: time
        ifabsent: time(invalid)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("arrivalTime")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "time(8, 13, 4)"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("departureTime")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "time(17, 32, 22)"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidTime")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `time(invalid)` of the `invalidTime` slot does not match a valid time value"
    )


def test_date_default_value():
    schema = (
        base_schema
        + """
      - name: lastSickLeave
        range: date
        ifabsent: date(2024-06-26)
      - name: graduationDate
        range: date_or_datetime
        ifabsent: date(2026-06-18)
      - name: invalidDate
        range: date
        ifabsent: date(invalid)
      - name: invalidDateOrDatetime
        range: date_or_datetime
        ifabsent: date(invalid)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("lastSickLeave")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "date(2024, 6, 26)"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("graduationDate")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "date(2026, 6, 18)"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidDate")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `date(invalid)` of the `invalidDate` slot does not match a valid date value"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidDateOrDatetime")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `date(invalid)` of the `invalidDateOrDatetime` slot does not match a valid date or "
        "datetime value"
    )


def test_datetime_default_value():
    schema = (
        base_schema
        + """
      - name: creationTimestamp
        range: datetime
        ifabsent: datetime(2024-04-12T11:45:34)
      - name: modificationTimestamp
        range: datetime
        ifabsent: datetime(2024-04-18T09:10:11Z)
      - name: lastMeetingWithParents
        range: date_or_datetime
        ifabsent: datetime(2024-02-09T18:25:44Z)
      - name: invalidDatetime
        range: datetime
        ifabsent: datetime(invalid)
      - name: invalidDateOrDatetime
        range: date_or_datetime
        ifabsent: datetime(invalid)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("creationTimestamp")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "datetime(2024, 4, 12, 11, 45, 34)"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("modificationTimestamp")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "datetime(2024, 4, 18, 9, 10, 11)"
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("lastMeetingWithParents")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "datetime(2024, 2, 9, 18, 25, 44)"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidDatetime")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `datetime(invalid)` of the `invalidDatetime` slot does not match a valid datetime value"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidDateOrDatetime")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `datetime(invalid)` of the `invalidDateOrDatetime` slot does not match a valid date or "
        "datetime value"
    )


def test_uri_default_value():
    schema = (
        base_schema
        + """
      - name: classUri
        range: uri
        ifabsent: uri(https://example.org/class/123)
      - name: schoolUri
        range: uri
        ifabsent: uri(ex:school/321)
      - name: parentsUri
        range: uri
        ifabsent: uri(https://parents.com/456)
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("classUri")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == 'EX["class/123"]'
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("schoolUri")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == 'EX["school/321"]'
    )
    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("parentsUri")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == '"https://parents.com/456"'
    )


def test_enum_default_value():
    schema = (
        base_schema
        + """
      - name: presence
        range: PresenceEnum
        ifabsent: PresenceEnum(Missing)
      - name: invalidPresence
        range: PresenceEnum
        ifabsent: PresenceEnum(invalid)

enums:
  PresenceEnum:
    permissible_values:
      Present:
        description: It's there.
      Missing:
        description: It's not there.
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("presence")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "PresenceEnum.Missing"
    )

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("invalidPresence")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `PresenceEnum(invalid)` of the `invalidPresence` slot could not be processed"
    )


def test_bnode_default_value():
    schema = (
        base_schema
        + """
      - name: bnode
        range: Student
        ifabsent: bnode
    """
    )
    schema_view = SchemaView(schema)

    processor = PythonIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("bnode")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        == "bnode()"
    )
