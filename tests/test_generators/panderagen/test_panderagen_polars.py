import logging
from pathlib import Path

import pytest
from click.testing import CliRunner

from linkml.generators.panderagen import PanderaDataframeGenerator
from linkml.generators.panderagen.panderagen import DataframeGeneratorCli
from linkml.generators.panderagen.polars_schema.polars_schema_dataframe_generator import PolarsSchemaDataframeGenerator

pl = pytest.importorskip("polars", minversion="1.0", reason="Polars >= 1.0 not installed")

logger = logging.getLogger(__name__)


@pytest.fixture
def test_inputs_dir():
    return Path(__file__).parent / "input"


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture(scope="module")
def N():
    """Number of rows in the test dataframes, 1M is enough to be real but not strain most machines."""
    return 1000


@pytest.fixture(scope="module")
def synthetic_flat_dataframe_model():
    return """\
id: https://w3id.org/linkml/examples/pandera_constraints
name: test_pandera_constraints
prefixes:
  linkml: https://w3id.org/linkml/
  ex: https://w3id.org/linkml/examples/pandera_constraints/
imports:
  - linkml:types
default_range: string
default_prefix: ex

classes:

  AnyType:
    description: the magic class_uri makes this map to linkml Any or polars Object
    class_uri: linkml:Any

  ColumnType:
    description: Nested in a column
    attributes:
      id:
        identifier: true
        range: string
      x:
        range: integer
        required: true
      y:
        range: integer
        required: true

  SimpleDictType:
    description: Nested as a simple dict
    attributes:
      id:
        identifier: True
        range: string
      x:
        range: integer
        required: true

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
        #ifabsent: true
      integer_column:
        description: test integer column with min/max values
        range: integer
        required: true
        minimum_value: 0
        maximum_value: 999
        #ifabsent: int(5)
      float_column:
        description: test float column
        range: float
        required: true
        #ifabsent: float(2.3)
      string_column:
        description: test string column
        range: string
        required: true
        pattern: "^(this)|(that)|(whatever)$"
        #ifabsent: string("whatever")
      date_column:
        description: test date column
        range: date
        required: true
        #ifabsent: date("2020-01-31")
      datetime_column:
        description: test datetime column
        range: datetime
        required: true
        #ifabsent: datetime("2020-01-31 03:23:57")
      enum_column:
        description: test enum column
        range: SyntheticEnum
        required: true
      ontology_enum_column:
        description: test enum column with ontology values
        range: SyntheticEnumOnt
        required: true
        #ifabsent: SyntheticEnumOnt(ANIMAL)
      multivalued_column:
        description: one-to-many form
        range: integer
        required: true
        multivalued: true
        inlined_as_list: true
      # multivalued_one_many_column:
      #   description: list form
      #   range: integer
      #   required: true
      #   multivalued: true
      any_type_column:
        description: needs to have type object
        range: AnyType
        required: true
      cardinality_column:
        description: check cardinality
        range: integer
        required: true
        minimum_cardinality: 1
        maximum_cardinality: 1
      inlined_as_object_column:
        description: test column that is a directly nested single object
        range: ColumnType
        required: true
        inlined: true
        multivalued: false
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


enums:
  SyntheticEnum:
    description: simple enum for tests
    permissible_values:
      ANIMAL:
      VEGETABLE:
      MINERAL:

  SyntheticEnumOnt:
    description: ontology enum for tests
    permissible_values:
      fiction: ex:000001
      non fiction: ex:000002
"""


MODEL_COLUMNS = [
    "identifier_column",
    "bool_column",
    "integer_column",
    "float_column",
    "string_column",
    "date_column",
    "datetime_column",
    "enum_column",
    "ontology_enum_column",
    "multivalued_column",
    "any_type_column",
    "cardinality_column",
    "inlined_as_object_column",
    "inlined_class_column",
    "inlined_as_list_column",
    "inlined_simple_dict_column",
]


@pytest.fixture(scope="module")
def column_type_instances():
    """valid ColumnType instances that can be used in tests"""
    return [
        pl.struct(
            pl.lit("thing_one").alias("id"),
            pl.lit(1111, dtype=pl.Int64).alias("x"),
            pl.lit(2222, dtype=pl.Int64).alias("y"),
        ),
        pl.struct(
            pl.lit("thing_two").alias("id"),
            pl.lit(3333, dtype=pl.Int64).alias("x"),
            pl.lit(4444, dtype=pl.Int64).alias("y"),
        ),
    ]


