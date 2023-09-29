from pathlib import Path
from typing import Any, Iterator, List, Optional, TextIO, Union

from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.loaders import yaml_loader

from linkml.validator.loaders import Loader
from linkml.validator.loaders.passthrough_loader import PassthroughLoader
from linkml.validator.plugins import ValidationPlugin
from linkml.validator.report import ValidationReport, ValidationResult
from linkml.validator.validation_context import ValidationContext


class Validator:
    """A class for coordinating instance validation using configurable plugins"""

    def __init__(
        self,
        schema: Union[str, dict, TextIO, Path, SchemaDefinition],
        validation_plugins: Optional[List[ValidationPlugin]] = None,
    ) -> None:
        """Constructor method

        :param schema: The schema to validate against. If a string or Path, the schema
            will be loaded from that location. Otherwise, a `SchemaDefinition` is required.
        :param validation_plugins: A list of plugins that be used to validate instances
            using the given schema. Each element should be an instance of a subclass of
            `linkml.validator.plugins.ValidationPlugin`. Defaults to None.
        """
        if isinstance(schema, Path):
            schema = str(schema)
        if isinstance(schema, SchemaDefinition):
            self._schema = schema
        else:
            self._schema: SchemaDefinition = yaml_loader.load(schema, SchemaDefinition)
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
        loader = PassthroughLoader(iter([instance]))
        yield from self.iter_results_from_source(loader, target_class)

    def iter_results_from_source(
        self, loader: Loader, target_class: Optional[str] = None
    ) -> Iterator[ValidationResult]:
        """Lazily yield validation results for the instances provided by a loader

        :param loader: An instance of a subclass of `linkml.validator.loaders.Loader`
            which provides the instances to validate
        :param target_class: Name of the class within the schema to validate
            against. If None, the class will be inferred from the schema by
            looked for a class with `tree_root: true`. Defaults to None.
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        if not self._validation_plugins:
            return []

        context = ValidationContext(self._schema, target_class)

        for plugin in self._validation_plugins:
            plugin.pre_process(context)

        for index, instance in enumerate(loader.iter_instances()):
            for plugin in self._validation_plugins:
                for result in plugin.process(instance, context):
                    result.instance_index = index
                    yield result

        for plugin in self._validation_plugins:
            plugin.post_process(context)
