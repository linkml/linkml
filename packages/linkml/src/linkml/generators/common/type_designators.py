from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.uri_validator import validate_uri


def get_type_designator_value(sv: SchemaView, type_designator_slot: SlotDefinition, class_def: ClassDefinition) -> str:
    """
    returns the correct value for a type designator field for a given class, depending on its range
    this implements the logic described in https://github.com/linkml/linkml/issues/945:
    """
    slot_types = set(sv.type_ancestors(type_designator_slot.range))
    if "uri" in slot_types:
        return sv.get_uri(class_def, expand=True, native=False)
    elif "uriorcurie" in slot_types:
        return sv.get_uri(class_def, expand=False, native=False)
    elif "string" in slot_types:
        return class_def.name
    else:
        return sv.get_uri(class_def, expand=False, native=False)


def get_uriorcurie_type_designator_values(sv: SchemaView, class_def: ClassDefinition) -> list[str]:
    """Return the URI and CURIE forms of a class's effective ``class_uri``.

    The native ``definition_uri`` is intentionally not included.  Consumers
    that support native aliases have a separate, more permissive policy.
    """
    compact_value = sv.get_uri(class_def, expand=False, native=False)
    uri_value = sv.get_uri(class_def, expand=True, native=False)

    if compact_value == uri_value and validate_uri(uri_value):
        compact_value = sv.namespaces().curie_for(uri_value)

    values = [value for value in (compact_value, uri_value) if value is not None]
    return list(dict.fromkeys(values))


def get_accepted_type_designator_values(
    sv: SchemaView, type_designator_slot: SlotDefinition, class_def: ClassDefinition
) -> list[str]:
    """
    returns the accepted values for a type designator field for a given class, depending on its range
    this implements the logic described in https://github.com/linkml/linkml/issues/945:
    """
    accepted_uri_values = [
        sv.get_uri(class_def, expand=True, native=True),
        sv.get_uri(class_def, expand=True, native=False),
        sv.get_uri(class_def, expand=False, native=True),
        sv.get_uri(class_def, expand=False, native=False),
    ]
    # unique, but with order preserved (https://stackoverflow.com/a/17016257)
    accepted_uri_values = list(dict.fromkeys(accepted_uri_values))

    slot_types = set(sv.type_ancestors(type_designator_slot.range))
    uri_types = ["uri", "uriorcurie"]

    if slot_types.intersection(uri_types):
        return accepted_uri_values
    elif type_designator_slot.range == "string":
        return [class_def.name]
    else:
        return accepted_uri_values
