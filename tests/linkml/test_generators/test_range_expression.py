"""A slot's ``range_expression`` constrains each of its values alike in the JSON Schema and SHACL generators.

Each value must satisfy the expression as an instance of its range class
satisfies a class-level expression: its conditions constrain the slots of the
value as induced for that class, and an expression is violated only when it is
definitely false.  The agreement tests validate the same instance with both
generated artifacts, loading it as RDF through the generated JSON-LD context.
"""

import json
import logging
from pathlib import Path
from typing import Any

import pytest
import yaml
from click.testing import CliRunner
from jsonschema import Draft201909Validator
from pyshacl import validate
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import SH

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.shaclgen import ShaclGenerator, cli
from tests.linkml.utils import generator_agreement

EX = Namespace("https://example.org/context/")
PREFIX = f"@prefix ex: <{EX}> . "


@pytest.fixture
def schema() -> dict[str, Any]:
    """A resource is constrained differently when used as a document's license."""
    return yaml.safe_load("""
id: https://example.org/context
name: context
prefixes:
  ex: https://example.org/context/
  linkml: https://w3id.org/linkml/
default_prefix: ex
imports: [linkml:types]
classes:
  Document:
    tree_root: true
    slots: [license]
    slot_usage:
      license:
        range_expression:
          slot_conditions:
            category: {equals_string: license, required: true}
  Resource:
    slots: [category, code, tags, details]
  Details:
    slots: [code]
slots:
  license: {range: Resource, inlined: true}
  category: {range: string}
  code: {range: integer}
  tags: {range: string, multivalued: true}
  details: {range: Details, inlined: true}
enums:
  Category:
    permissible_values:
      license: {}
""")


def verdicts(schema: dict[str, Any], instance: dict[str, Any], target: str = "Document") -> tuple[bool, bool]:
    """Whether the JSON Schema and the SHACL shapes generated for *schema* accept *instance* of *target*."""
    return generator_agreement.verdicts(schema, instance, target)


def conforms(schema: dict[str, Any], data: str, **options: Any) -> bool:
    """Whether Turtle *data* conforms to the SHACL shapes generated for *schema*, which must pass meta-SHACL."""
    shapes = ShaclGenerator(yaml.safe_dump(schema), closed=False, **options).serialize()
    return validate(
        data_graph=PREFIX + data,
        data_graph_format="turtle",
        shacl_graph=shapes,
        shacl_graph_format="turtle",
        meta_shacl=True,
    )[0]


def _equals(slot: str, value: str | int) -> dict[str, Any]:
    """A class expression requiring *slot* to equal *value*, unknown when *slot* is absent."""
    key = "equals_number" if isinstance(value, int) else "equals_string"
    return {"slot_conditions": {slot: {key: value}}}


_REQUIRED_LICENSE = {"slot_conditions": {"category": {"equals_string": "license", "required": True}}}
_LICENSE_OR_CODE = [_equals("category", "license"), _equals("code", 5)]
_NO_TAGS_AND_LICENSE = {
    "slot_conditions": {"tags": {"maximum_cardinality": 0}},
    "all_of": [_equals("category", "license")],
}
_TWO_TAGS = {"slot_conditions": {"tags": {"minimum_cardinality": 2}}}
_CATEGORY_RANGE = {"slot_conditions": {"category": {"range": "Category"}}}
_CODE_FROM_TWO = {"slot_conditions": {"code": {"minimum_value": 2}}}
_REQUIRED_DETAILS = {"slot_conditions": {"details": {"required": True, "range_expression": _CODE_FROM_TWO}}}
_NO_DETAILS_CODE = {"none_of": [{"slot_conditions": {"details": {"range_expression": _CODE_FROM_TWO}}}]}


