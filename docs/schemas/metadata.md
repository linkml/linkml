# Schema Element Metadata

There are various slots that can be used to provide metadata about
either a schema or elements of a schema. These typically don't affect
the semantics of the model, but rather act as annotations that can be
used to provide more information to people, or that can guide the
behavior of some tools.

## Providing descriptions

The [description](https://w3id.org/linkml/description) slot can be used to provide a human-readable description of any schema element

```yaml
  Person:
    is_a: NamedThing
    description: >-
      A person (alive, dead, undead, or fictional).
```

descriptions can include markdown

```yaml
  Person:
    is_a: NamedThing
    description: |-
      A human being including those that are:
         * alive
         * dead
         * undead
         * fictional
```

However, this is only recommended for schema descriptions.

This [guide to yaml formatting](https://yaml-multiline.info/) may be helpful

## Providing aliases

The [aliases](https://w3id.org/linkml/aliases) slot can be used to define a list of aliases for a class or slot. This is useful for adding synonymous names to your class (or slot), that serve either as hints for human users, or to enhance search and findability over your model

Example:

```yaml
Person:
  aliases:
    - human being
    - individual
```

In practice, aliases are used to help interpret the model, not as an equivalent name for a class or slot name.
Downstream tooling could use these aliases to help users query the model for example, but the LinkML tooling does not consider
aliases and element names interchangeable.

## Structured aliases

Sometimes you may want to include additional information about an alias

```yaml
Person:
  structured_aliases:
    - literal_form: Homo sapiens
      alias_predicate: skos:exactMapping
      source: Linnaeus
  - literal_form: Persona
      alias_predicate: skos:exactMapping
      source: Google Translate
      in_language: es
```

## Deprecating elements

Any schema element can be deprecated, with a reason provided; optionally, a replacement can be provided

```yaml
classes:
  Agent:
    deprecated: the concept of Agent was too abstract, use Person instead
    deprecated_element_has_exact_replacement: Person
```

## Specifying units

You can use the [unit](https://w3id.org/linkml/unit) element to annotate a slot
as holding a value in a particular unit:

```yaml
slots:
  height_in_cm:
    range: float
    unit:
      ucum_code: cm
```

In this case we are annotating the `height_in_cm` slot with a unit, where that unit is
itself described as having a [UCUM](https://ucum.org/) code of `cm`.

__Note__: embedding the unit in the name of the slot *as well* as the explicit annotation may seem redundant.
However, in most scenarios it is good practice to make a measurement slot unambiguous, unless it can be guaranteed
that the data will never be separated from the LinkML schema / data dictionary.

You can use a number of different systems for specifying the unit, including:

- UCUM
- QUDT
- IEC61360 codes
- Arbitrary ontology or vocabulary CURIEs, taken from sources like:
   - [UO](https://obofoundry.org/ontology/uo)
   - [NCIT](https://obofoundry.org/ontology/ncit)
   - [OM](https://bioportal.bioontology.org/ontologies/OM)
   - [UOM](https://w3id.org/uom/)

Additionally, you can specify what kind of quantity is being measured,
using an ontology.

For example:

```yaml
prefixes:
  linkml: https://w3id.org/linkml/
  UO: http://purl.obolibrary.org/obo/UO_
  PATO: http://purl.obolibrary.org/obo/UO_
  qudt: http://qudt.org/schema/qudt/
  uom: https://w3id.org/uom/

slots:
  height_in_cm:
    range: float
    unit:
      ucum_code: cm
      iec61360code: UAA375
      exact_mappings:
        - UO:0000015 ## centimeter
        - uom:cm
      has_quantity_kind: PATO:0000119 ## height
```

If you must, you can omit any kind of formal description altogether and simply
provide a symbol.


You can also declare your own primitive types extending float, double, decimal, or integer,
and describing these with a unit element. This type can then be used in multiple
different slots.

For example:

```yaml
types:
  KilogramValue:
    typeof: float
    unit:
      ucum_code: kg
```

Specifying the unit doesn't affect the behavior of the slot or type, but it's a useful way of
formally specifying the intended use of a slot, and provides a potential hook for interoperation
and automated data model mapping.

## Other metadata slots

See [CommonMetadata](https://w3id.org/linkml/CommonMetadata) for other slots
