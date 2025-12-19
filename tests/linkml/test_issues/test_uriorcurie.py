import pytest

from linkml.utils.schemaloader import SchemaLoader


def test_uriorcurie_error(input_path):
    """ """
    match = r'Slot: "s1" - subproperty_of: "homologous to" does not reference a slot definition'
    with pytest.raises(ValueError, match=match):
        SchemaLoader(input_path("issue_uriorcurie.yaml")).resolve()
