import json
import os
from functools import lru_cache
from typing import Optional

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition

from linkml.generators import JsonSchemaGenerator, PydanticGenerator


class ValidationContext:
    """Provides state that may be shared between validation plugins"""

    def __init__(self, schema: SchemaDefinition, target_class: Optional[str] = None) -> None:
        # Since SchemaDefinition is not hashable, to make caching simpler we store the schema
        # in a "private" property and assume it never changes.
        self._schema = schema
        self._schema_view = SchemaView(self._schema)
        self._target_class = self._get_target_class(target_class)

    @property
    def schema_view(self):
        return self._schema_view

    @property
    def target_class(self):
        return self._target_class

    @lru_cache
    def json_schema(
        self,
        *,
        closed: bool,
        include_range_class_descendants: bool,
        path_override: Optional[os.PathLike] = None,
    ):
        if path_override:
            with open(path_override) as json_schema_file:
                return json.load(json_schema_file)

        not_closed = not closed
        jsonschema_gen = JsonSchemaGenerator(
            schema=self._schema,
            mergeimports=True,
            top_class=self._target_class,
            not_closed=not_closed,
            include_range_class_descendants=include_range_class_descendants,
        )
        return jsonschema_gen.generate()

    def pydantic_model(self, *, closed: bool):
        module = self._pydantic_module(closed)
        return module.__dict__[self._target_class]

    @lru_cache
    def _pydantic_module(self, *closed: bool):
        return PydanticGenerator(self._schema, allow_extra=not closed).compile_module()

    def _get_target_class(self, target_class: Optional[str] = None) -> str:
        if target_class is None:
            roots = [
                class_name
                for class_name, class_def in self._schema_view.all_classes().items()
                if class_def.tree_root
            ]
            if len(roots) != 1:
                raise ValueError(f"Cannot determine tree root: {roots}")
            return roots[0]
        else:
            # strict=True raises ValueError if class is not found in schema
            class_def = self._schema_view.get_class(target_class, strict=True)
            return class_def.name
