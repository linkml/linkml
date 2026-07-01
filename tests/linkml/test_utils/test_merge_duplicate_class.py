"""Tests for tolerating structurally-identical re-declarations during schema merging.

When two sibling imports redeclare the same class, slot, type, enum, or subset
identically (modulo provenance fields such as ``from_schema``), ``merge_schemas``
should treat them as a single element rather than raising a conflict.

See: pre-existing user report — ``gen-project`` failed with
``ValueError: Conflicting URIs ...`` when two sibling modules redeclared a
shared ``Base`` class.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from linkml.generators.pythongen import PythonGenerator
from linkml.utils.schemaloader import SchemaLoader
from linkml_runtime.utils.schemaview import SchemaView

MODULE_A = """\
id: https://example.org/a
name: a
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Base:
    attributes:
      id:
        identifier: true
  ItemA:
    is_a: Base
"""

MODULE_B = """\
id: https://example.org/b
name: b
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Base:
    attributes:
      id:
        identifier: true
  ItemB:
    is_a: Base
"""

MODULE_B_CONFLICTING = """\
id: https://example.org/b
name: b
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
classes:
  Base:
    description: A structurally different Base
    attributes:
      id:
        identifier: true
      extra:
        range: string
  ItemB:
    is_a: Base
"""

MAIN = """\
id: https://example.org/main
name: main
prefixes:
  linkml: https://w3id.org/linkml/
imports:
  - linkml:types
  - ./modules/a
  - ./modules/b
"""


@pytest.fixture
def multi_module_workspace(tmp_path: Path):
    """Create a workspace with main + two sibling modules that redeclare ``Base`` identically."""
    modules = tmp_path / "modules"
    modules.mkdir()
    (modules / "a.yaml").write_text(MODULE_A)
    (modules / "b.yaml").write_text(MODULE_B)
    main = tmp_path / "main.yaml"
    main.write_text(MAIN)
    return main


@pytest.fixture
def conflicting_module_workspace(tmp_path: Path):
    """Create a workspace where two sibling modules redeclare ``Base`` *differently*."""
    modules = tmp_path / "modules"
    modules.mkdir()
    (modules / "a.yaml").write_text(MODULE_A)
    (modules / "b.yaml").write_text(MODULE_B_CONFLICTING)
    main = tmp_path / "main.yaml"
    main.write_text(MAIN)
    return main


def test_schemaloader_merges_identical_redeclared_classes(multi_module_workspace: Path) -> None:
    """SchemaLoader.resolve should not raise when sibling imports redeclare ``Base`` identically."""
    loader = SchemaLoader(str(multi_module_workspace))
    resolved = loader.resolve()

    assert "Base" in resolved.classes
    assert "ItemA" in resolved.classes
    assert "ItemB" in resolved.classes
    # Only the first-encountered provenance is retained, but ItemA/ItemB still see Base
    assert resolved.classes["ItemA"].is_a == "Base"
    assert resolved.classes["ItemB"].is_a == "Base"


def test_schemaloader_still_raises_on_structurally_different_redeclaration(
    conflicting_module_workspace: Path,
) -> None:
    """When sibling imports redeclare ``Base`` with different structure, the conflict must still be raised."""
    loader = SchemaLoader(str(conflicting_module_workspace))
    with pytest.raises(ValueError, match=r"Conflicting URIs .* for item: Base"):
        loader.resolve()


def test_pythongen_round_trips_multi_module_schema(multi_module_workspace: Path) -> None:
    """PythonGenerator should produce valid Python from the merged multi-module schema."""
    code = PythonGenerator(str(multi_module_workspace)).serialize()
    # A single Base class definition should appear in the merged output
    assert code.count("class Base(YAMLRoot):") == 1
    assert "class ItemA(Base):" in code
    assert "class ItemB(Base):" in code


def test_schemaview_sees_single_base(multi_module_workspace: Path) -> None:
    """SchemaView should expose a single ``Base`` class derived from the merged imports."""
    view = SchemaView(str(multi_module_workspace))
    all_classes = view.all_classes()
    assert "Base" in all_classes
    assert "ItemA" in all_classes
    assert "ItemB" in all_classes
