"""``has_member`` asks for a value satisfying an expression alike in the JSON Schema and SHACL generators.

A member is one value of a multivalued slot, so a slot without a value, absent
or empty, has no member.  In a condition of a class-level expression,
``has_member`` therefore decides whether the slot may be absent, and its member
takes the form of the condition.  The agreement tests validate the same
instance with both generated artifacts, loading it as RDF through the
generated JSON-LD context.
"""

import json
import logging
from typing import Any

import pytest
import yaml
from jsonschema import Draft201909Validator
from pyshacl import validate

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator
from tests.linkml.utils import generator_agreement

PREFIX = "@prefix ex: <https://example.org/membership/> . "


@pytest.fixture
def schema() -> dict[str, Any]:
    """A collection of tags, scores and inlined items."""
    return yaml.safe_load("""
id: https://example.org/membership
name: membership
prefixes:
  ex: https://example.org/membership/
  linkml: https://w3id.org/linkml/
default_prefix: ex
imports: [linkml:types]
classes:
  Collection:
    tree_root: true
    slots: [tags, scores, items]
  Item:
    slots: [status]
slots:
  tags: {range: string, multivalued: true}
  scores: {range: integer, multivalued: true}
  items: {range: Item, multivalued: true, inlined_as_list: true}
  status: {range: string}
""")


def verdicts(schema: dict[str, Any], instance: dict[str, Any]) -> tuple[bool, bool]:
    """Whether the JSON Schema and the SHACL shapes generated for *schema* accept *instance* of ``Collection``."""
    return generator_agreement.verdicts(schema, instance, "Collection")


def conforms(schema: dict[str, Any], data: str) -> bool:
    """Whether Turtle *data* conforms to the SHACL shapes generated for *schema*, which must pass meta-SHACL."""
    shapes = ShaclGenerator(yaml.safe_dump(schema), closed=False).serialize()
    return validate(
        data_graph=PREFIX + data,
        data_graph_format="turtle",
        shacl_graph=shapes,
        shacl_graph_format="turtle",
        meta_shacl=True,
    )[0]


def json_valid(schema: dict[str, Any], instance: dict[str, Any]) -> bool:
    """Whether the JSON Schema generated for *schema* accepts *instance* of ``Collection``."""
    json_schema = json.loads(JsonSchemaGenerator(yaml.safe_dump(schema), top_class="Collection").serialize())
    return Draft201909Validator(json_schema).is_valid(instance)


_READY = {"range_expression": {"slot_conditions": {"status": {"equals_string": "ready"}}}}


@pytest.mark.parametrize(
    "slot,member,values,valid",
    [
        pytest.param("tags", {"equals_string": "reviewed"}, ["reviewed", "pending"], True, id="match"),
        pytest.param("tags", {"equals_string": "reviewed"}, ["pending"], False, id="no-match"),
        # a slot without a value has no member
        pytest.param("tags", {"equals_string": "reviewed"}, [], False, id="empty"),
        pytest.param("tags", {"equals_string": "reviewed"}, None, False, id="absent"),
        pytest.param("tags", {}, ["anything"], True, id="any-value"),
        pytest.param("tags", {}, None, False, id="any-value-absent"),
        pytest.param("tags", {"equals_string_in": ["a", "b"], "pattern": "^a"}, ["a", "b"], True, id="conjunction"),
        pytest.param("tags", {"equals_string_in": ["a", "b"], "pattern": "^a"}, ["b"], False, id="conjunction-other"),
        pytest.param("scores", {"minimum_value": 10}, [9, 10], True, id="bound"),
        pytest.param("scores", {"minimum_value": 10}, [8, 9], False, id="bound-other"),
        # two values of one SHACL parameter hold together
        pytest.param("scores", {"minimum_value": 0, "equals_number": 0}, [-1, 0], True, id="repeated"),
        pytest.param("scores", {"minimum_value": 0, "equals_number": 0}, [-1, 1], False, id="repeated-other"),
        pytest.param("scores", {"minimum_value": 5, "equals_number": 3}, [3, 5], False, id="contradiction"),
        pytest.param("scores", {"minimum_value": 5, "equals_number": 7}, [6], False, id="repeated-second"),
        pytest.param("items", _READY, [{"status": "draft"}, {"status": "ready"}], True, id="range_expression"),
        pytest.param("items", _READY, [{"status": "draft"}], False, id="range_expression-other"),
        # a value whose status is unknown is not definitely no member
        pytest.param("items", _READY, [{"status": "draft"}, {}], True, id="range_expression-unknown"),
    ],
)
def test_slot_has_member(
    schema: dict[str, Any], slot: str, member: dict[str, Any], values: list | None, valid: bool
) -> None:
    """At least one value of the slot must satisfy the member expression; the others need not."""
    schema["slots"][slot]["has_member"] = member
    assert verdicts(schema, {} if values is None else {slot: values}) == (valid, valid)


_REVIEWED = {"has_member": {"equals_string": "reviewed"}}


