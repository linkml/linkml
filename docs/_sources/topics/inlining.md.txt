# Inlining objects

LinkML allows control over whether objects should be *inlined* or *referenced* in JSON-style representations using the [inlined](https://w3id.org/linkml/inlined) slot.

## Example

For example, given a model with a Organism class that can reference other Organism classes:

```yaml
classes:
  Organism:
    attributes:
      id:
        identifier: true
      name:
        range: string
      has_subtypes:
        range: Organism
        multivalued: true
```

for example, the object for "mammals" may be logically related to objects for "primates" and "cats" via the `has_subtypes` slot. This logical relationship can be serialized in the following different ways:

## No inlining, reference by key

schema:

```yaml
      has_subtypes:
        range: Organism
        multivalued: true
        inlined: false
```

example data:

```yaml
- id: NCBITaxon:40674
  name: mammals
  has_subtypes:
    - NCBITaxon:9443
    - NCBITaxon:9682
    - ...
- id: NCBITaxon:9443
  name: primates
  has_subtypes:
    - NCBITaxon:9606
    - ...
```

Here the range of the has_subtypes slot is a list of strings, where each string is a *reference* to a separate object

## Inlining as a list

schema:

```yaml
      has_subtypes:
        range: Organism
        multivalued: true
        inlined: true
        inlined_as_list: true
```

data:

```yaml
- id: NCBITaxon:40674
  name: mammals
  has_subtypes:
    - id: NCBITaxon:9443
      name: primates
      has_subtypes:
        - id: NCBITaxon:9606
          name: humans
        - id: NCBITaxon:9682
          ...
```

## Inlining as a dictionary

This is a slight variant on inlining as a list - here a dictionary keyed by identifier is provided

**Note** this is only possible if the range of the slot is a class that has an identifier slot

schema:

```yaml
      has_subtypes:
        range: Organism
        multivalued: true
        inlined: true
        inlined_as_list: false
```

data:


```yaml
- id: NCBITaxon:40674
  name: mammals
  has_subtypes:
    NCBITaxon:9443:
      name: primates
      has_subtypes:
        NCBITaxon:9606:
          name: humans
        NCBITaxon:9682:
          ...

```

## Inlining a single-valued object

Consider a variant of the above schema, with a non-multivalued slot

```yaml
      has_parent:
        range: Organism
        multivalued: false
        inlined: true
```

data:


```yaml
- id: NCBITaxon:9606
  name: human
  has_parent:
    id: NCBITaxon:9443:
    name: primates
    has_parent:
      id: NCBITaxon:40674
      name: mammals

```


## Inlining with non-JSON serializations

The concept of inlining only makes sense with JSON-like tree-oriented data serializations:

 * JSON and JSON-LD
 * YAML
 * Programmatic representations such as Python object trees

When serializing data as RDF triples or in a relational database, the value for the slot will always be a reference.

The inlined slot in LinkML corresponds to `@embed` in JSON-LD

## When should inlining be used

The choice of whether to inline in a JSON representation is application dependent. Inlining can be more convenient for applications that need to traverse an object tree, but inlining can also lead to redundancy in representation and more verbose object payloads.
