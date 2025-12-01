from enum import Enum
from typing import ClassVar, Optional

from jinja2 import Environment, PackageLoader
from linkml_runtime.utils.formatutils import uncamelcase, underscore
from pydantic import BaseModel, Field, computed_field, field_validator

from linkml.generators.common.template import Import as Import_
from linkml.generators.common.template import Imports as Imports_
from linkml.generators.common.template import TemplateModel, _render


class ContainerType(Enum):
    LIST = "list"
    MAPPING = "mapping"


class RustRange(BaseModel):
    optional: bool = False
    containerType: Optional[ContainerType] = None
    has_default: bool = False
    is_class_range: bool = False
    is_reference: bool = False
    box_needed: bool = False
    has_class_subtypes: bool = False
    child_ranges: Optional[list["RustRange"]] = None
    type_: str

    def type_name(self) -> str:
        """
        Canonical Rust type name (no module path).

        Centralizes how we derive a display/type identifier for variants,
        avoiding ad-hoc string splitting in templates or other models.
        """
        # For references, range.type_ is already "String" in current generator,
        # but keep behavior robust even if callers pass a namespaced path.
        t = self.type_
        # Trim any module path qualifiers like crate::mod::Type
        if "::" in t:
            t = t.split("::")[-1]
        return t

    def is_copy(self) -> bool:
        """Return True when values of this range implement Rust's Copy.

        Used to decide whether scalar getters can return by value or must
        borrow. The set is intentionally conservative and limited to common
        numeric and boolean primitives.
        """
        return self.type_ in ["i8", "i16", "i32", "i64", "u8", "u16", "u32", "u64", "f32", "f64", "bool", "isize"]

    def type_for_field(self):
        """Concrete Rust type to store in a struct field.

        Applies structural adjustments in this order:
        - Promote class types with subtypes to `OrSubtype` (unless references).
        - Box inlined class values when needed to break recursive ownership.
        - Wrap in `Vec<>` or `HashMap<String, _>` for list/map slots.
        - Wrap in `Option<>` when the slot is optional.
        """
        tp = self.type_
        if self.has_class_subtypes:
            if not self.is_reference:
                tp = f"{tp}OrSubtype"
        if self.box_needed:
            tp = f"Box<{tp}>"
        if self.containerType == ContainerType.LIST:
            tp = f"Vec<{tp}>"
        elif self.containerType == ContainerType.MAPPING:
            tp = f"HashMap<String, {tp}>"
        if self.optional:
            tp = f"Option<{tp}>"
        return tp

    def type_without_option(self) -> str:
        """Field type without the outer Option wrapper."""

        tp = self.type_for_field()
        if self.optional and tp.startswith("Option<") and tp.endswith(">"):
            return tp[7:-1]
        return tp

    def type_for_constructor(self) -> str:
        """Parameter type for struct constructors (PyO3 new).

        Class ranges accept a serde-backed adapter that can deserialize
        dictionaries or reuse existing pyclass instances. Other ranges
        keep their field types unchanged.
        """

        if self.is_class_range and not self.is_reference:
            inner = self.type_without_option()
            wrapped = f"serde_utils::PyValue<{inner}>"
            if self.optional:
                return f"Option<{wrapped}>"
            return wrapped
        return self.type_for_field()

    def needs_constructor_conversion(self) -> bool:
        """True when constructor arguments need post-processing."""

        return self.is_class_range and not self.is_reference

    def convert_constructor_value(self, var_name: str) -> str:
        """Expression to convert constructor argument into field value."""

        if not self.needs_constructor_conversion():
            return var_name
        if self.optional:
            return f"{var_name}.map(|v| v.into_inner())"
        return f"{var_name}.into_inner()"

    def type_for_trait(self, crateref: Optional[str], setter: bool = False):
        """Signature type for trait getters/setters over this range.

        - For getters (setter=False):
          - Lists/Maps return borrowed views (`SeqRef`/`MapRef`) with explicit lifetimes.
          - Scalars borrow `&T` for non-Copy values; Copy values return by value.
          - Class types without subtypes are prefixed with `crate::` for stability;
            with subtypes, use `OrSubtype`.
          - Optional scalars collapse to `Option<&str>` for strings and borrow for others.
        - For setters (setter=True):
          - Lists/Maps accept `&Vec<_>`/`&HashMap<_, _>`.
          - Class scalars accept a generic `E` with `Into<T>` bound (computed separately).
        """
        tp = self.type_
        if self.is_class_range and not self.has_class_subtypes and not setter:
            if crateref and not self.is_reference:
                tp = f"{crateref}::{tp}"
        if self.has_class_subtypes and not self.is_reference:
            tp = f"{tp}OrSubtype"
        if self.is_class_range and setter and not self.is_reference:
            tp = "E"
        convert_ref = False
        if self.containerType == ContainerType.LIST:
            if not setter:
                # tp = f"poly_containers::ListView<{tp}>"
                tp = f"impl poly_containers::SeqRef<'a, {tp}>"
            else:
                tp = f"&Vec<{tp}>"
        elif self.containerType == ContainerType.MAPPING:
            if not setter:
                tp = f"impl poly_containers::MapRef<'a, String,{tp}>"
            else:
                tp = f"&HashMap<String, {tp}>"
        else:
            if not self.is_copy():
                convert_ref = True
        if not setter and convert_ref and (not self.optional or (self.is_class_range and not self.is_reference)):
            tp = f"&'a {tp}"
        if self.optional:
            if self.containerType or (self.is_class_range and not self.is_reference):
                tp = f"Option<{tp}>"
            else:
                if tp == "String":
                    tp = "Option<&'a str>"
                else:
                    if self.is_copy():
                        tp = f"Option<{tp}>"
                    else:
                        tp = f"Option<&'a {tp}>"
        if tp == "&'a String":
            tp = "&'a str"
        return tp

    def type_for_trait_value(self, crateref: Optional[str]) -> str:
        """By-value getter type for trait methods.

        Used when the trait returns a canonical union or otherwise needs owned
        values. Containers become `Vec<_>`/`HashMap<_, _>`. For class scalars,
        add `crate::` unless the range admits subtypes (then use `OrSubtype`).
        """
        # Union type: already canonical
        if self.child_ranges is not None and len(self.child_ranges) > 1:
            tp = self.type_
        else:
            tp = self.type_
            if self.is_class_range and not self.is_reference:
                if self.has_class_subtypes:
                    tp = f"{tp}OrSubtype"
                elif crateref:
                    tp = f"{crateref}::{tp}"
        if self.containerType == ContainerType.LIST:
            tp = f"Vec<{tp}>"
        elif self.containerType == ContainerType.MAPPING:
            tp = f"HashMap<String, {tp}>"
        if self.optional:
            tp = f"Option<{tp}>"
        return tp

    def type_bound_for_setter(self, crateref: Optional[str]) -> Optional[str]:
        """Generic bound to accept convertible values in setter signatures.

        For class ranges, setters use a type parameter `E` constrained as
        `Into<T>` to allow ergonomic conversions. Non-class ranges do not
        require a bound and return None.
        """
        if self.is_class_range:
            tp = self.type_
            return f"Into<{tp}>"
        return None


