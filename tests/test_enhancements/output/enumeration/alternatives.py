# Auto generated from alternatives.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-07-09 16:24
# Schema: alternatives
#
# id: http://example.org/test/alternatives
# description: Enumeration alternatives
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CLUE = CurieNamespace('CLUE', 'http://ontologies-r.us/clue/')
CS = CurieNamespace('CS', 'http://ontologies-r.us/codesystems/')
EVIDENCE = CurieNamespace('evidence', 'http://example.org/test/evidence/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
DEFAULT_ = EVIDENCE


# Types

# Class references
class AllEnumsEntryName(extended_str):
    pass


@dataclass
class AllEnums(YAMLRoot):
    """
    A class that incorporates all of the enumeration examples above
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = EVIDENCE.AllEnums
    class_class_curie: ClassVar[str] = "evidence:AllEnums"
    class_name: ClassVar[str] = "all_enums"
    class_model_uri: ClassVar[URIRef] = EVIDENCE.AllEnums

    entry_name: Union[str, AllEnumsEntryName] = None
    code_1: Union[Union[str, "OpenEnum"], List[Union[str, "OpenEnum"]]] = None
    code_2: Optional[Union[str, "ConstrainedEnum2"]] = None
    code_3: Optional[Union[str, "ConstrainedEnum3"]] = None
    code_4: Optional[Union[str, "ConstrainedEnum4"]] = None
    code_5: Optional[Union[str, "ConstrainedEnum4"]] = None
    code_6: Optional[Union[str, "ConstrainedEnum4"]] = None
    code_7: Optional[Union[str, "ConstrainedEvidence"]] = None
    code_8: Optional[Union[str, "MappedEvidence"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.entry_name):
            self.MissingRequiredField("entry_name")
        if not isinstance(self.entry_name, AllEnumsEntryName):
            self.entry_name = AllEnumsEntryName(self.entry_name)

        if self._is_empty(self.code_1):
            self.MissingRequiredField("code_1")
        if not isinstance(self.code_1, list):
            self.code_1 = [self.code_1] if self.code_1 is not None else []
        self.code_1 = [v if isinstance(v, OpenEnum) else OpenEnum(v) for v in self.code_1]

        if self.code_2 is not None and not isinstance(self.code_2, ConstrainedEnum2):
            self.code_2 = ConstrainedEnum2(self.code_2)

        if self.code_3 is not None and not isinstance(self.code_3, ConstrainedEnum3):
            self.code_3 = ConstrainedEnum3(self.code_3)

        if self.code_4 is not None and not isinstance(self.code_4, ConstrainedEnum4):
            self.code_4 = ConstrainedEnum4(self.code_4)

        if self.code_5 is not None and not isinstance(self.code_5, ConstrainedEnum4):
            self.code_5 = ConstrainedEnum4(self.code_5)

        if self.code_6 is not None and not isinstance(self.code_6, ConstrainedEnum4):
            self.code_6 = ConstrainedEnum4(self.code_6)

        if self.code_7 is not None and not isinstance(self.code_7, ConstrainedEvidence):
            self.code_7 = ConstrainedEvidence(self.code_7)

        if self.code_8 is not None and not isinstance(self.code_8, MappedEvidence):
            self.code_8 = MappedEvidence(self.code_8)

        super().__post_init__(**kwargs)


# Enumerations
class OpenEnum(EnumDefinitionImpl):
    """
    Baseline enumeration -- simple code/value pairs, where the value (description) is optional
    """
    a = PermissibleValue(text="a",
                         description="top")
    b = PermissibleValue(text="b",
                         description="middle")
    c = PermissibleValue(text="c",
                         description="bottom")
    d = PermissibleValue(text="d")

    _defn = EnumDefinition(
        name="OpenEnum",
        description="Baseline enumeration -- simple code/value pairs, where the value (description) is optional",
    )

class ConstrainedEnum2(EnumDefinitionImpl):
    """
    All codes from the version of HPO labeled "current" by the referenced service
    """
    _defn = EnumDefinition(
        name="ConstrainedEnum2",
        description="All codes from the version of HPO labeled \"current\" by the referenced service",
        code_set=CS.HPO,
        pv_formula=PvFormulaOptions.CODE,
    )

class ConstrainedEnum3(EnumDefinitionImpl):
    """
    All uris from the version of HPO with the tag, "production"
    """
    _defn = EnumDefinition(
        name="ConstrainedEnum3",
        description="All uris from the version of HPO with the tag, \"production\"",
        code_set=CS.HPO,
        code_set_tag="production",
        pv_formula=PvFormulaOptions.URI,
    )

class ConstrainedEnum4(EnumDefinitionImpl):
    """
    All curies from version 1.17 of HPO
    """
    _defn = EnumDefinition(
        name="ConstrainedEnum4",
        description="All curies from version 1.17 of HPO",
        code_set=CS.HPO,
        code_set_version="1.17",
        pv_formula=PvFormulaOptions.CURIE,
    )

class ConstrainedEnum5(EnumDefinitionImpl):
    """
    All fhir codings from the "current" version of the CLUE "mustard options" value set
    """
    _defn = EnumDefinition(
        name="ConstrainedEnum5",
        description="All fhir codings from the \"current\" version of the CLUE \"mustard options\" value set",
        code_set=CLUE.mustard_options,
        pv_formula=PvFormulaOptions.FHIR_CODING,
    )

class ConstrainedEnum6(EnumDefinitionImpl):
    """
    All codes from SNOMED CT INTL 2020-7-31 or greater
    """
    _defn = EnumDefinition(
        name="ConstrainedEnum6",
        description="All codes from SNOMED CT INTL 2020-7-31 or greater",
        code_set=CS.SCT,
        code_set_version=">=2020-7-31",
        pv_formula=PvFormulaOptions.CODE,
    )

class ConstrainedEvidence(EnumDefinitionImpl):
    """
    Permissible values for CLUE evidence fragments
    """
    IEA = PermissibleValue(text="IEA",
                             description="Colonel Mustard in the Ballroom")
    ISS = PermissibleValue(text="ISS",
                             description="Mrs. Peacock with the Dagger",
                             meaning=CLUE["1173"])

    _defn = EnumDefinition(
        name="ConstrainedEvidence",
        description="Permissible values for CLUE evidence fragments",
        code_set=EVIDENCE.clue_answers,
    )

class MappedEvidence(EnumDefinitionImpl):
    """
    Permissible values that draw directly from the code set
    """
    _defn = EnumDefinition(
        name="MappedEvidence",
        description="Permissible values that draw directly from the code set",
        code_set=EVIDENCE.clue_answers,
        pv_formula=PvFormulaOptions.URI,
    )

# Slots
class slots:
    pass

slots.allEnums__entry_name = Slot(uri=EVIDENCE.entry_name, name="allEnums__entry_name", curie=EVIDENCE.curie('entry_name'),
                   model_uri=EVIDENCE.allEnums__entry_name, domain=None, range=URIRef)

slots.allEnums__code_1 = Slot(uri=EVIDENCE.code_1, name="allEnums__code_1", curie=EVIDENCE.curie('code_1'),
                   model_uri=EVIDENCE.allEnums__code_1, domain=None, range=Union[Union[str, "OpenEnum"], List[Union[str, "OpenEnum"]]])

slots.allEnums__code_2 = Slot(uri=EVIDENCE.code_2, name="allEnums__code_2", curie=EVIDENCE.curie('code_2'),
                   model_uri=EVIDENCE.allEnums__code_2, domain=None, range=Optional[Union[str, "ConstrainedEnum2"]])

slots.allEnums__code_3 = Slot(uri=EVIDENCE.code_3, name="allEnums__code_3", curie=EVIDENCE.curie('code_3'),
                   model_uri=EVIDENCE.allEnums__code_3, domain=None, range=Optional[Union[str, "ConstrainedEnum3"]])

slots.allEnums__code_4 = Slot(uri=EVIDENCE.code_4, name="allEnums__code_4", curie=EVIDENCE.curie('code_4'),
                   model_uri=EVIDENCE.allEnums__code_4, domain=None, range=Optional[Union[str, "ConstrainedEnum4"]])

slots.allEnums__code_5 = Slot(uri=EVIDENCE.code_5, name="allEnums__code_5", curie=EVIDENCE.curie('code_5'),
                   model_uri=EVIDENCE.allEnums__code_5, domain=None, range=Optional[Union[str, "ConstrainedEnum4"]])

slots.allEnums__code_6 = Slot(uri=EVIDENCE.code_6, name="allEnums__code_6", curie=EVIDENCE.curie('code_6'),
                   model_uri=EVIDENCE.allEnums__code_6, domain=None, range=Optional[Union[str, "ConstrainedEnum4"]])

slots.allEnums__code_7 = Slot(uri=EVIDENCE.code_7, name="allEnums__code_7", curie=EVIDENCE.curie('code_7'),
                   model_uri=EVIDENCE.allEnums__code_7, domain=None, range=Optional[Union[str, "ConstrainedEvidence"]])

slots.allEnums__code_8 = Slot(uri=EVIDENCE.code_8, name="allEnums__code_8", curie=EVIDENCE.curie('code_8'),
                   model_uri=EVIDENCE.allEnums__code_8, domain=None, range=Optional[Union[str, "MappedEvidence"]])