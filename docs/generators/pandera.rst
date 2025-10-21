:tocdepth: 3

.. _panderagen:

Pandera
=======

Overview
--------

`Pandera <https://pandera.readthedocs.io/en/stable/index.html#>`__ is an open-source framework
for data validation on dataframe-like objects.
`PolaRS <https://docs.pola.rs/>`__ is a fast dataframe library.

The Pandera Generator produces Pandera models using the class-based API
using the PolaRS integration. It can also produce PolaRS schemas for use in loading data.

The implementation of the generator is incomplete. Because Pandera is a dataframe library,
the first priority is implementing models of literal and nested data types and checks for single tables as shown below.
`tests/test\_generators/test\_panderagen.py` also has an example using supported LinkML features.

Currently supported LinkML features are:

- literal slot ranges: string, integer, float, boolean, date, datetime
- enums
- constraints: required, pattern, minimum_value, maximum_value, multivalued
- inlining: nested single-valued objects, lists of literals, lists of objects

Future priorities that are currently not supported include:

- foreign key association to other tables
- model and slot inheritance
- aliases
- additional target dataframe libraries

Example
^^^^^^^

Given a definition of a synthetic flat table with some nested/inlined columns:

.. code-block:: yaml

  PanderaSyntheticTable:
      description: A flat table with a reasonably complete assortment of datatypes.
      attributes:
        identifier_column:
          description: identifier
          identifier: true
          range: integer
          required: true
        bool_column:
          description: test boolean column
          range: boolean
          required: true
        integer_column:
          description: test integer column with min/max values
          range: integer
          required: true
          minimum_value: 0
          maximum_value: 999
        float_column:
          description: test float column
          range: float
          required: true
        string_column:
          description: test string column
          range: string
          required: true
          pattern: "^(this)|(that)|(whatever)$"
        date_column:
          description: test date column
          range: date
          required: true
        datetime_column:
          description: test datetime column
          range: datetime
          required: true
        enum_column:
          description: test enum column
          range: SyntheticEnum
          required: true
        ontology_enum_column:
          description: test enum column with ontology values
          range: SyntheticEnumOnt
          required: true
        multivalued_column:
          description: one-to-many form
          range: integer
          required: true
          multivalued: true
          inlined_as_list: true
        any_type_column:
          description: needs to have type object
          range: AnyType
          required: true
        inlined_class_column:
          description: test column with another class inlined as a struct
          range: ColumnType
          required: true
          inlined: true
          inlined_as_list: false
          multivalued: true
        inlined_as_list_column:
          description: test column with another class inlined as a list
          range: ColumnType
          required: true
          inlined: true
          inlined_as_list: true
          multivalued: true
        inlined_simple_dict_column:
          description: test column inlined using simple dict form
          range: SimpleDictType
          multivalued: true
          inlined: true
          inlined_as_list: false
          required: true


(details omitted, including header information, slots, enums and nested class definitions)

The generate python looks like this:

