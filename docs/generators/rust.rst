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

The Rust Generator produces a Rust crate with structs and enums from a LinkML model, with optional pyo3 and serde support.
It additionally generates a trait for every struct to provide polymorphic access, in the `poly.rs` file.

For all classes having subclasses, an extra enum is generated to represent an object of the class or a subtype. 
All the enums implement the trait, so they can be (optionally) directly used without match statement.



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

    pub trait Event   {
        fn started_at_time(&self) -> Option<&NaiveDate>;
        fn ended_at_time(&self) -> Option<&NaiveDate>;
        fn duration(&self) -> Option<&f64>;
        fn is_current(&self) -> Option<&bool>;
    }

    pub trait MedicalEvent : Event   {
        fn in_location(&self) -> Option<&str>;
        fn diagnosis(&self) -> Option<&crate::DiagnosisConcept>;
        fn procedure(&self) -> Option<&crate::ProcedureConcept>;
    }    

    impl Event for crate::MedicalEvent {
            fn started_at_time(&self) -> Option<&NaiveDate> {
            return self.started_at_time.as_ref();
        }
            fn ended_at_time(&self) -> Option<&NaiveDate> {
            return self.ended_at_time.as_ref();
        }
            fn duration(&self) -> Option<&f64> {
            return self.duration.as_ref();
        }
            fn is_current(&self) -> Option<&bool> {
            return self.is_current.as_ref();
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

.. click:: linkml.generators.rustgen:cli
    :prog: gen-rust
    :nested: short
        
Generator
---------

        
.. autoclass:: RustGenerator
    :members:

