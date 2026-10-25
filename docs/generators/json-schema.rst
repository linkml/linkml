.. _jsonschemagen:

JSON Schema
===========

Example Output
--------------

`personinfo.schema.json <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/jsonschema/personinfo.schema.json>`_

Overview
--------

`JSON Schema <https://json-schema.org/>`__ is a schema language for JSON
documents.

JSON-Schema can be generated from a LinkML schema and used to validate
JSON documents using standard JSON-Schema validators.

To run:

.. code:: bash

   gen-json-schema personinfo.yaml > personinfo.schema.json

To use this in combination with the standard python jsonschema
validator (bundled with linkml):

.. code:: bash

   jsonschema -i data/example_personinfo_data.yaml personinfo.schema.json

.. seealso:: :doc:`Data Validation <./../data/validating-data>` for  other
             validation strategies

.. note ::

   Note that any JSON that conforms to the derived JSON Schema can be
   converted to RDF using the derived JSON-LD context.


CURIE usage
^^^^^^^^^^^

By default, JSON Schema property names use the generator's normal slot-name alias. With
``--use-curies``, non-identifier slot properties use their CURIEs (for example,
``demo_id`` with ``slot_uri: demo:id`` becomes ``demo:id``). Identifier slots marked
``identifier: true`` are an exception: they retain their slot-name alias (``id`` in
the example) so that the property name agrees with the JSON-LD ``@id`` alias. Class
``$defs`` names are CURIE-keyed as well.

The CURIE mode is opt-in. CURIEs are resolved with ``SchemaView.get_curie`` using the
schema's prefixes and default prefix.

Example (``ex`` is the schema's ``default_prefix``):

.. code-block:: yaml

    prefixes:
      ex: https://example.org/
      demo: https://example.org/demo/
    default_prefix: ex

    classes:
      Entity:
        slots:
          - id
          - demo_id

    slots:
      id:
        range: string
        required: true
        identifier: true
      demo_id:
        range: string
        slot_uri: demo:id

With ``gen-json-schema --use-curies``, the identifier property remains ``id`` and
``demo_id`` is keyed as ``demo:id``.


Inheritance
^^^^^^^^^^^

Because JSON-Schema does not support inheritance hierarchy, slots are
"rolled down" from parent.

For example, in the personinfo schema, slots such as `id` and `name`
are inherited from NamedThing, and `aliases` are inherited from a mixin:

.. code-block:: yaml

  NamedThing:
    slots:
      - id
      - name

  HasAliases:
    mixin: true
    attributes:
      aliases:
        multivalued: true

  Person:
    is_a: NamedThing
    mixins:
      - HasAliases
    slots:
      - birth_date
      - age_in_years
      - gender

(some parts truncated for brevity)

This would generate the following JSON-Schema:

.. code-block:: json

      "Person": {
         "additionalProperties": false,
         "description": "A person (alive, dead, undead, or fictional).",
         "properties": {
            "age_in_years": {
               "type": "integer"
            },
            "aliases": {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            "birth_date": {
               "type": "string"
            },
            "gender": {
               "$ref": "#/definitions/GenderType"
            },
            "id": {
               "type": "string"
            },
            "name": {
               "type": "string"
            },
         },
         "required": [
            "id"
         ],
         "title": "Person",
         "type": "object"
      },


Composition
^^^^^^^^^^^

JSON-Schema supports schema *composition* through:

* allOf
* anyOf
* oneOf
* not

See `Schema Composition <https://json-schema.org/understanding-json-schema/reference/combining.html>`_

LinkML supports analogous elements:

* `any_of <https://w3id.org/linkml/any_of>`_
* `all_of <https://w3id.org/linkml/all_of>`_
* `exactly_one_of <https://w3id.org/linkml/exactly_one_of>`_
* `none_of <https://w3id.org/linkml/none_of>`_

Use of these elements will be translated into the appropriate JSON-Schema construct.

Inlining
^^^^^^^^

LinkML separates the underlying logical model from choices of how
references are inlined in JSON.

If an `inlined <https://w3id.org/linkml/inlined>`_ directive is added
to a slot definition as follows:

.. code-block:: yaml

  has_employment_history:
    range: EmploymentEvent
    multivalued: true
    inlined: true
    inlined_as_list: true

then the JSON-Schema will use a ``$ref``:

.. code-block:: json

            "has_employment_history": {
               "items": {
                  "$ref": "#/definitions/EmploymentEvent"
               },
               "type": "array"
            },

However, if a slot is not inlined and the range is a class with an
identifier, then the reference is by key.

For example, given:

.. code-block:: yaml

  FamilialRelationship:
    is_a: Relationship
    slot_usage:
      related to:
        range: Person
        required: true

Here the value of ``related_to`` is expected to be a string must be an
identifier for a ``Person`` object:

the range is treated as a simple string in the JSON-Schema

.. code-block:: json

      "FamilialRelationship": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "related_to": {
               "type": "string"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            }
         },
         "required": [
            "type",
            "related_to"
         ],
         "title": "FamilialRelationship",
         "type": "object"
      },

