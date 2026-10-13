"""
Tests for :class:`.MultiFileJsonSchemaGenerator`.

These tests are intentionally self-contained. Every annotation
in the public contract is exercised at least once.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from linkml.generators.multifilejsonschemagen import (
    MultiFileJsonSchemaGenerator,
    cli,
)

pytestmark = pytest.mark.multifilejsonschemagen


SCHEMA_YAML = """
id: https://example.org/multifile-demo
name: multifile_demo
title: Multi-file JSON Schema demo
description: Synthetic schema exercising the multi-file generator contract.

annotations:
  property_name_style: kebab_case

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/

default_prefix: ex
default_range: string

imports:
  - linkml:types

enums:
  ColorKind:
    permissible_values:
      red:
      blue:

  ChoiceKind:
    permissible_values:
      first-choice:
      second-choice:

classes:

  Foo:
    annotations:
      output_file: foo
      jsonschema:is_root_of_file: true
    attributes:
      unique_id:
        aliases:
          - unique-id
        identifier: true
      bar_ref:
        range: Bar

  Bar:
    annotations:
      output_file: bar
      jsonschema:def_name: bar-entry
    attributes:
      label:
        required: true
      color:
        range: ColorKind
      choice:
        range: Choice

  Choice:
    annotations:
      output_file: bar
      inline_class: "true"
      jsonschema:discriminator_enum: ChoiceKind
    attributes:
      first-choice:
        range: string
      second-choice:
        range: string

  ControlsBlock:
    annotations:
      output_file: controls
      jsonschema:pattern_properties: "^[a-z][a-z0-9-]*$"
    attributes:
      enabled:
        range: boolean
        required: true
      level:
        range: integer

  OpenBag:
    annotations:
      output_file: foo
      additional_properties: "true"
    attributes:
      tag:
        range: string
"""


@pytest.fixture
def schema_path(tmp_path: Path) -> str:
    path = tmp_path / "multifile_demo.yaml"
    path.write_text(SCHEMA_YAML, encoding="utf-8")
    return str(path)


@pytest.fixture
def manifest(schema_path: str) -> dict[str, dict]:
    generator = MultiFileJsonSchemaGenerator(schema_path, not_closed=False)
    rendered = generator.serialize()
    # serialize() without output_dir returns a JSON object mapping
    # filename -> schema body.
    return json.loads(rendered)


def test_file_partitioning(manifest):
    assert set(manifest) == {"foo.json", "bar.json", "controls.json", "schema.json"}


def test_default_file_present_even_when_unused(manifest):
    """The default file is always materialized; an empty default is fine
    because un-annotated classes (none here) would land there."""
    default = manifest["schema.json"]
    assert default["$schema"].startswith("https://json-schema.org/")
    assert default["$id"].endswith("schema.json")


def test_per_file_schema_id(manifest):
    assert manifest["foo.json"]["$id"].endswith("/foo.json")
    assert manifest["bar.json"]["$id"].endswith("/bar.json")


def test_is_root_of_file_promotes_body(manifest):
    """`is_root_of_file: true` on Foo means Foo's body lives at the file
    root and no $defs entry is emitted for it in foo.json."""
    foo = manifest["foo.json"]
    assert foo["type"] == "object"
    assert "properties" in foo
    assert "unique-id" in foo["properties"]
    if "$defs" in foo:
        assert "Foo" not in foo["$defs"]


def test_kebab_case_property_names(manifest):
    """Schema-level `property_name_style: kebab_case` produces hyphenated
    property names, using the first hyphen-containing alias when available."""
    foo = manifest["foo.json"]
    assert "unique-id" in foo["properties"]
    assert "unique_id" not in foo["properties"]
    # Slot without an explicit hyphen alias gets converted via snake→kebab.
    assert "bar-ref" in foo["properties"]


def test_cross_file_ref_quoting(manifest):
    """Foo.bar_ref ranges Bar in bar.json — the $ref must include the file.

    Optional slots are wrapped in an ``anyOf: [{$ref}, {type: null}]`` by
    :class:`.JsonSchemaGenerator`; the ref still lives inside the anyOf.
    """
    foo = manifest["foo.json"]
    slot = foo["properties"]["bar-ref"]
    candidates = [slot, *slot.get("anyOf", [])]
    refs = [c["$ref"] for c in candidates if isinstance(c, dict) and "$ref" in c]
    # def_name override renames the bar entry to ``bar-entry``.
    assert "bar.json#/$defs/bar-entry" in refs


def test_def_name_override(manifest):
    """Bar has `def_name: bar-entry`; the $defs key in bar.json is renamed
    accordingly, and same-file refs follow."""
    bar_file = manifest["bar.json"]
    assert "bar-entry" in bar_file["$defs"]
    assert "Bar" not in bar_file["$defs"]


def test_pattern_properties_transform(manifest):
    """ControlsBlock's body is rewrapped as a patternProperties map."""
    controls_file = manifest["controls.json"]
    controls = controls_file["$defs"]["ControlsBlock"]
    assert "patternProperties" in controls
    assert "properties" not in controls
    inner = controls["patternProperties"]["^[a-z][a-z0-9-]*$"]
    assert inner["type"] == "object"
    assert set(inner["properties"]) == {"enabled", "level"}
    assert inner["required"] == ["enabled"]
    assert controls["additionalProperties"] is False


