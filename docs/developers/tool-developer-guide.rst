Tool Implementer Guide
======================

This guide is for developers of *generic* LinkML tools that operate
over the linkml metamodel, for example:

- Generic Web-based data submission tools driven by a LinkML schema
- Tools that produce or modify LinkML schemas
- Tools that analyze schemas or align schemas or schema elements
- Tools that auto-genete APIs from schemas
- Generic faceted data browsers that flexibly operate over multiple
  schemas (see `this draft <https://docs.google.com/document/d/1jOLRF_doeSomVxZD5H8Ig_WujQ-2sNxhvWBmojZos3o/edit>`_)
- Schema editors for LinkML itself


.. note:: This guide is *not* intended for developers of *specific*
          applications that are built for any one particular
          schema. For example, if I am building an application geared
          towards entering phenotypic data about patients then I may
          want to build that application around a schema for
          patients. In this case, my application isn't intended to
          work with other schemas, and hence does not need to know
          anything about the linkml metamodel.

An example of a generic-schema driven editing application is json-editor
`<https://github.com/json-editor/json-editor>`_, which provides a way
to create instance data for an arbitrary JSON-Schema.

[react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/)
is based on the same idea.

Another example is `DataHarmonizer
<https://github.com/cidgoh/DataHarmonizer>`_ which provides a
spreadsheet-like data entry interface for any "flat" LinkML schema.


General Considerations
----------------------

Any generic LinkML application will be driven by a LinkML *model*
(schema), which itself conforms to the `LinkML metamodel
<https://w3id.org/linkml>`_. It follows that these applications will
itself need to conform to that model.

One challenge is that the LinkML metamodel includes many different
features, not all of which may be required for a particular
application. See the section on Schema Conformance Levels for guidance
here, as this will help you target your application to a particular
profile.

Another challenge is working with schemas themselves. The native
syntax for LinkML is YAML, and YAML parsers are provided with all
major languages. However, you will likely need to do more than parse
the model. There is a lot of "business logic" associated with a
model. For example, the rules that govern
:doc:`inheritance and refinement of slots </schemas/inheritance>`.

For Python applications, the SchemaView library provides this business
logic, but currently this logic must be re-implemented for different
languages. This may be a concern if you are building web applications
in JavaScript. The section on Working with Other Languages addresses
this.

Another challenge with building generic applications is making these
configurable at the schema level for different domains. The section on
customization and application hints deals with this.

Finally, you may wish to target a different framework than LinkML
itself. For semantic web applications, ShEx or SHACL may be a good
choice to build applications from. One advantage of LinkML is that you
can author in LinkML and compile to these other frameworks. But there
are trade-offs here. See the section on Other Frameworks.


Schema Conformance Levels
-------------------------

LinkML is a rich language supporting extensible types, inheritance,
use of Linked Data IRIs, ontological enums, imports, rules, boolean
constructs. It can be daunting to consider building a tool that
supports all of this. Thankfully this is not necessary.

We are including support for the notion of "conformance levels" or
"profiles" to LinkML. This will allow applications to clearly state
what parts of the specification are supported, and for people
deploying the application to adapt accordingly.

.note:: An example use case is a simple questionnaire UI/application that is
        driven by a LinkML schema, where each question is a slot and
        each answer either free text or in the case of multiple
        choice, an enum. There is no need for inheritance in this
        case, so the application only needs to pay attention to
        elements in the schema such as `slots` and
        `permissible_values`.

Currently specific conformance levels in LinkML have not been defined,
but current thinking is to have different categories:

- A *structural* conformance level that pertains to logical parts of
  the schema

    * The minimal level would include `classes`, `attributes`, `range`
      and basic builtin types, as well as cardinalities
    * The next level would include class inheritance and slots, and
      basic enums
    * The level above this would include slot inheritance, and slot
      overrides with `slot_usage`
    * The highest level would include boolean expressions and rules

- A *metadata* conformance level that pertains to informational
  aspects of the schema that do not drive validation or inference

    * minimal metadata would include metaslots for `description`,
      `comments`
    * above this, a minimal semantic level would include class and
      slot uris, and mappings
    * the full level would include all possible metaslots

The LinkML framework provides some functionality for being able to do
transformations "down" levels. For example, a rich schema that uses
inheritance and `slot_usage` can be "rolled down" to a schema that
includes only leaf elements, with inferred slots materialized as
attributes. The resulting schema will be less rich, but may be
sufficient for certain kinds of applications.

See the YAML Generator for one such tool.

Other Languages
---------------

LinkML is programming language neutral. However, currently much of the
stack for introspecting schemas is written in Python.

