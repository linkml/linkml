# Mapping Schemas to Programming Language Structures

LinkML Schemas can be mapped to modeling constructs in different programming languages.
This allows for *code generation*, in which a LinkML schema is used as the source to generate
code in a target language.

This has a number of advantages, including type safety, programmer efficiency, ease of mapping
to other serializations, helping ensure code and domain models are aligned.

As each programming language differs in which constructs it offers and the precise
semantics of these constructs, there is single standard for mapping. Instead, we provide
a set of general recommendations that can be adapted to each language.

## Terminology

* Programming language constructs:
  * `Structure`: a compound datatype that consists of one of more attributes
  * `Class`: a Structure that supports or partially supports inheritance
  * `Attribute`: a field or property of a class or struct
  * `Class-level variable`: a property of a class rather than of an instance of that class
  * `Module`: A file-level bundle of classes or structures
  * `Package`: A collection of modules

## Mapping of LinkML Schemas

### Schemas to Modules

A schema SHOULD be mapped to EITHER a module or a collection of modules, depending on the idioms
of the target language.

For languages where it is conventional to include multiple classes or structures in
a single module (e.g. Python), the schema SHOULD correspond to a module.

For languages where it is conventional to include a single classes or structures in
a single module (e.g. Java), a single module will correspond to a single LinkML class or enum.

Current implementations:

| Target        | Default Mapping     |
|---------------|---------------------|
| Dataclasses   | One file per schema |
| Pydantic      | One file per schema |
| Java          | One file per class  |
| Typescript    | One file per schema |

### Imports

A mapping MAY choose to merge imports prior to code generation. If imports are not merged,
then each `imports` in the SchemaDefinition MUST be mapped to an import statement in the target
language.

Where modules correspond to structures, there SHOULD be one import in the target language module for
every import in the source LinkML schema.

Mappings MAY choose to selectively import via inspection of all used elements.

### Naming Conventions for Modules

There MUST be a correspondence between schema `name` and module name. The mapping MAY
prioritize idioms of the target language over LinkML idioms, although the mapping MUST
be deterministic.

For example, if the target language has module names as `CamelCase` then a mapping MAY
translate all module names using a standard camel case string transformation.

Schema level metadata MAY be included in the header of the module. This MAY
be as comments, but if the target language supports module-level variables or other
ways to make schema metadata introspectable at runtime, these mechanisms SHOULD be used.

Current implementations:

| Target        | Default Mapping |
|---------------|-----------------|
| Dataclasses   | underscore      |
| Pydantic      | underscore      |
| Java          | CamelCase       |
| Typescript    | CamelCase       |

## Mapping of LinkML Classes

### Target Constructs

Different languages support different constructs, which may all make
appropriate targets for LinkML classes. For example:

* Java has both Interfaces and Classes, and newer versions of Java support Records
* Scala has traits and sealed traits
* Rust has structs, traits, and enums
* Typescript has classes and interfaces

The choice should reflect whatever is most idiomatic for the target language.
The generation MAY allow for different mappings, controlled by either user configuration,
or by properties of either the schema and its elements.

For example, when mapping to Rust, a generator MAY choose to map to either structs
or to struct/enum/trait combinations, depending on whether polymorphism is used
in the schema.

A mapping MAY be non-isomorphic (i.e not one-to-one). For example, 
in languages that have a split between
interface-like constructs and concrete class-like constructs, a generator MAY choose to
implement a mapping where each LinkML class creates *both* structures, in order
to leverage the full benefits of the target language.



### Class level variables

A generator SHOULD map certain properties of schema elements to class level
variables where the target language allows. When this mapping occurs,
the names of the class level variables MUST correspond to LinkML metamodel elements,
allowing for translation to language idioms.

The following class-level variables are recommended:

* class_class_uri: the semantic URI of the class, as defined by `class_uri`
* class_class_curie: the CURIE form of class_class_uri
* class_name: the normalized name of the LinkML class, corresponding to the name of the class
* class_model_uri: the URI of the class within the namespace of the schema

A generator MAY allow for generation of class level variables to be suppressed.

A generator MAY choose to use annotations in place of class-level variables

Current implementations:

| Target        | Default Mapping |
|---------------|-----------------|
| Dataclasses   | all             |
| Pydantic      | none (planned)  |
| Java          | none (planned)  |
| Typescript    | none            |

### Inheritance

Mapping of `is_a` and `mixins` may be dependent on properties of target language
constructs.

Generators MAY choose to roll-down attributes from parent classes.

If the target construct for a class supports single inheritance, then the is_a SHOULD
correspond to the analogous construct (for example, `extends` in Java). The mixins MAY be
represented using an alternative construct (such as `implements` in Java).

Generators MAY choose to create type checkers for runtime inspection
of instantiated classes. This SHOULD NOT be done in languages that
support polymorphism and type checking natively (for example `isinstance` in Python)

### Mapping of class slots and attributes

Mapping of class slots and attributes should be entailment-preserving, such that
the semantics of the generated code in the target language corresponds to
a *derived* schema.

For example, consider a schema with classes:

```yaml
classes:
  NamedThing:
    attributes:
      id:
  Person:
    is_a: NamedThing
    attributes:
      address:
```

The following are both valid ways to map `Person` to a target language construct:

* a non-class structure with two asserted attributes, `id` and `address` (the address has been "rolled down")
* a class structure whose structure mirrors the source LinkML, with `id` only asserted on the parent

### Constructors

Generation of constructors will be highly dependent on source language, but the following
guidelines should be followed:

- if the target language allows named assignment of attributes, then this SHOULD be the default constructor style
- if the target language allows positional assignment of attributes, then this MAY be allowed:
    - the order of attributes MUST correspond to `rank` metaslots in the derived schema, if specified
    - otherwise the ordering MUST correspond to the order in which slots or attributes are specified
        - starting from the is_a root, working down the is_a hierarchy
        - `slots` order prioritized over `attributes`
- if the target language and idiom uses builder patterns then these may be used        

### Mapping of schema-level slots

### Mapping of constraints and rules

Constraints and rules in LinkML SHOULD be mapped to declarative target
constructs where possible. If this is not possible then the generator
MAY choose to generate code that implements the constraint or rule.

For example, when mapping the LinkML metaslot `maximum_value` to Pydantic,
a `Field` with property `maximum_value` should be used. This makes the generated
code more declarative, and takes advantage of the target framework's
builtin abilities to perform validation.

If mapping to a target that does not support the feature then code generation
may be applied. For example, if there is no equivalent direct correspondence to
`maximum_value`, then the generated construct MAY include a validation
procedure that checks the value against the maximum.

### Complex boolean ranges

## Mapping of enums

## Runtime dependencies

A generator MAY choose to generate code that is either self-contained,
or that has runtime dependencies. The runtime library SHOULD be kept
minimal, within the constraints of the requirements of the runtime library.

## Mapping of types

Types SHOULD be mapped to one of the following:

* primitive types in the target language
* type variables
* class-like structures that can emulate scalar-like properties

Some languages like Java have a choice for primitives, either builtin
like `str` or classes like `String`.

## Metaclasses

If the target language supports it then metaclasses may be used to
type generated LinkML classes.



## Loaders and Dumpers

## Packages and package distribution

