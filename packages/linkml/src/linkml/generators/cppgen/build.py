"""Build result classes for C++ generator."""

from typing import TypeVar

from linkml.generators.common.build import BuildResult
from linkml.generators.common.build import ClassResult as ClassResult_
from linkml.generators.common.build import SlotResult as SlotResult_
from linkml.generators.cppgen.template import CppField, CppInclude, CppStruct, Includes

T = TypeVar("T", bound="CppBuildResult", covariant=True)


class CppBuildResult(BuildResult):
    """BuildResult parent class for C++ generator."""

    includes: list[CppInclude] | Includes | None = None

    def merge(self, other: T) -> T:
        """Merge a build result with another, combining includes."""
        self_copy = self.model_copy()
        if other.includes:
            if self.includes is not None:
                self_copy.includes += other.includes
            else:
                self_copy.includes = other.includes
        return self_copy


class FieldResult(CppBuildResult, SlotResult_):
    """Result of building a struct field."""

    field: CppField


class StructResult(CppBuildResult, ClassResult_):
    """Result of building a struct."""

    struct: CppStruct
