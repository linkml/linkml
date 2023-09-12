from functools import lru_cache

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition

from linkml.generators.jsonschemagen import JsonSchemaGenerator


class ValidationContext:
    """Provides state that may be shared between validation plugins"""

    def __init__(self, schema: SchemaDefinition, target_class: str) -> None:
        self.schema = schema
        self.schema_view = SchemaView(self.schema)
        self.target_class = self._get_target_class(target_class)
        self.cached_artefacts = {}

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

    def _get_target_class(self, target_class: str) -> str:
        if target_class is None:
            roots = [
                class_name
                for class_name, class_def in self.schema_view.all_classes().items()
                if class_def.tree_root
            ]
            if len(roots) != 1:
                raise ValueError(f"Cannot determine tree root: {roots}")
            return roots[0]
        else:
            # strict=True raises ValueError if class is not found in schema
            class_def = self.schema_view.get_class(target_class, strict=True)
            return class_def.name