@pytest.mark.parametrize(
    "expression,values,valid",
    [
        pytest.param({"all_of": [{"slot_conditions": {"tags": _REVIEWED}}]}, None, False, id="all_of-absent"),
        pytest.param({"all_of": [{"slot_conditions": {"tags": _REVIEWED}}]}, ["reviewed"], True, id="all_of"),
        pytest.param({"all_of": [{"slot_conditions": {"tags": _REVIEWED}}]}, ["pending"], False, id="all_of-other"),
        # has_member decides presence, so it is false, not unknown, for an absent slot
        pytest.param({"none_of": [{"slot_conditions": {"tags": _REVIEWED}}]}, None, True, id="none_of-absent"),
        pytest.param({"none_of": [{"slot_conditions": {"tags": _REVIEWED}}]}, ["pending"], True, id="none_of-other"),
        pytest.param(
            {"none_of": [{"slot_conditions": {"tags": _REVIEWED}}]}, ["pending", "reviewed"], False, id="none_of"
        ),
        pytest.param(
            {"any_of": [{"slot_conditions": {"tags": _REVIEWED}}, {"slot_conditions": {"scores": {"required": True}}}]},
            None,
            False,
            id="any_of-absent",
        ),
    ],
)
def test_has_member_in_class_expression(
    schema: dict[str, Any], expression: dict[str, Any], values: list | None, valid: bool
) -> None:
    """In a condition of a class-level expression, ``has_member`` is false for a slot without a value."""
    schema["classes"]["Collection"].update(expression)
    assert verdicts(schema, {} if values is None else {"tags": values}) == (valid, valid)


@pytest.mark.parametrize(
    "items,valid",
    [
        pytest.param([{}], True, id="unknown"),
        pytest.param([{"status": "draft"}], True, id="other"),
        pytest.param([{"status": "draft"}, {"status": "ready"}], False, id="match"),
    ],
)
def test_member_under_negation_takes_the_definite_form(schema: dict[str, Any], items: list, valid: bool) -> None:
    """Under ``none_of``, a member must definitely satisfy its expression to count."""
    schema["classes"]["Collection"]["none_of"] = [{"slot_conditions": {"items": {"has_member": _READY}}}]
    assert verdicts(schema, {"items": items}) == (valid, valid)


@pytest.mark.parametrize("scores,valid", [([5], True), ([-1, 11], True), ([11], False), ([-1], False)])
def test_members_of_two_conditions_may_be_one_value(schema: dict[str, Any], scores: list[int], valid: bool) -> None:
    """Each ``has_member`` asks for a value of its own expression, which may or may not be the same value."""
    schema["classes"]["Collection"]["all_of"] = [
        {"slot_conditions": {"scores": {"has_member": {"minimum_value": 0}}}},
        {"slot_conditions": {"scores": {"has_member": {"maximum_value": 10}}}},
    ]
    assert verdicts(schema, {"scores": scores}) == (valid, valid)


@pytest.mark.parametrize("statuses,valid", [(["draft", "ready"], True), (["draft"], False), ([], False)])
@pytest.mark.parametrize("in_class_expression", [False, True])
def test_has_member_on_values_inlined_as_dict(
    schema: dict[str, Any], statuses: list[str], valid: bool, in_class_expression: bool
) -> None:
    """The members of a slot inlined as a dict are the values of the dict."""
    schema["classes"]["Item"]["slots"].insert(0, "id")
    schema["slots"]["id"] = {"identifier": True, "range": "string"}
    del schema["slots"]["items"]["inlined_as_list"]
    schema["slots"]["items"]["inlined"] = True
    if in_class_expression:
        schema["classes"]["Collection"]["all_of"] = [{"slot_conditions": {"items": {"has_member": _READY}}}]
    else:
        schema["slots"]["items"]["has_member"] = _READY
    items = {f"i{n}": {"status": status} for n, status in enumerate(statuses)}
    assert json_valid(schema, {"items": items}) is valid
    data = "ex:c a ex:Collection" + "".join(f"; ex:items ex:{key}" for key in items) + " . "
    data += "".join(f'ex:{key} a ex:Item; ex:status "{value["status"]}" . ' for key, value in items.items())
    assert conforms(schema, data) is valid


@pytest.mark.parametrize("target", ["Collection", "SpecialCollection"])
@pytest.mark.parametrize(
    "values,valid",
    [(["reviewed", "pending"], True), (["pending"], False), (None, False)],
    ids=["match", "other", "absent"],
)
def test_has_member_is_inherited(schema: dict[str, Any], target: str, values: list | None, valid: bool) -> None:
    """A subclass keeps the ``has_member`` its parent places on a slot through ``slot_usage``."""
    schema["classes"]["Collection"]["slot_usage"] = {"tags": _REVIEWED}
    schema["classes"]["SpecialCollection"] = {"is_a": "Collection"}
    instance = {} if values is None else {"tags": values}
    assert generator_agreement.verdicts(schema, instance, target) == (valid, valid)


