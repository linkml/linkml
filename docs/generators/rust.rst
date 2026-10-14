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

For every class that has subclasses, an extra ``<Class>OrSubtype`` enum is generated with one variant per subclass,
plus a last variant for the class itself unless it is abstract or a mixin. Variants are tried in that order when
deserializing without a type designator, so subtypes are matched before the base class.
All the enums implement the trait, so they can be (optionally) directly used without match statement.

How to Generate a Rust Crate with Python Bindings
-------------------------------------------------

It is possible to generate a Rust Crate from a linkml schema complete with python bindings.

The steps below walk through producing a PyO3-enabled crate from a LinkML schema and installing it in a Python
environment. The commands were exercised against ``examples/PersonSchema/personinfo.yaml`` to verify they work end-to-end.

To build a rust crate as a python lib, you need ``maturin``. Maturin can easily be installed using pip.
A convenient way to build pip packages for multiple python versions and libc alternatives is the ``manylinux`` docker image.

#. **Generate the crate** using the main ``linkml`` CLI. The ``--mode crate`` option is the default; ``--pyo3`` and
   ``--serde`` ensure the generated ``Cargo.toml`` enables those features by default. Add ``--handwritten-lib`` when you
   want a regeneration-friendly layout: generated sources land under ``src/generated`` while ``src/lib.rs`` becomes a shim
   that is created only on the first run and then left untouched.

   .. code-block:: bash

      linkml generate rust \
        --output personinfo_rust \
        --pyo3 --serde --handwritten-lib \
        --force \
        examples/PersonSchema/personinfo.yaml

   The output directory contains ``Cargo.toml`` (with ``[lib]`` configured for both ``cdylib`` and ``rlib`` when PyO3 is
   requested), ``pyproject.toml`` with a ``maturin`` build-system section, ``src/bin/stub_gen.rs`` for type stubs, and a
   ``src/generated`` tree that houses the regenerated code. A small ``src/lib.rs`` file is emitted on the first run only;
   it re-exports everything from ``generated`` so you can regenerate safely.

#. **Adjust what is exposed to Python** in ``src/lib.rs``. The file declares the PyO3 module and calls
   ``generated::register_pymodule``; edit it to add your own functions/classes. Because the shim is only created on the
   first run, later regenerations leave your changes intact.

#. **Generate type stubs** so Python users get better typing support. With the ``stubgen`` feature enabled, run
   ``cargo run --bin stub_gen --features stubgen`` from the crate directory; add ``-- --check`` when you want to verify
   existing stubs instead of overwriting them.

#. **Build and install the wheel** with ``maturin``. Running ``maturin develop`` compiles the extension and puts it in the
   active virtual environment.

   .. code-block:: bash

      cd personinfo_rust
      maturin develop

   ``maturin build`` is an alternative when you want distributable wheels in ``target/wheels`` instead.

#. **Import the module from Python** and try the generated YAML loader. The module takes the crate's name, which here is
   the schema name, ``personinfo`` (see :ref:`rust-crate-name`).

   .. code-block:: python

      import personinfo
      # Update the path below to point at your data file.
      container = personinfo.load_yaml_container("examples/PersonSchema/data/example_personinfo_data.yaml")
      print(container.persons[0].name)

When repeating the process, pass ``--force`` (as above) or delete the output directory to avoid collisions with previous
runs.

.. _rust-crate-name:

Crate Name Configuration
------------------------

The generated crate name -- written to ``[package]`` and ``[lib]`` in ``Cargo.toml``,
and naming the Python module -- is driven by the following precedence:

1. ``--crate-name`` command-line option, or ``crate_name=...`` when using
   ``RustGenerator`` programmatically
2. ``generator_args.rust.crate_name`` set via ``--config-file``/``-C`` (see
   :ref:`rust-configuration-file` below)
3. Fallback: derived from the schema name, with any character outside
   ``[A-Za-z0-9_]`` replaced by an underscore (e.g. a schema named ``person-info``
   yields ``person_info``)

The derived fallback is always a legal crate name: a name that collides with a Rust
keyword, or with a name cargo reserves (``alloc``, ``core``, ``proc_macro``, ``std``,
``test``), is suffixed with an underscore (``test`` produces ``test_``), and one that
is still unusable -- for example, a schema name starting with a digit -- falls back to
``example``. A ``--crate-name`` or config-file value, by contrast, is never rewritten:
an invalid one (``my-crate``, ``fn``, ``std``) is reported as an error rather than
silently corrected. Cargo accepts a hyphen in a package name, but not in a ``[lib]``
name, so use ``my_crate``.

.. _rust-configuration-file:

Configuration File
------------------

As an alternative to ``--crate-name``, ``gen-rust`` accepts a ``--config-file``/``-C``
YAML file -- the **same format** used by ``gen-project``'s own ``--config-file``
(see :doc:`project-generator`) and by ``gen-java`` (see :doc:`java`), so a single
project-wide ``config.yaml`` can be shared between them. ``crate_name`` lives under
``generator_args.rust``:

.. code-block:: yaml

    # config.yaml
    generator_args:
      rust:
        crate_name: personinfo_rs
        pyo3: true
        serde: true

``gen-rust`` reads only the ``generator_args.rust`` section of this file, so a full
multi-generator project ``config.yaml`` can be passed as-is. Any ``gen-rust`` option
can be set there, keyed by its name with dashes as underscores; command-line options
take precedence, and a key that is not an option is reported as a warning and ignored.