For example, in Python, if you want a list of slots for that class you can use :attr:`class_slots
<linkml_runtime.utils.schemaview.SchemaView.class_slots>`. But
what if you are building a generic JavaScript data entry widget that
will work for any LinkML class?

There are a few broad approaches here:

- 1. Use the direct output of your language's YAML/JSON parser, and
  implement logic ad-hoc
- 2. Develop a full blown analog of the Python SchemaView class for
  your language
- 3. Write Python code to transform LinkML YAML into a native form
  geared for your application


The first approach may be easiest, but we would only recommend this
for simple schemas (low structural conformance -- see above).

If you are interested in approach 2, please make an issue on our
GitHub repo so we can coordinate! We may have suggestions for general
strategies for bootstrapping. And we may already have prototype
implementations for your language.

For example, we have a prototype Java code generator that can create
Java classes for any LinkML model. The LinkML metamodel is in LinkML,
so this can be used to make a Java object model for LinkML itself,
which can help bootstrap efforts to make domain logical libraries.

Materializing imports and inferences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The :doc:`linkml generator <../generators/linkml>` can be used to
materialize imports closure and to materialize inferred/induced slots
as attributes. This frees the client logic from needing to implement
this logic locally.


General Guidelines for applications
-----------------------------------

These guidelines apply to how applications should use elements of the
LinkML metamodel.

- Applications should use `title <https://w3id.org/linkml/>`_ to
  obtain the user-friendly name for a slot. For example a
  spreadsheet-like data entry tool should display these as column
  headers
- If `title` field is not available, use the `name` slot
- The `description <https://w3id.org/linkml/description>`_ slot should
  be used to provide information to users, e.g. as tool-tips
- The `pattern <https://w3id.org/linkml/pattern>`_ slot should be used
  to constrain values entered by the user
- The `required <https://w3id.org/linkml/required>`_ slot should be used
  to indicate to users if a field is not filled in. Applications MAY
  choose to still allow such data to be saved, e.g. if the user is in
  an intermediate state
- The `multivalued <https://w3id.org/linkml/multivalued>`_ slot should
  be used to indicate whether data should be inputted or displayed as
  a list/set
- The `range <https://w3id.org/linkml/range>`_ slot should
  be used to constrain values for a slot. The application should also
  apply relevant logic to this calculation depending on conformance
  level supported.
- The URI of a construct may be used to provide links for a user to
  find more information in an element. For example, in a data entry
  form a column may have a hyperlink to complete documentation on that
  data dictionary element
- An application may use the primary URI of a concept or its mappings
  to look up semantics for the type and behave appropriately (see
  examples with geolocation below)
- Minimally, data entry applications should treat enums as dropdowns
  or radio-button selectors
- In a data entry application, a slot that is multivalued and has a
  range of an enum may be implemented as a multi-select.
- Enums that take exactly two possible permissible values may be
  displayed as toggles
- Applications may choose to use standard ontology browsers such as
  OLS or BioPortal, or standard query endpoints to obtain more
  information on enums. See below.


Slots that may potentially be added to provide applications with
hints:

- precedence order
- grouping categories



Customizing and application hints
---------------------------------

One challenge with generic applications is that they often look and
feel... generic. This can have some advantages, e.g. consistent look
and feel. But in general UX can be improved by customizing things.

There are three broad approaches:

- 1. Make a custom application, with custom domain logic implemented programmatically
- 2. Define configuration files
- 3. Add schema hints

The first approach is out of scope for this guide -- but if you do go
down this route, the LinkML framework provides various utilities that
may help, such as the ability to generate custom language bindings.

The other two approaches are fairly similar and involve providing a
mechanism for a generic application to customize look, feel, and
behavior in a way that doesn't require changing software/code.

External Configuration
^^^^^^^^^^^^^^^^^^^^^^

External configuration files may be best for "style sheet" type
configurations for controlling colors, shapes, sizes, etc. These could
potentially be tweaked by an individual user.

It is easy to roll your own configuration format, but we would
recommend creating a schema for your configuration data model. An
example of this is `KGViz Schema
<https://berkeleybop.github.io/kgviz-model/>`_ which is a stylesheet
language for visualizing ontology graphs, based on `Graphviz<https://graphviz.org/>`.

Schema Hints
^^^^^^^^^^^^

Schema hints embed additional information in the schema itself. In
contrast to external configurations, this is harder for a user to
change, and so is best suited for 'centralized' configuration.

A simple example might be a slot that takes a string as range. A
generic data entry application has no way of knowing how big a text
entry box to provide, and whether this should accept single-line or
multi-line output. The application could 'play it safe' and give the
user a large multi-line box, but this would be poor UX if the string
field is always a 3-letter code.

