# Mapping of instance graphs to trees and graphs

## Introduction

This section describes how LinkML instances are translated to different formats and data models.

The formal specification of LinkML instances is described in [Section 2](02instances.md).

LinkML instances can be *realized* in a number of different concrete forms, including:

1. tree-shaped serializations such as JSON or YAML
2. graph serializations such as RDF
3. in-memory programmatic typed object representations, such as Python dataclass instances or java objects.
4. Tables in a relational database
5. flattened tabular representations

This part of the LinkML specification only deals with 1-3. Future versions of the specification may also include 4-5.

### Terminology

- a *mapping* describes how the abstract LinkML instance model maps to a concrete form and back
- *dumping* or *serialization* is the process realizing a mapping from a programmatic representation to a serialization syntax
- *conversion* is the processing of converting between one serialization and another
- a *lossy* mapping is one that is not guaranteed to preserve all information

### Implementations

As the functional syntax is only intended for specification purposes, it is not expected that implementations use this as an intermediate. Instead, it is expected that an implementation will go via an internal programmatic representation.

The reference implementation is the [linkml-runtime](https://github.com/linkml/linkml-runtime/) but other implementations that conform to this specification are valid.

## Mapping to JSON or YAML

Here we define a mapping of LinkML instances to JSON.

| note on YAML|
|---|
| As JSON is a subset of YAML, this can also be used to load and dump from YAML. This is the canonical YAML mapping. We leave open the possibility of a *direct* YAML conversion in future which makes use of YAML tags to encode typing information. |

### Mapping to JSON: Overview

- Serialization to JSON takes as input:
    - a (root) instance
- Parsing from JSON takes as input:
    - a JSON document
    - a target ElementName
    - a SchemaDefinition

The following table defines a translation function **tr<sub>J</sub>**(*i*) that maps LinkML instances to JSON.

To apply this, *i* is matched against the instance column, and if a match is found, the production rule on the right hand side is applied.

| Instance                                           | JSON                                                  |
|----------------------------------------------------|-------------------------------------------------------|
| `None`                                             | `null`                                                |
| `<TypeDefinitionName>&<StringValue>`               | `string(<StringValue>)`                               |
| `<TypeDefinitionName>&<NumberValue>`               | `number(<AtomicValue>)`                               |
| `<TypeDefinitionName>&<BooleanValue>`              | `bool(<AtomicValue>)`                                 |
| `<EnumDefinitionName>[<PermissibleValue>]`         | `<PermissibleValue>`                                  |
| `<ClassDefinitionName>&<StringValue>`              | `string(<StringValue>)`                               |
| `<ClassDefinitionName>&<NumberValue>`              | `number(<NumberValue>)`                               |
| `<ClassDefinitionName>(<s1>=<v1>, ..., <sN>=<vN>)` | `object(string(s1)=trJ(v1), ..., string(sN)=trJ(vN))` |
| `[<Values>]`                                       | See below                                             |

the functions `object` and `number` and `string` apply as per the [definitions here](https://www.json.org/json-en.html)

### Collection Forms

There are 4 different *forms* in which a LinkML collection can be serialized as JSON. These forms *only* apply to lists uniformly consisting of **InstanceOfClass** objects.

| Form           | JSON                                                                     |
|----------------|--------------------------------------------------------------------------|
| `SimpleDict`   | `object( K(i1): tr(V(i1)), ..., K(iN): tr(V(iN)) )`                      |
| `CompactDict`  | `object( K(i1): tr(i1) - {PK: K(i1), ..., K(iN): tr(iN) - {PK: K(iN)} )` |
| `ExpandedDict` | `object( K(i1): tr(i1), ..., K(iN): tr(iN) )`                            |
| `List`         | `'[' tr(i1), ..., tr(iN) ']'`                                            |

This is determined in part by the parent slot `s`

* If `s.inlined_as_dict == False` then the form is `List`
* If `s.inlined_as_dict == True` then the form is `SimpleDict` or `CompactDict` or `ExpandedDict`
    * If `s.inlined_as_simple_dict == True` then the form is `SimpleDict`
    * If `s.inlined_as_simple_dict == False` then the form is `CompactDict` or `ExpandedDict`
        * If `s.inlined_as_expanded_dict == True` then the form is `ExpandedDict`
        * If `s.inlined_as_expanded_dict == False` then the form is `CompactDict`

Note that `inlined_as_simple_dict` and `inlined_as_expanded_dict` are only explicitly added to the metamodel in LinkML 1.5 and above. Prior to 1.5 these are calculated as follows:

* `inlined_as_simple_dict` is True if `inlined_as_dict` is True, and the derived model has a total of two attributes (one of which is the key)
* `inlined_as_expanded_dict` is False

### Collection Form Normalization

*Normalization* is the process of translating or *coercing* one form to the canonical form.

There are 12 non-identity normalizations possible, according to this table:

| Source Form    | Target Form    | Repair? |
|----------------|----------------|---------|
| `List`         | `SimpleDict`   | `True`  |
| `List`         | `CompactDict`  | `True`  |
| `List`         | `ExpandedDict` | `True`  |
| `SimpleDict`   | `List`         | `True`  |
| `SimpleDict`   | `CompactDict`  | `False` |
| `SimpleDict`   | `ExpandedDict` | `False` |
| `CompactDict`  | `List`         | `True`  |
| `CompactDict`  | `SimpleDict`   | `False` |
| `CompactDict`  | `ExpandedDict` | `False` |
| `ExpandedDict` | `List`         | `True`  |
| `ExpandedDict` | `SimpleDict`   | `False` |
| `ExpandedDict` | `CompactDict`  | `False` |

Additionally, the process of converting between a list of length 1 and a singleton, or the reverse translation, is considered a Repair normalization.

JSON Parsers MUST implement normalizations where Repair=False. These indicate alternative *valid* serializations. JSON Parsers MAY choose to implement Repair normalizations. If they choose to implement these, there SHOULD be a way to allow the user to disable these repairs.

Validators that take JSON as input SHOULD perform normalizations where Repair=False. These normalizations SHOULD be reported as part of the validation report, and MUST NOT be counted as validation errors. Validators MAY perform normalization of Repair=True normalizations, if they do, they MUST report these as errors.

### Mapping from JSON

Mapping to JSON is potentially lossy, as the definition names are not preserved.

When mapping from JSON, the function is **tr<sup>-1</sup><sub>J</sub>**(*obj*, *target*) where target is a schema element.

The same table as above is used, but an additional inference rule is applied when the target is a `ClassDefinitionName`.

First a *deepening* procedure is applied. If `target` has an induced slot **s<sup>t</sup>** such as that **s<sup>t</sup>**`.designates_type` is `True`, then the value of `obj.`**s<sup>t</sup>** is used to determine the type of the instance.

* If the range of **s<sup>t</sup>** is a TypeDefinition `uriorcurie` then the ClassDefinitionName is indexed by the uriorcurie of the class
* If the range of **s<sup>t</sup>** is a TypeDefinition with uri `xsd:anyURI` then the ClassDefinitionName is indexed by the URI of the class
* Otherwise the value of the **s<sup>t</sup>** is the target class name

For each assignment, the induced slot `s` is calculated (see section 5 of the specification), and `s.range` is used for the target of subsequent calls to **tr<sup>-1</sup><sub>J</sub>**(*obj*, *target*).

## Translation to RDF

Two RDF translations can be specified:

- A *direct* translation
- Translation via JSON-LD, which combines
    1. Translation of a LinkML **SchemaDefinition** to a **JSON-LD Context**
    2. The standard translation of LinkML instances to JSON
   
Both translations make use of the **prefixes** provided in the schema

The semantic content of both is equivalent. 

### Mapping of CURIEs to URIs

LinkML provides standard types:

- Curie
- Uri
- Curieoruri

The syntax for a CURIE is defined by [W3C CURIE Syntax 1.0](https://www.w3.org/TR/curie/)

> **curie**       :=   [ [ **prefix** ] ':' ] **reference**

> **prefix**      :=   **[NCName](https://www.w3.org/TR/1999/REC-xml-names-19990114/#NT-NCName)**

> **reference**   :=   **[irelative-ref](https://www.ietf.org/rfc/rfc3987.txt)**

See the Part 5 for rules for generating CURIEs and URIs from schema elements.

### Mapping functions

The following three functions are used when mapping LinkML instances to RDF:

| Function          | Value                      |
|-------------------|----------------------------|
| Literal(*v*, *T*) | `"<v>"^^T.uri`             |
| Node(*v*)         | `URI(<v>)`                 |
| Pred(*p*)         | `URI(p.slot_uri)`          |
| Subj(*i*)         | `URI(K(i))` *or* **Blank** |

### Direct Translation of instance graphs to RDF

A translation **Tr**<sub>R</sub> operates on an instance `i`, which is matched against the first column here, generating triples in the second column, and returning the value in the final column. 

| *i*                                         | Triples                                        | Returns            |
|---------------------------------------------|------------------------------------------------|--------------------|
| `None`                                      | `{}`                                           | `None`             |
| `<Type>&<V>`                                | `{}`                                           | `Literal(V, Type)` |
| `<Enum>[<PV>]` *where* `PV.meaning=None`    | `{}`                                           | `Literal(V, Type)` |
| `<Enum>[<PV>]` *where* `PV.meaning!==None`  | `{}`                                           | `Node(PV.meaning)` |
| `<Class>&<V>`                               | `{}`                                           | `Node(V)`          |
| `<Class>(<s1>=<v1>, ..., <sN>=<vN>)`        | `<Subj(i) Pred(si) L(tr(vi))>` *for i in 1..N* | `Subj(i)`          |

The triple generator column contains either the empty list or rules to generate triples. The templates `<s p L(o)>` denotes a triple `<s p oi>` for each `oi` in `L(o)`.

### Translation of instance graphs to RDF graphs (via JSON-LD)

This is an alternative specification of a mapping to RDF, specified in terms of a mapping to JSON-LD.

The mapping to JSON-LD is in two parts:

1. mapping the instance to JSON-LD
2. mapping the derived schema to a JSON-LD context

For (1), the mapping is the same as in "Mapping to JSON", above, with the addition of the insertion of a `@context` key-value pair into the top level object.

For (2), a JSON-LD context is generated by walking the entire derived SchemaDefinition object applying matches in the table below:

| Schema Element     | Match                            | Context Key        | Context Value                             |
|--------------------|----------------------------------|--------------------|-------------------------------------------|
| `SchemaDefinition` | p in e.prefixes`                 | `p.prefix_prefix`  | `@id=<p.prefix_reference>` `@prefix=true` |
| `SchemaDefinition` | `s in e.slots`                   | `s.name`           | `@type=<s.type.uri>`                      |
| `SchemaDefinition` | `s in e.slots`                   | `s.name`           | `@id=URI(<s.slot_uri>)`                   |
| `SchemaDefinition` | `s in e.slots`, `s.inlined=True` | `s.name`           | `@id=URI(<s.slot_uri>)`                   |
| `SchemaDefinition` | `c in e.classes`                 | `c.name`           | `@id=URI(<s.class_uri>)` `                |
| `ClassDefinition`  | `s in e.attributes`              | `s.name`           | `@type=<s.type.uri>`                      |
| `ClassDefinition` | `s in e.attributes`                   | `s.name`           | `@id=URI(<s.slot_uri>)`                   |
| `ClassDefinition` | `s in e.attributes`, `s.inlined=True` | `s.name`           | `@id=URI(<s.slot_uri>)`                   |

## Mapping to Typed Objects

Different programming languages have different formalisms for representing objects. We specify a generic mapping
to an abstract *typed object* representation, which can be mapped to the native object representation of a given language.

The mapping to Typed Objects is similar to the mapping to JSON, with the addition that each node in the tree has an **ElementName** (type)
associated with it.

| Instance                                           | TypedObject                                          |
|----------------------------------------------------|------------------------------------------------------|
| `None`                                             | `null`                                               |
| `<TypeDefinitionName>&<Value>`                     | `<TypeDefinitionName>(<Value>)`                      |
| `<EnumDefinitionName>[<PermissibleValue>]`         | `<EnumDefinitionName>(<PermissibleValue>)`           |
| `<ClassDefinitionName>&<Value>`                    | `REF(<ClassDefinitionName>)(<Value>)`                |
| `<ClassDefinitionName>(<s1>=<v1>, ..., <sN>=<vN>)` | `<ClassDefinitionName>(s1=trO(v1), ..., sN=trO(vN))` |
| `[<Values>]`                                       | As for JSON                                          |

The function `REF` takes a ClassDefinitionName and returns a function that returns the name of an atomic class by
concatenating the ClassDefinitionName with the name of `PK(ClassDefinitionName)` using the naming conventions of the target language.
For example, if the class `Person` has an attribute `id` marked `identifier=True` then `REF(Person)` returns `PersonId`,
assuming CamelCase naming conventions.

Mappings to target languages MAY choose to simplify AtomicClassNamees to the corresponding primitives for that language.