class RustTemplateModel(TemplateModel):
    """
    Parent class for rust template models :)
    """

    template: ClassVar[str]
    _environment: ClassVar[Environment] = Environment(
        loader=PackageLoader("linkml.generators.rustgen", "templates"), trim_blocks=True, lstrip_blocks=True
    )
    meta_exclude: ClassVar[list[str]] = None

    pyo3: bool = True
    """
    Whether pyO3 annotations should be added to generated items :)
    """
    serde: bool = False
    """
    Whether serde serialization/deserialization annotations should be added.
    """
    stubgen: bool = False
    """
    Whether pyo3-stub-gen instrumentation should be emitted.
    """
    handwritten_lib: bool = False
    """Place generated sources under src/generated and leave lib.rs untouched for user code."""
    attributes: dict[str, str] = Field(default_factory=dict)


class RustTypeViews(BaseModel):
    """Precomputed trait signature fragments for a slot's range.

    Encapsulates the decisions around by-value vs borrowed returns, container
    view types, optional wrapping, and whether explicit lifetimes are required
    in the generated method signature. Templates consume these strings directly
    to avoid branching on typing details.
    """

    type_getter: str
    needs_lifetime: bool


def _needs_lifetime(sig: str) -> bool:
    """Heuristic to detect if a signature string requires an explicit lifetime.

    We consider borrowed types (`&T`), container views (`SeqRef`/`MapRef`), and
    explicit generics (`<'a>`) as requiring a lifetime parameter on the method.
    """
    return ("&" in sig) or ("SeqRef" in sig) or ("MapRef" in sig) or ("<'a>" in sig)


