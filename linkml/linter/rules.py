import re
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Callable, Iterable, List

from linkml_runtime.linkml_model import (ClassDefinition, ClassDefinitionName,
                                         Element, SlotDefinition)
from linkml_runtime.utils.schemaview import SchemaView
from prefixmaps.io.parser import load_multi_context

from linkml import LOCAL_METAMODEL_YAML_FILE

from .config.datamodel.config import (CanonicalPrefixesConfig,
                                      RecommendedRuleConfig, RuleConfig,
                                      StandardNamingConfig,
                                      TreeRootClassRuleConfig)
from .linter import LinterProblem


class LinterRule(ABC):

    PATTERNS = {
        "snake": re.compile(r"[a-z][_a-z0-9]+"),
        "uppersnake": re.compile(r"[A-Z][_A-Z0-9]+"),
        "camel": re.compile(r"[a-z][a-zA-Z0-9]+"),
        "uppercamel": re.compile(r"[A-Z][a-zA-Z0-9]+"),
        "kebab": re.compile(r"[a-z][\-a-z0-9]+"),
        "_uncamel": re.compile(r"(?<!^)(?=[A-Z])"),
    }

    def __init__(self, config: RuleConfig) -> None:
        super().__init__()
        self.config = config

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @abstractmethod
    def check(self, schema_view: SchemaView, fix: bool) -> Iterable[LinterProblem]:
        pass

    @staticmethod
    def uncamel(n: str) -> str:
        return LinterRule.PATTERNS._uncamel.sub(" ", n)

    @staticmethod
    def format_element(element: Element):
        class_name = element.__class__.__name__.replace("Definition", "")
        return f"{class_name} '{element.name}'"


class NoEmptyTitleRule(LinterRule):

    id = "no_empty_title"

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        for e in schema_view.all_elements(imports=False).values():
            if fix and e.title is None:
                title = e.name.replace("_", " ")
                title = self.uncamel(title).lower()
                e.title = title
            if e.title is None:
                problem = LinterProblem(
                    message=f"{self.format_element(e)} has no title"
                )
                yield problem


class NoXsdIntTypeRule(LinterRule):

    id = "no_xsd_int_type"

    def check(self, schema_view: SchemaView, fix: bool = False):
        for type_definition in schema_view.all_types(imports=False).values():
            if type_definition.uri == "xsd:int":
                if fix:
                    type_definition.uri = "xsd:integer"
                else:
                    yield LinterProblem(
                        f"{self.format_element(type_definition)} has uri xsd:int"
                    )


class PermissibleValuesFormatRule(LinterRule):

    id = "permissible_values_format"

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        pattern = self.PATTERNS.get(self.config.format, re.compile(self.config.format))
        for enum_def in schema_view.all_enums(imports=False).values():
            for value in enum_def.permissible_values.keys():
                if pattern.fullmatch(value) is None:
                    yield LinterProblem(
                        f"{self.format_element(enum_def)} has permissible value '{value}'"
                    )


@lru_cache(maxsize=None)
def _get_recommended_metamodel_slots() -> List[str]:
    meta_schema_view = SchemaView(LOCAL_METAMODEL_YAML_FILE)
    recommended_meta_slots = []
    for class_name in meta_schema_view.all_classes(imports=False).keys():
        class_slots = meta_schema_view.class_induced_slots(class_name)
        for slot in class_slots:
            if slot.recommended:
                recommended_meta_slots.append(f"{class_name}__{slot.name}")
    return recommended_meta_slots


class RecommendedRule(LinterRule):

    id = "recommended"

    def __init__(self, config: RecommendedRuleConfig) -> None:
        self.config = config

    def check(self, schema_view: SchemaView, fix: bool = False):
        recommended_meta_slots = _get_recommended_metamodel_slots()
        for element_name, element_definition in schema_view.all_elements(
            imports=False
        ).items():
            if self.config.include and element_name not in self.config.include:
                continue
            if element_name in self.config.exclude:
                continue
            for meta_slot_name, meta_slot_value in vars(element_definition).items():
                key = f"{element_definition.class_name}__{meta_slot_name}"
                if key in recommended_meta_slots and not meta_slot_value:
                    yield LinterProblem(
                        f"{self.format_element(element_definition)} does not have recommended slot '{meta_slot_name}'"
                    )


