import json
from pathlib import Path

from linkml.generators import JsonSchemaGenerator

SCHEMA = str(Path(__file__).parent / "input" / "issue_1371" / "test.schema.yaml")


def test_json_schema():
    jschema = json.loads(JsonSchemaGenerator(SCHEMA).serialize())
    props = jschema["$defs"]["Test"]["properties"]
    assert props["de_phone_number"]["pattern"] == r"0\d{3}-\d{8}"
    assert props["us_phone_number"]["pattern"] == r"\d{3} \d{3} \d{4}"
