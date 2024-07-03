"""
A model transformer that transforms a schema into logical form with inheritance remaoved.

Formally, this transformer generates a logical model of the schema in which inheritance
of slots/attributes is replaced by boolean conjunctions.

For example, given a slot s and two classes C and D, where C is_a D. If both C and D
place constraints on s (for example, C may refine the range, or make more restricted
value constraints), then an attribute is generated for C that for which the conjunction
of constraints in both classes hold.

These logical constraints are then simplified by translating to disjunctive normal form,
and applying simplification rules.
"""

import logging
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, List, Union

from linkml_runtime.dumpers import json_dumper
from linkml_runtime.linkml_model import ClassDefinitionName, SchemaDefinition
from linkml_runtime.linkml_model.meta import (
    AnonymousSlotExpression,
    AnonymousTypeExpression,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
)

from linkml.transformers.model_transformer import ModelTransformer
from linkml.utils import logictools

HERITABLE_METASLOT = [
    # "multivalued",
    "range",
    "range_expression",
    "minimum_value",
    "maximum_value",
    "pattern",
    "structured_pattern",
    "required",
    "recommended",
    "inlined",
    "inlined_as_list",
    "all_of",
    "exactly_one_of",
    "none_of",
    "any_of",
    "unit",
    "value_presence",
    "equals_string",
    "equals_string_in",
    "equals_number",
    "equals_expression",
    "has_member",
    "all_members",
]
"""Metamodel slots that can be rolled down or inherited"""

DIRECT_ROLL_DOWN = ["multivalued", "key", "identifier", "designates_type"]
"""Additional slots that can be rolled down, but only if they are on a SlotDefinition, not a slot expression"""

HERITABLE_TYPE_METASLOT = [
    "minimum_value",
    "maximum_value",
    "pattern",
    "structured_pattern",
    "all_of",
    "exactly_one_of",
    "none_of",
    "any_of",
    "unit",
    "repr",
]

MATCHES_PREDICATE = "matches"

logger = logging.getLogger(__name__)


class UnsatisfiableAttribute(ValueError):
    """The attribute specifies constraints that cannot be satisfied"""

    pass


