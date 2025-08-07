"""Rule implementation for the linkml linter."""

from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Iterable
from functools import cache
from itertools import chain

from linkml_runtime.linkml_model import (
    ClassDefinition,
    ClassDefinitionName,
    Element,
    ElementName,
    EnumDefinition,
    EnumDefinitionName,
    SlotDefinition,
    TypeDefinition,
    TypeDefinitionName,
)
from linkml_runtime.utils.schemaview import SchemaView
from prefixmaps.io.parser import load_multi_context

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.linter.config.datamodel.config import (
    CanonicalPrefixesConfig,
    RecommendedRuleConfig,
    RuleConfig,
    StandardNamingConfig,
    TreeRootClassRuleConfig,
)
from linkml.linter.linter import LinterProblem


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

    # todo PVs are not checked for titles yet

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        excluded_types = [t.text if hasattr(t, "text") else str(t) for t in getattr(self.config, "exclude_type", [])]
        for e in schema_view.all_elements(imports=False).values():
            element_type_name = type(e).class_name
            if element_type_name in excluded_types:
                continue
            if fix and e.title is None:
                title = e.name.replace("_", " ")
                title = self.uncamel(title).lower()
                e.title = title
            if e.title is None:
                problem = LinterProblem(message=f"{self.format_element(e)} has no title")
                yield problem


class NoXsdIntTypeRule(LinterRule):
    id = "no_xsd_int_type"

    def check(self, schema_view: SchemaView, fix: bool = False):
        for type_definition in schema_view.all_types(imports=False).values():
            if type_definition.uri == "xsd:int":
                if fix:
                    type_definition.uri = "xsd:integer"
                else:
                    yield LinterProblem(f"{self.format_element(type_definition)} has uri xsd:int")


class PermissibleValuesFormatRule(LinterRule):
    id = "permissible_values_format"

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        pattern = self.PATTERNS.get(self.config.format, re.compile(self.config.format))
        for enum_def in schema_view.all_enums(imports=False).values():
            for value in enum_def.permissible_values:
                if pattern.fullmatch(value) is None:
                    yield LinterProblem(f"{self.format_element(enum_def)} has permissible value '{value}'")


@cache
def _get_recommended_metamodel_slots() -> list[str]:
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

    # todo PVs are not checked for recommended fields yet

    def __init__(self, config: RecommendedRuleConfig) -> None:
        self.config = config

    def check(self, schema_view: SchemaView, fix: bool = False):
        recommended_meta_slots = _get_recommended_metamodel_slots()
        excluded_types = [t.text if hasattr(t, "text") else str(t) for t in getattr(self.config, "exclude_type", [])]
        for element_name, element_definition in schema_view.all_elements(imports=False).items():
            element_type_name = type(element_definition).class_name
            if self.config.include and element_name not in self.config.include:
                continue
            if element_name in self.config.exclude:
                continue
            if element_type_name in excluded_types:
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

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        tree_roots = [c for c in schema_view.all_classes(imports=False).values() if c.tree_root]
        if len(tree_roots) > 0:
            if self.config.validate_existing_class_name:
                for tree_root in tree_roots:
                    if str(tree_root.name) != self.config.root_class_name:
                        yield LinterProblem(message=f"Tree root class has an invalid name '{tree_root.name}'")
            if len(tree_roots) > 1:
                yield LinterProblem("Schema has more than one class with `tree_root: true`")
        elif fix:
            container = ClassDefinition(self.config.root_class_name, tree_root=True)
            schema_view.add_class(container)
            self.add_index_slots(schema_view, container.name)
        else:
            yield LinterProblem("Schema does not have class with `tree_root: true`")

    def add_index_slots(
        self,
        schema_view: SchemaView,
        container_name: ClassDefinitionName,
        inlined_as_list: bool = False,
        must_have_identifier: bool = False,
        slot_name_func: Callable | None = None,
        convert_camel_case: bool = False,
    ) -> list[SlotDefinition]:
        """Add index slots to a container pointing at all top-level classes.

        :param schema: input schema, will be modified in place
        :param container_name:
        :param inlined_as_list:
        :param must_have_identifier:
        :param slot_name_func: function to determine the name of the slot from the class
        :return: new slots
        """
        container = schema_view.get_class(container_name)
        ranges = {s.range for cn in schema_view.all_classes() for s in schema_view.class_induced_slots(cn)}
        top_level_classes = [c for c in schema_view.all_classes().values() if not c.tree_root and c.name not in ranges]
        if must_have_identifier:
            top_level_classes = [c for c in top_level_classes if schema_view.get_identifier_slot(c.name) is not None]
        index_slots: list[SlotDefinition] = []
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


