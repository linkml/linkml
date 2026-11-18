Zod
===

Overview
--------

This generator produces `Zod <https://zod.dev>`_ schemas together with the
TypeScript types inferred from them (via ``z.infer``). Zod is a TypeScript-first
schema declaration and validation library: the generated schemas can be used to
validate untrusted data at runtime (``.parse`` / ``.safeParse``) while
simultaneously giving you static types for free.

.. seealso:: :doc:`TypeScript </generators/typescript>` for plain interface
   definitions without runtime validation.

Each LinkML class becomes a self-contained ``z.object`` schema that includes
every slot induced through ``is_a`` inheritance and ``mixins``, and each enum
becomes a ``z.enum``. For every class ``Foo`` the generator emits both a
``FooSchema`` constant and an inferred ``Foo`` type.

Both **Zod Mini** and **custom registries** are supported (see *Options*).

.. note:: The generated code targets the **Zod v4** API. Projects still on
   **Zod v3.25+** can consume it too, since those versions ship the v4 API
   under the ``zod/v4`` subpath (rewrite the emitted import accordingly).

Example
-------

Given this LinkML schema (``personinfo.yaml``):

.. code-block:: yaml

    classes:
      Person:
        slots: [id, name, age_in_years, has_medical_history]
      MedicalEvent: {}

    slots:
      id:
        identifier: true
        range: string
      name:
        range: string
      age_in_years:
        range: integer
        minimum_value: 0
        maximum_value: 999
      has_medical_history:
        range: MedicalEvent
        multivalued: true
        inlined_as_list: true

running:

.. code-block:: bash

    gen-zod personinfo.yaml > personinfo.ts

emits:

.. code-block:: typescript

    import { z } from "zod";

    export const PersonSchema = z.object({
        id: z.string(),
        name: z.string().optional().nullable(),
        age_in_years: z.number().int().gte(0).lte(999).optional().nullable(),
        get has_medical_history() { return z.array(MedicalEventSchema).optional().nullable(); }
    });
    export type Person = z.infer<typeof PersonSchema>;

The generated module can then validate untrusted data and type the result in
one step:

.. code-block:: typescript

    import { PersonSchema, type Person } from "./personinfo";

    const person: Person = PersonSchema.parse(untrustedInput);   // throws on invalid data
    const result = PersonSchema.safeParse(untrustedInput);        // { success, data | error }

Feature mapping
---------------

.. raw:: html

   <style>
   table.fixed-table { table-layout: fixed; width: 100%; }
   table.fixed-table td, table.fixed-table th { word-wrap: break-word; }
   </style>

