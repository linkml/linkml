import pytest
import requests

from linkml.generators.yumlgen import YumlGenerator


@pytest.mark.network
def test_prefix(input_path, snapshot):
    output = YumlGenerator(input_path("issue_112.yaml")).serialize()
    assert output == snapshot("issue112.yuml")

    resp = requests.get(output)
    assert resp.ok
