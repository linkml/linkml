import logging
from dataclasses import dataclass
from typing import Set, List, Union

from linkml_runtime.utils.schemaview import SchemaView, CLASS_NAME
from linkml_runtime.linkml_model.meta import SchemaDefinition, ClassDefinition, SlotDefinition, Expression, \
    ClassExpression, ClassDefinitionName, ClassRule, AnonymousClassExpression, SlotExpression, SlotDefinitionName


class AtomicClassExpression:
    """
    aka literal (https://en.wikipedia.org/wiki/Literal_(mathematical_logic))
    """
    expression: ClassExpression
    negated: bool

    def __str__(self):
        if self.negated:
            return f'NOT {self.expression}'
        else:
            return str(self.expression)

class ClassExpressionConjunction:
    """
    conjunction of class literals
    """
    operands: AtomicClassExpression

    def __str__(self):
        return ' AND '.join([str(op) for op in self.operands])

@dataclass
class DisjunctiveNormalFormClassExpression:
    """
    A boolean combination of class expressions in Disjunctive Normal Form
    """
    operands: List[ClassExpressionConjunction]

    def __str__(self):
        return ' OR '.join([str(op) for op in self.operands])


def get_range_as_disjunction(slot: SlotExpression) ->  Set[ClassDefinitionName]:
    """
    translate the range of a slot as defined by both range expressions and direct
    named class ranges to a disjunctive expression

    :param slot:
    :return:
    """
    conjs = []
    if slot.any_of or slot.exactly_one_of:
        disj = set()
        for s in slot.any_of + slot.exactly_one_of:
            disj.update(get_range_as_disjunction(s))
        conjs.append(disj)
    if slot.range_expression:
        if isinstance(slot.range_expression, ClassExpression):
            conjs.append(get_disjunction(slot.range_expression))
        else:
            logging.warning(f'Expected range_expression for {slot.name} to be a class expression, not {type(slot.range_expression)}')
    if len(conjs) == 0:
        if slot.range:
            conjs.append({slot.range})
        else:
            logging.warning(f'No range for {slot}')
    if len(conjs) > 1:
        raise Exception(f'Cannot determine range disjunction for {slot}, got conjunctions: {conjs}')
    if len(conjs) == 0:
        return None
    else:
        return conjs[0]


def get_disjunction(cx: ClassExpression) -> Set[ClassDefinitionName]:
    disj = set()
    if cx.is_a:
        disj.add(cx.is_a)
    for arg in cx.any_of + cx.exactly_one_of:
        if isinstance(arg, ClassExpression):
            disj.update(get_disjunction(arg))
    return disj


def subclass_to_rules(view: SchemaView, child: ClassDefinitionName, parent: ClassDefinitionName,
                      type_designator_slot: SlotDefinitionName = None) -> List[ClassRule]:
    """
    rolls up child class to parent class, turning class-specific slot_usages into rules
    :param view:
    :param child: class to roll up to
    :param parent: class to roll up from
    :return:
    """
    child_slots = view.class_induced_slots(child)
    rule = ClassRule()
    if type_designator_slot is None:
        type_designators = [s.name for s in view.class_induced_slots(parent) if s.designates_type]
        if len(type_designators) == 1:
            type_designator_slot = type_designators[0]
        elif len(type_designators) > 1:
            raise Exception(f'Multiple type designatirs: {type_designators}')
        else:
            type_designator_slot = SlotDefinitionName('type')
    rule.preconditions = AnonymousClassExpression(slot_conditions=[SlotDefinition('type', equals_string=child)])
    rule.postconditions = AnonymousClassExpression(slot_conditions=child_slots)
    # ensure slots are declared for parent
    parent_slots = view.class_induced_slots(parent)
    parent_slot_names = [s.name for s in parent_slots]
    parent_cls = view.get_class(parent)
    for child_slot in child_slots:
        if child_slot.name not in parent_slot_names:
            parent_cls.slots.append(child_slot.name)
    if not rule_subsumed_by_class(view, rule=rule, cls=parent_cls):
        parent_cls.rules.append(rule)
    return [rule]


def rule_subsumed_by_class(view: SchemaView, rule, cls: ClassDefinition):
    induced_slots = view.class_induced_slots(cls.name)
    return False


def remove_redundant_rules(view: SchemaView, class_name: ClassDefinitionName):
    induced_slots = view.class_induced_slots(class_name)
    cls = view.get_class(class_name)
    redundant_rules = []
    for rule in cls.rules:
        if rule_subsumed_by_class(view, rule, cls):
            redundant_rules.append(rule)
    for rule in redundant_rules:
        cls.rules.remove(rule)
    return redundant_rules





