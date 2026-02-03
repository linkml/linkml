"""Pytest fixtures for metamodel compatibility tests."""

import pytest

# Schemas bundled with linkml-model that schema authors are expected to use
# (via imports or `implements`). These must be loadable and processable by
# the linkml toolkit, just like the core metamodel.
BUNDLED_SCHEMAS = ["arrays", "extended_types"]


@pytest.fixture
def metamodel_path(input_path) -> str:
    """Return the path to the local copy of the LinkML metamodel."""
    return str(input_path("metamodel/meta.yaml"))


@pytest.fixture(params=BUNDLED_SCHEMAS)
def bundled_schema_path(request, input_path) -> str:
    """Return the path to a schema bundled with linkml-model."""
    return str(input_path(f"metamodel/{request.param}.yaml"))
