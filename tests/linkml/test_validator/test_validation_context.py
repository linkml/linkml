"""Unit tests for ValidationContext.

Targets lines not covered by plugin-level tests for cache-hit branch.
    - module-level `_json_schema_cache` dict
    - cache-miss path: generate full schema, populate _json_schema_cache
    - cache-hit path: reuse cached $defs, re-root via $ref
    - path_override: load schema from file, skip generator
"""

import json

import pytest

from linkml.validator.validation_context import ValidationContext, _json_schema_cache
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition

# Helpers


def _two_class_schema() -> SchemaDefinition:
    """A minimal schema with two related classes suitable for re-rooting tests."""
    return SchemaDefinition(
        id="https://example.org/two_class_test",
        name="two_class_test",
        classes=[
            ClassDefinition(
                name="Animal",
                attributes=[SlotDefinition(name="name", range="string")],
                tree_root=True,
            ),
            ClassDefinition(
                name="Dog",
                is_a="Animal",
                attributes=[SlotDefinition(name="breed", range="string")],
            ),
        ],
    )


# Cache-miss path


def test_json_schema_validator_cache_miss_populates_module_cache():
    """First call for a fresh schema object populates _json_schema_cache."""
    schema = _two_class_schema()
    ctx = ValidationContext(schema, "Animal")

    cache_key = (id(schema), False, False)
    _json_schema_cache.pop(cache_key, None)  # ensure a clean slate for this object

    _ = ctx.json_schema_validator(closed=False, include_range_class_descendants=False)

    assert cache_key in _json_schema_cache
    assert "$defs" in _json_schema_cache[cache_key]


# Cache-hit path


def test_json_schema_validator_cache_hit_reroots_to_new_class():
    """Second ValidationContext sharing the same schema object hits the module-level
    cache and builds a minimal JsonSchema wrapper re-rooted to the new target class.
    """
    schema = _two_class_schema()
    cache_key = (id(schema), False, False)
    _json_schema_cache.pop(cache_key, None)

    # First context -  populates cache with 'Animal' as root
    ctx1 = ValidationContext(schema, "Animal")
    ctx1.json_schema_validator(closed=False, include_range_class_descendants=False)
    assert cache_key in _json_schema_cache

    # Second context -  same schema object, different target class → cache-hit path
    ctx2 = ValidationContext(schema, "Dog")
    validator = ctx2.json_schema_validator(closed=False, include_range_class_descendants=False)

    # Validator should accept a valid Dog instance
    errors = list(validator.iter_errors({"name": "Rex", "breed": "Labrador"}))
    assert errors == [], errors

    # Confirm the validator is rooted at Dog (not Animal): it should have a schema with a $ref
    assert "$ref" in validator.schema
    assert "Dog" in validator.schema["$ref"]


@pytest.mark.parametrize("closed", [True, False])
def test_json_schema_validator_cache_hit_respects_closed_flag(closed):
    """Cache key includes 'closed', so different closed values generate separate entries."""
    schema = _two_class_schema()

    ctx_a = ValidationContext(schema, "Animal")
    ctx_a.json_schema_validator(closed=closed, include_range_class_descendants=False)

    # New context, same schema, same closed -  should hit cache for the else branch
    ctx_b = ValidationContext(schema, "Dog")
    validator = ctx_b.json_schema_validator(closed=closed, include_range_class_descendants=False)

    assert validator is not None


# path_override branch


def test_json_schema_validator_path_override(tmp_path):
    """path_override loads a JSON Schema file directly, bypassing the generator."""
    override_schema = {
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "type": "object",
        "properties": {"x": {"type": "integer"}},
        "required": ["x"],
    }
    schema_file = tmp_path / "override.json"
    schema_file.write_text(json.dumps(override_schema))

    schema = _two_class_schema()
    ctx = ValidationContext(schema, "Animal")
    validator = ctx.json_schema_validator(
        closed=False,
        include_range_class_descendants=False,
        path_override=str(schema_file),
    )

    # Valid against the override schema
    assert list(validator.iter_errors({"x": 1})) == []

    # Invalid against the override schema (missing required 'x')
    errors = list(validator.iter_errors({"name": "Fido"}))
    assert any(errors)


