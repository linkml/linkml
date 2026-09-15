"""Runner for the prototype LinkML conformance suite.

The suite is described by a YAML manifest that declares each test as a schema, an
action to run against it, and an assertion about the action's output. The manifest
is loaded into classes generated from the conformance model, so the suite itself
stays independent of any one LinkML implementation.

Every manifest entry becomes its own test case, named after the entry.

The generated classes are checked in. To regenerate them after changing the model:

    uv run gen-python tests/linkml/test_conformance/input/model.yaml \
        > tests/linkml/test_conformance/generated.py
"""

import json
from pathlib import Path

import pytest
import yaml
from jsonpointer import resolve_pointer
from jsonschema.validators import Draft202012Validator, validator_for

from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.linkmlgen import LinkmlGenerator
from linkml_runtime.loaders import yaml_loader
from tests.linkml.test_conformance import generated as conformance

SUITE = "demo-suite"

# Read at import time: parametrization happens before fixtures exist.
MANIFEST: conformance.Manifest = yaml_loader.load(
    str(Path(__file__).parent / "input" / SUITE / "manifest.yaml"), conformance.Manifest
)


def run_action(action: conformance.Action, schema_path: Path) -> str:
    """Run a manifest action against a schema and return its output as a string."""
    if isinstance(action, conformance.JsonSchemaGenerate):
        return JsonSchemaGenerator(str(schema_path)).serialize()
    if isinstance(action, conformance.DeriveAction):
        return LinkmlGenerator(str(schema_path), format="json", materialize_attributes=True).serialize()
    raise NotImplementedError(f"unsupported action: {type(action).__name__}")


def validation_errors(schema_text: str, instance_path: Path) -> list:
    """Validate a JSON instance against a generated JSON Schema, returning every error."""
    schema = json.loads(schema_text)
    validator_cls = validator_for(schema, default=Draft202012Validator)
    validator = validator_cls(schema, format_checker=validator_cls.FORMAT_CHECKER)
    return list(validator.iter_errors(json.loads(instance_path.read_text())))


def check_assertion(assertion: conformance.Assertion, result: str, suite_dir: Path) -> None:
    """Fail if the action's output does not satisfy the assertion."""
    if isinstance(assertion, conformance.JsonPointerAssertion):
        actual = resolve_pointer(yaml.safe_load(result), f"/{assertion.path}")
        assert actual == assertion.value, f"at {assertion.path}: expected {assertion.value!r}, got {actual!r}"

    elif isinstance(assertion, conformance.JsonSchemaAccepts):
        errors = validation_errors(result, suite_dir / assertion.instance)
        assert not errors, "\n".join(f"{assertion.instance} should validate, but: {e.message}" for e in errors)

    elif isinstance(assertion, conformance.JsonSchemaRejects):
        errors = validation_errors(result, suite_dir / assertion.instance)
        assert errors, f"{assertion.instance} should not validate, but it did"

    else:
        raise NotImplementedError(f"unsupported assertion: {type(assertion).__name__}")


@pytest.mark.parametrize("entry", MANIFEST.entries.values(), ids=lambda entry: entry.name)
def test_conformance_entry(entry: conformance.Test, input_path) -> None:
    """Run one conformance manifest entry: perform its action, then check its assertion."""
    suite_dir = Path(input_path(SUITE))
    result = run_action(entry.action, suite_dir / entry.schema)
    check_assertion(entry.assertion, result, suite_dir)
