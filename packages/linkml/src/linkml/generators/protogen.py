import os
import re
from dataclasses import dataclass, field

import click

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore

# ---------------------------------------------------------------------------
# LinkML built-in type -> proto3 scalar
# https://linkml.io/linkml-model/linkml_model/model/schema/types.yaml
# https://protobuf.dev/programming-guides/proto3/#scalar
# ---------------------------------------------------------------------------
# Proto scalar, keyed by LinkML types->base.
_PROTO_SCALAR_BY_LINKML_BASE: dict[str, str] = {
    "str": "string",  # str, jsonpointer, jsonpath, sqarqlpath
    "int": "int32",
    "Bool": "bool",  # base: Bool
    "bool": "bool",  # repr: bool
    "float": "float",  # proto =IEEE 754 single-precision
    "double": "double",  # proto =IEEE 754 double-precision
    "Decimal": "string",  # linkml =Capitalized.
    ## Linkml - repr: str
    "XSDTime": "string",
    "XSDDate": "string",
    "XSDDateTime": "string",  # (datetime/date_or_datetime)
    "URIorCURIE": "string",
    "Curie": "string",
    "URI": "string",
    "NCName": "string",
    "NodeIdentifier": "string",
    "ElementIdentifier": "string",
    "Bytes": "bytes",
    # XSD-flavoured aliases, defensive
    "XSDString": "string",
    "XSDInteger": "int32",
    "XSDBoolean": "bool",
    "XSDFloat": "float",
    "XSDDouble": "double",
}

# Name-keyed override for LinkML types whose ``base`` is ambiguous.
#
# LinkML's standard library defines both "float" and "double" with
# "base: float" (both Python floats), so a base-only lookup would
# collapse the proto-side distinction between 32-bit and 64-bit IEEE 754.
# So special-case the canonical type names here.
_PROTO_SCALAR_BY_LINKML_NAME: dict[str, str] = {
    "double": "double",
}

# https://protobuf.dev/programming-guides/proto3/#assigning
# proto3 reserves field numbers 19000-19999 for internal use.
_RESERVED_FIELD_LO = 19000
_RESERVED_FIELD_HI = 19999

# Fallback when we can't resolve a slot range (e.g. unknown reference).
# "string" is safest choice - (see _PROTO_SCALAR_BY_LINKML_BASE)
_PROTO_DEFAULT_SCALAR = "string"


def _to_proto_ident(value: str) -> str:
    """Sanitise *value* into a proto3 identifier that follows Google's style guide.

    See https://protobuf.dev/programming-guides/style/#identifier

    The rule we enforce: identifiers must not start or end with an underscore,
    and every underscore must be followed by a letter (never a digit or another
    underscore). Concretely:

    - Non-identifier characters become ``_``.
    - Runs of underscores collapse to one (no ``__``).
    - Any underscore immediately followed by a digit has an ``N`` inserted
      (``foo_2bar`` becomes "foo_N2bar") since digits aren't allowed after
      ``_``. Inserting rather than dropping keeps ``foo_2bar`` distinct from
      ``foo2bar`` (reusing the same leading-digit prefix rule below).
    - Leading and trailing underscores are stripped.
    - An empty result, or one starting with a digit, is prefixed with ``N`` so
      identifier matches ``[A-Za-z][A-Za-z0-9_]*`` and never starts with ``_``.
    """
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", (value or "").strip())
    cleaned = re.sub(r"_+", "_", cleaned)
    cleaned = re.sub(r"_(\d)", r"_N\1", cleaned)
    cleaned = cleaned.strip("_")
    if not cleaned:
        return "N"
    if cleaned[0].isdigit():
        cleaned = "N" + cleaned
    return cleaned


def _to_upper_snake(value: str) -> str:
    """Convert *value* to UPPER_SNAKE_CASE for use as a proto3 enum value name."""
    # Break CamelCase into CAMEL_CASE before sanitising - this preserves word
    # boundaries that would otherwise be merged together by _to_proto_ident.
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value or "")
    return _to_proto_ident(s).upper()