class NoUndeclaredSlotsRule(LinterRule):
    """Linter rule to check that all slots from a class have been declared in the `slots` section."""

    id = "no_undeclared_slots"

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        """Perform the check for undeclared slots.

        :param schema_view: schema to be checked in a SchemaView object.
        :type schema_view: SchemaView
        :param fix: whether or not to fix, defaults to False
        :type fix: bool, optional
        :yield: iterable of error messages about non-compliant slots.
        :rtype: Iterator[Iterable[LinterProblem]]
        """
        all_slots = schema_view.all_slots()
        for class_name in schema_view.all_classes():
            for slot_name in schema_view.class_slots(class_name):
                if slot_name not in all_slots:
                    yield LinterProblem(
                        f"Slot '{slot_name}' from class '{class_name}' not found in schema 'slots' declaration."
                    )


class NoInvalidSlotUsageRule(LinterRule):
    id = "no_invalid_slot_usage"

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        for class_name, class_definition in schema_view.all_classes(imports=False).items():
            slot_usage = class_definition.slot_usage
            if not slot_usage:
                continue
            class_slots = schema_view.class_slots(class_name)
            for slot_usage_name in slot_usage:
                if slot_usage_name not in class_slots:
                    yield LinterProblem(f"Slot '{slot_usage_name}' not found on class '{class_name}'")


class NoUndeclaredRangesRule(LinterRule):
    id = "no_undeclared_ranges"

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        all_types: dict[TypeDefinitionName, TypeDefinition] = schema_view.all_types()
        all_enums: dict[EnumDefinitionName, EnumDefinition] = schema_view.all_enums()
        all_classes: dict[ClassDefinitionName, ClassDefinition] = schema_view.all_classes()
        all_possible_ranges: set[TypeDefinitionName | EnumDefinitionName | ClassDefinitionName] = (
            set(all_types) | set(all_enums) | set(all_classes)
        )

        # check that the default_range has a valid value
        default_range = schema_view.schema.default_range
        if default_range and default_range not in all_possible_ranges:
            yield LinterProblem(f"Schema default_range '{default_range}' is not defined.")

        for class_name in schema_view.all_classes():
            for slot in schema_view.class_induced_slots(class_name):
                slot_range: set[ElementName] = set(schema_view.slot_range_as_union(slot))

                # check slot range is valid
                for range_name in slot_range:
                    if range_name not in all_possible_ranges:
                        yield LinterProblem(
                            f"Class '{class_name}' slot '{slot.name}' range '{range_name}' is not defined."
                        )


class RootTypeChecks(LinterRule):
    """Performs basic checks on types.

    Types can be defined as subtypes of existing types using the `typeof` attribute.
    Root types are those types that do not inherit from other types using `typeof`.

    - types used in 'typeof' statements must be defined in the types section
    - types cannot be their own 'typeof' parent
    - every root type must have a 'base'
    - every root type must have a 'uri'

    :param LinterRule: linter rule class
    :type LinterRule: LinterRule
    """

    id = "root_type_checks"

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        type_ix = schema_view.all_types()
        for t, type_def in type_ix.items():
            if type_def.typeof:
                # This is a child type. Ensure that the parent exists.
                if type_def.typeof not in schema_view.all_types():
                    yield LinterProblem(f"'{t}' has invalid typeof parent '{type_def.typeof}'")
                # Ensure that a type is not its own parent.
                # N.b. at some point, this can/should be extended to checking the full 'typeof' ancestor chain
                # for circular inheritance.
                if type_def.typeof == type_def.name:
                    yield LinterProblem(f"'{t}' has invalid circular typeof parent '{type_def.typeof}'")
                continue
            if not type_def.base:
                yield LinterProblem(f"Root type '{t}' is missing the required 'base' attribute")

            if not type_def.uri:
                yield LinterProblem(f"Root type '{t}' is missing the required 'uri' attribute")


