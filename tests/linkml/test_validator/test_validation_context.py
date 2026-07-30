"""Unit tests for ValidationContext.

Targets lines not covered by plugin-level tests for cache-hit branch.
    - module-level `_json_schema_cache` OrderedDict
    - cache-miss path: generate full schema, populate _json_schema_cache
    - cache-hit path: reuse cached $defs, inline target class at root
    - path_override: load schema from file, skip generator
    - bounded LRU eviction
"""

import json

import pytest

from linkml.validator.validation_context import (
    _JSON_SCHEMA_CACHE_MAXSIZE,
    ValidationContext,
    _json_schema_cache,
    _make_cache_key,
    _schema_pins,
)
from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition, SlotDefinition
from linkml_runtime.linkml_model.meta import AnonymousClassExpression, ClassRule, PresenceEnum


@pytest.fixture(autouse=True)
def _isolate_json_schema_cache():
    """Clear the module-level cache around every test so state doesn't leak
    between cases. Tests that need a populated cache should warm it themselves."""
    _json_schema_cache.clear()
    _schema_pins.clear()
    yield
    _json_schema_cache.clear()
    _schema_pins.clear()


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

    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    _ = ctx.json_schema_validator(closed=False, include_range_class_descendants=False)

    assert cache_key in _json_schema_cache
    assert "$defs" in _json_schema_cache[cache_key]


# Cache-hit path


def test_json_schema_validator_cache_hit_reroots_to_new_class():
    """Second ValidationContext sharing the same schema object hits the module-level
    cache and builds a JsonSchema root inlined to the new target class.
    """
    schema = _two_class_schema()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    # First context -  populates cache with 'Animal' as root
    ctx1 = ValidationContext(schema, "Animal")
    ctx1.json_schema_validator(closed=False, include_range_class_descendants=False)
    assert cache_key in _json_schema_cache

    # Second context -  same schema object, different target class -> cache-hit path
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


# cache_key is (schema.id, schema.name, schema.version, include_range_class_descendants)
# `closed` is intentionally NOT in the key — see comment on _make_cache_key.


@pytest.mark.parametrize("include_range_class_descendants", [True, False])
def test_cache_key_distinct_per_range_descendants(include_range_class_descendants):
    """Different include_range_class_descendants values produce separate entries
    (because they affect $defs contents)."""
    schema = _two_class_schema()
    cache_key = _make_cache_key(schema, include_range_class_descendants=include_range_class_descendants)

    ctx = ValidationContext(schema, "Animal")
    ctx.json_schema_validator(closed=False, include_range_class_descendants=include_range_class_descendants)

    assert cache_key in _json_schema_cache, "entry written after cache miss"
    assert "$defs" in _json_schema_cache[cache_key], "generated schema has $defs"


def test_closed_flag_shares_cache_entry():
    """closed=True and closed=False share a cache entry because the not_closed flag
    only affects the root's additionalProperties (which is re-applied per-call on
    cache hit). This is a meaningful efficiency win for callers that flip the flag."""
    schema = _two_class_schema()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    # First call with closed=False (cache miss)
    v_open = ValidationContext(schema, "Animal").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )
    assert cache_key in _json_schema_cache
    assert len(_json_schema_cache) == 1
    cached_after_first = _json_schema_cache[cache_key]

    # Second call with closed=True (must hit cache, no second entry)
    v_closed = ValidationContext(schema, "Animal").json_schema_validator(
        closed=True, include_range_class_descendants=False
    )
    assert len(_json_schema_cache) == 1, "closed flag must not introduce a new cache entry"
    assert _json_schema_cache[cache_key] is cached_after_first

    # But the validators DO differ: additionalProperties is re-applied per-call.
    assert v_open.schema["additionalProperties"] is True
    assert v_closed.schema["additionalProperties"] is False


# Behavioural check: not_closed = not closed reaches root.additionalProperties


@pytest.mark.parametrize(
    "closed,extras_accepted",
    [(True, False), (False, True)],
)
def test_closed_flag_governs_root_additional_properties(closed, extras_accepted):
    """closed=True rejects extra root-level properties; closed=False accepts them.
    Exercises the full pipeline (generator -> cache -> validator) end-to-end without
    introspecting kwargs or call counts."""
    schema = _two_class_schema()
    validator = ValidationContext(schema, "Animal").json_schema_validator(
        closed=closed, include_range_class_descendants=False
    )
    errors = list(validator.iter_errors({"name": "Rex", "extra_prop": "hi"}))
    if extras_accepted:
        assert errors == [], errors
    else:
        assert errors != []
        assert any("extra_prop" in e.message for e in errors)