@pytest.mark.parametrize(
    "expression,value,valid",
    [
        pytest.param(_REQUIRED_LICENSE, {"category": "license"}, True, id="required-match"),
        pytest.param(_REQUIRED_LICENSE, {"category": "other"}, False, id="required-other"),
        pytest.param(_REQUIRED_LICENSE, {}, False, id="required-absent"),
        # a condition that doesn't state presence is unknown for an absent slot
        pytest.param(_equals("category", "license"), {}, True, id="optional-absent"),
        pytest.param(_equals("category", "license"), {"category": "other"}, False, id="optional-other"),
        pytest.param({"none_of": [_equals("category", "license")]}, {}, True, id="none_of-absent"),
        pytest.param({"none_of": [_equals("category", "license")]}, {"category": "license"}, False, id="none_of-match"),
        pytest.param({"none_of": [_equals("category", "license")]}, {"category": "other"}, True, id="none_of-other"),
        pytest.param({"any_of": _LICENSE_OR_CODE}, {}, True, id="any_of-absent"),
        pytest.param({"any_of": _LICENSE_OR_CODE}, {"category": "other"}, True, id="any_of-false-or-unknown"),
        pytest.param({"any_of": _LICENSE_OR_CODE}, {"category": "other", "code": 1}, False, id="any_of-false"),
        # exactly_one_of counts the members that are definitely true
        pytest.param({"exactly_one_of": _LICENSE_OR_CODE}, {}, False, id="exactly_one_of-absent"),
        pytest.param({"exactly_one_of": _LICENSE_OR_CODE}, {"category": "license"}, True, id="exactly_one_of-first"),
        pytest.param({"exactly_one_of": _LICENSE_OR_CODE}, {"code": 5}, True, id="exactly_one_of-second"),
        pytest.param(
            {"exactly_one_of": _LICENSE_OR_CODE}, {"category": "license", "code": 5}, False, id="exactly_one_of-both"
        ),
        pytest.param({"exactly_one_of": _LICENSE_OR_CODE}, {"category": "other"}, False, id="exactly_one_of-none"),
        pytest.param(_NO_TAGS_AND_LICENSE, {"tags": ["a"]}, False, id="absent-and-all_of-tags"),
        pytest.param(_NO_TAGS_AND_LICENSE, {"category": "other"}, False, id="absent-and-all_of-other"),
        pytest.param(_NO_TAGS_AND_LICENSE, {"category": "license"}, True, id="absent-and-all_of-match"),
        pytest.param(_TWO_TAGS, {}, False, id="cardinality-absent"),
        pytest.param(_TWO_TAGS, {"tags": ["a"]}, False, id="cardinality-too-few"),
        pytest.param(_TWO_TAGS, {"tags": ["a", "b"]}, True, id="cardinality-enough"),
        pytest.param(_CATEGORY_RANGE, {"category": "license"}, True, id="condition-range"),
        pytest.param(_CATEGORY_RANGE, {"category": "other"}, False, id="condition-range-other"),
        # a nested expression constrains the slots of the value's value, as induced for its range class
        pytest.param(_REQUIRED_DETAILS, {"details": {"code": 2}}, True, id="nested"),
        pytest.param(_REQUIRED_DETAILS, {"details": {"code": 1}}, False, id="nested-other"),
        pytest.param(_REQUIRED_DETAILS, {"details": {}}, True, id="nested-absent"),
        pytest.param(_REQUIRED_DETAILS, {}, False, id="nested-required"),
        # under a negation, a nested expression takes its "definitely true" form
        pytest.param(_NO_DETAILS_CODE, {"details": {}}, True, id="nested-in-none_of-absent"),
        pytest.param(_NO_DETAILS_CODE, {"details": {"code": 3}}, False, id="nested-in-none_of-match"),
        pytest.param(_NO_DETAILS_CODE, {"details": {"code": 1}}, True, id="nested-in-none_of-other"),
    ],
)
@pytest.mark.parametrize("multivalued", [False, True])
def test_range_expression_constrains_each_value(
    schema: dict[str, Any], expression: dict[str, Any], value: dict[str, Any], valid: bool, multivalued: bool
) -> None:
    """Both generators read a range expression alike, on a single value and on a list of values."""
    schema["classes"]["Document"]["slot_usage"]["license"]["range_expression"] = expression
    schema["slots"]["license"]["multivalued"] = multivalued
    assert verdicts(schema, {"license": [value] if multivalued else value}) == (valid, valid)