def test_inline_class_has_no_def_entry(manifest):
    """Choice is `inline_class: true` and must not appear in $defs anywhere."""
    for filename, schema in manifest.items():
        defs = schema.get("$defs", {})
        assert "Choice" not in defs, f"Choice leaked into $defs of {filename}"


def test_inline_class_body_expanded_in_referers(manifest):
    """Bar.choice ranges Choice; the slot's subschema must be the inlined
    Choice body, not a $ref."""
    bar_file = manifest["bar.json"]
    bar = bar_file["$defs"]["bar-entry"]
    choice_slot = bar["properties"]["choice"]
    # The slot may carry anyOf/null wrapping. Find the inlined body.
    candidates = [choice_slot]
    if "anyOf" in choice_slot:
        candidates.extend(choice_slot["anyOf"])
    bodies = [c for c in candidates if isinstance(c, dict) and "oneOf" in c]
    assert bodies, f"inlined Choice body not found in {choice_slot}"
    body = bodies[0]
    assert body["oneOf"] == [
        {"required": ["first-choice"]},
        {"required": ["second-choice"]},
    ]
    # No $ref to Choice anywhere on the slot.
    assert "$ref" not in choice_slot
    if "anyOf" in choice_slot:
        for branch in choice_slot["anyOf"]:
            assert "$ref" not in branch or "Choice" not in branch.get("$ref", "")


def test_discriminator_enum_oneof_keys(manifest):
    """The inlined Choice body keeps the discriminator oneOf from the
    `discriminator_enum: ChoiceKind` annotation."""
    bar = manifest["bar.json"]["$defs"]["bar-entry"]
    choice_slot = bar["properties"]["choice"]
    candidates = [choice_slot, *choice_slot.get("anyOf", [])]
    body = next(c for c in candidates if isinstance(c, dict) and "oneOf" in c)
    keys = sorted(item["required"][0] for item in body["oneOf"])
    assert keys == ["first-choice", "second-choice"]


def test_additional_properties_annotation_fallback(manifest):
    """OpenBag uses the `additional_properties: true` annotation in lieu of
    `extra_slots.allowed`."""
    foo = manifest["foo.json"]
    open_bag = foo["$defs"]["OpenBag"]
    assert open_bag["additionalProperties"] is True


def test_split_file_annotation_override(tmp_path: Path):
    """Re-annotating the schema with `meta_file:` and passing
    `--split-file-annotation meta_file` produces identical routing."""
    renamed = SCHEMA_YAML.replace("output_file:", "meta_file:")
    schema_file = tmp_path / "renamed.yaml"
    schema_file.write_text(renamed, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False, split_file_annotation="meta_file")
    manifest = json.loads(gen.serialize())
    assert set(manifest) == {"foo.json", "bar.json", "controls.json", "schema.json"}


def test_writes_files_when_output_dir_set(schema_path: str, tmp_path: Path):
    out_dir = tmp_path / "out"
    gen = MultiFileJsonSchemaGenerator(schema_path, not_closed=False, output_dir=str(out_dir))
    gen.serialize()
    written = sorted(p.name for p in out_dir.glob("*.json"))
    assert written == ["bar.json", "controls.json", "foo.json", "schema.json"]
    # Files must be parseable JSON.
    for path in out_dir.glob("*.json"):
        json.loads(path.read_text(encoding="utf-8"))


def test_cli_smoke(schema_path: str, tmp_path: Path):
    out_dir = tmp_path / "cli-out"
    runner = CliRunner()
    result = runner.invoke(
        cli,
        [
            "--output-dir",
            str(out_dir),
            "--not-closed/--closed",
            schema_path,
        ],
    )
    # If the boolean flag form above isn't accepted by click in this
    # version, retry with the standalone flag.
    if result.exit_code != 0:
        result = runner.invoke(cli, ["--output-dir", str(out_dir), "--closed", schema_path])
    assert result.exit_code == 0, result.output
    assert (out_dir / "foo.json").exists()
    assert (out_dir / "bar.json").exists()
    assert (out_dir / "controls.json").exists()


# Audit-driven regression tests