# cache-hit path inlines the target class and shares $defs by reference


def test_cache_hit_wrapper_inlines_class_and_shares_defs():
    """When the module-level cache is warm, a second ValidationContext for a different
    target class must inline that class's keywords at the root, share the cached $defs
    dict by reference (no deep copy), and re-apply additionalProperties = not_closed."""
    schema = _two_class_schema()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

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
    # additionalProperties re-applied from not_closed (closed=False -> True)
    assert validator.schema["additionalProperties"] is True
    # Metadata inherited from the cached root (belt-and-braces parity)
    assert validator.schema["$schema"] == cached_root["$schema"]
    assert validator.schema["$id"] == cached_root["$id"]
    # Dog's keywords inlined at root
    assert "properties" in validator.schema
    assert set(validator.schema["properties"]) == {"name", "breed"}


# Regression: keys from the warming class must not leak into a different target


def test_cache_hit_does_not_leak_warmer_class_required_into_target():
    """When the cache is warmed by a class with required slots, then hit for a
    target class that has none, the cache-hit root must NOT carry the warming
    class's `required` list. Previously this leaked because root-mergeable keys
    were only excluded from `cached` when the target class also defined them."""
    schema = SchemaDefinition(
        id="https://example.org/leakage_test",
        name="leakage_test",
        classes=[
            ClassDefinition(name="Strict", tree_root=True, slots=["required_field"]),
            ClassDefinition(name="Lenient", slots=["optional_field"]),
        ],
        slots=[
            SlotDefinition(name="required_field", required=True),
            SlotDefinition(name="optional_field"),
        ],
    )
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    # Warm with Strict -> cached root carries required: ["required_field"]
    ValidationContext(schema, "Strict").json_schema_validator(closed=False, include_range_class_descendants=False)
    assert _json_schema_cache[cache_key].get("required") == ["required_field"]

    # Hit cache for Lenient -> root must not inherit the leaked `required`
    validator = ValidationContext(schema, "Lenient").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )
    assert "required" not in validator.schema, validator.schema.get("required")

    # And the instance must validate (would fail with the leak: missing required_field)
    errors = list(validator.iter_errors({"optional_field": "ok"}))
    assert errors == [], errors


# Regression: cache-hit validator must behave identically to a cold-cache one


@pytest.mark.parametrize("closed", [True, False])
def test_cache_hit_validator_matches_cold_cache(closed):
    """A cache-hit validator must produce the same errors as a cold-cache one
    for the same target_class on every instance. Guards against the
    additionalProperties divergence caused by the old $ref-wrapping approach,
    plus any sibling cases (extra props, missing fields, etc)."""
    schema = _two_class_schema()

    # Cold-cache validator for Dog
    cold = ValidationContext(schema, "Dog").json_schema_validator(closed=closed, include_range_class_descendants=False)

    # Warm the cache via Animal, then build a hit-path validator for Dog
    _json_schema_cache.clear()
    ValidationContext(schema, "Animal").json_schema_validator(closed=closed, include_range_class_descendants=False)
    warm = ValidationContext(schema, "Dog").json_schema_validator(closed=closed, include_range_class_descendants=False)

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


# Cache bounding & stable-key behaviour