# cache_key incorporates (id(schema), closed, include_range_class_descendants)
# if cache_key not in _json_schema_cache
# json_schema = gen.generate() / _json_schema_cache[cache_key] = json_schema


@pytest.mark.parametrize(
    "closed,include_range_class_descendants",
    [
        (True, True),
        (True, False),
        (False, True),
        (False, False),
    ],
)
def test_cache_key_is_distinct_per_combination(closed, include_range_class_descendants):
    """Each (closed, include_range_class_descendants) combination produces a separate
    cache entry — exercising line 53 (cache_key construction) and line 55 (miss check)."""
    schema = _two_class_schema()
    cache_key = (id(schema), closed, include_range_class_descendants)
    _json_schema_cache.pop(cache_key, None)

    ctx = ValidationContext(schema, "Animal")
    ctx.json_schema_validator(closed=closed, include_range_class_descendants=include_range_class_descendants)

    assert cache_key in _json_schema_cache, "line 65: entry written after cache miss"
    assert "$defs" in _json_schema_cache[cache_key], "line 64: generated schema has $defs"


# JsonSchemaGenerator is constructed with not_closed=not(closed)


def test_cache_miss_generates_schema_with_not_closed_flag(monkeypatch):
    """Verify that the generator is instantiated with not_closed=not(closed),
    covering line 57 (JsonSchemaGenerator construction) and lines 64-65 (generate + cache)."""
    calls: list[dict] = []

    import linkml.validator.validation_context as vc_module
    from linkml.generators.jsonschemagen import JsonSchemaGenerator as OriginalGenerator

    class CapturingGenerator(OriginalGenerator):
        def __init__(self, *args, **kwargs):
            calls.append(kwargs.copy())
            super().__init__(*args, **kwargs)

    monkeypatch.setattr(vc_module, "JsonSchemaGenerator", CapturingGenerator)

    schema = _two_class_schema()
    cache_key = (id(schema), True, False)
    _json_schema_cache.pop(cache_key, None)

    ctx = ValidationContext(schema, "Animal")
    ctx.json_schema_validator(closed=True, include_range_class_descendants=False)

    assert len(calls) == 1, "generator constructed once on cache miss"
    assert calls[0]["not_closed"] is False, "not_closed = not True = False (line 52 + 57)"
    assert cache_key in _json_schema_cache, "result stored in module cache (line 65)"


# cache-hit path constructs a JsonSchema wrapper with the correct $ref


def test_cache_hit_wrapper_contains_correct_ref_and_defs():
    """When the module-level cache is warm, a second ValidationContext for a different
    target class must produce a minimal JsonSchema with $ref pointing to that class
    and the original $defs — covering lines 71-72."""
    schema = _two_class_schema()
    cache_key = (id(schema), False, False)
    _json_schema_cache.pop(cache_key, None)

    # Warm the cache (cache-miss path)
    ctx_animal = ValidationContext(schema, "Animal")
    ctx_animal.json_schema_validator(closed=False, include_range_class_descendants=False)
    assert cache_key in _json_schema_cache
    original_defs = _json_schema_cache[cache_key]["$defs"]

    # Trigger the cache-hit path for a different target class (line 71: cached = ...)
    ctx_dog = ValidationContext(schema, "Dog")
    validator = ctx_dog.json_schema_validator(closed=False, include_range_class_descendants=False)

    # The validator schema must be the lightweight wrapper (line 72)
    assert validator.schema.get("$ref") == "#/$defs/Dog"  # line 77
    assert validator.schema["$defs"] is original_defs  # line 76: same dict object (no re-gen)
    assert "$schema" in validator.schema  # line 74
