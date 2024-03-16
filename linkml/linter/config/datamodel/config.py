# Auto generated from config.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-09-19T10:30:48
# Schema: linter-config
#
# id: https://w3id.org/linkml/linter/config
# description: A datamodel describing the configuration file accepted by the linkml-lint command
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import as_dict
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.metamodelcore import Bool, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot
from rdflib import URIRef

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
    """
    This is the top-level representation of a LinkML linter configuration file. Each attribute represents a rule that
    can be enabled and possibly configured by a configuration file.
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.Config
    class_class_curie: ClassVar[str] = "lintcfg:Config"
    class_name: ClassVar[str] = "Config"
    class_model_uri: ClassVar[URIRef] = LINTCFG.Config

    extends: Optional[Union[str, "ExtendableConfigs"]] = None
    rules: Optional[Union[dict, "Rules"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.extends is not None and not isinstance(self.extends, ExtendableConfigs):
            self.extends = ExtendableConfigs(self.extends)

        if self.rules is not None and not isinstance(self.rules, Rules):
            self.rules = Rules(**as_dict(self.rules))

        super().__post_init__(**kwargs)


@dataclass
class Rules(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.Rules
    class_class_curie: ClassVar[str] = "lintcfg:Rules"
    class_name: ClassVar[str] = "Rules"
    class_model_uri: ClassVar[URIRef] = LINTCFG.Rules

    no_empty_title: Optional[Union[dict, "RuleConfig"]] = None
    permissible_values_format: Optional[Union[dict, "PermissibleValuesFormatRuleConfig"]] = None
    tree_root_class: Optional[Union[dict, "TreeRootClassRuleConfig"]] = None
    recommended: Optional[Union[dict, "RecommendedRuleConfig"]] = None
    no_xsd_int_type: Optional[Union[dict, "RuleConfig"]] = None
    no_invalid_slot_usage: Optional[Union[dict, "RuleConfig"]] = None
    standard_naming: Optional[Union[dict, "StandardNamingConfig"]] = None
    canonical_prefixes: Optional[Union[dict, "CanonicalPrefixesConfig"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.no_empty_title is not None and not isinstance(self.no_empty_title, RuleConfig):
            self.no_empty_title = RuleConfig(**as_dict(self.no_empty_title))

        if self.permissible_values_format is not None and not isinstance(
            self.permissible_values_format, PermissibleValuesFormatRuleConfig
        ):
            self.permissible_values_format = PermissibleValuesFormatRuleConfig(
                **as_dict(self.permissible_values_format)
            )

        if self.tree_root_class is not None and not isinstance(self.tree_root_class, TreeRootClassRuleConfig):
            self.tree_root_class = TreeRootClassRuleConfig(**as_dict(self.tree_root_class))

        if self.recommended is not None and not isinstance(self.recommended, RecommendedRuleConfig):
            self.recommended = RecommendedRuleConfig(**as_dict(self.recommended))

        if self.no_xsd_int_type is not None and not isinstance(self.no_xsd_int_type, RuleConfig):
            self.no_xsd_int_type = RuleConfig(**as_dict(self.no_xsd_int_type))

        if self.no_invalid_slot_usage is not None and not isinstance(self.no_invalid_slot_usage, RuleConfig):
            self.no_invalid_slot_usage = RuleConfig(**as_dict(self.no_invalid_slot_usage))

        if self.standard_naming is not None and not isinstance(self.standard_naming, StandardNamingConfig):
            self.standard_naming = StandardNamingConfig(**as_dict(self.standard_naming))

        if self.canonical_prefixes is not None and not isinstance(self.canonical_prefixes, CanonicalPrefixesConfig):
            self.canonical_prefixes = CanonicalPrefixesConfig(**as_dict(self.canonical_prefixes))

        super().__post_init__(**kwargs)


@dataclass
class RuleConfig(YAMLRoot):
    """
    This is the base class for linter rules. It contains configuration options that are  common to all rules.
    """

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


@dataclass
class PermissibleValuesFormatRuleConfig(RuleConfig):
    """
    Additional configuration options for the `permissible_values_format` rule
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.PermissibleValuesFormatRuleConfig
    class_class_curie: ClassVar[str] = "lintcfg:PermissibleValuesFormatRuleConfig"
    class_name: ClassVar[str] = "PermissibleValuesFormatRuleConfig"
    class_model_uri: ClassVar[URIRef] = LINTCFG.PermissibleValuesFormatRuleConfig

    level: Union[str, "RuleLevel"] = None
    format: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.format is not None and not isinstance(self.format, str):
            self.format = str(self.format)

        super().__post_init__(**kwargs)