def test_cache_key_disambiguates_distinct_schemas_with_shared_metadata():
    """Two distinct SchemaDefinition Python objects must always get distinct
    cache slots, even when they share (id, name, version). This is the
    property that prevents `--include` overlay merges from aliasing onto an
    earlier no-overlay generation, and prevents the compliance test suite's
    placeholder-id pattern from cross-contaminating cache entries."""
    # Same id+name+version, but distinct Python objects with different content
    schema_a = SchemaDefinition(
        id="https://example.org/shared",
        name="shared",
        classes=[
            ClassDefinition(
                name="X",
                tree_root=True,
                attributes=[SlotDefinition(name="s1", required=True)],
            )
        ],
    )
    schema_b = SchemaDefinition(
        id="https://example.org/shared",
        name="shared",
        classes=[
            ClassDefinition(
                name="X",
                tree_root=True,
                attributes=[SlotDefinition(name="s1")],  # not required — different content
            )
        ],
    )
    assert schema_a is not schema_b

    key_a = _make_cache_key(schema_a, include_range_class_descendants=False)
    key_b = _make_cache_key(schema_b, include_range_class_descendants=False)
    assert key_a != key_b, "distinct Python objects must not share a cache slot"

    v_a = ValidationContext(schema_a, "X").json_schema_validator(closed=False, include_range_class_descendants=False)
    v_b = ValidationContext(schema_b, "X").json_schema_validator(closed=False, include_range_class_descendants=False)

    # Each validator honours its own content, not whichever warmed the cache first.
    assert list(v_a.iter_errors({})) != [], "schema_a requires s1  -> must reject {}"
    assert list(v_b.iter_errors({})) == [], "schema_b does not require s1  -> must accept {}"


def test_cache_pins_schema_to_prevent_id_recycling():
    """While a cache entry exists, the cache holds a strong reference to the
    schema in `_schema_pins`. This prevents CPython from GC'ing the schema and
    recycling its id() onto an unrelated SchemaDefinition (which would alias
    the new object onto the stale cache entry)."""
    schema = _two_class_schema()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    ValidationContext(schema, "Animal").json_schema_validator(closed=False, include_range_class_descendants=False)

    assert cache_key in _schema_pins
    assert _schema_pins[cache_key] is schema  # same object, kept alive by the pin


def test_cache_key_disambiguates_same_id_different_name():
    """Two distinct schemas sharing the same id but different names (e.g. the
    linkml compliance suite's pattern of building many test schemas under a
    shared placeholder id like "http://example.org/default") must cache
    separately so their $defs do not bleed across tests."""
    shared_id = "http://example.org/shared_placeholder"
    # Make the two schemas behaviorally distinct: A requires s1, B does not.
    schema_a = SchemaDefinition(
        id=shared_id,
        name="logically_distinct_a",
        classes=[
            ClassDefinition(
                name="A",
                tree_root=True,
                attributes=[SlotDefinition(name="s1", required=True)],
            )
        ],
    )
    schema_b = SchemaDefinition(
        id=shared_id,
        name="logically_distinct_b",
        classes=[
            ClassDefinition(
                name="A",
                tree_root=True,
                attributes=[SlotDefinition(name="s1")],  # not required
            )
        ],
    )

    key_a = _make_cache_key(schema_a, include_range_class_descendants=False)
    key_b = _make_cache_key(schema_b, include_range_class_descendants=False)
    assert key_a != key_b, "schemas with same id but different names must NOT share a cache slot"

    v_a = ValidationContext(schema_a, "A").json_schema_validator(closed=False, include_range_class_descendants=False)
    v_b = ValidationContext(schema_b, "A").json_schema_validator(closed=False, include_range_class_descendants=False)

    # Distinct cache entries, not aliased
    assert _json_schema_cache[key_a] is not _json_schema_cache[key_b]

    # Each validator honours its own schema's `required`, not whichever warmed the cache first.
    empty_instance = {}
    assert list(v_a.iter_errors(empty_instance)) != [], "schema_a requires s1  -> must reject {}"
    assert list(v_b.iter_errors(empty_instance)) == [], "schema_b does not require s1  -> must accept {}"


def test_cache_is_bounded_lru_evicts_oldest():
    """Once the cache exceeds _JSON_SCHEMA_CACHE_MAXSIZE, the least recently used
    entry is evicted. Recent entries (including the one we just touched) stay."""
    # Build maxsize+1 distinct schemas to force one eviction
    schemas = [
        SchemaDefinition(
            id=f"https://example.org/schema_{i}",
            name=f"schema_{i}",
            classes=[ClassDefinition(name="Root", tree_root=True)],
        )
        for i in range(_JSON_SCHEMA_CACHE_MAXSIZE + 1)
    ]

    keys = []
    for schema in schemas:
        key = _make_cache_key(schema, include_range_class_descendants=False)
        keys.append(key)
        ValidationContext(schema, "Root").json_schema_validator(closed=False, include_range_class_descendants=False)

    # The very first key should have been evicted; the rest remain
    assert len(_json_schema_cache) == _JSON_SCHEMA_CACHE_MAXSIZE
    assert keys[0] not in _json_schema_cache
    assert keys[0] not in _schema_pins, "evicted entry must also drop the schema pin"
    for key in keys[1:]:
        assert key in _json_schema_cache
        assert key in _schema_pins


