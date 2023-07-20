import datetime

import pytest
import requests

from linkml.generators.yumlgen import YumlGenerator

# Get the "real" now before it is frozen within the test
now = datetime.datetime.now()


@pytest.mark.network
def test_domain_slots(input_path, frozen_time):
    """has_phenotype shouldn't appear in the UML graph"""
    yuml = YumlGenerator(input_path("issue_12.yaml")).serialize()
    expected = (
        "https://yuml.me/diagram/nofunky;dir:TB/class/[BiologicalEntity]++- "
        "required thing 0..1>[PhenotypicFeature],[BiologicalEntity]"
    )
    assert yuml == expected

    # Need to move the frozen time ahead to avoid SSL issues
    frozen_time.move_to(now)
    resp = requests.get(yuml)
    assert resp.ok
