from dataclasses import fields
from typing import Optional

from linkml_runtime.utils.metamodelcore import Curie
from linkml_runtime.utils.yamlutils import YAMLRoot


class EnumDefinitionMeta(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._addvals()
        cls._promote_permissible_values()

    def _promote_permissible_values(cls) -> None:
        """Replace bare ``PermissibleValue`` class attributes with real enum instances.

        So ``pythongen`` emits each enum member as a plain ``PermissibleValue``
        class attribute, e.g. ``ALIVE = PermissibleValue(text="ALIVE")``.  On
        its own that leaves ``MyEnum.ALIVE`` as a raw metamodel object rather
        than a member of the enum (https://github.com/linkml/linkml/issues/723).

        This method runs once per class at metaclass ``__init__`` time.  For
        each such attribute it calls the enum constructor (``cls(pv)``) and
        rebinds the name to the result, so ``MyEnum.ALIVE`` becomes an
        ``EnumDefinitionImpl`` instance ("promotion").

        Two cases are handled implicitly ("no permissible values"):

        * ``EnumDefinitionImpl`` base class has ``_defn = None`` and is skipped.
        * Identifier-wrapper subclasses (``class Wrapper(Parent): pass``) is
          no-op. Lookups fall through the MRO to the parent's promoted instances.
        """
        if getattr(cls, "_defn", None) is None:
            return
        # Lazy import: ``linkml_runtime.linkml_model.meta`` depends on this
        # module via ``EnumDefinitionImpl`` so the top-level import would be
        # circular.
        from linkml_runtime.linkml_model.meta import PermissibleValue

        for name, attr in list(cls.__dict__.items()):
            if isinstance(attr, PermissibleValue):
                type.__setattr__(cls, name, cls(attr))

    def __getitem__(cls, item):
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
            val = self.__class__[key]
            # After promotion the class attribute is an ``EnumDefinitionImpl``;
            # unwrap to its underlying ``PermissibleValue`` so ``self._code``
            # always stores a PV.
            if isinstance_dt(val, "EnumDefinitionImpl"):
                self._code = val._code
            else:
                self._code = val

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
    def text(self):
        """The permissible-value text (canonical short code)."""
        return self._code.text

    @property
    def description(self):
        return self._code.description

    @property
    def title(self):
        return self._code.title

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