def test_cache_hit_marks_entry_as_mru():
    """A cache hit moves the entry to the MRU end so it survives subsequent eviction
    even if it was the oldest at the time of the hit."""
    # Insert 2 entries: A then B (B is MRU)
    schema_a = SchemaDefinition(
        id="https://example.org/mru_a",
        name="mru_a",
        classes=[ClassDefinition(name="Root", tree_root=True)],
    )
    schema_b = SchemaDefinition(
        id="https://example.org/mru_b",
        name="mru_b",
        classes=[ClassDefinition(name="Root", tree_root=True)],
    )
    ValidationContext(schema_a, "Root").json_schema_validator(closed=False, include_range_class_descendants=False)
    ValidationContext(schema_b, "Root").json_schema_validator(closed=False, include_range_class_descendants=False)

    # Touch A again -> now A becomes MRU, B becomes LRU
    ValidationContext(schema_a, "Root").json_schema_validator(closed=False, include_range_class_descendants=False)

    # Fill the cache to capacity with maxsize-1 fresh entries (A and B already there,
    # plus maxsize-1 new ones -> maxsize+1 total -> one eviction). B (now LRU) should go.
    for i in range(_JSON_SCHEMA_CACHE_MAXSIZE - 1):
        schema_fresh = SchemaDefinition(
            id=f"https://example.org/mru_fresh_{i}",
            name=f"mru_fresh_{i}",
            classes=[ClassDefinition(name="Root", tree_root=True)],
        )
        ValidationContext(schema_fresh, "Root").json_schema_validator(
            closed=False, include_range_class_descendants=False
        )

    key_a = _make_cache_key(schema_a, include_range_class_descendants=False)
    key_b = _make_cache_key(schema_b, include_range_class_descendants=False)
    assert key_a in _json_schema_cache, "A was touched, should be MRU-protected"
    assert key_b not in _json_schema_cache, "B was the LRU at eviction time"


# Class-level rules (if/then) at root must round-trip through cache-hit


def _schema_with_rule() -> SchemaDefinition:
    """Schema where Address has a class-level rule (country=USA -> postal_code
    must be 5 digits) and Simple has no rule. JsonSchemaGenerator hoists the
    rule's `if`/`then` from Address's class_subschema into the root of any
    validator targeted at Address — exercising root-level keywords the cache-hit
    rebuild must preserve (when targeting Address) AND must NOT leak from
    cached (when targeting Simple after Address has warmed the cache)."""
    return SchemaDefinition(
        id="https://example.org/rules_test",
        name="rules_test",
        classes=[
            ClassDefinition(
                name="Address",
                tree_root=True,
                slots=["country", "postal_code"],
                rules=[
                    ClassRule(
                        preconditions=AnonymousClassExpression(
                            slot_conditions={
                                "country": SlotDefinition(name="country", equals_string="USA"),
                            },
                        ),
                        postconditions=AnonymousClassExpression(
                            slot_conditions={
                                "postal_code": SlotDefinition(name="postal_code", pattern=r"^[0-9]{5}$"),
                            },
                        ),
                    ),
                ],
            ),
            ClassDefinition(name="Simple", slots=["country"]),
        ],
        slots=[
            SlotDefinition(name="country", range="string"),
            SlotDefinition(name="postal_code", range="string"),
        ],
    )


def test_cache_hit_preserves_class_rules_if_then():
    """A rule-bearing target_class hit on a cache warmed by a rule-less class
    must still apply the rule. Previously, the $ref-wrapper approach would also
    delegate to $defs[Address] (which has the rule), but the inlined rebuild
    must explicitly carry if/then over from defs_class — pin this."""
    schema = _schema_with_rule()

    # Cold cache for Address
    cold = ValidationContext(schema, "Address").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )
    # Warm via Simple (no rule), then hit cache for Address
    _json_schema_cache.clear()
    ValidationContext(schema, "Simple").json_schema_validator(closed=False, include_range_class_descendants=False)
    warm = ValidationContext(schema, "Address").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )

    # Root-level if/then must be present in both
    assert "if" in cold.schema and "then" in cold.schema
    assert "if" in warm.schema and "then" in warm.schema, "rule's if/then must survive cache-hit"

    # Rule fires: country=USA, postal_code='ABCDE' violates the pattern
    bad = {"country": "USA", "postal_code": "ABCDE"}
    cold_errs = sorted(e.message for e in cold.iter_errors(bad))
    warm_errs = sorted(e.message for e in warm.iter_errors(bad))
    assert cold_errs == warm_errs
    assert cold_errs != [], "rule must produce at least one error"

    # Counter-example — rule does not fire for non-US country
    ok = {"country": "Canada", "postal_code": "K1A 0B1"}
    assert list(cold.iter_errors(ok)) == list(warm.iter_errors(ok)) == []


