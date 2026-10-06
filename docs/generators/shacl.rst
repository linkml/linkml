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


Rule constraints (SHACL-SPARQL)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

LinkML `rules <https://w3id.org/linkml/rules>`_ state conditional
constraints ("if slot A holds X, slot B must ..."), which property shapes
cannot express. The generator translates each rule into a
`SHACL-SPARQL constraint <https://www.w3.org/TR/shacl/#sparql-constraints>`_
(``sh:sparql``) on the node shape of its class, and of every subclass, since
a rule applies to all members of its class. ``--no-emit-rules`` turns this
off.

The constraint's query selects each focus node that satisfies the
preconditions and violates the postconditions. ``$this`` is the focus node
(`SHACL §5.3.1 <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_),
and each result names the postcondition's property and, where there is one,
the offending value (``sh:resultPath``, ``sh:value``).

Two patterns are recognised first:

* **Presence implies value**: precondition ``value_presence: PRESENT`` on a
  guard slot, and postcondition ``equals_string`` or ``equals_string_in`` on a
  target slot.
* **Exclusive value**: precondition ``has_member: {equals_string: V}``, and
  postcondition ``maximum_cardinality`` on the same slot. The older form
  with a bare ``equals_string: V`` precondition is read the same way, with a
  warning.

Any other rule with one postcondition slot is composed from the operators
its conditions use: ``value_presence``, ``required``, ``equals_string``,
``equals_string_in``, ``minimum_value``, ``maximum_value``,
``range_expression`` (slot conditions on the slot's class) and
``has_member``.

All translations follow the JSON Schema generator's ``if`` / ``then``:

* **Presence:** ``value_presence`` decides, then ``required``. Otherwise a
  precondition requires its slot, a postcondition requires its slot unless
  the rule is ``open_world``, and a condition inside a ``range_expression``
  or ``has_member`` does not.
* **Multivalued slots:** a condition holds when *every* value satisfies it.
  ``has_member`` holds when *some* value does.
* **Values:** ``equals_string`` and ``equals_string_in`` are compared as
  strings on enum and ``xsd:string`` slots, where an enum value with a
  ``meaning`` is compared as that IRI. On ``xsd:boolean`` slots they are
  compared as booleans and must be ``true``, ``false``, ``1`` or ``0``.
  ``minimum_value`` and ``maximum_value`` are inclusive bounds, translated
  only on slots whose datatype SPARQL compares as a number (``xsd:integer``,
  ``decimal``, ``float``, ``double`` and the types derived from them).

A rule outside these forms is skipped with a warning that names the rule and
the reason. It is never partially translated. ``deactivated`` rules are
ignored and ``bidirectional`` rules are skipped. For a rule with
``elseconditions``, only the if/then direction is emitted, and a warning
says so.

Example:

.. code-block:: yaml

    classes:
      Document:
        attributes:
          review_score:
            range: integer
          status:
            range: Status   # an enum: draft, approved, published
        rules:
          - description: A document scoring 4 or more must be approved or published.
            preconditions:
              slot_conditions:
                review_score:
                  minimum_value: 4
            postconditions:
              slot_conditions:
                status:
                  equals_string_in: [approved, published]

generates (abridged):

.. code-block:: turtle

    ex:Document a sh:NodeShape ;
        sh:sparql [ a sh:SPARQLConstraint ;
            sh:message "A document scoring 4 or more must be approved or published." ;
            sh:select """SELECT DISTINCT $this (<https://example.org/status> AS ?path) ?value WHERE {
        FILTER EXISTS { $this <https://example.org/review_score> ?pre0 . }
        FILTER NOT EXISTS { $this <https://example.org/review_score> ?pre0 . FILTER ( !( COALESCE( isNumeric( ?pre0 ) && ?pre0 >= 4, false ) ) ) }
        { FILTER NOT EXISTS { $this <https://example.org/status> ?value . } }
        UNION { $this <https://example.org/status> ?value . FILTER ( !( COALESCE( ?value = "approved" || ?value = "published", false ) ) ) }
    }""" ] .

A ``Document`` with a ``review_score`` of 4 or more violates the constraint
if it has no ``status``, or once for each ``status`` other than ``approved``
or ``published``, which the result reports as ``sh:value``. SHACL processors
that support SHACL-SPARQL, such as ``pyshacl``, validate these constraints.


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
