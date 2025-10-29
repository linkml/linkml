from jsonasobj2 import loads
from linkml_runtime.linkml_model.meta import LINKML

from linkml import LOCAL_TYPES_YAML_FILE
from linkml.generators.shexgen import ShExGenerator


def test_uri_type():
    """URI datatype should map to ShEx URI instead of NONLITERAL"""
    shex = loads(ShExGenerator(LOCAL_TYPES_YAML_FILE, format="json").serialize())
    uri_shape = [s for s in shex.shapes if s.id == str(LINKML.Uri)]
    assert len(uri_shape) == 1
    assert uri_shape[0].nodeKind == "iri"