def test_cache_hit_does_not_leak_class_rules_to_target_without_rules():
    """Warming the cache with the rule-bearing Address leaves cached root with
    if/then. A subsequent cache-hit for Simple (which has no rule) must NOT
    inherit those keys — they live outside _ROOT_METADATA_KEYS and are not in
    Simple's defs entry, so the rebuild correctly drops them."""
    schema = _schema_with_rule()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    # Warm via Address -> cached carries if/then at root from the rule merge
    ValidationContext(schema, "Address").json_schema_validator(closed=False, include_range_class_descendants=False)
    assert "if" in _json_schema_cache[cache_key]

    # Hit cache for Simple
    validator = ValidationContext(schema, "Simple").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )
    assert "if" not in validator.schema, validator.schema.get("if")
    assert "then" not in validator.schema, validator.schema.get("then")

    # And rule must not fire — country=USA with no postal_code is fine for Simple
    assert list(validator.iter_errors({"country": "USA"})) == []


# include_range_class_descendants: cold-vs-warm parity in the affirmative case


def test_cache_hit_with_include_range_class_descendants_matches_cold():
    """include_range_class_descendants=True is in the cache key (because it
    changes $defs contents). Confirm cold and warm validators behave identically
    when the flag is True — guards against any future refactor that would
    accidentally rebuild differently for the descendants-enabled cache slot."""
    schema = _two_class_schema()

    cold = ValidationContext(schema, "Dog").json_schema_validator(closed=False, include_range_class_descendants=True)

    _json_schema_cache.clear()
    ValidationContext(schema, "Animal").json_schema_validator(closed=False, include_range_class_descendants=True)
    warm = ValidationContext(schema, "Dog").json_schema_validator(closed=False, include_range_class_descendants=True)

    for inst in [{"name": "Rex", "breed": "Lab"}, {"breed": "Lab"}, {}]:
        cold_errs = sorted(e.message for e in cold.iter_errors(inst))
        warm_errs = sorted(e.message for e in warm.iter_errors(inst))
        assert cold_errs == warm_errs, (inst, cold_errs, warm_errs)


# value_disallowed (value_presence=ABSENT) emits a root-level `not` keyword.
# Same mechanism as rules, different keyword — guard explicitly because `not`
# is the only root-level boolean-combinator JsonSchemaGenerator can emit and
# regressing it silently would weaken validation in a subtle way.


def _schema_with_value_disallowed() -> SchemaDefinition:
    """ForbidsX has a slot whose value_presence=ABSENT — the generator emits
    `not: {required: [forbidden_field]}` on that class. Plain has no such slot.
    Used to verify the cache-hit rebuild both preserves and contains `not`."""
    return SchemaDefinition(
        id="https://example.org/value_disallowed_test",
        name="value_disallowed_test",
        classes=[
            ClassDefinition(
                name="ForbidsX",
                tree_root=True,
                slots=["forbidden_field", "other_field"],
                slot_usage={
                    "forbidden_field": SlotDefinition(
                        name="forbidden_field",
                        value_presence=PresenceEnum(PresenceEnum.ABSENT),
                    ),
                },
            ),
            ClassDefinition(name="Plain", slots=["other_field"]),
        ],
        slots=[
            SlotDefinition(name="forbidden_field", range="string"),
            SlotDefinition(name="other_field", range="string"),
        ],
    )