.. list-table::
   :header-rows: 1
   :widths: 45 55
   :class: fixed-table

   * - LinkML construct
     - Zod output
   * - Scalar types
     - ``string`` -> ``z.string()``, ``integer`` -> ``z.number().int()``, ``boolean`` -> ``z.boolean()``, ``float`` / ``double`` / ``decimal`` -> ``z.number()``, ``uri`` -> ``z.url()``, ``ncname`` -> NCName-patterned ``z.string()``
   * - ``date`` / ``datetime`` / ``time``
     - coerced to ``Date`` via a ``dateFromString`` preprocessor; with ``--iso-dates`` validated as ISO strings (``z.iso.*``)
   * - Enums
     - ``z.enum([...])``; dynamic (``reachable_from``) or empty enums fall back to ``z.string()`` (materialize with ``vskit expand`` first)
   * - Inheritance & mixins
     - every schema is self-contained - all induced slots are inlined onto each class
   * - Polymorphism
     - an inlined range with concrete ``is_a`` descendants -> ``z.union([...])`` (or ``z.discriminatedUnion`` when a ``designates_type`` slot is present); class-level ``union_of`` -> ``z.lazy(() => z.union([...]))``
   * - References
     - inlined class range -> embedded schema (lazy getter for recursion); non-inlined -> identifier string
   * - ``class_uri: linkml:Any``
     - ``z.any()`` (arbitrary payloads pass through unchanged)
   * - Collections
     - multivalued -> ``z.array(...)`` bounded by ``minimum`` / ``maximum`` / ``exact_cardinality`` (``.min`` / ``.max`` / ``.length``); inlined identifier-keyed -> ``z.record(...)``
   * - ``array`` (n-dimensional)
     - nested ``z.array(...)`` layers with per-dimension cardinality
   * - ``all_members`` / ``has_member``
     - a ``.refine`` requiring every / at least one element to match
   * - Constraints
     - ``pattern`` -> ``.regex(...)``, ``minimum_value`` / ``maximum_value`` -> ``.gte(...)`` / ``.lte(...)`` (type-level constraints apply wherever the type is used)
   * - Boolean expressions
     - ``any_of`` -> ``z.union``, ``exactly_one_of`` -> ``z.xor``, ``all_of`` -> chained ``.and``, ``none_of`` -> a rejecting ``.refine``
   * - Constant constraints
     - ``equals_string`` / ``equals_number`` -> ``z.literal(...)``, ``equals_string_in`` -> ``z.enum([...])``
   * - Rules
     - class-level ``rules`` -> cross-field ``.refine`` (``pre implies post``)
   * - ``ifabsent``
     - ``.default(...)`` literal
   * - Optionality
     - non-required slots -> ``.optional().nullable()``
   * - ``readonly``
     - ``.readonly()``
   * - Metadata
     - ``title`` / ``description`` / ``unit`` / ``examples`` / ``aliases`` / ``see_also`` / ``deprecated`` -> ``.meta({...})`` (survives ``z.toJSONSchema()``); a unique-name ``id`` names the ``$defs`` entry; enum value descriptions/meanings go under ``values``. Descriptions are also JSDoc comments.

Options
-------

* ``--strict`` - emit ``z.strictObject`` (reject unknown keys) instead of ``z.object`` (which strips them).

* ``--coerce`` - wrap scalar validators in ``z.coerce.*`` so inputs are converted before validation (numeric and string constraints are preserved).

* ``--iso-dates`` - validate ``date`` / ``datetime`` / ``time`` values as ISO strings (``z.iso.*``) instead of coercing them to JavaScript ``Date`` objects. ``ifabsent`` date defaults are emitted as ISO string literals in this mode.

* ``--brand`` - nominally brand class schemas that carry an identifier (``.brand("ClassName")``) so structurally-identical objects are not interchangeable in TypeScript.

* ``--zod-mini`` - target ``zod/mini``, the functional tree-shakable variant (``import * as z from "zod/mini"``). Optionality becomes wrappers (``z.nullable(z.optional(x))``), constraints collect into ``.check(...)``, intersections use ``z.intersection(...)``, defaults use ``z._default(...)`` and metadata uses ``.check(z.meta({...}))``. Implies ``--iso-dates`` (Zod Mini has no ``z.preprocess``). Reference getters that form a cycle are annotated ``: z.ZodMiniType`` so the self-referential type checks; those recursive fields infer as (required) ``unknown``. Non-recursive reference fields keep their precise, correctly-optional inferred types.

* ``--registry NAME`` - emit ``export const NAME = z.registry<LinkmlMeta>()`` and register every class and enum schema in it. The registry is both an enumerable collection of all generated schemas (``NAME.has(S)`` / iterate) and a carrier of LinkML *semantic* metadata kept out of the global ``.meta()`` / JSON Schema: each schema is added with its ``uri``, ``definition_uri``, ``exact_mappings`` / ``close_mappings`` / ``related_mappings`` / ``narrow_mappings`` / ``broad_mappings``, ``in_subset``, ``rank`` and ``source`` (whichever are present). Works identically for ``--zod-mini``.

* ``--output PATH`` - write the generated module to ``PATH`` instead of stdout.

Schema annotations
------------------

Because LinkML is schema-first, some options can also be declared *in the schema*
via annotations, so the intent travels with the model. A CLI flag, when passed,
always overrides the annotation.

