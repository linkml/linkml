import logging
import re
import numpy as np
import pytest

from linkml.generators.panderagen import PanderaGenerator

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def np():
    """The numpy package is optional? so use fixtures and importorskip to only run tests when it's installed
    """
    return pytest.importorskip("numpy", minversion="1.0", reason="Polars >= 1.0 not installed")


@pytest.fixture(scope="module")
def pl():
    """The PolaRS package is optional, so use fixtures and importorskip to only run tests when it's installed
    """
    return pytest.importorskip("polars", minversion="1.0", reason="Polars >= 1.0 not installed")

@pytest.fixture(scope="module")
def pandera():
    """The pandera package is optional, so use fixtures and importorskip to only run tests when it's installed
    """
    return pytest.importorskip("pandera", reason="Pandera not installed")


@pytest.fixture(scope="module")
def N():
    """Number of rows in the test dataframes, 100K is enough to be real but not strain most machines.
    """
    return 100000

# for use with Person age_in_years column
OK_AGE_RANGE = 99
MAX_AGE = 999


@pytest.fixture(scope="module")
def big_person_dataframe(pl, np, N):
    """Construct a dataframe with person records (id, name, age_in_years) using efficient numpy and polars operations
    """
    return (
        pl.DataFrame({
            "id": np.arange(0, N)
        })
        .select(
            pl.col("id").cast(pl.Utf8),
            pl.concat_str(
                pl.lit("Person "),
                pl.col("id")
            ).alias("name"),
            (pl.col("id") % OK_AGE_RANGE).alias("age_in_years")
        )
    )


@pytest.fixture(scope="module")
def schema(input_path):
    return str(input_path("personinfo.yaml"))


@pytest.fixture(scope="module")
def generator(schema):
    return PanderaGenerator(schema)


@pytest.fixture(scope="module")
def compiled_schema_module(generator):
    return generator.compile_pandera(compile_python_dataclasses=False)


def test_pandera_basic_class_based(generator):
    """
    Test generation of Pandera for classed-based mode

    This test will check the generated python, but does not include a compilation step
    """
    code = generator.generate_pandera()  # default is class-based

    logger.info(f"generated Pandera model:\n{code}")

    classes = []

    class_declaration_re = re.compile(r"class (\S+)\(")

    for item in code.splitlines():
        match = class_declaration_re.search(item)
        if match:
            classes.append(match.group(1))

    expected_classes = [
        "NamedThing",
        "Person",
        "Organization",
        "Place",
        "Address",
        "Event",
        "NewsEvent",
        "WithLocation",
        "Concept",
        "DiagnosisConcept",
        "ProcedureConcept",
        "Relationship",
        "FamilialRelationship",
        "HasAliases",
        "HasNewsEvents",
        "IntegerPrimaryKeyObject",
        "EmploymentEvent",
        "MedicalEvent",
        "Container" # check if this is expected
    ]

    assert sorted(expected_classes) == sorted(classes)


def test_pandera_compile_basic_class_based(compiled_schema_module, big_person_dataframe):
    """
    tests compilation and validation of correct class-based schema
    """
    # raises pandera.errors.SchemaErrors, so no assert needed
    compiled_schema_module.Person.validate(big_person_dataframe, lazy=True) 


def test_pandera_validation_error_ge(pl, pandera, compiled_schema_module, big_person_dataframe):
    """
    tests ge range validation error
    """
    high_age_dataframe = (
        big_person_dataframe
        .with_columns(
            (pl.col("age_in_years") + MAX_AGE).alias("age_in_years")
        )
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_schema_module.Person.validate(high_age_dataframe, lazy=True)

    assert "DATAFRAME_CHECK" in str(e)
    assert "'column': 'age_in_years'" in str(e)


def test_pandera_validation_error_it_type(pl, pandera, compiled_schema_module, big_person_dataframe):
    """
    tests incorrect datatype of a dataframe column
    """
    high_age_dataframe = (
        big_person_dataframe
        .with_columns(
            pl.col("id").cast(pl.Int32).alias("id")
        )
    )

    with pytest.raises(pandera.errors.SchemaErrors) as e:
        compiled_schema_module.Person.validate(high_age_dataframe, lazy=True)

    assert "WRONG_DATATYPE" in str(e.value)
    assert "'column': 'id'" in str(e)
    