@pytest.mark.parametrize(
    "values,valid",
    [
        ([{"category": "license"}, {"category": "license"}], True),
        ([{"category": "license"}, {"category": "other"}], False),
        ([{"category": "license"}, {}], False),
    ],
)
def test_range_expression_holds_for_every_value(schema: dict[str, Any], values: list[dict], valid: bool) -> None:
    """Every value of a multivalued slot must satisfy the expression."""
    schema["slots"]["license"]["multivalued"] = True
    assert verdicts(schema, {"license": values}) == (valid, valid)


@pytest.mark.parametrize(
    "operator,value,valid",
    [
        ("all_of", {}, True),
        ("all_of", {"category": "license"}, True),
        ("all_of", {"category": "other"}, False),
        ("none_of", {}, True),
        ("none_of", {"category": "license"}, False),
        ("none_of", {"category": "other"}, True),
    ],
)
def test_range_expression_in_class_expression(
    schema: dict[str, Any], operator: str, value: dict[str, Any], valid: bool
) -> None:
    """In a condition of a class-level expression, a range expression takes the form of the condition."""
    del schema["classes"]["Document"]["slot_usage"]
    schema["classes"]["Document"][operator] = [
        {"slot_conditions": {"license": {"range_expression": _equals("category", "license")}}}
    ]
    assert verdicts(schema, {"license": value}) == (valid, valid)


@pytest.mark.parametrize("value,valid", [({"category": "license"}, True), ({"category": "other"}, False)])
def test_range_expression_on_union_branch(schema: dict[str, Any], value: dict[str, Any], valid: bool) -> None:
    """A class alternative of a slot's ``any_of`` carries its own range expression."""
    expression = schema["classes"]["Document"].pop("slot_usage")["license"]["range_expression"]
    schema["classes"]["Note"] = {"slots": ["text"]}
    schema["slots"]["text"] = {"range": "string", "required": True}
    schema["slots"]["license"] = {
        "inlined": True,
        "any_of": [{"range": "Resource", "range_expression": expression}, {"range": "Note"}],
    }
    # the RDF type of a value of a union is the alternative it is an instance of
    assert verdicts(schema, {"license": {"@type": "Resource", **value}}) == (valid, valid)
    assert verdicts(schema, {"license": {"@type": "Note", "text": "explanation"}}) == (True, True)


def test_union_branch_keeps_its_class(schema: dict[str, Any]) -> None:
    """Satisfying the expression of a class alternative doesn't make a value an instance of that class."""
    expression = schema["classes"]["Document"].pop("slot_usage")["license"]["range_expression"]
    schema["slots"]["license"] = {"inlined": True, "any_of": [{"range": "Resource", "range_expression": expression}]}
    assert conforms(schema, 'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "license"] .')
    assert not conforms(schema, 'ex:doc a ex:Document; ex:license [a ex:Details; ex:category "license"] .')


@pytest.mark.parametrize(
    "value,valid", [({"category": "mit"}, True), ({"category": "eula"}, True), ({"category": "gpl"}, False)]
)
def test_range_expression_combining_enums(schema: dict[str, Any], value: dict[str, Any], valid: bool) -> None:
    """A range expression on values that aren't class instances can combine enums."""
    del schema["classes"]["Document"]["slot_usage"]
    schema["enums"] = {
        "Open": {"permissible_values": {"mit": {}, "bsd": {}}},
        "Proprietary": {"permissible_values": {"eula": {}}},
    }
    schema["slots"]["category"]["range_expression"] = {"any_of": [{"is_a": "Open"}, {"is_a": "Proprietary"}]}
    assert verdicts(schema, {"license": value}) == (valid, valid)


@pytest.mark.parametrize("in_class_expression", [False, True])
@pytest.mark.parametrize("value,valid", [({"category": ["license"]}, True), ({"category": ["license", "x"]}, False)])
def test_range_expression_uses_the_slots_of_the_range_class(
    schema: dict[str, Any], value: dict[str, Any], valid: bool, in_class_expression: bool
) -> None:
    """A condition constrains the slot as induced for the range class, whose ``slot_usage`` applies."""
    schema["classes"]["SpecialResource"] = {"is_a": "Resource", "slot_usage": {"category": {"multivalued": True}}}
    schema["slots"]["license"]["range"] = "SpecialResource"
    if in_class_expression:
        del schema["classes"]["Document"]["slot_usage"]
        condition = {"range_expression": _equals("category", "license")}
        schema["classes"]["Document"]["all_of"] = [{"slot_conditions": {"license": condition}}]
    else:
        schema["classes"]["Document"]["slot_usage"]["license"]["range_expression"] = _equals("category", "license")
    assert verdicts(schema, {"license": value}) == (valid, valid)


