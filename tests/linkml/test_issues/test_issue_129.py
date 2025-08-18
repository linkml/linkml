import jsonasobj
import pytest

from linkml.generators.jsonschemagen import JsonSchemaGenerator


@pytest.mark.jsonschemagen
def test_issue_types(input_path):
    """Make sure that types are generated as part of the output"""

    gen = JsonSchemaGenerator(input_path("issue_129.yaml"))
    gen.top_class = "c"
    sobj_str = gen.serialize()

    sobj = jsonasobj.loads(sobj_str)
    defs = sobj["$defs"]
    C = defs["C"]
    props = C["properties"]
    assert "integer" in props["age_in_years"]["type"]
    assert "boolean" in props["has_prop"]["type"]
    # multivalued primitive type, inlined
    assert "array" in props["scores"]["type"]
    assert "number" in props["scores"]["items"]["type"]
    # single-valued complex type, inlined
    assert props["has_d"]["anyOf"][0]["$ref"] == "#/$defs/D"

    # multi-valued, inlined_as_list
    assert "array" in props["has_ds"]["type"]
    assert props["has_ds"]["items"]["$ref"] == "#/$defs/D"

    # multi-valued, inlined (as dict) #411
    D_id_any_of = props["has_ds2"]["additionalProperties"]["anyOf"]
    D_id_with_ref = next(d for d in D_id_any_of if "$ref" in d)
    assert D_id_with_ref
    D_id_opt = D_id_with_ref["$ref"].replace("#/$defs/", "")
    assert D_id_opt in defs
    assert defs[D_id_opt]["required"] == []
    # D has no required slots other than the id, so the inlined value can also be null
    D_type_null = next(d for d in D_id_any_of if "type" in d and d.type == "null")
    assert D_type_null

    # single-valued, non-inlined (foreign key)
    assert "string" in props["parent"]["type"]

    # multi-valued, non-inlined (foreign key)
    assert "array" in props["children"]["type"]
    assert props["children"]["items"]["type"] == "string"
