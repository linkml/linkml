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
# Field numbers run from 1 to 2**29 - 1.
_MAX_FIELD_NUMBER = 536_870_911

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


def _proto_field_name(aliased_slot_name: str) -> str:
    """Return the proto3 field name for a slot: ``snake_case`` and a valid identifier.

    See https://protobuf.dev/programming-guides/style/#message-and-field-names
    """
    return _to_proto_ident(underscore(aliased_slot_name))


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
    # Per-class field statements keyed by field number. visit_class_slot fills
    # it and end_class writes it out in field-number order.
    _fields: dict[int, str] = field(default_factory=dict, init=False, repr=False)

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

    def _identifier_slot_for(self, cls_name: str) -> SlotDefinition | None:
        """Return the identifier slot of the class *cls_name*, or None.

        The SchemaLoader has already rolled inherited and mixin slots into
        ``cls.slots``, so no ``is_a`` walk is needed. Only ``identifier``
        counts: a ``key`` identifies an object within its container only, so a
        key-only class is still inlined, as ``SchemaView.is_inlined`` has it.
        """
        for sname in self.schema.classes[cls_name].slots:
            slot = self.schema.slots[sname]
            if slot.identifier:
                return slot
        return None

    def _proto_range_for_slot(self, slot: SlotDefinition) -> tuple[str, str | None]:
        """Resolve *slot* to a proto3 type, honouring inlined versus reference.

        A slot whose range is a class carries either the whole nested object
        (inlined) or only its identifier (a reference). A reference maps to the
        identifier slot's scalar, typically ``string``, because that is what
        travels on the wire; an inlined object keeps the message reference. A
        slot is inlined when ``inlined`` or ``inlined_as_list`` is set, or when
        the range class has no identifier slot that could stand in for it. The
        SchemaLoader sets ``inlined`` in that second case itself, except for a
        class that has only a ``key``.

        Returns the proto type and, for a reference, the name of the class
        referred to, so that the caller can say so in a comment.
        """
        if slot.range in self.schema.classes and not (slot.inlined or slot.inlined_as_list):
            id_slot = self._identifier_slot_for(slot.range)
            if id_slot is not None:
                return self._proto_range(id_slot.range), slot.range
        return self._proto_range(slot.range), None

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

    def _ranked_field_numbers(self, cls: ClassDefinition, slots: list[SlotDefinition]) -> dict[str, int]:
        """Return the field numbers that ``rank`` pins for *slots*, keyed by slot name.

        A rank that proto3 cannot use as a field number is dropped with a
        warning, and the slot is numbered automatically instead: a rank outside
        1 to 536870911, one inside the reserved range 19000 to 19999, or one
        that another slot of the same class already claims.
        """
        numbers: dict[str, int] = {}
        taken: dict[int, str] = {}
        for slot in slots:
            rank = slot.rank
            if not rank:
                continue
            name = self.aliased_slot_name(slot)
            if rank in taken:
                reason = f"rank {rank} is already used by {taken[rank]}"
            elif not 1 <= rank <= _MAX_FIELD_NUMBER or _RESERVED_FIELD_LO <= rank <= _RESERVED_FIELD_HI:
                reason = f"rank {rank} is not a usable proto3 field number"
            else:
                numbers[slot.name] = rank
                taken[rank] = name
                continue
            self.logger.warning(f"{cls.name}.{name}: {reason}; assigning its field number automatically")
        return numbers

    def _slots_to_emit(self, cls: ClassDefinition) -> list[SlotDefinition]:
        """Return the slots of *cls* to write out, one per proto field name.

        Two LinkML slot names can sanitise to one field name, for example when
        a ``slot_usage`` spells an inherited slot ``related to`` instead of
        ``related_to`` and the SchemaLoader induces a second slot from it. A
        message cannot declare a field twice, so the later slot replaces the
        earlier one, with a warning; in the loader's order that is the more
        specific slot, because a class's own and ``slot_usage`` slots follow
        the ones it inherits. The field keeps the earlier slot's position.
        """
        by_field: dict[str, SlotDefinition] = {}
        for slot in self.all_slots(cls):
            field_name = _proto_field_name(self.aliased_slot_name(slot))
            if field_name in by_field:
                self.logger.warning(
                    f"{cls.name}: slots {self.aliased_slot_name(by_field[field_name])} and "
                    f"{self.aliased_slot_name(slot)} both map to proto field {field_name}; keeping the latter"
                )
            by_field[field_name] = slot
        return list(by_field.values())

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
        # proto3 forbids field number 0, requires uniqueness within a message,
        # caps numbers at 2**29 - 1 and reserves 19000-19999. LinkML's `rank`
        # pins a number, which lets authors keep wire compatibility; every
        # other slot is numbered automatically from 1 in source order, skipping
        # pinned and reserved numbers. When no slot has a rank, the identifier
        # slot, if any, takes field 1: the convention phenopackets and other
        # wire-shaped schemas follow.
        #
        # Doing this once up front keeps visit_class_slot a simple lookup.
        slots = self._slots_to_emit(cls)
        self._field_numbers = self._ranked_field_numbers(cls, slots)
        if not self._field_numbers:
            id_slot = next((s for s in slots if s.identifier), None)
            if id_slot is not None:
                self._field_numbers[id_slot.name] = 1
        used = set(self._field_numbers.values())
        next_auto = 1
        for slot in slots:
            if slot.name in self._field_numbers:
                continue
            next_auto = self._next_field_number(next_auto, used)
            self._field_numbers[slot.name] = next_auto
            used.add(next_auto)
            next_auto += 1
        self._fields = {}

        items = []
        if cls.description:
            for dline in cls.description.split("\n"):
                items.append(f"// {dline}")
        items.append(f"message {camelcase(cls.name)} {{")
        return "\n".join(items)

    def end_class(self, cls: ClassDefinition) -> str:
        # Fields are written in field-number order, so the identifier (field 1
        # when no rank is set) leads the message whatever its source order.
        body = "".join(self._fields[n] for n in sorted(self._fields))
        return body + "\n}\n"

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        if slot.name not in self._field_numbers:
            # Another slot of this class claimed the same proto field name (see _slots_to_emit).
            return
        qual = "repeated " if slot.multivalued else ""
        slotname = _proto_field_name(aliased_slot_name)

        # A non-inlined class range resolves to the identifier scalar of the
        # range class (typically `string`) rather than the class name: a
        # reference travels as the identifier, not as a nested message.
        slot_range, referenced = self._proto_range_for_slot(slot)
        lines: list[str] = []
        # Slot description -> `//` comments, mirroring the class-level loop in
        # visit_class. Useful for both meta and wire consumers.
        if slot.description:
            for dline in slot.description.split("\n"):
                lines.append(f"  // {dline}")
        # Mark the identifier slot, as phenopackets and FHIR proto files do.
        if slot.identifier:
            lines.append("  // identifier")
        # proto3 has no `required` keyword (proto2 dropped it), but the comment
        # still tells downstream consumers and a LinkML round-trip what holds.
        if slot.required:
            lines.append("  // required")
        # Name the class a reference points at; the scalar type alone no longer says.
        if referenced is not None:
            lines.append(f"  // reference to {camelcase(referenced)}")
        # Every proto3 field statement must end with `;` - without it `protoc`
        # rejects the file. The field number comes from the pre-computed map
        # built in visit_class so we never emit forbidden ""= 0".
        number = self._field_numbers[slot.name]
        lines.append(f"  {qual}{slot_range} {slotname} = {number};")
        self._fields[number] = "\n" + "\n".join(lines)

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
