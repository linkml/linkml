from functools import lru_cache

from linkml_runtime.linkml_model import SchemaDefinition

from linkml.generators.jsonschemagen import JsonSchemaGenerator


class ValidationContext:
    """Provides state that may be shared between validation plugins"""

    def __init__(self, schema: SchemaDefinition, target_class: str) -> None:
        self.schema = schema
        self.target_class = target_class

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ValidationContext):
            return False

        return self.schema.id == other.schema.id and self.target_class == other.target_class

    def __hash__(self) -> int:
        return hash((self.schema.id, self.target_class))

    @lru_cache
    def json_schema(self, *, closed):
        not_closed = not closed
        jsonschema_gen = JsonSchemaGenerator(
            schema=self.schema,
            mergeimports=True,
            top_class=self.target_class,
            not_closed=not_closed,
        )
        return jsonschema_gen.generate()
