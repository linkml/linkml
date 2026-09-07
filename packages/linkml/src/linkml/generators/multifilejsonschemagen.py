"""
Multi-file JSON Schema generator.

Partitions a LinkML schema across multiple JSON Schema files based on a
two-tier annotation contract. Cross-file ``$ref`` targets are rewritten
to reference the file in which their target class lives.

Designed as a thin subclass of :class:`.JsonSchemaGenerator` so that all
mature JSON-Schema emission machinery is reused without modification.

Annotation contract
-------------------

Annotations live under the LinkML metamodel's native ``annotations``
mapping. The contract is **tiered** so a single annotated schema can
drive multiple multi-file generators (JSON Schema today; Pydantic,
Rust, etc. in the future) without coupling the schema to JSON-Schema
terminology.

**Tier 1 — generic vocabulary (no prefix).** Concepts every multi-file
generator needs. Reserved well-known tags, candidates for promotion to
first-class LinkML metamodel slots later.

``output_file`` (str)
    Stem (or full filename) of the artifact the class is emitted into.
    Stems without a ``.`` get the generator's extension appended
    (``.json`` here). Classes without this annotation are routed to
    ``--default-file``.

``inline_class`` (bool)
    When true, the class is not emitted as a standalone definition;
    every reference to the class is replaced by an inlined copy of
    its body at the use site.

``additional_properties`` (bool)
    Per-class "open vs. closed" override. Prefer ``extra_slots.allowed``
    (LinkML 1.6+) when available; this annotation only applies when
    ``extra_slots`` is not set.

**Tier 2 — JSON-Schema-specific (``jsonschema:`` prefix).** Concepts
that have no equivalent (or different semantics) in other generators.

``jsonschema:is_root_of_file`` (bool)
    Promote the class body to the *root* of its file
    (``{type, properties, ...}``); no ``$defs`` entry is emitted for it.

``jsonschema:def_name`` (str)
    Override the ``$defs`` key under which the class is emitted.
    Defaults to the parent generator's canonical key (``camelcase``
    unless ``--preserve-names``).

``jsonschema:pattern_properties`` (str)
    Rewrap the class body as
    ``{type: object, patternProperties: {<pattern>: <inner>}}`` where
    ``<inner>`` is the regular block the parent would emit.

``jsonschema:discriminator_enum`` (str)
    Name of an enum whose permissible values name required keys on
    this class. Emits ``oneOf: [{required: [<v>]}, ...]`` appended to
    the class body. Pairs naturally with ``inline_class``.

**Override precedence.** For any Tier 1 tag, a Tier 2 form
(``jsonschema:<key>``) takes precedence when present, so generic
defaults can be selectively overridden per generator. Tier 2-only tags
have no Tier 1 fallback by design.

**Subset-driven defaults (DRY).** Every **class-level** tag above is
also resolvable from the annotations of any
:class:`~linkml_runtime.linkml_model.meta.SubsetDefinition` the class
belongs to (via ``in_subset``). This lets schemas declare per-bucket
defaults once at the subset level instead of repeating them on every
class:

.. code-block:: yaml

    subsets:
      core:
        annotations:
          output_file: core
          jsonschema:additional_properties: true

    classes:
      Architecture:
        in_subset: [core]
        annotations:
          jsonschema:is_root_of_file: true   # class-level override
      Decision:
        in_subset: [core]                    # inherits output_file=core

Full resolution order, most specific to least:

1. ``jsonschema:<key>`` on the class
2. ``<key>`` on the class
3. ``jsonschema:<key>`` on any of the class's ``in_subset[]`` subsets
4. ``<key>`` on any of the class's ``in_subset[]`` subsets

When a class is in multiple subsets that resolve the same key to
different values, generation fails loudly with a :class:`ValueError`
naming the class, the annotation, and the conflicting
``(subset, value)`` pairs. Resolve by setting the annotation directly
on the class, or by making the subset values agree.

A second related constraint: at most one class per output file may
carry ``jsonschema:is_root_of_file: true`` (a single file cannot have
two competing root bodies). Subset-level promotion that lands two or
more member classes on the same file therefore also fails loudly at
lookup-build time; opt one class out with a class-level
``jsonschema:is_root_of_file: false`` (class wins over subset) or
split them across distinct ``output_file`` targets.

**Schema-level annotations.** Schema-level tags (``property_name_style``)
are read from the schema's own annotations and are **not** subset-resolved
(subsets are element-level constructs).

``property_name_style`` (str)
    One of ``snake_case`` (default), ``kebab_case``, ``preserve``. When
    ``kebab_case``, property names use the first hyphen-containing alias
    if present, otherwise the slot name with underscores replaced by
    hyphens. Implies ``preserve_names`` so the generator does not
    canonicalize names downstream. Honors the same Tier 2 override
    (``jsonschema:property_name_style``).
"""

