from dataclasses import dataclass
from typing import Set, cast

from linkml_runtime.linkml_model.meta import (ClassDefinitionName, ElementName,
                                              EnumDefinitionName,
                                              SlotDefinitionName,
                                              SubsetDefinitionName,
                                              TypeDefinitionName)
from linkml_runtime.utils.metamodelcore import empty_set


@dataclass(repr=False, frozen=True)
class RefType:
    name: str

    def __repr__(self):
        return self.name


ClassType = RefType("Class")
TypeType = RefType("Type")
SlotType = RefType("Slot")
SubsetType = RefType("Subset")
EnumType = RefType("Enum")


@dataclass
class References:
    """
    Summary of references to a given class. The reference class is the key to the dictionary carrying classrefs
    """

    classrefs: Set[ClassDefinitionName] = empty_set()  # Refs of type class
    slotrefs: Set[SlotDefinitionName] = empty_set()  # Refs of type slot
    typerefs: Set[TypeDefinitionName] = empty_set()  # Refs of type type
    subsetrefs: Set[SubsetDefinitionName] = empty_set()  # Refs of type subset
    enumrefs: Set[EnumDefinitionName] = empty_set()  # Refs of type enum

    def addref(self, fromtype: RefType, fromname: ElementName) -> None:
        if fromtype is ClassType:
            self.classrefs.add(ClassDefinitionName(fromname))
        elif fromtype is TypeType:
            self.typerefs.add(TypeDefinitionName(fromname))
        elif fromtype is SlotType:
            self.slotrefs.add(SlotDefinitionName(fromname))
        elif fromtype is SubsetType:
            self.subsetrefs.add(SubsetDefinitionName(fromname))
        elif fromtype is EnumType:
            self.slotrefs.add(EnumDefinitionName(fromname))
        else:
            raise TypeError(f"Unknown typ: {fromtype}")

    def update(self, other: "References") -> None:
        self.classrefs.update(other.classrefs)
        self.slotrefs.update(other.slotrefs)
        self.typerefs.update(other.typerefs)
        self.subsetrefs.union(other.subsetrefs)
        self.enumrefs.update(other.enumrefs)

    def __bool__(self):
        return (
            bool(self.classrefs)
            or bool(self.slotrefs)
            or bool(self.typerefs)
            or bool(self.subsetrefs)
            or bool(self.enumrefs)
        )
