import logging
import math
import os
import re
import string
from collections.abc import Callable
from dataclasses import dataclass, fields

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
from linkml_runtime.linkml_model.meta import (
    AnonymousClassExpression,
    AnonymousSlotExpression,
    ClassDefinition,
    ClassRule,
    Element,
    ElementName,
    PresenceEnum,
    SlotDefinition,
    SlotExpression,
)
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


_PRESENT = PresenceEnum(PresenceEnum.PRESENT)
_ABSENT = PresenceEnum(PresenceEnum.ABSENT)
_UNCOMMITTED = PresenceEnum(PresenceEnum.UNCOMMITTED)


@dataclass
class _RuleSite:
    """A rule as it is translated for the shape of a class.

    *cls* is the class whose shape the rule constrains, *owner* the class
    that declares it, and *index* its 1-based position among the owner's
    rules; *cls* differs from *owner* when the rule is inherited.
    """

    cls: ClassDefinition
    owner: str
    index: int
    rule: ClassRule

    def __str__(self) -> str:
        text = f"Rule {self.index} of class {self.owner!r}"
        if self.rule.description:
            text += f" ({self.rule.description})"
        return text


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

    When ``True`` (default), rules are translated into SHACL-SPARQL
    constraints (``sh:SPARQLConstraint``) on the corresponding
    ``sh:NodeShape``.  Two patterns are recognised first:

    * *Presence implies value* — a precondition with ``value_presence: PRESENT``
      on a guard slot and a postcondition with ``equals_string`` or
      ``equals_string_in`` on a target slot holding strings (an enum, or a type
      with datatype ``xsd:string``) or booleans.  The *boolean guard* is the
      case ``equals_string: "true"`` on an ``xsd:boolean``-typed flag.
    * *Exclusive value* — a precondition with ``has_member: {equals_string: V}``
      (or a bare ``equals_string: V``) on a slot and a postcondition with
      ``maximum_cardinality`` on the *same* slot.

    Any other rule with one postcondition slot is composed from the operators
    its conditions use (presence, value comparisons, numeric bounds,
    ``range_expression``, ``has_member``).  A rule that cannot be translated
    exactly is skipped with a warning.  A class shape carries the rules of the
    class's ancestors and mixins too.

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
        # Problems with rules, collected while the rules are translated for
        # every class that has them and reported once each at the end.
        self._rule_problems: dict[tuple[str, int, str], tuple[str, list[str]]] = {}
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
                if s.minimum_cardinality is not None:
                    prop_pv_literal(SH.minCount, s.minimum_cardinality)
                elif s.exact_cardinality is not None:
                    prop_pv_literal(SH.minCount, s.exact_cardinality)
                # Identifiers map to the node's IRI rather than a property triple,
                # so there's no arc to constrain with sh:minCount 1 — emitting it
                # would cause spurious violations on every instance.
                elif s.required and not s.identifier:
                    prop_pv_literal(SH.minCount, 1)
                # maxCount
                if s.maximum_cardinality is not None:
                    prop_pv_literal(SH.maxCount, s.maximum_cardinality)
                elif s.exact_cardinality is not None:
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

        self._report_rule_problems()
        return g

    LINKML_ANY_URI = "https://w3id.org/linkml/Any"

    # -------------------------------------------------------------------
    # Rules → sh:sparql
    # -------------------------------------------------------------------

    def _add_rules(self, g: Graph, shape_uri: URIRef, cls: ClassDefinition) -> None:
        """Emit ``sh:sparql`` constraints from the LinkML ``rules`` that apply to *cls*.

        Each recognised rule is converted into an ``sh:SPARQLConstraint``
        attached to *shape_uri*.  Currently recognised patterns:

        * **Presence implies value** — a *precondition* with
          ``value_presence: PRESENT`` on a guard slot and a *postcondition*
          with ``equals_string`` or ``equals_string_in`` on a target slot.
          When the guard is present, the target must be present and hold one
          of the allowed values.  The target must hold strings (an enum, or a
          type with datatype ``xsd:string``) or booleans (``xsd:boolean``).
          The **boolean guard** is the case ``equals_string: "true"`` on a
          boolean flag.

        * **Exclusive value** — a *precondition* with ``has_member:
          {equals_string: V}`` on a slot and a *postcondition* with
          ``maximum_cardinality`` on the *same* slot.  When V is one of the
          slot's values, the slot holds at most that many values (typically 1
          for mutual exclusion).  A bare ``equals_string: V`` precondition on a
          multivalued slot is read the same way, with a warning, although the
          specification applies ``equals_string`` to all members of a
          collection.

        * **Composed** — any other rule with one postcondition slot is
          composed from the operators its conditions use: presence,
          ``equals_string(_in)`` and numeric bounds on each value, a
          ``range_expression`` on the slot's class, and ``has_member`` (see
          :meth:`_compose_rule_sparql`).

        Apart from that reading, every emitted constraint translates its rule
        exactly.  A rule that cannot be translated exactly is skipped with a
        warning naming the reason: an operator the translations do not
        support, a condition on an unknown or identifier slot, a value the
        slot's range cannot hold (see :meth:`_value_terms`), or
        ``bidirectional``.  Of a rule with ``elseconditions`` the forward
        (if/then) direction is emitted, exactly, and a warning reports the
        else branch as not enforced.

        A rule applies to "all members of this class" (metamodel ``rules``),
        so the shape of a class carries the rules of its ancestors and mixins
        as well, as it carries their slots, and as the JSON Schema generator
        applies them.  Each rule is translated in the context of *cls*, where
        ``slot_usage`` may refine a slot the rule references.

        See `W3C SHACL §5 <https://www.w3.org/TR/shacl/#sparql-constraints>`_.
        """
        sv = self.schemaview
        for owner in sv.class_ancestors(cls.name):
            for index, rule in enumerate(sv.get_class(owner).rules, start=1):
                self._add_rule(g, shape_uri, _RuleSite(cls, owner, index, rule))

    def _add_rule(self, g: Graph, shape_uri: URIRef, site: _RuleSite) -> None:
        """Emit the ``sh:SPARQLConstraint`` of the rule at *site* on *shape_uri*, unless it is skipped."""
        rule = site.rule
        if rule.deactivated:
            return
        if rule.bidirectional:
            self._skip_rule(site, "bidirectional rules are not supported")
            return
        sparql_query = self._rule_to_sparql(site)
        if sparql_query is None:
            return
        if rule.elseconditions is not None:
            self._warn_rule(
                site, "its elseconditions are not enforced; SHACL-SPARQL generation emits the if/then direction only"
            )
        message = Literal(rule.description, lang=self._resolve_language(rule)) if rule.description else None
        if self._has_sparql_constraint(g, shape_uri, Literal(sparql_query), message):
            return

        constraint = BNode()
        g.add((shape_uri, SH.sparql, constraint))
        g.add((constraint, RDF.type, SH.SPARQLConstraint))
        if message is not None:
            g.add((constraint, SH.message, message))
        g.add((constraint, SH.select, Literal(sparql_query)))

    @staticmethod
    def _has_sparql_constraint(g: Graph, shape_uri: URIRef, query: Literal, message: Literal | None) -> bool:
        """Whether the shape *shape_uri* already carries the constraint with *query* and *message*.

        Classes that share a ``class_uri`` share one shape when shapes are named
        by ``class_uri`` (the default), so a rule they all inherit would
        otherwise be added once per class and reported twice.
        """
        return any(
            (constraint, SH.select, query) in g and set(g.objects(constraint, SH.message)) == {message} - {None}
            for constraint in g.objects(shape_uri, SH.sparql)
        )

    def _warn_rule(self, site: _RuleSite, problem: str) -> None:
        """Record *problem* with the rule at *site* for the shape of ``site.cls``.

        A rule is translated once for every class that has it, declared or
        inherited, so the same problem can arise several times; it is reported
        once, by :meth:`_report_rule_problems`.
        """
        _, classes = self._rule_problems.setdefault((site.owner, site.index, problem), (str(site), []))
        if site.cls.name not in classes:
            classes.append(site.cls.name)

    def _report_rule_problems(self) -> None:
        """Log each recorded rule problem once, naming the class shapes it affects
        unless that is only the class declaring the rule."""
        for (owner, _, problem), (rule, classes) in self._rule_problems.items():
            shapes = "" if classes == [owner] else f" (in the shapes of {', '.join(map(repr, classes))})"
            logger.warning("%s: %s%s.", rule, problem, shapes)

    def _skip_rule(self, site: _RuleSite, reason: str) -> None:
        """Log that the rule at *site* is not translated, and why.

        This replaces the problems recorded so far while translating the rule
        for the shape of ``site.cls``, which describe a constraint that is not
        emitted.
        """
        for key, (_, classes) in list(self._rule_problems.items()):
            if key[:2] == (site.owner, site.index) and site.cls.name in classes:
                classes.remove(site.cls.name)
                if not classes:
                    del self._rule_problems[key]
        self._warn_rule(site, f"skipped, because {reason}")

    # Fields on a slot condition / class expression that carry no constraint
    # semantics: they never change which instances satisfy the condition, so
    # they are ignored by the operator accounting below.  Anything set on a
    # condition that is neither here nor explicitly translated by a converter
    # makes the rule untranslatable — the converters must SKIP such a rule
    # rather than emit a query that silently drops a conjunct (which would
    # widen the trigger or narrow the check: a mis-translation, not a skip).
    # Derived from the metamodel: the metadata every ``element`` carries, minus
    # anything that is a ``slot_expression`` operator.
    _NON_OPERATOR_FIELDS = frozenset(f.name for f in fields(Element)) - frozenset(
        f.name for f in fields(SlotExpression)
    )

    # The lexical space of xsd:boolean and the value each lexical form maps to
    # (XML Schema 1.1 Part 2 §3.3.2.2, <https://www.w3.org/TR/xmlschema11-2/#boolean>),
    # as SPARQL boolean literals.
    _XSD_BOOLEAN_LEXICAL = {"true": "true", "1": "true", "false": "false", "0": "false"}

    # Prefixes the reason a rule is skipped when it uses an operator, or a
    # combination of conditions, that no translation supports.
    _NO_PATTERN = (
        "its conditions match none of the translated patterns (presence implies value, exclusive value, "
        "and the compositional translation)"
    )

    @classmethod
    def _set_operator_fields(
        cls, condition: SlotDefinition | AnonymousSlotExpression | AnonymousClassExpression
    ) -> set[str]:
        """Return the names of the constraint-bearing fields actually set on a
        rule condition or class expression.

        A field counts as *set* when it is not ``None`` and not an empty
        collection (SchemaView materialises unset multivalued fields as empty
        lists / dicts).  Scalars are never judged by truthiness, so legitimate
        falsy constraints such as ``minimum_value: 0`` or
        ``equals_string: ""`` still count as set.  Metadata fields
        (:data:`_NON_OPERATOR_FIELDS`) are excluded.

        The converters compare this set against the exact operator set they
        translate and skip the rule on any mismatch, so an unrecognised (or
        future-metamodel) operator can never be silently dropped.
        """
        return {
            name
            for name, value in vars(condition).items()
            if not name.startswith("_")
            and name not in cls._NON_OPERATOR_FIELDS
            and value is not None
            and not (isinstance(value, list | dict) and not value)
        }

    def _rule_to_sparql(self, site: _RuleSite) -> str | None:
        """Translate the rule at *site* to a SPARQL SELECT query.

        Returns ``None``, after a warning naming the reason, when the rule
        matches no supported pattern exactly.  Each pattern requires its
        conditions to set **exactly** the operators it translates; a rule whose
        pre/postconditions carry anything more (extra scalar operators,
        expression-level ``any_of``/``all_of``/``none_of``/``exactly_one_of``,
        ...) is skipped rather than partially translated, since dropping a term
        would widen the precondition (false positives) or weaken the
        postcondition (false negatives).
        """
        pre, post = site.rule.preconditions, site.rule.postconditions
        if pre is None or post is None:
            self._skip_rule(site, "only rules with preconditions and postconditions are translated")
            return None
        for side, expression in (("preconditions", pre), ("postconditions", post)):
            untranslated = self._set_operator_fields(expression) - {"slot_conditions"}
            if untranslated:
                self._skip_rule(site, f"its {side} use {', '.join(sorted(untranslated))}")
                return None
            if not expression.slot_conditions:
                self._skip_rule(site, f"its {side} constrain no slot")
                return None
        if len(pre.slot_conditions) != 1 or len(post.slot_conditions) != 1:
            return self._compose_rule_sparql(site, pre.slot_conditions, post.slot_conditions)

        ((pre_name, pre_cond),) = pre.slot_conditions.items()
        ((post_name, post_cond),) = post.slot_conditions.items()
        pre_slot = self._rule_condition_slot(site, pre_name)
        post_slot = self._rule_condition_slot(site, post_name) if pre_slot is not None else None
        if pre_slot is None or post_slot is None:
            return None
        pre_ops = self._set_operator_fields(pre_cond)
        post_ops = self._set_operator_fields(post_cond)

        # Presence implies value: "if the guard is present, the target must be
        # present and hold one of the allowed values".  The boolean guard is
        # the case `equals_string: "true"` on a boolean flag.
        if (
            pre_ops == {"value_presence"}
            and pre_cond.value_presence == _PRESENT
            and post_ops in ({"equals_string"}, {"equals_string_in"})
        ):
            values = [post_cond.equals_string] if post_ops == {"equals_string"} else list(post_cond.equals_string_in)
            terms = self._value_terms(site, post_slot, values)
            if terms is None:
                return None
            return self._build_presence_implies_value_sparql(pre_slot, post_slot, terms, bool(site.rule.open_world))

        # Exclusive value: "if V is one of the values of slot X, then X has at
        # most N values".
        if post_ops == {"maximum_cardinality"} and pre_slot.name == post_slot.name:
            exclusive = self._exclusive_value(site, pre_slot, pre_cond, pre_ops)
            if exclusive is not None:
                terms = self._value_terms(site, pre_slot, [exclusive])
                if terms is None:
                    return None
                return self._build_exclusive_value_sparql(pre_slot, terms[0], int(post_cond.maximum_cardinality))

        return self._compose_rule_sparql(site, pre.slot_conditions, post.slot_conditions)

    def _exclusive_value(
        self, site: _RuleSite, slot: SlotDefinition, condition: SlotDefinition, operators: set[str]
    ) -> str | None:
        """The value V of an exclusive-value precondition on *slot*, or ``None`` if *condition* is not one.

        ``has_member: {equals_string: V}`` states "V is one of the values"
        (metamodel ``has_member``: "at least one member satisfying the
        condition").  A bare ``equals_string: V`` on a multivalued slot is read
        the same way, as the pattern always has, with a warning: the
        specification applies a slot constraint to all members of a collection
        (``05validation.md``), under which the rule would mean something else.
        Every other rule reads it that way (:meth:`_compose_rule_sparql`).
        """
        if operators == {"has_member"} and self._set_operator_fields(condition.has_member) == {"equals_string"}:
            return condition.has_member.equals_string
        if operators == {"equals_string"}:
            if slot.multivalued:
                self._warn_rule(
                    site,
                    f"its precondition equals_string on the multivalued slot {slot.name!r} is read as "
                    "'one of the values equals', which has_member: {equals_string: ...} states explicitly; "
                    "the specification applies equals_string to all members of a collection",
                )
            return condition.equals_string
        return None

    # Operators the compositional translation supports on a condition: those a
    # value is tested against, and those stating whether the slot is present or
    # some value satisfies a condition.
    _VALUE_OPERATORS = frozenset(
        {"equals_string", "equals_string_in", "minimum_value", "maximum_value", "range_expression"}
    )
    _CONDITION_OPERATORS = _VALUE_OPERATORS | {"required", "value_presence", "has_member"}

    # The datatypes SPARQL compares numerically: the numeric types and the types
    # derived from them (SPARQL 1.1 §17.1,
    # <https://www.w3.org/TR/sparql11-query/#operandDataTypes>).
    _SPARQL_NUMERIC_DATATYPES = frozenset(
        str(XSD[name])
        for name in (
            "integer",
            "decimal",
            "float",
            "double",
            "nonPositiveInteger",
            "negativeInteger",
            "long",
            "int",
            "short",
            "byte",
            "nonNegativeInteger",
            "unsignedLong",
            "unsignedInt",
            "unsignedShort",
            "unsignedByte",
            "positiveInteger",
        )
    )

    def _compose_rule_sparql(
        self, site: _RuleSite, pre: dict[str, SlotDefinition], post: dict[str, SlotDefinition]
    ) -> str | None:
        """Compose the query of a rule no named pattern matches from its slot conditions *pre* and *post*.

        The caller passes them after checking that the pre- and postconditions
        set nothing else (:meth:`_rule_to_sparql`).  Each precondition becomes
        filters on ``$this``, and the single postcondition the union of the
        ways to violate it, so the query selects the focus nodes that satisfy
        every precondition and violate the postcondition (`SHACL §5.3.1
        <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_), with
        the offending value where there is one (`SHACL §5.3.2
        <https://www.w3.org/TR/shacl/#sparql-constraints-variables>`_).

        Whether a condition requires its slot is decided by :meth:`_presence`.
        Its value operators and ``range_expression`` apply to every value of
        the slot: a slot constraint applies to all members of a collection
        (``05validation.md``), as the JSON Schema generator applies it through
        ``items``.  ``has_member`` requires some value to satisfy its
        condition.  A condition may use :data:`_CONDITION_OPERATORS`; any other
        operator skips the rule, as does an untranslatable value.
        """
        if len(post) != 1:
            self._skip_rule(site, f"{self._NO_PATTERN}, and its postconditions constrain more than one slot")
            return None
        lines: list[str] = []
        for index, (slot_name, condition) in enumerate(pre.items()):
            slot = self._rule_condition_slot(site, slot_name)
            if slot is None:
                return None
            filters = self._precondition_filters(site, slot, condition, f"?pre{index}")
            if filters is None:
                return None
            lines.extend(filters)
        ((post_name, post_cond),) = post.items()
        post_slot = self._rule_condition_slot(site, post_name)
        if post_slot is None:
            return None
        violations = self._postcondition_violations(site, post_slot, post_cond, bool(site.rule.open_world))
        if violations is None:
            return None
        if len(violations) == 1:
            lines.extend(violations)
        else:
            lines.append(f"{{ {violations[0]} }}")
            lines.extend(f"UNION {{ {violation} }}" for violation in violations[1:])
        body = "\n".join(f"    {line}" for line in lines)
        return f"SELECT DISTINCT $this (<{self._slot_iri(post_slot)}> AS ?path) ?value WHERE {{\n{body}\n}}"

    @staticmethod
    def _presence(condition: SlotDefinition, default: PresenceEnum) -> PresenceEnum:
        """Whether the rule *condition* requires its slot to be ``PRESENT``, ``ABSENT``, or neither (``UNCOMMITTED``).

        ``value_presence`` decides, then ``required``, then *default*, as the
        JSON Schema generator decides whether a rule condition requires its
        property: by default a precondition does, a postcondition unless the
        rule is ``open_world`` ("the postconditions may be omitted in instance
        data", metamodel), and an inner condition of a nested expression never.
        """
        if condition.value_presence is not None:
            return PresenceEnum(condition.value_presence)
        if condition.required is not None:
            return _PRESENT if condition.required else _UNCOMMITTED
        return default

    def _precondition_filters(
        self, site: _RuleSite, slot: SlotDefinition, condition: SlotDefinition, var: str
    ) -> list[str] | None:
        """The SPARQL filters that hold when *slot* of ``$this`` satisfies the precondition *condition*:
        the slot is present (by default) or absent as :meth:`_presence` decides, and nothing violates it."""
        checked = self._condition_violations(site, slot, condition, "$this", var, _PRESENT, "precondition")
        if checked is None:
            return None
        presence, violations = checked
        value = f"$this <{self._slot_iri(slot)}> {var} ."
        filters: list[str] = []
        if presence == _PRESENT:
            filters.append(f"FILTER EXISTS {{ {value} }}")
        elif presence == _ABSENT:
            filters.append(f"FILTER NOT EXISTS {{ {value} }}")
        return filters + [f"FILTER NOT EXISTS {{ {violation} }}" for violation in violations]

    def _postcondition_violations(
        self, site: _RuleSite, slot: SlotDefinition, condition: SlotDefinition, open_world: bool
    ) -> list[str] | None:
        """The patterns by which ``$this`` violates the postcondition *condition* on *slot*.

        A pattern matching an offending value binds it to ``?value``.  With
        *open_world* "the postconditions may be omitted in instance data"
        (metamodel ``open_world``), so the slot is not required by default.
        """
        default = _UNCOMMITTED if open_world else _PRESENT
        checked = self._condition_violations(site, slot, condition, "$this", "?value", default, "postcondition")
        if checked is None:
            return None
        presence, violations = checked
        presence_violation = self._presence_violation("$this", slot, "?value", presence)
        violations = [presence_violation, *violations] if presence_violation else violations
        if not violations:
            self._skip_rule(site, f"its postcondition on slot {slot.name!r} constrains nothing")
            return None
        return violations

    def _presence_violation(self, subject: str, slot: SlotDefinition, var: str, presence: PresenceEnum) -> str | None:
        """The pattern matching *subject* when its *slot* violates *presence*, binding *var* to a value that must
        be absent; ``None`` when *presence* is ``UNCOMMITTED``."""
        value = f"{subject} <{self._slot_iri(slot)}> {var} ."
        if presence == _PRESENT:
            return f"FILTER NOT EXISTS {{ {value} }}"
        if presence == _ABSENT:
            return value
        return None

    def _condition_violations(
        self,
        site: _RuleSite,
        slot: SlotDefinition,
        condition: SlotDefinition,
        subject: str,
        var: str,
        default: PresenceEnum,
        role: str,
    ) -> tuple[PresenceEnum, list[str]] | None:
        """The presence the *role* *condition* on *slot* of *subject* requires, and its other violations.

        A value bound to *var* violates the value operators or the
        ``range_expression`` (:meth:`_value_violations`); ``has_member`` is
        violated when the slot has values and none satisfies the member
        condition.
        """
        operators = self._set_operator_fields(condition)
        if not operators <= self._CONDITION_OPERATORS:
            self._skip_rule(site, self._unsupported(slot, operators, self._CONDITION_OPERATORS, role))
            return None
        violations = self._value_violations(site, slot, condition, subject, var)
        if violations is None:
            return None
        member_condition = condition.has_member
        if member_condition is not None:
            member_operators = self._set_operator_fields(member_condition)
            if not member_operators or not member_operators <= self._VALUE_OPERATORS:
                self._skip_rule(site, self._unsupported(slot, member_operators, self._VALUE_OPERATORS, "has_member"))
                return None
            member = f"{var}_member"
            member_violations = self._value_violations(site, slot, member_condition, subject, member)
            if member_violations is None:
                return None
            iri = self._slot_iri(slot)
            satisfied = "".join(f" FILTER NOT EXISTS {{ {violation} }}" for violation in member_violations)
            violations.append(
                f"FILTER EXISTS {{ {subject} <{iri}> {var}_any . }} "
                f"FILTER NOT EXISTS {{ {subject} <{iri}> {member} .{satisfied} }}"
            )
        return self._presence(condition, default), violations

    def _value_violations(
        self, site: _RuleSite, slot: SlotDefinition, condition: SlotDefinition, subject: str, var: str
    ) -> list[str] | None:
        """The patterns matching a value *var* of *slot* of *subject* that violates a value operator of *condition*.

        The value operators are tested on the value itself, a
        ``range_expression`` on the value's own slots
        (:meth:`_nested_violations`).
        """
        value = f"{subject} <{self._slot_iri(slot)}> {var} ."
        violations: list[str] = []
        if condition.range_expression is not None:
            nested = self._nested_violations(site, slot, condition.range_expression, var)
            if nested is None:
                return None
            violations.extend(f"{value} {violation}" for violation in nested)
        test = self._value_test(site, slot, condition, var)
        if test is None:
            return None
        if test:
            violations.append(f"{value} FILTER ( !( {test} ) )")
        return violations

    def _nested_violations(
        self, site: _RuleSite, slot: SlotDefinition, expression: AnonymousClassExpression, node: str
    ) -> list[str] | None:
        """The patterns by which an object *node*, a value of *slot*, violates the class expression *expression*.

        *expression* must consist of slot conditions on the slot's range class,
        resolved in that class's induced context.  Each one holds for an absent
        inner slot unless it requires the slot (:meth:`_presence`), as a slot
        constraint applies to the values present and as the JSON Schema
        generator reads a nested expression.  On a reference that is not
        inlined, the conditions apply to the referenced node's triples in the
        data graph.
        """
        sv = self.schemaview
        operators = self._set_operator_fields(expression)
        if operators != {"slot_conditions"}:
            self._skip_rule(
                site, self._unsupported(slot, operators, frozenset({"slot_conditions"}), "range_expression")
            )
            return None
        range_name = self._slot_range(slot)
        if range_name not in sv.all_classes():
            self._skip_rule(site, f"its range_expression is on slot {slot.name!r}, whose range is not a class")
            return None
        range_class = sv.get_class(range_name)
        violations: list[str] = []
        for index, (inner_name, condition) in enumerate(expression.slot_conditions.items()):
            inner = self._rule_condition_slot(site, inner_name, range_class)
            if inner is None:
                return None
            var = f"{node}_{index}"
            checked = self._condition_violations(site, inner, condition, node, var, _UNCOMMITTED, "inner condition")
            if checked is None:
                return None
            presence, inner_violations = checked
            presence_violation = self._presence_violation(node, inner, var, presence)
            if presence_violation:
                violations.append(presence_violation)
            violations.extend(inner_violations)
        return violations

    def _value_test(self, site: _RuleSite, slot: SlotDefinition, condition: SlotDefinition, var: str) -> str | None:
        """The SPARQL test that a value *var* of *slot* satisfies the value operators of *condition*.

        Returns ``""`` when *condition* sets no value operator, and ``None``
        (rule skipped) when a value cannot be translated.  ``equals_string``
        and ``equals_string_in`` compare as :meth:`_value_terms` renders them.
        ``minimum_value`` / ``maximum_value`` are inclusive bounds (metamodel),
        compared numerically, so the slot's datatype must be one SPARQL
        compares as a number (:data:`_SPARQL_NUMERIC_DATATYPES`).  Comparing a
        value of another type with a number is a type error (`SPARQL 1.1 §17.3
        <https://www.w3.org/TR/sparql11-query/#OperatorMapping>`_), which some
        engines resolve as an ordering anyway, so `isNumeric
        <https://www.w3.org/TR/sparql11-query/#func-isNumeric>`_ guards the
        comparison; an engine that takes an ill-typed literal such as
        ``"abc"^^xsd:integer`` for a number still compares it.  Every part is
        false, rather than an error, for a value it cannot compare (see
        :meth:`_sparql_is_one_of`).
        """
        parts: list[str] = []
        for values in (
            [condition.equals_string] if condition.equals_string is not None else None,
            list(condition.equals_string_in) if condition.equals_string_in else None,
        ):
            if values is None:
                continue
            terms = self._value_terms(site, slot, values)
            if terms is None:
                return None
            parts.append(self._sparql_is_one_of(var, terms))
        bounds = {
            name: (bound, operator)
            for name, bound, operator in (
                ("minimum_value", condition.minimum_value, ">="),
                ("maximum_value", condition.maximum_value, "<="),
            )
            if bound is not None
        }
        r = self._slot_range(slot)
        if bounds and self._type_uri(r) not in self._SPARQL_NUMERIC_DATATYPES:
            self._skip_rule(
                site,
                f"its {' and '.join(bounds)} on slot {slot.name!r} {'need' if len(bounds) > 1 else 'needs'} a type "
                "with a numeric datatype, and " + (f"the slot's range is {r!r}" if r else "the slot has no range"),
            )
            return None
        comparisons: list[str] = []
        for bound, operator in bounds.values():
            number = self._sparql_number(bound)
            if number is None:
                self._skip_rule(site, f"its bound {bound!r} on slot {slot.name!r} is not a finite number")
                return None
            comparisons.append(f"{var} {operator} {number}")
        if comparisons:
            parts.append(f"COALESCE( {' && '.join([f'isNumeric( {var} )', *comparisons])}, false )")
        return " && ".join(parts)

    @staticmethod
    def _sparql_number(value: object) -> str | None:
        """Render a ``minimum_value`` / ``maximum_value`` bound as a SPARQL numeric literal, or ``None``.

        The metamodel range of both is ``Anything``, so strings, dates,
        booleans and ``.nan`` / ``.inf`` reach the generator unchanged.
        Interpolated raw, ``"abc"`` makes the query unparsable and a date such
        as ``2020-01-01`` parses as arithmetic; only ``int`` and finite
        ``float`` values are rendered, and their ``str`` is a plain numeric
        token that SPARQL compares with numeric type promotion.
        """
        if isinstance(value, bool) or not isinstance(value, int | float):
            return None
        if isinstance(value, float) and not math.isfinite(value):
            return None
        return str(value)

    @classmethod
    def _unsupported(cls, slot: SlotDefinition, operators: set[str], supported: frozenset[str], role: str) -> str:
        """The reason a condition with *operators* in *role* on *slot* is not translated."""
        used = ", ".join(sorted(operators)) or "no operator"
        return (
            f"{cls._NO_PATTERN}; its {role} on slot {slot.name!r} uses {used}, where the compositional "
            f"translation supports only {', '.join(sorted(supported))}"
        )

    def _rule_slot(self, cls: ClassDefinition, slot_name: str) -> SlotDefinition | None:
        """Resolve a rule condition's slot key to the slot it names, or ``None``
        when no such slot exists.

        Resolution order mirrors ``sh:path`` in the main slot loop: the induced
        (class-specific) slot when the key names one of the class's slots, then
        the underscored alias form (a rule key ``my_slot`` for a slot named
        ``my slot`` — SchemaView normalises names the same way elsewhere), then
        the base slot.
        """
        sv = self.schemaview
        class_slot_names = sv.class_slots(cls.name)
        if slot_name in class_slot_names:
            return sv.induced_slot(slot_name, cls.name)
        canonical = next((s for s in class_slot_names if underscore(s) == underscore(slot_name)), None)
        if canonical is not None:
            return sv.induced_slot(canonical, cls.name)
        return sv.get_slot(slot_name)

    def _rule_condition_slot(
        self, site: _RuleSite, slot_name: str, cls: ClassDefinition | None = None
    ) -> SlotDefinition | None:
        """The slot a condition of the rule at *site* names, or ``None`` (rule skipped) when it cannot be queried.

        The slot is resolved in the context of ``site.cls``, or of *cls* for an
        inner condition on the range class of a nested expression.

        An unknown name would make the query use a predicate no shape or data
        uses.  An identifier slot is the node's IRI, not a property arc (the
        main slot loop does not require it either), so a condition on it can
        never match.
        """
        slot = self._rule_slot(cls if cls is not None else site.cls, slot_name)
        if slot is None:
            self._skip_rule(site, f"its condition names {slot_name!r}, which is not a slot")
            return None
        if slot.identifier:
            self._skip_rule(
                site, f"its condition is on the identifier slot {slot_name!r}, which is the node IRI, not a property"
            )
            return None
        return slot

    def _slot_range(self, slot: SlotDefinition) -> ElementName | None:
        """The range of *slot*, defaulting to the schema's ``default_range`` as an induced slot does."""
        return slot.range or self.schemaview.schema.default_range

    def _slot_iri(self, slot: SlotDefinition) -> str:
        """The full IRI of *slot*, exactly as ``sh:path`` in the main slot loop renders it.

        An induced slot carries its ``slot_usage`` overrides, so an overridden
        ``slot_uri`` yields the same IRI as ``sh:path``; otherwise the query
        would use a property the data never uses and never fire.
        """
        sv = self.schemaview
        if slot.name in sv.element_by_schema_map():
            return sv.get_uri(slot, expand=True)
        return sv.expand_curie(f"{sv.schema.default_prefix}:{underscore(slot.name)}")

    def _type_uri(self, r: ElementName | None) -> str | None:
        """The expanded datatype IRI of type range *r*, or ``None`` when *r* is not a type.

        Resolved through the induced type, so a type derived with ``typeof``
        inherits the ``uri`` of its ancestor.  A built-in type name in a schema
        that does not import ``linkml:types`` resolves as the main slot loop
        resolves it (:class:`ShaclDataType`).
        """
        sv = self.schemaview
        if r in sv.all_types():
            return sv.get_uri(sv.induced_type(r), expand=True)
        builtin = next((t for t in ShaclDataType if t.linkml_type == r), None)
        return str(builtin.uri_ref) if builtin is not None else None

    def _is_string_range(self, r: ElementName | None) -> bool:
        """Whether a slot with range *r* holds strings, which ``equals_string`` compares against.

        True for an enum, whose permissible values are rendered as their
        ``meaning`` IRI or as a plain literal (as :meth:`_add_enum` renders
        them); for a type whose datatype is ``xsd:string``, whose values are
        plain literals; and for no range at all, whose values are untyped and
        compared as strings, as the JSON Schema generator compares them.  A
        type with any other datatype, including one derived from ``string``
        (``xsd:anyURI``, ``xsd:token``, ...), holds typed literals or IRIs
        that a string literal does not match.
        """
        if r is None or r in self.schemaview.all_enums():
            return True
        return self._type_uri(r) == str(XSD.string)

    def _value_terms(self, site: _RuleSite, slot: SlotDefinition, values: list[str]) -> list[str] | None:
        """The SPARQL terms of the equals_string(_in) *values* on *slot*, or ``None`` (rule skipped).

        The metamodel defines both operators for slots of range ``string``.
        Enums, whose values are strings in instance data, and types with
        datatype ``xsd:string`` are treated alike (:meth:`_string_value_term`).
        A slot whose range is ``xsd:boolean``-typed holds booleans, as the
        boolean guard compares them: each value must be a lexical form of
        ``xsd:boolean`` and becomes the boolean it denotes, compared by value.
        On any other range the RDF data holds typed literals
        (``"3"^^xsd:integer``) or IRIs that no string equals, so the
        constraint would report conforming data or never fire.
        """
        r = self._slot_range(slot)
        if self._is_string_range(r):
            return [self._string_value_term(site, slot, value) for value in values]
        if self._type_uri(r) == str(XSD.boolean):
            terms = [self._XSD_BOOLEAN_LEXICAL.get(value) for value in values]
            if None not in terms:
                return terms
            self._skip_rule(
                site,
                f"equals_string(_in) on the boolean slot {slot.name!r} with {values!r}, "
                "which are not all xsd:boolean lexical forms (true, false, 1, 0)",
            )
            return None
        self._skip_rule(
            site,
            f"equals_string(_in) on slot {slot.name!r}, whose range {r!r} is neither an enum "
            "nor a type with datatype xsd:string or xsd:boolean",
        )
        return None

    def _string_value_term(self, site: _RuleSite, slot: SlotDefinition, value: str) -> str:
        """The SPARQL term of the ``equals_string`` *value* of string-valued *slot*.

        A permissible value of an enum range is rendered as :meth:`_add_enum`
        renders it, as the IRI of its ``meaning`` where it has one; anything
        else is a string literal.  A value that is not a permissible value of
        an enum with static permissible values is reported: no valid value of
        the slot can equal it.
        """
        sv = self.schemaview
        r = self._slot_range(slot)
        if r in sv.all_enums():
            permissible_values = sv.get_enum(r).permissible_values
            pv = permissible_values.get(value)
            if pv is not None and pv.meaning:
                return f"<{sv.expand_curie(pv.meaning)}>"
            if pv is None and permissible_values:
                self._warn_rule(
                    site,
                    f"it compares slot {slot.name!r} with {value!r}, which is not a permissible value of enum {r!r}",
                )
        return self._sparql_string_literal(value)

    @staticmethod
    def _sparql_string_literal(value: str) -> str:
        """Render *value* as a SPARQL expression for that string.

        The characters the grammar forbids raw are escaped (`SPARQL 1.1 §19.7
        <https://www.w3.org/TR/sparql11-query/#grammarEscapes>`_), so a value
        with a double quote, backslash or newline neither breaks the
        ``sh:select`` query nor injects into it.  Codepoint escapes are replaced
        before parsing (`§19.2 <https://www.w3.org/TR/sparql11-query/#codepointEscape>`_),
        so an escaped backslash followed by ``u`` / ``U`` would be read as one:
        the literal is split there and rejoined with ``CONCAT``.
        """
        escaped = (
            str(value)
            .replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
        )
        parts = re.split(r"(?<=\\)(?=[uU])", escaped)
        if len(parts) == 1:
            return f'"{escaped}"'
        return "CONCAT(" + ", ".join(f'"{part}"' for part in parts) + ")"

    @staticmethod
    def _sparql_is_one_of(var: str, terms: list[str]) -> str:
        """A SPARQL expression that is true when *var* equals one of *terms*, and false otherwise.

        The test is spelled out as ``var = t1 || var = t2 || ...``, which is how
        `SPARQL 1.1 §17.4.1.9 <https://www.w3.org/TR/sparql11-query/#func-in>`_
        defines ``IN``.  The ``=`` operator compares values, so a plain literal
        also matches its RDF 1.1-identical ``xsd:string`` form (`RDF 1.1
        Concepts §3.3 <https://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal>`_),
        which JSON-LD produces under ``"@type": "xsd:string"`` coercion; some
        engines, rdflib among them, match ``IN`` and triple-pattern constants by
        term identity and miss that form.  ``COALESCE`` (§17.4.1.3) turns the
        type error that ``RDFterm-equal`` (§17.4.1.7) raises for incomparable
        literals into false: such a value equals none of *terms*, and an
        unguarded error would drop the row and hide the violation.  An unbound
        *var* is false as well.
        """
        disjunction = " || ".join(f"{var} = {term}" for term in terms)
        return f"COALESCE( {disjunction}, false )"

    def _build_presence_implies_value_sparql(
        self, guard: SlotDefinition, target: SlotDefinition, terms: list[str], open_world: bool
    ) -> str:
        """Build the SPARQL SELECT query of the presence-implies-value pattern.

        A focus node violates the rule when the *guard* slot is present and the
        *target* slot is absent or holds a value that equals none of the SPARQL
        *terms* (see :meth:`_sparql_is_one_of`).  The boolean guard is this
        pattern with the boolean ``true`` as the only term.  With *open_world*,
        "the postconditions may be omitted in instance data" (metamodel
        ``open_world``), so an absent target is no violation.

        Conforms to `SHACL §5.3.1
        <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_ (``$this``
        is pre-bound to each focus node) and projects ``?path`` and ``?value``
        as result variables (`§5.3.2
        <https://www.w3.org/TR/shacl/#sparql-constraints-variables>`_), so each
        result names the target property and the offending value.
        """
        guard_iri = self._slot_iri(guard)
        target_iri = self._slot_iri(target)
        is_allowed = self._sparql_is_one_of("?value", terms)
        if open_world:
            target_pattern = f"$this <{target_iri}> ?value ."
            violation = f"!{is_allowed}"
        else:
            target_pattern = f"OPTIONAL {{ $this <{target_iri}> ?value . }}"
            violation = f"!BOUND(?value) || !{is_allowed}"
        return (
            f"SELECT DISTINCT $this (<{target_iri}> AS ?path) ?value WHERE {{\n"
            f"    $this <{guard_iri}> ?guard .\n"
            f"    {target_pattern}\n"
            f"    FILTER ( {violation} )\n"
            f"}}"
        )

    def _build_exclusive_value_sparql(self, slot: SlotDefinition, term: str, max_card: int) -> str:
        """Build the SPARQL SELECT query of the exclusive-value pattern.

        A focus node violates the rule when *slot* holds a value equal to the
        SPARQL *term* (see :meth:`_sparql_is_one_of`) and more than *max_card*
        values in total.  For ``max_card == 1`` the query reports each other
        value that coexists with the exclusive one.  For ``max_card > 1`` a
        subquery counts all values, testing ``HAVING`` on the ``COUNT``
        aggregate itself: expressions projected by ``SELECT`` are not visible
        to ``HAVING`` (`SPARQL 1.1 §18.2.4.2
        <https://www.w3.org/TR/sparql11-query/#sparqlHavingClause>`_), so a
        projected alias would be unbound there and the constraint never fire.

        Conforms to `SHACL §5.3.1
        <https://www.w3.org/TR/shacl/#sparql-constraints-prebound>`_ and
        projects ``?path`` (and, for ``max_card == 1``, the coexisting value as
        ``?value``) as result variables (`§5.3.2
        <https://www.w3.org/TR/shacl/#sparql-constraints-variables>`_).
        """
        iri = self._slot_iri(slot)
        is_exclusive = self._sparql_is_one_of("?exclusive", [term])
        if max_card == 1:
            is_other_exclusive = self._sparql_is_one_of("?other", [term])
            return (
                f"SELECT DISTINCT $this (<{iri}> AS ?path) (?other AS ?value) WHERE {{\n"
                f"    $this <{iri}> ?exclusive .\n"
                f"    $this <{iri}> ?other .\n"
                f"    FILTER ( {is_exclusive} && !{is_other_exclusive} )\n"
                f"}}"
            )
        return (
            f"SELECT DISTINCT $this (<{iri}> AS ?path) WHERE {{\n"
            f"    $this <{iri}> ?exclusive .\n"
            f"    FILTER ( {is_exclusive} )\n"
            f"    {{\n"
            f"        SELECT $this\n"
            f"        WHERE {{ $this <{iri}> ?item . }}\n"
            f"        GROUP BY $this\n"
            f"        HAVING ( COUNT(?item) > {max_card} )\n"
            f"    }}\n"
            f"}}"
        )

    def _add_class(self, func: Callable, r: ElementName) -> None:
        """Add a class/shape constraint for range class *r*.

        Skips the constraint when *r* resolves to ``linkml:Any`` — the
        LinkML meta-type representing an unconstrained range.

        In default mode (``use_class_uri_names=True``): emits ``sh:class <class_uri>``
        so validators check the RDF type hierarchy.

        In native names mode (``use_class_uri_names=False``): emits ``sh:node <native_shape_uri>``
        instead of ``sh:class``.  Using ``sh:class`` with a native shape URI (e.g.
        ``dcatapplus:Resource``) is incorrect because data nodes are never typed as
        that URI — it is a shape identifier, not an RDF class.  ``sh:node`` correctly
        validates the referenced node against the named shape.

        Because ``sh:node`` references a shape by its identifier, the ``suffix``
        option has to be applied here too — otherwise the reference points at a
        shape that was never emitted and the constraint silently passes.
        """
        sv = self.schemaview
        cls = sv.get_class(r)
        if cls and getattr(cls, "class_uri", None) == "linkml:Any":
            return
        range_ref = sv.get_uri(r, expand=True, native=not self.use_class_uri_names)
        if range_ref == self.LINKML_ANY_URI:
            return
        if self.use_class_uri_names:
            func(SH["class"], URIRef(range_ref))
            return
        if self.suffix:
            range_ref += self.suffix
        func(SH["node"], URIRef(range_ref))

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
        # Types can inherit URI and pattern constraints.
        rt = sv.induced_type(r)
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
        "When enabled (default), recognised rule patterns (boolean-guard, "
        "presence-implies-value, exclusive-value) are translated into "
        "SHACL-SPARQL constraints on the corresponding "
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
