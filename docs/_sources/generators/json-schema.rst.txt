JSON Schema
===========

Example Output
--------------

`personinfo.schema.json <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/jsonschema/personinfo.schema.json>`_

Overview
--------

`JSON Schema <https://json-schema.org/>`__ is a schema language for JSON
documents.

To run:

.. code:: bash

   gen-json-schema personinfo.yaml > personinfo.schema.json

Note that any JSON that conforms to the derived JSON Schema can be
converted to RDF using the derived JSON-LD context.

Because JSON-Schema does not support inheritance hierarchy, slots are
"rolled down" from parent.

For example, in the personinfo schema, slots such as `id` and `name`
are inherited from NamedThing, and `aliases` are inherited from a mixin:

.. code-block:: yaml

  Person:
    is_a: NamedThing
    description: >-
      A person (alive, dead, undead, or fictional).
    class_uri: schema:Person
    mixins:
      - HasAliases
    slots:
      - primary_email
      - birth_date
      - age_in_years
      - gender
      - current_address
      - has_employment_history
      - has_familial_relationships
      - has_medical_history
    slot_usage:
      primary_email:
        pattern: "^\\S+@[\\S+\\.]+\\S+"  

(some parts truncated for brevity)

This would generate the following JSON-Schema:
        
.. code-block:: json

  "Person": {
         "description": "A person (alive, dead, undead, or fictional).",
         "properties": {
            "id": {
               "type": "string"
            },
            "name": {
               "type": "string"
            },
            "primary_email": {
               "pattern": "^\\S+@[\\S+\\.]+\\S+",
               "type": "string"
            },
            "age_in_years": {
               "type": "integer"
            },
            "aliases": {
               "items": {
                  "type": "string"
               },
               "type": "array"
            },
            "current_address": {
               "$ref": "#/definitions/Address"
            },
            "has_employment_history": {
               "items": {
                  "$ref": "#/definitions/EmploymentEvent"
               },
               "type": "array"
            },
            "has_familial_relationships": {
               "items": {
                  "$ref": "#/definitions/FamilialRelationship"
               },
               "type": "array"
            },
            "has_medical_history": {
               "items": {
                  "$ref": "#/definitions/MedicalEvent"
               },
               "type": "array"
            },
            ...
         },
         "required": [
            "id"
         ],
         "title": "Person",
         "type": "object"
      }                

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

