"""Build result classes for Golang generator."""

from pathlib import Path
from typing import TypeVar

from linkml.generators.common.build import (
    BuildResult,
    SchemaResult,
)
from linkml.generators.common.build import (
    ClassResult as ClassResult_,
)
from linkml.generators.common.build import (
    SlotResult as SlotResult_,
)
from linkml.generators.golanggen.template import GolangField, GolangStruct, Import, Imports

T = TypeVar("T", bound="GolangBuildResult", covariant=True)


class GolangBuildResult(BuildResult):
    """
    BuildResult parent class for golang generator
    """

    imports: list[Import] | Imports | None = None

    def merge(self, other: T) -> T:
        """
        Merge a build result with another.

        - Merges imports with :meth:`.Imports.__add__`

        Args:
            other (:class:`.GolangBuildResult`): A subclass of GolangBuildResult

        Returns:
            :class:`.GolangBuildResult`
        """
        self_copy = self.model_copy()
        if other.imports:
            if self.imports is not None:
                self_copy.imports += other.imports
            else:
                self_copy.imports = other.imports
        return self_copy


class FieldResult(GolangBuildResult, SlotResult_):
    """Result of building a struct field"""

    field: GolangField


class StructResult(GolangBuildResult, ClassResult_):
    """Result of building a struct"""

    struct: GolangStruct


class SplitResult(SchemaResult):
    """Build result when generating with split mode"""

    main: bool = False
    path: Path
    serialized_module: str
    module_import: str | None = None