def build_trait_views_for_promoted(promoted: "RustRange") -> RustTypeViews:
    """Return signature strings for a trait using the promoted (max) range.

    - Raw getter: by-value for unions; otherwise borrowed/container view types.
    - Typed getter: by-value for unions; otherwise borrowed/container view types
      with `SeqRef`/`MapRef` and optional wrapping.
    The goal is consistency across a class hierarchy regardless of concrete fields.
    """
    # Raw getter: by-value union if union; else borrowed/containers
    if promoted.child_ranges is not None and len(promoted.child_ranges) > 1:
        raw = promoted.type_for_trait_value(crateref="crate")
    else:
        raw = promoted.type_for_trait(setter=False, crateref="crate")

    return RustTypeViews(
        type_getter=raw,
        needs_lifetime=_needs_lifetime(raw),
    )


def build_trait_views_for_range(rng: "RustRange") -> RustTypeViews:
    """Return signature strings for a concrete (non-promoted) range.

    Mirrors the promoted logic but based on the actual field's range, used in
    impls so that borrow vs value and container view decisions match the trait.
    """
    # Raw getter
    if rng.child_ranges is not None and len(rng.child_ranges) > 1:
        raw = rng.type_for_trait_value(crateref="crate")
    else:
        raw = rng.type_for_trait(setter=False, crateref="crate")

    return RustTypeViews(
        type_getter=raw,
        needs_lifetime=_needs_lifetime(raw),
    )


class PolyContainersFile(RustTemplateModel):
    template: ClassVar[str] = "poly_containers.rs.jinja"


class Import(Import_, RustTemplateModel):
    template: ClassVar[str] = "import.rs.jinja"

    version: Optional[str] = None
    """Version specifier to use in Cargo.toml"""
    features: Optional[list[str]] = None
    """Features to require in Cargo.toml"""
    ## whether this import should be behind a feature flag
    feature_flag: Optional[str] = None
    feature_dependencies: list[str] = Field(default_factory=list)
    """Additional crate features to enable alongside the optional dependency."""


class Imports(Imports_, RustTemplateModel):
    template: ClassVar[str] = "imports.rs.jinja"


class RustProperty(RustTemplateModel):
    """
    A property within a rust struct
    """

    template: ClassVar[str] = "property.rs.jinja"
    inline_mode: str
    alias: Optional[str] = None
    generate_merge: bool = False
    container_mode: str
    name: str
    type_: RustRange  # might be a union type, so list length > 1
    required: bool
    multivalued: bool = False
    is_key_value: bool = False

    @computed_field
    def optional(self) -> bool:
        """
        Whether this property is optional
        """
        return self.type_.optional

    @computed_field
    def merge_strategy(self) -> str:
        if self.type_.optional:
            return "strategy = overwrite_except_none"
        elif self.type_.containerType == ContainerType.LIST:
            return "skip"
        elif self.type_.containerType == ContainerType.MAPPING:
            return "strategy = merge::hashmap::overwrite"
        else:
            return "skip"

    @computed_field
    def type_for_field(self) -> str:
        """
        The type of this field, as it would be used in a struct definition
        """
        return self.type_.type_for_field()

    @computed_field
    def hasdefault(self) -> bool:
        return self.multivalued or not self.required


