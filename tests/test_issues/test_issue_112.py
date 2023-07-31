import datetime

import pytest
import requests

from linkml.generators.yumlgen import YumlGenerator

now = datetime.datetime.now()


@pytest.mark.network
def test_prefix(input_path, snapshot, frozen_time):
    output = YumlGenerator(input_path("issue_112.yaml")).serialize()
    assert output == snapshot("issue112.yuml")

    frozen_time.move_to(now)
    resp = requests.get(output)
    assert resp.ok
