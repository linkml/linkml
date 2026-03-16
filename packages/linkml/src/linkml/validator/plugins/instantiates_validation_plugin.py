"""Validation plugin that enforces constraints from ``instantiates`` annotations.

When a class declares ``instantiates: [SomeClass]``, and ``SomeClass`` carries
annotations such as ``must_not_have_id_slot: true`` or ``must_be_inlined: true``,
this plugin verifies that the instantiating class actually satisfies those
constraints.

Supported annotations on the instantiated class:

* ``must_not_have_id_slot`` – the instantiating class must **not** define an
  identifier slot.
* ``must_be_inlined`` – every slot in the schema whose range is the
  instantiating class must have ``inlined: true`` (or ``inlined_as_list: true``).
"""

from __future__ import annotations

from collections.abc import Iterator

from linkml_runtime.utils.schemaview import SchemaView

from linkml.validator.plugins.validation_plugin import ValidationPlugin
from linkml.validator.report import Severity, ValidationResult
from linkml.validator.validation_context import ValidationContext


def _check_must_not_have_id_slot(
    class_name: str,
    instantiated_name: str,
    schema_view: SchemaView,
) -> Iterator[ValidationResult]:
    """Yield a result if *class_name* has an identifier slot."""
    id_slot = schema_view.get_identifier_slot(class_name)
    if id_slot is not None:
        yield ValidationResult(
            type="instantiates",
            severity=Severity.ERROR,
            message=(
                f"Class '{class_name}' instantiates '{instantiated_name}' which "
                f"requires no identifier slot, but '{class_name}' has identifier "
                f"slot '{id_slot.name}'"
            ),
        )


def _check_must_be_inlined(
    class_name: str,
    instantiated_name: str,
    schema_view: SchemaView,
) -> Iterator[ValidationResult]:
    """Yield a result for each slot whose range is *class_name* but is not inlined."""
    for owner_class_name in schema_view.all_classes():
        for slot in schema_view.class_induced_slots(owner_class_name):
            if slot.range != class_name:
                continue
            if not (slot.inlined or slot.inlined_as_list):
                yield ValidationResult(
                    type="instantiates",
                    severity=Severity.ERROR,
                    message=(
                        f"Class '{class_name}' instantiates '{instantiated_name}' which "
                        f"requires inlined usage, but slot '{slot.name}' on class "
                        f"'{owner_class_name}' has range '{class_name}' without "
                        f"inlined=true"
                    ),
                )


# Maps annotation tag → checker function
_ANNOTATION_CHECKERS = {
    "must_not_have_id_slot": _check_must_not_have_id_slot,
    "must_be_inlined": _check_must_be_inlined,
}


def check_instantiates_constraints(schema_view: SchemaView) -> Iterator[ValidationResult]:
    """Check all ``instantiates`` constraints across the schema.

    For every class that has ``instantiates``, look up each instantiated class,
    read its annotations, and delegate to the appropriate checker.

    :param schema_view: A :class:`SchemaView` over the schema to check.
    :return: An iterator of :class:`ValidationResult` for any violations found.
    """
    for class_name, class_def in schema_view.all_classes().items():
        if not class_def.instantiates:
            continue

        for instantiated_uri in class_def.instantiates:
            instantiated_class = schema_view.get_class(str(instantiated_uri))
            if instantiated_class is None:
                yield ValidationResult(
                    type="instantiates",
                    severity=Severity.WARN,
                    message=(
                        f"Class '{class_name}' instantiates '{instantiated_uri}' "
                        f"which could not be resolved in the schema"
                    ),
                )
                continue

            annotations = instantiated_class.annotations or {}
            for annotation_tag, checker_fn in _ANNOTATION_CHECKERS.items():
                annotation = annotations.get(annotation_tag)
                if annotation is None:
                    continue
                # Annotation value may be an Annotation object or a raw value
                value = getattr(annotation, "value", annotation)
                if str(value).lower() in ("true", "1", "yes"):
                    yield from checker_fn(class_name, str(instantiated_uri), schema_view)


class InstantiatesValidationPlugin(ValidationPlugin):
    """Validation plugin that checks ``instantiates`` annotation constraints.

    This plugin performs schema-level checks: it verifies that classes using
    ``instantiates`` comply with annotations on the instantiated classes.
    Results are computed once and yielded on the first ``process()`` call.
    """

    def __init__(self) -> None:
        self._results: list[ValidationResult] | None = None

    def pre_process(self, context: ValidationContext) -> None:
        """Compute and cache schema-level validation results."""
        self._results = list(check_instantiates_constraints(context.schema_view))

    def process(self, instance: dict, context: ValidationContext) -> Iterator[ValidationResult]:
        """Yield any cached schema-level results, then clear them.

        Since instantiates constraints are schema-level (not per-instance),
        results are yielded only once, on the first call to ``process()``.
        """
        if self._results:
            yield from self._results
            self._results = []
