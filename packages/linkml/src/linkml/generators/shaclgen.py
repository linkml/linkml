import logging
import os
import string
from collections.abc import Callable
from dataclasses import dataclass

import click
from jsonasobj2 import JsonObj, as_dict
from rdflib import BNode, Graph, Literal, URIRef
from rdflib.collection import Collection
from rdflib.namespace import RDF, RDFS, SH, XSD

from linkml._version import __version__
from linkml.generators.common.subproperty import get_subproperty_values, is_uri_range
from linkml.generators.shacl.shacl_data_type import ShaclDataType
from linkml.generators.shacl.shacl_ifabsent_processor import ShaclIfAbsentProcessor
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.language_tags import LanguageTagResolver
from linkml_runtime.linkml_model.meta import ClassDefinition, ElementName, PresenceEnum
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph
from linkml_runtime.utils.yamlutils import TypedNode, extended_float, extended_int, extended_str

logger = logging.getLogger(__name__)


MESSAGE_TEMPLATE_FIELDS = ("name", "title", "description", "comments", "class", "path")
"""Placeholders permitted in ``--message-template`` (see :attr:`ShaclGenerator.message_template`)."""


def _validate_message_template(template: str) -> None:
    """Validate a ``--message-template`` string, failing fast with a helpful error.

    Only the bare placeholders in :data:`MESSAGE_TEMPLATE_FIELDS` are permitted.
    Attribute access (``{name.foo}``), indexing (``{name[0]}``), positional fields
    (``{0}`` / ``{}``), conversions (``{name!r}``) and format specs (``{name:>5}``)
    are all rejected, as are unbalanced braces. Validation runs once, up front, so a
    malformed template is caught even for schemas that contain no slots.

    :param template: the raw template string.
    :raises ValueError: if the template contains an unsupported placeholder or is
        otherwise malformed.
    """
    allowed = frozenset(MESSAGE_TEMPLATE_FIELDS)
    hint = "Allowed placeholders: " + ", ".join(f"{{{name}}}" for name in MESSAGE_TEMPLATE_FIELDS)
    try:
        parsed = list(string.Formatter().parse(template))
    except ValueError as exc:
        raise ValueError(f"Invalid placeholder in --message-template ({exc}). {hint}") from None
    for _literal_text, field_name, format_spec, conversion in parsed:
        if field_name is None:
            continue
        if field_name not in allowed:
            raise ValueError(f"Invalid placeholder '{{{field_name}}}' in --message-template. {hint}")
        if conversion is not None or format_spec:
            raise ValueError(
                f"Invalid placeholder '{{{field_name}}}' in --message-template: "
                f"conversions and format specs are not supported. {hint}"
            )