@pytest.fixture(scope="module")
def invalid_column_type_instances():
    """invalid (float values) ColumnType instances that can trigger failures."""
    return [
        pl.struct(
            pl.lit("thing_one").alias("id"),
            pl.lit(1111.0).alias("x"),
            pl.lit(2222.0).alias("y"),
        ),
        pl.struct(
            pl.lit("thing_two").alias("id"),
            pl.lit(3333.0).alias("x"),
            pl.lit(4444.0).alias("y"),
        ),
    ]


@pytest.fixture(scope="module")
def valid_inlined_dict_column_expression(pl, column_type_instances):
    """synthetic data that conforms to the inlined_class_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
        column_type_instances[0].alias("thing_one"),
        column_type_instances[1].alias("thing_two")
    )
    # fmt: on


@pytest.fixture(scope="module")
def invalid_inlined_dict_column_expression(pl, invalid_column_type_instances):
    """synthetic data that conforms to the inlined_class_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
        invalid_column_type_instances[0].alias("thing_one"),
        invalid_column_type_instances[1].alias("thing_two")
    )
    # fmt: on


@pytest.fixture(scope="module")
def valid_simple_dict_column_expression(pl):
    """synthetic data that conforms to the inlined_simple_dict_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
      pl.lit(1).alias("A"),
      pl.lit(2).alias("B"),
      pl.lit(3).alias("C")
    )
    # fmt: on


@pytest.fixture(scope="module")
def invalid_simple_dict_column_expression(pl):
    """synthetic data with float values that does not conform to the inlined_simple_dict_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.struct(
      pl.lit(1.0).alias("A"),
      pl.lit(2.0).alias("B"),
      pl.lit(3.0).alias("C")
    )
    # fmt: on


