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
   
.. seealso:: `Data Validation <../data/validating-data>`_ for  other
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

JSON-Schema support schema composition through:

* allOf
* anyOf
* oneOf
* not

See `Schema Composition <https://json-schema.org/understanding-json-schema/reference/combining.html>`_

Currently there are no directly equivalent constructs in LinkML,
although future versions of LinkML will support an expressive
constraint mechanism.

Note that many uses of the above constructs may be better handled by
using inheritance (see below) in LinkML. Future versions of LinkML may
support translation of certain object oriented patterns to JSON-Schema
compositions, for example:

* The `union_of <https://w3id.org/linkml/union_of>`_ slot could be
  used to generate oneOf


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

Enums
^^^^^

Enumerations are treated as simple strings. If the LinkML schema has
additional metadata about the enumeration values, this is lost in
translations.

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
    :members: serialize, json_schema_types