class AsKeyValue(RustTemplateModel):
    """
    A key-value representation for this struct
    """

    template: ClassVar[str] = "as_key_value.rs.jinja"
    name: str
    key_property_name: str
    key_property_type: str
    value_property_name: str
    value_property_type: str
    can_convert_from_primitive: bool = False
    can_convert_from_empty: bool = False
    value_property_optional: bool = False


class RustStructOrSubtypeEnum(RustTemplateModel):
    template: ClassVar[str] = "struct_or_subtype_enum.rs.jinja"
    enum_name: str
    struct_names: list[str]
    as_key_value: bool = False
    type_designator_field: Optional[str] = None
    type_designators: dict[str, str]
    key_property_type: str = "String"


class SlotRangeAsUnion(RustTemplateModel):
    """
    A union of ranges!
    """

    template: ClassVar[str] = "slot_range_as_union.rs.jinja"
    slot_name: str
    ranges: list[str]


class RustClassModule(RustTemplateModel):
    class_name: str
    class_name_snakecase: str
    template: ClassVar[str] = "class_module.rs.jinja"
    slot_ranges: list[SlotRangeAsUnion]


class RustStruct(RustTemplateModel):
    """
    A struct!
    """

    template: ClassVar[str] = "struct.rs.jinja"
    special_case_enabled: bool = False
    class_module: Optional[RustClassModule] = None

    name: str
    bases: Optional[list[str]] = None
    """
    Base classes to inherit from - must have entire MRO, just just immediate ancestor
    """
    properties: list[RustProperty] = Field(default_factory=list)
    unsendable: bool = False
    generate_merge: bool = False
    as_key_value: Optional[AsKeyValue] = None
    struct_or_subtype_enum: Optional[RustStructOrSubtypeEnum] = None

    @computed_field()
    def property_names_and_types(self) -> dict[str, str]:
        return [(p.name, p.type_.type_for_constructor()) for p in self.constructor_params]

    @computed_field()
    def property_names(self) -> list[str]:
        return [p.name for p in self.properties]

    @computed_field()
    def constructor_params(self) -> list[RustProperty]:
        required = [p for p in self.properties if not p.type_.optional]
        optional = [p for p in self.properties if p.type_.optional]
        return required + optional

    @computed_field()
    def constructor_signature(self) -> str:
        parts: list[str] = []
        for prop in self.constructor_params:
            if prop.type_.optional:
                parts.append(f"{prop.name}=None")
            else:
                parts.append(prop.name)
        return ", ".join(parts)

    @computed_field()
    def constructor_conversions(self) -> list[tuple[str, str]]:
        return [
            (p.name, p.type_.convert_constructor_value(p.name))
            for p in self.constructor_params
            if p.type_.needs_constructor_conversion()
        ]


class RustEnum(RustTemplateModel):
    """
    A rust enum!
    """

    template: ClassVar[str] = "enum.rs.jinja"

    name: str
    items: list["RustEnumItem"]


class RustEnumItem(BaseModel):
    """Single enum variant with its original permissible value text."""

    variant: str
    text: str

    @computed_field
    def python_literals(self) -> list[str]:
        """Return acceptable string literals when converting from Python."""

        literals = [self.text]
        if self.variant != self.text:
            literals.append(self.variant)
        return literals

    @staticmethod
    def _escape(value: str) -> str:
        return value.replace("\\", "\\\\").replace('"', '\\"')

    @computed_field
    def text_literal(self) -> str:
        """Escaped literal suitable for embedding in Rust source."""

        return self._escape(self.text)

    @computed_field
    def python_match_pattern(self) -> str:
        """Match arm pattern accepting any permitted Python literal."""

        literals = []
        for literal in self.python_literals:
            if literal not in literals:
                literals.append(literal)
        escaped = [f'"{self._escape(lit)}"' for lit in literals]
        return " | ".join(escaped)


