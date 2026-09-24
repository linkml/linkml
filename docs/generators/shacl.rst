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
                shacl:pattern "^\\S+ \\S+" ],
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


Class Expressions
^^^^^^^^^^^^^^^^^

Class-level boolean expressions become the SHACL logical constraint components
their metamodel definitions map to (`SHACL §4.6
<https://www.w3.org/TR/shacl/#core-components-logical>`__):

==================  =====================================================
LinkML              SHACL, on the class's ``sh:NodeShape``
==================  =====================================================
``any_of``          ``sh:or`` over the member shapes
``all_of``          ``sh:and`` over the member shapes
``exactly_one_of``  ``sh:xone`` over the member shapes
``none_of``         one ``sh:not`` per member
==================  =====================================================

Each member becomes an anonymous node shape. ``is_a`` gives ``sh:class``, and
nested expressions recurse. Each entry of ``slot_conditions`` gives an
``sh:property`` whose path is that of the slot as induced for the class, so
``slot_usage`` applies:

* ``required``, ``value_presence`` and the cardinalities give ``sh:minCount`` /
  ``sh:maxCount``;
* ``minimum_value`` / ``maximum_value`` give ``sh:minInclusive`` /
  ``sh:maxInclusive``, and ``equals_number`` gives both, so that ``5`` also
  matches ``5.0``;
* ``pattern`` gives ``sh:pattern``;
* ``equals_string`` and ``equals_string_in`` give ``sh:in``; on an enum slot the
  values are the permissible values as the enum renders them, the IRI of their
  ``meaning`` where they have one;
* ``range`` gives the same class, type or enum constraint as a slot's range.

SHACL allows ``sh:minInclusive``, ``sh:maxInclusive``, ``sh:in`` and
``sh:pattern`` at most once per shape. Where one condition needs one of them
twice, for example ``minimum_value`` next to ``equals_number``, the second value
goes into an ``sh:and`` member of the property shape, where it applies to the
same values.

A slot condition constrains only the values that are present, so it also holds
when the slot is absent - unless ``required: true``, ``value_presence: PRESENT``
or a minimum or exact cardinality of at least 1 requires the slot. Inside
``none_of``, at any depth, a condition that constrains values requires the slot,
so that an absent slot is not rejected by the negation - unless the condition
decides presence itself, through ``required``, ``value_presence`` or a maximum
or exact cardinality of 0. The JSON Schema generator requires the slot in a
class's own ``none_of`` for every condition that sets neither ``required`` nor
``value_presence``.

.. code-block:: yaml

  GeodeticReferenceSystem:
    slots: [code, name]
    any_of:
      - slot_conditions:
          code:
            required: true
      - slot_conditions:
          name:
            required: true

.. code-block:: turtle

    ex:GeodeticReferenceSystem a sh:NodeShape ;
        sh:or ( [ sh:property [ sh:path ex:code ; sh:minCount 1 ] ]
                [ sh:property [ sh:path ex:name ; sh:minCount 1 ] ] ) ;
        ...

An expression is attached to the shape of the class that declares it. Like
every ``sh:targetClass``, it reaches instances of subclasses where the data
graph states the ``rdfs:subClassOf`` (`SHACL §2.1.3.2
<https://www.w3.org/TR/shacl/#targetClass>`__); the ``sh:class`` that ``is_a``
gives recognises instances of subclasses the same way, as it does for a slot's
range.

An operator whose members use anything else is skipped as a whole and logged as
a warning, because leaving out one member would change what the operator
admits. That covers, for example, ``has_member`` or a slot-level ``any_of``
inside a slot condition, a condition on a name that is not a slot, a condition
on the identifier slot (the node's IRI rather than a property), and
``equals_string`` on a slot whose range does not hold strings.


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