class TreeRootClassRule(LinterRule):

    id = "tree_root_class"

    def __init__(self, config: TreeRootClassRuleConfig) -> None:
        super().__init__(config)

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        tree_roots = [
            c for c in schema_view.all_classes(imports=False).values() if c.tree_root
        ]
        if len(tree_roots) > 0:
            if self.config.validate_existing_class_name:
                for tree_root in tree_roots:
                    if str(tree_root.name) != self.config.root_class_name:
                        yield LinterProblem(
                            message=f"Tree root class has name '{tree_root.name}'"
                        )
        else:
            if fix:
                container = ClassDefinition(self.config.root_class_name, tree_root=True)
                schema_view.add_class(container)
                self.add_index_slots(schema_view, container.name)
            else:
                yield LinterProblem("Schema does not have class with `tree_root: true`")

    def add_index_slots(
        self,
        schema_view: SchemaView,
        container_name: ClassDefinitionName,
        inlined_as_list=False,
        must_have_identifier=False,
        slot_name_func: Callable = None,
        convert_camel_case=False,
    ) -> List[SlotDefinition]:
        """
        Adds index slots to a container pointing at all top-level classes

        :param schema: input schema, will be modified in place
        :param container_name:
        :param inlined_as_list:
        :param must_have_identifier:
        :param slot_name_func: function to determine the name of the slot from the class
        :return: new slots
        """
        container = schema_view.get_class(container_name)
        ranges = set()
        for cn in schema_view.all_classes():
            for s in schema_view.class_induced_slots(cn):
                ranges.add(s.range)
        top_level_classes = [
            c
            for c in schema_view.all_classes().values()
            if not c.tree_root and c.name not in ranges
        ]
        if must_have_identifier:
            top_level_classes = [
                c
                for c in top_level_classes
                if schema_view.get_identifier_slot(c.name) is not None
            ]
        index_slots = []
        for c in top_level_classes:
            has_identifier = schema_view.get_identifier_slot(c.name)
            if slot_name_func:
                sn = slot_name_func(c)
            else:
                cn = c.name
                if convert_camel_case:
                    cn = self.uncamel(cn).lower()
                cn = cn.replace(" ", "_")
                sn = f"{cn}_index"
            index_slot = SlotDefinition(
                sn,
                range=c.name,
                multivalued=True,
                inlined_as_list=not has_identifier or inlined_as_list,
            )
            index_slots.append(index_slot)
            schema_view.add_slot(index_slot)
            container.slots.append(index_slot.name)
        return index_slots


class NoInvalidSlotUsageRule(LinterRule):

    id = "no_invalid_slot_usage"

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        for class_name, class_definition in schema_view.all_classes(
            imports=False
        ).items():
            slot_usage = class_definition.slot_usage
            if not slot_usage:
                continue
            class_slots = schema_view.class_slots(class_name)
            for slot_usage_name in slot_usage.keys():
                if slot_usage_name not in class_slots:
                    yield LinterProblem(
                        f"Slot '{slot_usage_name}' not found on class '{class_name}'"
                    )


class StandardNamingRule(LinterRule):

    id = "standard_naming"

    def __init__(self, config: StandardNamingConfig) -> None:
        self.config = config

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        class_pattern = self.PATTERNS["uppercamel"]
        slot_pattern = self.PATTERNS["snake"]
        enum_pattern = self.PATTERNS["uppercamel"]
        permissible_value_pattern = (
            self.PATTERNS["uppersnake"]
            if self.config.permissible_values_upper_case
            else self.PATTERNS["snake"]
        )

        for class_name in schema_view.all_classes(imports=False).keys():
            if class_pattern.fullmatch(class_name) is None:
                yield LinterProblem(f"Class has name '{class_name}'")

        for slot_name in schema_view.all_slots(imports=False).keys():
            if slot_pattern.fullmatch(slot_name) is None:
                yield LinterProblem(f"Slot has name '{slot_name}'")

        for enum_name, enum_definition in schema_view.all_enums(imports=False).items():
            if enum_pattern.fullmatch(enum_name) is None:
                yield LinterProblem(f"Enum has name '{enum_name}'")

            for permissible_value_name in enum_definition.permissible_values.keys():
                if permissible_value_pattern.fullmatch(permissible_value_name) is None:
                    yield LinterProblem(
                        f"Permissible value of {self.format_element(enum_definition)} has name '{permissible_value_name}'"
                    )


class CanonicalPrefixesRule(LinterRule):

    id = "canonical_prefixes"

    def __init__(self, config: CanonicalPrefixesConfig) -> None:
        self.config = config

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        context = load_multi_context(self.config.prefixmaps_contexts)
        prefix_to_namespace = context.as_dict()
        namespace_to_prefix = context.as_inverted_dict()
        for prefix in schema_view.schema.prefixes.values():
            if prefix.prefix_prefix in prefix_to_namespace:
                if prefix.prefix_reference != prefix_to_namespace[prefix.prefix_prefix]:
                    yield LinterProblem(
                        f"Schema maps prefix '{prefix.prefix_prefix}' to namespace '{prefix.prefix_reference}' instead of namespace '{prefix_to_namespace[prefix.prefix_prefix]}'"
                    )
            if prefix.prefix_reference in namespace_to_prefix:
                if prefix.prefix_prefix != namespace_to_prefix[prefix.prefix_reference]:
                    yield LinterProblem(
                        f"Schema maps prefix '{prefix.prefix_prefix}' to namespace '{prefix.prefix_reference}' instead of using prefix '{namespace_to_prefix[prefix.prefix_reference]}'"
                    )
