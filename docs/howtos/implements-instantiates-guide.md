(howto-implements-instantiates)=
# Implements vs Instantiates vs Inheritance: A Best Practices Guide

LinkML offers several mechanisms for relating schema elements to one another:
**`is_a` + `mixins`** (inheritance), **`implements`** (structural conformance),
and **`instantiates`** (metamodel extension). This guide clarifies when and why
to use each one.

## Quick Reference

| Mechanism | Relationship | Analogy | What it governs |
|-----------|-------------|---------|-----------------|
| `is_a` | "is a kind of" | Class inheritance (OOP) | Slot inheritance, type hierarchy |
| `mixins` | "also behaves like" | Traits / interfaces (OOP) | Slot inheritance without single-parent constraint |
| `implements` | "conforms to the structure of" | Interface implementation | Declares structural conformance to a template |
| `instantiates` | "is an instance of (at the meta level)" | Metaclass instantiation | Governs which annotations are valid on a schema element |

## `is_a` and `mixins` — Classical Inheritance

Use `is_a` and `mixins` when your classes form a genuine **type hierarchy** —
where a child class truly *is a kind of* the parent.

```yaml
classes:
  NamedThing:
    abstract: true
    slots:
      - id
      - name

  WithProvenance:
    mixin: true
    slots:
      - created_by
      - created_on

  Person:
    is_a: NamedThing
    mixins:
      - WithProvenance
    slots:
      - birth_date
```

Key properties:

