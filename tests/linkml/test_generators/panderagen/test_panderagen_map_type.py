"""Error handling for ``PanderaDataframeGenerator.map_type`` (issue #3594).

A type whose ``uri`` is outside the generator's ``TYPE_MAP`` and that has no
``typeof`` used to recurse into ``map_type(None)`` and crash deep in the
generator with ``AttributeError: 'NoneType' object has no attribute 'uri'``,
giving no hint which type was at fault. It should instead fail fast with a
clear, actionable error that names the offending type.
"""

import pytest

pytest.importorskip("polars", reason="Polars not installed")
pytest.importorskip("numpy", reason="NumPy not installed")
pytest.importorskip("pandera", reason="Pandera not installed")

from linkml.generators.panderagen import PanderaDataframeGenerator  # noqa: E402

SCHEMA_HEADER = """\
id: https://example.org/repro
name: repro
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/repro/
  xsd: http://www.w3.org/2001/XMLSchema#
default_prefix: ex
default_range: string
imports:
  - linkml:types
"""


def _schema(types_block: str, slot_range: str) -> str:
    """Build a one-class schema whose single slot ``n`` has range ``slot_range``."""
    return (
        f"{SCHEMA_HEADER}types:\n{types_block}"
        f"classes:\n  Holder:\n    attributes:\n      n:\n        range: {slot_range}\n"
    )


@pytest.mark.panderagen
@pytest.mark.parametrize(
    ("type_name", "type_uri"),
    [
        ("PositiveCount", "xsd:positiveInteger"),
        ("NonNegativeCount", "xsd:nonNegativeInteger"),
    ],
)
def test_map_type_unmapped_uri_without_typeof_raises_value_error(type_name: str, type_uri: str) -> None:
    """An unmapped ``uri`` with no ``typeof`` raises a ValueError naming the type."""
    types_block = f"  {type_name}:\n    uri: {type_uri}\n    base: int\n"
    gen = PanderaDataframeGenerator(_schema(types_block, type_name))

    with pytest.raises(ValueError, match=type_name):
        gen.serialize()


@pytest.mark.panderagen
def test_map_type_follows_typeof_chain_for_custom_type() -> None:
    """A custom type chaining via ``typeof`` to a mapped base still resolves."""
    types_block = "  PositiveCount:\n    typeof: integer\n    minimum_value: 1\n"
    gen = PanderaDataframeGenerator(_schema(types_block, "PositiveCount"))

    assert "n: Optional[int]" in gen.serialize()
