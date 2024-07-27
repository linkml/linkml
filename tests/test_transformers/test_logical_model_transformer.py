from pathlib import Path

import pytest
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition

from linkml.transformers.logical_model_transformer import (
    LogicalModelTransformer,
    UnsatisfiableAttribute,
)
from linkml.utils.schema_builder import SchemaBuilder

THIS_DIR = Path(__file__).parent
OUTPUT_DIR = THIS_DIR / "output"


@pytest.mark.parametrize("abstract", [False, True])
@pytest.mark.parametrize("default_range", [None, "string", "Any"])
@pytest.mark.parametrize("preserve_class_is_a", [False, True])
@pytest.mark.parametrize("force_any_of", [False, True])
def test_simple(default_range, preserve_class_is_a, abstract, force_any_of):
    """
    Test with a simple schema structure involving inheritance.

    :param default_range:
    :param preserve_class_is_a:
    :param abstract:
    :param force_any_of:
    :return:
    """
    sb = SchemaBuilder()
    sb.add_class("Thing", abstract=abstract, slots=["id", "name"])
    sb.add_class("Person", slots={"age": {"range": "integer"}}, is_a="Thing")
    if default_range == "Any":
        sb.add_class("Any", class_uri="linkml:Any")
    sb.add_slot("id", identifier=True, replace_if_present=True)
    sb.add_slot("name", required=True, replace_if_present=True)
    tr = LogicalModelTransformer(preserve_class_is_a=preserve_class_is_a)
    sb.add_defaults()
    sb.schema.default_range = default_range
    tr.set_schema(sb.schema)
    flat_schema = tr.transform(force_any_of=force_any_of)
    thing = flat_schema.classes["Thing"]
    actual_default_range = default_range if default_range != "Any" else None
    if not force_any_of:
        assert thing.attributes["name"].range == actual_default_range
    else:
        assert len(thing.attributes["name"].any_of) == 1
        assert thing.attributes["name"].any_of[0].range == actual_default_range
    person = flat_schema.classes["Person"]
    if not force_any_of:
        assert person.attributes["age"].range == "integer"
    else:
        assert len(person.attributes["age"].any_of) == 1
        assert person.attributes["age"].any_of[0].range == "integer"
    if preserve_class_is_a:
        assert "id" not in person.attributes
    else:
        assert person.attributes["id"].identifier is True
        if not force_any_of:
            assert person.attributes["name"].range == actual_default_range
            assert person.attributes["name"].required is True
    sb.add_class("Organization", is_a="Thing")
    sb.add_class("Container", slots=[SlotDefinition("entities", range="Thing", multivalued=True)])
    tr.set_schema(sb.schema)
    flat_schema = tr.transform()
    container = flat_schema.classes["Container"]
    entities_att = container.attributes["entities"]
    if preserve_class_is_a:
        # range is preserved
        if not force_any_of:
            assert entities_att.range == "Thing"
    else:
        # when fully unrolled a non-leaf class as range becomes as any_of ranges
        assert entities_att.range is None
        any_of = entities_att.any_of
        if abstract:
            # abstract classes should not be included in full enrolled results
            assert len(any_of) == 2
            assert {"Organization", "Person"} == {c.range for c in any_of}
        else:
            assert len(any_of) == 3
            assert {"Organization", "Person", "Thing"} == {c.range for c in any_of}