@dataclass
class TreeRootClassRuleConfig(RuleConfig):
    """
    Additional configuration options for the `tree_root_class` rule
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.TreeRootClassRuleConfig
    class_class_curie: ClassVar[str] = "lintcfg:TreeRootClassRuleConfig"
    class_name: ClassVar[str] = "TreeRootClassRuleConfig"
    class_model_uri: ClassVar[URIRef] = LINTCFG.TreeRootClassRuleConfig

    level: Union[str, "RuleLevel"] = None
    root_class_name: Optional[str] = None
    validate_existing_class_name: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.root_class_name is not None and not isinstance(self.root_class_name, str):
            self.root_class_name = str(self.root_class_name)

        if self.validate_existing_class_name is not None and not isinstance(self.validate_existing_class_name, Bool):
            self.validate_existing_class_name = Bool(self.validate_existing_class_name)

        super().__post_init__(**kwargs)


@dataclass
class RecommendedRuleConfig(RuleConfig):
    """
    Additional configuration options for the `recommended` rule
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.RecommendedRuleConfig
    class_class_curie: ClassVar[str] = "lintcfg:RecommendedRuleConfig"
    class_name: ClassVar[str] = "RecommendedRuleConfig"
    class_model_uri: ClassVar[URIRef] = LINTCFG.RecommendedRuleConfig

    level: Union[str, "RuleLevel"] = None
    include: Optional[Union[str, List[str]]] = empty_list()
    exclude: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.include, list):
            self.include = [self.include] if self.include is not None else []
        self.include = [v if isinstance(v, str) else str(v) for v in self.include]

        if not isinstance(self.exclude, list):
            self.exclude = [self.exclude] if self.exclude is not None else []
        self.exclude = [v if isinstance(v, str) else str(v) for v in self.exclude]

        super().__post_init__(**kwargs)


