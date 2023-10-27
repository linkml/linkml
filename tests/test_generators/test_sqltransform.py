from collections import Counter

import pytest
from linkml_runtime.linkml_model import SlotDefinition
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.relmodel_transformer import (
    ForeignKeyPolicy,
    RelationalModelTransformer,
    TransformationResult,
    get_foreign_key_map,
    get_primary_key_attributes,
)
from linkml.utils.schema_builder import SchemaBuilder

DUMMY_CLASS = "c"


"""
Tests transformation from a linkml model to a relational model (independent of SQL).

Note: This tests the transformation between one LinkML model and another.

The input model may include mulitvalued fields, but these are transformed away in
the relational representation.
"""


def _translate(builder: SchemaBuilder) -> TransformationResult:
    sv = SchemaView(builder.schema)
    sqltr = RelationalModelTransformer(sv)
    return sqltr.transform()


def test_inject_primary_key():
    """
    test a minimal schema with no primary names declared
    """
    b = SchemaBuilder()
    slots = ["name", "description"]
    b.add_class(DUMMY_CLASS, slots)
    rel_schema = _translate(b).schema
    assert Counter(slots + ["id"]) == Counter(rel_schema.classes[DUMMY_CLASS].attributes.keys())
    assert rel_schema.mappings == []
    rsv = SchemaView(rel_schema)
    assert "id" == rsv.get_identifier_slot(DUMMY_CLASS).name
    assert ["id"] == get_primary_key_attributes(rel_schema.classes[DUMMY_CLASS])
    assert {} == get_foreign_key_map(rel_schema.classes[DUMMY_CLASS])


@pytest.mark.parametrize("c_has_pk", (True, False))
@pytest.mark.parametrize("d_has_pk", (True, False))
def test_injection_clash(c_has_pk, d_has_pk):
    """
    test conflict with injected primary key
    """
    name_slot = SlotDefinition("name")
    b = SchemaBuilder(name=f"test_conflicting_primary_key_name_{c_has_pk}_{d_has_pk}")
    b.add_class(
        "c",
        use_attributes=True,
        slots=[
            SlotDefinition("id", identifier=c_has_pk),
            name_slot,
            SlotDefinition(
                "has_ds",
                singular_name="has_d",
                range="d",
                multivalued=True,
                inlined=False,
            ),
        ],
    )
    b = b.add_class(
        "d",
        use_attributes=True,
        slots=[SlotDefinition("id", identifier=d_has_pk), name_slot],
    )
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    d = rsv.get_class("d")
    c_has_d = rsv.get_class("c_has_d")
    if c_has_pk:
        assert Counter(["id", "name"]) == Counter(c.attributes.keys())
        assert ["id"] == get_primary_key_attributes(c)
    else:
        assert Counter(["id", "uid", "name"]) == Counter(c.attributes.keys())
        assert ["uid"] == get_primary_key_attributes(c)
    if d_has_pk:
        assert Counter(["id", "name"]) == Counter(d.attributes.keys())
        assert ["id"] == get_primary_key_attributes(d)
    else:
        assert Counter(["id", "uid", "name"]) == Counter(d.attributes.keys())
        assert ["uid"] == get_primary_key_attributes(d)
    c_id_col = "id" if c_has_pk else "uid"
    d_id_col = "id" if d_has_pk else "uid"
    assert Counter([f"c_{c_id_col}", f"has_d_{d_id_col}"]) == Counter(c_has_d.attributes.keys())
    assert Counter([f"c_{c_id_col}", f"has_d_{d_id_col}"]) == Counter(get_primary_key_attributes(c_has_d))


def test_no_inject_primary_key():
    """
    PKs should not be injected if identifier is declared
    """
    b = SchemaBuilder()
    slots = ["name", "description"]
    b.add_class(DUMMY_CLASS, slots).set_slot("name", identifier=True)
    rel_schema = _translate(b).schema
    assert Counter(slots) == Counter(rel_schema.classes[DUMMY_CLASS].attributes.keys())
    assert [] == rel_schema.mappings
    rsv = SchemaView(rel_schema)
    assert "name" == rsv.get_identifier_slot(DUMMY_CLASS).name
    assert ["name"] == get_primary_key_attributes(rel_schema.classes[DUMMY_CLASS])


def test_multivalued_literal():
    """
    Test translation of lists of strings
    """
    b = SchemaBuilder()
    b.add_class("c", ["name", "description", "aliases"]).set_slot("aliases", multivalued=True, singular_name="alias")
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    assert c
    assert Counter(["id", "name", "description"]) == Counter(c.attributes.keys())
    c_alias = rsv.get_class("c_alias")
    assert c_alias
    c_alias_c_id = rsv.induced_slot("c_id", c_alias.name)
    assert c_alias_c_id.range == "c"
    assert Counter(["c_id", "alias"]) == Counter(c_alias.attributes.keys())
    assert [] == rel_schema.mappings
    assert ["id"] == get_primary_key_attributes(c)
    assert {} == get_foreign_key_map(c)
    assert {"c_id": "c.id"} == get_foreign_key_map(c_alias)


