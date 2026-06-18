import logging
import sys
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
    return polars_generator_cli.generator.compile_dataframe_model("polars_test_module")


@pytest.fixture(scope="module")
def compiled_polars_loaded_module(synthetic_flat_dataframe_model):
    generator = PolarsSchemaDataframeGenerator(synthetic_flat_dataframe_model, backing_form="loaded")
    polars_generator_cli = DataframeGeneratorCli(
        generator=generator, template_path="panderagen_polars_schema", template_file="polars_schema.jinja2"
    )
    return polars_generator_cli.generator.compile_dataframe_model("polars_loaded_module")


@pytest.fixture(scope="module")
def polars_transform_module_code(synthetic_flat_dataframe_model):
    generator = PolarsSchemaDataframeGenerator(
        synthetic_flat_dataframe_model,
        template_path="panderagen_polars_schema",
        template_file="load_transformer.jinja2",
        backing_form="transform",
    )
    serialized_code = generator.serialize()
    logger.info(f"polars transform module code:\n\n{serialized_code}")

    return serialized_code


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
@pytest.mark.skipif(sys.version_info < (3, 11), reason="typing.Optional error with structs in python < 3.11")
def test_stub(compiled_model, class_name, data):
    schema_class = getattr(compiled_model, class_name)
    logger.info(
        "DIFF: "
        + ", ".join(list(set(schema_class.keys()) - set(data.keys())))
        + " / , ".join(list(set(data.keys()) - set(schema_class.keys())))
    )
    logger.info(schema_class)
    logger.info(data)

    df = pl.DataFrame(data, schema=schema_class)

    assert df is not None


def test_synthetic_dataframe(
    big_synthetic_dataframe,
):
    """Test that the synthetic dataframe conforms to the generated pandera schema"""
    logger.info(big_synthetic_dataframe.head(5))

    assert big_synthetic_dataframe is not None


def test_dump_synthetic_df(big_synthetic_dataframe):
    logger.info(big_synthetic_dataframe)


def test_enums(compiled_polars_synthetic_schema_module):
    SyntheticEnum = compiled_polars_synthetic_schema_module.SyntheticEnum
    SyntheticEnumOnt = compiled_polars_synthetic_schema_module.SyntheticEnumOnt

    assert set(SyntheticEnum.categories) == {"ANIMAL", "VEGETABLE", "MINERAL"}
    assert set(SyntheticEnumOnt.categories) == {"fiction", "non fiction"}


def test_polars_loaded_module(compiled_polars_loaded_module):
    schema = compiled_polars_loaded_module.PanderaSyntheticTable

    for name, dtype in schema.items():
        if name == "any_type_column":
            assert str(dtype) == "Object"
        else:
            assert str(dtype) != "Object"


def test_polars_transform_module(polars_transform_module_code):
    """Verify some lines that are characteristic of the polars transform are present"""
    for expected in [
        "from . import panderagen_polars_schema as serialized_schema",
        "from . import panderagen_polars_schema_loaded as loaded_schema",
        "load(",
    ]:
        assert expected in polars_transform_module_code


_INPUT_DIR = Path(__file__).parent / "input"


# type-mapping tests
# date_or_datetime  linkml:DateOrDatetime   pl.Utf8 - Polars has no Date|Datetime union
# objectidentifier  shex:iri                pl.Utf8 - an IRI is a string
# nodeidentifier    shex:nonLiteral         pl.Utf8 - a non-literal RDF node identifier


@pytest.mark.parametrize(
    "field_name, expected_dtype",
    [
        ("dod_field", "pl.Utf8"),
        ("oid_field", "pl.Utf8"),
        ("nid_field", "pl.Utf8"),
    ],
)
def test_linkml_specific_type_mapping(field_name, expected_dtype):
    """Non-XSD LinkML builtin types resolve to correct Polars dtypes without raising ValueError."""
    generator = PolarsSchemaDataframeGenerator(str(_INPUT_DIR / "linkml_types_model.yaml"), backing_form="serialized")
    code = generator.serialize()
    assert f'"{field_name}": {expected_dtype},' in code


