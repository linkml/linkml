from pathlib import Path
from types import ModuleType
from typing import Dict

import pytest

from linkml.generators import PydanticGenerator, PythonGenerator


@pytest.fixture(scope="module")
def person(input_path) -> Dict[str, Path]:
    return {
        "schema": input_path("personinfo.yaml"),
        "data": input_path("personinfo_data01.yaml"),
    }


@pytest.fixture(scope="function")
def tmp_outputs(tmp_path) -> Dict[str, Path]:
    return {"db": tmp_path / "tmp.db", "tsv": tmp_path / "tmp.tsv", "data": tmp_path / "tmp.yaml"}


@pytest.fixture(scope="module")
def person_python(input_path, person) -> ModuleType:
    return PythonGenerator(person["schema"]).compile_module()


@pytest.fixture(scope="module")
def person_pydantic(input_path, person) -> ModuleType:
    return PydanticGenerator(person["schema"]).compile_module()