@pytest.mark.parametrize("target", ["Document", "SpecialDocument"])
@pytest.mark.parametrize("value,valid", [({"category": "license"}, True), ({"category": "other"}, False)])
def test_range_expression_is_inherited(schema: dict[str, Any], target: str, value: dict[str, Any], valid: bool) -> None:
    """A subclass keeps the range expression its parent places on a slot."""
    schema["classes"]["SpecialDocument"] = {"is_a": "Document"}
    assert verdicts(schema, {"license": value}, target=target) == (valid, valid)


@pytest.mark.parametrize("category,valid", [("license", True), ("other", False)])
def test_range_expression_on_values_inlined_as_dict(schema: dict[str, Any], category: str, valid: bool) -> None:
    """The values of a slot inlined as a dict are the values of the dict, not the dict itself."""
    schema["classes"]["Resource"]["slots"].insert(0, "id")
    schema["slots"]["id"] = {"identifier": True, "range": "string"}
    schema["slots"]["license"]["multivalued"] = True
    json_schema = json.loads(JsonSchemaGenerator(yaml.safe_dump(schema), top_class="Document").serialize())
    instance = {"license": {"r1": {"category": "license"}, "r2": {"category": category}}}
    assert Draft201909Validator(json_schema).is_valid(instance) is valid
    data = 'ex:doc a ex:Document; ex:license ex:r1, ex:r2 . ex:r1 a ex:Resource; ex:category "license" . '
    assert conforms(schema, data + f'ex:r2 a ex:Resource; ex:category "{category}" .') is valid


@pytest.mark.parametrize("category,valid", [("license", True), ("other", False)])
def test_range_expression_in_condition_on_values_inlined_as_dict(
    schema: dict[str, Any], category: str, valid: bool
) -> None:
    """In a condition of a class-level expression, a range expression constrains the values of a dict."""
    del schema["classes"]["Document"]["slot_usage"]
    schema["classes"]["Resource"]["slots"].insert(0, "id")
    schema["slots"]["id"] = {"identifier": True, "range": "string"}
    schema["slots"]["license"]["multivalued"] = True
    condition = {"range_expression": _equals("category", "license")}
    schema["classes"]["Document"]["all_of"] = [{"slot_conditions": {"license": condition}}]
    json_schema = json.loads(JsonSchemaGenerator(yaml.safe_dump(schema), top_class="Document").serialize())
    assert Draft201909Validator(json_schema).is_valid({"license": {"r1": {"category": category}}}) is valid


_COMPACT_DICT_SCHEMA = """
id: https://example.org/compact
name: compact
prefixes: {ex: https://example.org/compact/, linkml: https://w3id.org/linkml/}
default_prefix: ex
imports: [linkml:types]
classes:
  Resource:
    attributes:
      id: {identifier: true}
      category: {range: string}
  Document:
    attributes:
      license:
        range: Resource
        multivalued: true
        inlined: true
        range_expression:
          slot_conditions:
            category: {equals_string: license, required: true}
"""


@pytest.mark.xfail(strict=True, reason="JSON Schema can't apply a range expression to the compact forms of a dict")
@pytest.mark.parametrize("value", ["other", None], ids=["simple-dict", "null"])
def test_range_expression_on_compact_dict_forms(value: str | None) -> None:
    """The compact forms ``{id: value}`` and ``{id: null}`` of a slot inlined as a dict escape the
    expression in JSON Schema, while SHACL rejects the resources they denote."""
    json_schema = json.loads(JsonSchemaGenerator(_COMPACT_DICT_SCHEMA, top_class="Document").serialize())
    assert not Draft201909Validator(json_schema).is_valid({"license": {"r1": value}})


