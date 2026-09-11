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

LinkML `rules <https://linkml.io/linkml/schemas/advanced.html#rules>`_ express
cross-parameter, conditional validation ("if slot A holds X, slot B must
..."). Plain per-slot SHACL property shapes cannot express these, so the
generator translates recognised rule shapes into
`SHACL-SPARQL constraints <https://www.w3.org/TR/shacl/#sparql-constraints>`_
(``sh:sparql`` / ``sh:SPARQLConstraint``) on the class's ``sh:NodeShape``.
Generation is controlled by ``--emit-rules/--no-emit-rules`` (default: on).

Three named patterns are recognised first:

* **Boolean guard** — precondition ``value_presence: PRESENT`` on a value
  slot, postcondition ``equals_string: "true"`` on a *boolean-range* flag
  slot: if the value is present, the flag must be true.
* **Presence implies value** — precondition ``value_presence: PRESENT``,
  postcondition ``equals_string`` / ``equals_string_in`` on a target slot:
  if the guard is present, the target must hold one of the allowed values.
  Enum values resolve to their ``meaning`` IRIs; values without ``meaning``
  compare as string literals.
* **Exclusive value** — precondition ``equals_string`` and postcondition
  ``maximum_cardinality`` on the *same* multivalued slot: if the value is
  present, the slot has at most N values.

Combinations outside the named patterns are handled by a compositional
fallback that conjoins the preconditions and negates a single postcondition:
conditional-required (``required: true``), conditional-absent
(``value_presence: ABSENT``), numeric threshold preconditions
(``minimum_value`` / ``maximum_value``), a one-hop nested precondition into
an inlined child object (``range_expression.slot_conditions``), and
``has_member`` list membership.

The translation contract is *skip, never mis-translate*: a rule whose
conditions set any operator outside the translated set (including
expression-level ``any_of``/``all_of``/``none_of``/``exactly_one_of``), or
whose slot keys resolve to no slot, is skipped and logged at ``DEBUG``.
``deactivated`` rules are skipped; ``bidirectional``, ``open_world``, and
``elseconditions`` warn (the forward direction is emitted).

Example:

.. code-block:: yaml

    classes:
      Weather:
        slots: [sun_altitude, daytime]
        rules:
          - description: If sun_altitude is present, daytime must be day or twilight.
            preconditions:
              slot_conditions:
                sun_altitude:
                  value_presence: PRESENT
            postconditions:
              slot_conditions:
                daytime:
                  equals_string_in: [day, twilight]

generates (abridged):

.. code-block:: turtle

    ex:Weather a sh:NodeShape ;
        sh:sparql [ a sh:SPARQLConstraint ;
            sh:message "If sun_altitude is present, daytime must be day or twilight." ;
            sh:select """SELECT $this WHERE {
        $this <https://example.org/sun_altitude> ?value .
        OPTIONAL { $this <https://example.org/daytime> ?target . }
        FILTER ( !BOUND(?target) || ?target NOT IN (<https://example.org/Day>, <https://example.org/Twilight>) )
    }""" ] .

``$this`` is pre-bound to each focus node per
`SHACL §5.3.1 <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_.
Note that SPARQL-based constraints require a SHACL processor with
SHACL-SPARQL support (e.g. ``pyshacl`` with ``advanced=True``).


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
