from linkml.generators.common.build import (
    BuildResult,
    SchemaResult,
)
from linkml.generators.common.build import (
    ClassResult as ClassResult_,
)
from linkml.generators.common.build import EnumResult as EnumResult_
from linkml.generators.common.build import (
    SlotResult as SlotResult_,
)
from linkml.generators.rustgen.template import (
    Imports,
    RustCargo,
    RustEnum,
    RustFile,
    RustProperty,
    RustPyProject,
    RustStruct,
    RustTypeAlias,
)


class RustBuildResult(BuildResult):
    """
    BuildResult parent class for rustgen
    """

    imports: Imports = Imports()

    def merge(self, other: "RustBuildResult") -> "RustBuildResult":
        self.imports += other.imports
        return self


class ClassResult(RustBuildResult, ClassResult_):
    """
    A single built rust struct
    """

    cls: RustStruct


class SlotResult(RustBuildResult, SlotResult_):
    """
    A type alias
    """

    slot: RustTypeAlias


class AttributeResult(RustBuildResult, SlotResult_):
    """
    A field within a rust struct
    """

    attribute: RustProperty


class EnumResult(RustBuildResult, EnumResult_):
    """
    A rust enum!
    """

    enum: RustEnum


class CrateResult(RustBuildResult, SchemaResult):
    """
    A schema built into a rust crate
    """

    cargo: RustCargo
    file: RustFile
    pyproject: RustPyProject


class FileResult(RustBuildResult, SchemaResult):
    """
    A schema built into a single rust file
    """

    file: RustFile