.. code-block:: python

  class PanderaSyntheticTable(pla.DataFrameModel, _LinkmlPanderaValidator):
        """A flat table with a reasonably complete assortment of datatypes."""


        identifier_column: int= pla.Field()
        """identifier"""

        bool_column: bool= pla.Field()
        """test boolean column"""

        integer_column: int= pla.Field(ge=0, le=999, )
        """test integer column with min/max values"""

        float_column: float= pla.Field()
        """test float column"""

        string_column: str= pla.Field()
        """test string column"""

        date_column: Date= pla.Field()
        """test date column"""

        datetime_column: DateTime= pla.Field()
        """test datetime column"""

        enum_column: Enum= pla.Field(dtype_kwargs={"categories":('ANIMAL','VEGETABLE','MINERAL',)})
        """test enum column"""

        ontology_enum_column: Enum= pla.Field(dtype_kwargs={"categories":('fiction','non fiction',)})
        """test enum column with ontology values"""

        multivalued_column: List[int]= pla.Field()
        """one-to-many form"""

        any_type_column: Object = pla.Field()
        """needs to have type object"""

        inlined_class_column: Struct = pla.Field()
        """test column with another class inlined as a struct"""

        inlined_as_list_column: pl.List = pla.Field()
        """test column with another class inlined as a list"""

        inlined_simple_dict_column: Struct = pla.Field()
        """test column inlined using simple dict form"""

        @pla.check("inlined_class_column")
        def check_nested_struct_inlined_class_column(cls, data: PolarsData):
            return cls._check_collection_struct(data)

        @pla.check("inlined_as_list_column")
        def check_nested_struct_inlined_as_list_column(cls, data: PolarsData):
            return cls._check_nested_list_struct(data)

        @pla.check("inlined_simple_dict_column")
        def check_nested_struct_inlined_simple_dict_column(cls, data: PolarsData):
            return cls._check_simple_dict(data)

        _NESTED_RANGES = {
            "inlined_class_column": "ColumnType",
            "inlined_as_list_column": "ColumnType",
            "inlined_simple_dict_column": "SimpleDictType",
        }
        _INLINE_FORM = {
            "inlined_class_column": "inline_collection_dict",
            "inlined_as_list_column": "inlined_list_dict",
            "inlined_simple_dict_column": "simple_dict",
        }
        _INLINE_DETAILS = {
            "inlined_simple_dict_column": {'id': 'id', 'other': 'x'},
        }

Command Line
------------

.. currentmodule:: linkml.generators.panderagen

.. click:: linkml.generators.panderagen:cli
    :prog: gen-pandera
    :nested: short

The Python code is written to a package directory if the `--package` command line option is provided.
Otherwise the code is written to the console if only generation of a single module is specified.


Usage Example
-------------

Generate the package from tutorial 01 using the `gen-pandera` command
Command-line options are under active development and are likely to change.

.. code-block:: bash
    # recommended is to generate a package with all schema forms
    gen-pandera --package personinfo examples/tutorial/tutorial01/personinfo.yaml

    # alternatively you can generate the schemas individually using the --template-path and --template-file arguments
    # instead of --package
    gen-pandera --template-path panderagen_polars_schema --template-file polars_schema.jinja2 examples/tutorial/tutorial01/personinfo.yaml > personinfo_panderagern_polars_schema.py

    # the panderagen schema is the default, but note that it depends on the polars schema
    gen-pandera examples/tutorial/tutorial01/personinfo.yaml > personinfo_panderagen_class_based.py

Run an example program to create a one row dataframe and validate it.
No exceptions are raised because the data matches the model.

.. code-block:: python

    import personinfo.panderagen_polars_schema as personinfo_pl
    import personinfo.panderagen_class_based as personinfo_pa
    import polars as pl

    # generated schema is more reliable than PolaRS inferred schema
    dataframe = pl.DataFrame(
      [
          {
          "id": "ORCID:1234",
          "full_name": "Clark Kent",
          "age": "32",
          "phone": "555-555-5555"
          }
      ],
      schema = personinfo_pl.Person
    )

    # Pandera validation supports more LinkML features than PolaRS.
    # Would throw an exception if validation failed.
    personinfo_pa.Person.validate(dataframe)


Generator
---------


.. autoclass:: PanderaDataframeGenerator
    :members:


Templates
---------

The panderagen module uses a templating system that allows generating different target APIs.
The currently provided templates are the default `panderagen_class_based` template and `panderagen_polars_schema`

Subclasses of :class:`.DataframeGenerator` serve as a translation layer between
the source models and schema view from :mod:`linkml_runtime` and the target models under
:mod:`.panderagen` , making clear what is needed to generate
schema code as well as what parts of the linkml metamodel are supported.


Pandera Custom Checks
---------------------

When possible the Pandera Generator implements LinkML constraints directly as Pandera checks.
Support for nested columns uses Pandera custom checks to first isolate the nested column
and then recursvely call Pandera validation.

The generated Pandera class depends on helper methods in the LinkML library at runtime to perform nested checks.


Validation and Lazyframes
-------------------------

