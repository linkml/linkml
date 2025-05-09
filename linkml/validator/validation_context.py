import json
import os
from functools import lru_cache
from typing import Optional

import jsonschema
from jsonschema.protocols import Validator
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition

from linkml.generators import JsonSchemaGenerator, PydanticGenerator
from linkml.utils.datautils import infer_root_class


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
    def json_schema_validator(
        self,
        *,
        closed: bool,
        include_range_class_descendants: bool,
        path_override: Optional[os.PathLike] = None,
    ) -> Validator:
        if path_override:
            with open(path_override) as json_schema_file:
                json_schema = json.load(json_schema_file)
        else:
            not_closed = not closed
            jsonschema_gen = JsonSchemaGenerator(
                schema=self._schema,
                mergeimports=True,
                top_class=self._target_class,
                not_closed=not_closed,
                include_range_class_descendants=include_range_class_descendants,
            )
            json_schema = jsonschema_gen.generate()

        validator_cls = jsonschema.validators.validator_for(json_schema, default=jsonschema.Draft7Validator)
        return validator_cls(json_schema, format_checker=validator_cls.FORMAT_CHECKER)

    def pydantic_model(self, *, closed: bool):
        module = self._pydantic_module(closed=closed)
        return module.__dict__[self._target_class]

    @lru_cache
    def _pydantic_module(self, *, closed: bool):
        return PydanticGenerator(
            self._schema,
            extra_fields="forbid" if closed else "ignore" if closed is None else "allow",
        ).compile_module()

    def _get_target_class(self, target_class: Optional[str] = None) -> str:
        if target_class is None:
            return infer_root_class(self._schema_view)
        else:
            # strict=True raises ValueError if class is not found in schema
            class_def = self._schema_view.get_class(target_class, strict=True)
            return class_def.name