- **`is_a` forms a tree** — each class has at most one `is_a` parent.
- **`mixins` form a DAG** — a class can mix in multiple mixin classes, avoiding
  the [diamond problem](https://en.wikipedia.org/wiki/Mixin).
- **Slots are inherited.** `Person` above inherits `id`, `name`, `created_by`,
  and `created_on` without redeclaring them.
- **`slot_usage` refines inherited slots** in the context of the child class
  (e.g. making an inherited slot required).

**When to use:** You are modeling a domain ontology where child classes are
genuinely subtypes of parent classes. Data validated against the child class
should also be valid against the parent class (Liskov substitution).

## `implements` — Structural Conformance

Use `implements` when a class **conforms to a structural template** without
being a subtype of it. Think of it like implementing an interface or satisfying
a contract.

```yaml
classes:
  FieldObservation:
    description: >-
      Contract for field observation classes.
      Any class that implements this must provide these slots.
    slots:
      - location
      - timestamp
      - observer

  RadonObservation:
    implements:
      - geochem_profile:FieldObservation
    slots:
      - location
      - timestamp
      - observer
      - radon_activity
```

Key properties:

- **No slot inheritance.** Unlike `is_a`, `implements` does not automatically
  pull slots into the implementing class. You must declare them yourself.
- **Cross-schema references.** The value of `implements` is a `uriorcurie`,
  so you can reference classes from external schemas without importing them.
- **Documentative intent.** `implements` declares that your class is *intended*
  to conform to a contract. Tooling support for enforcement is evolving.

**When to use:** You want to declare that your class or slot satisfies a
structural contract defined elsewhere, but it is *not* a subtype of that
contract class. This is especially useful when:

- The contract comes from an external schema you do not want to import wholesale.
- Your class belongs to a different type hierarchy but must meet certain
  structural requirements.
- You are working with schema profiles (see [Schema Profiles](#schema-profiles)
  below).
- A slot implements a well-known semantic property (see below).

### `implements` for Semantic Properties

`implements` can also be used at the **slot level** to declare that a slot
represents a well-known semantic property. For example, to declare that a
`name` attribute implements `rdfs:label`:

```yaml
classes:
  OntologyTerm:
    attributes:
      id:
        identifier: true
      name:
        implements:
          - rdfs:label
```

This is the recommended approach for binding validation in the
[linkml-term-validator](https://linkml.io/linkml-term-validator/binding-validation/#1-using-implements-recommended),
where it signals which field holds the canonical label for ontology term
lookups.

## `instantiates` — Metamodel Extension

Use `instantiates` when a schema element **is an instance of a metaclass** that
governs what *annotations* (metadata about the schema element itself) are valid.
This operates at the *meta* level — it does not affect the data instances, but
rather the schema element's own metadata.

```yaml
classes:
  RadonObservation:
    instantiates:
      - geochem_profile:GeochemClass
    annotations:
      provenance_status: "validated"   # governed by GeochemClass
      data_steward: "smoxon"           # governed by GeochemClass
    slots:
      - radon_activity
```

Where `GeochemClass` is defined as:

```yaml
# In geochem_profile schema
classes:
  GeochemClass:
    description: "Any class in a geochem schema must have provenance"
    class_uri: geochem_profile:GeochemClass
    attributes:
      provenance_status:
        range: string
        required: true
      data_steward:
        range: string
```

Key properties:

- **Governs annotations, not data slots.** `instantiates` controls which
  annotation tags are valid on the schema element.
- **Metaclass relationship.** The instantiated class acts as a metaclass — its
  slots define the valid annotation keys for the instantiating element.
- **Works on any schema element.** Classes, slots, enums, and even schemas
  themselves can use `instantiates`.
- **Validation is declarative.** As of LinkML 1.6+, `instantiates` declares
  intent. Full validation enforcement is under active development.

**When to use:** You want to constrain or extend the *metadata* that schema
authors must provide on their schema elements (not the data those elements
describe).

## Putting It All Together

Here is a complete example showing all three mechanisms working in concert,
adapted from a geochemistry schema profile:

```yaml
# geochem_profile.yaml — defines rules for geochem schemas

id: https://example.org/geochem-profile/
name: geochem_profile
prefixes:
  geochem_profile: https://example.org/geochem-profile/
  linkml: https://w3id.org/linkml/

classes:
  # Metaclass: governs annotations on classes
  GeochemClass:
    description: "Any class in a geochem schema must have provenance metadata"
    class_uri: geochem_profile:GeochemClass
    attributes:
      provenance_status:
        range: string
        required: true
      data_steward:
        range: string

  # Metaclass: governs annotations on slots
  GeochemSlot:
    description: "Any slot in a geochem schema must declare units"
    class_uri: geochem_profile:GeochemSlot
    attributes:
      unit_ontology_term:
        range: uriorcurie

  # Structural contract: defines required slots for field observations
  FieldObservation:
    description: "Contract for field observation classes"
    slots:
      - location
      - timestamp
      - observer
```

Then in a downstream schema:

```yaml
# radon_schema.yaml — a domain schema that uses the profile

id: https://example.org/radon/
name: radon_schema
prefixes:
  geochem_profile: https://example.org/geochem-profile/

classes:
  RadonObservation:
    # META-LEVEL: "I am an instance of your metaclass"
    # → governs which annotations are valid on this class
    instantiates:
      - geochem_profile:GeochemClass

    # STRUCTURAL: "I conform to your structural contract"
    # → declares that this class provides the slots required by FieldObservation
    implements:
      - geochem_profile:FieldObservation

    # Annotations governed by instantiates (GeochemClass attributes)
    annotations:
      provenance_status: "validated"
      data_steward: "smoxon"

    # Data slots — some from implements contract, some domain-specific
    slots:
      - location       # ← required by FieldObservation contract
      - timestamp      # ← required by FieldObservation contract
      - observer       # ← required by FieldObservation contract
      - radon_activity # ← domain-specific

slots:
  radon_activity:
    # META-LEVEL: "I am an instance of your slot metaclass"
    instantiates:
      - geochem_profile:GeochemSlot
    annotations:
      unit_ontology_term: "UO:0000134"   # governed by GeochemSlot
    range: float

  location:
    range: string
  timestamp:
    range: datetime
  observer:
    range: string
```

Notice how:

- **`instantiates`** operates at the meta level, governing annotations
  (`provenance_status`, `data_steward`, `unit_ontology_term`).
- **`implements`** operates at the structural level, declaring conformance to
  a slot contract (`location`, `timestamp`, `observer`).
- Neither `instantiates` nor `implements` *inherits* slots — that is the job
  of `is_a` and `mixins`.

## Decision Flowchart

When deciding which mechanism to use, ask yourself:

1. **Is the child a genuine subtype of the parent?**
   → Use `is_a` (and `mixins` for cross-cutting concerns).

2. **Does the class need to satisfy a structural contract from another schema?**
   → Use `implements`.

3. **Do I need to govern what metadata (annotations) schema authors can attach
   to a schema element?**
   → Use `instantiates`.

4. **Do I need more than one?**
   → Yes! These mechanisms are complementary. A single class can use `is_a`,
   `mixins`, `implements`, and `instantiates` simultaneously.

(schema-profiles)=
## Schema Profiles

The `implements` and `instantiates` mechanisms are foundational to the concept
of **schema profiles** — reusable sets of constraints and conventions that
downstream schemas can adopt.

The [linkml-microschema-profile](https://github.com/linkml/linkml-microschema-profile)
project provides an example of this pattern. It defines a small, generic profile
that schema authors can reference to ensure their schemas follow common
conventions (e.g. requiring descriptions on all classes, enforcing naming
patterns).

Profiles are useful when:

- An organization wants to enforce governance rules across many schemas without
  requiring full schema imports.
- Domain-specific conventions (like the geochemistry example above) need to be
  separated from generic best practices.
- You want to layer constraints: a generic profile for all schemas, plus a
  domain profile for your specific field.

For instance, generic constraints like "all classes must have descriptions"
belong in a base profile, while domain-specific metaclasses like
`GeochemClass` belong in a domain-specific child profile. See
[issue #3282](https://github.com/linkml/linkml/issues/3282) for discussion on
separating generic from domain-specific profile components.

## Common Pitfalls

**Pitfall 1: Using `is_a` when you mean `implements`.**
If your class is not genuinely a subtype — it just happens to share some
slots — prefer `implements`. Misusing `is_a` creates misleading type
hierarchies.

**Pitfall 2: Expecting slot inheritance from `implements`.**
Unlike `is_a`, `implements` does not pull in slots. You must declare the
required slots explicitly in your class.

**Pitfall 3: Confusing `instantiates` with `implements`.**
`instantiates` governs *annotations on the schema element itself* (metadata
about the class/slot). `implements` governs *the structure of data instances*
(which slots the class provides). They operate at different levels.

**Pitfall 4: Using `instantiates` to try to add data slots.**
`instantiates` controls annotation validity, not data structure. If you need
to add data slots, use `is_a`, `mixins`, or declare them directly.

## Summary

| Question | Use |
|----------|-----|
| "Is RadonObservation a kind of Observation?" | `is_a: Observation` |
| "Should RadonObservation also behave like a Locatable thing?" | `mixins: [Locatable]` |
| "Does RadonObservation conform to the FieldObservation contract?" | `implements: [geochem_profile:FieldObservation]` |
| "What metadata must the RadonObservation *class definition* carry?" | `instantiates: [geochem_profile:GeochemClass]` |
