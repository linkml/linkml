OWL
===

Example Output
--------------

`personinfo.owl.ttl <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/owl/personinfo.owl.ttl>`_

Overview
--------

Web Ontology Language
`OWL <https://www.w3.org/TR/2012/REC-owl2-overview-20121211/>`_ is a
modeling language used to author ontologies.

OWL is used for building *ontologies*, whereas LinkML is a *schema*
language. Nevertheless, it can be useful to render Schemas as OWL (and
in fact many semantic web schemas such as PROV have an OWL or RDFS
rendering)


.. seealso:: The `linkml-owl <https://github.com/linkml/linkml-owl>`_
             maps between LinkML *data* and OWL

.. note:: The OWL is rendered as RDF/turtle. We recommend the suffix
          ``.owl.ttl`` to distinguish from the direct RDF mapping


Mapping
^^^^^^^

* Each LinkML class maps to an OWL class
* Each LinkML slot maps to an OWL property

    - if the range of the slot is class, then an ObjectProperty is used
    - otherwise DataProperty is used
    - Exception to the above: if ``type_objects`` is set then ObjectProperties are always used;
      instead of having ranges of type be mapped to literals, these map to class-shadows of
      literals, that have a data property ``value``.
      This can be useful in some scenarios - for example, if you want to use the same property and
      allow *either* literals or objects as values.

* OWL *restrictions* are used for cardinality and range constraints

    - ``only`` (universal restrictions) is used for ranges
    - If a slot is not `multivalued` then ``max 1`` cardinality
      restrictions are used
    - required non-multivalued slots have an ``exactly 1`` cardinality restriction
    - required slots have a ``min 1`` cardinality restriction
    - non-required slots have a ``min 0`` cardinality restriction. Note that formally
      this is tautological and not necessary. However, adding this axiom helps make the intention
      explicit.
    - it should be understood that OWL follows the Open World
      Assumption, thus OWL reasoners enforce a weaker model

* By default both ``is_a`` and ``mixins`` are mapped to ``rdfs:subClassOf``

    - Use ``--mixins-as-expressions`` to treat mixins as existential axioms

* Each LinkML element is rendered as an instance of the relevant metamodel class

    - This means *punning* is used
    - Set ``--no-metaclasses`` if you do not want this behavior
    - Set ``--add-root-classes`` to add a root class for each metamodel class



.. note:: The current default settings for ``metaclasses`` and ``type-objects`` may change in the future

Enums and PermissibleValues
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Enums and PermissibleValues are treated as *classes* by default. An enum has a *definition* added using
an OWL ``UnionOf`` construct.

* Use ``--default-permissible-value-type`` to change the default type
* Use ``--enum-iri-separator`` to change the separator character in the enum IRI which is ``#`` by default

You can make an enum represent individuals by adding an ``implements`` slot assignment:

.. code-block:: yaml

    enums:
      HomePlanetType:
        implements:
         - owl:NamedIndividual
        description: The type of home planet
        permissible_values:
          Earth:
          Venus:


Tips
^^^^

If you wish to produce an OWL file that is primarily for browsing or release on an ontology portal
such as the Ontology Lookup Service (OLS) or OntoPortal/BioPortal, then consider using the
``--add-root-classes`` option to make the ontology more navigable.

If ``gen-owl`` is run on PersonInfo *without* this option it results in a flat structure
that is faithful and isomorphic to the existing schema:

.. code-block::

    * GenderType
    * FamilialRelationshipType
        * CHILD_OF
        * PARENT_OF
        * ...
    * Relationship
        * FamilialRelationship
    * Event
        * EmploymentEvent
        * MedicalEvent
    * NamedThing
        * Concept
    * HasAliases

Running with the option:

.. code-block::

    * EnumDefinition
        * GenderType
        * FamilialRelationshipType
    * ClassDefinition
        * Relationship
            * FamilialRelationship
        * Event
            * EmploymentEvent
            * MedicalEvent
        * NamedThing
            * Concept
        * HasAliases
    * PermissibleValue
        * CHILD_OF
        * ...

If your schema is heavy on mixins, the resulting polyhierarchy can be hard to navigate. In this case,
using ``--mixins-as-expressions`` will restrict the main subClassOf backbone to be purely ``is_a``
relationships. Mixin relationships will be modeled using existential restrictions (some values from).
OWL General Class Inclusion (GCI) axioms will be used to preserve semantics.

For example, on PersonInfo the default conversion yields:

.. code::

    Class: Person
      SubClassOf: NamedThing, HasAlias, ...
    Class: HasAlias
      SubClassOf: aliases only xsd:string, ...
    ...

Using ``--mixins-as-expressions`` gives:

.. code::

    Class: Person
      SubClassOf: NamedThing, mixins some HasAlias, ...
    Class: HasAlias
    GCIs:
      (mixins some HasAlias) SubClassOf: aliases only xsd:string, ...
    ...

Semantics of mapping from LinkML
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generated OWL should be a faithful open-world rendering of the LinkML schema. This means that it may not be
*complete* for the purposes of data validation. If a slot is not required, then an OWL reasoner will infer
the presence of a slot value, even if not explicitly stated. However, it does not treat this as an error.

Nevertheless, it can be informative to translate schemas with rich logical information to OWL, combine these
with data converted to RDF, and then perform reasoning. If you use an ontology development environment
like Protege, this can be an intuitive way of debugging errors with your schema.

Note that currently only a subset of LinkML rules can be expressed as OWL. In future, we may
add support to generate auxhiliary SWRL files including rules.

Pitfalls
^^^^^^^^

Many OWL tools such as those based on the OWL API are intended to consume a [profile](https://www.w3.org/TR/owl2-profiles/)
of OWL called OWL-DL. It's relatively easy to create LinkML that can't be *directly* expressed in
OWL-DL, and the resulting RDF triples are said to be [OWL Full](https://www.w3.org/TR/owl2-overview/#Semantics).

For example, if you have slots in your schema that have an `Any`
range, then there is no direct translation of that slot to an OWL-DL
property, since each property needs to explicitly commit to being a
`DatatypeProperty` or `ObjectProperty` in OWL-DL.

Other examples
^^^^^^^^^^^^^^

- `Biolink <https://bioportal.bioontology.org/ontologies/BIOLINK>`_ :
  translation of Biolink schema to OWL


Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.owlgen

.. click:: linkml.generators.owlgen:cli
    :prog: gen-owl
    :nested: short

Code
^^^^


.. autoclass:: OwlSchemaGenerator
    :members: serialize
