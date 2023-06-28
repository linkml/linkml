from abc import ABC, abstractmethod
from typing import Any, Dict
from linkml.validator.models import ValidationReport


class BasePlugin(ABC):
    """
    Base plugin class that all validation plugins should inherit from.
    """

    NAME = "BasePlugin"

    def __init__(self, schema: str, **kwargs) -> None:
        """
        Initialize the plugin with the given schema YAML.

        Args:
            schema: Path or URL to schema YAML
            kwargs: Additional arguments that are used to instantiate the plugin

        """
        self.schema = schema

    @abstractmethod
    def process(self, obj: Dict, **kwargs) -> ValidationReport:
        """
        Run one or more operations on the given object and return
        a validation report.

        Args:
            obj: The object to process
            kwargs: Additional arguments that are used for processing

        """
        ...