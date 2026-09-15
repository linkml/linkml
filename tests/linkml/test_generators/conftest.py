from pathlib import Path

import pytest

from linkml_runtime.linkml_model import ClassDefinition, SchemaDefinition
from linkml_runtime.utils.schemaview import load_schema_wrap


@pytest.fixture
def kitchen_sink_path(input_path):
    return str(input_path("kitchen_sink.yaml"))


class MyInjectedClass:
    classattr: str = "hey"

    def __init__(self, up: str = "doc"):
        self.what = up


@pytest.fixture(scope="module")
def array_anyshape(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "any_shape.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_bounded(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "bounded_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_parameterized(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "parameterized_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_complex(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "complex_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_dtype(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "dtype.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_error_complex_dimensions(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "error_complex_dimensions.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_error_complex_unbounded(input_path) -> SchemaDefinition:
    schema = str(Path(input_path("arrays")) / "error_complex_unbounded.yaml")
    return load_schema_wrap(schema)


@pytest.fixture(scope="module")
def array_validator_errors(input_path) -> ClassDefinition:
    schema_file = str(Path(input_path("arrays")) / "validator_errors.yaml")
    schema = load_schema_wrap(schema_file)
    return schema.classes["ErrorRiddenClass"]
