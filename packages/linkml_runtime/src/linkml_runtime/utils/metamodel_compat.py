"""
Compatibility helpers for code that must work with both metamodel flavors:
the dataclass metamodel (:mod:`linkml_runtime.linkml_model.meta`) and the
provisional pydantic metamodel (:mod:`linkml_runtime.linkml_model.pydantic`).

The pydantic flavor is only considered when its module has already been
imported (e.g. by constructing a ``SchemaView`` with ``metamodel="pydantic"``
or by passing a pydantic ``SchemaDefinition``), so dataclass-only consumers
never pay the import cost of the pydantic metamodel.
"""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from types import ModuleType
from typing import Any, Literal

MetamodelFlavor = Literal["dataclass", "pydantic"]

_PYDANTIC_META_MODULE = "linkml_runtime.linkml_model.pydantic.meta"


@lru_cache(maxsize=None)
def metamodel_module(flavor: MetamodelFlavor = "dataclass") -> ModuleType:
    """Return the module providing the metamodel classes for the given flavor.

    >>> metamodel_module("dataclass").SlotDefinition(name="s").name
    's'
    """
    if flavor == "pydantic":
        import linkml_runtime.linkml_model.pydantic.meta as module
    elif flavor == "dataclass":
        import linkml_runtime.linkml_model.meta as module
    else:
        msg = f"Unknown metamodel flavor: {flavor}"
        raise ValueError(msg)
    return module


def flavor_of(element: Any) -> MetamodelFlavor:
    """Return the metamodel flavor of a schema or element instance.

    >>> from linkml_runtime.linkml_model.meta import SlotDefinition
    >>> flavor_of(SlotDefinition("s"))
    'dataclass'
    """
    from pydantic import BaseModel

    return "pydantic" if isinstance(element, BaseModel) else "dataclass"


def _available_flavors() -> tuple[MetamodelFlavor, ...]:
    """Flavors whose metamodel modules are currently imported."""
    if _PYDANTIC_META_MODULE in sys.modules:
        return ("dataclass", "pydantic")
    return ("dataclass",)


@lru_cache(maxsize=None)
def _types_for(flavors: tuple[MetamodelFlavor, ...], class_names: tuple[str, ...]) -> tuple[type, ...]:
    return tuple(getattr(metamodel_module(flavor), name) for flavor in flavors for name in class_names)


def metamodel_types(*class_names: str) -> tuple[type, ...]:
    """Return the named metamodel classes from every available flavor.

    Use in place of a direct ``isinstance`` check against dataclass metamodel
    types, so the check also recognizes pydantic metamodel instances:

    >>> from linkml_runtime.linkml_model.meta import ClassDefinition
    >>> isinstance(ClassDefinition("C"), metamodel_types("ClassDefinition"))
    True
    """
    return _types_for(_available_flavors(), class_names)


def element_type_name(element: Any) -> str:
    """Return the metamodel type name of an element, e.g. ``class_definition``.

    The dataclass metamodel carries this as the ``class_name`` ClassVar; for
    pydantic models it is derived from the python class name.

    >>> from linkml_runtime.linkml_model.meta import ClassDefinition
    >>> element_type_name(ClassDefinition("C"))
    'class_definition'
    """
    class_name = getattr(type(element), "class_name", None)
    if isinstance(class_name, str):
        return class_name
    return re.sub(r"(?<!^)(?=[A-Z])", "_", type(element).__name__).lower()
