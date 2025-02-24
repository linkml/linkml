from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterator, List, Optional

from linkml_runtime import SchemaView
from linkml_runtime.linkml_model import ClassDefinition, Element, SlotDefinition

from linkml.validator import JsonschemaValidationPlugin
from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


@dataclass
class URIMapping:
    uri: str
    element: Element
    schema_view: SchemaView


def get_uri_mappings(schema_views: List[SchemaView]) -> List[URIMapping]:
    mappings = []
    for sv in schema_views:
        for elt in sv.all_elements().values():
            uri = sv.get_uri(expand=True, native=False)
            mappings.append(URIMapping(uri=uri, element=elt, schema_view=sv))
    return mappings


class SchemaValidationPlugin(ValidationPlugin):
    """A validation plugin which validates instances of the LinkML metamodel.

    TODO: decide if this should remain a plugin; other plugins
    are particular to *methods* of validation; this is particular to a *schema*
    (the metamodel).

    :param closed: If ``True``, additional properties are not allowed on instances.
        Defaults to ``False``.
    """

    def __init__(self, wrapped_plugin: ValidationPlugin = None) -> None:
        if wrapped_plugin is None:
            wrapped_plugin = JsonschemaValidationPlugin()
        self.wrapped_plugin = wrapped_plugin

    def process(self, instance: Any, context: ValidationContext) -> Iterator[ValidationResult]:
        """Perform validation on the provided schema

        :param instance: The instance to validate (must be a schema)
        :param context: The validation context which provides a Pydantic artifact
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        yield from self.wrapped_plugin.process(instance, context)

    def validate_implements(self, schema_view: SchemaView, context: ValidationContext) -> Iterator[ValidationResult]:
        """Validate that the schema implements the LinkML metamodel

        :param schema_view: The schema to validate
        :param context: The validation context
        :return: Iterator over validation results
        :rtype: Iterator[ValidationResult]
        """
        uri_mappings = get_uri_mappings([schema_view])
        uri_mappings_by_uri = {m.uri: m for m in uri_mappings}

        def lookup(uri_or_curie: str) -> Optional[URIMapping]:
            uri = schema_view.get_uri(uri_or_curie, expand=True, native=False)
            return uri_mappings_by_uri.get(uri, None)

        def ensure_consistent(child_att: SlotDefinition, parent_att: SlotDefinition) -> Iterator[ValidationResult]:
            for k in ["multivalued", "required"]:
                if getattr(child_att, k) != getattr(parent_att, k):
                    yield ValidationResult(
                        type="schema validation",
                        severity=Severity.ERROR,
                        instance=child_att,
                        instantiates=child_att.name,
                        message=f"Slot '{child_att.name}' has inconsistent '{k}' with parent '{parent_att.name}'",
                    )
            # TODO: Range
            return

        for cls in schema_view.all_classes().values():
            child_atts = schema_view.class_induced_slots(cls.name)
            att_impl_map = defaultdict(list)
            rev_att_impl_map = defaultdict(list)
            for att in child_atts:
                for att_impl in att.implements:
                    parent_att = lookup(att_impl)
                    if not parent_att:
                        continue
                    if not isinstance(parent_att, SlotDefinition):
                        raise ValueError(f"Expected slot definition for '{att.implements}'")
                    att_impl_map[att.name] += [att_impl]
                    rev_att_impl_map[att_impl.name] += [att]
                    yield from ensure_consistent(att, parent_att)
            for impl in cls.implements:
                parent_cls = lookup(impl)
                if not parent_cls:
                    continue
                if not isinstance(parent_cls, ClassDefinition):
                    raise ValueError(f"Expected class definition for '{impl}'")
                parent_atts = schema_view.class_induced_slots(parent_cls.name)
                for parent_att in parent_atts:
                    if parent_att.required:
                        child_att = rev_att_impl_map.get(parent_att.name, [])
                        if not any([att.required for att in child_att]):
                            yield ValidationResult(
                                type="schema validation",
                                severity=Severity.ERROR,
                                instance=cls,
                                instantiates=cls.name,
                                message=f"Class '{cls.name}' does not require slot '{parent_att.name}'",
                            )