def test_inject_foreign_key():
    """
    test translation of a single-valuaed object reference to a foreign key
    """
    b = SchemaBuilder()
    slots = ["name", "description", "has_d"]
    b.add_class("c", slots).add_class("d", ["name"]).set_slot("has_d", range="d")
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    d = rsv.get_class("d")
    assert Counter(["id", "name", "description", "has_d_id"]) == Counter(c.attributes.keys())
    assert Counter(["id", "name"]) == Counter(d.attributes.keys())
    assert ["id"] == get_primary_key_attributes(c)
    assert ["id"] == get_primary_key_attributes(d)
    assert {"has_d_id": "d.id"} == get_foreign_key_map(c)
    assert {} == get_foreign_key_map(d)


def test_inject_backref_foreign_key():
    """
    test translation of a multi-valued object reference to a foreign key from the referenced class
    """
    b = SchemaBuilder()
    slots = ["name", "description", "has_ds"]
    b.add_class("c", slots).add_class("d", ["name"]).set_slot(
        "has_ds",
        singular_name="has_d",
        alias="d",
        range="d",
        multivalued=True,
        inlined=True,
    )
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    d = rsv.get_class("d")
    assert Counter(["id", "name", "description"]) == Counter(c.attributes.keys())
    assert Counter(["id", "name", "c_id"]) == Counter(d.attributes.keys())
    assert ["id"] == get_primary_key_attributes(c)
    assert ["id"] == get_primary_key_attributes(d)
    assert {} == get_foreign_key_map(c)
    assert {"c_id": "c.id"} == get_foreign_key_map(d)


@pytest.mark.parametrize("add_id_to_c", (True, False))
@pytest.mark.parametrize("add_id_to_d", (True, False))
def test_inject_many_to_many(add_id_to_c, add_id_to_d):
    """
    test translation of a non-inlined multivalued reference to a class into
    a linking table
    """
    # It should not matter if we invent the "id" identifier
    # column on tables lacking an identifier column
    slots_c = ["name", "description", "has_ds"]
    slots_d = ["name"]
    b = SchemaBuilder()
    b.add_class("c", slots_c + (["id"] if add_id_to_c else []))
    b = b.add_class("d", slots_d + (["id"] if add_id_to_d else []))
    b = b.set_slot("has_ds", singular_name="has_d", range="d", multivalued=True, inlined=False)
    if add_id_to_c or add_id_to_d:
        b = b.set_slot("id", identifier=True)
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    d = rsv.get_class("d")
    c_has_d = rsv.get_class("c_has_d")
    assert Counter(["id", "name", "description"]) == Counter(c.attributes.keys())
    assert Counter(["id", "name"]) == Counter(d.attributes.keys())
    assert Counter(["c_id", "has_d_id"]) == Counter(c_has_d.attributes.keys())
    assert Counter(["id"]) == Counter(get_primary_key_attributes(c))
    assert Counter(["id"]) == Counter(get_primary_key_attributes(d))
    assert Counter(["c_id", "has_d_id"]) == Counter(get_primary_key_attributes(c_has_d))
    assert {} == get_foreign_key_map(c)
    assert {} == get_foreign_key_map(d)
    assert {"c_id": "c.id", "has_d_id": "d.id"} == get_foreign_key_map(c_has_d)


def test_inject_many_to_many_with_inheritance():
    """
    as above, but with inheritance
    """
    b = SchemaBuilder()
    slots = ["name", "description", "has_ds"]
    b.add_class("c", slots).add_class("d", ["name"]).set_slot(
        "has_ds", singular_name="has_d", range="d", multivalued=True, inlined=False
    )
    b.add_class("c1", is_a="c", slot_usage={"has_ds": SlotDefinition("has_ds", range="d1")})
    b.add_class("d1", is_a="d")
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    d = rsv.get_class("d")
    rsv.get_class("c1")
    d1 = rsv.get_class("d1")
    c_has_d = rsv.get_class("c_has_d")
    rsv.get_class("c1_has_d")
    assert ["id"] == get_primary_key_attributes(d1)
    assert Counter(["id", "name", "description"]) == Counter(c.attributes.keys())
    assert Counter(["id", "name"]) == Counter(d.attributes.keys())
    assert Counter(["c_id", "has_d_id"]) == Counter(c_has_d.attributes.keys())
    assert Counter(["id"]) == Counter(get_primary_key_attributes(c))
    assert ["id"] == get_primary_key_attributes(d)
    assert Counter(["c_id", "has_d_id"]) == Counter(get_primary_key_attributes(c_has_d))
    assert {} == get_foreign_key_map(c)
    assert {} == get_foreign_key_map(d)
    assert {"c_id": "c.id", "has_d_id": "d.id"} == get_foreign_key_map(c_has_d)


