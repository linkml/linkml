<<<<<<< HEAD
import pytest

from linkml.transformers.relmodel_transformer import (
    ForeignKeyPolicy,
    RelationalAnnotations,
    RelationalModelTransformer,
    add_attribute,
    get_primary_key_attributes,
)
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import Annotation, ClassDefinition, SchemaDefinition, SlotDefinition
=======
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from linkml_runtime import SchemaView
>>>>>>> main
from linkml_runtime.utils.schema_builder import SchemaBuilder


def test_nested_key():
    """
    Test that the nested key is correctly handled

    Expected:

    ```yaml
    ExamResult:
        attributes:
          name:
            key: true
            range: string
            required: true
          score:
            range: integer
          additional_info:
            range: string
          Student_id:
            annotations:
              backref:
                tag: backref
                value: 'true'
              rdfs:subPropertyOf:
                tag: rdfs:subPropertyOf
                value: rdf:subject
              primary_key:
                tag: primary_key
                value: 'true'
              foreign_key:
                tag: foreign_key
                value: Student.id
            description: Autocreated FK slot
            slot_uri: rdf:subject
            range: Student
        unique_keys:
          Student_name:
            unique_key_slots:
            - Student_id
            - name
    """
    sb = SchemaBuilder()
    sb.add_slot("id", identifier=True)
    sb.add_slot("full_name")
    sb.add_slot("exam_results", range="ExamResult", multivalued=True, inlined=True)
    sb.add_slot("name", key=True)
    sb.add_slot("score", range="integer")
    sb.add_class("Student", ["id", "full_name", "exam_results"])
    sb.add_class("ExamResult", ["name", "score", "additional_info"])
    sb.add_defaults()
    schema = sb.schema
    rmt = RelationalModelTransformer()
    rmt.schemaview = SchemaView(schema)
    result = rmt.transform("test")
    rel_schema = result.schema
    exam_result = rel_schema.classes["ExamResult"]
    assert exam_result
    exam_result_atts = exam_result.attributes
    student_id = exam_result_atts["Student_id"]
    assert student_id.range == "Student"
    assert not student_id.multivalued
    unique_keys = list(exam_result.unique_keys.values())
    assert len(unique_keys) == 1
    unique_key = unique_keys[0]
    assert sorted(unique_key.unique_key_slots) == ["Student_id", "name"]


# Tests for helper functions
def test_add_attribute() -> None:
    """Test that add_attribute inserts a slot into an attributes dict keyed by slot name."""
    attrs: dict[str, SlotDefinition] = {}
    slot = SlotDefinition(name="age", range="integer")
    add_attribute(attrs, slot)
    assert "age" in attrs
    assert attrs["age"] is slot


def test_get_primary_key_attributes_empty() -> None:
    """Test get_primary_key_attributes returns an empty list when no PK annotations exist."""
    cls = ClassDefinition(name="Person")
    cls.attributes["name"] = SlotDefinition(name="name", range="string")
    assert get_primary_key_attributes(cls) == []


def test_get_primary_key_attributes_with_pk() -> None:
    """Test get_primary_key_attributes returns the name of slots annotated as primary_key."""
    cls = ClassDefinition(name="Person")
    pk_slot = SlotDefinition(name="id")
    pk_slot.annotations[RelationalAnnotations.PRIMARY_KEY] = Annotation("primary_key", "true")
    cls.attributes["id"] = pk_slot
    cls.attributes["name"] = SlotDefinition(name="name")
    assert get_primary_key_attributes(cls) == ["id"]


# Tests for RelationalModelTransformer.add_primary_key


