from linkml_runtime import SchemaView

from linkml.utils.schema_fixer import SchemaFixer

MY_CLASS = "MyClass"
MY_CLASS2 = "MyClass2"
MY_ENUM = "MyEnum"
ID = "id"
FULL_NAME = "full_name"
DESC = "description"
LIVING = "Living"
DEAD = "Dead"


def test_nmdc_submission_schema(input_path):
    """
    Tests https://github.com/linkml/linkml/issues/954
    """
    NMDC_SCHEMA = input_path("nmdc_submission_schema.yaml")
    view = SchemaView(NMDC_SCHEMA)
    s = view.schema
    fixer = SchemaFixer()
    fixer.remove_redundant_slot_usage(s)
    assert len(fixer.history) > 100

    jgi = s.classes["soil_jgi_mg"].slot_usage
    jgi_ecosystem = jgi["ecosystem"]
    assert "slot_group" in jgi_ecosystem
    assert "required" in jgi_ecosystem
    assert "range" in jgi_ecosystem
    assert "description" not in jgi_ecosystem
    assert "name" not in jgi_ecosystem
    assert "owner" not in jgi_ecosystem
