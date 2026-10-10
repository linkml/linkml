OpenAPI
=======

`OpenAPI <https://www.openapis.org/>`_ is a specification for describing
RESTful HTTP APIs. The OpenAPI generator produces an OpenAPI
specification in YAML from a LinkML schema. As of now it supports OpenAPI
specification versions v3.0.3 and v3.1.0.

.. note:: This generator produces a complete OpenAPI spec by combining a
          user-provided *template* (containing the API header, endpoints, and
          security schemes) with JSON Schema components derived from the
          LinkML schema.

Overview
--------

The generator works in two stages:

1. The user provides an **OpenAPI template** — a valid OpenAPI YAML
   file that defines the API metadata (title, version, servers), paths
   (endpoints), and security schemes. It also specifies the version of
   the OpenAPI specification in its top-level attribute `openapi`.
2. The generator fills the ``components/schemas`` section with JSON Schema
   definitions generated from the LinkML schema, keeping only those classes
   that are transitively reachable from the endpoints.
   A reference counts wherever it sits in an endpoint's schema object, so a
   list endpoint (``type: array`` with the ``$ref`` under ``items``) and a
   polymorphic one (``oneOf``, ``anyOf``, ``allOf``) seed generation too.

Both the input template and the final output are automatically validated
against the corresponding OpenAPI specification version using
`openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`_.

To run:

.. code:: bash

   gen-openapi personinfo.yaml --template api-template.yaml > personinfo.openapi.yaml

The **template's top-level attribute `openapi` MUST specify the supported OpenAPI
version**.

The ``--template`` / ``-t`` option is required when generating a concrete
specification. If omitted, the generator prints a generic template that can
be used as a starting point:

.. code:: bash

   gen-openapi personinfo.yaml > api-template.yaml

To create a template for the classes an API exposes instead, from the schema and a
configuration file, see :ref:`openapi-create-template`.

OpenAPI Validation
------------------

The generator validates both the input template and the final output against
the OpenAPI specification using
`openapi-spec-validator <https://github.com/p1c2u/openapi-spec-validator>`_.

The template's ``components/schemas`` section must declare each resource
that is referenced by an endpoint, using two custom extension fields:

``x-linkml-schema``
   The ``id`` of the LinkML schema being used. Must match exactly.
``x-linkml-source``
   The name of the LinkML class that provides the schema for this resource.

Example template fragment:

.. code-block:: yaml

   components:
     schemas:
       Person:
         type: object
         x-linkml-schema: https://w3id.org/linkml/my_schema
         x-linkml-source: Person
       Organization:
         type: object
         x-linkml-schema: https://w3id.org/linkml/my_schema
         x-linkml-source: Organization

If the ``x-linkml-schema`` value does not match the schema being processed,
the generator raises a ``ValueError``. Any endpoint that references a
resource not declared in ``components/schemas`` also raises an error.

Name Rewiring
-------------

If the name used for a resource in the OpenAPI template differs from the
LinkML class name specified in ``x-linkml-source``, the generator
automatically rewires all ``$ref`` references and schema keys to use the
template name.

For example, given this template:

.. code-block:: yaml

   components:
     schemas:
       PersonResource:
         type: object
         x-linkml-schema: https://w3id.org/linkml/my_schema
         x-linkml-source: Person

The generated spec will use ``PersonResource`` rather than ``Person``
throughout ``components/schemas`` and all ``$ref`` values.

Template Annotations
--------------------

A template placeholder is normally read only for ``x-linkml-schema`` and
``x-linkml-source``; the schema body is generated from the LinkML element.
A placeholder may additionally declare annotations, which override the
generated values for that resource:

* ``description``, ``title``, ``example``, ``externalDocs``, ``deprecated``
* any ``x-`` vendor extension (``x-linkml-*`` keys are never published)