Pandera validation can operate on lazyframes or dataframes. However when a lazyframe is validated,
checks that require collection are not run. In general this means only schema-level checks are performed on lazyframes.
The :class:`.LinkmlPanderaValidator` checks whether it is validating a dataframe or lazyframe and maintains
the same form when making nesteded validation calls.


Inlined Dictionary Handling
---------------------------

Many dataframe libraries do not handle dictionaries efficiently. Inlining objects as lists is an efficient alternative.
The pandera generator supports transforming dictionaries to lists either at load time (preferred) or at validation time.

The implementation of the load-time transform makes use of several generated schemas:
- PolaRS serialized form
- PolaRS loaded form
- Pandera serialized form
- Pandera loaded form

The PolaRS serialized form represents any inlined dictionary as an opaque pl.Object.
This schema is compatible with loading dataframes using `polars.read_json` or `pl.DataFrame()`.
The PolaRS loaded form uses lists rather than dictionaries for inlining.
To transform between the forms, the pandera generator can also generate a load transform module.
The transform currently only implements the load direction.
The generator also generates serialized and loaded forms of the Pandera schema.

Not all of these schemas are needed for every application. The example below shows
how to use all of them to load a python object into a dataframe. Note the specific model
does not actually contain dictionaries forms that require a transform.

.. code-block:: python
    import personinfo.panderagen_class_based as pcb
    import personinfo.panderagen_polars_schema_loaded as ppsl
    import personinfo.panderagen_polars_schema_transform as ppst
    import personinfo.panderagen_polars_schema as pps
    import personinfo.panderagen_schema_loaded as psl
    import polars as pl

    # some of the schema forms have informative string representations
    print(f"Panderagen (serialized): {pcb.Person}")
    print(f"Panderagen (loaded): {ppsl.Person}")
    print(f"PolaRS load transform: {ppst.Person}")
    print(f"PolaRS schema (serialized): {pps.Person}")
    print(f"PolaRS schema (loaded): {psl.Person}")

    p = pl.DataFrame([
          {
            "full_name": "Old Joe Clark",
            "age": 23
          }
        ],
        schema=pps.Person
    )
    pcb.Person.validate(p)

    print(p)

    p_loaded = ppst.Person().load(p)
    psl.Person.validate(p_loaded)

Development Notes
-----------------

This generator supports Pandera, which is a validator. To assist with loading or constructing dataframes that conform to the model,
the underlying PolaRS dataframe schema is also generated. Transforming the forms found in the unit tests and existing models are also
prioritized in future development.

Following nested objects (and eventually foreign-key associations) relies on using PolaRS expressions API for efficiency.
These may make greater use of the Narwhals API for more general support of additional dataframe libraries in the future.

Testing
-------

The panderagen package is tested against the subset of the LinkML compliance tests
that it currently implements. There is also a specific test for the generator that
emphasizes the dataframe nature of the validation.

To test panderagen compliance use the `-m panderagen` pytest mark. Use `-m dataframe_polars_schema` for the PolaRS compliance.

.. code-block:: sh

    pytest -m panderagen tests/test_compliance
    pytest -m dataframe_polars_schema tests/test_compliance


In the tests, the optional LinkML dependencies such as NumPy, PolaRS, and Pandera
are wrapped in test fixtures and imported using pytest.importerskip.
This prevents test collection errors and skips the tests when the optional packages
are not installed.


Future Roadmap
--------------

The following major features need to be prioritized

- ability to generate a schema from examples/PersonSchema/personinfo.yaml
- Foreign key associations
- Expand the transformer model to support literal types (datetime cases) and boolean constraints.
- Model and slot inheritance, including abstract models
- Generalize support for additional dataframe libraries
  - Parquet/PyArrow storage formats
  - PySpark (also supported by Pandera)
  - Narwhals (general dataframe API wrapper)
- Improve modularity
  - leverage and align with existing linkml-runtime modules and tables
- Top-level validator cli tool under linkml/validators
- Ability to use the generated Pandera without a runtime LinkML dependency.
- Cardinality checks over entire dataframe columns
