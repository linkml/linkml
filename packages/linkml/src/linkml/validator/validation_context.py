import json
import os
from collections import OrderedDict
from functools import lru_cache

import jsonschema
from jsonschema.protocols import Validator

from linkml.generators import JsonSchemaGenerator, PydanticGenerator
from linkml.generators.jsonschemagen import JsonSchema
from linkml.utils.datautils import infer_root_class
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.formatutils import camelcase

# Module-level bounded cache of generated JSON Schemas.
# See https://github.com/linkml/linkml/pull/3430 for discussion.
#
# Key: (id(schema), include_range_class_descendants).
# Using id(schema) as the discriminator avoids two failure modes of any
# metadata-based key (id/name/version): (a) workflows that load multiple
# distinct schemas under a placeholder id like "http://example.org/default"
# (test_compliance.py); (b) workflows that merge overlays into a base schema
# via `--include`, producing a logically different schema that inherits the
# base's id/name/version. Distinct Python objects always get distinct keys.
#
# To guard against CPython recycling id() after a schema is GC'd (aliasing
# the new object onto a stale cache entry), the `_schema_pins` dict has
# a strong reference to each cached schema. The ref drops only when the
# entry is evicted by the bounded LRU policy - allowing id reuse, but
# the cache no longer has any stale entry to alias against.
# See: https://en.wikipedia.org/wiki/Cache_replacement_policies
#
# The root's additionalProperties is overridden at retrieval time, so cached
# $defs are reusable regardless of closed.
_JSON_SCHEMA_CACHE_MAXSIZE = 32
_json_schema_cache: OrderedDict[tuple, JsonSchema] = OrderedDict()
_schema_pins: dict[tuple, SchemaDefinition] = {}


def _make_cache_key(
    schema: SchemaDefinition,
    include_range_class_descendants: bool,
) -> tuple:
    return (id(schema), include_range_class_descendants)


# Keys that JsonSchemaGenerator's start_schema sets on the root and that the
# per-class merge step in handle_class does NOT overwrite. These are
# schema-level: they describe the schema as a whole, not whichever class
# happens to have warmed the cache. Safe to inherit from the cached root.
_ROOT_METADATA_KEYS: tuple = ("$schema", "$id", "metamodel_version", "version", "title", "type")


class ValidationContext:
    """Provides state that may be shared between validation plugins"""

    def __init__(self, schema: SchemaDefinition, target_class: str | None = None) -> None:
        # Since SchemaDefinition is not hashable, to make caching simpler we store the schema
        # in a "private" property and assume it never changes.
        self._schema = schema
        self._schema_view = SchemaView(self._schema)
        self._target_class = self._get_target_class(target_class)

    @property
    def schema_view(self):
        return self._schema_view

    @property
    def target_class(self):
        return self._target_class

    @lru_cache
    def json_schema_validator(
        self,
        *,
        closed: bool,
        include_range_class_descendants: bool,
        path_override: os.PathLike | None = None,
    ) -> Validator:
        if path_override:
            with open(path_override) as json_schema_file:
                json_schema = json.load(json_schema_file)
        else:
            not_closed = not closed
            cache_key = _make_cache_key(self._schema, include_range_class_descendants)

            if cache_key not in _json_schema_cache:
                # First call: generate and cache entire schema (full generation cost)
                jsonschema_gen = JsonSchemaGenerator(
                    schema=self._schema,
                    mergeimports=True,
                    top_class=self._target_class,
                    not_closed=not_closed,
                    include_range_class_descendants=include_range_class_descendants,
                )
                json_schema = jsonschema_gen.generate()
                _json_schema_cache[cache_key] = json_schema
                # Pin the schema so id() cannot be recycled while this entry exists.
                _schema_pins[cache_key] = self._schema
                while len(_json_schema_cache) > _JSON_SCHEMA_CACHE_MAXSIZE:
                    evicted_key, _ = _json_schema_cache.popitem(last=False)
                    _schema_pins.pop(evicted_key, None)
            else:
                # Subsequent calls: reuse cached $defs, rebuild the root by re-doing
                # JsonSchemaGenerator's "merge top class into root" step for a new target.
                # Wrapping with $ref would inherit the hardcoded additionalProperties=False
                # from $defs[X] (see jsonschemagen.py handle_class) and diverge from a
                # freshly-generated validator when closed=False.
                _json_schema_cache.move_to_end(cache_key)  # mark as MRU (most recently used)
                cached = _json_schema_cache[cache_key]
                # $defs keys are camelCased by JsonSchemaGenerator when preserve_names=False
                # (the mode used here), so look up under the canonical name.
                defs_key = camelcase(self._target_class)
                defs_class = cached["$defs"].get(defs_key, {})
                # Build the root in three layers:
                # 1) Schema-level metadata inherited from cached (immune to which class
                #    happened to warm the cache).
                # 2) Class-specific keys from $defs[target_class] (properties, required,
                #    description, if/then/else, allOf, plus any extension-hook additions).
                #    Exclude $schema/$id/$defs/additionalProperties (handled separately)
                #    and the metadata keys (already inherited from cached).
                # 3) additionalProperties explicitly set to not_closed.
                root = {k: cached[k] for k in _ROOT_METADATA_KEYS if k in cached}
                root["$defs"] = cached["$defs"]
                root.update(
                    {
                        k: v
                        for k, v in defs_class.items()
                        if k not in _ROOT_METADATA_KEYS and k not in ("$schema", "$id", "$defs", "additionalProperties")
                    }
                )
                root["additionalProperties"] = not_closed
                json_schema = JsonSchema(root)

        validator_cls = jsonschema.validators.validator_for(json_schema, default=jsonschema.Draft7Validator)
        return validator_cls(json_schema, format_checker=validator_cls.FORMAT_CHECKER)

    def pydantic_model(self, *, closed: bool):
        module = self._pydantic_module(closed=closed)
        return module.__dict__[self._target_class]

    @lru_cache
    def _pydantic_module(self, *, closed: bool):
        return PydanticGenerator(
            self._schema,
            extra_fields="forbid" if closed else "ignore" if closed is None else "allow",
        ).compile_module()

    def _get_target_class(self, target_class: str | None = None) -> str:
        if target_class is None:
            return infer_root_class(self._schema_view)
        else:
            # strict=True raises ValueError if class is not found in schema
            class_def = self._schema_view.get_class(target_class, strict=True)
            return class_def.name
