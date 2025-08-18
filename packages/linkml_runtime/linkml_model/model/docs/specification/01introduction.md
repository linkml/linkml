# Introduction

This document is a functional draft specification for the Linked Data Modeling Language (LinkML).

LinkML is a data modeling language for describing the structure of a collection of *instances*, where instances are tree-like object-oriented structures. Instances represent things of interest in a particular domain, such as individual people, biological samples, places, events, or abstract entities. 

Instances are either primitive *types* such as numbers or strings, or *objects* that are typed using *classes* from a LinkML *schema*. Classes are categories or groupings of things in the domain of interest; for example, `Person`, `Medical History`, `Data file`, or `Country`. Instances can be inter-related by assigning *values* to particular *slots*; for example, an instance of a Person may have values for slots `name` or `country of birth`.

LinkML schemas also specify *rules* for determining if instances conform to the schema, and for *inference* adding additional implicit slot values.

LinkML is independent of any programming language, database technology, and is independent of any concrete form for serializing instances of schemas. Mappings are provided for serializing instances as JSON, YAML, RDF, flat tables, or relational models, or for mapping to programming language structures. However, the structure and semantics of LinkML are not dependent on any of these. Schemas are typically expressed using the YAML serialization, but this specification is defined independent of that particular serialization.

LinkML is self-describing, and any LinkML schema is itself a collection instances that instantiates elements in a special schema called the *LinkML metamodel*.

## Audience

This document is intended for LinkML tool and framework implementers, and is intended to formally specify the structure and semantics of LinkML.

For a more lightweight introduction, consult the material on the main [LinkML site](https://linkml.io),
including the LinkML tutorial.

## Conventions and terminology

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## BNF

Grammars in this specification are written using the BNF notation, summarized below:

Construct | Syntax |
|---|---|
terminal symbols | enclosed in single quotes |
a set of terminal symbols described in English | italic |
nonterminal symbols | boldface |
zero or more | curly braces |
zero or one | square brackets |
alternative | vertical bar |

We also include a meta-production rule for expressing comma-delimited lists

```
<NT>List ::= [ <NT> { ',' <NT>List } ]
```

## Outline

The specification is organized in 6 parts. The parts are not independent, as each part builds on concepts introduced in previous parts.

### Part 1: Introduction

This section. Background information and preliminary definitions.

### Part 2: Structure and Syntax of Instances

Part 2 provides a *structural specification* of LinkML **instances**. The structural specification is provided as a normative abstract functional-style syntax. UML diagrams are provided for informative purposes.

This syntax is not intended as an actual exchange syntax for LinkML data. For that, existing syntaxes such as JSON, YAML, or RDF syntaxes should be used (see Part 6). The abstract syntax allows for a separation of the essential features of the language from issues related to any particular syntax.

Part 2 also introduces a **path accessor** syntax for specifying how to traverse LinkML instances.

The abstract syntax and path accessor syntax are used in the remainder of the specification.

### Part 3: Structure of Schemas

Introduces the concept of a LinkML schema, which specifies how conforming LinkML instances are intended to be structured.

This part specifies the core elements of a LinkML schema: [ClassDefinitions](https://w3id.org/linkml/ClassDefinition), [TypeDefinitions](https://w3id.org/linkml/TypeDefinition), [SlotDefinitions](https://w3id.org/linkml/SlotDefinition), [EnumDefinitions](https://w3id.org/linkml/EnumDefinition), as well as ancillary structures.

This part also introduces the concept of the LinkML metamodel. A LinkML schema is both a specification of conformance conditions for an instance, and at the same time an instance that conforms to the metamodel schema.

### Part 4: Derived Schemas and Schema Semantics

Specification of inference functions and procedures for **derived schemas** to populate missing values in schemas.

### Part 5: Validation of Instance Data

Specification of the procedure for **validating** LinkML instances using a derived schema.

### Part 6: Mapping of Instance Data

Specification of how LinkML instances are mapped to other data models and concrete syntaxes:

- JSON and the JSON subset of YAML
- RDF and JSON-LD
- in-memory object-oriented representations