def test_cache_hit_preserves_value_disallowed_not_keyword():
    """A slot with value_presence=ABSENT produces a root-level `not` keyword.
    Cache-hit must carry it through from defs_class so the validator rejects
    instances that include the forbidden field."""
    schema = _schema_with_value_disallowed()

    cold = ValidationContext(schema, "ForbidsX").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )
    _json_schema_cache.clear()
    ValidationContext(schema, "Plain").json_schema_validator(closed=False, include_range_class_descendants=False)
    warm = ValidationContext(schema, "ForbidsX").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )

    assert "not" in cold.schema, cold.schema
    assert "not" in warm.schema, "value_disallowed `not` keyword must survive cache-hit"

    # Instance includes the forbidden field -> both validators reject
    bad = {"forbidden_field": "anything", "other_field": "ok"}
    cold_errs = sorted(e.message for e in cold.iter_errors(bad))
    warm_errs = sorted(e.message for e in warm.iter_errors(bad))
    assert cold_errs == warm_errs
    assert cold_errs != []

    # Instance omits the forbidden field -> both accept
    ok = {"other_field": "ok"}
    assert list(cold.iter_errors(ok)) == list(warm.iter_errors(ok)) == []


def test_cache_hit_does_not_leak_value_disallowed_not_to_target_without():
    """Warming with ForbidsX places `not` at root in cached. Hitting cache for
    Plain (which has no value_disallowed slots) must NOT inherit `not`."""
    schema = _schema_with_value_disallowed()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    ValidationContext(schema, "ForbidsX").json_schema_validator(closed=False, include_range_class_descendants=False)
    assert "not" in _json_schema_cache[cache_key]

    validator = ValidationContext(schema, "Plain").json_schema_validator(
        closed=False, include_range_class_descendants=False
    )
    assert "not" not in validator.schema, validator.schema.get("not")

    # Plain has no constraint against `forbidden_field` — the leak would falsely
    # reject this. Confirm it doesn't.
    assert list(validator.iter_errors({"other_field": "ok", "forbidden_field": "x"})) == []


# Defensive: target_class missing from $defs is unreachable through the public
# API (because _get_target_class validates against schema and the generator
# processes every class), but the .get(defs_key, {}) fallback exists in case
# a future code path skips that guard. Pin it.


def test_cache_hit_with_missing_defs_class_falls_back_safely():
    """If the cached $defs lacks the canonical target class entry, the rebuild
    must not crash and must produce a validator with only the metadata + an
    overridden additionalProperties — a maximally permissive root."""
    schema = _two_class_schema()
    cache_key = _make_cache_key(schema, include_range_class_descendants=False)

    # Warm cache normally
    ValidationContext(schema, "Animal").json_schema_validator(closed=False, include_range_class_descendants=False)
    # Surgically remove Dog's entry from the cached $defs to simulate the gap
    del _json_schema_cache[cache_key]["$defs"]["Dog"]

    ctx = ValidationContext(schema, "Dog")
    validator = ctx.json_schema_validator(closed=False, include_range_class_descendants=False)

    # Rebuild succeeded — no KeyError
    assert "$schema" in validator.schema
    assert "$defs" in validator.schema
    assert validator.schema["additionalProperties"] is True
    # No class-specific keys leaked from cached (Animal's properties stayed put)
    assert "properties" not in validator.schema
    assert "required" not in validator.schema


# Combinatorial: rules + include_range_class_descendants. Each axis is covered
# individually above; this pins their interaction so a future refactor of one
# can't break the other.


def test_cache_hit_with_rules_and_range_descendants_matches_cold():
    schema = _schema_with_rule()

    cold = ValidationContext(schema, "Address").json_schema_validator(
        closed=False, include_range_class_descendants=True
    )
    _json_schema_cache.clear()
    ValidationContext(schema, "Simple").json_schema_validator(closed=False, include_range_class_descendants=True)
    warm = ValidationContext(schema, "Address").json_schema_validator(
        closed=False, include_range_class_descendants=True
    )

    instances = [
        {"country": "USA", "postal_code": "12345"},  # rule satisfied
        {"country": "USA", "postal_code": "ABCDE"},  # rule violated
        {"country": "Canada", "postal_code": "K1A 0B1"},  # rule does not fire
        {},  # rule does not fire
    ]
    for inst in instances:
        cold_errs = sorted(e.message for e in cold.iter_errors(inst))
        warm_errs = sorted(e.message for e in warm.iter_errors(inst))
        assert cold_errs == warm_errs, (inst, cold_errs, warm_errs)