@pytest.mark.parametrize("default_range", [None, "string", "Any"])
@pytest.mark.parametrize("preserve_class_is_a", [False, True])
def test_unrestricted_range(default_range, preserve_class_is_a):
    """
    Test a schema with unrestricted ranges at slot level.

    :param default_range:
    :param preserve_class_is_a:
    :return:
    """
    sb = SchemaBuilder()
    sb.add_class("Thing", slots=["id", "name", "a_number", "foo"])
    sb.add_class(
        "Person",
        slots={"age": {"range": "integer"}},
        slot_usage={"name": {"range": "string"}},
        is_a="Thing",
    )
    sb.add_class("Any", class_uri="linkml:Any")
    sb.add_slot("id", identifier=True, replace_if_present=True)
    sb.add_slot("name", required=True, range="Any", replace_if_present=True)
    sb.add_slot("a_number", replace_if_present=True, any_of=[{"range": "integer"}, {"range": "float"}])
    sb.add_slot("foo", replace_if_present=True, any_of=[{"range": "string"}, {"range": "Any"}])
    tr = LogicalModelTransformer(preserve_class_is_a=preserve_class_is_a)
    sb.schema.default_range = default_range
    tr.set_schema(sb.schema)
    flat_schema = tr.transform(simplify=True)
    thing = flat_schema.classes["Thing"]
    person = flat_schema.classes["Person"]
    assert person.attributes["age"].range == "integer", "direct assertion"
    assert person.attributes["name"].range == "string", "range is restricted by slot_usage"
    assert thing.attributes["name"].range is None, "Any is eliminated"
    assert thing.attributes["foo"].range is None, "the union of Any and string is Any"
    if preserve_class_is_a:
        assert "id" not in person.attributes, "id is assumed to be inherited from Thing"
        thing_id = thing.attributes["id"]
        if default_range is None:
            assert thing_id.range is None, "no default, Any assumed"
        elif default_range == "Any":
            assert thing_id.range is None, "Any is eliminated"
        elif default_range == "string":
            assert thing_id.range == "string", "unassigned range assigned to default"
        else:
            raise ValueError(f"Unexpected default_range: {default_range}")
    else:
        person_id = person.attributes["id"]
        thing_id = thing.attributes["id"]
        if default_range is None:
            assert person_id.range is None, "no default, Any assumed"
            assert thing_id.range is None, "no default, Any assumed"
        elif default_range == "Any":
            assert person_id.range is None, "Any is eliminated"
            assert thing_id.range is None, "Any is eliminated"
        elif default_range == "string":
            assert person_id.range == "string", "unassigned range assigned to default"
            assert thing_id.range == "string", "unassigned range assigned to default"
        else:
            raise ValueError(f"Unexpected default_range: {default_range}")


def test_unsatisfiable():
    """
    Test a schema that is unsatisfiable, e.g. when maximum/minimum value ranges do not intersect.

    Tests for:

    - incompatible domain and range
    - incompatible max/min values
    """
    sb = SchemaBuilder()
    sb.add_class("Thing", slots=["id", "name"])
    sb.add_class("Person", slots={"age": {"range": "integer"}, "pets": {"multivalued": True}}, is_a="Thing")
    sb.add_class("Person2", is_a="Person", slot_usage={"age": {"range": "string"}})
    tr = LogicalModelTransformer()
    sb.add_defaults()
    tr.set_schema(sb.schema)
    with pytest.raises(UnsatisfiableAttribute):
        _ = tr.transform()
    del sb.schema.classes["Person2"]
    tr.set_schema(sb.schema)
    _ = tr.transform()
    sb.add_slot("bad_slot", range="integer", minimum_value=-100, maximum_value=-2)
    age_slot = sb.schema.slots["age"]
    age_slot.is_a = "bad_slot"
    age_slot.minimum_value = 0
    age_slot.maximum_value = 100
    tr.set_schema(sb.schema)
    assert sb.schema.slots["age"].minimum_value == 0, "check direct assignment"
    with pytest.raises(UnsatisfiableAttribute):
        _ = tr.transform()


