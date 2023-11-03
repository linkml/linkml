Data Validation
===============

LinkML is designed to allow for a variety of strategies for data
validation. The overall philosophy is to provide maximum expressivity
in the language to allow model designers to state all constraints in a
declarative fashion, and then to leverage existing frameworks and to
allow the user to balance concerns such as expressivity vs efficiency.

Currently there are several supported strategies:

- validation with the ``linkml.validator`` package and its CLI
- validation via Python object instantiation
- validation via JSON Schema using external tools
- validation of triples in a triplestore or RDF file via generation of SPARQL constraints
- validation of RDF via generation of ShEx or SHACL
- validation via SQL loading and queries

However, others will be supported in future; in particular, scalable validation
of massive databases.

The ``linkml.validator`` package and CLI
----------------------------------------

This package contains the main entry point for various flexible validation strategies.

Validation in Python code
^^^^^^^^^^^^^^^^^^^^^^^^^

If you are writing your own Python code to perform validation the simplest approach is to use the :func:`linkml.validator.validate` function. For example:

.. code-block:: python

    from linkml.validator import validate

    instance = {
        "id": "ORCID:1234",
        "full_name": "Clark Kent",
        "age": 32,
        "phone": "555-555-5555",
    }

    report = validate(instance, "personinfo.yaml", "Person")

    if not report.results:
        print('The instance is valid!')
    else:
        for result in report.results:
            print(result.message)

This function takes a single instance (typically represented as a Python dict) and validates it according to the given schema (specified here by a path to the source file, but dict or object representation of the schema is also accepted). This example also explicitly specifies which class within the schema (``Person``) the data instance should adhere to. If this is omitted, the function will attempt to infer it.

The other high-level function is :func:`linkml.validator.validate_file`. It loads data instances from a file and validates each of them according to a class in a schema. Assuming the contents of ``people.csv`` look like:

.. code-block:: text

    id,full_name,age,phone
    ORCID:1234,Clark Kent,32,555-555-5555
    ORCID:5678,Lois Lane,33,555-555-1234

Each row can be validated with:

.. code-block:: python

    from linkml.validator import validate_file

    report = validate_file("people.csv", "personinfo.yaml", "Person")

Under the hood, both of these functions use a strategy of generating a JSON Schema artifact from the LinkML schema and validating instances using a JSON Schema validator.

While many LinkML constructs can be expressed in JSON Schema (which makes it a good default validation strategy), there are some features of LinkML not supported by JSON Schema. For more fine-grained control over the validation strategy use the :class:`linkml.validator.Validator` class. Using this class it is possible to mix JSON Schema validation with other strategies or forego it altogether.

The key idea behind the :class:`linkml.validator.Validator` is that it does not do any validation itself. Instead, it simply orchestrates validation according to a set of validation plugins. In this example, the basic JSON Schema validation will happen (disallowing additional properties because of the ``closed`` option) as well as a validation that checks that recommended slots are populated:

.. code-block:: python

    from linkml.validator import Validator
    from linkml.validator.plugins import JsonschemaValidationPlugin, RecommendedSlotsPlugin

    validator = Validator(
        schema="personinfo.yaml",
        validation_plugins=[
            JsonschemaValidationPlugin(closed=True),
            RecommendedSlotsPlugin()
        ]
    )
    validator.validate({"id": "ORCID:1234", "full_name": "Clark Kent", "age": 32, "phone": "555-555-5555"}, "Person")

This example only uses a validation strategy based on generating `Pydantic <https://docs.pydantic.dev/latest/>`_ models from the LinkML schema instead:

.. code-block:: python

    from linkml.validator import Validator
    from linkml.validator.plugins import PydanticValidationPlugin

    validator = Validator(
        schema="personinfo.yaml",
        validation_plugins=[PydanticValidationPlugin()]
    )
    validator.validate({"id": "ORCID:1234", "full_name": "Clark Kent", "age": 32, "phone": "555-555-5555"}, "Person")

Refer to the :mod:`linkml.validator.plugins` documentation for more information about the available plugins and their benefits and tradeoffs.

The ``linkml-validate`` CLI
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same functionality is also available via a the ``linkml-validate`` command line interface. For basic validation, simply provide a schema and a source to load data instances from:

.. code-block:: bash

    $ linkml-validate --schema personinfo.yaml --target-class Person people.csv
    No issues found!

Similar to the :func:`linkml.validator.validate` and :func:`linkml.validator.validate_file` functions, this will perform basic validation based on a JSON Schema validator. If advanced customization is needed, create a configuration YAML file and provide it with the ``--config`` argument:

.. code-block:: bash

    $ linkml-validate --config person-validation.config.yaml

The configuration YAML file can have the following keys. All keys are optional:

