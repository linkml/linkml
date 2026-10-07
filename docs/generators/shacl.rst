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

Each member becomes an anonymous node shape. ``is_a`` names a class that every
instance of the shape's class belongs to (the class itself or an ancestor), and
then adds nothing; one that only some instances belong to, because a descendant
of the class has it among its ancestors, and then gives ``sh:class``; or one that
none belongs to, and then gives a shape nothing conforms to. An instance belongs
to its class and that class's ancestors, by ``is_a`` and by ``mixins``, so a
class that may also be another is declared as a subclass with that mixin. For a
type or an enum, ``is_a`` gives its value constraint. Nested expressions recurse.
Each entry of ``slot_conditions`` gives an
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
* ``range`` gives the same class, type or enum constraint as a slot's range;
* ``range_expression`` gives an ``sh:node``, as described under
  `Range Expressions`_;
* ``has_member`` gives an ``sh:qualifiedValueShape``, as described under
  `Members`_.

A shape may have at most one value of ``sh:minInclusive``, ``sh:maxInclusive``
or ``sh:in``, and of ``sh:pattern``, whose component also takes ``sh:flags``
(`SHACL §2.1.1 <https://www.w3.org/TR/shacl/#constraints>`__). Where one condition
needs one of them twice, for example ``minimum_value`` next to
``equals_number``, the second value goes into an ``sh:and`` member of the
property shape, where it applies to the same values.

A slot condition is unknown for an absent slot unless it decides whether the slot
may be absent, and an instance violates an expression only when the expression is
definitely false, as described under "Class-level expressions and absent slots" in
:doc:`Advanced features </schemas/advanced>`.
The JSON Schema generator reads them the same way. In SHACL, each expression gets
its "not false" form, and, under ``sh:not``, its "definitely true" form, where
such a condition also requires its slot (``sh:minCount 1``). ``exactly_one_of``
becomes ``sh:xone`` over the "definitely true" forms of its members.

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

A class expression constrains every instance of its class, so the shape of a
class carries the expressions of its ancestors and mixins as well, as it carries
their slots. Each is translated in the context of that class, where
``slot_usage`` applies. A node typed only with a subclass, as ``rdflib_dumper``
and the JSON-LD context produce it, is therefore checked without an
``rdfs:subClassOf`` triple in the data. The ``sh:class`` that ``is_a`` gives
recognises instances of subclasses only where the data graph states the
``rdfs:subClassOf`` (`SHACL §4.1.1
<https://www.w3.org/TR/shacl/#ClassConstraintComponent>`__), as it does for a
slot's range.

An operator whose members use anything else is skipped as a whole and logged as
a warning, because leaving out one member would change what the operator
admits. That covers, for example, ``all_members``, ``equals_expression`` or a
slot-level ``any_of`` inside a slot condition, a condition on a name that is not a slot, a condition
on the identifier slot (the node's IRI rather than a property), and
``equals_string`` on a slot whose range does not hold strings.


Range Expressions
^^^^^^^^^^^^^^^^^

A slot's `range_expression <https://w3id.org/linkml/range_expression>`__
constrains each of its values as a class-level expression constrains an
instance: its conditions constrain the slots of the value as induced for the
range class, and a value violates it only when it is definitely false. It
becomes an ``sh:node`` (`SHACL §4.7.1
<https://www.w3.org/TR/shacl/#NodeConstraintComponent>`__) on the property shape,
next to the range's ``sh:class``, so it constrains only the values of this slot,
and matching it doesn't make a node an instance of the range. The JSON Schema
generator reads it the same way.

.. code-block:: yaml

   classes:
     Document:
       slots: [license]
       slot_usage:
         license:
           range_expression:
             slot_conditions:
               category:
                 required: true
                 equals_string: license
     Resource:
       slots: [category]
   slots:
     license:
       range: Resource
     category:
       range: string

.. code-block:: turtle

   ex:Document a sh:NodeShape ;
       sh:property [ sh:path ex:license ;
               sh:class ex:Resource ;
               sh:node [ sh:property [ sh:path ex:category ;
                           sh:minCount 1 ;
                           sh:in ( "license" ) ] ] ;
               ... ] ;
       ...

A class alternative in a slot's ``any_of`` can carry its own
``range_expression``, and so can a slot condition, where the expression takes
the form of the condition: under ``sh:not``, its "definitely true" form. For
values that aren't instances of a class, an expression can combine types and
enums with ``is_a``, for example ``any_of: [{is_a: OpenLicense}, {is_a:
ProprietaryLicense}]``; such values have no slots for a condition to constrain.
An expression that uses anything SHACL can't express (see above) is skipped and
logged as a warning.

A value that is a reference is checked against its description in the data
graph, as ``sh:class`` is. The JSON Schema generator can't check it, because
there the value is just an identifier.


Members
^^^^^^^

A multivalued slot's `has_member <https://w3id.org/linkml/has_member>`__ asks
for at least one value that satisfies an expression. It becomes an
``sh:qualifiedValueShape`` with ``sh:qualifiedMinCount 1`` (`SHACL §4.7.3
<https://www.w3.org/TR/shacl/#QualifiedValueShapeConstraintComponent>`__), so
the other values need only satisfy the slot's own constraints. The member
expression constrains one value: its value operators, ``range`` and
``range_expression`` apply.

.. code-block:: yaml

   slots:
     tags:
       range: string
       multivalued: true
       has_member:
         equals_string: reviewed

This accepts ``[reviewed, pending]`` and rejects ``[pending]``. A slot without a
value, absent or empty, has no member, so it fails ``has_member``, as the JSON
Schema generator also reads it. In a slot condition of a class-level expression,
``has_member`` therefore decides whether the slot may be absent, and the member
takes the form of the condition. Several conditions with ``has_member`` may be
satisfied by the same value. A ``has_member`` on a slot that isn't multivalued,
or one that uses anything else, is skipped and logged as a warning.


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