from __future__ import annotations

import json
import logging
import os
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import click

from linkml._version import __version__
from linkml.generators.jsonschemagen import (
    JsonSchema,
    JsonSchemaGenerator,
    SchemaResult,
)
from linkml.utils.generator import shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore

logger = logging.getLogger(__name__)


#: Prefix that scopes Tier 2 annotations to this generator. Matches the
#: existing LinkML convention for system-level annotation tags
#: (e.g. ``linkml:derived_from`` in sqlalchemygen).
TARGET_PREFIX = "jsonschema"

#: Tier 1 — generic, cross-target concepts. A Tier 2 form
#: (``jsonschema:<key>``) wins when both are present.
GENERIC_CLASS_ANNOTATIONS = (
    "output_file",
    "inline_class",
    "additional_properties",
)
#: Tier 2 — JSON-Schema-only concepts. No Tier 1 fallback by design.
TARGET_ONLY_CLASS_ANNOTATIONS = (
    "is_root_of_file",
    "def_name",
    "pattern_properties",
    "discriminator_enum",
)
#: Schema-level annotations follow the same precedence rules.
GENERIC_SCHEMA_ANNOTATIONS = ("property_name_style",)

PROPERTY_NAME_STYLES = ("snake_case", "kebab_case", "preserve")


def _annotation_value(ann: Any) -> Any:
    """Extract the value of a LinkML annotation.

    LinkML annotations are typed as ``Annotation`` objects with a ``.value``
    attribute, but raw dict values may also appear when annotations are read
    via plain dict access. Return the underlying value in either case.
    """
    if ann is None:
        return None
    if hasattr(ann, "value"):
        return ann.value
    return ann


def _read_annotation(
    annotations: Any,
    key: str,
    *,
    target_only: bool = False,
) -> Any:
    """Resolve an annotation with target-override-then-generic precedence.

    Lookup order:

    1. ``jsonschema:<key>`` — Tier 2 target-scoped override
    2. ``<key>`` — Tier 1 generic (skipped when ``target_only=True``)

    Returns the underlying value (via :func:`_annotation_value`) or
    ``None`` if neither key is set.
    """
    if not annotations or not hasattr(annotations, "get"):
        return None
    target_ann = annotations.get(f"{TARGET_PREFIX}:{key}")
    if target_ann is not None:
        return _annotation_value(target_ann)
    if target_only:
        return None
    return _annotation_value(annotations.get(key))


def _coerce_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "yes", "1", "on"):
            return True
        if lowered in ("false", "no", "0", "off"):
            return False
    return None


def _normalize_filename(value: str, extension: str = ".json") -> str:
    """Append the generator's extension to a stem if missing.

    Values containing a ``.`` are treated as full filenames and pass
    through verbatim — an escape hatch for explicit overrides.
    """
    return value if "." in value else f"{value}{extension}"


