import pytest
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinitionName, SlotDefinitionName
from rdflib import URIRef
from rdflib.term import Literal

from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml.generators.shacl.shacl_ifabsent_processor import ShaclIfAbsentProcessor

schema_base = """
id: ifabsent_tests
name: ifabsent_tests

prefixes:
  ex: https://example.org/
default_prefix: ex

classes:
  Student:
    attributes:
"""


def test_process_ifabsent_string():
    schema_view = SchemaView(
        schema_base
        + """
    - name: studentName
      range: string
      ifabsent: string(N/A)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("studentName")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("N/A", datatype=ShaclDataType.STRING.uri_ref)


def test_process_ifabsent_boolean():
    schema_view = SchemaView(
        schema_base
        + """
    - name: didHomework
      range: boolean
      ifabsent: boolean(True)
    - name: wasLate
      range: boolean
      ifabsent: boolean(False)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("didHomework")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("True", datatype=ShaclDataType.BOOLEAN.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("wasLate")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("False", datatype=ShaclDataType.BOOLEAN.uri_ref)


def test_process_ifabsent_numeric():
    schema_view = SchemaView(
        schema_base
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

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("age")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("17", datatype=ShaclDataType.INTEGER.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("averageScore")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("13.52", datatype=ShaclDataType.FLOAT.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("minimalScore")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("8.453", datatype=ShaclDataType.DOUBLE.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("maximalScore")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("18.9", datatype=ShaclDataType.DECIMAL.uri_ref)


def test_process_ifabsent_time():
    schema_view = SchemaView(
        schema_base
        + """
    - name: arrivalTime
      range: time
      ifabsent: time(08:13:04)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("arrivalTime")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("08:13:04", datatype=ShaclDataType.TIME.uri_ref)


def test_process_ifabsent_date():
    schema_view = SchemaView(
        schema_base
        + """
    - name: lastSickLeave
      range: date
      ifabsent: date(2024-06-26)
    - name: graduationDate
      range: date_or_datetime
      ifabsent: date(2026-06-18)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("lastSickLeave")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("2024-06-26", datatype=ShaclDataType.DATE.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("graduationDate")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("2026-06-18", datatype=ShaclDataType.DATE.uri_ref)


def test_process_ifabsent_datetime():
    schema_view = SchemaView(
        schema_base
        + """
    - name: creationTimestamp
      range: datetime
      ifabsent: datetime(2024-04-12T11:45:34)
    - name: lastMeetingWithParents
      range: date_or_datetime
      ifabsent: datetime(2024-02-09T18:25:44Z)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("creationTimestamp")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("2024-04-12T11:45:34", datatype=ShaclDataType.DATETIME.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("lastMeetingWithParents")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("2024-02-09T18:25:44", datatype=ShaclDataType.DATETIME.uri_ref)


def test_process_ifabsent_curie():
    schema_view = SchemaView(
        schema_base
        + """
    - name: definition
      range: curie
      ifabsent: curie(wikipedia:Student)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("definition")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("wikipedia:Student", datatype=ShaclDataType.CURIE.uri_ref)


def test_process_ifabsent_uri():
    schema_view = SchemaView(
        schema_base
        + """
    - name: definition
      range: uri
      ifabsent: uri(https://en.wikipedia.org/wiki/Student)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("definition")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("https://en.wikipedia.org/wiki/Student", datatype=ShaclDataType.URI.uri_ref)


def test_process_ifabsent_uriorcurie():
    schema_view = SchemaView(
        schema_base
        + """
    - name: definition_A
      range: uriorcurie
      ifabsent: string(https://en.wikipedia.org/wiki/Student)
    - name: definition_B
      range: uriorcurie
      ifabsent: string(ex:Student)
    - name: definition_C
      range: uriorcurie
      ifabsent: string(wikipedia:Student)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("definition_A")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("https://en.wikipedia.org/wiki/Student", datatype=ShaclDataType.URI.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("definition_B")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("https://example.org/Student", datatype=ShaclDataType.URI.uri_ref)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("definition_C")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("wikipedia:Student", datatype=ShaclDataType.URI.uri_ref)


def test_process_class_curie():
    schema_view = SchemaView(
        schema_base
        + """
    - name: thisURI
      range: uriorcurie
      ifabsent: class_curie
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("thisURI")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == URIRef("https://example.org/Student")


def test_process_ifabsent_enum():
    schema_view = SchemaView(
        schema_base
        + """
    - name: presence
      range: PresenceEnum
      ifabsent: PresenceEnum(Missing)

enums:
  PresenceEnum:
    permissible_values:
      Present:
        description: It's there.
      Missing:
        description: It's not there.
"""
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("presence")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("Missing")


def test_process_missing_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: missing
      range: string
      ifabsent:
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert (
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("missing")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
        is None
    )


def test_process_empty_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: empty
      range: string
      ifabsent: string('')
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("empty")], schema_view.all_classes()[ClassDefinitionName("Student")]
    ) == Literal("", datatype=ShaclDataType.STRING.uri_ref)


def test_process_incompatible_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: incompatible
      range: decimal
      ifabsent: not a decimal
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    assert processor.process_slot(
        schema_view.all_slots()[SlotDefinitionName("incompatible")],
        schema_view.all_classes()[ClassDefinitionName("Student")],
    ) == Literal("not a decimal", datatype=ShaclDataType.DECIMAL.uri_ref)


def test_process_impossible_range_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: impossibleRange
      range: ImpossibleEnum
      ifabsent: ImpossibleEnum(DivideByZero)
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(ValueError) as e:
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("impossibleRange")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )

    assert str(e.value) == (
        "The ifabsent value `ImpossibleEnum(DivideByZero)` of the `impossibleRange` slot could not " "be processed"
    )


def test_process_nc_name_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: unimplementedNcName
      range: ncname
      ifabsent: ncname()
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(NotImplementedError):
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplementedNcName")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )


def test_process_object_identifier_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: unimplementedObjectIdentifier
      range: objectidentifier
      ifabsent: objectidentifier()
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(NotImplementedError):
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplementedObjectIdentifier")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )


def test_process_node_identifier_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: unimplementedNodeIdentifier
      range: nodeidentifier
      ifabsent: nodeidentifier()
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(NotImplementedError):
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplementedNodeIdentifier")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )


def test_process_json_pointer_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: unimplementedJsonPointer
      range: jsonpointer
      ifabsent: jsonpointer()
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(NotImplementedError):
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplementedJsonPointer")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )


def test_process_json_path_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: unimplementedJsonPath
      range: jsonpath
      ifabsent: jsonpath()
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(NotImplementedError):
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplementedJsonPath")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )


def test_process_sparql_path_ifabsent_attribute():
    schema_view = SchemaView(
        schema_base
        + """
    - name: unimplementedSparqlPath
      range: sparqlpath
      ifabsent: sparqlpath()
    """
    )

    processor = ShaclIfAbsentProcessor(schema_view)

    with pytest.raises(NotImplementedError):
        processor.process_slot(
            schema_view.all_slots()[SlotDefinitionName("unimplementedSparqlPath")],
            schema_view.all_classes()[ClassDefinitionName("Student")],
        )