@pytest.fixture(scope="module")
def valid_inlined_as_list_column_expression(pl, np, N):
    """synthetic data that conforms to the inlined_as_list_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.concat_list([
      pl.struct(
          pl.Series(values=np.arange(0, N), dtype=pl.Int64).cast(pl.Utf8).alias("id"),
          pl.Series(values=np.random.choice([0, 1], size=N), dtype=pl.Int64).alias("x"),
          pl.Series(values=np.random.choice([0, 1], size=N), dtype=pl.Int64).alias("y")
      )
    ])
    # fmt: on


@pytest.fixture(scope="module")
def invalid_inlined_as_list_column_expression(pl, np, N):
    """synthetic data that does not conforms to the inlined_as_list_column schema
    using polars expression API.
    """
    # fmt: off
    return pl.concat_list([
      pl.struct(
          pl.Series(values=np.arange(0, N), dtype=pl.Int64).cast(pl.Utf8).alias("id"),
          pl.Series(values=np.random.choice([0.0, 1.0], size=N), dtype=pl.Float64).alias("x"),
          pl.Series(values=np.random.choice([0.1, 1.0], size=N), dtype=pl.Float64).alias("y")
      )
    ])
    # fmt: on


@pytest.fixture(scope="module")
def big_synthetic_dataframe(
    pl,
    np,
    N,
    valid_inlined_dict_column_expression,
    valid_simple_dict_column_expression,
    valid_inlined_as_list_column_expression,
    column_type_instances,
):
    """Construct a reasonably sized dataframe that complies with the PanderaSyntheticTable model"""
    test_enum = pl.Enum(["ANIMAL", "VEGETABLE", "MINERAL"])
    test_ont_enum = pl.Enum(["fiction", "non fiction"])

    # fmt: off
    df = (
        pl.DataFrame(
            {
                "identifier_column": pl.Series(np.arange(0, N), dtype=pl.Int64),
                "bool_column": pl.Series(np.random.choice([True, False], size=N), dtype=pl.Boolean),
                "integer_column": pl.Series(np.random.choice(range(100), size=N), dtype=pl.Int64),
                "float_column": pl.Series(np.random.choice([1.0, 2.0, 3.0], size=N), dtype=pl.Float64),
                "string_column": np.random.choice(["this", "that"], size=N),
                "date_column": pl.Series(
                    np.random.choice(["2021-03-27", "2021-03-28"], size=N),
                    dtype=pl.Date,
                    strict=False
                ),
                "datetime_column": pl.Series(
                    np.random.choice(["2021-03-27T03:00:00", "2021-03-28T03:00:00"], size=N),
                    dtype=pl.Datetime,
                    strict=False
                ),
                "enum_column": pl.Series(
                    np.random.choice(["ANIMAL", "VEGETABLE", "MINERAL"], size=N),
                    dtype=test_enum,
                    strict=False
                ),
                "ontology_enum_column": pl.Series(
                    np.random.choice(["fiction", "non fiction"], size=N),
                    dtype=test_ont_enum,
                    strict=False
                ),
                "multivalued_column": [[1, 2, 3],] * N,
                "any_type_column": pl.Series([1,] * N, dtype=pl.Object),
                "cardinality_column": pl.Series(np.arange(1, N+1), dtype=pl.Int64),
            }
        )
        .with_columns(
            column_type_instances[0].alias("inlined_as_object_column"),
            valid_simple_dict_column_expression.alias("inlined_simple_dict_column"),
            valid_inlined_as_list_column_expression.alias("inlined_as_list_column"),
            valid_inlined_dict_column_expression.alias("inlined_class_column")
        )
    )
    # fmt: on

    return df


@pytest.fixture(scope="module")
def synthetic_schema(synthetic_flat_dataframe_model):
    return PanderaDataframeGenerator(synthetic_flat_dataframe_model)


@pytest.fixture(scope="module")
def compiled_synthetic_schema_module(synthetic_schema):
    return synthetic_schema.compile_dataframe_model()


@pytest.fixture(scope="module")
def generator():
    yamlfile = "/Users/tpfliss/git/linkml/examples/PersonSchema/personinfo.yaml"

    #
    # OK, this bit needs to be fixed, it's not clear how it works
    #
    return PolarsSchemaDataframeGenerator(yamlfile)


@pytest.fixture(scope="module")
def polars_generator_cli(generator):
    generator = DataframeGeneratorCli(
        generator=generator, template_path="panderagen_polars_schema", template_file="polars_schema.jinja2"
    )

    return generator


@pytest.fixture(scope="module")
def compiled_model(polars_generator_cli):
    print(polars_generator_cli.serialize())
    model = polars_generator_cli.generator.compile_dataframe_model()

    return model


@pytest.mark.parametrize(
    "class_name, data",
    [
        (
            "NamedThing",
            {
                "id": ["a", "b", "c"],
                "name": ["one", "two", "three"],
                "description": ["thing one", "thing two", "thing three"],
                "depicted_by": [
                    "http://example.org/image_one.jpg",
                    "http://example.org/image_two.jpg",
                    "http://example.org/image_three.jpg",
                ],
            },
        ),
        (
            "Person",
            {
                "id": ["1", "2", "3"],
                "name": ["P. One", "P. Two", "P. Three"],
                "description": ["Person One", "Person Two", "Person Three"],
                "depicted_by": [
                    "http://example.org/image_one.jpg",
                    "http://example.org/image_two.jpg",
                    "http://example.org/image_three.jpg",
                ],
                "primary_email": ["one@example.org", "two@example.org", "three@example.org"],
                "birth_date": ["1900-01-01", "1900-01-02", "1900-01-03"],
                "age": [125, 125, 125],
                "gender": ["cisgender man", "transgender woman", "cisgender woman"],
                "current_address": [
                    {"street": "1 Maple Street", "city": "Springfield, AZ", "postal_code": "12345"},
                    {"street": "1 Maple Street", "city": "Springfield, AZ", "postal_code": "12345"},
                    {"street": "1 Maple Street", "city": "Springfield, AZ", "postal_code": "12345"},
                ],
                "telephone": ["800-555-1111", "800-555-2222", "800-555-3333"],
                "has_employment_history": [None, None, None],
                "has_familial_relationships": [None, None, None],
                "has_interpersonal_relationships": [None, None, None],
                "has_medical_history": [None, None, None],
                "has_news_events": [None, None, None],
                "aliases": [None, None, None],
            },
        ),
        (
            "Organization",
            {
                "id": ["a", "b", "c"],
                "name": ["one", "two", "three"],
                "description": ["thing one", "thing two", "thing three"],
                "depicted_by": [
                    "http://example.org/image_one.jpg",
                    "http://example.org/image_two.jpg",
                    "http://example.org/image_three.jpg",
                ],
                "aliases": [None, None, None],
                "mission_statement": ["one", "two", "three"],
                "founding_date": ["1900-01-01", "1900-01-02", "1900-01-03"],
                "founding_location": ["a", "b", "c"],
                "categories": [None, None, None],
                "score": [None, None, None],
                "min_salary": [None, None, None],
                "has_news_events": [None, None, None],
            },
        ),
        (
            "Place",
            {
                "id": ["a", "b", "c"],
                "name": ["one", "two", "three"],
                "aliases": [None, None, None],
                "depicted_by": [
                    "http://example.org/image_one.jpg",
                    "http://example.org/image_two.jpg",
                    "http://example.org/image_three.jpg",
                ],
            },
        ),
    ],
)
def test_stub(compiled_model, class_name, data):
    schema_class = getattr(compiled_model, class_name)
    print(
        "DIFF: "
        + ", ".join(list(set(schema_class.keys()) - set(data.keys())))
        + " / , ".join(list(set(data.keys()) - set(schema_class.keys())))
    )
    print(schema_class)
    print(data)

    df = pl.DataFrame(data, schema=schema_class)

    assert df is not None