=================== ======================================================== ================================
Key                 Description                                              Default value
=================== ======================================================== ================================
``schema``          Path to the LinkML schema. Overrides ``--schema`` CLI    None
                    argument if both are provided.
``target_class``    Class in the schema to validate against. Overrides the   None
                    ``--target-class`` CLI argument if both are provided.
``data_sources``    A list of sources where each source is either a string   None
                    or a dictionary with a single key.

                    - If the source is a string it is interpreted as a
                      file path and data will be loaded from it based on
                      the file extension.
                    - If the source is a dictionary it should have a
                      single key representing the the name of a
                      :class:`linkml.validator.loaders.Loader` subclass.
                      The value is a dictionary that will be interpreted
                      as constructor keyword arguments for the given class.

                    This value overrides any ``DATA_SOURCES`` arguments
                    passed to the CLI
``plugins``         A dictionary where each key is the name of a             .. code-block:: yaml
                    :class:`linkml.validator.plugins.ValidationPlugin`
                    subclass. Each value is a dictionary that will be            JsonschemaValidationPlugin:
                    interpreted as constructor keyword arguments for the           closed: true
                    given class.

                    Classes defined in the ``linkml.validator.plugins``
                    package do not required a full dotted name (e.g. just
                    ``JsonschemaValidationPlugin`` is sufficient). Classes
                    outside of this package can be used, but you must
                    specify the full dotted name (e.g.
                    ``my_project.MyCustomValidationPlugin``)
=================== ======================================================== ================================

Here is an example configuration file:

.. code-block:: yaml

    # person-validation.config.yaml
    schema: personinfo.yaml
    target_class: Container

    # Data from two files will be validated. A loader for the JSON file will be created
    # automatically based on the file extension. A loader for the CSV file is specified
    # manually in order to provide custom options.
    data_sources:
      - people.json
      - CsvLoader:
          source: people.csv
          index_slot_name: persons

    # Data will be validated according to the JsonschemaValidationPlugin with additional
    # properties allowed (closed: false) and also the RecommendedSlotsPlugin
    plugins:
      JsonschemaValidationPlugin:
        closed: false
      RecommendedSlotsPlugin:

.. click:: linkml.validator.cli:cli
    :prog: linkml-validate


Python object instantiation
---------------------------

If you have generated :doc:`../generators/python` dataclasses or :doc:`../generators/pydantic` models from your LinkML schema, you can also use them as a lightweight form of validation.

.. code-block:: shell

    $ gen-python personinfo.yaml > personinfo.py
    $ echo '{"id":"ORCID:1234","full_name":"Clark Kent","age":32,"phone":"555-555-5555"}' > person.json

.. code-block:: python

    from personinfo import Person
    import json

    with open("person.json") as f:
        person_data = json.load(f)

    kent = Person(**person_data)

If you remove the ``id`` key from ``person.json`` and run the above code again, you will see a ``ValueError`` raised indicating that ``id`` is required.

JSON Schema with external tools
-------------------------------

If you need to perform validation outside of a Python-based project, JSON Schema validation is often the most straightforward to implement. From your LinkML schema project, generate a JSON Schema artifact:

.. code-block:: shell

    $ gen-json-schema personinfo.yaml > personinfo.schema.json

The ``personinfo.schema.json`` artifact can then be used in any other project where a `JSON Schema implementation <https://json-schema.org/implementations>`_ is available.

Validation of RDF triplestores using generated SPARQL
-----------------------------------------------------

The LinkML framework can also be used to validate RDF, either in a file, or a triplestore. There are two steps:

1. generation of SPARQL constraint-style queries (see [sparqlgen](../generators/sparql) )
2. execution of those queries on an in-memory graph or external triplestore

The user can choose to run only the first step, to obtain a bank of SPARQL queries that can be applied selectively

.. click:: linkml.validators.sparqlvalidator:cli
    :prog: linkml-sparql-validate
    :nested: full


Validation via shape languages
------------------------------

Currently the linkml framework does not provide builtin support for validating using a shape language, but the following strategy can be used:

1. Convert data to RDF using ``linkml-convert``
2. Convert schema to a shape language using ``gen-shex`` or ``gen-shacl``
3. Use a ShEx or SHACL validator

See next section for more details.

Future plans
------------

Future versions of LinkML will employ a powerful constraint and inference language.

One of the use cases here is being able to specify that the ``length`` field is equal to ``end - start``. This declarative knowledge can then be used to either (1) infer the value of ``length`` if unspecified (2) infer either ``start`` or ``end`` if only one of these is specified alongside ``length`` (3) check consistency if all three are specified.

These constraints can then be executed over large databases via a variety of strategies including:

 * generation of datalog programs for efficient engines such as souffle
 * generation of SQL queries to be used with relational databases
