from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator, List, Optional, Union

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import SchemaDefinition

from linkml.validator.loaders import Loader
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import ValidationReport, ValidationResult
from linkml.validator.validation_context import ValidationContext


class Validator:
    """A class for coordinating instance validation using configurable plugins"""

    def __init__(
        self,
        schema: Union[str, Path, SchemaDefinition],
        validation_plugins: Optional[List[ValidationPlugin]] = None,
    ) -> None:
        """Constructor method

        :param schema: The schema to validate against. If a string or Path, the schema
            will be loaded from that location. Otherwise, a `SchemaDefinition` is required.
        :param validation_plugins: A list of plugins that be used to validate instances
            using the given schema. Each element should be an instance of a subclass of
            `linkml.validator.plugins.ValidationPlugin`. Defaults to None.
        """
        self._schema_view = SchemaView(schema)
        self._validation_plugins = validation_plugins

    def validate(self, instance: Any, target_class: Optional[str] = None) -> ValidationReport:
        """Validate the given instance

        :param instance: The instance to validate
        :param target_class: Name of the class within the schema to validate
            against. If None, the class will be inferred from the schema by
            looked for a class with `tree_root: true`. Defaults to None.
        :return: A validation report
        :rtype: ValidationReport
        """
        return ValidationReport(results=list(self.iter_results(instance, target_class)))

    def validate_source(
        self, loader: Loader, target_class: Optional[str] = None
    ) -> ValidationReport:
        """Validate instances from a data source

        :param loader: An instance of a subclass of `linkml.validator.loaders.Loader`
            which provides the instances to validate
        :param target_class: Name of the class within the schema to validate
            against. If None, the class will be inferred from the schema by
            looked for a class with `tree_root: true`. Defaults to None.
        :return: A validation report
        :rtype: ValidationReport
        """
        return ValidationReport(results=list(self.iter_results_from_source(loader, target_class)))

    def iter_results(
        self, instance: Any, target_class: Optional[str] = None
    ) -> Iterator[ValidationResult]:
        """Lazily yield validation results for the given instance

        :param instance: The instance to validate
        :param target_class: Name of the class within the schema to validate
            against. If None, the class will be inferred from the schema by
            looked for a class with `tree_root: true`. Defaults to None.
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        if not self._validation_plugins:
            return []

        target_class = self._get_target_class(target_class)
        context = ValidationContext(self._schema_view.schema, target_class)
        for plugin in self._validation_plugins:
            yield from plugin.process(instance, context)

    def iter_results_from_source(
        self, loader: Loader, target_class: Optional[str] = None
    ) -> Iterator[ValidationResult]:
        """Lazily yield validation results for the given instance

        :param loader: An instance of a subclass of `linkml.validator.loaders.Loader`
            which provides the instances to validate
        :param target_class: Name of the class within the schema to validate
            against. If None, the class will be inferred from the schema by
            looked for a class with `tree_root: true`. Defaults to None.
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        for instance in loader.iter_instances():
            yield from self.iter_results(instance, target_class)

    @lru_cache
    def _get_target_class(self, target_class: str) -> str:
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
