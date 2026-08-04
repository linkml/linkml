from copy import deepcopy

import pytest

from linkml.generators.pydanticgen import PydanticGenerator
from linkml.generators.pythongen import PythonGenerator
from linkml_runtime.loaders import json_loader

SCHEMA = """
id: https://example.org/discriminator-test
name: discriminator_test

prefixes:
  ex: https://example.org/
  linkml: https://w3id.org/linkml/

default_prefix: ex

imports:
  - linkml:types

slots:
  schema_type:
    range: uriorcurie
    designates_type: true

  members:
    range: Thing
    multivalued: true
    inlined: true
    inlined_as_list: true

classes:
  Record:
    slots:
      - members

  Thing:
    slots:
      - schema_type

  Association:
    is_a: Thing
    class_uri: https://example.org/Association

  Outside:
    class_uri: https://example.org/Outside
"""


def test_full_uri_type_designator_loads_generated_subclass():
    pydantic_model = PydanticGenerator(SCHEMA).compile_module()
    python_model = PythonGenerator(SCHEMA).compile_module()
    record = pydantic_model.Record(members=[pydantic_model.Association()])

    payload = record.model_dump(mode="json", exclude_none=True)
    assert payload["members"][0]["schema_type"] == "https://example.org/Association"

    for designator in ("ex:Association", "https://example.org/Association"):
        candidate = deepcopy(payload)
        candidate["members"][0]["schema_type"] = designator

        loaded = json_loader.load(candidate, target_class=python_model.Record)

        assert isinstance(loaded.members[0], python_model.Association)
        assert loaded.members[0].schema_type == "ex:Association"


@pytest.mark.parametrize(
    "designator",
    [
        "ex:Unknown",
        "https://example.org/Unknown",
        "ex:Outside",
        "https://example.org/Outside",
    ],
)
def test_type_designator_rejects_unknown_or_out_of_hierarchy_class(designator):
    python_model = PythonGenerator(SCHEMA).compile_module()
    payload = {"members": [{"schema_type": designator}]}

    with pytest.raises(ValueError, match="Wrong type designator value"):
        json_loader.load(payload, target_class=python_model.Record)