Thus the JSON-Schema loses some information that is useful for
validation, and for understanding of the schema.

LinkML also supports the ability to inline multivalued slots as
dictionaries, where the key is the object identifier. See :doc:`Inlining </schemas/inlining>`

This example schema supports inlining a list of people as a dictionary:

.. code-block:: yaml

    classes:
      Container:
        tree_root: true
        attributes:
          persons:
            range: Person
            inlined: true
            multivalued: true
      Person:
        attributes:
          name:
            identifier: true
          age:
            range: integer
            required: true
          gender:
            range: string
            required: true

The following data is conformant according to LinkML semantics:

.. code-block:: json

    {
     "persons":
       {
         "Bob": {
             "age": 42,
             "gender": "male"
         },
         "Alice": {
             "age": 37,
             "gender": "female"
         }
       }
    }

This presents an additional complication when generating JSON-Schema:
semantically the ``name`` field is required (all identifiers are
automatically required in json-schema). However, we don't want it to
be required *in the body of the dictionary* since it is already
present as a key.

The JSON-Schema generator takes care of this for you by making an
alternative "laxer" version of the Person class that is used for
validating the body of the ``persons`` dict.

This is what the underlying JSON-Schema looks like:

.. code-block:: json

   "$defs": {
      "Person": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "age": {
               "type": "integer"
            },
            "gender": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "name",
            "age",
            "gender"
         ],
         "title": "Person",
         "type": "object"
      },
      "Person__identifier_optional": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "age": {
               "type": "integer"
            },
            "gender": {
               "type": "string"
            },
            "name": {
               "type": "string"
            }
         },
         "required": [
            "age",
            "gender"
         ],
         "title": "Person",
         "type": "object"
      }
   },
   "$id": "http://example.org",
   "$schema": "http://json-schema.org/draft-07/schema#",
   "additionalProperties": false,
   "properties": {
      "persons": {
         "additionalProperties": {
            "$ref": "#/$defs/Person__identifier_optional"
         }
      }
   },
   "title": "example.org",
   "type": "object"



Optional slots and null
^^^^^^^^^^^^^^^^^^^^^^^

By default, optional (non-required) slots accept an explicit JSON ``null`` in
addition to their base type — the generator emits ``"type": ["string", "null"]``
for an optional string slot. This is convenient for producers that serialise
missing values as ``null``.

Some target schemas forbid explicit ``null`` on optional properties (a property
must either be present with a typed value or absent). Use
``--no-include-null`` to restrict optional slots to their base type:

.. code:: bash

   gen-json-schema --no-include-null personinfo.yaml

With ``--no-include-null`` the optional string slot above is emitted as
``"type": "string"``, so instance documents carrying ``"slot": null`` fail
validation. The default (``--include-null``) preserves the previous behaviour.


Dialect
^^^^^^^

The generated document declares JSON Schema draft 2019-09 in ``$schema`` by
default. Use ``--draft 2020-12`` to declare draft 2020-12 instead:

.. code:: bash

   gen-json-schema --draft 2020-12 personinfo.yaml

Only ``$schema`` changes, because the generator uses only keywords that mean
the same in both drafts. ``linkml-validate`` reads ``$schema`` and validates
with the matching dialect.


Definition names
^^^^^^^^^^^^^^^^

Classes and enums become entries under ``$defs``, keyed in CamelCase by
default (``node interface`` becomes ``NodeInterface``), or by the name as
written under ``--preserve-names``. A published specification may name its
definitions in another style. ``--def-name-style`` chooses the style of every
key and of every ``$ref`` that points at one:

.. code:: bash

   gen-json-schema --def-name-style kebab-case personinfo.yaml

The styles are ``CamelCase``, ``camelCase``, ``snake_case``, ``kebab-case``
and ``preserve``. With ``kebab-case``, the class ``ControlDetail`` is keyed
``control-detail`` and referenced as ``#/$defs/control-detail``. If two names
give the same key, as ``HttpServer`` and ``HTTPServer`` do in ``kebab-case``,
the generator stops with an error instead of letting one definition replace
the other.

The option sets the names of definitions only. Property names still come
from the slot name or its ``alias``, under the rules of ``--preserve-names``. Under
``--use-curies``, class definitions are keyed by CURIE whatever the style.


One document per module
^^^^^^^^^^^^^^^^^^^^^^^

By default the generator writes one document that covers the schema and
everything it imports. With ``--split``, it writes one document per schema
module instead, so the output follows the structure of the model. Published
specifications are often a set of JSON Schema files that refer to each other,
and a modular LinkML schema can reproduce that layout.

In split mode:

* each class and enum is written to the document of the module that defines it;
* each document's ``$id`` is the module's URI, given by ``--split-pattern``,
  which defaults to the module's ``id``;
