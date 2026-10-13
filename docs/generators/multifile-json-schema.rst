Multi-file JSON Schema
======================

Overview
--------

The :class:`.MultiFileJsonSchemaGenerator` partitions a single LinkML
schema across multiple JSON Schema output files using annotations.
It is a thin subclass of :class:`.JsonSchemaGenerator`; only file
partitioning, cross-file ``$ref`` rewriting, and a few opt-in shape
transforms are added.

This generator is useful when the consumers of the generated JSON
Schema expect a published multi-file artifact tree, for example a
versioned ``meta/`` directory with stable per-entity URLs.

To run:

.. code:: bash

   gen-multifile-json-schema --output-dir build/schemas mymodel.yaml

To inspect the manifest without writing to disk:

.. code:: bash

   gen-multifile-json-schema mymodel.yaml | jq 'keys'

Annotation contract
-------------------

Annotations live under the LinkML metamodel's native ``annotations``
mapping. The contract is **tiered** so a single annotated schema can
drive multiple multi-file generators (JSON Schema today; Pydantic,
Rust, GraphQL, etc. in the future) without coupling the schema to
JSON-Schema terminology.

Override precedence: for any Tier 1 tag, a Tier 2 form
(``jsonschema:<key>``) wins when present, so generic defaults can be
selectively overridden per generator. Tier 2-only tags have no Tier 1
fallback by design.

Tier 1 — generic vocabulary (no prefix)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Concepts every multi-file generator needs. Reserved well-known tags,
candidates for future first-class LinkML metamodel slots.

``output_file`` (string)
   Stem or full filename of the artifact the class is emitted into.
   Stems without a ``.`` get the generator's extension appended
   (``.json`` here, ``.py`` for a hypothetical Pydantic multi-file
   generator). Classes without this annotation default to
   ``--default-file``. The Tier 1 tag name is configurable via
   ``--split-file-annotation``; the Tier 2 override
   ``jsonschema:<key>`` still wins.

``inline_class`` (boolean)
   When ``true``, the class is not emitted as a standalone definition;
   references to it are replaced by an inlined copy of its body.

``additional_properties`` (boolean)
   Per-class "open vs. closed" override. Prefer ``extra_slots.allowed``
   (LinkML 1.6+) when available; this annotation only applies when
   ``extra_slots`` is not set on the class.

Tier 2 — JSON-Schema-specific (``jsonschema:`` prefix)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Concepts that have no equivalent (or different semantics) in other
generators. Other generators must silently ignore tags they do not
recognize.

``jsonschema:is_root_of_file`` (boolean)
   When ``true``, the class body is promoted to the *root* of its file
   (``{type, properties, …}``) and no ``$defs`` entry is emitted for it.
   Equivalent to ``tree_root: true`` but scoped per file, so a multi-file
   output can have multiple root classes (one per file).

``jsonschema:def_name`` (string)
   Overrides the ``$defs`` key under which the class is emitted.
   Defaults to the canonical key chosen by the parent generator
   (``camelcase(class_name)`` unless ``--preserve-names`` is set, in
   which case the raw class name is used). ``$ref`` targets to the
   class are rewritten to use this key.

``jsonschema:pattern_properties`` (string)
   Rewrap the class body as
   ``{type: object, patternProperties: {<pattern>: <inner>}}``, where
   ``<inner>`` is the regular ``{type, properties, required, ...}``
   block the parent generator would have produced. Useful when a class
   represents a map whose keys must match a regular expression.

``jsonschema:discriminator_enum`` (string)
   Name of an enum whose permissible values name required keys on this
   class. Emits ``oneOf: [{required: [<v>]}, ...]`` appended to the
   class body, producing the standard JSON-Schema discriminator pattern.
   Pairs naturally with ``inline_class``.

Schema-level annotations
^^^^^^^^^^^^^^^^^^^^^^^^

``property_name_style`` (string, Tier 1)
   One of ``snake_case`` (default), ``kebab_case``, or ``preserve``.
   When ``kebab_case``, property names are taken from the first
   hyphen-containing entry in ``slot.aliases`` if present, otherwise
   the slot name with underscores replaced by hyphens. Selecting
   ``kebab_case`` or ``preserve`` implies ``--preserve-names`` so the
   generator does not normalize names further downstream. Honors the
   same Tier 2 override (``jsonschema:property_name_style``).

Subset-driven defaults
----------------------

Every class-level annotation in the contract is also resolvable from
the annotations of any :class:`~linkml_runtime.linkml_model.meta.SubsetDefinition`
the class belongs to (via ``in_subset``). This lets schemas declare
per-bucket defaults once at the subset level instead of repeating them
on every class.

Full resolution order, most specific to least:

1. ``jsonschema:<key>`` on the class.
2. ``<key>`` on the class.
3. ``jsonschema:<key>`` on any of the class's ``in_subset[]`` subsets.
4. ``<key>`` on any of the class's ``in_subset[]`` subsets.

When a class is in multiple subsets that resolve the same key to
different values, generation **fails** with a ``ValueError``
naming the class, the annotation, and the conflicting
``(subset, value)`` pairs. Resolve by setting the annotation directly
on the class, or by making the subset values agree. As a related
guard, at most one class per output file may carry
``jsonschema:is_root_of_file: true``; a second promotion target raises
the same error rather than silently overwriting a file's body.

