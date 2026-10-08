# id: https://w3id.org/linkml/examples/slot-names
# description: Slots whose names differ from their Python field names: Python keywords (from -> from_) and names with spaces (term id -> term_id). Generated model: ../model/slot_names_example.py
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import (
    date,
    datetime,
    time
)
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Optional,
    Union
)

from jsonasobj2 import (
    JsonObj,
    as_dict
)
from linkml_runtime.linkml_model.meta import (
    EnumDefinition,
    PermissibleValue,
    PvFormulaOptions
)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import (
    camelcase,
    sfx,
    underscore
)
from linkml_runtime.utils.metamodelcore import (
    bnode,
    empty_dict,
    empty_list
)
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (
    YAMLRoot,
    extended_float,
    extended_int,
    extended_str,
    slot_aliases
)
from rdflib import (
    Namespace,
    URIRef
)

from linkml_runtime.linkml_model.types import Integer, String

metamodel_version = "1.12.0"
version = None

# Namespaces
EX = CurieNamespace('ex', 'https://w3id.org/linkml/examples/slot-names/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = EX


# Types

# Class references
class TermIn(extended_str):
    pass


class NamedTermId(extended_str):
    pass


@slot_aliases({"from_": "from"})
@dataclass(repr=False)
class Window(YAMLRoot):
    """
    Keyword-named slots and no inference rules
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Window"]
    class_class_curie: ClassVar[str] = "ex:Window"
    class_name: ClassVar[str] = "Window"
    class_model_uri: ClassVar[URIRef] = EX.Window

    from_: Optional[str] = None
    to: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.from_ is not None and not isinstance(self.from_, str):
            self.from_ = str(self.from_)

        if self.to is not None and not isinstance(self.to, str):
            self.to = str(self.to)

        super().__post_init__(**kwargs)


@slot_aliases({"from_": "from", "as_": "as"})
@dataclass(repr=False)
class Span(YAMLRoot):
    """
    A string_serialization that reads and writes keyword-named slots
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Span"]
    class_class_curie: ClassVar[str] = "ex:Span"
    class_name: ClassVar[str] = "Span"
    class_model_uri: ClassVar[URIRef] = EX.Span

    from_: Optional[str] = None
    to: Optional[str] = None
    as_: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.from_ is not None and not isinstance(self.from_, str):
            self.from_ = str(self.from_)

        if self.to is not None and not isinstance(self.to, str):
            self.to = str(self.to)

        if self.as_ is not None and not isinstance(self.as_, str):
            self.as_ = str(self.as_)

        super().__post_init__(**kwargs)


@slot_aliases({"in_": "in"})
@dataclass(repr=False)
class Sum(YAMLRoot):
    """
    An equals_expression over keyword-named slots
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Sum"]
    class_class_curie: ClassVar[str] = "ex:Sum"
    class_name: ClassVar[str] = "Sum"
    class_model_uri: ClassVar[URIRef] = EX.Sum

    in_: Optional[int] = None
    out: Optional[int] = None
    total: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.in_ is not None and not isinstance(self.in_, int):
            self.in_ = int(self.in_)

        if self.out is not None and not isinstance(self.out, int):
            self.out = int(self.out)

        if self.total is not None and not isinstance(self.total, int):
            self.total = int(self.total)

        super().__post_init__(**kwargs)


@slot_aliases({"in_": "in", "from_": "from"})
@dataclass(repr=False)
class Term(YAMLRoot):
    """
    A keyword-named identifier
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Term"]
    class_class_curie: ClassVar[str] = "ex:Term"
    class_name: ClassVar[str] = "Term"
    class_model_uri: ClassVar[URIRef] = EX.Term

    in_: Union[str, TermIn] = None
    from_: Optional[str] = None
    label: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.in_):
            self.MissingRequiredField("in")
        if not isinstance(self.in_, TermIn):
            self.in_ = TermIn(self.in_)

        if self.from_ is not None and not isinstance(self.from_, str):
            self.from_ = str(self.from_)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Named(YAMLRoot):
    """
    An identifier with a space in its name
    """
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Named"]
    class_class_curie: ClassVar[str] = "ex:Named"
    class_name: ClassVar[str] = "Named"
    class_model_uri: ClassVar[URIRef] = EX.Named

    term_id: Union[str, NamedTermId] = None
    start_date: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.term_id):
            self.MissingRequiredField("term_id")
        if not isinstance(self.term_id, NamedTermId):
            self.term_id = NamedTermId(self.term_id)

        if self.start_date is not None and not isinstance(self.start_date, str):
            self.start_date = str(self.start_date)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Container(YAMLRoot):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = EX["Container"]
    class_class_curie: ClassVar[str] = "ex:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = EX.Container

    terms: Optional[Union[dict[Union[str, TermIn], Union[dict, Term]], list[Union[dict, Term]]]] = empty_dict()
    named: Optional[Union[dict, Named]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        self._normalize_inlined_as_list(slot_name="terms", slot_type=Term, key_name="in", keyed=True)

        if self.named is not None and not isinstance(self.named, Named):
            self.named = Named(**as_dict(self.named))

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.window__from = Slot(uri=EX['from'], name="window__from", curie=EX.curie('from'),
                   model_uri=EX.window__from, domain=None, range=Optional[str])

slots.window__to = Slot(uri=EX.to, name="window__to", curie=EX.curie('to'),
                   model_uri=EX.window__to, domain=None, range=Optional[str])

slots.span__from = Slot(uri=EX['from'], name="span__from", curie=EX.curie('from'),
                   model_uri=EX.span__from, domain=None, range=Optional[str])

slots.span__to = Slot(uri=EX.to, name="span__to", curie=EX.curie('to'),
                   model_uri=EX.span__to, domain=None, range=Optional[str])

slots.span__as = Slot(uri=EX['as'], name="span__as", curie=EX.curie('as'),
                   model_uri=EX.span__as, domain=None, range=Optional[str])

slots.sum__in = Slot(uri=EX['in'], name="sum__in", curie=EX.curie('in'),
                   model_uri=EX.sum__in, domain=None, range=Optional[int])

slots.sum__out = Slot(uri=EX.out, name="sum__out", curie=EX.curie('out'),
                   model_uri=EX.sum__out, domain=None, range=Optional[int])

slots.sum__total = Slot(uri=EX.total, name="sum__total", curie=EX.curie('total'),
                   model_uri=EX.sum__total, domain=None, range=Optional[int])

slots.term__in = Slot(uri=EX['in'], name="term__in", curie=EX.curie('in'),
                   model_uri=EX.term__in, domain=None, range=URIRef)

slots.term__from = Slot(uri=EX['from'], name="term__from", curie=EX.curie('from'),
                   model_uri=EX.term__from, domain=None, range=Optional[str])

slots.term__label = Slot(uri=EX.label, name="term__label", curie=EX.curie('label'),
                   model_uri=EX.term__label, domain=None, range=Optional[str])

slots.named__term_id = Slot(uri=EX.term_id, name="named__term_id", curie=EX.curie('term_id'),
                   model_uri=EX.named__term_id, domain=None, range=URIRef)

slots.named__start_date = Slot(uri=EX.start_date, name="named__start_date", curie=EX.curie('start_date'),
                   model_uri=EX.named__start_date, domain=None, range=Optional[str])

slots.container__terms = Slot(uri=EX.terms, name="container__terms", curie=EX.curie('terms'),
                   model_uri=EX.container__terms, domain=None, range=Optional[Union[dict[Union[str, TermIn], Union[dict, Term]], list[Union[dict, Term]]]])

slots.container__named = Slot(uri=EX.named, name="container__named", curie=EX.curie('named'),
                   model_uri=EX.container__named, domain=None, range=Optional[Union[dict, Named]])

