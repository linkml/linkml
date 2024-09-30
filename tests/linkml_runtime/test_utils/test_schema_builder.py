import pytest

from linkml_runtime.utils.schema_builder import SchemaBuilder
from linkml_runtime.linkml_model import ClassDefinition


@pytest.mark.parametrize("replace_if_present", [True, False])
def test_add_existing_class(replace_if_present):
    """
    Test the case of adding a class with a name that is the same as a class that already
    exists in the schema
    """
    builder = SchemaBuilder()

    cls_name = "Person"

    # Add a class to the schema
    cls = ClassDefinition(name=cls_name, slots=["name"])
    builder.add_class(cls)

    # Add another class with the same name to the schema
    cls_repeat = ClassDefinition(name=cls_name, slots=["age"])

    if replace_if_present:
        builder.add_class(cls_repeat, replace_if_present=True)
        assert builder.schema.classes[cls_name].slots == ["age"]
    else:
        with pytest.raises(ValueError, match=f"Class {cls_name} already exists"):
            builder.add_class(cls_repeat)
        assert builder.schema.classes[cls_name].slots == ["name"]