@dataclass
class MultiFileJsonSchemaGenerator(JsonSchemaGenerator):
    """Generate JSON Schema across multiple files, one bucket per
    ``output_file`` annotation, with cross-file ``$ref`` rewriting and
    optional inline-class, discriminator, and pattern-properties transforms.

    See module docstring for the full annotation contract.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["json"]
    file_extension = "schema.json"

    # New fields
    output_dir: str | None = None
    default_file: str = "schema.json"
    #: Tier 1 annotation key consulted for file partitioning. Override to
    #: rename the routing tag (e.g. to ``meta_file``) without changing the
    #: tiered precedence rules — ``jsonschema:<value>`` still wins.
    split_file_annotation: str = "output_file"

    # Internal state (not part of the public API; ``init=False`` keeps them
    # out of the dataclass-generated ``__init__`` signature).
    top_level_schemas: dict[str, JsonSchema] = field(init=False, default_factory=dict)
    _class_to_file: dict[str, str] = field(init=False, default_factory=dict)
    _class_to_parent_key: dict[str, str] = field(init=False, default_factory=dict)
    _parent_key_to_class: dict[str, str] = field(init=False, default_factory=dict)
    _class_to_def_name: dict[str, str] = field(init=False, default_factory=dict)
    _inline_class_names: set[str] = field(init=False, default_factory=set)
    _inline_class_bodies: dict[str, JsonSchema] = field(init=False, default_factory=dict)
    _root_of_file_classes: set[str] = field(init=False, default_factory=set)
    _resolved_property_name_style: str | None = field(init=False, default=None)
    _default_output_filename: str | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        super().__post_init__()
        # Activate name preservation if the schema requests a non-snake-case style.
        style = self._property_name_style()
        if style in ("kebab_case", "preserve"):
            self.preserve_names = True
            JsonSchema.PRESERVE_NAMES = True

    # Annotation helpers

    def _property_name_style(self) -> str:
        # Cached: called per slot via ``aliased_slot_name`` on large schemas.
        if self._resolved_property_name_style is not None:
            return self._resolved_property_name_style
        annotations = getattr(self.schema, "annotations", None) or {}
        value = _read_annotation(annotations, "property_name_style")
        if value is None:
            resolved = "snake_case"
        elif value not in PROPERTY_NAME_STYLES:
            logger.warning(
                "Unknown property_name_style %r; falling back to snake_case (valid: %s)",
                value,
                ", ".join(PROPERTY_NAME_STYLES),
            )
            resolved = "snake_case"
        else:
            resolved = value
        self._resolved_property_name_style = resolved
        return resolved

    def _get_default_filename(self) -> str:
        # Cached: ``_normalize_filename(self.default_file)`` is consulted from
        # multiple code paths (start_schema, handle_class, generate,
        # _target_file) but ``self.default_file`` never changes after init.
        if self._default_output_filename is None:
            self._default_output_filename = _normalize_filename(self.default_file)
        return self._default_output_filename

    def _class_annotation(
        self,
        cls,
        key: str,
        *,
        target_only: bool = False,
    ) -> Any:
        """Resolve a class-level annotation with target-override + subset fallback.

        Precedence order:

        1. ``jsonschema:<key>`` on the class (Tier 2)
        2. ``<key>`` on the class (Tier 1)
        3. Same Tier 2-then-Tier 1 precedence on each ``cls.in_subset[]``
           subset's own annotations.

        At step 3, every contributing subset's resolved value must agree;
        a disagreement raises :class:`ValueError` naming the class, the
        annotation, and the conflicting (subset, value) pairs. Authors
        resolve a conflict by setting the annotation directly on the
        class (which then wins via step 1 or 2) or by aligning the
        subset values.

        Pass ``target_only=True`` for Tier 2-only annotations whose
        semantics are JSON-Schema-specific.
        """
        # Step 1+2: class-level lookup (existing behavior).
        annotations = getattr(cls, "annotations", None)
        value = _read_annotation(annotations, key, target_only=target_only)
        if value is not None:
            return value
        # Step 3: subset-level fallback.
        return self._subset_annotation(cls, key, target_only=target_only)

    def _subset_annotation(
        self,
        cls,
        key: str,
        *,
        target_only: bool = False,
    ) -> Any:
        """Resolve an annotation from the subsets a class belongs to.

        Within each subset, ``_read_annotation`` is used so the same
        Tier 2 (``jsonschema:<key>``) wins over Tier 1 (``<key>``) rule
        applies. Across subsets, every contributing value must agree;
        otherwise a :class:`ValueError` is raised.
        """
        in_subset = getattr(cls, "in_subset", None) or []
        if not in_subset:
            return None

        contributions: list[tuple[str, Any]] = []
        for subset_name in in_subset:
            # ``get_subset`` returns ``None`` for unknown subset names
            # (it does not raise). An unknown name is a schema-lint
            # concern, not a generator concern — skip silently.
            subset = self.schemaview.get_subset(subset_name)
            if subset is None:
                logger.debug(
                    "in_subset references unknown subset %r on class %r",
                    subset_name,
                    cls.name,
                )
                continue
            subset_value = _read_annotation(
                getattr(subset, "annotations", None),
                key,
                target_only=target_only,
            )
            if subset_value is not None:
                contributions.append((subset_name, subset_value))

        if not contributions:
            return None

        distinct = {value for _, value in contributions}
        if len(distinct) > 1:
            details = ", ".join(f"{name!s}={value!r}" for name, value in contributions)
            raise ValueError(
                f"Class {cls.name!r} inherits conflicting values for annotation "
                f"{key!r} from multiple subsets: {details}. Resolve by setting "
                f"the annotation directly on the class, or by making the "
                f"subset values agree."
            )

        return contributions[0][1]

    def _target_file(self, cls: ClassDefinition) -> str:
        """Resolve the output filename for a class.

        Stem-only values get ``.json`` appended; values containing a ``.``
        pass through verbatim. The ``split_file_annotation`` field
        determines the Tier 1 tag name; ``jsonschema:<that-tag>`` still
        wins per the tiered precedence rules.
        """
        value = self._class_annotation(cls, self.split_file_annotation)
        if not value:
            return self._get_default_filename()
        return _normalize_filename(str(value))

    def _parent_def_key(self, name: str) -> str:
        """Reproduce the ``$defs`` key the parent generator will emit."""
        return name if self.preserve_names else camelcase(name)

    def _desired_def_name(self, cls: ClassDefinition) -> str:
        explicit = self._class_annotation(cls, "def_name", target_only=True)
        if explicit:
            return explicit
        return self._parent_def_key(cls.name)

    def _build_class_lookups(self) -> None:
        self._class_to_file = {}
        self._class_to_parent_key = {}
        self._parent_key_to_class = {}
        self._class_to_def_name = {}
        self._inline_class_names = set()
        self._root_of_file_classes = set()
        # ``imports=True`` (the default) mirrors what ``generate()`` iterates
        # over so imported classes (when ``mergeimports=True``) are routable
        # via the file-partition annotations and their ``$ref``s rewriteable.
        for cls in self.schemaview.all_classes().values():
            self._class_to_file[cls.name] = self._target_file(cls)
            parent_key = self._parent_def_key(cls.name)
            self._class_to_parent_key[cls.name] = parent_key
            self._parent_key_to_class[parent_key] = cls.name
            self._class_to_def_name[cls.name] = self._desired_def_name(cls)
            if _coerce_bool(self._class_annotation(cls, "inline_class")):
                self._inline_class_names.add(cls.name)
            if _coerce_bool(self._class_annotation(cls, "is_root_of_file", target_only=True)):
                self._root_of_file_classes.add(cls.name)

        # At most one root-of-file class may land on each output file —
        # otherwise ``_promote_root_of_file`` would silently overwrite the
        # first body with the second. This is easy to trip when
        # ``jsonschema:is_root_of_file`` is set at the subset level and
        # the subset has multiple member classes routed to the same file.
        root_by_file: dict[str, list[str]] = {}
        for cls_name in self._root_of_file_classes:
            root_by_file.setdefault(self._class_to_file[cls_name], []).append(cls_name)
        conflicts = {f: sorted(c) for f, c in root_by_file.items() if len(c) > 1}
        if conflicts:
            details = "; ".join(f"{filename}: {classes}" for filename, classes in sorted(conflicts.items()))
            raise ValueError(
                "Multiple classes marked 'jsonschema:is_root_of_file' route to "
                f"the same file: {details}. Each output file can promote at most "
                "one class to its root; set the annotation on the class directly "
                "(class wins over subset) or split the classes across different "
                "'output_file' targets."
            )

    # Overrides of JsonSchemaGenerator extension points

    def start_schema(self, inline: bool = False) -> None:
        """Build a ``JsonSchema`` per target file instead of one global doc.

        ``self.top_level_schema`` always points at the per-file ``JsonSchema``
        that is currently being populated; ``handle_class`` swaps it for the
        duration of each class.
        """
        self.inline = inline
        if not self._class_to_file:
            self._build_class_lookups()

        self.top_level_schemas = {}
        self._inline_class_bodies = {}

        default_filename = self._get_default_filename()
        filenames = set(self._class_to_file.values()) | {default_filename}
        for filename in sorted(filenames):
            self.top_level_schemas[filename] = self._new_top_level_schema(filename)

        # Parent code paths that touch ``self.top_level_schema`` directly
        # (e.g. ``add_lax_def`` during slot subschema construction) need a
        # sensible default before any class is being processed.
        self.top_level_schema = self.top_level_schemas[default_filename]

    def _new_top_level_schema(self, filename: str) -> JsonSchema:
        base_id = self.schema.id or ""
        if base_id and not base_id.endswith("/"):
            file_id = f"{base_id}/{filename}"
        else:
            file_id = f"{base_id}{filename}"
        title = self.schema.title if self.title_from == "title" and self.schema.title else self.schema.name
        return JsonSchema(
            {
                "$schema": "https://json-schema.org/draft/2019-09/schema",
                "$id": file_id,
                "title": title,
                "type": "object",
                "additionalProperties": self.not_closed,
            }
        )

    def handle_class(self, cls: ClassDefinition) -> None:
        # Make sure lookups exist even when handle_class is called outside of
        # ``generate`` (e.g. by tests exercising single classes).
        if not self._class_to_file:
            self._build_class_lookups()

        default_filename = self._get_default_filename()
        target_file = self._class_to_file.get(cls.name, default_filename)
        file_schema = self.top_level_schemas.setdefault(target_file, self._new_top_level_schema(target_file))

        # Route the parent generator's writes (``add_def``, ``add_lax_def``,
        # tree-root promotion) into the per-file schema.
        previous = self.top_level_schema
        self.top_level_schema = file_schema
        try:
            super().handle_class(cls)
        finally:
            self.top_level_schema = previous

        parent_key = self._class_to_parent_key.get(cls.name, self._parent_def_key(cls.name))
        defs = file_schema.get("$defs") or {}
        if parent_key not in defs:
            # ``is_class_unconstrained`` paths or anonymous classes may not
            # produce a def entry; nothing further to post-process.
            return

        class_subschema = defs[parent_key]

        # Apply def_name override by relocating the entry.
        desired_def_name = self._class_to_def_name.get(cls.name, parent_key)
        if desired_def_name != parent_key:
            defs[desired_def_name] = defs.pop(parent_key)

        # Apply transforms in fixed order: pattern_properties, then
        # discriminator_enum (which appends a oneOf), then inline_class
        # (which removes the def entry entirely).
        pattern = self._class_annotation(cls, "pattern_properties", target_only=True)
        if pattern:
            self._apply_pattern_properties(class_subschema, str(pattern))

        discriminator = self._class_annotation(cls, "discriminator_enum", target_only=True)
        if discriminator:
            self._apply_discriminator_enum(class_subschema, str(discriminator))

        if cls.name in self._inline_class_names:
            self._inline_class_bodies[cls.name] = deepcopy(class_subschema)
            del defs[desired_def_name]
            if not defs:
                file_schema.pop("$defs", None)
            # Inline classes never become file roots; nothing more to do.
            return

        if cls.name in self._root_of_file_classes:
            self._promote_root_of_file(file_schema, class_subschema, desired_def_name)

    def _apply_pattern_properties(self, class_subschema: JsonSchema, pattern: str) -> None:
        """Rewrap the class body as a ``patternProperties`` map.

        The value schema is the existing properties block (``properties`` +
        ``required`` + ``additionalProperties``); the outer wrapper becomes
        an open object whose keys match ``pattern``.
        """
        value_schema = JsonSchema({"type": "object"})
        for key in ("properties", "required", "additionalProperties"):
            if key in class_subschema:
                value_schema[key] = class_subschema.pop(key)
        if "title" in class_subschema:
            value_schema.setdefault("title", class_subschema["title"])

        class_subschema["additionalProperties"] = False
        class_subschema["patternProperties"] = {pattern: value_schema}

    def _apply_discriminator_enum(self, class_subschema: JsonSchema, enum_name: str) -> None:
        enum_def = self.schemaview.get_enum(enum_name)
        if enum_def is None or not enum_def.permissible_values:
            logger.warning(
                "discriminator_enum %r references an unknown or empty enum; skipping oneOf emission",
                enum_name,
            )
            return
        keys = list(enum_def.permissible_values.keys())
        class_subschema["oneOf"] = [{"required": [k]} for k in keys]

    def _promote_root_of_file(self, file_schema: JsonSchema, class_subschema: JsonSchema, def_name: str) -> None:
        for key, value in class_subschema.items():
            # Preserve the file-level $schema, $id, title that start_schema set.
            if key in ("$schema", "$id"):
                continue
            file_schema[key] = value
        defs = file_schema.get("$defs") or {}
        defs.pop(def_name, None)
        if not defs and "$defs" in file_schema:
            del file_schema["$defs"]

    # Post-pass: cross-file $ref rewriting + inline expansion

    def _ref_target(self, ref: str) -> tuple[str | None, str, bool]:
        """Decode ``#/$defs/<key>``.

        Returns ``(class_name, bare_def_key, has_optional_suffix)``. The
        bare def key is the key stripped of the optional-identifier suffix;
        ``class_name`` is ``None`` when the ref does not target a known
        class (or is not a local ``#/$defs/`` ref at all).
        """
        if not ref.startswith("#/$defs/"):
            return None, "", False
        bare_def = ref[len("#/$defs/") :]
        suffix = JsonSchema.OPTIONAL_IDENTIFIER_SUFFIX
        has_suffix = bare_def.endswith(suffix)
        stripped = bare_def.removesuffix(suffix) if has_suffix else bare_def
        cls_name = self._parent_key_to_class.get(stripped)
        return cls_name, stripped, has_suffix

    def _emit_def_key(self, cls_name: str, has_optional_suffix: bool) -> str:
        """Compose the emitted ``$defs`` key for ``cls_name``, preserving the
        ``__identifier_optional`` suffix if the original ref carried it."""
        desired = self._class_to_def_name.get(cls_name, cls_name)
        if has_optional_suffix:
            return desired + JsonSchema.OPTIONAL_IDENTIFIER_SUFFIX
        return desired

    def _rewrite_refs(self) -> None:
        for filename, schema in self.top_level_schemas.items():
            self._walk_and_rewrite(schema, filename, frozenset())

    def _materialize_cross_file_lax_defs(self) -> None:
        """Resolve cross-file ``_lax_forward_refs``.

        The parent generator calls ``self.top_level_schema.add_lax_def(...)``
        from inside slot processing, which queues a forward ref on the
        *referrer* file rather than the file where the canonical class
        lives. We materialize each pending lax def in the canonical class's
        file so cross-file ``$ref``s land on a real entry.
        """
        suffix = JsonSchema.OPTIONAL_IDENTIFIER_SUFFIX
        for source_file, source_schema in list(self.top_level_schemas.items()):
            fwd = getattr(source_schema, "_lax_forward_refs", None)
            if not fwd:
                continue
            for canonical_name in list(fwd):
                cls_name = self._parent_key_to_class.get(canonical_name)
                if cls_name is None:
                    continue
                target_file = self._class_to_file.get(cls_name, source_file)
                target_schema = self.top_level_schemas.get(target_file)
                if target_schema is None:
                    continue
                # ``handle_class`` may have renamed the canonical def via
                # ``def_name`` — find whichever key is actually present.
                desired = self._class_to_def_name.get(cls_name, canonical_name)
                target_defs = target_schema.get("$defs") or {}
                if desired in target_defs:
                    base_key = desired
                elif canonical_name in target_defs:
                    base_key = canonical_name
                else:
                    # Canonical class isn't materialized (e.g. inline_class
                    # or is_root_of_file). Drop the forward ref silently.
                    fwd.pop(canonical_name, None)
                    continue
                identifier_name = fwd.pop(canonical_name)
                lax = deepcopy(target_defs[base_key])
                if "required" in lax and identifier_name in lax["required"]:
                    lax["required"].remove(identifier_name)
                target_schema.setdefault("$defs", JsonSchema({}))
                target_schema["$defs"][desired + suffix] = lax

    def _walk_and_rewrite(self, node: Any, current_file: str, inlining_stack: frozenset[str]) -> None:
        if isinstance(node, dict):
            ref_value = node.get("$ref")
            if isinstance(ref_value, str):
                cls_name, stripped, has_suffix = self._ref_target(ref_value)
                if cls_name is not None and cls_name in self._inline_class_names:
                    if cls_name in inlining_stack:
                        # Cycle: leave the ref alone rather than infinitely
                        # expanding. The resulting schema will be invalid,
                        # but no better answer exists for cyclic inlines.
                        logger.warning(
                            "Cyclic inline_class expansion detected at %s; leaving $ref in place",
                            ref_value,
                        )
                    else:
                        body = self._inline_class_bodies.get(cls_name)
                        if body is not None:
                            node.clear()
                            node.update(deepcopy(body))
                            # Recurse into the inlined body with the current
                            # class added to the inlining stack so cycles
                            # are detected.
                            child_stack = inlining_stack | {cls_name}
                            for value in list(node.values()):
                                self._walk_and_rewrite(value, current_file, child_stack)
                            return
                elif cls_name is not None:
                    target_file = self._class_to_file.get(cls_name)
                    if target_file and target_file != current_file:
                        if cls_name in self._root_of_file_classes:
                            # The class body lives at the file root; refs
                            # target the file (no fragment).
                            node["$ref"] = target_file
                        else:
                            emit_key = self._emit_def_key(cls_name, has_suffix)
                            node["$ref"] = f"{target_file}#/$defs/{emit_key}"
                    else:
                        # Same-file ref: rewrite to the desired def name if
                        # the class has a def_name override OR if it is a
                        # root-of-file class (refs become the empty
                        # fragment ``#``).
                        if cls_name in self._root_of_file_classes:
                            node["$ref"] = "#"
                        else:
                            emit_key = self._emit_def_key(cls_name, has_suffix)
                            if emit_key != (stripped + (JsonSchema.OPTIONAL_IDENTIFIER_SUFFIX if has_suffix else "")):
                                node["$ref"] = f"#/$defs/{emit_key}"
            for value in list(node.values()):
                self._walk_and_rewrite(value, current_file, inlining_stack)
        elif isinstance(node, list):
            for item in node:
                self._walk_and_rewrite(item, current_file, inlining_stack)

    # Property naming: kebab-case support

    def aliased_slot_name(self, slot) -> str:
        style = self._property_name_style()
        if style != "kebab_case":
            return super().aliased_slot_name(slot)

        # Resolve to a SlotDefinition so aliases are accessible.
        slot_def = slot
        if isinstance(slot, str):
            slot_def = self.schemaview.get_slot(slot)
        aliases = getattr(slot_def, "aliases", None) or []
        for alias in aliases:
            if "-" in alias:
                return alias
        base = super().aliased_slot_name(slot)
        return underscore(base).replace("_", "-")

    # additionalProperties fallback

    def get_additional_properties(self, cls: ClassDefinition):
        if not getattr(cls, "extra_slots", None):
            override = _coerce_bool(self._class_annotation(cls, "additional_properties"))
            if override is not None:
                return override
        return super().get_additional_properties(cls)

    # Top-level orchestration

    def generate(self) -> dict[str, JsonSchema]:  # type: ignore[override]
        self._build_class_lookups()
        self.schema = self.before_generate_schema(self.schema, self.schemaview)
        self.start_schema()

        all_enums = self.before_generate_enums(self.schemaview.all_enums().values(), self.schemaview)
        # Enums are routed to the default file. Per-file enum routing is a
        # straightforward future extension via a class-style annotation on
        # ``EnumDefinition``; not in scope for the initial contract.
        default_schema = self.top_level_schemas[self._get_default_filename()]
        previous = self.top_level_schema
        self.top_level_schema = default_schema
        try:
            for enum_definition in all_enums:
                self.handle_enum(enum_definition)
        finally:
            self.top_level_schema = previous

        all_classes = self.before_generate_classes(self.schemaview.all_classes().values(), self.schemaview)
        for class_definition in all_classes:
            self.handle_class(class_definition)

        self._materialize_cross_file_lax_defs()
        self._rewrite_refs()

        # Apply the after_generate_schema lifecycle hook to each per-file
        # schema so downstream consumers can post-process individual files.
        for filename, schema in list(self.top_level_schemas.items()):
            result = self.after_generate_schema(
                SchemaResult.model_construct(schema_=schema, source=self.schema),
                self.schemaview,
            )
            self.top_level_schemas[filename] = result.schema_

        return self.top_level_schemas

    def serialize(self, **kwargs) -> str:  # type: ignore[override]
        if self.materialize_patterns:
            logger.info("Materializing patterns in the schema before serialization")
            self.schemaview.materialize_patterns()

        manifest = self.generate()
        indent = self.indent if self.indent and self.indent > 0 else None

        if self.output_dir:
            output_path = Path(self.output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            written: list[str] = []
            for filename, schema in sorted(manifest.items()):
                target = output_path / filename
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(
                    schema.to_json(sort_keys=True, indent=indent).rstrip() + "\n",
                    encoding="utf-8",
                )
                written.append(str(target))
            return "\n".join(written) + "\n"

        # No output_dir: emit a single JSON document mapping filename to its
        # JSON-Schema body. This keeps the CLI ``print(serialize())`` pattern
        # working without an output directory.
        return (
            json.dumps(
                {fn: dict(schema) for fn, schema in sorted(manifest.items())},
                sort_keys=True,
                indent=indent,
            ).rstrip()
            + "\n"
        )


@shared_arguments(MultiFileJsonSchemaGenerator)
@click.command(name="gen-multifile-json-schema")
@click.option(
    "-t",
    "--top-class",
    help=(
        "Top level class; slots of this class will become top level properties "
        "in the JSON Schema for the file the class lives in. Prefer the "
        "`jsonschema:is_root_of_file` annotation for multi-file output."
    ),
)
@click.option(
    "--not-closed/--closed",
    default=True,
    show_default=True,
    help="Set additionalProperties=False if closed otherwise true if not closed at the global level",
)
@click.option(
    "--include-range-class-descendants/--no-range-class-descendants",
    default=False,
    show_default=False,
    help=(
        "When handling range constraints, include all descendants of the range class instead of just the range class"
    ),
)
@click.option(
    "--indent",
    default=4,
    show_default=True,
    help=(
        "If positive, the resulting JSON will be pretty-printed with that indent level. "
        "Set to 0 to disable pretty-printing and return the most compact JSON representation."
    ),
)
@click.option(
    "--title-from",
    type=click.Choice(["name", "title"], case_sensitive=False),
    default="name",
    help="Specify from which slot are JSON Schema 'title' annotations generated.",
)
@click.option(
    "--materialize-patterns/--no-materialize-patterns",
    default=True,
    show_default=True,
    help="If set, patterns will be materialized in the generated JSON Schema.",
)
@click.option(
    "--preserve-names/--normalize-names",
    default=False,
    show_default=True,
    help=(
        "Preserve original LinkML names in JSON Schema output (e.g., for $defs, properties, "
        "$ref targets). Implied by schema-level `property_name_style: kebab_case`."
    ),
)
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True),
    default=None,
    help=(
        "Directory to write one JSON Schema file per `output_file` bucket. "
        "If omitted, a single JSON document mapping filename to schema is printed to stdout."
    ),
)
@click.option(
    "--default-file",
    default="schema.json",
    show_default=True,
    help=(
        "Output filename used for classes that lack an `output_file` annotation. "
        "Stems without a `.` get `.json` appended."
    ),
)
@click.option(
    "--split-file-annotation",
    default="output_file",
    show_default=True,
    help=(
        "Tier 1 class annotation key used for file routing. The Tier 2 form "
        "`jsonschema:<key>` always wins when present."
    ),
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate one or more JSON Schema documents from a LinkML model.

    Classes are partitioned across output files using class-level
    annotations on the source schema; see the module docstring for the
    annotation contract.
    """
    print(MultiFileJsonSchemaGenerator(yamlfile, **kwargs).serialize(**kwargs))


if __name__ == "__main__":
    cli()