def test_range_expression_follows_the_alias(schema: dict[str, Any]) -> None:
    """A condition names a slot of the value, whose alias is its JSON key and whose IRI is its RDF property."""
    schema["slots"]["category"]["alias"] = "kind"
    validator = Draft201909Validator(
        json.loads(JsonSchemaGenerator(yaml.safe_dump(schema), top_class="Document").serialize())
    )
    assert validator.is_valid({"license": {"kind": "license"}})
    assert not validator.is_valid({"license": {"kind": "other"}})
    assert conforms(schema, 'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "license"] .')
    assert not conforms(schema, 'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "other"] .')


@pytest.mark.parametrize("type_statement,expected", [("a ex:Resource;", True), ("", False), ("a ex:Details;", False)])
def test_range_expression_preserves_class_membership(
    schema: dict[str, Any], type_statement: str, expected: bool
) -> None:
    """Matching content cannot substitute for membership in the declared range."""
    assert conforms(schema, f'ex:doc a ex:Document; ex:license [{type_statement} ex:category "license"] .') is expected


@pytest.mark.parametrize("category,expected", [("license", True), ("other", False)])
@pytest.mark.parametrize("suffix", [None, "Shape"])
@pytest.mark.parametrize("use_class_uri_names", [False, True])
def test_range_expression_independent_of_shape_names(
    schema: dict[str, Any], category: str, expected: bool, suffix: str | None, use_class_uri_names: bool
) -> None:
    """The anonymous shape of a range expression works with either naming mode and a suffix."""
    data = f'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "{category}"] .'
    assert conforms(schema, data, suffix=suffix, use_class_uri_names=use_class_uri_names) is expected


def test_range_expression_does_not_constrain_every_instance_of_the_range(schema: dict[str, Any]) -> None:
    """Only the values of the constrained slot get the extra requirement."""
    assert conforms(
        schema,
        'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "license"] . '
        'ex:other a ex:Resource; ex:category "other" .',
    )


@pytest.mark.parametrize("category,expected", [("license", True), ("other", False)])
def test_range_expression_on_referenced_values(schema: dict[str, Any], category: str, expected: bool) -> None:
    """In RDF, a value that is a reference is constrained by its description in the data graph."""
    schema["classes"]["Resource"]["slots"].append("id")
    schema["slots"]["id"] = {"identifier": True, "range": "uriorcurie"}
    schema["slots"]["license"]["inlined"] = False
    data = f'ex:doc a ex:Document; ex:license ex:resource . ex:resource a ex:Resource; ex:category "{category}" .'
    assert conforms(schema, data) is expected


def test_range_expression_uses_the_condition_range(schema: dict[str, Any]) -> None:
    """A range expression in a condition with a ``range`` resolves its conditions in that range class."""
    schema["classes"]["SpecialResource"] = {"is_a": "Resource", "attributes": {"grade": {"range": "integer"}}}
    del schema["classes"]["Document"]["slot_usage"]
    expression = {"slot_conditions": {"grade": {"minimum_value": 2}}}
    condition = {"range": "SpecialResource", "range_expression": expression}
    schema["classes"]["Document"]["all_of"] = [{"slot_conditions": {"license": condition}}]
    data = "ex:doc a ex:Document; ex:license [a ex:Resource, ex:SpecialResource; ex:grade {}] ."
    assert conforms(schema, data.format(2))
    assert not conforms(schema, data.format(1))


@pytest.mark.parametrize("category,expected", [("license", True), ("other", False)])
def test_cli_enforces_range_expression(schema: dict[str, Any], tmp_path: Path, category: str, expected: bool) -> None:
    """The command line generates the same shapes, without an option."""
    path = tmp_path / "context.yaml"
    path.write_text(yaml.safe_dump(schema))
    result = CliRunner().invoke(cli, [str(path), "--non-closed"])
    assert result.exit_code == 0, result.output
    data = PREFIX + f'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "{category}"] .'
    report = validate(
        data_graph=data, data_graph_format="turtle", shacl_graph=result.output, shacl_graph_format="turtle"
    )
    assert report[0] is expected


