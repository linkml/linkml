---
name: generator-audit
description: Audit LinkML generators for conformance to the project's architecture, conventions, and design ethos (how a generator is built, not whether its output is correct). Use when reviewing a generator PR, before handing a generator to a contributor, or to survey which generators have drifted from the SchemaView / common-machinery conventions. Optionally scope to one generator by name (e.g. jsonschema); omit to survey all.
allowed-tools: Read, Grep, Glob, Bash
---

# Generator Audit Skill

Audit whether LinkML generator(s) follow our documented architecture and design ethos — not
whether their **output** is correct (that's the compliance suite's job), but whether the
**generator itself is built the way our generators are supposed to be built**. The goal is that a
generator handed to an outside contributor keeps tracking our core conventions without core-team
review on every change.

If the user names a generator (e.g. `jsonschema`, `pydantic`, or a path under
`packages/linkml/src/linkml/generators/`), do a deep single-generator audit. Otherwise, survey
**all** generators and rank them by how far each has drifted from the ethos, most-divergent first.

Read generator **source structure**. Do **not** run generators, diff generated artifacts, or
execute the compliance suite — those test output, and this is about how the code is written. (You
*should* check whether a generator is registered for compliance and has tests, as conformance
signals — see Layer 3 — but don't run them.)

## The reference: how our generators are supposed to work

There is no single spec doc; the contract lives in the code. Ground the audit in these:

- **Base class** — `packages/linkml/src/linkml/utils/generator.py`. `Generator` is an
  `abc.ABCMeta` `@dataclass`. Its module docstring states the central rule: generators are either
  old-style (SchemaLoader + visitor pattern) or new-style (SchemaView, no visitor), and **new
  generators must always be SchemaView-based** (issue #923).
- **Shared machinery** — `packages/linkml/src/linkml/generators/common/`: `LifecycleMixin`
  (`lifecycle.py`), `BuildResult` (`build.py`), `TemplateModel` (`template.py`), plus `naming.py`,
  `subproperty.py`, `ifabsent_processor.py`, `type_designators.py`. Reusing these instead of
  reinventing them **is** the ethos.
- **Exemplars** — `packages/linkml/src/linkml/generators/jsonschemagen.py` (dict-subclass output
  strategy) and `packages/linkml/src/linkml/generators/pydanticgen/` (model/template-driven
  strategy). Use them as **worked examples** of
  each criterion below.
- **Governance intent** — `docs/maintainers/generator-governance.md` for why per-generator
  conformance matters.

**The exemplars are references, not gospel.** They demonstrate the conventions but they are not
guaranteed perfect. Where an exemplar itself violates a rubric principle (a lingering deprecated
field, an inconsistency, a hand-rolled shortcut), **the rubric governs** — flag the exemplar's
deviation if it's relevant, and never treat "jsonschemagen/pydanticgen does it this way" as
license for the audited generator to do the same when it conflicts with the rubric below. When the
two exemplars disagree with each other, say so and reason from the rubric.

## Findings vs. maturity tier — read this before scoring

Separate two very different things, and never conflate them:

- **Findings** = things that are *wrong relative to what the generator is trying to be*. These are
  defects at any altitude: mutating shared schema state without a deep copy, a `uses_schemaloader`
  flag that contradicts the generator's actual style, reinventing `common/` logic, defining
  lifecycle hooks instead of firing them, swallowed errors, missing tests. Findings are actionable
  and belong in the report as work to do.
- **Maturity tier** = a *label* describing where a generator sits on the architecture curve
  (modern SchemaView vs. legacy visitor/SchemaLoader). Being a legacy visitor generator is **not a
  finding** — most of these predate the SchemaView direction (#923) and porting them is a large,
  separately-tracked migration, not something to charge against the current code. Report it as a
  tier with a pointer to the target pattern, not as a failure.

The "new generators must be SchemaView" rule is a **gate on new or materially-changed generators**
(apply it in review of a generator PR), **not** a retroactive verdict on the existing legacy set.
When you audit an existing legacy generator, label its tier and move on; only raise findings for
things wrong *within* that generator's own design.

## The rubric

Assess each generator across three layers. Interface issues are cheap to fix; ethos issues are the
ones that actually matter for keeping a contributor-owned generator on-model. Classify each item as
a **finding** (defect) or a **tier label** per the section above.

### Layer 1 — Interface & structural conformance (mechanical)

- `@dataclass` subclass of `Generator` (or `OOCodeGenerator` for object-oriented code generators).
- Declares the self-identifying ClassVars: `generatorname = os.path.basename(__file__)`,
  `generatorversion`, `valid_formats` (first entry is the default), `file_extension`.
- Sets `uses_schemaloader = False` (see Layer 2 — this is the load-bearing one).
- `__post_init__` calls `super().__post_init__()`.
- Overrides `serialize(self, **kwargs) -> str` and returns a string.
- CLI entrypoint: `@shared_arguments(TheGenerator)` + `@click.command(...)` +
  `@click.version_option(__version__, "-V", "--version")`, ending in
  `if __name__ == "__main__": cli()`.
- Modern typing (PEP 604 `X | None` unions), `ClassVar[...]` on generator metadata, and
  docstrings at module, class, and field level.

### Layer 2 — Architectural ethos (the core — where the real judgment is)

- **SchemaView, not SchemaLoader/visitor** *(tier label, not a finding, for existing generators).*
  Record whether the generator is modern (SchemaView, `uses_schemaloader = False`, no `visit_*`) or
  legacy (visitor/SchemaLoader). Legacy is a **tier**, with #923 as the migration target — do not
  score it as a divergence. The consuming idiom to expect in modern generators is `self.schemaview`
  (`all_classes`, `class_induced_slots`, `get_identifier_slot`, `induced_type`, range-dispatch via
  `all_types`/`all_enums`/`all_classes`). *However*, a **finding** does arise when the flag and the
  code disagree: a generator written against `self.schemaview` that still inherits
  `uses_schemaloader = True` (or vice versa) is a real bug — it triggers a wrong/redundant init path
  and can desync `self.schema` from `self.schemaview.schema`. Raise that.
- **Reuse `common/`, don't reinvent.** Hand-rolled name munging, ifabsent handling, type-designator
  resolution, or subproperty logic that duplicates `naming.py` / `ifabsent_processor.py` /
  `type_designators.py` / `subproperty.py` is a finding. Name the shared helper it should be using.
- **LifecycleMixin as an extension surface.** The generator should *fire* `before_generate_*` /
  `after_generate_*` hooks around its phases and **document which it fires** in its class docstring,
  and must **not define the hook methods itself** (that defeats the mixin — see `lifecycle.py`
  docstring). Missing hooks = no clean way for a downstream user to customize; self-defined hooks =
  misunderstanding of the pattern.
- **Structured intermediate representation where it fits.** Model-driven output (`BuildResult` /
  `TemplateModel`, as pydanticgen does) or a typed builder (as jsonschemagen's `JsonSchema(dict)`
  does) rather than raw string concatenation. Don't demand a template engine where a simple builder
  is genuinely cleaner — but flag ad-hoc string assembly of structured output.
- **No side effects on shared inputs.** Generation must not mutate the `SchemaView`, the underlying
  `SchemaDefinition`, or any element it hands out (classes, slots, induced slots) as a side effect.
  These are shared, and a mutation silently corrupts every downstream consumer and any generator run
  after it (e.g. under `gen-project`). If a generator needs to transform the schema, it must work on
  its **own deep copy** (`copy.deepcopy`, or an explicitly copied `SchemaDefinition`), not the live
  view. Treat in-place edits to `self.schemaview` / `self.schema` / returned metamodel objects
  during `serialize()` as a finding. More broadly, hold generators to being **pure and
  deterministic** with respect to their inputs: same schema in, same output out; no hidden global
  or class-level mutable state carried between runs.

### Layer 3 — Handoff readiness (maintainability)

- Registered in the compliance-suite `GENERATORS` map
  (`tests/linkml/test_compliance/helper.py`) so it's in the cross-framework matrix.
- Has tests under `tests/linkml/test_generators/` with a per-generator `pytest.mark.<name>` marker,
  including round-trip / validation tests (generate then validate real data), not snapshots alone.
- Lifecycle hooks are tested (subclass, override a hook, assert the effect).
- Deprecations go through `packages/linkml/src/linkml/utils/deprecation.py`
  (`deprecation_warning`, `deprecated_fields`, `METADATA_FLAG`) rather than ad-hoc warnings.
- No footguns: errors surfaced, not swallowed in bare `try/except`; failing fast over silent
  fallback. Complete docstrings and type hints.

## Output

Advisory report only — **no code changes.** Structure the report in two clearly separated parts so
the actionable work never hides behind the architectural backlog:

1. **Defects to fix (findings).** The punch-list — every finding with a `file:line`, the rule it
   breaks, and rough effort-vs-payoff. This is the part someone acts on. Order by severity: shared
   state mutation and flag/style contradictions first, then reinvented `common/` logic and
   self-defined hooks, then missing tests. Keep it tight; a legacy generator with no *defects* has
   an empty findings list even though it's on an old tier.
2. **Maturity map (tiers).** A table of every generator with its tier label (modern SchemaView /
   legacy visitor / SchemaView-intent), `common/` reuse, compliance registration, and test presence
   — informational, so you can see the migration landscape and spot the highest-drift-risk
   generators (legacy *and* untested *and* unregistered). This is context, not a list of failures.

- **Single generator** (a generator name was given): same two parts, scoped to one — its findings,
  then its tier line and what the target pattern/exemplar is if it's legacy.

Be direct, and keep the two registers distinct. For a *finding*: "flag says `uses_schemaloader=True`
but the code is pure SchemaView — remove the flag" beats hedging. For a *tier*: "legacy visitor
generator; SchemaView port tracked under #923; exemplar: jsonschemagen" — stated as context, not
scolding. Prefer naming the specific shared helper or exemplar pattern over vague suggestions, and
never frame a pre-existing architectural tier as something the current code did wrong.