def test_has_member_on_a_single_valued_slot_is_ignored_with_a_warning(
    schema: dict[str, Any], caplog: pytest.LogCaptureFixture
) -> None:
    """A member is a value of a multivalued slot, so both generators ignore ``has_member`` on a
    single-valued slot and say so."""
    schema["slots"]["tags"] = {"range": "string", "has_member": {"equals_string": "reviewed"}}
    with caplog.at_level(logging.WARNING):
        assert verdicts(schema, {"tags": "pending"}) == (True, True)
    assert sorted({r.getMessage() for r in caplog.records if r.name.startswith("linkml.generators.")}) == [
        "Slot 'tags': has_member is not translated to JSON Schema, because the slot is not multivalued.",
        "Slot 'tags': has_member is not translated to SHACL, because it uses has_member on slot 'tags', "
        "which is not multivalued (in the shapes of 'Collection').",
    ]


@pytest.mark.parametrize("typed,valid", [(True, True), (False, False)])
def test_member_range_needs_the_class(schema: dict[str, Any], typed: bool, valid: bool) -> None:
    """A member with a class ``range`` must be an instance of that class."""
    schema["classes"]["Special"] = {"is_a": "Item", "slot_usage": {"status": {"required": True}}}
    schema["slots"]["items"]["has_member"] = {"range": "Special"}
    special = "ex:Special, " if typed else ""
    assert conforms(schema, f'ex:c a ex:Collection; ex:items [a {special}ex:Item; ex:status "ready"] .') is valid
    assert json_valid(schema, {"items": [{"status": "ready"}]})
    assert not json_valid(schema, {"items": [{}]})


@pytest.mark.parametrize("dict_inlined", [False, True])
def test_null_has_no_member(schema: dict[str, Any], dict_inlined: bool) -> None:
    """A JSON ``null`` is no value, so it has no member, although the generator otherwise allows ``null``."""
    if dict_inlined:
        schema["classes"]["Item"]["slots"].insert(0, "id")
        schema["slots"]["id"] = {"identifier": True, "range": "string"}
        del schema["slots"]["items"]["inlined_as_list"]
        schema["slots"]["items"]["inlined"] = True
    schema["slots"]["items"]["has_member"] = {}
    assert not json_valid(schema, {"items": None})
    del schema["slots"]["items"]["has_member"]
    assert json_valid(schema, {"items": None})


@pytest.mark.parametrize("grade,valid", [(3, True), (1, False)])
def test_member_range_resolves_its_range_expression(schema: dict[str, Any], grade: int, valid: bool) -> None:
    """The ``range_expression`` of a member with a ``range`` constrains the slots of that range class."""
    schema["classes"]["Special"] = {"is_a": "Item", "attributes": {"grade": {"range": "integer"}}}
    expression = {"slot_conditions": {"grade": {"minimum_value": 2}}}
    schema["slots"]["items"]["has_member"] = {"range": "Special", "range_expression": expression}
    assert conforms(schema, f"ex:c a ex:Collection; ex:items [a ex:Item, ex:Special; ex:grade {grade}] .") is valid


@pytest.mark.parametrize(
    "slot_change,member,reason",
    [
        pytest.param(
            {"multivalued": False},
            {"equals_string": "reviewed"},
            "has_member on slot 'tags', which is not multivalued",
            id="single-valued",
        ),
        pytest.param(
            {},
            {"minimum_cardinality": 1},
            "'minimum_cardinality' in the has_member of slot 'tags'",
            id="cardinality-of-a-value",
        ),
        pytest.param(
            {},
            {"any_of": [{"equals_string": "reviewed"}]},
            "'any_of' in the has_member of slot 'tags'",
            id="slot-operator",
        ),
        pytest.param(
            {"range": "integer"},
            {"equals_string": "5"},
            "equals_string in the has_member of slot 'tags', whose range 'integer' does not hold strings",
            id="string-on-integer",
        ),
    ],
)
def test_untranslatable_has_member_skipped_with_warning(
    schema: dict[str, Any],
    caplog: pytest.LogCaptureFixture,
    slot_change: dict[str, Any],
    member: dict[str, Any],
    reason: str,
) -> None:
    """A ``has_member`` SHACL cannot express is left out of the shapes, with one warning."""
    schema["slots"]["tags"].update(slot_change, has_member=member)
    with caplog.at_level(logging.WARNING, logger="linkml.generators.shaclgen"):
        assert conforms(schema, "ex:c a ex:Collection .")
    assert [r.getMessage() for r in caplog.records] == [
        f"Slot 'tags': has_member is not translated to SHACL, because it uses {reason} (in the shapes of 'Collection')."
    ]


def test_untranslatable_has_member_in_class_expression_skips_it(
    schema: dict[str, Any], caplog: pytest.LogCaptureFixture
) -> None:
    """A class-level expression whose ``has_member`` cannot be translated is skipped as a whole."""
    member = {"any_of": [{"equals_string": "reviewed"}]}
    schema["classes"]["Collection"]["all_of"] = [{"slot_conditions": {"tags": {"has_member": member}}}]
    with caplog.at_level(logging.WARNING, logger="linkml.generators.shaclgen"):
        assert conforms(schema, "ex:c a ex:Collection .")
    assert [r.getMessage() for r in caplog.records] == [
        "Class 'Collection': all_of is not translated to SHACL, because it uses "
        "'any_of' in the has_member of slot 'tags'."
    ]