LinkML allows for slots and types to be annotated with information
that would serve as hints for applications. It is up to you the level
of granularity you provide here. However, specifying the precise
number of rows and columns may be embedding too much application logic
in the schema. Instead we encourage thinking of "semantic types". For
example, you could define two types:

.. code-block:: yaml

  types:

    NameString:
      typeof: string
      pattern: "^[^\\n]$"
      description: A description that holds a human readable name
      comments:
       - This is designed to support different styles of names from
         multiple languages, but certain characters such as newlines are
         never in names

    FormattedString:
      typeof: string
      description: >-
        A string in which characters such as newlines are
        permitted and used for formatting

  slots:
    full_name:
      range: NameString
    address:
      range: FormattedString



And then hardcode these types into the application.

A more flexible approach would be instead to use annotations on the
types:

.. code-block:: yaml

  types:

    NameString:
      typeof: string
      pattern: "^[^\\n]$"
      description: ...
      annotations:
        dash.singleLine: true

    FormattedString:
      typeof: string
      description: ...
      annotations:
        dash.singleLine: false



This is better as you can reuse the same vocabulary on different
types, and you introduce decoupling between specific schemas and your
application.

In this case, we are reusing the `dash vocabulary
<https://datashapes.org/forms.html>`_ which is intended for exactly
this kind of purpose. Furthermore, if you compile your schema to SHACL
then it will have the dash annotations, allowing you to leverage
generic SHACL applications (next section).

Using ontologies and standard vocabularies to drive behavior
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Consider a schema that reuses standard vocabularies such as wgs84 for
slots:


.. code-block:: yaml

  prefixes:
    wgs: http://www.w3.org/2003/01/geo/wgs84_pos#
    schema: http://schema.org/

  slots:
    latitude:
      domain: geolocation value
      range: decimal degree
      description: >-
        latitude
      slot_uri: wgs:lat
      exact_mappings:
        - schema:latitude

    longitude:
      domain: geolocation value
      range: decimal degree
      description: >-
        longitude
      slot_uri: wgs:long
      exact_mappings:
        - schema:longitude


Applications may choose to have specific behavior for lat-long fields,
for example, including a map widget. Applications may also choose to
use mappings as well as the primary URI.

Handling enums
^^^^^^^^^^^^^^

In addition to the general guidance above, applications may allow for
custom behavior with enums.

Applications may choose to display enum permissible values as a
hierarchy, especially if there are many permissible values. The
hierarchy is not provided in the schema itself, but additional APIs or
ontology files can be used. The choice of which relationship types to
display in the hierarchy may be ontology or application dependent but
applications are encouraged to use standard annotations from an
ontology like OMO.

For open-ended enums or enums with very many permissible values,
applications may choose to use an autocomplete service from an
existing ontology. This has the advantage of lookup on multiple
different aliases. However, note the autocomplete service may return
more values than are present in the permissible value list.


Handling units and quantities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are a wide variety of ways to model quantities, and these are
use case dependent. Is it important to capture ranges or
precision/error bars? Is the unit baked in to the slot, or does the
user specify this? Is the quantity captured as a single parseable text
string, or is a complex object used?

The modeling decisions will vary based on the use case. However, if
certain conventions are followed, then generic applications can be made
'smart'.

For example, if we model quantity values as classes and reuse the
concept from the standard `qudt<http://qudt.org/>` vocabulary:

.. code-block:: yaml

    quantity value:
      description: >-
        A simple quantity, e.g. 2cm
      attributes:
        verbatim:
          description: >-
            Unnormalized atomic string representation, should in syntax {number} {unit}
        has unit:
          description: >-
            The unit of the quantity
          slot_uri: qudt:unit
        has numeric value:
          description: >-
            The number part of the quantity
          range:
            double
      class_uri: qudt:QuantityValue
      mappings:
        - schema:QuantityValue



Then applications can be aware of the semantics of this field and act
accordingly; for example:

 - allow free text entry and use a library like `quantulum<https://github.com/marcolagi/quantulum>` to parse
   into structured form
 - allow for conversion between units
 - use sliders to allow input
 - etc


Using other frameworks
----------------------

You should also feel free to build applications that use other
frameworks. You can compile to these from LinkML, but be aware that
you will be restricted to the expressivity of that language--e.g. a
project like json-edit can only make use of what is expressible in
JSON Schema.

If considering a non-LinkML framework for form-based data entry we
would strongly recommend SHACL + DASH. See `Form Generation using
SHACL and DASH <https://datashapes.org/forms.html>`_.