class StandardNamingRule(LinterRule):
    id = "standard_naming"

    def __init__(self, config: StandardNamingConfig) -> None:
        self.config = config

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        excluded_types = [t.text if hasattr(t, "text") else str(t) for t in getattr(self.config, "exclude_type", [])]
        excluded_names = set(getattr(self.config, "exclude", []))

        # element naming patterns indexed by element type
        pattern = {
            "class": (
                self.PATTERNS["uppercamel"]
                if not self.config.class_pattern
                else self.PATTERNS.get(self.config.class_pattern, re.compile(self.config.class_pattern))
            ),
            "slot": (
                self.PATTERNS["snake"]
                if not self.config.slot_pattern
                else self.PATTERNS.get(self.config.slot_pattern, re.compile(self.config.slot_pattern))
            ),
            "enum": self.PATTERNS["uppercamel"],
            "permissible_value": self.PATTERNS["uppersnake"]
            if self.config.permissible_values_upper_case
            else self.PATTERNS["snake"],
        }

        # explicit method mapping for better readability and maintainability
        element_extractors = {
            "class": schema_view.all_classes,
            "slot": schema_view.all_slots,
            "enum": schema_view.all_enums,
        }

        # cache the results to avoid repeated method calls
        cached_elements = {el_type: element_extractors[el_type]() for el_type in element_extractors}

        # generate LinterProblems for classes, slots, and enums incrementally
        problems = (
            LinterProblem(f"{el_type.capitalize()} has name '{el_name}'")
            for el_type, elements in cached_elements.items()
            for el_name in elements
            if f"{el_type}_definition" not in excluded_types
            and el_name not in excluded_names
            and pattern[el_type].fullmatch(el_name) is None
        )

        if "permissible_value" not in excluded_types:
            # add issues from the permissible values, if appropriate
            pv_problems = (
                LinterProblem(f"Permissible value of Enum '{en}' has name '{pv}'")
                for en, en_def in schema_view.all_enums(imports=False).items()
                for pv in en_def.permissible_values
                if pv not in excluded_names and pattern["permissible_value"].fullmatch(pv) is None
            )
            # chain the generators together
            return chain(problems, pv_problems)

        return iter(problems)


class CanonicalPrefixesRule(LinterRule):
    id = "canonical_prefixes"

    def __init__(self, config: CanonicalPrefixesConfig) -> None:
        self.config = config

    def check(self, schema_view: SchemaView, fix: bool = False) -> Iterable[LinterProblem]:
        context = load_multi_context(self.config.prefixmaps_contexts)
        prefix_to_namespace = context.as_dict()
        namespace_to_prefix = context.as_inverted_dict()
        for prefix in schema_view.schema.prefixes.values():
            if (
                prefix.prefix_prefix in prefix_to_namespace
                and prefix.prefix_reference != prefix_to_namespace[prefix.prefix_prefix]
            ):
                yield LinterProblem(
                    f"Schema maps prefix '{prefix.prefix_prefix}' to namespace "
                    f"'{prefix.prefix_reference}' instead of namespace "
                    f"'{prefix_to_namespace[prefix.prefix_prefix]}'"
                )
            if (
                prefix.prefix_reference in namespace_to_prefix
                and prefix.prefix_prefix != namespace_to_prefix[prefix.prefix_reference]
            ):
                yield LinterProblem(
                    f"Schema maps prefix '{prefix.prefix_prefix}' to namespace "
                    f"'{prefix.prefix_reference}' instead of using prefix "
                    f"'{namespace_to_prefix[prefix.prefix_reference]}'"
                )
