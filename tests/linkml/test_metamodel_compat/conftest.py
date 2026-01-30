"""Pytest fixtures for metamodel compatibility tests."""

import pytest


@pytest.fixture
def metamodel_path(input_path) -> str:
    """Return the path to the local copy of the LinkML metamodel."""
    return str(input_path("metamodel/meta.yaml"))