class RustTypeAlias(RustTemplateModel):
    """
    A type alias used to represent slots
    """

    template: ClassVar[str] = "typealias.rs.jinja"

    name: str
    type_: str
    description: Optional[str] = None
    multivalued: Optional[bool] = False
    class_range: bool = False
    slot_range_as_union: Optional[SlotRangeAsUnion] = None

    @field_validator("attributes", mode="before")
    @classmethod
    def attr_values_as_strings(cls, value: dict[str, any]) -> dict[str, str]:
        return {k: str(v) for k, v in value.items()}


class SerdeUtilsFile(RustTemplateModel):
    """
    A file containing utility functions for serde serialization/deserialization
    """

    template: ClassVar[str] = "serde_utils.rs.jinja"


class StubUtilsFile(RustTemplateModel):
    """Helper utilities shared by stub generation code."""

    template: ClassVar[str] = "stub_utils.rs.jinja"


class StubGenBin(RustTemplateModel):
    """Binary entry point to orchestrate stub generation checks."""

    template: ClassVar[str] = "stub_gen.rs.jinja"
    crate_name: str
    stubgen: bool

    @computed_field
    def crate_module(self) -> str:
        """Crate identifier usable in Rust source."""

        return self.crate_name.replace("-", "_")


class PolyTraitProperty(RustTemplateModel):
    template: ClassVar[str] = "poly_trait_property.rs.jinja"
    name: str
    range: RustRange
    promoted_range: RustRange
    promoted_range: RustRange

    @computed_field
    def class_range(self) -> bool:
        """
        Whether this range is a class range
        """
        return self.range.is_class_range

    @computed_field
    def type_getter(self) -> str:
        # Centralized via RustTypeViews builder
        views = build_trait_views_for_promoted(self.promoted_range)
        return views.type_getter

    @computed_field
    def needs_lifetime(self) -> bool:
        """Whether the trait getter requires an explicit lifetime."""
        views = build_trait_views_for_promoted(self.promoted_range)
        return views.needs_lifetime

    @computed_field
    def type_setter(self) -> str:
        return self.range.type_for_trait(setter=True, crateref="crate")

    @computed_field
    def type_bound(self) -> Optional[str]:
        """
        The type bound for the setter method
        """
        return self.range.type_bound_for_setter(crateref="crate")


