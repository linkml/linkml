from dataclasses import fields
from typing import Optional

from linkml_runtime.utils.metamodelcore import Curie
from linkml_runtime.utils.yamlutils import YAMLRoot


class EnumDefinitionMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._addvals()

    def __getitem__(cls, item):
        # Walk the MRO so that empty wrapper subclasses (e.g. identifier
        # wrappers emitted by ``pythongen``) can inherit permissible values
        # from their parent enum class.
        for klass in cls.__mro__:
            if item in klass.__dict__:
                return klass.__dict__[item]
        raise KeyError(item)

    def __setitem__(cls, key, value):
        if key in cls.__dict__:
            raise ValueError(f"{cls.__name__} - {key} already assigned")
        cls.__dict__[key] = value

    def __contains__(cls, item) -> bool:
        # Accept strings, ``PermissibleValue`` instances, and ``EnumDefinitionImpl``
        # instances as membership tests against the class's permissible value names.
        # Walk the MRO so that empty wrapper subclasses inherit their parent
        # enum's permissible values.
        if isinstance_dt(item, "EnumDefinitionImpl"):
            code = getattr(item, "_code", None)
            if code is not None:
                item = code.text
        elif isinstance_dt(item, "PermissibleValue"):
            item = item.text
        return any(item in klass.__dict__ for klass in cls.__mro__)


def isinstance_dt(cls: type, inst: str) -> bool:
    """Duck typing isinstance to prevent recursion errors"""
    return inst in [c.__name__ for c in type(cls).mro()]


class EnumDefinitionImpl(YAMLRoot, metaclass=EnumDefinitionMeta):
    _defn: "EnumDefinition" = None  # Overridden by implementation

    def __init__(self, code: str | Curie) -> None:
        if isinstance_dt(code, "PermissibleValue"):
            key = code.text
        elif isinstance(code, Curie):
            key = str(code)
        else:
            key = code

        if key not in self.__class__ and self._defn.code_set:
            code = self._lookup(key)
            if code:
                self.__class__[key] = code
                self._code = code
        elif key not in self.__class__:
            raise ValueError(f"Unknown {self.__class__.__name__} enumeration code: {key}")
        elif isinstance_dt(code, "PermissibleValue"):
            if getattr(self, "code", None):
                if self._code != code:
                    raise ValueError(
                        f"Enumeration: {self.__class__.__name__} - "
                        f"Cannot change an existing permissible value entry for {code}"
                    )
            else:
                self._code = code
        else:
            self._code = self.__class__[key]

    def _lookup(self, key: str) -> Optional["PermissibleValue"]:
        """
        Hook to look up key in the appropriate code system
        @param key: URI or string in Curie form (TBD)
        @return: Permissible value rendering if key is valid
        """
        return None

    # WARNING: any non "_" prefix pollutes the EnumDefinition namespace.  These CAN be overridden, but be aware that
    # the value "code", "meaning" "uri", or "curie" as actual codes will mean that one will need to use "_code" and
    # direct access to get at the real values
    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, val):
        self._code = val

    @property
    def meaning(self):
        return self._code.meaning

    @property
    def uri(self):
        return self._code.meaning

    @property
    def curie(self):
        return "Curie for: " + self._code.meaning

    @classmethod
    def _addvals(cls):
        """Override this to add non-python compatible values"""
        pass

    def _as_value(self) -> str:
        """Return the primitive string representation for serialization.

        This is the canonical way for serializers (JSON, YAML) to convert
        an ``EnumDefinitionImpl`` into a plain string value suitable for
        output formats.  It simply returns the ``text`` of the underlying
        ``PermissibleValue``.
        """
        return self._code.text

    def __str__(self) -> str:
        """The string representation of an enumerated value should be the code representing this value."""
        return self._code.text

    def __repr__(self) -> str:
        rlist = [(f.name, getattr(self._code, f.name)) for f in fields(self._code)]
        return self.__class__.__name__ + "(" + ", ".join([f"{f[0]}={repr(f[1])}" for f in rlist if f[1]]) + ")"

    def __eq__(self, other) -> bool:
        """Equality against another enum instance, a ``PermissibleValue``, or a ``str``.

        Two enumerated values are considered equal when they share the same
        underlying permissible value text.  Comparison with a bare ``str`` (or
        ``PermissibleValue``) is supported so that user code can write
        ``MyEnum.A == "A"`` in the same way as stdlib ``StrEnum``.
        """
        if isinstance(other, EnumDefinitionImpl):
            return self._code.text == other._code.text
        if isinstance_dt(other, "PermissibleValue"):
            return self._code.text == other.text
        if isinstance(other, str):
            return self._code.text == other
        return NotImplemented

    def __ne__(self, other) -> bool:
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result

    def __hash__(self) -> int:
        return hash(self._code.text)


def _patch_permissible_value() -> None:
    """Temporary runtime back-fill for issue #1203 — to be removed once #723 lands.

    The metamodel's ``PermissibleValue`` is a generated ``@dataclass``. It lacks
    string-aware equality capability, is unhashable, and ``__str__`` is noisy.

    Since pythongen emits enum members as bare ``PermissibleValue`` class attrs,
    (``VitalStatus.ALIVE = PermissibleValue(text="ALIVE")``) instead of real
    ``EnumDefinitionImpl`` instances, user code that does ``p.status == "ALIVE"``,
    ``hash(VitalStatus.ALIVE)``, or ``VitalStatus.ALIVE in {...}`` would fail or
    behave non-intuitively.

    This function monkey-patches ``__eq__``, ``__ne__``, ``__hash__`` and ``__str__``
    onto ``PermissibleValue`` so those operations work idempotently for strings,
    other ``PermissibleValue`` instances, and ``EnumDefinitionImpl`` instances.

    .. deprecated::
        This patch is a temporary workaround, not the intended design.
        ``PermissibleValue`` is conceptually a clean metamodel descriptor and
        should retain that default dataclass equality semantics.

        The proper fix lives in pythongen + the runtime metaclass: enum
        members should be promoted to real ``EnumDefinitionImpl`` instances
        at class-creation time (see ``EnumDefinitionMeta``), at which point
        this patch will no longer be necessary.

    See also:
        * https://github.com/linkml/linkml/issues/1203 (the bug patch addresses)
        * https://github.com/linkml/linkml/issues/723  (the structural fix)
        * https://github.com/linkml/linkml/pull/3596   (tracking PR)
    """
    from linkml_runtime.linkml_model.meta import PermissibleValue

    if getattr(PermissibleValue, "_linkml_enum_patches_applied", False):
        return

    def _pv_eq(self, other) -> bool:
        if isinstance(other, EnumDefinitionImpl):
            code = getattr(other, "_code", None)
            return code is not None and self.text == code.text
        if isinstance(other, PermissibleValue):
            return self.text == other.text
        if isinstance(other, str):
            return self.text == other
        return NotImplemented

    def _pv_ne(self, other) -> bool:
        result = _pv_eq(self, other)
        if result is NotImplemented:
            return result
        return not result

    def _pv_hash(self) -> int:
        return hash(self.text)

    def _pv_str(self) -> str:
        return str(self.text)

    PermissibleValue.__eq__ = _pv_eq
    PermissibleValue.__ne__ = _pv_ne
    PermissibleValue.__hash__ = _pv_hash
    PermissibleValue.__str__ = _pv_str
    PermissibleValue._linkml_enum_patches_applied = True
