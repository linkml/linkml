# Auto generated from config.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-08-16T12:05:08
# Schema: linter-config
#
# id: https://w3id.org/linkml/linter/config
# description: A datamodel describing the configuration file accepted by the linkml-lint command
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
import sys
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import (EnumDefinition, PermissibleValue,
                                              PvFormulaOptions)
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import \
    dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import (YAMLRoot, extended_float,
                                            extended_int, extended_str)
from rdflib import Namespace, URIRef

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
LINTCFG = CurieNamespace("lintcfg", "https://w3id.org/linkml/linter/config")
DEFAULT_ = LINTCFG


# Types

# Class references


@dataclass
class Config(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.Config
    class_class_curie: ClassVar[str] = "lintcfg:Config"
    class_name: ClassVar[str] = "Config"
    class_model_uri: ClassVar[URIRef] = LINTCFG.Config

    no_empty_title: Optional[Union[dict, "RuleConfig"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.no_empty_title is not None and not isinstance(
            self.no_empty_title, RuleConfig
        ):
            self.no_empty_title = RuleConfig(**as_dict(self.no_empty_title))

        super().__post_init__(**kwargs)


@dataclass
class RuleConfig(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.RuleConfig
    class_class_curie: ClassVar[str] = "lintcfg:RuleConfig"
    class_name: ClassVar[str] = "RuleConfig"
    class_model_uri: ClassVar[URIRef] = LINTCFG.RuleConfig

    level: Union[str, "RuleLevel"] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.level):
            self.MissingRequiredField("level")
        if not isinstance(self.level, RuleLevel):
            self.level = RuleLevel(self.level)

        super().__post_init__(**kwargs)


# Enumerations
class RuleLevel(EnumDefinitionImpl):

    disabled = PermissibleValue(
        text="disabled", description="The rule will not be checked"
    )
    warning = PermissibleValue(
        text="warning",
        description="A violation of a rule at this level is a minor issue that should be fixed",
    )
    error = PermissibleValue(
        text="error",
        description="A violation of a rule at this level is a major issue that must be fixed",
    )

    _defn = EnumDefinition(
        name="RuleLevel",
    )


# Slots
class slots:
    pass


slots.config__no_empty_title = Slot(
    uri=LINTCFG.no_empty_title,
    name="config__no_empty_title",
    curie=LINTCFG.curie("no_empty_title"),
    model_uri=LINTCFG.config__no_empty_title,
    domain=None,
    range=Optional[Union[dict, RuleConfig]],
)

slots.ruleConfig__level = Slot(
    uri=LINTCFG.level,
    name="ruleConfig__level",
    curie=LINTCFG.curie("level"),
    model_uri=LINTCFG.ruleConfig__level,
    domain=None,
    range=Union[str, "RuleLevel"],
)
