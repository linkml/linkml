# Auto generated from alternatives.yaml by pythongen.py version: 0.9.0
# Generation date: 2020-11-16 08:55
# Schema: alternatives
#
# id: http://example.org/test/alternatives
# description: Enumeration alternatives
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from includes.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
CLUE = CurieNamespace('CLUE', 'http://ontologies-r.us/clue/')
CS = CurieNamespace('CS', 'http://ontologies-r.us/codesystems/')
BIOLINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
EVIDENCE = CurieNamespace('evidence', 'http://example.org/test/evidence/')
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

    def __post_init__(self, **kwargs: Dict[str, Any]):
        if self.entry_name is None:
            raise ValueError("entry_name must be supplied")
        if not isinstance(self.entry_name, AllEnumsEntryName):
            self.entry_name = AllEnumsEntryName(self.entry_name)

        if self.code_1 is None:
            raise ValueError("code_1 must be supplied")
        elif not isinstance(self.code_1, list):
            self.code_1 = [self.code_1]
        elif len(self.code_1) == 0:
            raise ValueError(f"code_1 must be a non-empty list")
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
@dataclass
class OpenEnum(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="OpenEnum",
        description="Baseline enumeration -- simple code/value pairs, where the value (description) is optional",
        permissible_values={
            "a": PermissibleValue("top"),
            "b": PermissibleValue("middle"),
            "c": PermissibleValue("bottom"),
            "d": PermissibleValue("")}
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in OpenEnum.defn.permissible_values:
            raise ValueError(f"Unknown OpenEnum value: {self.code}")


@dataclass
class ConstrainedEnum2(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="ConstrainedEnum2",
        description="All codes from the version of HPO labeled \"current\" by the referenced service",
        code_set=CS.HPO,
        pv_formula=PvFormulaOptions(code='CODE'),
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in ConstrainedEnum2.defn.permissible_values:
            raise ValueError(f"Unknown ConstrainedEnum2 value: {self.code}")


@dataclass
class ConstrainedEnum3(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="ConstrainedEnum3",
        description="All uris from the version of HPO with the tag, \"production\"",
        code_set=CS.HPO,
        code_set_tag="production",
        pv_formula=PvFormulaOptions(code='URI'),
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in ConstrainedEnum3.defn.permissible_values:
            raise ValueError(f"Unknown ConstrainedEnum3 value: {self.code}")


@dataclass
class ConstrainedEnum4(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="ConstrainedEnum4",
        description="All curies from version 1.17 of HPO",
        code_set=CS.HPO,
        code_set_version="1.17",
        pv_formula=PvFormulaOptions(code='CURIE'),
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in ConstrainedEnum4.defn.permissible_values:
            raise ValueError(f"Unknown ConstrainedEnum4 value: {self.code}")


@dataclass
class ConstrainedEnum5(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="ConstrainedEnum5",
        description="All fhir codings from the \"current\" version of the CLUE \"mustard options\" value set",
        code_set=CLUE.mustard_options,
        pv_formula=PvFormulaOptions(code='FHIR_CODING'),
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in ConstrainedEnum5.defn.permissible_values:
            raise ValueError(f"Unknown ConstrainedEnum5 value: {self.code}")


@dataclass
class ConstrainedEnum6(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="ConstrainedEnum6",
        description="All codes from SNOMED CT INTL 2020-7-31 or greater",
        code_set=CS.SCT,
        code_set_version=">=2020-7-31",
        pv_formula=PvFormulaOptions(code='CODE'),
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in ConstrainedEnum6.defn.permissible_values:
            raise ValueError(f"Unknown ConstrainedEnum6 value: {self.code}")


@dataclass
class ConstrainedEvidence(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="ConstrainedEvidence",
        description="Permissible values for CLUE evidence fragments",
        code_set=EVIDENCE.clue_answers,
        permissible_values={
            "IEA": PermissibleValue("Colonel Mustard in the Ballroom"),
            "ISS": PermissibleValue("Mrs. Peacock with the Dagger",
                                    meaning=CLUE["1173"])}
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in ConstrainedEvidence.defn.permissible_values:
            raise ValueError(f"Unknown ConstrainedEvidence value: {self.code}")


@dataclass
class MappedEvidence(YAMLRoot):
    defn: ClassVar[EnumDefinition] = EnumDefinition(
        name="MappedEvidence",
        description="Permissible values that draw directly from the code set",
        code_set=EVIDENCE.clue_answers,
        pv_formula=PvFormulaOptions(code='URI'),
    )
    code: str

    def __post_init__(self) -> None:
        self.code = str(self.code)
        if self.code not in MappedEvidence.defn.permissible_values:
            raise ValueError(f"Unknown MappedEvidence value: {self.code}")



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