def test_no_foreign_keys():
    """Test Simple transformation with no injections of FKs."""
    b = SchemaBuilder()
    slots = ["name", "description", "has_ds"]
    b.add_class("c", slots).add_class("d", ["name"]).set_slot(
        "has_ds", singular_name="has_d", range="d", multivalued=True, inlined=False
    )
    b.add_class("c1", is_a="c", slot_usage={"has_ds": SlotDefinition("has_ds", range="d1")})
    b.add_class("d1", is_a="d")
    sv = SchemaView(b.schema)
    sqltr = RelationalModelTransformer(sv, foreign_key_policy=ForeignKeyPolicy.NO_FOREIGN_KEYS)
    result = sqltr.transform()
    rel_schema = result.schema
    rsv = SchemaView(rel_schema)
    assert "c_has_d" not in rsv.all_classes()
    c1 = rsv.get_class("c1")
    assert Counter(c1.attributes.keys()) == Counter(["name", "description", "has_ds"])


def test_aliases():
    """
    tests using alias to override name
    """
    b = SchemaBuilder()
    b.add_class(
        "c",
        [
            SlotDefinition("foo_name", alias="name"),
            SlotDefinition("foo_description", alias="description"),
            SlotDefinition("foo_aliases", alias="aliases", multivalued=True),
            SlotDefinition("foo_has_d", alias="has_d", multivalued=True, range="d"),
        ],
    )
    b.add_class("d", [SlotDefinition("name")])
    rel_schema = _translate(b).schema
    rsv = SchemaView(rel_schema)
    c = rsv.get_class("c")
    d = rsv.get_class("d")
    c_has_d = rsv.get_class("c_has_d")
    assert sorted(c.attributes.keys()) == ["description", "id", "name"]
    assert sorted(d.attributes.keys()) == ["id", "name"]
    assert sorted(c_has_d.attributes.keys()) == ["c_id", "has_d_id"]

    assert sorted(get_primary_key_attributes(c)) == ["id"]
    assert sorted(get_primary_key_attributes(d)) == ["id"]
    assert sorted(get_primary_key_attributes(c_has_d)) == ["c_id", "has_d_id"]

    assert get_foreign_key_map(c) == {}
    assert get_foreign_key_map(d) == {}
    assert get_foreign_key_map(c_has_d) == {"c_id": "c.id", "has_d_id": "d.id"}


def test_sqlt_on_metamodel():
    sv = package_schemaview("linkml_runtime.linkml_model.meta")
    sqltr = RelationalModelTransformer(sv)
    result = sqltr.transform()
    rschema = result.schema
    # test Annotation is handled correctly. This has a key annotation_tag with alias 'tag'
    assert "id" not in rschema.classes["annotation"].attributes.keys()
    assert "tag" in rschema.classes["annotation"].attributes.keys()
    # TODO: in the metamodel this changed from string to Any;
    # currently behavior of Any is undefined in SQL Transform
    # assert "value" in rschema.classes["annotation"].attributes.keys()
    cd = rschema.classes["class_definition"]
    assert cd.name == "class_definition"
    assert "name" in cd.attributes.keys()
    assert "primary_key" in cd.attributes["name"].annotations


def test_sqlt_complete_example(input_path):
    """Test Relational Model Transform on personinfo.yaml schema."""
    sv = SchemaView(input_path("personinfo.yaml"))
    sqltr = RelationalModelTransformer(sv)
    result = sqltr.transform()
    rschema = result.schema
    assert rschema.name == "personinfo_relational"
    sv = SchemaView(rschema)

    # check roots, mixins, and abstracts are omitted
    # NOTE: for now we keep all classes in
    # assert 'Container' not in sv.all_classes()
    # assert 'HasAliases' not in sv.all_classes()
    # assert 'WithLocation' not in sv.all_classes()

    # check multivalued are preserved as slots;
    # these are referenced from inverses
    # assert sv.get_slot('aliases').multivalued
    assert sv.get_slot("has_medical_history").multivalued
    assert sv.get_slot("has_familial_relationships").multivalued
    assert sv.get_slot("has_employment_history").multivalued

    c = sv.get_class("Person")
    assert "aliases" not in c.attributes
    assert "aliases" not in c.slots

    for cn in ["Person", "Organization"]:
        c = sv.get_class(f"{cn}_alias")
        assert len(c.attributes) == 2
        ranges = [s.range for s in c.attributes.values()]
        assert sorted(ranges) == sorted([cn, "string"])

    for relationship_class in [
        "FamilialRelationship",
        "EmploymentEvent",
        "MedicalEvent",
    ]:
        c = sv.get_class(relationship_class)
        assert any(a for a in c.attributes.values() if a.range == "Person" and a.name == "Person_id")
        pk = sv.get_identifier_slot(cn)
        assert pk is not None
        assert pk.name == "id"

    news_event_pk = sv.get_identifier_slot("NewsEvent")
    assert news_event_pk is not None
    assert news_event_pk.name == "id"

    for cn in ["Person", "Organization"]:
        c = sv.get_class(f"{cn}_has_news_event")
        a1 = c.attributes["has_news_event_id"]
        assert a1.range == "NewsEvent"
        a2 = c.attributes[f"{cn}_id"]
        assert a2.range == cn