# cyclic-dependency regression tests


@pytest.mark.parametrize(
    "field_range, expected",
    [
        # single inlined struct reference
        ("ChildStruct", "pl.Struct(ChildDict)"),
        # multivalued inlined struct reference
        ("pl.List(ChildStruct)", "pl.List(pl.Struct(ChildDict))"),
        # primitive — must pass through unchanged
        ("pl.Utf8", "pl.Utf8"),
        # Any type — must pass through unchanged
        ("pl.Object", "pl.Object"),
        # enum name — must pass through unchanged (does not end in "Struct")
        ("CordialnessEnum", "CordialnessEnum"),
    ],
)
def test_dict_range(field_range, expected):
    """dict_range converts *Struct references to pl.Struct(*Dict) and leaves everything else alone."""
    assert PolarsSchemaDataframeGenerator.dict_range(field_range) == expected


@pytest.mark.skipif(sys.version_info < (3, 11), reason="typing.Optional error with structs in python < 3.11")
def test_parent_slot_range_child_no_cycle():
    """A parent class whose slot ranges over a child class must not raise a cyclic dependency error.

    Without the fix in ClassHandlerBase.add_dependencies_by_association the hierarchy edge
    Child→Parent and the association edge Parent→Child form a cycle in the dependency sorter.
    The generated code must also be importable (no NameError from forward references).
    Both single-valued (child_ref: ChildStruct) and multivalued (child_refs: pl.List(ChildStruct))
    cross-references are covered.
    """
    generator = PolarsSchemaDataframeGenerator(str(_INPUT_DIR / "cyclic_model.yaml"), backing_form="serialized")
    # Must not raise ValueError: Cyclic dependency detected, and the emitted code
    # must compile without NameError (forward-refs resolved via the three-pass template).
    mod = generator.compile_dataframe_model("cyclic_test_module")
    assert hasattr(mod, "ParentDict")
    assert hasattr(mod, "ChildDict")
    # Verify that the three-pass template emitted pl.List(pl.Struct(ChildDict)) for the
    # multivalued cross-reference (dict_range applied), not the bare XStruct name.
    code = generator.serialize()
    assert "pl.List(pl.Struct(ChildDict))" in code


@pytest.mark.skipif(sys.version_info < (3, 11), reason="typing.Optional error with structs in python < 3.11")
def test_peer_cycle_three_mutually_recursive_classes():
    """Three peer classes that form a cycle (no parent/child hierarchy) must
    still be generated cleanly.

    The PR #3467 ancestor-skip in ``add_dependencies_by_association`` only
    breaks parent/child association cycles. Peer cycles between
    mutually-recursive classes are common in real-world metamodels
    (``schema_definition`` ↔ ``slot_definition`` ↔ ``path_expression`` in the
    LinkML metamodel itself) and require ``DependencySorter(allow_cycles=True)``
    to handle. This test pins that behaviour down.

    The schema also includes a self-loop on Alpha to verify both fixes apply
    together — self-loops never raise, peer cycles broken under allow_cycles,
    and the three-pass polars template handles all forward references.
    """
    generator = PolarsSchemaDataframeGenerator(str(_INPUT_DIR / "peer_cycle_model.yaml"), backing_form="serialized")
    # Generation must not raise on the cycle, and the compiled module must
    # import cleanly with all three structs available.
    mod = generator.compile_dataframe_model("peer_cycle_test_module")
    assert hasattr(mod, "AlphaDict")
    assert hasattr(mod, "BetaDict")
    assert hasattr(mod, "GammaDict")
    assert hasattr(mod, "AlphaStruct")
    assert hasattr(mod, "BetaStruct")
    assert hasattr(mod, "GammaStruct")
    # The cross-references must be lifted to pl.Struct(XDict) form by the
    # three-pass template — bare XStruct would NameError because there's no
    # ordering that defines every Struct before it's referenced.
    code = generator.serialize()
    assert "pl.Struct(BetaDict)" in code
    assert "pl.Struct(GammaDict)" in code
    assert "pl.Struct(AlphaDict)" in code