@pytest.mark.parametrize(
    "person_min,person_max,person2_min,person2_max",
    [
        (0, 5, 1, 3),
        (2, None, None, 1),
        (None, None, None, None),
        (1, 1, 1, 1),
        (2, 1, None, None),
        (None, None, 2, 1),
    ],
)
def test_cardinality(person_min, person_max, person2_min, person2_max):
    """
    Test a schema that is unsatisfiable via min/max cardinality
    """
    sb = SchemaBuilder()
    sb.add_class("Thing", slots=["id", "name"])
    sb.add_class(
        "Person",
        slots={"pets": {"multivalued": True, "minimum_cardinality": person_min, "maximum_cardinality": person_max}},
        is_a="Thing",
    )
    sb.add_class(
        "Person2",
        is_a="Person",
        slot_usage={"pets": {"minimum_cardinality": person2_min, "maximum_cardinality": person2_max}},
    )
    tr = LogicalModelTransformer()
    sb.add_defaults()
    tr.set_schema(sb.schema)
    if person_min is None:
        entailed_person2_min = person2_min
    elif person2_min is None:
        entailed_person2_min = person_min
    else:
        entailed_person2_min = max(person_min, person2_min)
    if person_max is None:
        entailed_person2_max = person2_max
    elif person2_max is None:
        entailed_person2_max = person_max
    else:
        entailed_person2_max = min(person_max, person2_max)
    if entailed_person2_max is None or entailed_person2_min is None:
        satisfiable = True
    else:
        satisfiable = entailed_person2_min <= entailed_person2_max
    if satisfiable:
        s2 = tr.transform()
        entailed_att = s2.classes["Person2"].attributes["pets"]
        assert (entailed_att.minimum_cardinality, entailed_att.maximum_cardinality) == (
            entailed_person2_min,
            entailed_person2_max,
        )
    else:
        with pytest.raises(UnsatisfiableAttribute):
            _ = tr.transform()


def test_type_inheritance():
    """
    Test that type inheritance is properly unrolled.

    """
    sb = SchemaBuilder()
    sb.add_type("AgeType", typeof="integer", minimum_value=0, maximum_value=1000)
    sb.add_type("CodeType", typeof="string", pattern=r"^[A-Z][a-z]+$")
    sb.add_type("PersonCodeType", typeof="CodeType", pattern=r"^P[A-Z][a-z]+$")
    sb.add_type(
        "FooType",
        typeof="integer",
        any_of=[
            {"minimum_value": 0, "maximum_value": 100},
            {"minimum_value": 200, "maximum_value": 300},
        ],
    )
    sb.add_slot("id", identifier=True, range="CodeType")
    sb.add_slot("name", range="string")
    sb.add_slot("age", range="AgeType")
    sb.add_slot("foo", range="FooType")
    sb.add_class("Thing", slots=["id", "name", "foo"])
    sb.add_class(
        "Person",
        slots=["age"],
        is_a="Thing",
        slot_usage={"id": {"range": "PersonCodeType"}, "age": {"maximum_value": 200}},
    )
    sb.add_defaults()
    tr = LogicalModelTransformer()
    tr.set_schema(sb.schema)
    # flat_schema = tr.transform(simplify=False)
    # print(yaml_dumper.dumps(flat_schema))
    flat_schema = tr.transform(simplify=True)
    p = flat_schema.classes["Person"]
    id_slot = p.attributes["id"]
    assert id_slot.range == "PersonCodeType"
    assert id_slot.identifier is True
    assert {r"^P[A-Z][a-z]+$", r"^[A-Z][a-z]+$"} == {t.pattern for t in id_slot.all_of}.union({id_slot.pattern})
    age_slot = p.attributes["age"]
    assert age_slot.range == "AgeType"
    assert (age_slot.minimum_value, age_slot.maximum_value) == (0, 200)
    foo_slot = p.attributes["foo"]
    assert len(foo_slot.any_of) == 2
    assert {0, 200} == {t.minimum_value for t in foo_slot.any_of}