The LinkML-derived value is the default; a key the template declares
explicitly wins. Structural keys such as ``type``, ``properties`` and
``enum`` are never taken from the template: placeholders conventionally
carry ``type: object`` even for LinkML types and enums, which generate as
``type: string``.

.. code-block:: yaml

   components:
     schemas:
       PersonResource:
         type: object
         description: A person, as exposed by this API.
         deprecated: true
         x-linkml-schema: https://w3id.org/linkml/my_schema
         x-linkml-source: Person

Overrides are applied by template name, so they also reach renamed
resources (see Name Rewiring above). A placeholder whose schema is pruned
is ignored. Annotations must have the type OpenAPI requires (for example
``deprecated`` must be a boolean); a wrongly typed value fails template
validation before generation starts.

JSON Schema Transformations
---------------------------

The generator applies several compatibility transforms to the JSON Schema
generated by :doc:`JsonSchemaGenerator <json-schema>`:

* ``const`` values become single-element ``enum`` arrays (OpenAPI 3.0 does
  not support ``const``).
* ``type`` lists (e.g. ``["string", "null"]`` for nullable fields) are
  rewritten as ``anyOf``.
* ``$ref`` paths are rewritten from ``#/$defs/`` to ``#/components/schemas/``.
* Class-level ``title`` fields (redundant with the schema key) are
  stripped, unless the template declares a ``title`` for that resource.

Only classes transitively reachable from the endpoints are included in the
output — unreferenced schemas are pruned automatically.

Advanced Usage
--------------

Keeping Unreferenced OpenAPI Schemas
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, if the OpenAPI template declares schemas in ``components/schemas``
that are not referenced by any of the endpoints, they are removed.

Using the *keep unreferenced* option (object constructor boolean argument
``keep_unreferenced``, CLI flag ``--keep-unreferenced``) it's possible to change
that behavior so that all schemas provided in ``components/schemas`` are kept
in the resulting OAD (OpenAPI Description) document.

Inlining Enums
^^^^^^^^^^^^^^

By default enumerations are declared as separate schemas in the
``components/schemas`` of the resulting OAD (OpenAPI Description) document.

Using the *inline_enums* option (object constructor boolean argument
``inline_enums``, CLI flag ``--inline-enums``) it's possible to change
that behavior so that enumerations are inlined, instead of being
referenced, into the schemas that use them in the resulting OAD (OpenAPI
Description) document.

.. _openapi-configuration-file:

Configuration File
------------------

``gen-openapi`` accepts a ``--config-file``/``-C`` YAML file in the format that
``gen-project`` reads (see :doc:`project-generator`), and reads only its
``generator_args.openapi`` section. Any option of the command can be set there,
keyed by its name with dashes as underscores, such as ``template``,
``keep_unreferenced``, ``inline_enums`` and ``openapi_version``. Options given on
the command line take precedence over the file, and a key that is not an option is
reported as a warning and ignored.

.. code-block:: yaml

    # api.yaml
    generator_args:
      openapi:
        template: api-template.yaml
        inline_enums: true

.. code:: bash

   gen-openapi -C api.yaml personinfo.yaml > personinfo.openapi.yaml

The same section carries two settings that are not options, which
``--create-template`` reads: ``expose`` and ``exclude`` choose the classes the API
exposes. The schema itself says nothing about the API, so one schema can serve
several APIs, each with its own file.

.. code-block:: yaml

    # api.yaml
    generator_args:
      openapi:
        template: api-template.yaml
        expose:
          subset: core
          classes:
            Risk: {path: /risks, operation_id: list_risks}
            Hazard: {crud: false}
        exclude: [Entity]

.. _openapi-create-template:

Creating a Template from the Schema
-----------------------------------

``--create-template`` prints a template for the classes the configuration file
exposes, which the generator then instantiates like a hand-written one:

.. code-block:: bash

   gen-openapi --create-template -C api.yaml risks.yaml > api-template.yaml
   gen-openapi -C api.yaml risks.yaml > risks.openapi.yaml