class PolyTraitPropertyImpl(RustTemplateModel):
    template: ClassVar[str] = "poly_trait_property_impl.rs.jinja"
    name: str
    range: RustRange
    struct_name: str
    definition_range: RustRange
    trait_range: RustRange

    @computed_field
    def is_copy(self) -> bool:
        """
        Whether this range is a copy type
        """
        return self.range.is_copy()

    @computed_field
    def need_option_wrap(self) -> bool:
        return self.definition_range.optional and not self.range.optional

    @computed_field
    def class_range(self) -> bool:
        """
        Whether this range is a class range
        """
        return self.range.is_class_range

    @computed_field
    def ct(self) -> str:
        """
        The container type for this range, if any
        """
        return self.range.containerType.value if self.range.containerType else "None"

    @computed_field
    def type_getter(self) -> str:
        # Mirror trait signature: promoted union by value; else concrete borrowed
        if self.definition_range.child_ranges is not None and len(self.definition_range.child_ranges) > 1:
            return build_trait_views_for_promoted(self.definition_range).type_getter
        return build_trait_views_for_range(self.trait_range).type_getter

    @computed_field
    def needs_lifetime(self) -> bool:
        sig = self.type_getter
        return ("&" in sig) or ("SeqRef" in sig) or ("MapRef" in sig)

    # Note: typed getters removed

    @computed_field
    def union_type(self) -> str:
        return self.definition_range.type_

    @computed_field
    def range_variant(self) -> str:
        # Use centralized type-name logic for a variant identifier
        return self.range.type_name()

    @computed_field
    def current_union_types(self) -> dict[str, str]:
        m: dict[str, str] = {}
        for c in self.cases:
            sc = underscore(uncamelcase(c))
            m[c] = f"{sc}_utl::{self.name}_range"
        return m

    @computed_field
    def base_union_variants(self) -> list[str]:
        vs: list[str] = []
        if self.definition_range.child_ranges is not None and len(self.definition_range.child_ranges) > 1:
            for cr in self.definition_range.child_ranges:
                vs.append(cr.type_name())
        return vs

    @computed_field
    def current_union_type(self) -> str:
        return self.range.type_

    @computed_field
    def type_setter(self) -> str:
        return self.definition_range.type_for_trait(setter=True, crateref="crate")

    @computed_field
    def type_bound(self) -> Optional[str]:
        """
        The type bound for the setter method
        """
        return self.definition_range.type_bound_for_setter(crateref="crate")

    @computed_field
    def union_conversion_arms(self) -> list[str]:
        """Pre-rendered match arms to convert current union -> base union.

        Example: Current::A(x) => Base::A(x.clone()),
        """
        arms: list[str] = []
        if self.definition_range.child_ranges is not None and len(self.definition_range.child_ranges) > 1:
            base = self.union_type
            cur = self.current_union_type
            for vn in self.base_union_variants:
                arms.append(f"{cur}::{vn}(x) => {base}::{vn}(x.clone()),")
        return arms


class PolyTraitImpl(RustTemplateModel):
    """Implementation of a :class:`PolyTrait` for a particular struct."""

    template: ClassVar[str] = "poly_trait_impl.rs.jinja"
    name: str
    struct_name: str
    attrs: list[PolyTraitPropertyImpl]


class PolyTraitPropertyMatch(RustTemplateModel):
    template: ClassVar[str] = "poly_trait_property_match.rs.jinja"
    name: str
    range: RustRange
    struct_name: str
    cases: list[str]

    @computed_field
    def is_optional(self) -> bool:
        """
        Whether this property is optional
        """
        return self.range.optional

    @computed_field
    def is_container(self) -> bool:
        """
        Whether this property is a container type
        """
        return self.range.containerType is not None

    @computed_field
    def type_getter(self) -> str:
        if self.range.child_ranges is not None and len(self.range.child_ranges) > 1:
            return self.range.type_for_trait_value(crateref="crate")
        return self.range.type_for_trait(setter=False, crateref="crate")

    @computed_field
    def needs_lifetime(self) -> bool:
        t = self.type_getter
        return ("&" in t) or ("SeqRef" in t) or ("MapRef" in t)

    @computed_field
    def base_union_type(self) -> str:
        return self.range.type_

    @computed_field
    def range_variant(self) -> str:
        # Always use centralized type name logic
        return self.range.type_name()

    @computed_field
    def current_union_types(self) -> dict[str, str]:
        m: dict[str, str] = {}
        for c in self.cases:
            sc = underscore(uncamelcase(c))
            m[c] = f"{sc}_utl::{self.name}_range"
        return m


class PolyTraitImplForSubtypeEnum(RustTemplateModel):
    """Trait implementation that dispatches based on subtype enums."""

    template: ClassVar[str] = "poly_trait_impl_orsubtype.rs.jinja"
    enum_name: str
    name: str
    attrs: list[PolyTraitPropertyMatch]


class PolyTrait(RustTemplateModel):
    """Definition of a polymorphic trait generated from a class hierarchy."""

    template: ClassVar[str] = "poly_trait.rs.jinja"
    name: str
    attrs: list[PolyTraitProperty]
    superclass_names: list[str]
    impls: list[PolyTraitImpl]
    subtypes: list[PolyTraitImplForSubtypeEnum]