@pytest.mark.parametrize("inlined_as_list", [False, True])
@pytest.mark.parametrize("inlined", [False, True])
@pytest.mark.parametrize("multivalued", [False, True])
@pytest.mark.parametrize("pattern", [None, "^[A-Z][a-z]+$"])
@pytest.mark.parametrize("preserve_class_is_a", [False, True])
def test_any_of_with_required(preserve_class_is_a, pattern, multivalued, inlined, inlined_as_list):
    """
    Test a schema that uses any_of.

    The schema includes a slot manufactured_by that is a list of either Organization or Person.

    :param preserve_class_is_a:
    :param pattern:
    :param multivalued:
    :param inlined:
    :param inlined_as_list:
    :return:
    """
    sb = SchemaBuilder()
    sb.add_class("Thing", slots=["id", "name"])
    sb.add_class("Person", slots={"age": {"range": "integer"}}, is_a="Thing")
    sb.add_class(
        "Employee",
        is_a="Person",
        slots={
            "salary": {"range": "integer", "required": True},
            "manager": {"range": "Employee"},
            "employer": {"range": "Organization"},
        },
    )

    sb.add_class("Organization", is_a="Thing")
    sb.add_class("Company", is_a="Organization")
    sb.add_slot("id", identifier=True, replace_if_present=True)
    sb.add_slot("name", required=True, replace_if_present=True)
    sb.add_class(
        "Device",
        slots={
            "manufactured_by": {
                "multivalued": multivalued,
                "any_of": [
                    {
                        "range": "Organization",
                        "pattern": pattern,
                        "inlined": inlined,
                        "inlined_as_list": inlined_as_list,
                        "required": True,
                    },
                    {"range": "Person"},
                ],
            }
        },
    )
    tr = LogicalModelTransformer(preserve_class_is_a=preserve_class_is_a)
    sb.add_defaults()
    tr.set_schema(sb.schema)
    flat_schema = tr.transform()
    device = flat_schema.classes["Device"]

    manufactured_by = device.attributes["manufactured_by"]
    py_field = tr.attribute_as_python_field(manufactured_by)
    any_of = manufactured_by.any_of
    assert len(any_of) == 2
    required_exprs = [c for c in any_of if c.required]
    non_required_exprs = [c for c in any_of if not c.required]
    assert len(required_exprs) == 1
    assert len(non_required_exprs) == 1
    required_expr = required_exprs[0]
    non_required_expr = non_required_exprs[0]
    if preserve_class_is_a:
        assert "Organization" == required_expr.range
        assert "Person" == non_required_expr.range
        if not multivalued:
            assert py_field in [
                "manufactured_by: Union[Organization, Optional[Person]]",
                "manufactured_by: Union[Optional[Person], Organization]",
            ], "unexpected for multivalued=False"
        else:
            # assert py_field == "xx"
            assert "Collection" in py_field, f"expected Collection for multivalued; attr={manufactured_by.multivalued}"
    else:
        assert {"Organization", "Company"} == {c.range for c in required_expr.any_of}
        assert {"Person", "Employee"} == {c.range for c in non_required_expr.any_of}
        assert "Employee" in py_field
        # assert "xx" == py_field


