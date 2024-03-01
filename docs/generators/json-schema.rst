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

