from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.schema_renamer import SchemaRenamer

MAP = {
    ClassDefinition: lambda s: s.upper(),
    SlotDefinition: lambda s: f"{s.lower()}_slot",
    EnumDefinition: lambda s: f"{s.lower()}_ENUM",
}


def test_renamer(input_path):
    """Test Relational Model Transform on personinfo.yaml schema."""
    sv = SchemaView(input_path("personinfo.yaml"))
    renamer = SchemaRenamer(rename_function_map=MAP)
    rschema = renamer.rename_elements(sv.schema)
    sv2 = SchemaView(yaml_dumper.dumps(rschema))
    p = sv2.get_class("PERSON")
    assert "primary_email_slot" in p.slots
    diagnosis_slot = sv2.induced_slot("diagnosis_slot", "MEDICALEVENT")
    assert diagnosis_slot.range == "DIAGNOSISCONCEPT"