CROSS_FILE_ROOT_SCHEMA = """
id: https://example.org/cross-file-root
name: cross_file_root
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Root:
    annotations:
      output_file: root
      jsonschema:is_root_of_file: true
    attributes:
      label:
        required: true
      sibling:
        range: Sibling

  Sibling:
    annotations:
      output_file: root
    attributes:
      back_ref:
        range: Root
      name:
        required: true

  Outsider:
    annotations:
      output_file: outsider
    attributes:
      root_ref:
        range: Root
        required: true
"""


def test_cross_file_ref_to_root_of_file_class(tmp_path: Path):
    """Refs from another file to an is_root_of_file class must point to the
    file itself (no ``#/$defs/...`` fragment), since the class body lives
    at the file root.
    """
    schema_file = tmp_path / "cfrs.yaml"
    schema_file.write_text(CROSS_FILE_ROOT_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    outsider = manifest["outsider.json"]["$defs"]["Outsider"]
    slot = outsider["properties"]["root_ref"]
    # Required slot — should be a direct $ref, not wrapped in anyOf.
    candidates = [slot, *slot.get("anyOf", [])]
    refs = [c["$ref"] for c in candidates if isinstance(c, dict) and "$ref" in c]
    assert "root.json" in refs, f"expected cross-file root ref to be 'root.json' (no fragment); got {refs}"


def test_same_file_ref_to_root_of_file_class(tmp_path: Path):
    """Same-file refs to an is_root_of_file class become the bare ``#``
    fragment (the file root), since the class has no $defs entry."""
    schema_file = tmp_path / "cfrs.yaml"
    schema_file.write_text(CROSS_FILE_ROOT_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    sibling = manifest["root.json"]["$defs"]["Sibling"]
    slot = sibling["properties"]["back_ref"]
    candidates = [slot, *slot.get("anyOf", [])]
    refs = [c["$ref"] for c in candidates if isinstance(c, dict) and "$ref" in c]
    assert "#" in refs, f"expected same-file root-of-file ref to be '#'; got {refs}"


IDENTIFIER_OPTIONAL_SCHEMA = """
id: https://example.org/ident-opt
name: ident_opt
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Anchor:
    annotations:
      output_file: anchor
    attributes:
      anchor_id:
        identifier: true
      label:
        required: true

  Referrer:
    annotations:
      output_file: referrer
    attributes:
      referrer_id:
        identifier: true
      anchors:
        range: Anchor
        inlined: true
        multivalued: true
"""


def test_optional_identifier_suffix_preserved_across_files(tmp_path: Path):
    """Cross-file refs that target the ``__identifier_optional`` lax variant
    must preserve the suffix on the rewritten ref. This guards against the
    historical ``rstrip(suffix)`` bug, which would silently mangle keys
    whose characters overlap with the suffix charset.
    """
    schema_file = tmp_path / "io.yaml"
    schema_file.write_text(IDENTIFIER_OPTIONAL_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    # Inlined multivalued ranges with identifiers produce a lax def under
    # ``Anchor__identifier_optional`` in the *target* file, and the
    # additionalProperties on the inlined dict $refs that lax def. After
    # cross-file rewriting, the ref must point at
    # ``anchor.json#/$defs/Anchor__identifier_optional`` with the suffix
    # intact.
    anchor_file = manifest["anchor.json"]
    assert "Anchor__identifier_optional" in anchor_file["$defs"], (
        f"lax def missing from anchor.json: keys={list(anchor_file['$defs'])}"
    )

    referrer = manifest["referrer.json"]["$defs"]["Referrer"]
    anchors_slot = referrer["properties"]["anchors"]

    # Walk the slot's subtree and collect every $ref pointing at anchor.json.
    refs: list[str] = []

    def collect(node):
        if isinstance(node, dict):
            r = node.get("$ref")
            if isinstance(r, str):
                refs.append(r)
            for v in node.values():
                collect(v)
        elif isinstance(node, list):
            for item in node:
                collect(item)

    collect(anchors_slot)
    anchor_refs = [r for r in refs if r.startswith("anchor.json")]
    assert anchor_refs, f"no anchor.json refs in slot subtree: {refs}"
    assert any(r == "anchor.json#/$defs/Anchor__identifier_optional" for r in anchor_refs), (
        f"expected lax-variant suffix preserved on cross-file ref; got: {anchor_refs}"
    )


UNANNOTATED_SCHEMA = """
id: https://example.org/unannotated
name: unannotated
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Loose:
    attributes:
      name:
        required: true
"""


def test_unannotated_classes_land_in_default_file(tmp_path: Path):
    """Classes without a ``source_file`` annotation belong in
    ``--default-file`` (default: ``schema.json``)."""
    schema_file = tmp_path / "u.yaml"
    schema_file.write_text(UNANNOTATED_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False, default_file="my-default.json")
    manifest = json.loads(gen.serialize())
    assert set(manifest) == {"my-default.json"}
    assert "Loose" in manifest["my-default.json"]["$defs"]


ADDITIONAL_PROPS_FALSE_SCHEMA = """
id: https://example.org/apfalse
name: apfalse
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Strict:
    annotations:
      additional_properties: "false"
    attributes:
      name:
        required: true
"""


def test_additional_properties_false_annotation(tmp_path: Path):
    """``additional_properties: false`` annotation closes the class even
    when the global ``--not-closed`` default would leave it open."""
    schema_file = tmp_path / "ap.yaml"
    schema_file.write_text(ADDITIONAL_PROPS_FALSE_SCHEMA, encoding="utf-8")
    # Use the open default (not_closed=True) so the annotation's effect is
    # observable.
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=True)
    manifest = json.loads(gen.serialize())
    strict = manifest["schema.json"]["$defs"]["Strict"]
    assert strict["additionalProperties"] is False


def test_generate_returns_dict_of_jsonschema(tmp_path: Path):
    """``generate()`` is the programmatic API — it must return a mapping
    from filename to a ``JsonSchema`` instance (not a JSON string)."""
    schema_file = tmp_path / "g.yaml"
    schema_file.write_text(UNANNOTATED_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    result = gen.generate()
    assert isinstance(result, dict)
    assert set(result) == {"schema.json"}
    # JsonSchema is a dict subclass; the key check is that we get a
    # subscriptable mapping with the expected structure.
    assert "$schema" in result["schema.json"]
    assert "$defs" in result["schema.json"]


INLINE_CYCLE_SCHEMA = """
id: https://example.org/cycle
name: cycle
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Holder:
    annotations:
      output_file: cycle
    attributes:
      a:
        range: A

  A:
    annotations:
      output_file: cycle
      inline_class: "true"
    attributes:
      to_b:
        range: B

  B:
    annotations:
      output_file: cycle
      inline_class: "true"
    attributes:
      to_a:
        range: A
"""


def test_inline_class_cycle_does_not_infinite_recurse(tmp_path: Path, caplog):
    """A→B→A inline cycle must terminate (and log a warning) rather than
    blow the stack."""
    schema_file = tmp_path / "c.yaml"
    schema_file.write_text(INLINE_CYCLE_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    with caplog.at_level("WARNING"):
        manifest = json.loads(gen.serialize())
    # The serialize call returned — no recursion blow-up.
    assert "cycle.json" in manifest
    # The cycle guard should have logged at least once.
    assert any("Cyclic inline_class" in rec.message for rec in caplog.records)


# ---------------------------------------------------------------------------
# Parity tests vs. parent JsonSchemaGenerator coverage
# ---------------------------------------------------------------------------


CROSS_FILE_INHERITANCE_SCHEMA = """
id: https://example.org/inherit
name: inherit
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Animal:
    annotations:
      output_file: animals
    abstract: true
    attributes:
      name:
        required: true
      species:
        range: string

  Dog:
    is_a: Animal
    annotations:
      output_file: animals
    attributes:
      breed:
        range: string

  Cat:
    is_a: Animal
    annotations:
      output_file: animals
    attributes:
      indoor:
        range: boolean

  Owner:
    annotations:
      output_file: owners
    attributes:
      pet:
        range: Animal
        inlined: true
"""


def test_cross_file_inheritance_rolldown(tmp_path: Path):
    """JSON Schema has no inheritance — inherited slots must be rolled down
    onto every subclass even when the parent class lives in the same file.
    This is the parent generator's behavior; the multi-file generator must
    not regress it.
    """
    schema_file = tmp_path / "inherit.yaml"
    schema_file.write_text(CROSS_FILE_INHERITANCE_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    animals = manifest["animals.json"]["$defs"]
    # Inherited `name` and `species` must appear on Dog and Cat.
    assert {"name", "species", "breed"} <= set(animals["Dog"]["properties"])
    assert {"name", "species", "indoor"} <= set(animals["Cat"]["properties"])
    assert animals["Dog"]["required"] == ["name"]
    assert animals["Cat"]["required"] == ["name"]


def test_cross_file_descendant_anyof(tmp_path: Path):
    """With ``include_range_class_descendants=True``, a slot ranging an
    abstract parent emits an ``anyOf`` of ``$ref``s to every descendant.
    When the descendants live in a different file than the slot's owner,
    every ref in the ``anyOf`` must be cross-file rewritten."""
    schema_file = tmp_path / "inherit.yaml"
    schema_file.write_text(CROSS_FILE_INHERITANCE_SCHEMA, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False, include_range_class_descendants=True)
    manifest = json.loads(gen.serialize())

    owner = manifest["owners.json"]["$defs"]["Owner"]
    pet_slot = owner["properties"]["pet"]
    # Walk the slot tree and collect every $ref.
    refs: list[str] = []

    def collect(node):
        if isinstance(node, dict):
            r = node.get("$ref")
            if isinstance(r, str):
                refs.append(r)
            for v in node.values():
                collect(v)
        elif isinstance(node, list):
            for item in node:
                collect(item)

    collect(pet_slot)
    # Every descendant ref must point at animals.json — none can be a
    # bare ``#/$defs/...`` (which would be a dangling same-file ref).
    assert refs, f"no $refs in pet slot subtree: {pet_slot}"
    for r in refs:
        assert r.startswith("animals.json#/$defs/"), f"descendant ref not cross-file rewritten: {r}"


def test_lifecycle_hooks_invoked_across_files(tmp_path: Path):
    """``before_generate_class`` / ``after_generate_class`` /
    ``before_generate_class_slot`` must fire for every class regardless of
    which file it lands in."""
    from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition
    from linkml_runtime.utils.schemaview import SchemaView

    seen: dict[str, list[str]] = {
        "before_class": [],
        "after_class": [],
        "before_slot": [],
    }

    class TracingGen(MultiFileJsonSchemaGenerator):
        def before_generate_class(self, cls: ClassDefinition, sv: SchemaView):
            seen["before_class"].append(cls.name)
            return cls

        def after_generate_class(self, cls, sv: SchemaView):
            seen["after_class"].append(cls.source.name)
            return cls

        def before_generate_class_slot(self, slot: SlotDefinition, cls, sv: SchemaView) -> SlotDefinition:
            seen["before_slot"].append(f"{cls.name}.{slot.name}")
            return slot

    schema_file = tmp_path / "inherit.yaml"
    schema_file.write_text(CROSS_FILE_INHERITANCE_SCHEMA, encoding="utf-8")
    gen = TracingGen(str(schema_file), not_closed=False)
    gen.serialize()

    assert {"Animal", "Dog", "Cat", "Owner"} <= set(seen["before_class"])
    assert {"Animal", "Dog", "Cat", "Owner"} <= set(seen["after_class"])
    # Owner.pet (cross-file slot) was visited.
    assert "Owner.pet" in seen["before_slot"]


def test_nullable_optional_cross_file_ref_preserved(tmp_path: Path):
    """Optional slots ranging a class in another file produce
    ``anyOf: [{$ref}, {type: null}]``. The ref must be cross-file rewritten
    while the ``{type: null}`` companion is preserved untouched.
    """
    schema_file = tmp_path / "demo.yaml"
    schema_file.write_text(SCHEMA_YAML, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    # Foo.bar_ref ranges Bar (in bar.json), is optional → anyOf wrapping.
    foo = manifest["foo.json"]
    slot = foo["properties"]["bar-ref"]
    assert "anyOf" in slot, f"expected anyOf wrapping for optional ref; got {slot}"
    branches = slot["anyOf"]
    assert {"type": "null"} in branches, f"null branch lost during $ref rewriting: {branches}"
    refs = [b["$ref"] for b in branches if isinstance(b, dict) and "$ref" in b]
    assert "bar.json#/$defs/bar-entry" in refs


def test_value_constraints_pass_through(tmp_path: Path):
    """``equals_string``, ``pattern``, ``minimum_value``, ``maximum_value``
    on a slot must survive into the per-file ``$defs`` body unchanged.
    """
    constraints_schema = """
id: https://example.org/vc
name: vc
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Constrained:
    annotations:
      output_file: c
    attributes:
      code:
        range: string
        pattern: '^[A-Z]{3}$'
        required: true
      score:
        range: integer
        minimum_value: 0
        maximum_value: 100
"""
    schema_file = tmp_path / "vc.yaml"
    schema_file.write_text(constraints_schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    constrained = manifest["c.json"]["$defs"]["Constrained"]["properties"]
    assert constrained["code"]["pattern"] == "^[A-Z]{3}$"
    # ``minimum`` / ``maximum`` are emitted on numeric slot subschemas.
    score = constrained["score"]
    # Optional slots may be wrapped in ``anyOf``; collect candidates.
    candidates = [score, *score.get("anyOf", [])]
    mins = [c.get("minimum") for c in candidates if isinstance(c, dict)]
    maxes = [c.get("maximum") for c in candidates if isinstance(c, dict)]
    assert 0 in mins
    assert 100 in maxes


def test_class_rules_pass_through(tmp_path: Path):
    """Class-level ``rules`` emit ``allOf: [{if: ..., then: ...}]`` on the
    class subschema. This is local to the class body and must survive
    multi-file partitioning unchanged.
    """
    rules_schema = """
id: https://example.org/rl
name: rl
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  RuleHaver:
    annotations:
      output_file: r
    attributes:
      kind:
        range: string
      detail:
        range: string
    rules:
      - preconditions:
          slot_conditions:
            kind:
              equals_string: special
        postconditions:
          slot_conditions:
            detail:
              required: true
"""
    schema_file = tmp_path / "rl.yaml"
    schema_file.write_text(rules_schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    body = manifest["r.json"]["$defs"]["RuleHaver"]
    # A single rule lands at the class body's top level as ``if``/``then``;
    # multiple rules would be combined under ``allOf``. The contract for
    # this test is that the rule survives partitioning at all.
    if "allOf" in body:
        branch = body["allOf"][0]
    else:
        branch = body
    assert "if" in branch and "then" in branch, f"rule not emitted on class body: keys={list(body)}"


def test_preserve_names_implied_by_kebab_case(tmp_path: Path):
    """``property_name_style: kebab_case`` implies ``preserve_names=True`` so
    LinkML class names with non-camel patterns are not normalized."""
    pname_schema = """
id: https://example.org/pn
name: pn
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

annotations:
  property_name_style: kebab_case

classes:
  my_class:
    annotations:
      output_file: mc
    attributes:
      some_slot:
        range: string
"""
    schema_file = tmp_path / "pn.yaml"
    schema_file.write_text(pname_schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())
    defs = manifest["mc.json"]["$defs"]
    # Raw LinkML name retained (no camelcasing).
    assert "my_class" in defs
    assert "MyClass" not in defs


def test_cross_file_lax_def_missing_required(tmp_path: Path):
    """Regression: ``_materialize_cross_file_lax_defs`` must not crash when
    the canonical class def has no ``required`` field.

    Mirrors the parent ``test_add_lax_def_missing_required`` regression
    (https://github.com/linkml/linkml/issues/3366) for the cross-file path.
    """
    # Anchor has only an identifier with no other required slots →
    # ``required`` is ``["anchor_id"]``; after the lax pass it becomes ``[]``
    # then is removed. Then Referrer triggers cross-file lax materialization.
    schema = """
id: https://example.org/lax
name: lax
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Anchor:
    annotations:
      output_file: anchor
    attributes:
      anchor_id:
        identifier: true

  Referrer:
    annotations:
      output_file: referrer
    attributes:
      anchors:
        range: Anchor
        inlined: true
        multivalued: true
"""
    schema_file = tmp_path / "lax.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    # Must not raise.
    manifest = json.loads(gen.serialize())
    lax_key = "Anchor__identifier_optional"
    assert lax_key in manifest["anchor.json"]["$defs"]
    lax_body = manifest["anchor.json"]["$defs"][lax_key]
    # anchor_id was the only required slot; after lax pass, ``required``
    # is either absent or empty.
    assert "required" not in lax_body or lax_body["required"] == []


def test_mergeimports_routes_imported_classes(tmp_path: Path):
    """When ``mergeimports=True``, imported classes participate in the
    iteration. Without ``imports=True`` in the lookup pass, those classes
    would have no entry in ``_class_to_file`` and their ``$ref``s would
    never be cross-file rewritten.

    This is a regression guard for the ``imports=False`` bug fixed in the
    audit pass.
    """
    # Imported schema providing a class with a source_file annotation.
    imported = tmp_path / "imported.yaml"
    imported.write_text(
        """
id: https://example.org/imported
name: imported
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Imported:
    annotations:
      output_file: imported
    attributes:
      label:
        required: true
""",
        encoding="utf-8",
    )

    main = tmp_path / "main.yaml"
    main.write_text(
        """
id: https://example.org/main
name: main
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types
  - imported

classes:
  Local:
    annotations:
      output_file: local
    attributes:
      ref_to_imported:
        range: Imported
""",
        encoding="utf-8",
    )

    gen = MultiFileJsonSchemaGenerator(str(main), not_closed=False, mergeimports=True)
    manifest = json.loads(gen.serialize())

    # The imported class must land in its annotated file, not default_file.
    assert "Imported" in manifest["imported.json"]["$defs"]
    # The cross-file ref from Local to Imported must be rewritten.
    local = manifest["local.json"]["$defs"]["Local"]
    slot = local["properties"]["ref_to_imported"]
    candidates = [slot, *slot.get("anyOf", [])]
    refs = [c["$ref"] for c in candidates if isinstance(c, dict) and "$ref" in c]
    assert any(r.startswith("imported.json#/$defs/") for r in refs), refs


# ---------------------------------------------------------------------------
# Tiered annotation contract tests
# ---------------------------------------------------------------------------


def test_output_file_stem_appends_json_extension(tmp_path: Path):
    """Tier 1 ``output_file: <stem>`` (no ``.``) must be normalized by
    appending ``.json``. This is what lets the same annotated schema drive
    multi-file generators for other targets (Pydantic → ``.py``, etc.).
    """
    schema = """
id: https://example.org/stem
name: stem
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Stemmed:
    annotations:
      output_file: stemmed
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "s.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())
    assert "stemmed.json" in manifest, list(manifest)
    assert "Stemmed" in manifest["stemmed.json"]["$defs"]


def test_output_file_with_extension_passes_through(tmp_path: Path):
    """Values containing a ``.`` are full filenames and pass through
    verbatim — the escape hatch for explicit overrides."""
    schema = """
id: https://example.org/full
name: full
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Explicit:
    annotations:
      output_file: explicit.alt.json
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "f.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())
    assert "explicit.alt.json" in manifest, list(manifest)


def test_target_override_wins_over_generic(tmp_path: Path):
    """Tier 2 (``jsonschema:<key>``) must take precedence over Tier 1
    (``<key>``) when both are present on the same class. Here, the
    generic value says "do not inline" and the JSON-specific override
    says "inline" — JSON gen must honor the override.
    """
    schema = """
id: https://example.org/ov
name: ov
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Holder:
    annotations:
      output_file: ov
    attributes:
      child:
        range: Child

  Child:
    annotations:
      output_file: ov
      inline_class: "false"
      jsonschema:inline_class: "true"
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "o.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    # Child was inlined → no $defs entry anywhere.
    for filename, schema_body in manifest.items():
        defs = schema_body.get("$defs", {})
        assert "Child" not in defs, f"Child leaked into $defs of {filename}"

    # Holder.child slot is the inlined Child body, not a $ref.
    holder = manifest["ov.json"]["$defs"]["Holder"]
    child_slot = holder["properties"]["child"]
    candidates = [child_slot, *child_slot.get("anyOf", [])]
    refs = [c.get("$ref") for c in candidates if isinstance(c, dict)]
    assert not any(r and "Child" in r for r in refs), f"Child should be inlined, not referenced: {refs}"
    # The inlined body shows ``label`` as a required property.
    bodies = [c for c in candidates if isinstance(c, dict) and "properties" in c]
    assert bodies, f"inlined Child body not found: {child_slot}"
    assert "label" in bodies[0]["properties"]


def test_target_only_annotation_ignored_without_prefix(tmp_path: Path):
    """Tier 2-only tags (e.g. ``is_root_of_file``) have no Tier 1 form by
    design. Writing them without the ``jsonschema:`` prefix should be a
    no-op — the class must NOT be promoted to file root.
    """
    schema = """
id: https://example.org/to
name: to
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

classes:
  Mistyped:
    annotations:
      output_file: m
      is_root_of_file: true   # WRONG TIER — should be jsonschema:is_root_of_file
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "to.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    m = manifest["m.json"]
    # Body NOT promoted: the file has a $defs entry for Mistyped, no
    # top-level ``properties``.
    assert "Mistyped" in m.get("$defs", {})
    assert "properties" not in m


# ---------------------------------------------------------------------------
# Subset-driven defaults (DRY layer)
# ---------------------------------------------------------------------------


def test_subset_provides_output_file_routing(tmp_path: Path):
    """A subset declaration carrying ``output_file`` routes every class in
    ``in_subset: [<that-subset>]`` to the same file without the class
    needing its own annotation. This is the DRY win that motivates
    subset-level resolution.
    """
    schema = """
id: https://example.org/ss-route
name: ss_route
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  core:
    description: Core entities
    annotations:
      output_file: core

classes:
  Alpha:
    in_subset: [core]
    attributes:
      name:
        required: true
  Beta:
    in_subset: [core]
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "ss.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    assert "core.json" in manifest
    assert {"Alpha", "Beta"} <= set(manifest["core.json"]["$defs"])


def test_subset_provides_tier2_annotation(tmp_path: Path):
    """Tier 2 (``jsonschema:<key>``) annotations on a subset must be
    honored by every member class. Here, the subset declares
    ``jsonschema:is_root_of_file: true`` and the member class must be
    promoted to its file root."""
    schema = """
id: https://example.org/ss-t2
name: ss_t2
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  root_bucket:
    annotations:
      output_file: root
      jsonschema:is_root_of_file: true

classes:
  Root:
    in_subset: [root_bucket]
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "ss2.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    root_file = manifest["root.json"]
    # is_root_of_file promotion: body lives at file root, no $defs entry.
    assert "properties" in root_file
    assert "label" in root_file["properties"]
    assert "Root" not in root_file.get("$defs", {})


def test_class_annotation_overrides_subset(tmp_path: Path):
    """A class-level annotation must override the subset-level value for
    the same key. This is the escape hatch for one-off classes in an
    otherwise-uniform subset."""
    schema = """
id: https://example.org/ss-ov
name: ss_ov
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  bulk:
    annotations:
      output_file: bulk

classes:
  Normal:
    in_subset: [bulk]
    attributes:
      label:
        required: true
  Oddball:
    in_subset: [bulk]
    annotations:
      output_file: special    # class-level override
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "ss3.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    assert "Normal" in manifest["bulk.json"]["$defs"]
    assert "Oddball" in manifest["special.json"]["$defs"]
    assert "Oddball" not in manifest["bulk.json"]["$defs"]


def test_multi_subset_agreement_does_not_raise(tmp_path: Path):
    """When a class is in multiple subsets that resolve the same key to
    the *same* value, generation proceeds without error — only
    disagreement is fatal."""
    schema = """
id: https://example.org/ss-agree
name: ss_agree
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  audited:
    annotations:
      output_file: audited
  reviewed:
    annotations:
      output_file: audited     # same value — agreement

classes:
  Thing:
    in_subset: [audited, reviewed]
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "ss4.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())
    assert "Thing" in manifest["audited.json"]["$defs"]


def test_multi_subset_routing_conflict_raises(tmp_path: Path):
    """When the same class is in subsets that disagree on a key,
    generation must fail loudly. The error message must name the
    class, the annotation key, and every contributing
    ``(subset, value)`` pair so the author can diagnose at a glance."""
    schema = """
id: https://example.org/ss-conflict
name: ss_conflict
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  alpha:
    annotations:
      output_file: alpha-file
  beta:
    annotations:
      output_file: beta-file

classes:
  Disputed:
    in_subset: [alpha, beta]
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "ss5.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    with pytest.raises(ValueError) as excinfo:
        gen.serialize()
    msg = str(excinfo.value)
    assert "Disputed" in msg
    assert "output_file" in msg
    assert "alpha" in msg and "beta" in msg
    assert "alpha-file" in msg and "beta-file" in msg


def test_subset_tier2_overrides_subset_tier1(tmp_path: Path):
    """Within a single subset, the Tier 2 form (``jsonschema:<key>``)
    must take precedence over Tier 1 (``<key>``) — the same precedence
    rule as at the class level."""
    schema = """
id: https://example.org/ss-t2-over
name: ss_t2_over
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  override_bucket:
    annotations:
      output_file: generic-name
      jsonschema:output_file: jsonschema-name   # Tier 2 wins

classes:
  Member:
    in_subset: [override_bucket]
    attributes:
      label:
        required: true
"""
    schema_file = tmp_path / "ss6.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())
    assert "jsonschema-name.json" in manifest, list(manifest)
    assert "generic-name.json" not in manifest
    assert "Member" in manifest["jsonschema-name.json"]["$defs"]


def test_multiple_root_of_file_classes_in_same_file_raises(tmp_path: Path):
    """At most one class per output file may carry
    ``jsonschema:is_root_of_file: true``; otherwise the second promotion
    silently overwrites the first. This is easy to trip via subsets so
    we fail loudly at lookup-build time."""
    schema = """
id: https://example.org/multi-root
name: multi_root
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  roots:
    annotations:
      output_file: shared
      jsonschema:is_root_of_file: true

classes:
  First:
    in_subset: [roots]
    attributes:
      a:
        required: true
  Second:
    in_subset: [roots]
    attributes:
      b:
        required: true
"""
    schema_file = tmp_path / "mr.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    with pytest.raises(ValueError) as excinfo:
        gen.serialize()
    msg = str(excinfo.value)
    assert "shared.json" in msg
    assert "First" in msg and "Second" in msg
    assert "is_root_of_file" in msg


def test_class_level_root_of_file_false_overrides_subset_true(tmp_path: Path):
    """The class-wins precedence rule provides the escape hatch for the
    multi-root collision: if a subset promotes its members but one class
    opts out via ``jsonschema:is_root_of_file: false``, generation must
    succeed and the opt-out class lives in ``$defs`` as usual.
    """
    schema = """
id: https://example.org/opt-out
name: opt_out
default_prefix: ex
default_range: string
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/
imports:
  - linkml:types

subsets:
  promoted:
    annotations:
      output_file: out
      jsonschema:is_root_of_file: true

classes:
  Promoted:
    in_subset: [promoted]
    attributes:
      a:
        required: true
  Demoted:
    in_subset: [promoted]
    annotations:
      jsonschema:is_root_of_file: false   # class wins
    attributes:
      b:
        required: true
"""
    schema_file = tmp_path / "oo.yaml"
    schema_file.write_text(schema, encoding="utf-8")
    gen = MultiFileJsonSchemaGenerator(str(schema_file), not_closed=False)
    manifest = json.loads(gen.serialize())

    out = manifest["out.json"]
    # Promoted at file root.
    assert "properties" in out and "a" in out["properties"]
    # Demoted stays in $defs of the same file.
    assert "Demoted" in out.get("$defs", {})
    assert "Promoted" not in out.get("$defs", {})