@pytest.mark.parametrize("category,expected", [("license", True), ("other", False)])
def test_range_expression_on_imported_slots(
    schema: dict[str, Any], tmp_path: Path, category: str, expected: bool
) -> None:
    """With imported shapes excluded, a condition still resolves the IRI of an imported slot."""
    imported = {
        "id": "https://example.org/imported",
        "name": "imported",
        "default_prefix": "imp",
        "prefixes": {"imp": "https://example.org/imported/"},
        "classes": {"Resource": {"class_uri": "imp:Resource", "slots": ["category"]}},
        "slots": {"category": {"slot_uri": "imp:category", "range": "string"}},
    }
    (tmp_path / "imported.yaml").write_text(yaml.safe_dump(imported))
    del schema["classes"]["Resource"]
    del schema["slots"]["category"]
    schema["imports"].append("imported")
    path = tmp_path / "context.yaml"
    path.write_text(yaml.safe_dump(schema))
    shapes = ShaclGenerator(str(path), closed=False, exclude_imports=True).serialize()
    graph = Graph().parse(data=shapes, format="turtle")
    assert (None, SH.targetClass, URIRef("https://example.org/imported/Resource")) not in graph
    data = (
        f"{PREFIX} @prefix imp: <https://example.org/imported/> . "
        f'ex:doc a ex:Document; ex:license [a imp:Resource; imp:category "{category}"] .'
    )
    report = validate(data_graph=data, data_graph_format="turtle", shacl_graph=graph, meta_shacl=True)
    assert report[0] is expected


@pytest.mark.parametrize(
    "condition,reason",
    [
        ({"unit": {"ucum_code": "m"}}, "'unit' in the condition on slot 'category'"),
        ({"equals_expression": "{code} * 2"}, "'equals_expression' in the condition on slot 'category'"),
    ],
)
def test_untranslatable_range_expression_skipped_with_warning(
    schema: dict[str, Any], caplog: pytest.LogCaptureFixture, condition: dict[str, Any], reason: str
) -> None:
    """A range expression SHACL cannot express is left out of the shapes of each class, with one warning."""
    expression = schema["classes"]["Document"]["slot_usage"]["license"]["range_expression"]
    expression["slot_conditions"]["category"].update(condition)
    schema["classes"]["SpecialDocument"] = {"is_a": "Document"}
    with caplog.at_level(logging.WARNING, logger="linkml.generators.shaclgen"):
        assert conforms(schema, 'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "other"] .')
    assert [r.getMessage() for r in caplog.records] == [
        f"Slot 'license': range_expression is not translated to SHACL, because it uses {reason} "
        "(in the shapes of 'Document', 'SpecialDocument')."
    ]


def test_range_expression_with_conditions_on_values_that_are_not_class_instances(
    schema: dict[str, Any], caplog: pytest.LogCaptureFixture
) -> None:
    """Values of a type or an enum have no slots for a condition to constrain."""
    del schema["classes"]["Document"]["slot_usage"]
    schema["slots"]["category"]["range_expression"] = {"slot_conditions": {"code": {"required": True}}}
    with caplog.at_level(logging.WARNING, logger="linkml.generators.shaclgen"):
        assert verdicts(schema, {"license": {"category": "other"}}) == (True, True)
    assert [r.getMessage() for r in caplog.records] == [
        "Slot 'category': range_expression is not translated to SHACL, because it uses a condition on slot 'code' "
        "of values that are not class instances (in the shapes of 'Resource')."
    ]


def test_untranslatable_range_expression_in_class_expression_skips_it(
    schema: dict[str, Any], caplog: pytest.LogCaptureFixture
) -> None:
    """A class-level expression whose range expression cannot be translated is skipped as a whole."""
    del schema["classes"]["Document"]["slot_usage"]
    expression = {"slot_conditions": {"category": {"equals_string": "license", "unit": {"ucum_code": "m"}}}}
    schema["classes"]["Document"]["all_of"] = [{"slot_conditions": {"license": {"range_expression": expression}}}]
    with caplog.at_level(logging.WARNING, logger="linkml.generators.shaclgen"):
        assert conforms(schema, 'ex:doc a ex:Document; ex:license [a ex:Resource; ex:category "other"] .')
    assert [r.getMessage() for r in caplog.records] == [
        "Class 'Document': all_of is not translated to SHACL, because it uses "
        "'unit' in the condition on slot 'category'."
    ]