@dataclass
class ProtoGenerator(Generator):
    """
    A `Generator` for creating Protobuf schemas from a linkml schema.

    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["proto"]
    visit_all_class_slots = True
    uses_schemaloader = True

    # ObjectVars
    # Per-class map of slot name -> proto field number. Populated in visit_class
    # so visit_class_slot can look up the pre-computed number without having to
    # repeat the collision-avoidance logic for every slot.
    _field_numbers: dict[str, int] = field(default_factory=dict, init=False, repr=False)

    # ------------------------------------------------------------------ header

    def visit_schema(self, **kwargs) -> str | None:
        return self.generate_header()

    @staticmethod
    def _sanitise_proto_package(value: str | None) -> str | None:
        """Coerce *value* into a valid proto3 package identifier, or return None.

        Proto3 package identifiers may be dot-separated; each segment must
        match ``[A-Za-z_][A-Za-z0-9_]*``. We additionally follow the proto3
        style guide: no leading/trailing underscores, no consecutive
        underscores, and no underscore immediately followed by a digit. An
        ``_`` before a digit gets an ``N`` inserted (``foo_2bar`` becomes
        "foo_n2bar") rather than dropped, so ``foo_2bar`` stays distinct from
        ``foo2bar``.

        Returns None when no usable identifier can be derived - the caller
        then omits the ``package`` line (it's optional in proto3).
        """
        candidate = re.sub(r"[^A-Za-z0-9_.]", "_", (value or "").strip())
        # Collapse runs of underscores; insert `N` after any `_` that precedes
        # a digit (non-destructive, keeps `foo_2bar` distinct from `foo2bar`).
        candidate = re.sub(r"_+", "_", candidate)
        candidate = re.sub(r"_(\d)", r"_N\1", candidate)
        candidate = candidate.strip("._").lower()
        if not candidate or candidate[0].isdigit():
            return None
        return candidate

    def _proto_package(self) -> str | None:
        """Derive a proto3 package name from the schema's ``name`` attribute.

        The schema id is a URI and rarely converts cleanly to a proto
        identifier, so we use "schema.name" as the source. If that name can't
        be sanitised into a valid identifier, return None.
        """
        return self._sanitise_proto_package(self.schema.name)

    def generate_header(self) -> str:
        # https://protobuf.dev/reference/protobuf/proto3-spec/#syntax
        items = ['syntax = "proto3";']
        # https://protobuf.dev/reference/protobuf/proto3-spec/#package
        pkg = self._proto_package()
        # 'package' is optional in proto3 - only emit when non-bare (valued).
        if pkg:
            items.append(f"package {pkg};")
        items.append(f"// metamodel_version: {self.schema.metamodel_version}")
        if self.schema.version:
            items.append(f"// version: {self.schema.version}")
        return "\n".join(items) + "\n"

    # ------------------------------------------------ range / type resolution

    def _proto_range(self, slot_range: str | None) -> str:
        """Resolve a slot range to a proto3 type reference.

        Order of resolution:
          1. LinkML type   -> mapped proto3 scalar (via its ``base``).
          2. Schema class  -> CamelCase message reference.
          3. Schema enum   -> CamelCase enum reference.
          4. Unknown / missing -> ``string`` (safe fallback).

        References to messages and enums must be CamelCase to match the
        declared names - earlier versions of this generator used lcamelcase
        here, producing references that didn't resolve.
        """
        if not slot_range:
            return _PROTO_DEFAULT_SCALAR
        if slot_range in self.schema.types:
            return self._proto_scalar_for_type(slot_range)
        if slot_range in self.schema.classes or slot_range in self.schema.enums:
            return camelcase(slot_range)
        return _PROTO_DEFAULT_SCALAR

    def _proto_scalar_for_type(self, type_name: str) -> str:
        """Map a LinkML type to a proto3 scalar by walking its ``typeof`` chain.

        Some schemas define derived types like ``age_in_years_type`` with
        ``typeof: integer``. We resolve with the following precedence:

        1. **Name override anywhere in the chain.** Handles e.g. ``double``,
           whose ``base`` ambiguously equals ``float`` in LinkML's stdlib —
           and which the schema-loader propagates down to derived types like
           ``Coordinate64: typeof: double``, so the name match needs to win
           regardless of where in the chain it appears.
        2. **Base mapping**, taking the first match while walking up.
        3. Otherwise, fall back to ``string``.
        """
        # Pass 1: name override anywhere in the typeof chain.
        seen: set[str] = set()
        current: str | None = type_name
        while current and current in self.schema.types and current not in seen:
            seen.add(current)
            if current in _PROTO_SCALAR_BY_LINKML_NAME:
                return _PROTO_SCALAR_BY_LINKML_NAME[current]
            current = self.schema.types[current].typeof

        # Pass 2: base lookup walking the chain top-down.
        seen.clear()
        current = type_name
        while current and current in self.schema.types and current not in seen:
            seen.add(current)
            t = self.schema.types[current]
            if t.base and t.base in _PROTO_SCALAR_BY_LINKML_BASE:
                return _PROTO_SCALAR_BY_LINKML_BASE[t.base]
            current = t.typeof
        return _PROTO_DEFAULT_SCALAR

    # ----------------------------------------------- field number assignment

    @staticmethod
    def _next_field_number(n: int, used: set[int]) -> int:
        """Return the next available field number >= *n*.

        Skips numbers already claimed, and reserved range 19000-19999.
        """
        while n in used or _RESERVED_FIELD_LO <= n <= _RESERVED_FIELD_HI:
            n += 1
        return n

    # ---------------------------------------------- class & slot emission

    def visit_class(self, cls: ClassDefinition) -> str | None:
        # Every class is emitted as a proto3 message - including mixins,
        # abstracts, and slot-less concrete classes:
        # https://protobuf.dev/reference/protobuf/proto3-spec/#message_definition
        #   - proto3 has no concept of "mixin" or "abstract"; the only way to
        #     keep a reference to such a class valid is to declare it.
        #   - Slot-less classes become empty messages (`message X {}`), which
        #     proto3 allows. https://protobuf.dev/reference/protobuf/google.protobuf/#empty
        #     Otherwise, any field whose range is such a class would point at a non-existent
        #     type and protoc would fail.
        # The trade-off is that LinkML's mixin/abstract semantics are not
        # carried over to proto3, but the resulting file is always compilable and every
        # range reference resolves to a declared message.

        # Pre-compute proto field numbers for every slot in this class.
        #
        # Pre-pass: proto3 forbids field number 0, requires uniqueness within a
        # message, and reserves 19000-19999. Honor LinkML's `rank` slot (allow
        # pinning numbers for wire compatibility) and auto-assign the rest (starting
        # at 1), skipping numbers already claimed by rank, and reserved range.

        # Doing this once up front keeps visit_class_slot a simple lookup.
        used_ranks = {s.rank for s in self.all_slots(cls) if s.rank}
        next_auto = 1
        self._field_numbers = {}
        for slot in self.all_slots(cls):
            if slot.rank:
                self._field_numbers[slot.name] = slot.rank
            else:
                next_auto = self._next_field_number(next_auto, used_ranks)
                self._field_numbers[slot.name] = next_auto
                next_auto += 1

        items = []
        if cls.description:
            for dline in cls.description.split("\n"):
                items.append(f"// {dline}")
        items.append(f"message {camelcase(cls.name)} {{")
        return "\n".join(items)

    def end_class(self, cls: ClassDefinition) -> str:
        return "\n}\n"

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> str:
        qual = "repeated " if slot.multivalued else ""
        # snake_case per https://protobuf.dev/programming-guides/style/#message-and-field-names
        # `_to_proto_ident` enforces the proto3 identifier rules:
        # (no leading or trailing `_`, no `__`, no `_<digit>`).
        slotname = _to_proto_ident(underscore(aliased_slot_name))

        slot_range = self._proto_range(slot.range)
        lines: list[str] = []
        # Slot description -> `//` comments, mirroring the class-level loop in
        # visit_class. Useful for both meta and wire consumers.
        if slot.description:
            for dline in slot.description.split("\n"):
                lines.append(f"  // {dline}")
        # Every proto3 field statement must end with `;` - without it `protoc`
        # rejects the file. The field number comes from the pre-computed map
        # built in visit_class so we never emit forbidden ""= 0".
        lines.append(f"  {qual}{slot_range} {slotname} = {self._field_numbers[slot.name]};")
        return "\n" + "\n".join(lines)

    # ------------------------------------------------------- enum emission

    def end_schema(self, **kwargs) -> str | None:
        """Emit an ``enum { ... }`` block for every LinkML enum.

        https://protobuf.dev/programming-guides/proto3/#enum
        https://protobuf.dev/programming-guides/proto3/#enum-default

        proto3 enum constraints honoured here:
          - The first enum declared value must be numeric "0" and should have
          . the name ENUM_TYPE_NAME_UNSPECIFIED or ENUM_TYPE_NAME_UNKNOWN.
            we can use 0 as a numeric default value, for proto2 compatibility.
            So real permissible values start at "1", preserving semantics.
          - All enum value names share a namespace at the enclosing scope.
            To avoid collisions across multiple enums in the same proto file
            we prefix every value with the enum name in UPPER_SNAKE_CASE
            (e.g. ``FAMILIAL_RELATIONSHIP_TYPE_SIBLING_OF``).
          - All identifiers must match ``[A-Za-z_][A-Za-z0-9_]*``; permissible
            values with spaces or other punctuation are sanitised.

        Enums are emitted after the messages. Order is purely cosmetic.
        """
        if not self.schema.enums:
            return None
        blocks: list[str] = []
        for ename in sorted(self.schema.enums):
            enum: EnumDefinition = self.schema.enums[ename]
            proto_name = camelcase(ename)
            value_prefix = _to_upper_snake(ename)
            lines: list[str] = []
            if enum.description:
                for dline in enum.description.split("\n"):
                    lines.append(f"// {dline}")
            lines.append(f"enum {proto_name} {{")

            # Synthetic zero-value sentinel - added first so its identifier
            # is also in `seen_values` for the dedupe loop below (in case a
            # real permissible value happens to be named "UNSPECIFIED").
            unspecified_ident = f"{value_prefix}_UNSPECIFIED"
            lines.append(f"  {unspecified_ident} = 0;")
            seen_values: set[str] = {unspecified_ident}

            # Real permissible values start at 1; 0 is reserved for the
            # UNSPECIFIED sentinel emitted above.
            for i, pv_name in enumerate(enum.permissible_values or {}, start=1):
                value_ident = f"{value_prefix}_{_to_upper_snake(pv_name)}"

                # Defensive dedupe - two permissible values that sanitise to
                # the same identifier would otherwise produce a proto3 error.
                # Suffix is `_V<n>` (not `_<n>`) so the underscore is followed
                # by a letter, per the proto3 style guide.
                base_ident = value_ident
                suffix = 2
                while value_ident in seen_values:
                    value_ident = f"{base_ident}_V{suffix}"
                    suffix += 1
                seen_values.add(value_ident)
                lines.append(f"  {value_ident} = {i};")
            lines.append("}")
            blocks.append("\n".join(lines))
        return "\n" + "\n".join(blocks) + "\n"


@shared_arguments(ProtoGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command(name="proto")
def cli(yamlfile, **args):
    """Generate proto representation of LinkML model"""
    print(ProtoGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
