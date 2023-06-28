import copy
from typing import Dict

import jsonschema
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.utils.generator import Generator
from linkml.validator.models import SeverityOptions, ValidationReport, ValidationResult
from linkml.validator.plugins.base import BasePlugin
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.formatutils import camelcase
from linkml.validator.utils import get_jsonschema, truncate


class JsonSchemaValidationPlugin(BasePlugin):
    """
    Plugin to perform JSONSchema validation.
    """

    NAME = "JsonSchemaValidationPlugin"

    def __init__(self, schema: str, generator: Generator = JsonSchemaGenerator, **kwargs) -> None:
        """
        Intialize the plugin and generate the JSON Schema for the given schema.

        Args:
            schema: Path or URL to schema YAML
            generator: A generator instance that will be used to create the required artifact
            kwargs: Additional arguments that are used to instantiate the plugin

        """
        super().__init__(schema)
        if "generator_args" in kwargs:
            generator_args = kwargs["generator_args"]
        else:
            generator_args = {}
        self.jsonschema_obj = get_jsonschema(
            schema=self.schema,
            generator=generator,
            **generator_args
        )
        self.jsonschema_obj_map = self._generate_jsonschema_obj_map(self.jsonschema_obj)

    def _generate_jsonschema_obj_map(self, jsonschema_obj: Dict) -> Dict:
        """
        Generate JSON Schema representation for all classes
        in the schema.

        Args:
            jsonschema_obj: The JSON Schema object

        Returns:
            A dictionary containing class-specific JSON Schema objects

        """
        jsonschema_obj_map = {}
        schemaview = SchemaView(self.schema)
        for class_name, class_def in schemaview.all_classes().items():
            if not class_def.mixin:
                formatted_name = camelcase(class_name)
                if class_def.abstract:
                    # Skip abstract classes
                    continue
                if formatted_name not in jsonschema_obj_map:
                    target_jsonschema_obj = copy.deepcopy(jsonschema_obj)
                    target_jsonschema_obj['properties'] = jsonschema_obj["$defs"][formatted_name].get('properties', {})
                    target_jsonschema_obj['required'] = jsonschema_obj["$defs"][formatted_name].get('required', [])
                    jsonschema_obj_map[formatted_name] = target_jsonschema_obj
        return jsonschema_obj_map

    def process(self, obj: Dict, **kwargs) -> ValidationReport:
        """
        Perform validation on an object.

        Args:
            obj: The object to validate
            kwargs: Additional arguments

        Returns:
            An instance of ValidationReport for the object

        """
        if "target_class" not in kwargs:
            raise Exception("Need `target_class` argument")
        if "truncate_message" in kwargs:
            truncate_message = kwargs["truncate_message"]
        else:
            truncate_message = False
        target_class = kwargs["target_class"]
        valid = True
        jsonschema_obj = self.jsonschema_obj_map[target_class]
        validator = jsonschema.Draft7Validator(jsonschema_obj)
        errors = [x for x in validator.iter_errors(obj)]
        results = []
        if errors:
            for error in errors:
                result = ValidationResult(
                            type=f"[{self.NAME}] jsonschema.Draft7Validator errors",
                            severity=SeverityOptions.ERROR,
                            subject=obj,
                            instantiates=target_class,
                            predicate=".".join(map(str, error.absolute_path)) if error.absolute_path else None,
                            object=error.instance if not isinstance(error.instance, dict) else None,
                            object_str=str(error.instance if not isinstance(error.instance, dict) else None),
                            info=truncate(error.message) if truncate_message else error.message
                        )
                results.append(result)
                for suberror in sorted(error.context, key=lambda e: e.schema_path):
                    result = ValidationResult(
                                type=f"[{self.NAME}] jsonschema.Draft7Validator suberrors",
                                severity=SeverityOptions.ERROR,
                                subject=obj,
                                instantiates=target_class,
                                predicate=".".join(map(str, suberror.absolute_path)) if suberror.absolute_path else None,
                                object=suberror.instance if not isinstance(suberror.instance, dict) else None,
                                object_str=str(suberror.instance if not isinstance(suberror.instance, dict) else None),
                                info=truncate(suberror.message) if truncate_message else suberror.message
                            )
                    results.append(result)
        return results
