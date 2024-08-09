"""
Create linkml classes from dataclasses.

.. note::
    These linkml classes are strictly "best effort" and do not fully capture
    the full details of a source schema that was used to generate dataclasses with the
    :class:`linkml.generators.PythonGenerator` class.

"""

from collections.abc import Iterable
from dataclasses import MISSING, dataclass, field, fields
from datetime import datetime
from typing import Any, Literal, Type, Union

from linkml_runtime.linkml_model import ClassDefinition, SlotDefinition
from linkml_runtime.linkml_model.meta import AnonymousSlotExpression

python_to_linkml = {
    str: "string",
    int: "integer",
    float: "float",
    bool: "boolean",
    datetime: "datetime",
}


def _is_optional(t: Any) -> bool:
    return getattr(t, "__origin__") is Union and len(t.__args__) == 2 and t.__args__[1] is None


def _strip_optional(t: Any) -> list[Type] | Type:
    if hasattr(t, "__args__"):
        args = [a_type for a_type in t.__args__ if a_type is not None]
        if len(args) == 1:
            return args[0]
        return args
    return t


@dataclass
class DataclassInverter:

    source: Type[dataclass]
    """The dataclass we are inverting"""
    exclude_attributes: Iterable[str] = field(default_factory=list)
    """Attributes that should not be generated for the dataclass"""
    exclude_private: bool = True
    """Exclude private attributes"""

    def ifabsent(self, f: field) -> str | None:
        if f.default is None:
            return None
        elif isinstance(f.default, bool):
            return f"boolean({f.default})"
        elif isinstance(f.default, str):
            return f"string({f.default})"
        elif isinstance(f.default, int):
            return f"integer({f.default})"
        elif isinstance(f.default, float):
            return f"float({f.default})"
        else:
            return None

    def range_or_any_of(
        self, typ: Type
    ) -> dict[Literal["range"], str] | dict[Literal["any_of"], list[AnonymousSlotExpression]]:
        if getattr(typ, "__origin__", None) is Union:
            if _is_optional(typ):
                typ = _strip_optional(typ)
            else:
                # remove optionals
                typ = _strip_optional(typ)
                if len(typ) == 1:
                    typ = typ[0]
                else:
                    any_ofs = [self.range_or_any_of(t) for t in typ]
                    # remove duplicates
                    return {"any_of": [AnonymousSlotExpression(**dict(t)) for t in {tuple(d.items()) for d in any_ofs}]}

        return {"range": python_to_linkml.get(typ, "linkml:Any")}

    def required(self, f: field) -> bool:
        return f.default is MISSING and f.default_factory is MISSING

    def multivalued(self, f: field) -> bool:
        args = _strip_optional(f.type)
        # strip optional returns a literal list, but isinstance(list[type], Iterable) still is True
        return (isinstance(args, Iterable) and not isinstance(args, list)) or (
            isinstance(args, list) and all([isinstance(a, Iterable) for a in args])
        )

    def is_excluded(self, name: str) -> bool:
        """
        True if a slot name is excluded from the generated class
        """
        return name in self.exclude_attributes or (name.startswith("_") and self.exclude_private)

    def render(self) -> ClassDefinition:
        return ClassDefinition(
            name=self.source.__name__,
            description=self.source.__doc__,
            attributes={
                f.name: SlotDefinition(
                    name=f.name,
                    multivalued=self.multivalued(f),
                    ifabsent=self.ifabsent(f),
                    required=self.required(f),
                    **self.range_or_any_of(f.type),
                )
                for f in fields(self.source)
                if not self.is_excluded(f.name)
            },
        )
