ER Diagrams
===========

Overview
--------

Entity-Relationship (ER) Diagrams are a graphical representation of the structure of a schema.

LinkML uses the `Mermaid ER Diagram <https://mermaid.js.org/syntax/entityRelationshipDiagram.html>`_
syntax to represent ER diagrams.

To run:

.. code:: bash

   gen-erdiagram personinfo.yaml

This will generate a single markdown-ready ER diagram file, that can be embedded
in a mkdocs or sphinx site, or included in a GitHub issue.

By default, the output includes markdown fence blocks:

.. code:: markdown

    ```mermaid
    erDiagram
       ...
    ```

To generate the mermaid without the fencing block, use ``--format mermaid``:

.. code:: bash

   gen-erdiagram --format mermaid personinfo.yaml

Customization
-------------

The default behavior is:

* Check if the schema has a `tree root <https://w3id.org/linkml/tree_root>`_ assigned

    * If assigned, then include this entity, and everything reachable from it
    * If not assigned, then include all entities

Here, "reachable" means reachable via `inlined <https://w3id.org/linkml/inlined>`_ references

If you want to draw a diagram for a particular class, and all reachable nodes,
you can pass these on the command line:


.. code:: bash

   gen-erdiagram personinfo.yaml -c MedicalEvent

This generates:

.. mermaid::

    erDiagram
    MedicalEvent {
        date started_at_time
        date ended_at_time
        float duration
        boolean is_current
    }
    ProcedureConcept {
        string id
        string name
        string description
        string image
    }
    DiagnosisConcept {
        string id
        string name
        string description
        string image
    }

    MedicalEvent ||--|o Place : "in_location"
    MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
    MedicalEvent ||--|o ProcedureConcept : "procedure"

By default, only inlined references are followed. State ``--follow-references`` to also
follow non-inlined references.

For large ER diagrams, to get a big-picture overview, you may want to exclude attributes:

.. code:: bash

   gen-erdiagram personinfo.yaml -c Person --exclude-attributes

Generates:

.. mermaid::

    erDiagram
    Person {

    }
    MedicalEvent {

    }
    ProcedureConcept {

    }
    DiagnosisConcept {

    }
    FamilialRelationship {

    }
    EmploymentEvent {

    }
    Address {

    }

    Person ||--|o Address : "current_address"
    Person ||--}o EmploymentEvent : "has_employment_history"
    Person ||--}o FamilialRelationship : "has_familial_relationships"
    Person ||--}o MedicalEvent : "has_medical_history"
    MedicalEvent ||--|o Place : "in_location"
    MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
    MedicalEvent ||--|o ProcedureConcept : "procedure"
    FamilialRelationship ||--|| Person : "related_to"
    EmploymentEvent ||--|o Organization : "employed_at"



Also you can include upstream entities into selected entities diagram.
This is helpful for creating smaller, focused diagrams that display the immediate
neighborhood of a selected class.

For example this

.. code:: bash

   erdiagramgen  kitchen-sink.yaml -c MedicalEvent --max-hops 0 --include-upstream --exclude-attributes

Generates:

.. mermaid::

    erDiagram
    MedicalEvent {
    }
    Person {
    }
    DiagnosisConcept {
    }
    ProcedureConcept {
    }

    MedicalEvent ||--|o Place : "in location"
    MedicalEvent ||--|o DiagnosisConcept : "diagnosis"
    MedicalEvent ||--|o ProcedureConcept : "procedure"
    MedicalEvent ||--|o AnyObject : "metadata"
    Person ||--}o MedicalEvent : "has medical history"


Limitations
-----------

* There is currently no way to directly generate PNGs/PDFs/etc from the mermaid code.
  You can use the `mermaid live editor <https://mermaid-js.github.io/mermaid-live-editor>`_
  to generate these.

* The mermaid diagrams are not yet directly integrated into the documentation generated
  by ``gen-docs``.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.erdiagramgen

.. click:: linkml.generators.erdiagramgen:cli
    :prog: gen-erdiagram
    :nested: short

Code
^^^^

.. autoclass:: ERDiagramGenerator
    :members: serialize, serialize_classes