**Schema-level behavior flags** - set any of ``zod_strict``, ``zod_coerce``,
``zod_iso_dates``, ``zod_brand`` in the schema's ``annotations`` to enable the
corresponding behavior by default:

.. code-block:: yaml

    annotations:
      zod_strict: true
      zod_coerce: true

Running with an explicit ``--no-strict`` / ``--strict`` (etc.) overrides the
annotation. Target/packaging options (``--zod-mini``, ``--registry``) remain
CLI-only, since the same schema is legitimately emitted for different targets.

**Per-slot type overrides** - annotate an individual slot to control its Zod
expression, which also fills several of the metamodel gaps below:

* ``zod_format`` - select a named format validator: ``email``, ``uuid``, ``url``,
  ``httpUrl``, ``ipv4``, ``ipv6``, ``e164``, ``jwt``, ``emoji``, ``base64``,
  ``base64url``, ``nanoid``, ``cuid``, ``cuid2``, ``ulid``, ``date``, ``time``,
  ``datetime``. The named validator becomes the base, and a ``pattern`` still
  applies on top of it.
* ``zod_type`` - emit a verbatim expression, overriding the range entirely (no
  auto-added constraints). Use for anything the generator can't express. If the
  expression references another generated schema, wrap it in ``z.lazy(() => ...)``
  so it is deferred (a bare forward reference would hit a temporal-dead-zone error).

.. code-block:: yaml

    classes:
      Contact:
        attributes:
          email:
            range: string
            annotations:
              zod_format: email        # -> z.email()
          handle:
            range: string
            annotations:
              zod_type: 'z.string().brand<"Handle">()'   # emitted verbatim

Both work identically under ``--zod-mini`` (the format validators are top-level
``z.*()`` calls shared by both dialects).

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.zodgen

.. click:: linkml.generators.zodgen:cli
    :prog: gen-zod
    :nested: short

Code
^^^^


.. autoclass:: ZodGenerator
    :members: serialize

.. _zodgen-metamodel-gaps:

Appendix A: LinkML metamodel gaps
----------------------------------

Parts of Zod feature surface cannot be driven from LinkML today, either
because the metamodel needs update or some construct is unresolved at
generation time. Needs work (in LinkML, its tooling, or in zodgen.py).

* **Explicit nullability** - LinkML has no notion of an explicitly *nullable*
  value distinct from an optional (absent) one. The generator emits
  ``.optional().nullable()`` for every non-required slot, which also admits
  ``null``. A metamodel flag distinguishing "may be absent" from "may be null"
  would let the generator stop over-permitting ``null``.

* **Exclusive unions (XOR)** - ``exactly_one_of`` maps to Zod's ``z.xor``, which
  requires *exactly one* member to match. Because LinkML does not guarantee the
  members are mutually exclusive, an input that happens to satisfy more than one
  branch will be rejected even though LinkML's ``exactly_one_of`` is only a
  cardinality-of-matches constraint; authors should keep branches disjoint.

* **Dynamic enums** - ``reachable_from`` / ``matches`` enums are not resolved at
  generation time, so they degrade to ``z.string()``. This requires an
  expansion step (e.g. ``vskit expand``) that the generator does not perform.

* **Semantic string formats** - LinkML has no first-class format types for most
  of Zod's string formats. ``uri`` maps to ``z.url()`` and ``ncname`` to an
  NCName-patterned ``z.string()``, but Zod's ``z.email()``, ``z.uuid()``,
  ``z.ipv4()``, ``z.jwt()``, etc. have no metamodel counterpart, so ``uriorcurie``
  / ``curie`` and similar remain bare ``z.string()``. ``date`` / ``time`` formats
  are available opt-in via ``--iso-dates``. As an escape hatch, a slot may set a
  ``zod_format`` (or ``zod_type``) annotation to select any Zod format explicitly
  (see *Schema annotations*).

* **Date bounds** - date-typed ``minimum_value`` / ``maximum_value`` are not
  emitted as ``z.date().min()`` / ``.max()``: the default ``date`` representation
  is a ``z.preprocess`` wrapper that does not expose those refinements.