Feature Compliance
------------------

The current implementation status is summarised below. These notes mirror the ongoing work tracked in
`linkml/linkml#2360 <https://github.com/linkml/linkml/issues/2360>`_.

Supported
~~~~~~~~~
- Core schema constructs: slots, classes, enums, and type aliases are emitted as Rust structs, enums, and aliases.
- Basic metamodel features: multivalued slots, required vs. optional cardinalities, inheritance (``is_a``) and mixins,
  union slots (``any_of``), inline list/dict slots, and slot aliases.
- Build targets: both single-file output and full Cargo crates (with ``Cargo.toml``).
- Fundamental scalar types: ``string``, ``integer``, ``bool``, and ``float`` map to native Rust types.
- Temporal scalars: ``date`` and ``datetime`` map to ``chrono``'s ``NaiveDate`` and ``NaiveDateTime`` respectively.
- Traits for polymorphic access to class hierarchies, along with enums for class-or-subtype containers.
- Type designators: a class-or-subtype enum is (de)serialized as a tagged union on the ``designates_type`` slot.
- ``subproperty_of``: a slot whose values are constrained to a slot hierarchy is emitted as a Rust enum of the slot's
  descendants.
- PyO3 bindings for the generated structs (behind a Cargo feature flag).
- Basic ``serde`` deserialization and serialization, including normalisation (behind a Cargo feature flag).

Partially Supported
~~~~~~~~~~~~~~~~~~~
- Many scalar types (e.g. ``time``, URI-related types) currently fall back to ``String`` representations.
- Testing covers unit-level behaviour with a dedicated Rust CI workflow; dynamic compilation and compliance suites are
  still pending.

Not Yet Supported
~~~~~~~~~~~~~~~~~
- Default handling (``ifabsent``) and broader constraint enforcement (``values_from``, ``value_presence``, equality and
  cardinality checks, numeric bounds, and ``pattern``).
- Schema metadata exports (``linkml_meta`` hash maps and module-level constants such as ``id`` and ``version``).
- Compliance test integration
- Rule/expression support
- Dynamic enumerations



Example
^^^^^^^

Given these event classes from ``examples/PersonSchema/personinfo.yaml`` (``NewsEvent`` omitted):

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
      - salary

  MedicalEvent:
    is_a: Event
    mixins:
      - WithLocation
    slots:
      - diagnosis
      - procedure

  WithLocation:
    mixin: true
    slots:
      - in_location


The generated Rust looks like this (serde and pyo3 annotations omitted for brevity):

.. code-block:: rust

    pub struct Event {
        pub started_at_time: Option<NaiveDate>,
        pub ended_at_time: Option<NaiveDate>,
        pub duration: Option<f64>,
        pub is_current: Option<bool>
    }

    pub struct EmploymentEvent {
        pub employed_at: Option<String>,
        pub salary: Option<f64>,
        pub started_at_time: Option<NaiveDate>,
        pub ended_at_time: Option<NaiveDate>,
        pub duration: Option<f64>,
        pub is_current: Option<bool>
    }

    pub struct MedicalEvent {
        pub diagnosis: Option<DiagnosisConcept>,
        pub procedure: Option<ProcedureConceptOrSubtype>,
        pub in_location: Option<String>,
        pub started_at_time: Option<NaiveDate>,
        pub ended_at_time: Option<NaiveDate>,
        pub duration: Option<f64>,
        pub is_current: Option<bool>
    }

    pub enum EventOrSubtype {
        EmploymentEvent(EmploymentEvent),
        MedicalEvent(MedicalEvent),
        Event(Event)
    }

polymorphic traits are implemented. Fields of ``Copy`` types such as ``f64`` and ``bool`` are returned by value, others
by reference:


.. code-block:: rust

    pub trait Event {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate>;
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate>;
        fn duration(&self) -> Option<f64>;
        fn is_current(&self) -> Option<bool>;
    }

    pub trait MedicalEvent: Event + WithLocation {
        fn diagnosis<'a>(&'a self) -> Option<&'a crate::DiagnosisConcept>;
        fn procedure<'a>(&'a self) -> Option<&'a ProcedureConceptOrSubtype>;
    }

    impl Event for crate::MedicalEvent {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
            return self.started_at_time.as_ref();
        }
        fn ended_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
            return self.ended_at_time.as_ref();
        }
        fn duration(&self) -> Option<f64> {
            return self.duration;
        }
        fn is_current(&self) -> Option<bool> {
            return self.is_current;
        }
    }

    ...

    impl Event for crate::EventOrSubtype {
        fn started_at_time<'a>(&'a self) -> Option<&'a crate::NaiveDate> {
            match self {
                EventOrSubtype::EmploymentEvent(val) => val.started_at_time(),
                EventOrSubtype::MedicalEvent(val) => val.started_at_time(),
                EventOrSubtype::Event(val) => val.started_at_time(),
            }
        }
        ...
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
- Stubgen: the ``stub_gen`` binary and its helpers are behind the Cargo feature ``stubgen``, which also enables ``pyo3``.
- Enable features when building your crate (e.g., ``--features serde,pyo3``) to include the corresponding code paths.

Single-File Mode
----------------

- When generating a single ``.rs`` file (``--mode file``):
  - ``serde_utils`` is inlined into the file (no separate module file).
  - Polymorphic traits/containers (``poly.rs``/``poly_containers.rs``) are not emitted — they are crate-mode only.
