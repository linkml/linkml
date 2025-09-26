:tocdepth: 3

.. _rustgen:

Rust
========

Example Output
--------------

The structs:
`lib.rs <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/rust/src/lib.rs>`_

The traits:
`poly.rs <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/rust/src/poly.rs>`_

Overview
--------

.. warning ::

    The rust generator is still currently under development. Notable missing features are ``ifabsent`` processing
    and the enforcement of rules and constraints.


The Rust Generator produces a Rust crate with structs and enums from a LinkML model, with optional pyo3 and serde support.
It additionally generates a trait for every struct to provide polymorphic access, in the `poly.rs` file.

For all classes having subclasses, an extra enum is generated to represent an object of the class or a subtype.
All the enums implement the trait, so they can be (optionally) directly used without match statement.


Feature Compliance
------------------

The current implementation status is summarised below. These notes mirror the ongoing work tracked in
`linkml/linkml#2360 <https://github.com/linkml/linkml/issues/2360>`_.

Supported
~~~~~~~~~
- Core schema constructs: slots, classes, enums, and type aliases are emitted as Rust structs, enums, and aliases.
- Basic metamodel features: multivalued slots, required vs. optional cardinalities, inheritance (``is_a``), union slots
  (``any_of``), inline list/dict slots, and slot aliases.
- Build targets: both single-file output and full Cargo crates (with ``Cargo.toml``).
- Fundamental scalar types: ``string``, ``integer``, ``bool``, and ``float`` map to native Rust types.
- Temporal scalars: ``date`` and ``datetime`` map to ``chrono``'s ``NaiveDate`` and ``NaiveDateTime`` respectively.
- Traits for polymorphic access to class hierarchies, along with enums for class-or-subtype containers.
- PyO3 bindings for the generated structs (behind a Cargo feature flag).
- Basic ``serde`` deserialization (behind a Cargo feature flag).

Partially Supported
~~~~~~~~~~~~~~~~~~~
- Many scalar types (e.g. ``time``, URI-related types) currently fall back to ``String`` representations.
- ``serde`` deserialization works; serialization still lacks the normalisation, and will not always produce correct yaml.
- Testing covers unit-level behaviour with a dedicated Rust CI workflow; dynamic compilation and compliance suites are
  still pending.

Not Yet Supported
~~~~~~~~~~~~~~~~~
- Default handling (``ifabsent``) and broader constraint enforcement (``values_from``, ``value_presence``, equality and
  cardinality checks, numeric bounds, and ``pattern``).
- Schema metadata exports (``linkml_meta`` hash maps and module-level constants such as ``id`` and ``version``) .
- Serde data normalisation for serialization
- Compliance test integration
- Rule/expression support
- Dynamic enumerations



Example
^^^^^^^

Given a definition of a Person class:

.. code-block:: yaml


  Event:
    slots:
      - started_at_time
      - ended_at_time
      - duration
      - is_current

  EmploymentEvent:
    is_a: Event
    slots:
      - employed_at

  MedicalEvent:
    is_a: Event
    slots:
      - in_location
      - diagnosis
      - procedure



The generate rust looks like this (serde and pyo3 annotations omitted for brevity):

.. code-block:: rust


    pub struct Event {
        pub started_at_time: Option<NaiveDate>,
        pub ended_at_time: Option<NaiveDate>,
        pub duration: Option<f64>,
        pub is_current: Option<bool>
    }

    pub struct EmploymentEvent {
        pub employed_at: Option<String>,
        pub started_at_time: Option<NaiveDate>,
        pub ended_at_time: Option<NaiveDate>,
        pub duration: Option<f64>,
        pub is_current: Option<bool>
    }

    pub struct MedicalEvent {
        pub in_location: Option<String>,
        pub diagnosis: Option<DiagnosisConcept>,
        pub procedure: Option<ProcedureConcept>,
        pub started_at_time: Option<NaiveDate>,
        pub ended_at_time: Option<NaiveDate>,
        pub duration: Option<f64>,
        pub is_current: Option<bool>
    }

    pub enum EventOrSubtype {
        Event(Event),
        EmploymentEvent(EmploymentEvent),
        MedicalEvent(MedicalEvent)
    }

polymorphic traits are implemented:


.. code-block:: rust

    pub trait Event {
        fn started_at_time<'a>(&'a self) -> Option<&'a NaiveDate>;
        fn ended_at_time<'a>(&'a self) -> Option<&'a NaiveDate>;
        fn duration<'a>(&'a self) -> Option<&'a f64>;
        fn is_current<'a>(&'a self) -> Option<&'a bool>;
    }

    pub trait MedicalEvent: Event {
        fn in_location<'a>(&'a self) -> Option<&'a str>;
        fn diagnosis<'a>(&'a self) -> Option<&'a crate::DiagnosisConcept>;
        fn procedure<'a>(&'a self) -> Option<&'a crate::ProcedureConcept>;
    }

    impl Event for crate::MedicalEvent {
            fn started_at_time(&self) -> Option<&NaiveDate> {
            self.started_at_time.as_ref()
        }
            fn ended_at_time(&self) -> Option<&NaiveDate> {
            self.ended_at_time.as_ref()
        }
            fn duration(&self) -> Option<&f64> {
            self.duration.as_ref()
        }
            fn is_current(&self) -> Option<&bool> {
            self.is_current.as_ref()
        }
    }

    ...

    impl Event for crate::EventOrSubtype {
            fn started_at_time(&self) -> Option<&NaiveDate> {
            match self {
                    EventOrSubtype::Event(val) => val.started_at_time(),
                    EventOrSubtype::EmploymentEvent(val) => val.started_at_time(),
                    EventOrSubtype::MedicalEvent(val) => val.started_at_time(),

            }
        }
            fn ended_at_time(&self) -> Option<&NaiveDate> {
            match self {
                    EventOrSubtype::Event(val) => val.ended_at_time(),
                    EventOrSubtype::EmploymentEvent(val) => val.ended_at_time(),
                    EventOrSubtype::MedicalEvent(val) => val.ended_at_time(),

            }
        }
            fn duration(&self) -> Option<&f64> {
            match self {
                    EventOrSubtype::Event(val) => val.duration(),
                    EventOrSubtype::EmploymentEvent(val) => val.duration(),
                    EventOrSubtype::MedicalEvent(val) => val.duration(),

            }
        }
            fn is_current(&self) -> Option<&bool> {
            match self {
                    EventOrSubtype::Event(val) => val.is_current(),
                    EventOrSubtype::EmploymentEvent(val) => val.is_current(),
                    EventOrSubtype::MedicalEvent(val) => val.is_current(),

            }
        }
    }




Command Line
------------

.. currentmodule:: linkml.generators.rustgen

.. click:: linkml.generators.rustgen.cli:cli
    :prog: gen-rust
    :nested: short

Generator
---------


.. autoclass:: RustGenerator
    :members:

Features
--------

- Serde: Code that depends on Serde is behind the Cargo feature ``serde`` (``#[cfg(feature = "serde")]``).
- PyO3: Python bindings are behind the Cargo feature ``pyo3`` (``#[cfg(feature = "pyo3")]``).
- Enable features when building your crate (e.g., ``--features serde,pyo3``) to include the corresponding code paths.

Single-File Mode
----------------

- When generating a single ``.rs`` file (``--mode file``):
  - ``serde_utils`` is inlined into the file (no separate module file).
  - Polymorphic traits/containers (``poly.rs``/``poly_containers.rs``) are not emitted — they are crate-mode only.
