import pytest
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.validation_context import ValidationContext


@pytest.fixture
def tmp_file_factory(tmp_path):
    def factory(filename, contents):
        file_path = tmp_path / filename
        with open(file_path, "w") as file:
            file.write(contents)
        return str(file_path)

    return factory


@pytest.fixture(scope="module")
def validation_context(input_path) -> ValidationContext:
    schema = yaml_loader.load(input_path("personinfo.yaml"), SchemaDefinition)
    return ValidationContext(schema, "Person")
