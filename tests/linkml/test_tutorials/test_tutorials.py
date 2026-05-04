"""Pytest wrapper for tutorial markdown execution tests.

Parses and executes the embedded CLI commands in the tutorial files
(docs/intro/tutorial01.md through tutorial09.md), comparing actual
outputs against expected outputs embedded in the markdown.
"""

from pathlib import Path

import pytest

from linkml.utils.execute_tutorial import execute_blocks, parse_file_to_blocks

TUTORIAL_DIR = Path(__file__).resolve().parents[3] / "docs" / "intro"


@pytest.mark.slow
@pytest.mark.tutorial
@pytest.mark.parametrize(
    "tutorial_file",
    [
        pytest.param("tutorial01.md"),
        pytest.param("tutorial02.md"),
        pytest.param("tutorial03.md"),
        pytest.param("tutorial04.md"),
        pytest.param("tutorial05.md"),
        pytest.param("tutorial06.md"),
        pytest.param("tutorial07.md"),
        pytest.param("tutorial08.md"),
        pytest.param("tutorial09.md"),
    ],
    ids=lambda p: p.removesuffix(".md"),
)
def test_tutorial(tutorial_file: str, tmp_path: Path) -> None:
    """Execute a tutorial markdown file and verify all outputs match."""
    md_path = TUTORIAL_DIR / tutorial_file
    assert md_path.exists(), f"Tutorial file not found: {md_path}"

    blocks = parse_file_to_blocks(str(md_path))
    errors = execute_blocks(str(tmp_path), blocks)

    assert not errors, f"Tutorial {tutorial_file} had {len(errors)} error(s):\n" + "\n".join(errors)