Subset-level resolution applies to class-scoped annotations only.
Schema-level annotations (``property_name_style``) are read from the
schema's own ``annotations``.

Worked example
^^^^^^^^^^^^^^

The schema below declares two subsets (``core`` and
``control-framework``) that carry the file-routing defaults; member
classes only declare ``in_subset``. ``Architecture`` adds a
class-level ``jsonschema:is_root_of_file`` (class wins over subset)
and references ``Control``, which lives in a different file — the
generator rewrites the ``$ref`` accordingly.

.. code-block:: yaml

   id: https://example.org/subset-demo
   name: subset_demo
   default_range: string
   prefixes:
     ex: https://example.org/
     linkml: https://w3id.org/linkml/
   imports:
     - linkml:types

   subsets:
     core:
       description: Core architectural entities.
       annotations:
         output_file: core
         jsonschema:additional_properties: true

     control-framework:
       description: Control / compliance vocabulary.
       annotations:
         output_file: controls

   classes:
     Architecture:
       in_subset: [core]
       annotations:
         jsonschema:is_root_of_file: true   # class-level override
       attributes:
         name:
           required: true
         controls:
           range: Control
           multivalued: true
           inlined_as_list: true            # force a $ref (not an id string)

     Decision:
       in_subset: [core]                    # inherits output_file=core
       attributes:
         summary:
           required: true

     Control:
       in_subset: [control-framework]       # inherits output_file=controls
       attributes:
         label:
           required: true
         description:

The generator emits ``core.json`` and ``controls.json`` plus an empty
default ``schema.json``. ``core.json`` promotes ``Architecture`` to
the file root, keeps ``Decision`` under ``$defs``, inherits
``additionalProperties: true`` from the subset, and rewrites the
reference to ``Control``:

.. code-block:: json

   {
     "$schema": "https://json-schema.org/draft/2019-09/schema",
     "$id": "https://example.org/subset-demo/core.json",
     "title": "Architecture",
     "type": "object",
     "additionalProperties": true,
     "properties": {
       "name": {"type": "string"},
       "controls": {
         "type": ["array", "null"],
         "items": {"$ref": "controls.json#/$defs/Control"}
       }
     },
     "required": ["name"],
     "$defs": {
       "Decision": {
         "type": "object",
         "additionalProperties": true,
         "title": "Decision",
         "properties": {"summary": {"type": "string"}},
         "required": ["summary"]
       }
     }
   }

``controls.json`` carries ``Control`` under ``$defs``:

.. code-block:: json

   {
     "$schema": "https://json-schema.org/draft/2019-09/schema",
     "$id": "https://example.org/subset-demo/controls.json",
     "title": "subset_demo",
     "type": "object",
     "additionalProperties": true,
     "$defs": {
       "Control": {
         "type": "object",
         "additionalProperties": true,
         "title": "Control",
         "properties": {
           "label": {"type": "string"},
           "description": {"type": ["string", "null"]}
         },
         "required": ["label"]
       }
     }
   }

Compared to the class-level form, the subset-driven version moves
``output_file`` and ``additional_properties`` out of every class and
into the subset declaration. Adding a new ``Decision``-shaped class
to the ``core`` bucket now requires only ``in_subset: [core]``.

The same routing contract also works without subsets: place
``output_file`` and any ``jsonschema:...`` annotations directly on
each class when that is clearer than declaring shared defaults.

CLI flags
---------

In addition to the standard :class:`.JsonSchemaGenerator` flags
(``--not-closed``, ``--top-class``, ``--indent``, ``--title-from``,
``--materialize-patterns``, ``--preserve-names``,
``--include-range-class-descendants``):

``--output-dir <DIR>``
   Directory to write one JSON Schema file per ``output_file`` bucket.
   If omitted, a single JSON document mapping filename to schema body
   is printed to stdout.

``--default-file <NAME>``
   Output filename used for classes that lack an ``output_file``
   annotation. Defaults to ``schema.json``. Stems without a ``.`` get
   ``.json`` appended. Enums are emitted to this file.

``--split-file-annotation <KEY>``
   Tier 1 class annotation key used for file routing. Defaults to
   ``output_file``. The Tier 2 form ``jsonschema:<key>`` always wins
   when present, regardless of this setting.

Notes and limitations
---------------------

* Enums are routed to ``--default-file`` regardless of where their
  consumers live. Per-enum routing via an analogous annotation on
  :class:`~linkml_runtime.linkml_model.meta.EnumDefinition` is a
  straightforward additive extension.

* When a slot is inlined as a dict whose range lives in a *different*
  file, the parent generator's ``__identifier_optional`` lax variant is
  emitted into the file of the *referring* class, not the file of the
  range class and is rewritten correctly to a cross-file ``$ref`` by
  the post-pass.

* ``jsonschema:pattern_properties`` value schemas use the existing
  class body as the inner shape; if a different shape is required at
  the value position (for example, ``$ref`` to a separate class), model
  that with an intermediate class and a single slot whose range is the
  desired type.

* Other multi-file generators (Pydantic, Rust, …) that consume the
  same annotated schema **must silently ignore** tags they do not
  recognize. The ``jsonschema:`` prefix is reserved for this
  generator; future generators should adopt their own prefixes
  (``pydantic:``, ``rust:``, …).
