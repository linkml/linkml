# LinkML specification (DRAFT)

<!--

Editors note: add comments using HTML syntax, such as this one.

-->

## Introduction (Informative)

This document defines the [linkml](https://linkml.github.io/linkml/) syntax and language.

A LinkML schema is a formal computable description of how
entities within a data model are inter-related. While LinkML arose in
response to a need in life-sciences domain modeling to define the
Biolink Model, it is completely domain-neutral, and can be used to
model pet stores, etc.

The primary representation of a schema is via a YAML document. This
YAML document can be translated to other representations.

The 3 core modeling elements in LinkML are *types*, *classes*, and *slots*:

 - **[types](https://linkml.github.io/linkml-model/docs/TypeDefinition)** correspond to primitive datatypes, such as integers, strings, URIs
 - **[classes](https://linkml.github.io/linkml-model/docs/ClassDefinition)** are categories for data instances
 - **[slots](https://linkml.github.io/linkml-model/docs/SlotDefinition)** categorize the linkages instances can have to other instances, or to type instances

A [schema](https://linkml.github.io/linkml-model/docs/SchemaDefinition) is a collection of these elements.

The LinkML also defines basic mechanisms for model element inheritance: **is_a**, **mixin** and **abstract** 
properties for both classes and slots, plus a **typeof** property for types. In addition, the 
**subclass_of** property can anchor a class to the semantics of an ontology term in an external 
3rd party (but model-designated) ontology. Semantic constraints to 'internal' model slot or class 
hierarchies are similarly constrained by **domain**, **range** and  **subproperty_of** properties.
 
LinkML is intended to be used in a variety of modeling contexts: JSON
documents, RDF graphs, RDF* graphs and property graphs, as well as
tabular data. Converters exist for these different representations.

This document contains a mixture of normative and informative
sections. Normative sections may have informative examples
within. Normative elements are those that are prescriptive, that is
they are to be followed in order to comply with scheme
requirements. Informative elements are those that are descriptive,
that is they are designed to help the reader understand the concepts
presented in the normative elements.

blml is also described by its [own schema](meta.yaml), which is also
Normative. The schema can also be viewed on [this site](https://linkml.github.io/linkml-model/docs).

The documentation in this specification _must_ be consistent with the
yaml representation.

The italicized keywords _must_, _must not_, _should_, _should not_,
and _may_ are used to specify normative features LinkML documents
and tools, and are interpreted as specified in RFC 211.

## Domain (Normative)

<!--

TODO

-->

The domain of linkml is an RDF graph:

```
G = Triple*
Triple = < Subject Predicate Object >
Subject = IRI | BlankNode
Predicate = IRI
Object = IRI | BlankNode | Literal
```

### Notes (informative)

The primary domain of linkml is an RDF graph, but LinkML schemas may
be used for JSON documents, Property Graphs, UML object graphs, and
tabular/relational data.

## Schema Representation (Informative)

The normative representation of a LinkML [schema](https://w3id.org/linkml/meta/SchemaDefinition) is as a YAML document.

The document includes dictionaries of schema **elements**. Each
dictionary is indexed by the element **name**. Dictionaries _may_ be
empty, and they _may_ be listed in any order.

The structure of the document

 * dictionary of prefixes
 * dictionary of subsets
 * dictionary of types
 * dictionary of slots
 * dictionary of classes
 * additional schema-level declarations
    * the schema _must_ have an [id](https://w3id.org/linkml/meta/id)
    * the schema _may_ have other declarations as allowed by [SchemaDefinition](https://w3id.org/linkml/meta/SchemaDefinition)

Example (Informative):

This example illustrates broadly structure of a LinkML schema. Ellipses indicate information omitted for brevity

```yaml
id: https://example.org/example-schema
name: example schema
description: This is...
license: https://creativecommons.org/publicdomain/zero/1.0/

prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://example.org/example-schema#
  wgs: http://www.w3.org/2003/01/geo/wgs84_pos
  qud: http://qudt.org/1.1/schema/qudt#
  
default_prefix: ex

default_curi_maps:
  - semweb_context

emit_prefixes:
  - rdf
  - rdfs
  - xsd
  - skos

imports:
  - linkml:types

subsets: ...

# Main schema follows
types: ...
slots: ...
classes: ...

```

## Names and Namespaces (Normative)

All schema elements _must_ have a unique name and a unique IRI. Names _must_ be declared as keys in dictionaries, and IRIs are constructed automatically for these by concatenating the [default_prefix](https://w3id.org/linkml/meta/default_prefix) with the IRI construction rule for that element type:

 * class elements use a CamelCase construction rule
 * slot, types, subset elements use a snake_case construction rule

<!--

TODO: define these rules.

-->

Values for schema element slots _may_ be IRIs, and these _may_ be specified as CURIEs. CURIEs are shortform representations of URIs, and _must_ be specified as `PREFIX:LocalID`, where the prefix has an associated URI base. The prefix _must_ be declared in one of several ways:

 * a [prefixes](https://w3id.org/linkml/meta/prefixes) dictionary, where the keys are prefixes and the values are URI bases.

Example (Informative):

```yaml
prefixes:
  linkml: https://w3id.org/linkml/
  wgs: http://www.w3.org/2003/01/geo/wgs84_pos#
  qud: http://qudt.org/1.1/schema/qudt#
```

The CURIE `wgs:lat` will exand to http://www.w3.org/2003/01/geo/wgs84_pos#lat.

* an external CURIE map specified via a [default_curi_maps](https://w3id.org/linkml/meta/default_curi_maps) section.

Example (Informative):

```
default_curi_maps:
  - semweb_context
```

* prefixes from public standard global namespaces used in the model (e.g. rdf) are indicated under the [emit_prefixes](https://w3id.org/linkml/meta/emit_prefixes) section.

Example (Informative):

```
emit_prefixes:
  - rdf
  - rdfs
  - xsd
  - skos
```

* a default prefix within a given schema is generally also declared by a value for the [default_prefix](https://w3id.org/linkml/meta/default_prefix) tag:

Example (Informative):

```
default_prefix: ex
```

## Schema Elements (Normative)

 * [SchemaDefinition](https://w3id.org/linkml/meta/SchemaDefinition)

### Imports (Normative)

Imports are specified as an import list in the main schema object. This specifies a set: the order of elements is not important.

```yaml
imports:
  - <IMPORT_1>
  - <IMPORT_2>
  - ...
  - <IMPORT_n>  
```

<!--

TODO

 * https://github.com/linkml/projects/1

-->

### Metadata elements (Normative)

As mentioned in the [Introduction](#introduction-Informative), semantic inheritance within a model is specified by several LinkML reserved properties:
- **is_a:**
- **abstract:**
- **mixin:**
- **typeof:** 
- **subclass_of:** 
- **domain:**
- **range:**
- **subproperty_of:**

A few fundamental rules guiding the use of these properties include:

- *range:* the **range** of the **mixins** property in a class SHOULD be a **mixin**
- *homeomorphicity:* **is_a** SHOULD only connect either (1) two mixins (2) two classes (3) two slots
- instances MUST NOT instantiate a **mixin** slot or class directly since it has default **abstract** character; 
  rather, it should be injected into non-abstract classes using the **mixins** property


## Core elements: Classes, Slots, and Types (Normative)

### Slots (Normative)

See [SlotDefinition](https://w3id.org/linkml/meta/SlotDefinition).

Slots are properties that can be assigned to classes.

The set of slots available in a model is defined in a slot dictionary, declared at the schema level

```yaml
slots:
  SLOT_NAME_1: DEFINITION_1
  SLOT_NAME_2: DEFINITION_2
  ...
  SLOT_NAME_m: DEFINITION_n
```

Each key in the dictionary is the slot [name](https://w3id.org/linkml/meta/name). The slot name must be unique.


### Class Slots (Normative)

The [SlotDefinition](https://w3id.org/linkml/meta/SlotDefinition) is described in the metamodel.

### Slot Hierarchies (Normative)

Each slot _must_ have zero or one **is_a** parents, as defined by [linkml:is_a](https://w3id.org/linkml/meta/is_a)

In addition a slot _may_ have multiple **mixin** parents, as defined by [linkml:mixins](https://w3id.org/linkml/meta/mixin)

We define function `ancestors*(s)` which is the transitive close of the union of slot *s*, the parents of slot *s* and defined by the union of `is_a` and `mixins`.

### Classes and Class Slots (Normative)

In LinkML, as in the [Web Ontology Language OWL class](https://www.w3.org/TR/owl-guide/), is a classification of individuals into groups 
which share common characteristics. If an individual is a member of a class, it tells a machine reader that it falls under the 
semantic classification given by the class.

The set of classes available in a model is defined in a class dictionary, declared at the schema level.  A class _may_ have any number of slots declared.

```yaml
classes:

  CLASS_NAME_1:
    slots:
      - CLASS_1_SLOT_NAME_1
      - CLASS_1_SLOT_NAME_2
      - ...
      - CLASS_1_SLOT_NAME_n
  ...
    CLASS_NAME_p:
    slots:
      - CLASS_p_SLOT_NAME_1
      - CLASS_p_SLOT_NAME_2
      - ...
      - CLASS_p_SLOT_NAME_q
```

Each declared slot _must_ be defined in the slot dictionary. Note, however, that the use of declared slots in instances of a class are not mandatory unless `slot_usage.required` property of the slot is declared 'true' directly in that class or indirectly, by parental inheritance. 

### Class Hierarchies (Normative)

Each class _must_ have zero or one **is_a** parents, as defined by [linkml:is_a](https://w3id.org/linkml/meta/is_a)

In addition a class _may_ have multiple **mixin** parents, as defined by [linkml:mixins](https://w3id.org/linkml/meta/mixin)

We define function `ancestors*(c)` which is the transitive close of the union of class *c*, the parents of class *c* and defined by the union of `is_a` and `mixins`.

### Slot Usages

Each class _may_ declare a dictionary of [slot_usage](https://w3id.org/linkml/meta/slot_usage)s.

```yaml
  CLASS:
    slot_usage:
      SLOT_1: USAGE_1
      SLOT_2: USAGE_2
      ...
      SLOT_n: USAGE_n
```

These refine a slot definition in the context of a particular class


```python
def effective_slot_property(s, p, c):
   if c declares slot_usage for p:
      use the value for p
   elif any m in mixins(c) declares a slot_usage for p:
      use the value for p from this mixin
   else:
      if effective_slot_property(s, p, c.is_a):
         use this
      elif: effective_slot_property(s, p, m) for any mixin m:
         use this
      else:
         use the default value of p for s
```


### Slot Validation

This section describes which slots can be used to describe which instances.

Consider instance *i* of type *t*, with an association of type *s* connecting to object or instance *j*.

```json
{
  ## instance i of type t
  "s": <j>
}
```

For this to be valid, it *must* be the case that:

 * for all *r* 

## Domain Declarations

<!--

test_issue_3 

-->

## Built-in Types (Informative)

You can import standard types:

```yaml
imports:
  - linkml:types
```

includes in its type dictionary entries such as:

```yaml
  date:
    uri: xsd:date
    base: XSDDate
    repr: str
```

[types.yaml](./includes/types.yaml)

<!--

test_issue_3 

-->

## Glossary of terms (Information)

