"""Tests for documentation content that answers frequently asked questions."""

from pathlib import Path

import pytest

FAQ_TOOLS_PATH = Path(__file__).resolve().parents[2] / "docs" / "faq" / "tools.md"


@pytest.mark.parametrize(
    "expected_text",
    [
        "## Can I change the default doc style/content for my LinkML schema project?",
        "customize both the style and the wording",
        'prefers "Field" or "Variable" instead of "Slot"',
        "slot.md.jinja2",
        "gen-doc --template-directory templates -d docs my_schema.yaml",
        'MIxS renames "slots" to "terms"',
    ],
)
def test_faq_documents_custom_docgen_templates(expected_text: str) -> None:
    """The tools FAQ explains how to customize generated documentation templates."""
    faq = FAQ_TOOLS_PATH.read_text(encoding="utf-8")
    assert expected_text in faq
