import pytest
import requests

from linkml.generators.yumlgen import YumlGenerator


@pytest.mark.network
def test_domain_slots(input_path):
    """has_phenotype shouldn't appear in the UML graph"""
    yuml = YumlGenerator(input_path("issue_12.yaml")).serialize()
    expected = (
        "https://yuml.me/diagram/nofunky;dir:TB/class/[BiologicalEntity]++- "
        "required thing 0..1>[PhenotypicFeature],[BiologicalEntity]"
    )
    assert yuml == expected

    resp = requests.get(yuml)
    assert resp.ok