@dataclass
class LogicalModelTransformer(ModelTransformer):
    """
    Flatten a schema by rolling down slots and attributes to subclasses.

    The primary application of this is as an intermediate product to be used in generators.
    For example, when compiling LinkML to frameworks that either lack inheritance (e.g. JSON-Schema),
    or only partially support inheritance (e.g. single inheritance), this transformer can be used
    to generate a schema with attributes that are as complete as possible within that framework.

    To demonstrate, consider a simple schema with a class Person inheriting from Thing:

    >>> from linkml.utils.schema_builder import SchemaBuilder
    >>> sb = SchemaBuilder()
    >>> _ = sb.add_class("Thing", slots=["id", "name"])
    >>> _ = sb.add_class("Person", slots={"age": {"range": "integer"}}, is_a="Thing")
    >>> _ = sb.add_class("Organization", slots={"category": {"range": "OrganizationType"}}, is_a="Thing")
    >>> _ = sb.add_enum("OrganizationType", ["commercial", "non-profit"])
    >>> from linkml.transformers.logical_model_transformer import LogicalModelTransformer
    >>> tr = LogicalModelTransformer()
    >>> tr.set_schema(sb.schema)
    >>> flat_schema = tr.transform()
    >>> from linkml_runtime.dumpers import yaml_dumper
    >>> print(yaml_dumper.dumps(flat_schema.classes['Person']))
    name: Person
    attributes:
      id:
        name: id
      name:
        name: name
      age:
        name: age
        range: integer

    ...

    Note that the id and name attributes have been rolled down from Thing to Person.

    This transformer will translate range assertions into any_of assertions, where the class
    hierarchy is rolled up:

    >>> _ = sb.add_class("Container", slots={"entities": {"range": "Thing", "multivalued": True}})
    >>> tr.set_schema(sb.schema)
    >>> flat_schema = tr.transform()
    >>> print(yaml_dumper.dumps(flat_schema.classes['Container']))
    name: Container
    attributes:
      entities:
        name: entities
        multivalued: true
        any_of:
        - range: Organization
        - range: Person
        - range: Thing

    ...

    If you are compiling to a framework that does have inheritance, then you can specify that these are
    preserved:

    >>> tr_inh = LogicalModelTransformer(preserve_class_mixins=True, preserve_class_is_a=True)
    >>> tr_inh.set_schema(sb.schema)
    >>> flat_schema = tr_inh.transform()
    >>> print(yaml_dumper.dumps(flat_schema.classes['Container']))
    name: Container
    from_schema: http://example.org/test-schema
    attributes:
      entities:
        name: entities
        range: Thing
        multivalued: true

    ...

    You can also use any_of directly in the schema:

    >>> _ = sb.add_class("Container2", slots={"entities2": {"multivalued": True,
    ...                                                     "any_of": [{"range": "Person"},
    ...                                                                {"range": "Organization"}]}})
    >>> tr.set_schema(sb.schema)
    >>> flat_schema = tr.transform()
    >>> print(yaml_dumper.dumps(flat_schema.classes['Container2']))
    name: Container2
    attributes:
      entities2:
        name: entities2
        multivalued: true
        any_of:
    ...

    Note that defaults are always applied after reasoning. So if you set a default_range to
    be string, and use inheritance preservation, the unfolded range expression is still
    correct:

    >>> sb.schema.default_range = "string"
    >>> tr_inh.set_schema(sb.schema)
    >>> flat_schema = tr_inh.transform()
    >>> print(yaml_dumper.dumps(flat_schema.classes['Container2']))
    name: Container2
    from_schema: http://example.org/test-schema
    attributes:
      entities2:
        name: entities2
        multivalued: true
        any_of:
        - range: Organization
        - range: Person


    When compiling to a framework that does not support inheritance, such as JSON Schema, the any_of expression
    can be directly translated to the same construct in JSON-Schema.

    This transformer will also perform reasoning on the schema, to provide the simplest complete form. Let's add
    some constraints onto the "age" slot and create a subclass of Person with a constrained age range:

    >>> sb.schema.slots["age"].minimum_value = 0
    >>> sb.schema.slots["age"].maximum_value = 200
    >>> _ = sb.add_class("MiddleAged", slot_usage={"age": {"minimum_value": 40, "maximum_value": 60}}, is_a="Person")
    >>> tr.set_schema(sb.schema)
    >>> flat_schema = tr.transform()
    >>> print(yaml_dumper.dumps(flat_schema.classes['MiddleAged'].attributes['age']))
    name: age
    range: integer
    minimum_value: 40
    maximum_value: 60

    The reasoning engine can also detect unsatisfiable constraints:

    >>> from linkml.transformers.logical_model_transformer import UnsatisfiableAttribute
    >>> _ = sb.add_class("YoungAdult", slot_usage={"age": {"minimum_value": 40, "maximum_value": 10}}, is_a="Person")
    >>> tr.set_schema(sb.schema)
    >>> try:
    ...   flat_schema = tr.transform()
    ... except UnsatisfiableAttribute as e:
    ...   print(e)
    <BLANKLINE>
    Attribute YoungAdult.age is unsatisfiable
    <BLANKLINE>

    Let's get rid of the problematic class:

    >>> del sb.schema.classes["YoungAdult"]
    >>> _ = sb.add_class("Person2", is_a="Person", slot_usage={"age": {"range": "string"}})
    >>> tr.set_schema(sb.schema)
    >>> try:
    ...   flat_schema = tr.transform()
    ... except UnsatisfiableAttribute as e:
    ...   print(e)
    <BLANKLINE>
    Attribute Person2.age is unsatisfiable
    <BLANKLINE>



    """

    preserve_class_is_a: bool = False
    """
    If True, preserve the is_a hierarchy in the flattened schema, and assume that entailments
    will hold in the transformed schema. If False, the is_a hierarchy will be flattened.
    """

    preserve_class_mixins: bool = False
    """
    If True, preserve the mixin hierarchy in the flattened schema, and assume that entailments
    will hold in the transformed schema. If False, the mixin hierarchy will be flattened.
    """

    preserve_type_is_a: bool = False
    """
    If True, preserve the is_a hierarchy in the flattened schema, and assume that entailments
    will hold in the transformed schema. If False, the is_a hierarchy will be flattened.
    """

    tidy_slots: bool = True
    """
    If True, remove all standalone slots from transformed schema. These will have been rolled
    up into class attributes.
    """

    tidy_inheritance: bool = True
    """
    If True, remove all inheritance from transformed schema. These will have been rolled
    up into class attributes.
    """

    tidy_default_range: bool = True
    """
    If True, remove the fake "Any" class from the transformed schema. This will be implicit based on
    a lack of range assignment.
    """

    def transform(self, tgt_schema_name: str = None, simplify=True, **kwargs) -> Any:
        """
        Transform the schema to a logical model, translating inheritance to boolean expressions.

        :param tgt_schema_name:
        :param simplify: If True (default), simplify the schema after transformation
        :return:
        """
        sv = self.schemaview
        target_schema = deepcopy(self.source_schema)
        for tn, typ in target_schema.types.items():
            ancs = sv.type_ancestors(tn, reflexive=False)
            logging.debug(f"Unrolling type {tn}, merging {len(ancs)}")
            if ancs:
                for type_anc in ancs:
                    self._merge_type_ancestors(target=typ, source=sv.get_type(type_anc))
        for sn, slot in target_schema.slots.items():
            ancs = sv.slot_ancestors(sn, reflexive=False)
            logging.debug(f"Unrolling slot {sn}, merging {len(ancs)}")
            if ancs:
                for slot_anc in ancs:
                    self._merge_slot_ancestors(target=slot, source=target_schema.slots[slot_anc])
        for cn, cls in target_schema.classes.items():
            ancs = sv.class_ancestors(
                cn,
                reflexive=True,
                is_a=not self.preserve_class_is_a,
                mixins=not self.preserve_class_mixins,
                depth_first=False,
            )
            ancs = list(reversed(ancs))
            logging.debug(f"Unrolling class {cn}, merging {len(ancs)}")
            self._roll_down(target_schema, cn, ancs)
        self.apply_defaults(target_schema)
        if simplify:
            self.simplify(target_schema)
        if self.tidy_slots:
            target_schema.slots = {}
        if self.tidy_inheritance:
            for c in target_schema.classes.values():
                if not self.preserve_class_is_a:
                    c.is_a = None
                if not self.preserve_class_mixins:
                    c.mixins = []
            if not self.preserve_type_is_a:
                for t in target_schema.types.values():
                    t.is_a = None
        if self.tidy_default_range:
            target_schema.default_range = None
            any_proxy_classes = [c for c in target_schema.classes.values() if c.class_uri == "linkml:Any"]
            if any_proxy_classes:
                for c in any_proxy_classes:
                    del target_schema.classes[c.name]
        return target_schema

    def _roll_down(
        self,
        target_schema: SchemaDefinition,
        target_class_name: ClassDefinitionName,
        ancestors: List[ClassDefinitionName],
    ):
        anc_classes = [self.schemaview.get_class(anc) for anc in ancestors]
        attributes: Dict[SlotDefinitionName, SlotDefinition] = {}
        for anc in anc_classes:
            top_level_slots = [(s, target_schema.slots[s]) for s in anc.slots]
            for slot_name, slot_expr in list(anc.attributes.items()) + list(anc.slot_usage.items()) + top_level_slots:
                if slot_name not in attributes:
                    attributes[slot_name] = SlotDefinition(slot_name)
                sx = attributes[slot_name]
                self._merge_slot_ancestors(target=sx, source=slot_expr)
        tgt_cls = target_schema.classes[target_class_name]
        for k, v in attributes.items():
            tgt_cls.attributes[k] = v
        tgt_cls.slots = []
        tgt_cls.slot_usage = {}

    def _merge_slot_ancestors(
        self,
        target: Union[AnonymousSlotExpression, SlotDefinition],
        source: Union[SlotDefinition, AnonymousSlotExpression],
    ):
        """
        Generate all_ofs for slot based on ancestors.

        :param target:
        :param source:
        :return:
        """
        new_slot_dict = {}
        for p in HERITABLE_METASLOT:
            pv = getattr(source, p)
            if pv is not None and pv != [] and pv != {} and pv is not False:
                new_slot_dict[p] = pv
        for p in DIRECT_ROLL_DOWN:
            pv = getattr(source, p, None)
            if pv is not None and pv != [] and pv != {} and pv is not False:
                setattr(target, p, pv)
        sv = self.schemaview
        if source.range in sv.all_types():
            typ = sv.get_type(source.range)
            for p in set(HERITABLE_TYPE_METASLOT).intersection(HERITABLE_METASLOT):
                pv = getattr(typ, p)
                if pv is not None and pv != [] and pv != {} and pv is not False:
                    new_slot_dict[p] = pv
        if new_slot_dict:
            target.all_of.append(AnonymousSlotExpression(**new_slot_dict))

    @staticmethod
    def _merge_type_ancestors(target: TypeDefinition, source: TypeDefinition):
        """
        Generate all_ofs for type based on ancestors.

        :param target:
        :param source:
        :return:
        """
        new_slot_dict = {}
        for p in HERITABLE_TYPE_METASLOT:
            pv = getattr(source, p)
            if pv is not None and pv != [] and pv != {} and pv is not False:
                new_slot_dict[p] = pv
        if new_slot_dict:
            target.all_of.append(AnonymousTypeExpression(**new_slot_dict))

    def apply_defaults(self, target_schema: SchemaDefinition):
        """
        Apply defaults to the schema

        :param target_schema:
        :return:
        """
        for cls in target_schema.classes.values():
            for att in cls.attributes.values():
                self._apply_defaults_to_attribute(att)

    def _apply_defaults_to_attribute(self, att: SlotDefinition):
        if not att.range:
            if not any(self._collection_slot_expressions(att, lambda sx: sx.range)):
                att.range = self.schemaview.schema.default_range

    def _collection_slot_expressions(
        self, att: Union[SlotDefinition, AnonymousSlotExpression], filter_function: Callable
    ) -> Iterator[AnonymousSlotExpression]:
        """
        Traverse nested slot expressions yielding those that match the filter function.

        :param att:
        :return:
        """
        if filter_function(att):
            yield att
        for sx in att.all_of + att.exactly_one_of + att.none_of + att.any_of:
            yield from self._collection_slot_expressions(sx, filter_function)

    def simplify(self, target_schema: SchemaDefinition):
        for cls in target_schema.classes.values():
            for att in cls.attributes.values():
                x = self._as_logical_expression(att)
                logger.debug(f"Translating {cls.name}.{att.name} ==> {x}")
                x = logictools.simplify_full(x)
                logger.debug(f"Simplified: {x}")
                if logictools.is_contradiction(x):
                    raise UnsatisfiableAttribute(f"Attribute {cls.name}.{att.name} is unsatisfiable")
                self._simplify_member_ofs(x)
                logger.debug(f"Simplified member of: {x}")
                simplified_att = self._from_logical_expression(x)
                for k, v in simplified_att.__dict__.items():
                    if v is None or v is False:
                        if k in ["multivalued"]:
                            continue
                    setattr(att, k, v)

    def _simplify_member_ofs(self, expr: logictools.Expression):
        if isinstance(expr, logictools.Term) and expr.predicate == "in":
            elements = expr.operands[1]
            if elements == logictools.UniversalSet():
                pass
            else:
                expr.operands[1] = self._remove_redundant(elements)
        elif isinstance(expr, logictools.And):
            [self._simplify_member_ofs(o) for o in expr.operands]
        elif isinstance(expr, logictools.Or):
            [self._simplify_member_ofs(o) for o in expr.operands]
        elif isinstance(expr, logictools.Not):
            self._simplify_member_ofs(expr.operand)

    def _remove_redundant(self, elements: List[str]) -> List[str]:
        sv = self.schemaview
        redundant = set()
        if not self.preserve_class_mixins:
            redundant.update([c.name for c in sv.all_classes().values() if c.mixin])
            if not self.preserve_class_is_a:
                redundant.update([c.name for c in sv.all_classes().values() if c.abstract])
        for x in elements:
            if x in sv.all_classes():
                redundant.update(
                    sv.class_descendants(
                        x,
                        reflexive=False,
                        is_a=self.preserve_class_is_a,
                        mixins=self.preserve_class_mixins,
                    )
                )
            elif x in sv.all_types():
                redundant.update(self._type_descendants(x, reflexive=False))
            elif x in sv.all_enums():
                redundant.update(self._enum_descendants(x, reflexive=False))
            else:
                logger.warning(f"Unknown class {x} in {elements}")
        return [x for x in elements if x not in redundant]

    def _type_descendants(self, type_name: str, imports=True, reflexive=True, depth_first=True) -> List[str]:
        # TODO: move this to schemaview
        sv = self.schemaview
        from linkml_runtime.utils.schemaview import _closure

        def type_children(type_name, imports=True):
            elts = [sv.get_type(x) for x in sv.all_types(imports)]
            return [x.name for x in elts if x.typeof == type_name]

        return _closure(
            lambda x: type_children(x, imports=imports),
            type_name,
            reflexive=reflexive,
            depth_first=depth_first,
        )

    def _enum_descendants(self, enum_name: str, imports=True, reflexive=True, depth_first=True) -> List[str]:
        # TODO: move this to schemaview
        sv = self.schemaview
        from linkml_runtime.utils.schemaview import _closure

        def enum_children(enum_name, imports=True):
            elts = [sv.get_enum(x) for x in sv.all_enums(imports)]
            return [x.name for x in elts if x.is_a == enum_name]

        return _closure(
            lambda x: enum_children(x, imports=imports),
            enum_name,
            reflexive=reflexive,
            depth_first=depth_first,
        )

    @property
    def _value_var(self) -> logictools.Variable:
        return logictools.Variable("value")

    @property
    def _type_var(self) -> logictools.Variable:
        return logictools.Variable("type")

    def _as_logical_expression(
        self, slot_expression: Union[SlotDefinition, AnonymousSlotExpression]
    ) -> logictools.Expression:
        sv = self.schemaview
        exprs = []
        value_var = self._value_var
        type_var = self._type_var
        if slot_expression.minimum_value is not None:
            exprs.append(value_var >= slot_expression.minimum_value)
        if slot_expression.maximum_value is not None:
            exprs.append(value_var <= slot_expression.maximum_value)
        if slot_expression.pattern is not None:
            exprs.append(logictools.Term(MATCHES_PREDICATE, value_var, slot_expression.pattern))
        if slot_expression.range:
            rn = slot_expression.range
            if slot_expression.range in sv.all_classes():
                rn_cls = sv.get_class(rn)
                if rn_cls.class_uri == "linkml:Any":
                    elts = logictools.UniversalSet()
                else:
                    elts = sv.class_descendants(rn, reflexive=True)
            elif slot_expression.range in sv.all_types():
                elts = self._type_descendants(rn, reflexive=True)
            else:
                elts = [rn]
            exprs.append(logictools.IsIn(type_var, elts))
        if slot_expression.all_of:
            exprs.append(logictools.And(*[self._as_logical_expression(subx) for subx in slot_expression.all_of]))
        if slot_expression.exactly_one_of:
            # TODO: disjointness
            exprs.append(logictools.Or(*[self._as_logical_expression(subx) for subx in slot_expression.exactly_one_of]))
        if slot_expression.none_of:
            exprs.append(
                logictools.Not(logictools.Or(*[self._as_logical_expression(subx) for subx in slot_expression.none_of]))
            )
        if slot_expression.any_of:
            exprs.append(logictools.Or(*[self._as_logical_expression(subx) for subx in slot_expression.any_of]))
        for p in HERITABLE_METASLOT:
            if p in [
                "range",
                "pattern",
                "minimum_value",
                "maximum_value",
                "all_of",
                "exactly_one_of",
                "none_of",
                "any_of",
            ]:
                continue
            v = getattr(slot_expression, p, None)
            if v is not None and v != [] and v != {}:
                exprs.append(logictools.Eq(p, v))
        return logictools.And(*exprs)

    def _from_logical_expression(self, expr: logictools.Expression) -> AnonymousSlotExpression:
        if isinstance(expr, logictools.And):
            all_of = [self._from_logical_expression(e) for e in expr.operands]
            if len(all_of) == 1:
                return all_of[0]
            x = json_dumper.to_dict(all_of[0])
            remaining_all_of = []
            for y in all_of[1:]:
                y = json_dumper.to_dict(y)
                if set(x.keys()).intersection(set(y.keys())):
                    remaining_all_of.append(AnonymousSlotExpression(**y))
                else:
                    x.update(y)
            ase = AnonymousSlotExpression(**x)
            ase.all_of.extend(remaining_all_of)
            return ase
        elif isinstance(expr, logictools.Or):
            return AnonymousSlotExpression(any_of=[self._from_logical_expression(e) for e in expr.operands])
        elif isinstance(expr, logictools.Not):
            return AnonymousSlotExpression(none_of=[self._from_logical_expression(expr.operand)])
        elif isinstance(expr, logictools.Eq):
            var = expr.lhs
            val = expr.rhs
            return AnonymousSlotExpression(**{var: val})
        # elif isinstance(expr, logictools.IsIn):
        #    return AnonymousSlotExpression(range=expr.operands[1])
        elif isinstance(expr, logictools.Term):
            var = expr.operands[0]
            val = expr.operands[1]
            if var == self._value_var:
                if expr.predicate == MATCHES_PREDICATE:
                    return AnonymousSlotExpression(pattern=val)
                elif expr.predicate == ">=":
                    return AnonymousSlotExpression(minimum_value=val)
                elif expr.predicate == ">":
                    return AnonymousSlotExpression(minimum_value=val + 1)
                elif expr.predicate == "<=":
                    return AnonymousSlotExpression(maximum_value=val)
                elif expr.predicate == "<":
                    return AnonymousSlotExpression(maximum_value=val - 1)
                else:
                    raise ValueError(f"Unknown predicate {expr.predicate} for {var}")
            elif var == self._type_var:
                if expr.predicate == "in":
                    if val == logictools.UniversalSet():
                        return AnonymousSlotExpression(range="Any")
                    elif len(val) == 1:
                        return AnonymousSlotExpression(range=val[0])
                    else:
                        return AnonymousSlotExpression(any_of=[AnonymousSlotExpression(range=v) for v in sorted(val)])
                else:
                    raise ValueError(f"Unknown predicate {expr.predicate} for {var}")
            else:
                raise ValueError(f"Unknown variable {var}")
        return AnonymousSlotExpression()

    def attribute_as_python_field(self, attribute: SlotDefinition) -> str:
        """
        Return a Python field declaration for the given attribute.

        Note: this method may move to pydanticgen, it is currently here for demonstration purposes.

        :param attribute:
        :return:
        """
        return f"{attribute.name}: {self._att_as_python_expression(attribute)}"

    def _att_as_python_expression(
        self,
        attribute: Union[SlotDefinition, AnonymousSlotExpression],
        root_slot: SlotDefinition = None,
        stack: List = None,
    ) -> str:
        # Note: in future versions of the metamodel, multivalued may move to the expression
        if stack is None:
            stack = [attribute]
        if root_slot is None:
            if isinstance(attribute, SlotDefinition):
                root_slot = attribute
            else:
                raise ValueError(f"root_slot must be provided for {attribute}")
        multivalued = root_slot.multivalued
        s = ""
        if attribute.any_of:
            union_terms = [self._att_as_python_expression(x, root_slot, stack + [x]) for x in attribute.any_of]
            s = f"Union[{', '.join(union_terms)}]"
        else:
            if attribute.range:
                s = attribute.range
            else:
                s = "Any"
            if not attribute.required:
                s = f"Optional[{s}]"
            if multivalued:
                if attribute.inlined and not attribute.inlined_as_list:
                    s = f'Dict["str", {s}]'
                else:
                    # TODO: ref by key
                    s = f"Collection[{s}]"
        return s