* a ``$ref`` to an element of another module points at that module's URI,
  as a relative reference when both URIs share scheme, host and parent path
  (``control.json#/$defs/ControlDetail``), and in full otherwise;
* each document takes its root class from the module's own ``tree_root``;
* a class from another module that is the range of a slot inlined as a
  dictionary gets a private copy, without a required identifier, in the
  referring document.

``--split-pattern`` is a jinja template that is given each module's schema
definition as ``schema``. ``--output-directory`` writes the document of every
module that defines a class or an enum, named after the last path segment of
its URI:

.. code:: bash

   gen-json-schema --split --draft 2020-12 \
     --split-pattern 'https://example.org/release/1.3/meta/{{ schema.name }}.json' \
     --output-directory meta/ \
     core.yaml

Without ``--output-directory``, ``--split`` prints the input module's
document only. From Python, ``JsonSchemaGenerator.generate_split`` writes the
documents and also accepts ``split_context``, a dictionary of further
variables for the template.

A validator resolves the references between documents by ``$id``. With the
``referencing`` library that ``jsonschema`` uses, register each document under
its ``$id`` and validate against the root document:

.. code:: python

   import json
   from pathlib import Path

   from jsonschema import Draft202012Validator
   from referencing import Registry, Resource

   documents = [json.loads(p.read_text()) for p in Path("meta").glob("*.json")]
   registry = Registry().with_resources((d["$id"], Resource.from_contents(d)) for d in documents)
   core = next(d for d in documents if d["$id"].endswith("/core.json"))
   Draft202012Validator(core, registry=registry).validate(instance)


Patterns
^^^^^^^^

Both LinkML and JSON-Schema support the same subset of `ECMA-262
<https://www.ecma-international.org/publications-and-standards/standards/ecma-262/>`_
regular expressions.

See `Regular Expressions
<https://json-schema.org/understanding-json-schema/reference/regular_expressions.html#example>`_.

For example, the following schema fragment

.. code-block:: yaml

    classes:
      # ...
      Person:
        # ...
        slot_usage:
          primary_email:

will generate:

.. code-block:: json

            "primary_email": {
               "pattern": "^\\S+@[\\S+\\.]+\\S+",
               "type": "string"
            }

LinkML also supports `Structured patterns <https://w3id.org/linkml/structured_pattern>`_, these are
compiled down to patterns during JSON Schema generation.

Rules
^^^^^

LinkML supports `Rules <https://linkml.io/linkml/schemas/advanced.html>`_ which allow for conditional
application of constraints.

These are converted to if/then/else constructs in JSON-Schema.

Uniqueness constraints
^^^^^^^^^^^^^^^^^^^^^^

LinkML provides different mechanisms for stating uniqueness constraints:

* The `identifier <https://w3id.org/linkml/identifier>`_ and `key <https://w3id.org/linkml/key>`_ slots
  metamodel slots allow a class to have a single primary key
* The `unique_keys <https://w3id.org/linkml/unique_keys>`_ slot allows for additional unique keys. These can be singular or compound.

Currently JSON-Schema does not yet support unique keys. See `This stackoverflow question <https://stackoverflow.com/questions/24763759/make-sure-item-property-in-array-is-unique-in-json-schema>`_
for a discussion.

It is possible to get a limited form of uniqueness key checking in JSON-Schema: slots
marked as ``identifier`` or ``key`` that are also `inlined <https://w3id.org/linkml/inlined>`_
are enforced to be unique by virtue of the fact that the slot is used as the key in a dictionary,
and dictionaries in JSON cannot have duplicate keys.

Enums
^^^^^

Enumerations are treated as simple strings. If the LinkML schema has
additional metadata about the enumeration values, this is lost in
translation.

Example:

.. code-block:: yaml

    classes:
      # ...
      FamilialRelationship:
        is_a: Relationship
        slot_usage:
          type:
            range: FamilialRelationshipType
            required: true
          related to:
            range: Person
            required: true
      #...

    enums:
      FamilialRelationshipType:
        permissible_values:
          SIBLING_OF:
            description: a relationship between two individuals who share a parent
          PARENT_OF:
            description: a relationship between a parent (biological or non-biological) and their child
          CHILD_OF:
            description: inverse of the PARENT_OF type


Generates

.. code-block:: json

      "FamilialRelationship": {
         "additionalProperties": false,
         "description": "",
         "properties": {
            "ended_at_time": {
               "format": "date",
               "type": "string"
            },
            "related_to": {
               "type": "string"
            },
            "started_at_time": {
               "format": "date",
               "type": "string"
            },
            "type": {
               "$ref": "#/definitions/FamilialRelationshipType"
            }
         },
         "required": [
            "type",
            "related_to"
         ],
         "title": "FamilialRelationship",
         "type": "object"
      },
      "FamilialRelationshipType": {
         "description": "",
         "enum": [
            "SIBLING_OF",
            "PARENT_OF",
            "CHILD_OF"
         ],
         "title": "FamilialRelationshipType",
         "type": "string"
      },

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.jsonschemagen:cli
    :prog: gen-json-schema
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.jsonschemagen

.. autoclass:: JsonSchemaGenerator
    :members: serialize