@dataclass
class StandardNamingConfig(RuleConfig):
    """
    Additional configuration options for the `standard_naming` rule
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.StandardNamingConfig
    class_class_curie: ClassVar[str] = "lintcfg:StandardNamingConfig"
    class_name: ClassVar[str] = "StandardNamingConfig"
    class_model_uri: ClassVar[URIRef] = LINTCFG.StandardNamingConfig

    level: Union[str, "RuleLevel"] = None
    permissible_values_upper_case: Optional[Union[bool, Bool]] = None
    slot_pattern: Optional[str] = None
    class_pattern: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.permissible_values_upper_case is not None and not isinstance(self.permissible_values_upper_case, Bool):
            self.permissible_values_upper_case = Bool(self.permissible_values_upper_case)

        if self.class_pattern is not None and not isinstance(self.class_pattern, str):
            self.class_pattern = str(self.class_pattern)

        if self.slot_pattern is not None and not isinstance(self.slot_pattern, str):
            self.slot_pattern = str(self.slot_pattern)

        super().__post_init__(**kwargs)


@dataclass
class CanonicalPrefixesConfig(RuleConfig):
    """
    Additional configuration options for the canonical_prefixes rule
    """

    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LINTCFG.CanonicalPrefixesConfig
    class_class_curie: ClassVar[str] = "lintcfg:CanonicalPrefixesConfig"
    class_name: ClassVar[str] = "CanonicalPrefixesConfig"
    class_model_uri: ClassVar[URIRef] = LINTCFG.CanonicalPrefixesConfig

    level: Union[str, "RuleLevel"] = None
    prefixmaps_contexts: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.prefixmaps_contexts, list):
            self.prefixmaps_contexts = [self.prefixmaps_contexts] if self.prefixmaps_contexts is not None else []
        self.prefixmaps_contexts = [v if isinstance(v, str) else str(v) for v in self.prefixmaps_contexts]

        super().__post_init__(**kwargs)


# Enumerations
class ExtendableConfigs(EnumDefinitionImpl):
    """
    The permissible values for the `extends` field of a config file
    """

    recommended = PermissibleValue(text="recommended", description="Extend the recommended rule set")

    _defn = EnumDefinition(
        name="ExtendableConfigs",
        description="The permissible values for the `extends` field of a config file",
    )


class RuleLevel(EnumDefinitionImpl):
    """
    The permissible values for the `level` option of all rules
    """

    disabled = PermissibleValue(text="disabled", description="The rule will not be checked")
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
        description="The permissible values for the `level` option of all rules",
    )


# Slots
class slots:
    pass


slots.config__extends = Slot(
    uri=LINTCFG.extends,
    name="config__extends",
    curie=LINTCFG.curie("extends"),
    model_uri=LINTCFG.config__extends,
    domain=None,
    range=Optional[Union[str, "ExtendableConfigs"]],
)

slots.config__rules = Slot(
    uri=LINTCFG.rules,
    name="config__rules",
    curie=LINTCFG.curie("rules"),
    model_uri=LINTCFG.config__rules,
    domain=None,
    range=Optional[Union[dict, Rules]],
)

slots.rules__no_empty_title = Slot(
    uri=LINTCFG.no_empty_title,
    name="rules__no_empty_title",
    curie=LINTCFG.curie("no_empty_title"),
    model_uri=LINTCFG.rules__no_empty_title,
    domain=None,
    range=Optional[Union[dict, RuleConfig]],
)

slots.rules__permissible_values_format = Slot(
    uri=LINTCFG.permissible_values_format,
    name="rules__permissible_values_format",
    curie=LINTCFG.curie("permissible_values_format"),
    model_uri=LINTCFG.rules__permissible_values_format,
    domain=None,
    range=Optional[Union[dict, PermissibleValuesFormatRuleConfig]],
)

slots.rules__tree_root_class = Slot(
    uri=LINTCFG.tree_root_class,
    name="rules__tree_root_class",
    curie=LINTCFG.curie("tree_root_class"),
    model_uri=LINTCFG.rules__tree_root_class,
    domain=None,
    range=Optional[Union[dict, TreeRootClassRuleConfig]],
)

slots.rules__recommended = Slot(
    uri=LINTCFG.recommended,
    name="rules__recommended",
    curie=LINTCFG.curie("recommended"),
    model_uri=LINTCFG.rules__recommended,
    domain=None,
    range=Optional[Union[dict, RecommendedRuleConfig]],
)

slots.rules__no_xsd_int_type = Slot(
    uri=LINTCFG.no_xsd_int_type,
    name="rules__no_xsd_int_type",
    curie=LINTCFG.curie("no_xsd_int_type"),
    model_uri=LINTCFG.rules__no_xsd_int_type,
    domain=None,
    range=Optional[Union[dict, RuleConfig]],
)

slots.rules__no_invalid_slot_usage = Slot(
    uri=LINTCFG.no_invalid_slot_usage,
    name="rules__no_invalid_slot_usage",
    curie=LINTCFG.curie("no_invalid_slot_usage"),
    model_uri=LINTCFG.rules__no_invalid_slot_usage,
    domain=None,
    range=Optional[Union[dict, RuleConfig]],
)

slots.rules__standard_naming = Slot(
    uri=LINTCFG.standard_naming,
    name="rules__standard_naming",
    curie=LINTCFG.curie("standard_naming"),
    model_uri=LINTCFG.rules__standard_naming,
    domain=None,
    range=Optional[Union[dict, StandardNamingConfig]],
)

slots.rules__canonical_prefixes = Slot(
    uri=LINTCFG.canonical_prefixes,
    name="rules__canonical_prefixes",
    curie=LINTCFG.curie("canonical_prefixes"),
    model_uri=LINTCFG.rules__canonical_prefixes,
    domain=None,
    range=Optional[Union[dict, CanonicalPrefixesConfig]],
)

slots.ruleConfig__level = Slot(
    uri=LINTCFG.level,
    name="ruleConfig__level",
    curie=LINTCFG.curie("level"),
    model_uri=LINTCFG.ruleConfig__level,
    domain=None,
    range=Union[str, "RuleLevel"],
)

slots.permissibleValuesFormatRuleConfig__format = Slot(
    uri=LINTCFG.format,
    name="permissibleValuesFormatRuleConfig__format",
    curie=LINTCFG.curie("format"),
    model_uri=LINTCFG.permissibleValuesFormatRuleConfig__format,
    domain=None,
    range=Optional[str],
)

slots.treeRootClassRuleConfig__root_class_name = Slot(
    uri=LINTCFG.root_class_name,
    name="treeRootClassRuleConfig__root_class_name",
    curie=LINTCFG.curie("root_class_name"),
    model_uri=LINTCFG.treeRootClassRuleConfig__root_class_name,
    domain=None,
    range=Optional[str],
)

slots.treeRootClassRuleConfig__validate_existing_class_name = Slot(
    uri=LINTCFG.validate_existing_class_name,
    name="treeRootClassRuleConfig__validate_existing_class_name",
    curie=LINTCFG.curie("validate_existing_class_name"),
    model_uri=LINTCFG.treeRootClassRuleConfig__validate_existing_class_name,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.recommendedRuleConfig__include = Slot(
    uri=LINTCFG.include,
    name="recommendedRuleConfig__include",
    curie=LINTCFG.curie("include"),
    model_uri=LINTCFG.recommendedRuleConfig__include,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.recommendedRuleConfig__exclude = Slot(
    uri=LINTCFG.exclude,
    name="recommendedRuleConfig__exclude",
    curie=LINTCFG.curie("exclude"),
    model_uri=LINTCFG.recommendedRuleConfig__exclude,
    domain=None,
    range=Optional[Union[str, List[str]]],
)

slots.standardNamingConfig__permissible_values_upper_case = Slot(
    uri=LINTCFG.permissible_values_upper_case,
    name="standardNamingConfig__permissible_values_upper_case",
    curie=LINTCFG.curie("permissible_values_upper_case"),
    model_uri=LINTCFG.standardNamingConfig__permissible_values_upper_case,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.canonicalPrefixesConfig__prefixmaps_contexts = Slot(
    uri=LINTCFG.prefixmaps_contexts,
    name="canonicalPrefixesConfig__prefixmaps_contexts",
    curie=LINTCFG.curie("prefixmaps_contexts"),
    model_uri=LINTCFG.canonicalPrefixesConfig__prefixmaps_contexts,
    domain=None,
    range=Optional[Union[str, List[str]]],
)