@pytest.mark.parametrize("specify_redundant", [False, True])
@pytest.mark.parametrize("preserve_class_is_a", [False, True])
def test_deep_schema(specify_redundant, preserve_class_is_a):
    """
    Test a schema that uses deep inheritance as well as many boolean combinations of constructs.

    :param specify_redundant:
    :param preserve_class_is_a:
    :return:
    """
    sb = SchemaBuilder()
    # Classes: two parallel hierarchies, C, and D.
    # The C classes will point to the D classes via slot 's'.
    cns = ["C", "C1", "C2", "C1a", "C1b", "C2a", "C2b"]
    cns += [cn.replace("C", "D") for cn in cns]
    # Slots:
    # - s (connects C to D)
    # - t (integer), constrained by minimum_value and maximum_value
    # - u (default string), constrained by pattern
    # - v (float)
    sns = ["s", "s1", "s2", "s1a", "s1b", "s2a", "s2b"]
    sns += (
        [sn.replace("s", "t") for sn in sns]
        + [sn.replace("s", "u") for sn in sns]
        + [sn.replace("s", "v") for sn in sns]
    )
    # Mixins: M and N
    mns = ["M", "M1", "M2", "M1a", "M1b", "M2a", "M2b"]
    mns += [mn.replace("M", "N") for mn in mns]
    # Slot assignments:
    for sn in sns:
        p = sn[0:-1]
        p = None if p == "" else p
        any_of = None
        range = None
        # only assert ranges at the roots
        if specify_redundant or len(sn) == 1:
            if sn.startswith("s"):
                range = "D"
            elif sn.startswith("t"):
                range = "integer"
            elif sn.startswith("u"):
                range = None
            elif sn.startswith("v"):
                range = "float"
            else:
                raise AssertionError(f"Bad slot name: {sn}")
        # make the u slot progressively more restricted via pattern as we go down the hierarchy.
        # each individual assertion is an any_of that constrains EITHER start OR end;
        # thus the overall effect is a conjunction of disjunctive constraints.
        if sn.startswith("u"):
            any_of = [
                {"pattern": f"^{sn}"},
                {"pattern": f"{sn}$"},
            ]
        sb.add_slot(sn, is_a=p, range=range, any_of=any_of)
    # identifier slot
    sb.add_slot("id", identifier=True, range="string")
    main_s = "s2a"
    main_t = "t2a"
    # Mixins
    for mn in mns:
        p = mn[0:-1]
        p = None if p == "" else p
        # mixin slots on leaf classes
        if len(mn) == 3:
            # mixin_slots = [mn.replace("M", "u"), mn.replace("N", "v")]
            mixin_slots = ["u" + mn[1:], "v" + mn[1:]]
        else:
            mixin_slots = []
        sb.add_class(mn, mixin=True, is_a=p, slots=mixin_slots)
    # Classes
    for cn in cns:
        extra = {}
        p = cn[0:-1]
        p = None if p == "" else p
        if cn == "C":
            slots = ["id", main_s]
        elif cn == "D":
            slots = [main_t]
        else:
            slots = []
        if cn.startswith("C"):
            # Cx classes point to Dx classes via slot s
            slot_usage = SlotDefinition(main_s, range=cn.replace("C", "D"))
            # Cx has mixins Mx and Nx
            mixins = [cn.replace("C", "M"), cn.replace("C", "N")]
        else:
            # D classes are ints with progressively more constrained numeric ranges
            slot_usage = SlotDefinition(main_t, minimum_value=len(cn), maximum_value=10 - len(cn))
            mixins = []
        sb.add_class(cn, is_a=p, slot_usage=[slot_usage], mixins=mixins, slots=slots, **extra)
    sb.add_defaults()
    schema = sb.schema
    # local_id = f"SR{specify_redundant}-PCI{preserve_class_is_a}"
    # print(yaml_dumper.dump(schema, f"/tmp/asserted-schema-{local_id}.yaml"))
    sv = SchemaView(schema)
    flattener = LogicalModelTransformer(sv, preserve_class_is_a=preserve_class_is_a)
    new_schema = flattener.transform(simplify=False)
    # print(f"## NEW SCHEMA")
    # print(yaml_dumper.dumps(new_schema))
    # print(yaml_dumper.dump(new_schema, f"/tmp/trSCHEMA-{local_id}.yaml"))
    flattener.simplify(new_schema)
    # _dump_schema(new_schema, local_id)
    # print(yaml_dumper.dump(new_schema, f"/tmp/trSIMPLIFIED-{local_id}.yaml"))
    class_C = new_schema.classes["C"]
    class_C1 = new_schema.classes["C1"]
    class_C1a = new_schema.classes["C1a"]
    c_s2a = class_C.attributes["s2a"]
    c1_s2a = class_C1.attributes["s2a"]
    c1a_u1a = class_C1a.attributes["u1a"]
    if not preserve_class_is_a:
        assert {"D", "D1", "D2", "D1a", "D1b", "D2a", "D2b"} == {c.range for c in c_s2a.any_of}
        assert {"D1", "D1a", "D1b"} == {c.range for c in c1_s2a.any_of}
        assert c_s2a.range is None
        assert c1_s2a.range is None
        assert class_C.attributes["id"].identifier is True
        assert class_C1.attributes["id"].identifier is True
    else:
        assert c_s2a.range == "D"
        assert c1_s2a.range == "D1"
        assert class_C.attributes["id"].identifier is True
        assert "id" not in class_C1.attributes
    assert len(c1a_u1a.any_of) > 1


def _dump_schema(schema: SchemaDefinition, local_id: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(yaml_dumper.dump(schema, f"{OUTPUT_DIR}/logical-model-{local_id}.yaml"))
