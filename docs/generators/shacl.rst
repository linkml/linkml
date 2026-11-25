SHACL
======

.. warning:: Beta implementation, some features may change

Example Output
--------------

`personinfo.shacl.ttl <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/shacl/personinfo.shacl.ttl>`_

Overview
--------

`SHACL <https://www.w3.org/TR/shacl/>`__ (Shapes Constraint Language) is a language for validating RDF graphs against a set of conditions

To run:

.. code:: bash

   gen-shacl personinfo.yaml > personinfo.shacl.ttl



Docs
----

Example Input:

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

Example Output:

.. code-block:: turtle

    <https://w3id.org/linkml/tests/kitchen_sink/Person> a shacl:NodeShape ;
        shacl:closed true ;
        shacl:ignoredProperties ( rdf:type ) ;
        shacl:property [ shacl:class <https://w3id.org/linkml/tests/kitchen_sink/BirthEvent> ;
                shacl:maxCount 1 ;
                shacl:nodeKind shacl:BlankNode ;
                shacl:path <https://w3id.org/linkml/tests/kitchen_sink/has_birth_event> ],
            [ shacl:maxCount 1 ;
                shacl:maxInclusive 999 ;
                shacl:minInclusive 0 ;
                shacl:path <https://w3id.org/linkml/tests/kitchen_sink/age_in_years> ],
            [ shacl:class <https://w3id.org/linkml/tests/kitchen_sink/FamilialRelationship> ;
                shacl:nodeKind shacl:BlankNode ;
                shacl:path <https://w3id.org/linkml/tests/kitchen_sink/has_familial_relationships> ],
            [ shacl:maxCount 1 ;
                shacl:path <https://w3id.org/linkml/tests/core/name> ;
                shacl:pattern "^[^\\s\u0085\u00A0\u1680\u2000-\u200A\u2028-\u2029\u202F\u205F\u3000]+ [^\\s\u0085\u00A0\u1680\u2000-\u200A\u2028-\u2029\u202F\u205F\u3000]+" ],
            [ shacl:class <https://w3id.org/linkml/tests/kitchen_sink/MedicalEvent> ;
                shacl:nodeKind shacl:BlankNode ;
                shacl:path <https://w3id.org/linkml/tests/kitchen_sink/has_medical_history> ],
            [ shacl:class <https://w3id.org/linkml/tests/kitchen_sink/Address> ;
                shacl:nodeKind shacl:BlankNode ;
                shacl:path <https://w3id.org/linkml/tests/kitchen_sink/addresses> ],
            [ shacl:maxCount 1 ;
                shacl:path <https://w3id.org/linkml/tests/core/id> ],
            [ shacl:path <https://w3id.org/linkml/tests/kitchen_sink/aliases> ],
            [ shacl:class <https://w3id.org/linkml/tests/kitchen_sink/EmploymentEvent> ;
                shacl:nodeKind shacl:BlankNode ;
                shacl:path <https://w3id.org/linkml/tests/kitchen_sink/has_employment_history> ] ;
        shacl:targetClass <https://w3id.org/linkml/tests/kitchen_sink/Person> .


Patterns
^^^^^^^^

A LinkML ``pattern`` is a Python regular expression, and a value conforms where Python's
``re.search`` finds it. SHACL's ``sh:pattern`` is an XPath regular expression
(`SHACL §4.4.3 <https://www.w3.org/TR/shacl/#PatternConstraintComponent>`__,
`XPath Functions 3.1 §5.6 <https://www.w3.org/TR/xpath-functions-31/#regex-syntax>`__), which
is also searched in the value but reads some constructs differently, while Python-based engines
such as pyshacl compile it with Python's ``re``. The generator writes each pattern in forms that
both read with Python's meaning: ``.`` as ``[^\n]``, ``\s`` and ``\S`` as explicit character
classes (in the example above), ``(?:`` as a group, ``{,n}`` as ``{0,n}``, a literal ``{`` or
``}`` escaped, and an escape that XPath does not have, such as ``\/``, as the character itself.
Two constructs stay as written, as no form reads alike in both:

* ``\w`` and ``\W``: XPath's ``\w`` excludes ``_`` and includes symbols, and Python's ``re``
  has no ``\p{...}`` to write Python's ``\w`` with;
* ``$``: Python's ``$`` also matches before a final line feed, XPath's only at the end.

A pattern with a construct XPath does not have, such as a lookahead or a backreference, is
written as it is. ``equals_string`` and ``equals_string_in`` become ``sh:in``, also on a type.
A shape has at most one ``sh:in``, so where a slot, its type or enum and its expanded
``subproperty_of`` give more than one list, the one list holds the values that all of them allow.


Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.shaclgen

.. click:: linkml.generators.shaclgen:cli
    :prog: gen-shacl
    :nested: short

Code
^^^^


.. autoclass:: ShaclGenerator
    :members: serialize
