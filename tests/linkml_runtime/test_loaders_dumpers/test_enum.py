import json

import yaml

from linkml_runtime.dumpers import json_dumper, yaml_dumper
from linkml_runtime.loaders import json_loader
from tests.linkml_runtime.test_loaders_dumpers.models.enum_model import Organism, StateEnum


def test_enum():
    """
    Tests that enums are encoded as json correctly

    * https://github.com/linkml/linkml/issues/337
    * https://github.com/linkml/linkml/issues/119
    """
    i = Organism(state="LIVING")
    print(i)
    print(i.state)
    print(i.state.code)
    print(i.state.code.text)
    print(type(i.state))
    print(StateEnum.LIVING)

    # Test string representation and enum code
    assert str(i.state) == "LIVING"
    assert i.state.code == StateEnum.LIVING

    # Test JSON dumping/loading
    obj = json.loads(json_dumper.dumps(i))
    assert obj["state"] == "LIVING"

    # Test YAML dumping
    obj = yaml.safe_load(yaml_dumper.dumps(i))
    assert obj["state"] == "LIVING"

    # Test round-trip JSON serialization
    reconstituted = json_loader.loads(json_dumper.dumps(i), target_class=Organism)
    print(f"RECONSTITUTED = {reconstituted}")
    assert reconstituted.state.code == StateEnum.LIVING


def test_as_value():
    """Test that _as_value() returns a plain string, not a PermissibleValue.

    This is the fix for https://github.com/linkml/linkml/issues/2382:
    enum values must serialize as simple strings, not as dicts like ``{'text': 'LIVING'}``.
    """
    enum_val = StateEnum("LIVING")
    result = enum_val._as_value()
    assert result == "LIVING"
    assert isinstance(result, str)


def test_enum_serializes_as_string_not_dict():
    """Verify that enum-valued slots serialize as plain strings in both JSON and YAML.

    Regression test for https://github.com/linkml/linkml/issues/2382
    where PermissibleValue('infant') serialized as ``{'text': 'infant'}`` instead of ``'infant'``.
    """
    i = Organism(state="DEAD")

    # JSON serialization should produce a plain string value, not a dict
    json_str = json_dumper.dumps(i)
    obj = json.loads(json_str)
    assert obj["state"] == "DEAD"
    assert isinstance(obj["state"], str), f"Expected str, got {type(obj['state'])}: {obj['state']}"

    # YAML serialization should produce a plain string value, not a mapping
    yaml_str = yaml_dumper.dumps(i)
    obj = yaml.safe_load(yaml_str)
    assert obj["state"] == "DEAD"
    assert isinstance(obj["state"], str), f"Expected str, got {type(obj['state'])}: {obj['state']}"