@pytest.mark.parametrize(
    "existing_attr_names, expected_pk_name",
    [
        ([], "id"),
        (["id"], "uid"),
        (["id", "uid"], "identifier"),
        (["id", "uid", "identifier"], "pk"),
    ],
)
def test_add_primary_key_candidate_names(existing_attr_names: list[str], expected_pk_name: str) -> None:
    """Test that add_primary_key uses the first available candidate name for the PK."""
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="Person")
    for attr_name in existing_attr_names:
        cls.attributes[attr_name] = SlotDefinition(name=attr_name, range="string")
    schema.classes["Person"] = cls
    sv = SchemaView(schema)

    pk = RelationalModelTransformer.add_primary_key("Person", sv)

    assert pk.name == expected_pk_name
    assert pk.identifier is True
    assert pk.range == "integer"
    assert expected_pk_name in sv.get_class("Person").attributes


def test_add_primary_key_all_candidates_taken() -> None:
    """Test that ValueError is raised when all candidate PK names are already in use."""
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="Person")
    for attr_name in ["id", "uid", "identifier", "pk"]:
        cls.attributes[attr_name] = SlotDefinition(name=attr_name, range="string")
    schema.classes["Person"] = cls
    sv = SchemaView(schema)

    with pytest.raises(ValueError, match="Cannot add primary key to class Person"):
        RelationalModelTransformer.add_primary_key("Person", sv)


def test_add_primary_key_pk_at_start_of_attributes() -> None:
    """Test that the injected PK is prepended as the first attribute of the class."""
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="Person")
    cls.attributes["name"] = SlotDefinition(name="name", range="string")
    cls.attributes["age"] = SlotDefinition(name="age", range="integer")
    schema.classes["Person"] = cls
    sv = SchemaView(schema)

    pk = RelationalModelTransformer.add_primary_key("Person", sv)

    attr_names = list(sv.get_class("Person").attributes.keys())
    assert attr_names[0] == pk.name
    assert set(attr_names) == {pk.name, "name", "age"}


def test_add_primary_key_does_not_call_set_modified() -> None:
    """
    Verify that add_primary_key does NOT call sv.set_modified().

    The caller is responsible for calling set_modified() once after all PKs are
    injected in bulk (see the single target_sv.set_modified() in transform()).
    Calling class_induced_slots() before add_primary_key fills the lru_cache;
    after add_primary_key the cache entry is still stale (no identifier) until
    set_modified() is explicitly called.
    """
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="Person")
    schema.classes["Person"] = cls
    sv = SchemaView(schema)

    # Prime the class_induced_slots cache — no identifier present yet.
    assert sv.class_induced_slots("Person") == []

    # add_primary_key modifies the class attributes dict without calling set_modified().
    RelationalModelTransformer.add_primary_key("Person", sv)

    # The class object is immediately updated …
    assert "id" in sv.get_class("Person").attributes

    # … but the cached class_induced_slots result is still stale.
    assert sv.class_induced_slots("Person") == []

    # After an explicit set_modified() the cache is busted and the PK is reflected.
    sv.set_modified()
    induced = sv.class_induced_slots("Person")
    assert any(s.name == "id" and s.identifier for s in induced)


# Tests for RelationalModelTransformer.get_direct_identifier_attribute


def test_get_direct_identifier_attribute_with_identifier() -> None:
    """Test that get_direct_identifier_attribute returns the attribute with identifier=True."""
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="Person")
    cls.attributes["id"] = SlotDefinition(name="id", identifier=True)
    cls.attributes["name"] = SlotDefinition(name="name", range="string")
    schema.classes["Person"] = cls
    sv = SchemaView(schema)

    result = RelationalModelTransformer.get_direct_identifier_attribute(sv, "Person")
    assert result is not None
    assert result.name == "id"


def test_get_direct_identifier_attribute_with_key() -> None:
    """Test that get_direct_identifier_attribute returns the attribute with key=True."""
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="ExamResult")
    cls.attributes["name"] = SlotDefinition(name="name", key=True)
    cls.attributes["score"] = SlotDefinition(name="score", range="integer")
    schema.classes["ExamResult"] = cls
    sv = SchemaView(schema)

    result = RelationalModelTransformer.get_direct_identifier_attribute(sv, "ExamResult")
    assert result is not None
    assert result.name == "name"


