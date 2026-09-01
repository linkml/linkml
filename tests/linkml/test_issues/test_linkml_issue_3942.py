from linkml.generators.pydanticgen import PydanticGenerator
from linkml_runtime.linkml_model import (
    ClassDefinition,
    EnumDefinition,
    PermissibleValue,
    SchemaDefinition,
    SlotDefinition,
)
from linkml_runtime.utils.compile_python import compile_python


def test_pydantic_generator_correctly_reference_default_enum_values():
    """ifabsent: MyEnum(MyValue) should work when MyValue has a title."""
    schema = SchemaDefinition(
        id="ifabsent_referencing_titled_enum_value",
        name="ifabsent_referencing_titled_enum_value",
        enums=[
            EnumDefinition(
                name="LengthUnit",
                permissible_values=[
                    PermissibleValue(text="mm", title="millimeter"),
                    PermissibleValue(text="cm", title="centimeter"),
                ],
            ),
        ],
        classes=[
            ClassDefinition(
                name="MyClass",
                attributes=[SlotDefinition(name="length_unit", range="LengthUnit", ifabsent="LengthUnit(mm)")],
            ),
        ],
    )
    gen = PydanticGenerator(schema=schema)
    code = gen.serialize()
    compile_python(code)