``--create-template`` cannot be given with ``--template`` on the command line. A
``template`` key in the configuration file is allowed, and the run that creates the
template does not read it, so one file can name the template that it creates.

The template holds structure only, so that it cannot drift from the schema:

* ``info`` takes the schema's ``title``, or its ``name`` when it has no title, its
  ``version``, or ``0.1.0`` when it has none, and its ``description``.
* Each exposed class gets a placeholder in ``components/schemas`` that carries
  ``type: object``, ``x-linkml-schema`` and ``x-linkml-source`` and nothing else.
* Each exposed class with ``crud`` on gets one ``GET`` path that returns a list of
  the class, with one query parameter per slot. A parameter carries ``in``,
  ``name``, ``required: false``, ``schema.type`` and
  ``x-linkml-source: <Class>.<slot>``, and no description, enum values or default.

When the template is instantiated, the component schemas are generated from the
schema with their descriptions and enum values, and a placeholder can still be
annotated by hand, as described under Template Annotations above. The query
parameters keep the bare type the template gives them. ``--openapi-version`` sets
the version the template declares, 3.0.3 by default, and the template is validated
against that version before it is printed. When ``expose`` names neither a subset
nor any classes, as without a configuration file, every class that is neither
abstract nor a mixin is exposed.

An excerpt of a created template, for the class ``Risk`` exposed at ``/risks``:

.. code-block:: yaml

    paths:
      /risks:
        get:
          summary: Get Risk
          operationId: list_risks
          parameters:
          - in: query
            name: severity
            required: false
            schema:
              type: string
            x-linkml-source: Risk.severity
          responses:
            '200':
              description: A list of Risk
              content:
                application/json:
                  schema:
                    type: array
                    items:
                      $ref: '#/components/schemas/Risk'
    components:
      schemas:
        Risk:
          type: object
          x-linkml-schema: https://w3id.org/linkml/my_schema
          x-linkml-source: Risk

Exposure
^^^^^^^^

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Setting
     - Effect
   * - ``expose.subset``
     - Exposes the classes the schema tags with this subset through ``in_subset``,
       leaving out abstract classes and mixins. When the subset also tags slots,
       the query parameters of every exposed class are narrowed to those slots.
   * - ``expose.classes``
     - Exposes each class it names, as stated, even an abstract class or a mixin:
       a listing of an abstract class returns the records of its subclasses, and a
       schema may give a mixin records of its own.
   * - ``exclude``
     - Removes classes from the exposed set. A class cannot be both named under
       ``expose.classes`` and excluded.
   * - ``crud: true``, the default
     - The class gets a placeholder and one list ``GET``.
   * - ``crud: false``
     - The class gets a placeholder and no path, for a class that only
       hand-written paths return.

An entry under ``expose.classes`` may set ``path``, ``operation_id`` and
``summary``. Otherwise they are derived from the class name, as
``/<class in lowercase>``, ``list_<class in lowercase>`` and ``Get <Class>``.

Query parameters come in the ``rank`` order of their slots, and slots without a
rank follow in schema order. A parameter is named as the generated schema names the
property, so by the slot's ``alias`` when it has one. Its type is ``integer``,
``number`` or ``boolean`` when the slot's range is an integer, a float, double or
decimal, or a boolean type, and ``string`` for any other type, for an enum, and for
a reference to a class, which is passed by its identifier.

The settings are checked before anything is printed. A key directly under
``expose`` other than ``subset`` and ``classes`` is an error, and so is a key in a
class entry that looks like a misspelling of ``path``, ``operation_id``,
``summary`` or ``crud``, such as ``operationId``. Any other key in a class entry is
left alone, so that a server reading the same file can keep its own settings beside
the class it serves. A class or a subset the schema does not declare is an error
too, and so are two exposed classes on one path.

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.openapigen:cli
    :prog: gen-openapi
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.openapigen

.. autoclass:: OpenApiGenerator
    :members: serialize, create_template
