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
    cache and builds a JsonSchema root inlined to the new target class.
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

    # The validator is rooted at Dog: Dog's properties inlined, additionalProperties
    # reflects closed=False, and $defs is preserved for nested $ref resolution.
    assert "properties" in validator.schema
    assert "breed" in validator.schema["properties"]
    assert validator.schema["additionalProperties"] is True
    assert "$defs" in validator.schema
    assert "$schema" in validator.schema


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


# cache-hit path inlines the target class and shares $defs by reference


def test_cache_hit_wrapper_inlines_class_and_shares_defs():
    """When the module-level cache is warm, a second ValidationContext for a different
    target class must inline that class's keywords at the root, share the cached $defs
    dict by reference (no deep copy), and re-apply additionalProperties = not_closed."""
    schema = _two_class_schema()
    cache_key = (id(schema), False, False)
    _json_schema_cache.pop(cache_key, None)

    # Warm the cache (cache-miss path)
    ctx_animal = ValidationContext(schema, "Animal")
    ctx_animal.json_schema_validator(closed=False, include_range_class_descendants=False)
    assert cache_key in _json_schema_cache
    cached_root = _json_schema_cache[cache_key]
    original_defs = cached_root["$defs"]

    # Trigger the cache-hit path for a different target class
    ctx_dog = ValidationContext(schema, "Dog")
    validator = ctx_dog.json_schema_validator(closed=False, include_range_class_descendants=False)

    # $defs shared by reference (no deep copy) — preserves O(1) cache-hit cost
    assert validator.schema["$defs"] is original_defs
    # additionalProperties re-applied from not_closed (closed=False → True)
    assert validator.schema["additionalProperties"] is True
    # Metadata inherited from the cached root (belt-and-braces parity)
    assert validator.schema["$schema"] == cached_root["$schema"]
    assert validator.schema["$id"] == cached_root["$id"]
    # Dog's keywords inlined at root
    assert "properties" in validator.schema
    assert set(validator.schema["properties"]) == {"name", "breed"}


# Regression: cache-hit validator must behave identically to a cold-cache one


@pytest.mark.parametrize("closed", [True, False])
def test_cache_hit_validator_matches_cold_cache(closed):
    """A cache-hit validator must produce the same errors as a cold-cache one
    for the same target_class on every instance. Guards against the
    additionalProperties divergence caused by the old $ref-wrapping approach,
    plus any sibling cases (extra props, missing fields, etc)."""
    schema = _two_class_schema()
    cache_key = (id(schema), closed, False)

    # Cold-cache validator for Dog
    _json_schema_cache.pop(cache_key, None)
    cold = ValidationContext(schema, "Dog").json_schema_validator(
        closed=closed, include_range_class_descendants=False
    )

    # Warm the cache via Animal, then build a hit-path validator for Dog
    _json_schema_cache.pop(cache_key, None)
    ValidationContext(schema, "Animal").json_schema_validator(
        closed=closed, include_range_class_descendants=False
    )
    warm = ValidationContext(schema, "Dog").json_schema_validator(
        closed=closed, include_range_class_descendants=False
    )

    instances = [
        {"name": "Rex", "breed": "Lab"},
        {"name": "Rex", "breed": "Lab", "extra_prop": "hi"},
        {"breed": "Lab"},
        {},
    ]
    for inst in instances:
        cold_msgs = sorted(e.message for e in cold.iter_errors(inst))
        warm_msgs = sorted(e.message for e in warm.iter_errors(inst))
        assert cold_msgs == warm_msgs, (inst, cold_msgs, warm_msgs)
