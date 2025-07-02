"""Tests of the linter's root type checks."""

import pytest
from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import RuleConfig, RuleLevel
from linkml.linter.linter import LinterProblem
from linkml.linter.rules import RootTypeChecks

SCHEMA_HEAD = ["id: http://example.org/test_linkml_type_checks", "types:"]
FAKE_TYPE = ["  char_str:", "    description: A character string"]
BASE_LINE = "    base: str"
URI_LINE = "    uri: xsd:string"


def check_schema(test_schema: str) -> list[LinterProblem]:
    """Check a schema using the RootTypeChecks linter.

    :param test_schema: schema to test, as a string
    :type test_schema: str
    :return: list of linting problems discovered
    :rtype: list[LinterProblem]
    """
    schema_view = SchemaView(test_schema)
    config = RuleConfig(level=RuleLevel.error.text)

    rule = RootTypeChecks(config)
    return list(rule.check(schema_view, fix=False))


def test_linkml_types_valid() -> None:
    """Ensure that the types declared in linkml:types are all valid."""
    test_schema = """id: http://example.org/test_linkml_type_checks
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  linkml:types
"""
    assert check_schema(test_schema) == []


@pytest.mark.parametrize(("lines", "errs"), [([], ["base", "uri"]), ([BASE_LINE], ["uri"]), ([URI_LINE], ["base"])])
def test_root_type_missing_required_attributes(lines: list[str], errs: list[str]) -> None:
    """Ensure that a root type with missing attributes throws errors.

    :param lines: extra lines for the type declaration
    :type lines: list[str]
    :param errs: attributes missing from the type declaration
    :type errs: list[str]
    """
    test_schema = "".join(f"{line}\n" for line in [*SCHEMA_HEAD, *FAKE_TYPE, *lines])
    problems = check_schema(test_schema)
    assert len(problems) == len(errs)
    expected_err_msgs = {f"Root type 'char_str' is missing the required '{attr}' attribute" for attr in errs}
    assert expected_err_msgs == {p.message for p in problems}


def test_child_type_invalid_typeof() -> None:
    """Ensure that types with invalid typeof parents throw errors."""
    BAD_TYPES = ["  child_char_str:", "    typeof: something", "  circular_type:", "    typeof: circular_type"]

    test_schema = "".join(f"{line}\n" for line in [*SCHEMA_HEAD, *FAKE_TYPE, BASE_LINE, URI_LINE, *BAD_TYPES])
    problems = check_schema(test_schema)
    assert len(problems) == 2
    assert {
        "'child_char_str' has invalid typeof parent 'something'",
        "'circular_type' has invalid circular typeof parent 'circular_type'",
    } == {p.message for p in problems}