* **Object openness** - LinkML core exposes no per-class "additional properties"
  / open-vs-closed flag to generators, so strictness is controlled globally via
  ``--strict`` rather than per class.

* **Set and tuple collections** - multivalued slots always map to ``z.array``.
  LinkML has no uniqueness (set) or heterogeneous fixed-length (tuple) collection
  construct, so ``z.set`` and ``z.tuple`` are never emitted.

* **Numeric bound exclusivity and step** - LinkML ``minimum_value`` /
  ``maximum_value`` are inclusive only; there is no exclusive bound
  (``.gt`` / ``.lt``) or ``multipleOf`` / step equivalent.

* **BigInt** - LinkML ``integer`` maps to ``z.number().int()``; there is no
  metamodel distinction for arbitrary-precision integers (``z.bigint``).

* **String length constraints** - LinkML has no ``minLength`` / ``maxLength``
  for strings, so ``z.string().min(n)`` / ``.max(n)`` cannot be derived.

* **Computed defaults** - ``equals_expression`` (and other computed/derived
  values) cannot be expressed as a static ``.default(...)`` literal.

* **Structured patterns** - ``structured_pattern`` with ``settings``
  interpolation is not resolved into a concrete regex.

* **Read-only and deprecated typing** - LinkML ``readonly`` is free text (treated
  as a boolean flag here) and ``deprecated`` is a reason string, whereas Zod's
  ``GlobalMeta.deprecated`` is a boolean; the reason is preserved separately as
  ``deprecatedReason``.

.. _zodgen-no-construct:

Appendix B: Zod features with no LinkML construct
-------------------------------------------------

These Zod primitives and combinators are intentionally **not** emitted because
LinkML has no corresponding modelling construct. They are listed for
completeness; there is nothing to "fix" until a LinkML equivalent exists.

* **Extra primitives** - ``z.symbol()``, ``z.void()``, ``z.never()``,
  ``z.unknown()`` and ``z.nan()`` (LinkML ``linkml:Any`` maps to ``z.any()``;
  everything else has a concrete range).

* **Map / Set collections** - ``z.map()`` and ``z.set()`` (LinkML collections are
  ordered arrays or identifier-keyed records).

* **Files, Promises, Functions** - ``z.file()``, ``z.promise()``,
  ``z.function()`` describe runtime/JS values, not data shapes.

* **Instanceof / Custom** - ``z.instanceof()``, ``z.property()`` and
  ``z.custom()`` validate host-language objects.

* **Stringbool / JSON** - ``z.stringbool()`` and ``z.json()`` are input-parsing
  conveniences without a schema-level counterpart.

* **Template literals** - ``z.templateLiteral()`` (the nearest LinkML feature,
  ``structured_pattern``, is a regex form and is not yet resolved).

* **Transform pipeline** - ``z.transform()`` / ``.pipe()`` / ``z.codec()`` /
  ``.catch()`` / ``.prefault()``; only the ``date`` ``z.preprocess`` is emitted.

* **Consumer-side object APIs** - ``.extend()`` / ``.pick()`` / ``.omit()`` /
  ``.partial()`` / ``.required()`` / ``.keyof()`` / ``.shape`` are authored
  against the generated schemas, not produced by the generator.

.. _zodgen-errors:

Appendix C: Error handling and internationalization
---------------------------------------------------

The generator emits *structural* validators only; Zod's error-presentation
surface is left to the consuming application, because LinkML carries no
corresponding metadata.

* **Custom error messages** - no per-field ``error`` / ``message`` strings are
  attached to schemas (LinkML has no slot-level validation-message field).

* **Refinement control** - the ``abort`` and ``when`` options of ``.refine`` are
  not used; generated refinements (``none_of``, ``rules``, member constraints)
  run with default continuation semantics.

* **Localization** - no locales or ``z.config`` internationalization are emitted;
  callers install their own locale (``z.config(z.locales.*)``).

* **Error formatting** - ``z.treeifyError`` / ``z.prettifyError`` /
  ``z.flattenError`` are consumer-side utilities and are out of scope.
