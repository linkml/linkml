import logging
from pathlib import Path

import pytest
from click.testing import CliRunner

from linkml.generators.panderagen.panderagen import DataframeGeneratorCli
from linkml.generators.panderagen.polars_schema.polars_schema_dataframe_generator import PolarsSchemaDataframeGenerator

pl = pytest.importorskip("polars", minversion="1.0", reason="Polars >= 1.0 not installed")
np = pytest.importorskip("numpy", reason="NumPY not installed")

logger = logging.getLogger(__name__)


@pytest.fixture
def test_inputs_dir():
    return Path(__file__).parent.parent / "input"


@pytest.fixture
def cli_runner():
    return CliRunner()


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
    "foreign_key_object_column",
    "inlined_class_column",
    "inlined_as_list_column",
    "inlined_simple_dict_column",
]


@pytest.fixture(scope="module")
def yamlfile():
    return "examples/PersonSchema/personinfo.yaml"


@pytest.fixture(scope="module")
def generator(yamlfile):
    return PolarsSchemaDataframeGenerator(yamlfile, backing_form="serialized")


@pytest.fixture(scope="module")
def polars_generator_cli(generator):
    return DataframeGeneratorCli(
        generator=generator, template_path="panderagen_polars_schema", template_file="polars_schema.jinja2"
    )


@pytest.fixture(scope="module")
def compiled_model(polars_generator_cli):
    logger.info(polars_generator_cli.serialize())
    return polars_generator_cli.generator.compile_dataframe_model("pandera_test_module")


@pytest.fixture(scope="module")
def compiled_polars_synthetic_schema_module(synthetic_flat_dataframe_model):
    generator = PolarsSchemaDataframeGenerator(synthetic_flat_dataframe_model, backing_form="serialized")
    polars_generator_cli = DataframeGeneratorCli(
        generator=generator, template_path="panderagen_polars_schema", template_file="polars_schema.jinja2"
    )
    return polars_generator_cli.generator.compile_dataframe_model("pandera_test_module")


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

    assert schema_class == "temp"


def test_synthetic_dataframe(
    big_synthetic_dataframe,
):
    """Test that the synthetic dataframe conforms to the generated pandera schema"""
    logger.info(big_synthetic_dataframe.head(5))

    assert big_synthetic_dataframe is not None


def test_dump_synthetic_df(big_synthetic_dataframe):
    logger.info(big_synthetic_dataframe)


def test_enums(compiled_polars_synthetic_schema_module):
    DemoEnum = compiled_polars_synthetic_schema_module.DemoEnum
    DemoOntologyEnum = compiled_polars_synthetic_schema_module.DemoOntologyEnum

    assert DemoEnum == "temp"
    assert DemoOntologyEnum == "temp"
