"""
THIS IS A TEMPORARY MODULE TO DEVELOP THE `extra_slots` FEATURE AND SHOULD BE REMOVED
BEFORE MERGING THIS PR, ONCE AN UPDATED METAMODEL HAS BEEN ISSUED
"""

from dataclasses import dataclass, field

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model import meta


@dataclass
class ExtraSlotsExpression(meta.Expression):
    allowed: bool | None = None
    range_expression: meta.AnonymousSlotExpression | None = None

    def __post_init__(self, **kwargs):
        if self.range_expression and not isinstance(self.range_expression, meta.AnonymousSlotExpression):
            self.range_expression = meta.AnonymousSlotExpression(**as_dict(self.range_expression))

        if self.allowed and not isinstance(self.allowed, bool):
            self.allowed = bool(self.allowed.allowed)
        super().__post_init__(**kwargs)


@dataclass
class ClassDefinition_(meta.ClassDefinition):
    extra_slots: ExtraSlotsExpression | None = field(default=None)

    def __post_init__(self, **kwargs):
        if self.extra_slots and not isinstance(self.extra_slots, ExtraSlotsExpression):
            self.extra_slots = ExtraSlotsExpression(**as_dict(self.extra_slots))
        super().__post_init__(**kwargs)


def monkeypatch_classdef():
    meta.ClassDefinition = ClassDefinition_
    meta.ExtraSlotsExpression = ExtraSlotsExpression