def test_get_direct_identifier_attribute_none() -> None:
    """Test that get_direct_identifier_attribute returns None when no identifier or key exists."""
    schema = SchemaDefinition(id="test", name="test")
    cls = ClassDefinition(name="Address")
    cls.attributes["street"] = SlotDefinition(name="street", range="string")
    schema.classes["Address"] = cls
    sv = SchemaView(schema)

    assert RelationalModelTransformer.get_direct_identifier_attribute(sv, "Address") is None


# Tests for RelationalModelTransformer.transform with various FK policies


def test_transform_no_foreign_keys_policy() -> None:
    """Test that NO_FOREIGN_KEYS policy skips surrogate PK injection and FK annotations."""
    sb = SchemaBuilder()
    sb.add_slot("name", range="string")
    sb.add_class("Person", ["name"])
    sb.add_defaults()
    rmt = RelationalModelTransformer(foreign_key_policy=ForeignKeyPolicy.NO_FOREIGN_KEYS)
    rmt.schemaview = SchemaView(sb.schema)
    result = rmt.transform("test")
    person = result.schema.classes["Person"]

    assert "id" not in person.attributes
    assert not any(RelationalAnnotations.PRIMARY_KEY in a.annotations for a in person.attributes.values())


def test_transform_multiple_classes_bulk_pk_injection() -> None:
    """
    Test that transform correctly injects PKs for multiple classes via a single
    set_modified() call after the bulk loop.

    add_primary_key is called once per class without calling set_modified() itself;
    the transformer calls set_modified() once after the entire PK-injection loop.
    All classes must still receive a properly annotated surrogate PK.
    """
    sb = SchemaBuilder()
    sb.add_slot("name", range="string")
    sb.add_slot("score", range="integer")
    for class_name in ["Alpha", "Beta", "Gamma"]:
        sb.add_class(class_name, ["name", "score"])
    sb.add_defaults()
    rmt = RelationalModelTransformer()
    rmt.schemaview = SchemaView(sb.schema)
    result = rmt.transform("test")
    rel_schema = result.schema

    for class_name in ["Alpha", "Beta", "Gamma"]:
        cls = rel_schema.classes[class_name]
        pk_attrs = get_primary_key_attributes(cls)
        assert len(pk_attrs) == 1, f"Expected exactly 1 PK for {class_name}, got {pk_attrs}"


def test_transform_inject_fk_for_all_refs_vs_nested() -> None:
    """
    Test the distinction between INJECT_FK_FOR_ALL_REFS and INJECT_FK_FOR_NESTED.

    When the referenced class has its own identifier (so it is not "inlined"),
    INJECT_FK_FOR_NESTED does NOT rename the referencing slot, while
    INJECT_FK_FOR_ALL_REFS DOES rename it to ``<slot>_<pk>``.
    """
    sb = SchemaBuilder()
    sb.add_slot("id", identifier=True)
    sb.add_slot("street", range="string")
    sb.add_slot("name", range="string")
    sb.add_slot("address", range="Address")  # non-inlined; target has its own identifier
    sb.add_class("Address", ["id", "street"])
    sb.add_class("Person", ["name", "address"])
    sb.add_defaults()

    # INJECT_FK_FOR_NESTED: address NOT renamed (Address has its own identifier → not inlined)
    rmt_nested = RelationalModelTransformer(foreign_key_policy=ForeignKeyPolicy.INJECT_FK_FOR_NESTED)
    rmt_nested.schemaview = SchemaView(sb.schema)
    person_nested = rmt_nested.transform("test").schema.classes["Person"]
    assert "address" in person_nested.attributes
    assert "address_id" not in person_nested.attributes

    # INJECT_FK_FOR_ALL_REFS: address IS renamed to address_id
    rmt_all = RelationalModelTransformer(foreign_key_policy=ForeignKeyPolicy.INJECT_FK_FOR_ALL_REFS)
    rmt_all.schemaview = SchemaView(sb.schema)
    person_all = rmt_all.transform("test").schema.classes["Person"]
    assert "address_id" in person_all.attributes
    assert "address" not in person_all.attributes
