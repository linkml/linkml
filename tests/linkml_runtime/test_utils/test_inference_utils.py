import os
from decimal import Decimal

import pytest

from linkml_runtime.utils.inference_utils import (
    Config,
    Policy,
    generate_slot_value,
    infer_all_slot_values,
    infer_slot_value,
)
from linkml_runtime.utils.schemaview import SchemaView
from tests.linkml_runtime.test_utils import INPUT_DIR
from tests.linkml_runtime.test_utils.model.inference_example import AgeEnum, Container, Evil, Person, Relationship

SCHEMA = os.path.join(INPUT_DIR, "inference-example.yaml")

AGE_IN_YEARS = 12
FIRST, LAST = "x", "y"
FULL = f"{FIRST} {LAST}"
REPLACE_ME = "REPLACE ME"


def test_rstring_serialization():
    """Tests serialization of strings via linkml:string_serialization"""
    sv = SchemaView(SCHEMA)
    p = Person(first_name=FIRST, last_name=LAST)
    v = generate_slot_value(p, "full_name", sv)


def test_string_serialization():
    """Tests serialization of strings via linkml:string_serialization"""
    sv = SchemaView(SCHEMA)
    p = Person(first_name=FIRST, last_name=LAST)
    v = generate_slot_value(p, "full_name", sv)
    assert v == FULL
    infer_slot_value(p, "full_name", sv)
    assert p.full_name == FULL
    p = Person(first_name=FIRST, last_name=LAST)
    infer_all_slot_values(p, schemaview=sv)
    assert p.full_name == FULL
    # test override
    p = Person(first_name=FIRST, last_name=LAST, full_name=REPLACE_ME)
    infer_all_slot_values(p, schemaview=sv, policy=Policy.OVERRIDE)
    assert p.full_name == FULL
    # test keep
    p = Person(first_name=FIRST, last_name=LAST, full_name=REPLACE_ME)
    infer_all_slot_values(p, schemaview=sv, policy=Policy.KEEP)
    assert p.full_name == REPLACE_ME
    # test strict
    p = Person(first_name=FIRST, last_name=LAST, full_name=REPLACE_ME)
    with pytest.raises(ValueError):
        infer_all_slot_values(p, schemaview=sv, policy=Policy.STRICT)
    # same value test
    for policy in [Policy.OVERRIDE, Policy.STRICT, Policy.KEEP]:
        p = Person(first_name=FIRST, last_name=LAST, full_name=FULL)
        infer_all_slot_values(p, schemaview=sv, policy=policy)
        assert p.full_name == FULL
    # test recursion
    c = Container(persons=[Person(first_name=FIRST, last_name=LAST)])
    infer_all_slot_values(c, schemaview=sv)
    assert c.persons[0].full_name == FULL
    # test slots with spaces
    p = Person(slot_with_spaces="test")
    infer_all_slot_values(p, schemaview=sv)
    assert p.derived_slot_with_spaces == "test"


def test_infer_expressions():
    """Tests using of string_serialization to infer value setting from expressions"""
    sv = SchemaView(SCHEMA)
    p = Person(age_in_years=Decimal(AGE_IN_YEARS))
    config = Config(use_expressions=True)
    policy = Policy.STRICT
    infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
    assert p.age_in_months == p.age_in_years * 12
    assert p.is_juvenile is True
    assert AGE_IN_YEARS == p.age_in_years
    infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
    assert p.age_in_months == p.age_in_years * 12
    p.age_in_months = None
    infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
    assert p.age_in_months == p.age_in_years * 12
    # reverse
    p = Person(age_in_months=Decimal(AGE_IN_YEARS) * 12)
    infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)
    assert p.age_in_months == p.age_in_years * 12
    assert p.age_in_years == AGE_IN_YEARS
    # inconsistency
    p = Person(age_in_years=Decimal(AGE_IN_YEARS), age_in_months=Decimal(AGE_IN_YEARS))
    with pytest.raises(ValueError):
        infer_all_slot_values(p, schemaview=sv, config=config, policy=Policy.STRICT)
    p = Person(age_in_years=Decimal(AGE_IN_YEARS), age_in_months=Decimal(AGE_IN_YEARS))
    infer_all_slot_values(p, schemaview=sv, config=config, policy=Policy.OVERRIDE)
    # final answer should be consistent
    assert p.age_in_months == p.age_in_years * 12
    # answer not guaranteed
    assert p.age_in_years == AGE_IN_YEARS or p.age_in_years == AGE_IN_YEARS / 12

    p = Person(age_in_years=Decimal(50))
    config = Config(use_expressions=True)
    infer_all_slot_values(p, schemaview=sv, config=config)
    assert not p.is_juvenile
    p = Person(age_in_years=Decimal(10))
    config = Config(use_expressions=True)
    infer_all_slot_values(p, schemaview=sv, config=config)
    assert p.is_juvenile
    assert p.age_category == AgeEnum("juvenile")
    assert p.age_category.code == AgeEnum.juvenile
    # test slots with spaces
    p = Person(slot_with_spaces="test")
    infer_all_slot_values(p, schemaview=sv, config=config)
    assert p.derived_expression_from_spaces == "test"


def test_if_then():
    sv = SchemaView(SCHEMA)
    p = Person(first_name="x", last_name="y", age_in_years=Decimal(AGE_IN_YEARS))
    config = Config(use_expressions=True)
    infer_all_slot_values(p, schemaview=sv, config=config)
    assert p.summary == f"xy AGE: {AGE_IN_YEARS}"
    p = Person(first_name="x", last_name="y")
    infer_all_slot_values(p, schemaview=sv, config=config)
    assert p.summary == "xy NO AGE SPECIFIED"


def test_custom_function():
    sv = SchemaView(SCHEMA)
    p = Person(first_name="abc", last_name="def", age_in_years=Decimal(AGE_IN_YEARS))
    config = Config(resolve_function=lambda x, _: f'"{x.upper()}"' if isinstance(x, str) else x)
    infer_all_slot_values(p, schemaview=sv, config=config)
    assert p.full_name == '"ABC" "DEF"'
    assert p.age_in_years == Decimal(AGE_IN_YEARS)


def test_protect_against_evil():
    """
    Ensure that certain patterns cannot be evaluated

    See `<https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string>`_
    """
    sv = SchemaView(SCHEMA)
    p = Evil()
    config = Config(use_expressions=True)
    policy = Policy.OVERRIDE
    with pytest.raises(NotImplementedError):
        infer_all_slot_values(p, schemaview=sv, config=config, policy=policy)


def test_nesting():
    """Tests use of nested variables"""
    sv = SchemaView(SCHEMA)
    p1 = Person(first_name="a", last_name="b")
    p2 = Person(first_name="c", last_name="d")
    r = Relationship(person1=p1, person2=p2, type="SIBLING_OF")
    infer_all_slot_values(r, schemaview=sv)
    assert '"b, a" IS SIBLING_OF "d, c"' == r.description
    assert '"a b" IS SIBLING_OF "c d"' == r.description2