@dataclass
class ShaclGenerator(Generator):
    """Generate SHACL (Shapes Constraint Language) shapes from a LinkML schema.

    SHACL shapes are used to validate RDF data. Each LinkML class is converted
    to a ``sh:NodeShape`` with property constraints derived from the class's slots.

    Shape Naming Modes
    ------------------
    The generator supports two naming modes controlled by ``use_class_uri_names``:

    **Default mode** (``use_class_uri_names=True``):
        Shapes are named using the ``class_uri``. If multiple LinkML classes share
        the same ``class_uri``, their properties are merged into a single shape.
        This is the traditional RDF-centric behavior.

        Example: LinkML classes ``Entity`` and ``EvaluatedEntity`` both with
        ``class_uri prov:Entity`` produce a single shape ``<prov:Entity>``.

    **Native names mode** (``use_class_uri_names=False``):
        Shapes are named using the native LinkML class name from the schema.
        Each LinkML class produces a distinct shape, even if they share a ``class_uri``.
        The ``sh:targetClass`` still correctly points to the ``class_uri``.

        Example: The same two classes produce two shapes, each with
        ``sh:targetClass prov:Entity``.

    Use native names mode when multiple LinkML classes intentionally map to the
    same external ontology class and you need distinct validation shapes per class.
    See `#3011 <https://github.com/linkml/linkml/issues/3011>`_ for background.
    """

    # ClassVars
    closed: bool = True
    """True means add 'sh:closed=true' to all shapes, except of mixin shapes and shapes, that have parents"""
    suffix: str = None
    """parameterized suffix to be appended. No suffix per default."""
    include_annotations: bool = False
    """True means include all class / slot / type annotations in generated Node or Property shapes"""
    exclude_imports: bool = False
    """If True, elements from imported ontologies won't be included in the generator's output"""
    use_class_uri_names: bool = True
    """
    Control how SHACL shape URIs are generated.

    If True (default): Shape URIs are derived from class_uri. Classes sharing a class_uri
    will be merged into a single shape.

    If False: Shape URIs use native LinkML class names. Each class gets a distinct shape
    even when sharing class_uri. The --suffix option still works in either mode.
    """
    expand_subproperty_of: bool = True
    """If True, expand subproperty_of to sh:in constraints with slot descendants"""

    default_language: str | None = None
    """Default BCP 47 language tag for human-readable string literals.

    When set, ``sh:name``, ``sh:description``, ``rdfs:label``, and
    ``rdfs:comment`` literals are emitted with the specified language tag.
    Conforms to :rfc:`5646` (BCP 47).
    """

    message_template: str | None = None
    """Template for ``sh:message`` on property shapes.

    When set, each property shape receives an ``sh:message`` literal built from
    this template.  The following placeholders are expanded:

    * ``{name}`` — the slot's LinkML name, exactly as written in the schema
    * ``{title}`` — the slot title (human-readable), falls back to *name*
    * ``{description}`` — the slot description, falls back to empty string
    * ``{comments}`` — the slot comments joined with ``; ``, falls back to empty string
    * ``{class}`` — the enclosing class name
    * ``{path}``  — the fully-expanded property IRI

    Example: ``"Validation of {name} failed!"`` →
    ``sh:message "Validation of has_speed failed!"``

    If ``default_language`` is set the literal is tagged with it. The message text
    is a single template, so it deliberately follows ``default_language`` only and
    ignores any per-slot ``in_language``.
    """

    emit_rules: bool = True
    """Emit ``sh:sparql`` constraints from LinkML ``rules:`` blocks.

    When ``True`` (default), recognised rule patterns are translated into
    SHACL-SPARQL constraints (``sh:SPARQLConstraint``) on the corresponding
    ``sh:NodeShape``.  Currently two patterns are recognised:

    * *Boolean guard* — a precondition with ``value_presence: PRESENT`` on a
      value slot and a postcondition with ``equals_string: "true"`` on a
      boolean flag slot.
    * *Exclusive value* — a precondition with ``equals_string`` on a slot and
      a postcondition with ``maximum_cardinality`` on the *same* slot.

    See `W3C SHACL §5 <https://www.w3.org/TR/shacl/#sparql-constraints>`_
    and `linkml/linkml#2464 <https://github.com/linkml/linkml/issues/2464>`_.
    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["ttl"]
    file_extension = "shacl.ttl"
    visit_all_class_slots = False
    uses_schemaloader = False

    def _resolve_language(self, element=None) -> str | None:
        """Return the BCP 47 language tag for *element*, or ``None``.

        Delegates to :class:`linkml.utils.language_tags.LanguageTagResolver`.
        Resolution order is element-level ``in_language`` first, then the
        generator-level default.
        """
        return self._language_resolver.resolve(element)

    def __post_init__(self) -> None:
        # Resolver must be assigned before ``super().__post_init__()`` so that
        # any hook the parent invokes during initialisation can safely call
        # ``_resolve_language``. The resolver also validates the default tag
        # once here; per-element tags are validated lazily, with at most one
        # warning per distinct malformed tag.
        self._language_resolver = LanguageTagResolver(self.default_language)
        super().__post_init__()
        self.message_template = (self.message_template or "").strip() or None
        if self.message_template is not None:
            _validate_message_template(self.message_template)
        self.generate_header()

    def generate_header(self) -> str:
        out = f"\n# metamodel_version: {self.schema.metamodel_version}"
        if self.schema.version:
            out += f"\n# version: {self.schema.version}"
        return out

    def serialize(self, **args) -> str:
        g = self.as_graph()
        fmt = "turtle" if self.format in ["owl", "ttl"] else self.format
        return canonicalize_rdf_graph(g, output_format=fmt)

    def as_graph(self) -> Graph:
        sv = self.schemaview
        g = Graph()
        g.bind("sh", SH)

        ifabsent_processor = ShaclIfAbsentProcessor(sv)

        for pfx in self.schema.prefixes.values():
            g.bind(str(pfx.prefix_prefix), pfx.prefix_reference)

        for c in sv.all_classes(imports=not self.exclude_imports).values():

            def shape_pv(p, v):
                if v is not None:
                    g.add((class_uri_with_suffix, p, v))

            class_uri = URIRef(sv.get_uri(c, expand=True))
            if self.use_class_uri_names:
                class_uri_with_suffix = class_uri
            else:
                class_uri_with_suffix = URIRef(sv.get_uri(c, expand=True, native=True))
            if self.suffix:
                class_uri_with_suffix += self.suffix
            shape_pv(RDF.type, SH.NodeShape)
            shape_pv(SH.targetClass, class_uri)  # TODO

            if self.closed:
                if c.mixin or c.abstract:
                    shape_pv(SH.closed, Literal(False))
                else:
                    shape_pv(SH.closed, Literal(True))
            else:
                shape_pv(SH.closed, Literal(False))
            if c.title is not None:
                # Use rdfs:label for NodeShape titles per SHACL spec.
                # sh:name has rdfs:domain of sh:PropertyShape. See issue #3059.
                shape_pv(RDFS.label, Literal(c.title, lang=self._resolve_language(c)))
            if c.description is not None:
                # Use rdfs:comment for NodeShape descriptions per SHACL spec.
                # sh:description has rdfs:domain of sh:PropertyShape, so using it
                # on NodeShapes causes RDFS-aware validators to incorrectly infer
                # the NodeShape is also a PropertyShape. See issue #3059.
                shape_pv(RDFS.comment, Literal(c.description, lang=self._resolve_language(c)))

            shape_pv(SH.ignoredProperties, self._build_ignored_properties(g, c))

            if c.annotations and self.include_annotations:
                self._add_annotations(shape_pv, c)
            order = 0
            for s in sv.class_induced_slots(c.name):
                # fixed in linkml-runtime 1.1.3
                if s.name in sv.element_by_schema_map():
                    slot_uri = URIRef(sv.get_uri(s, expand=True))
                else:
                    pfx = sv.schema.default_prefix
                    slot_uri = URIRef(sv.expand_curie(f"{pfx}:{underscore(s.name)}"))
                pnode = BNode()
                shape_pv(SH.property, pnode)

                def prop_pv(p, v):
                    if v is not None:
                        g.add((pnode, p, v))

                def prop_pv_literal(p, v):
                    if v is not None:
                        g.add((pnode, p, Literal(v)))

                def prop_pv_text(p, v):
                    if v is not None:
                        g.add((pnode, p, Literal(v, lang=self._resolve_language(s))))

                prop_pv(SH.path, slot_uri)
                prop_pv_literal(SH.order, order)
                order += 1
                prop_pv_text(SH.name, s.title)
                prop_pv_text(SH.description, s.description)

                # sh:message from a user template. The template is validated once in
                # __post_init__, so expansion here cannot raise. The message is a single
                # template string, so it is tagged with the generator default language
                # only (via _resolve_language(None)) and ignores per-slot in_language.
                if self.message_template is not None:
                    msg_text = self.message_template.format(
                        name=s.name,
                        title=s.title or s.name,
                        description=s.description or "",
                        comments="; ".join(s.comments) if s.comments else "",
                        **{"class": c.name},
                        path=str(slot_uri),
                    ).strip()
                    if msg_text:
                        g.add((pnode, SH.message, Literal(msg_text, lang=self._resolve_language(None))))
                # minCount
                if s.minimum_cardinality:
                    prop_pv_literal(SH.minCount, s.minimum_cardinality)
                elif s.exact_cardinality:
                    prop_pv_literal(SH.minCount, s.exact_cardinality)
                # Identifiers map to the node's IRI rather than a property triple,
                # so there's no arc to constrain with sh:minCount 1 — emitting it
                # would cause spurious violations on every instance.
                elif s.required and not s.identifier:
                    prop_pv_literal(SH.minCount, 1)
                # maxCount
                if s.maximum_cardinality:
                    prop_pv_literal(SH.maxCount, s.maximum_cardinality)
                elif s.exact_cardinality:
                    prop_pv_literal(SH.maxCount, s.exact_cardinality)
                elif not s.multivalued:
                    prop_pv_literal(SH.maxCount, 1)
                prop_pv_literal(SH.minInclusive, s.minimum_value)
                prop_pv_literal(SH.maxInclusive, s.maximum_value)

                all_classes = sv.all_classes()
                if s.any_of:
                    # It is not allowed to use any of and equals_string or equals_string_in in one
                    # slot definition, as both are mapped to sh:in in SHACL
                    if s.equals_string or s.equals_string_in:
                        error = "'equals_string'/'equals_string_in' and 'any_of' are mutually exclusive"
                        raise ValueError(f"{TypedNode.yaml_loc(str(s), suffix='')} {error}")

                    or_node = BNode()
                    prop_pv(SH["or"], or_node)
                    range_list = []
                    for any in s.any_of:
                        r = any.range
                        if r in all_classes:
                            class_node = BNode()

                            def cl_node_pv(p, v):
                                if v is not None:
                                    g.add((class_node, p, v))

                            self._add_class(cl_node_pv, r)
                            range_list.append(class_node)
                        elif r in sv.all_types():
                            t_node = BNode()

                            def t_node_pv(p, v):
                                if v is not None:
                                    g.add((t_node, p, v))

                            self._add_type(t_node_pv, r)
                            range_list.append(t_node)
                        elif r in sv.all_enums():
                            en_node = BNode()

                            def en_node_pv(p, v):
                                if v is not None:
                                    g.add((en_node, p, v))

                            self._add_enum(g, en_node_pv, r)
                            range_list.append(en_node)
                        else:
                            st_node = BNode()

                            def st_node_pv(p, v):
                                if v is not None:
                                    g.add((st_node, p, v))

                            add_simple_data_type(st_node_pv, r)
                            range_list.append(st_node)
                    Collection(g, or_node, range_list)
                else:
                    prop_pv_literal(SH.hasValue, s.equals_number)
                    r = s.range
                    if s.equals_string or s.equals_string_in:
                        # Check if range is "string" as this is mandatory for "equals_string" and "equals_string_in"
                        if r != "string":
                            raise ValueError(
                                f"slot: \"{slot_uri}\" - 'equals_string' and 'equals_string_in'"
                                f" require range 'string' and not '{r}'"
                            )

                    if r in all_classes:
                        cls_def = sv.get_class(r)
                        is_any = cls_def and getattr(cls_def, "class_uri", None) == "linkml:Any"
                        self._add_class(prop_pv, r)
                        if not is_any:
                            if sv.get_identifier_slot(r) is not None:
                                prop_pv(SH.nodeKind, SH.IRI)
                            else:
                                prop_pv(SH.nodeKind, SH.BlankNodeOrIRI)
                    elif r in sv.all_types():
                        self._add_type(prop_pv, r)
                    elif r in sv.all_enums():
                        self._add_enum(g, prop_pv, r)
                    else:
                        add_simple_data_type(prop_pv, r)
                    if s.pattern:
                        prop_pv(SH.pattern, Literal(s.pattern))
                    if s.equals_string:
                        # Map equal_string and equal_string_in to sh:in
                        self._and_equals_string(g, prop_pv, [s.equals_string])
                    if s.equals_string_in:
                        # Map equal_string and equal_string_in to sh:in
                        self._and_equals_string(g, prop_pv, s.equals_string_in)
                    if self.expand_subproperty_of and s.subproperty_of:
                        # Map subproperty_of to sh:in with slot descendants
                        self._add_subproperty_constraint(g, prop_pv, s)

                if s.annotations and self.include_annotations:
                    self._add_annotations(prop_pv, s)

                default_value = ifabsent_processor.process_slot(s, c)
                if default_value:
                    prop_pv(SH.defaultValue, default_value)

            if self.emit_rules:
                self._add_rules(g, class_uri_with_suffix, c)

        return g

    LINKML_ANY_URI = "https://w3id.org/linkml/Any"

    # -------------------------------------------------------------------
    # Rules → sh:sparql
    # -------------------------------------------------------------------

    def _add_rules(self, g: Graph, shape_uri: URIRef, cls: ClassDefinition) -> None:
        """Emit ``sh:sparql`` constraints from LinkML ``rules:`` blocks.

        Each recognised rule is converted into an ``sh:SPARQLConstraint``
        attached to *shape_uri*.  Unrecognised patterns are logged at
        ``DEBUG`` level and silently skipped.

        Currently recognised patterns:

        * **Boolean guard** — a *precondition* with
          ``value_presence: PRESENT`` on a value slot and a *postcondition*
          with ``equals_string: "true"`` on a boolean flag slot.

        * **Exclusive value** — a *precondition* with ``equals_string`` on
          a slot and a *postcondition* with ``maximum_cardinality`` on the
          *same* slot.  Enforces that when a specific value is present in a
          multivalued slot, the total number of values must not exceed the
          given cardinality (typically 1 for mutual exclusion).

        See `W3C SHACL §5 <https://www.w3.org/TR/shacl/#sparql-constraints>`_.
        """
        if not cls.rules:
            return

        sv = self.schemaview
        for rule in cls.rules:
            if getattr(rule, "deactivated", False):
                continue

            if getattr(rule, "bidirectional", False):
                logger.warning(
                    "Rule in class %r has bidirectional=true; "
                    "SHACL-SPARQL generation does not support bidirectional rules. "
                    "Skipping this rule entirely.",
                    cls.name,
                )
                continue

            if getattr(rule, "open_world", False):
                logger.warning(
                    "Rule in class %r has open_world=true; "
                    "SHACL operates under closed-world assumption. "
                    "The constraint is emitted but may not match open-world semantics.",
                    cls.name,
                )

            if getattr(rule, "elseconditions", None):
                logger.warning(
                    "Rule in class %r has elseconditions; "
                    "only the forward (if/then) branch is emitted as sh:sparql. "
                    "The else branch cannot be represented in SHACL-SPARQL.",
                    cls.name,
                )

            sparql_query = self._rule_to_sparql(sv, cls, rule)
            if sparql_query is None:
                logger.debug(
                    "Skipping unsupported rule pattern in class %r: %s",
                    cls.name,
                    getattr(rule, "description", "(no description)"),
                )
                continue

            constraint = BNode()
            g.add((shape_uri, SH.sparql, constraint))
            g.add((constraint, RDF.type, SH.SPARQLConstraint))

            message = getattr(rule, "description", None)
            if message:
                g.add((constraint, SH.message, Literal(message)))

            g.add((constraint, SH.select, Literal(sparql_query)))

    def _rule_to_sparql(self, sv, cls: ClassDefinition, rule) -> str | None:
        """Convert a ``ClassRule`` to a SPARQL SELECT query string.

        Returns ``None`` when the rule does not match any supported pattern.
        """
        pre = getattr(rule, "preconditions", None)
        post = getattr(rule, "postconditions", None)
        if not pre or not post:
            return None

        pre_slots = getattr(pre, "slot_conditions", None) or {}
        post_slots = getattr(post, "slot_conditions", None) or {}

        # Pattern: boolean guard
        # preconditions: exactly one slot with value_presence PRESENT
        # postconditions: exactly one slot with equals_string "true"
        if len(pre_slots) == 1 and len(post_slots) == 1:
            pre_slot_name = next(iter(pre_slots))
            post_slot_name = next(iter(post_slots))

            pre_cond = pre_slots[pre_slot_name]
            post_cond = post_slots[post_slot_name]

            # Note: PresenceEnum.PRESENT is a PermissibleValue, but parsed schemas
            # return PresenceEnum instances — wrapping ensures type-compatible comparison.
            is_value_present = getattr(pre_cond, "value_presence", None) == PresenceEnum(PresenceEnum.PRESENT)
            is_flag_true = getattr(post_cond, "equals_string", None) == "true"

            if is_value_present and is_flag_true:
                return self._build_boolean_guard_sparql(sv, cls, post_slot_name, pre_slot_name)

            # Pattern: exclusive value
            # preconditions: slot X has equals_string (a specific enum value)
            # postconditions: same slot X has maximum_cardinality N
            # Semantics: "If value V is present in slot X, then X has at most N values."
            pre_equals = getattr(pre_cond, "equals_string", None)
            post_max_card = getattr(post_cond, "maximum_cardinality", None)

            if pre_equals is not None and post_max_card is not None and pre_slot_name == post_slot_name:
                return self._build_exclusive_value_sparql(sv, cls, pre_slot_name, pre_equals, int(post_max_card))

        return None

    def _build_boolean_guard_sparql(self, sv, cls: ClassDefinition, flag_slot_name: str, value_slot_name: str) -> str:
        """Build a SPARQL SELECT query for the boolean-guard pattern.

        The query detects violations where the value property is present
        but the boolean flag is absent or not ``true``.

        Conforms to `SHACL §5.3.1
        <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_:
        ``$this`` is pre-bound to each focus node.
        """
        flag_uri = self._slot_uri(sv, flag_slot_name, cls)
        value_uri = self._slot_uri(sv, value_slot_name, cls)

        return (
            f"SELECT $this WHERE {{\n"
            f"    OPTIONAL {{ $this <{flag_uri}> ?flag . }}\n"
            f"    OPTIONAL {{ $this <{value_uri}> ?value . }}\n"
            f"    FILTER (\n"
            f'        ( !BOUND(?flag) || str(?flag) != "true" ) &&\n'
            f"        BOUND(?value)\n"
            f"    )\n"
            f"}}"
        )

    def _build_exclusive_value_sparql(
        self,
        sv,
        cls: ClassDefinition,
        slot_name: str,
        value_name: str,
        max_card: int,
    ) -> str | None:
        """Build a SPARQL SELECT query for the exclusive-value pattern.

        Detects violations where a specific value is present in a multivalued
        slot but the total number of values exceeds *max_card*.

        For the common case ``max_card == 1``, the query checks whether the
        exclusive value coexists with any other value (simple existence test).
        For ``max_card > 1``, a subquery counts all values and checks against
        the limit.

        The exclusive value is resolved to its full IRI via the slot's enum
        ``meaning`` field.  If the slot is not an enum or the value has no
        ``meaning``, the value is compared as a plain literal.

        Conforms to `SHACL §5.3.1
        <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_:
        ``$this`` is pre-bound to each focus node.
        """
        slot_uri = self._slot_uri(sv, slot_name, cls)
        value_ref = self._resolve_enum_value_ref(sv, slot_name, value_name)

        if max_card == 1:
            return (
                f"SELECT $this WHERE {{\n"
                f"    $this <{slot_uri}> {value_ref} .\n"
                f"    $this <{slot_uri}> ?other .\n"
                f"    FILTER (?other != {value_ref})\n"
                f"}}"
            )

        return (
            f"SELECT $this WHERE {{\n"
            f"    $this <{slot_uri}> {value_ref} .\n"
            f"    {{\n"
            f"        SELECT $this (COUNT(?val) AS ?count)\n"
            f"        WHERE {{ $this <{slot_uri}> ?val . }}\n"
            f"        GROUP BY $this\n"
            f"        HAVING (?count > {max_card})\n"
            f"    }}\n"
            f"}}"
        )

    def _resolve_enum_value_ref(self, sv, slot_name: str, value_name: str) -> str:
        """Resolve an enum value name to a SPARQL term (IRI or literal).

        Looks up the slot's range as an enum, finds the permissible value
        matching *value_name*, and returns its ``meaning`` as a full IRI
        wrapped in angle brackets.  Falls back to a quoted literal if the
        slot is not an enum or the value lacks a ``meaning``.
        """
        slot = sv.get_slot(slot_name)
        if slot:
            range_name = slot.range
            if range_name and range_name in sv.all_enums():
                enum = sv.get_enum(range_name)
                pv = enum.permissible_values.get(value_name)
                if pv and pv.meaning:
                    iri = sv.expand_curie(pv.meaning)
                    return f"<{iri}>"
        return f'"{value_name}"'

    def _slot_uri(self, sv, slot_name: str, cls: ClassDefinition) -> str:
        """Resolve a slot name to a full IRI string for use in SPARQL queries.

        Mirrors the resolution logic used for ``sh:path`` in the main slot loop:
        prefer ``sv.get_uri()`` for slots registered in the schema map, fall
        back to ``default_prefix:underscored_name``.
        """
        slot = sv.get_slot(slot_name)
        if slot and slot_name in sv.element_by_schema_map():
            return sv.get_uri(slot, expand=True)
        pfx = sv.schema.default_prefix
        return sv.expand_curie(f"{pfx}:{underscore(slot_name)}")

    def _add_class(self, func: Callable, r: ElementName) -> None:
        """Add an sh:class constraint for range class *r*.

        Skips the constraint when *r* resolves to ``linkml:Any`` — the
        LinkML meta-type representing an unconstrained range.  Emitting
        ``sh:class linkml:Any`` in SHACL output is incorrect because the
        ``linkml:Any`` class is never instantiated in real data; it would
        cause every instance to fail validation.
        """
        sv = self.schemaview
        cls = sv.get_class(r)
        if cls and getattr(cls, "class_uri", None) == "linkml:Any":
            return
        if self.use_class_uri_names:
            range_ref = sv.get_uri(r, expand=True)
        else:
            range_ref = sv.get_uri(r, expand=True, native=True)
        if range_ref == self.LINKML_ANY_URI:
            return
        func(SH["class"], URIRef(range_ref))

    def _add_enum(self, g: Graph, func: Callable, r: ElementName) -> None:
        sv = self.schemaview
        enum = sv.get_enum(r)
        pv_node = BNode()
        Collection(
            g,
            pv_node,
            [
                URIRef(sv.expand_curie(pv.meaning)) if pv.meaning else Literal(pv_name)
                for pv_name, pv in enum.permissible_values.items()
            ],
        )
        func(SH["in"], pv_node)

    # Type URIs denoting non-literal (IRI or blank-node) values.
    # SHACL §4.8.1 <https://www.w3.org/TR/shacl/#NodeKindConstraintComponent>
    # defines sh:IRI, sh:BlankNode, and sh:BlankNodeOrIRI as valid node kinds.
    # These URIs map to sh:IRI or sh:BlankNodeOrIRI constraints (never sh:Literal).
    _NON_LITERAL_TYPE_URIS = frozenset(
        {
            "xsd:anyURI",  # uri, uriorcurie → sh:IRI
            "http://www.w3.org/ns/shex#nonLiteral",  # nodeidentifier → sh:BlankNodeOrIRI
            "http://www.w3.org/ns/shex#iri",  # future-proofing → sh:IRI
        }
    )
    # IRI-only subset: uri/uriorcurie must be strict IRI references (sh:IRI),
    # while nodeidentifier (shex:nonLiteral) allows blank nodes too (sh:BlankNodeOrIRI).
    # See RDF 1.1 §3.2–3.3 <https://www.w3.org/TR/rdf11-concepts/#section-IRIs>.
    _IRI_ONLY_TYPE_URIS = frozenset(
        {
            "xsd:anyURI",
        }
    )

    def _add_type(self, func: Callable, r: ElementName) -> None:
        sv = self.schemaview
        rt = sv.get_type(r)
        type_uri = rt.uri
        expanded = sv.get_uri(rt, expand=True) if type_uri else None
        if type_uri and (type_uri in self._NON_LITERAL_TYPE_URIS or expanded in self._NON_LITERAL_TYPE_URIS):
            if type_uri in self._IRI_ONLY_TYPE_URIS:
                func(SH.nodeKind, SH.IRI)
            else:
                func(SH.nodeKind, SH.BlankNodeOrIRI)
        elif type_uri:
            func(SH.nodeKind, SH.Literal)
            func(SH.datatype, URIRef(sv.get_uri(rt, expand=True)))
            if rt.pattern:
                func(SH.pattern, Literal(rt.pattern))
            if rt.annotations and self.include_annotations:
                self._add_annotations(func, rt)
        else:
            logger.error(f"No URI for type {rt.name}")

    def _and_equals_string(self, g: Graph, func: Callable, values: list) -> None:
        pv_node = BNode()
        Collection(
            g,
            pv_node,
            [Literal(v) for v in values],
        )
        func(SH["in"], pv_node)

    def _add_subproperty_constraint(self, g: Graph, func: Callable, slot) -> None:
        """
        Add sh:in constraint from subproperty_of slot hierarchy.

        Following metamodel semantics: "any ontological child (related to X via
        an is_a relationship), is a valid value for the slot"

        :param g: RDF graph to add to
        :param func: Function to call with predicate and object
        :param slot: SlotDefinition with subproperty_of set
        """
        values = self._get_subproperty_values(slot)
        if values:
            pv_node = BNode()
            Collection(g, pv_node, values)
            func(SH["in"], pv_node)

    def _get_subproperty_values(self, slot) -> list:
        """
        Get all valid values from slot hierarchy for subproperty_of constraint.

        Values are formatted according to range type:
        - uri/uriorcurie: Returns URIRef objects with full URIs
        - string: Returns Literal objects with slot names

        :param slot: SlotDefinition with subproperty_of set
        :return: List of URIRef or Literal objects for sh:in constraint
        """
        sv = self.schemaview

        # SHACL uses full URIs for URI-like ranges
        use_uris = is_uri_range(sv, slot.range)

        # Get string values from shared utility
        # For URI ranges, get full URIs; for string ranges, get formatted names
        string_values = get_subproperty_values(sv, slot, expand_uri=True if use_uris else None)

        # Convert to RDF types
        if use_uris:
            return [URIRef(v) for v in string_values]
        else:
            return [Literal(v) for v in string_values]

    def _add_annotations(self, func: Callable, item) -> None:
        # TODO: migrate some of this logic to SchemaView
        sv = self.schemaview
        annotations = item.annotations
        # item could be a class, slot or type
        # annotation type could be dict (on types) or JsonObj (on slots)
        if type(annotations) is JsonObj:
            annotations = as_dict(annotations)
        for a in annotations.values():
            # If ':' is in the tag, treat it as a CURIE, otherwise string Literal
            if ":" in a["tag"]:
                N_predicate = URIRef(sv.expand_curie(a["tag"]))
            else:
                N_predicate = Literal(a["tag"], datatype=XSD.string)
            # If the value is a string and ':' is in the value, treat it as a CURIE,
            # otherwise treat as Literal with derived XSD datatype.
            # String annotations are language-tagged when default_language is set;
            # non-string types (bool, int, float) keep their XSD datatype.
            lang = self._resolve_language(item)
            if type(a["value"]) is extended_str and ":" in a["value"]:
                N_object = URIRef(sv.expand_curie(a["value"]))
            elif isinstance(a["value"], str) and lang:
                N_object = Literal(a["value"], lang=lang)
            else:
                N_object = Literal(a["value"], datatype=self._getXSDtype(a["value"]))

            func(N_predicate, N_object)

    def _getXSDtype(self, value):
        value_type = type(value)
        if value_type is bool:
            return XSD.boolean
        elif value_type is extended_str:
            return XSD.string
        elif value_type is extended_int:
            return XSD.integer
        elif value_type is extended_float:
            # TODO: distinguish between xsd:decimal and xsd:double?
            return XSD.decimal
        else:
            return None

    def _build_ignored_properties(self, g: Graph, c: ClassDefinition) -> BNode:
        def collect_child_properties(class_name: str, output: set) -> None:
            for childName in self.schemaview.class_children(class_name, imports=True, mixins=False, is_a=True):
                output.update(
                    {
                        URIRef(self.schemaview.get_uri(prop, expand=True))
                        for prop in self.schemaview.class_slots(childName)
                    }
                )
                collect_child_properties(childName, output)

        child_properties = set()
        collect_child_properties(c.name, child_properties)

        class_slot_uris = {
            URIRef(self.schemaview.get_uri(prop, expand=True)) for prop in self.schemaview.class_slots(c.name)
        }
        ignored_properties = child_properties.difference(class_slot_uris)

        list_node = BNode()
        ignored_properties.add(RDF.type)
        Collection(g, list_node, sorted(ignored_properties, key=str))

        return list_node


def add_simple_data_type(func: Callable, r: ElementName) -> None:
    for datatype in list(ShaclDataType):
        if datatype.linkml_type == r:
            func(SH.datatype, datatype.uri_ref)


@shared_arguments(ShaclGenerator)
@click.command(name="shacl")
@click.option(
    "--closed/--non-closed",
    default=True,
    show_default=True,
    help="Use '--closed' to generate closed SHACL shapes. Use '--non-closed' to generate open SHACL shapes.",
)
@click.option(
    "-s",
    "--suffix",
    default=None,
    show_default=True,
    help="Use --suffix to append given string to SHACL class name (e. g. --suffix Shape: Person becomes PersonShape).",
)
@click.option(
    "--include-annotations/--exclude-annotations",
    default=False,
    show_default=True,
    help="Use --include-annotations to include annotations of slots, types, and classes in the generated SHACL shapes.",
)
@click.option(
    "--exclude-imports/--include-imports",
    default=False,
    show_default=True,
    help="Use --exclude-imports to exclude imported elements from the generated SHACL shapes. This is useful when "
    "extending a substantial ontology to avoid large output files.",
)
@click.option(
    "--use-class-uri-names/--use-native-names",
    default=True,
    show_default=True,
    help="If --use-class-uri-names (default), SHACL shape names are based on class_uri. "
    "If --use-native-names, SHACL shape names are based on LinkML class names from the schema file. "
    "Suffixes from the --suffix option can still be appended.",
)
@click.option(
    "--expand-subproperty-of/--no-expand-subproperty-of",
    default=True,
    show_default=True,
    help="If --expand-subproperty-of (default), slots with subproperty_of will generate sh:in constraints "
    "containing all slot descendants. Use --no-expand-subproperty-of to disable this behavior.",
)
@click.option(
    "--default-language",
    default=None,
    show_default=True,
    help=(
        "Default BCP 47 language tag for human-readable string literals "
        "(e.g. en, de, zh-Hans).  When set, sh:name, sh:description, "
        "rdfs:label and rdfs:comment are emitted with the specified "
        "language tag."
    ),
)
@click.option(
    "--message-template",
    default=None,
    show_default=True,
    help=(
        "Template string for sh:message on each property shape. "
        "Placeholders: {name} (slot name), {title} (slot title or name), "
        "{description} (slot description), {comments} (slot comments joined with '; '), "
        "{class} (class name), {path} (fully-expanded property IRI). "
        'Example: "{name} ({class}): {description} [{comments}]"'
    ),
)
@click.option(
    "--emit-rules/--no-emit-rules",
    default=True,
    show_default=True,
    help=(
        "Emit sh:sparql constraints from LinkML rules: blocks. "
        "When enabled (default), recognised rule patterns (e.g. boolean-guard) "
        "are translated into SHACL-SPARQL constraints on the corresponding "
        "sh:NodeShape. Use --no-emit-rules to suppress rule generation."
    ),
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate SHACL turtle from a LinkML model"""
    gen = ShaclGenerator(yamlfile, **args)
    print(gen.serialize())


if __name__ == "__main__":
    cli()