class PolyFile(RustTemplateModel):
    """Rust file aggregating polymorphic traits."""

    template: ClassVar[str] = "poly.rs.jinja"
    imports: Imports = Imports()
    traits: list[PolyTrait]


class RustFile(RustTemplateModel):
    """
    A whole rust file!
    """

    template: ClassVar[str] = "file.rs.jinja"

    name: str
    imports: Imports = Imports()
    types: list[RustTypeAlias] = Field(default_factory=list)
    structs: list[RustStruct] = Field(default_factory=list)
    enums: list[RustEnum] = Field(default_factory=list)
    slots: list[RustTypeAlias] = Field(default_factory=list)
    # Single-file generation knobs
    inline_serde_utils: bool = False
    emit_poly: bool = True
    serde_utils: Optional[SerdeUtilsFile] = None
    root_struct_name: Optional[str] = None

    @computed_field
    def struct_names(self) -> list[str]:
        """Names of all the structs we have!"""
        return [c.name for c in self.structs]

    @computed_field
    def pyclass_struct_names(self) -> list[str]:
        """Names of structs that implement PyClass and should be registered.

        Excludes special cases like `Anything` (and its alias `AnyValue`) which
        are not exposed as #[pyclass] in the special-case template.
        """
        out: list[str] = []
        for c in self.structs:
            if c.name in ("Anything", "AnyValue"):
                continue
            out.append(c.name)
        return out

    @computed_field
    def needs_overwrite_except_none(self) -> bool:
        """Whether any struct uses the custom merge helper."""
        return any(s.generate_merge for s in self.structs)


class RangeEnum(RustTemplateModel):
    """
    A range enum!
    """

    template: ClassVar[str] = "range_enum.rs.jinja"
    name: str
    type_: list[str]


class RustCargo(RustTemplateModel):
    """
    A Cargo.toml file
    """

    template: ClassVar[str] = "Cargo.toml.jinja"

    name: str
    version: str = "0.0.0"
    edition: str = "2021"
    pyo3_version: str = "0.21.1"
    imports: Imports = Imports()

    @computed_field
    def cratefeatures(self) -> dict[str, list[str]]:
        feature_flags: dict[str, list[str]] = {}
        for i in self.imports.imports:
            assert isinstance(i, Import)
            if i.feature_flag is None:
                continue
            deps = feature_flags.setdefault(i.feature_flag, [])
            module = i.module.split("::")[0]
            dep_entry = f"dep:{module}"
            if dep_entry not in deps:
                deps.append(dep_entry)
            for extra in i.feature_dependencies:
                if extra not in deps:
                    deps.append(extra)
        return feature_flags

    @field_validator("name", mode="after")
    @classmethod
    def snake_case_name(cls, value: str) -> str:
        return underscore(value)

    def render(self, environment: Optional[Environment] = None, **kwargs) -> str:
        if environment is None:
            environment = RustTemplateModel.environment()

        fields = {**self.model_fields, **self.model_computed_fields}
        data = {k: getattr(self, k, None) for k in fields}
        # don't render the template
        imports = []
        for i in data.get("imports", []):
            imp = i.model_dump()
            imp["module"] = imp["module"].split("::")[0]
            imports.append(imp)
        data["imports"] = imports

        data = {k: _render(v, environment) for k, v in data.items()}
        template = environment.get_template(self.template)
        rendered = template.render(**data)
        return rendered


class RustPyProject(RustTemplateModel):
    """
    A pyproject.toml file to go with a maturin/pyo3 package
    """

    template: ClassVar[str] = "pyproject.toml.jinja"

    name: str
    version: str = "0.0.0"

    @field_validator("name", mode="after")
    @classmethod
    def snake_case_name(cls, value: str) -> str:
        return underscore(value)


class RustLibShim(RustTemplateModel):
    """Shim module that re-exports generated code and hosts the PyO3 entry point."""

    template: ClassVar[str] = "lib_shim.rs.jinja"
    module_name: str
    root_struct_name: Optional[str] = None
    root_struct_fn_snake: Optional[str] = None
