import dataclasses
from copy import deepcopy
from typing import Dict, Optional, Union, cast, List

from rdflib import URIRef

from linkml_runtime.linkml_model.meta import SchemaDefinition, Element, SlotDefinition, ClassDefinition, TypeDefinition, \
    SlotDefinitionName, TypeDefinitionName, EnumDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.yamlutils import extended_str


def merge_schemas(target: SchemaDefinition, mergee: SchemaDefinition, imported_from: Optional[str] = None,
                  namespaces: Optional[Namespaces] = None, merge_imports: bool = True) -> None:
    """ Merge mergee into target """
    assert target.name is not None, "Schema name must be supplied"
    if target.license is None:
        target.license = mergee.license

    target.imports += [imp for imp in mergee.imports if imp not in target.imports]
    set_from_schema(mergee)

    if namespaces:
        merge_namespaces(target, mergee, namespaces)

    if merge_imports:
        for prefix in mergee.emit_prefixes:
            if prefix not in target.emit_prefixes:
                target.emit_prefixes.append(prefix)

    if imported_from is None:
        imported_from_uri = None
    else:
        if imported_from.startswith("http") or ":" not in imported_from:
            imported_from_uri = imported_from
        else:
            imported_from_uri = namespaces.uri_for(imported_from)
    merge_dicts(target.classes, mergee.classes, imported_from, imported_from_uri, merge_imports)
    merge_dicts(target.slots, mergee.slots, imported_from, imported_from_uri, merge_imports)
    merge_dicts(target.types, mergee.types, imported_from, imported_from_uri, merge_imports)
    merge_dicts(target.subsets, mergee.subsets, imported_from, imported_from_uri, merge_imports)
    merge_dicts(target.enums, mergee.enums, imported_from, imported_from_uri, merge_imports)


def merge_namespaces(target: SchemaDefinition, mergee: SchemaDefinition, namespaces) -> None:
    """
    Add the mergee namespace definitions to target

    :param target:
    :param mergee:
    :param namespaces:
    :return:
    """
    for prefix in mergee.prefixes.values():
        namespaces[prefix.prefix_prefix] = prefix.prefix_reference
        # if prefix.prefix_prefix not in target.prefixes:
        #     target.prefixes[prefix.prefix_prefix] = prefix
        if prefix.prefix_prefix in target.prefixes and \
                target.prefixes[prefix.prefix_prefix].prefix_reference != prefix.prefix_reference:
            raise ValueError(f'Prefix: {prefix.prefix_prefix} mismatch between {target.name} and {mergee.name}')
    for mmap in mergee.default_curi_maps:
        namespaces.add_prefixmap(mmap)


def set_from_schema(schema: SchemaDefinition) -> None:
    for t in [schema.subsets, schema.classes, schema.slots, schema.types, schema.enums]:
        for k in t.keys():
            t[k].from_schema = schema.id
            if isinstance(t[k], SlotDefinition):
                fragment = underscore(t[k].name)
            else:
                fragment = camelcase(t[k].name)
            if schema.default_prefix in schema.prefixes:
                ns = schema.prefixes[schema.default_prefix].prefix_reference
            else:
                ns = str(URIRef(schema.id) + "/")
            t[k].definition_uri = f'{ns}{fragment}'


def merge_dicts(target: Dict[str, Element], source: Dict[str, Element], imported_from: str,
                imported_from_uri: str, merge_imports: bool) -> None:
    for k, v in source.items():
        if k in target and source[k].from_schema != target[k].from_schema:
            raise ValueError(f"Conflicting URIs ({source[k].from_schema}, {target[k].from_schema}) for item: {k}")
        target[k] = deepcopy(v)
        # currently all imports closures are merged into main schema, EXCEPT
        # internal linkml types, which are considered separate
        # https://github.com/linkml/issues/121
        if imported_from is not None:
            if not merge_imports or imported_from.startswith("linkml") or \
                    imported_from_uri.startswith("https://w3id.org/biolink/linkml"):
                target[k].imported_from = imported_from


def merge_slots(target: Union[SlotDefinition, TypeDefinition], source: Union[SlotDefinition, TypeDefinition],
                skip: List[Union[SlotDefinitionName, TypeDefinitionName]] = None, inheriting: bool = True) -> None:
    """
    Merge slot source into target

    :param target: slot to merge into
    :param source: slot to be merged from
    :param skip: Properties to not merge (used to prevent provenance such as 'inherited from' from propagating)
    :param inheriting: True means source is the parent.  False means that everything gets copied
    """
    if skip is None:
        skip = []
    for k, v in dataclasses.asdict(source).items():
        if k not in skip and v is not None and (not inheriting or getattr(target, k, None) is None):
            if k in source._inherited_slots or not inheriting:
                setattr(target, k, deepcopy(v))
            else:
                setattr(target, k, None)
    target.__post_init__()


def slot_usage_name(usage_name: SlotDefinitionName, owning_class: ClassDefinition) -> SlotDefinitionName:
    """
     Synthesize a unique name for an overridden slot

    :param usage_name:
    :param owning_class:
    :return: Synthesized name
    """
    return SlotDefinitionName(extended_str.concat(owning_class.name, '_', usage_name))


def alias_root(schema: SchemaDefinition, slotname: SlotDefinitionName) -> Optional[SlotDefinitionName]:
    """ Return the ultimate alias of a slot """
    alias = schema.slots[slotname].alias if slotname in schema.slots else None
    if alias and alias == slotname:
        raise ValueError("Error: Slot {slotname} is aliased to itself.")
    return alias_root(schema, cast(SlotDefinitionName, alias)) if alias else slotname


def merge_classes(schema: SchemaDefinition, target: ClassDefinition, source: ClassDefinition,
                  at_end: bool = False) -> None:
    """ Merge the slots in source into target

    :param schema: Containing schema
    :param target: mergee
    :param source: class to merge
    :param at_end: True means add mergee to the end.  False to the front
    """

    # List of grounded slots referenced in the target class
    target_base_slots = set(alias_root(schema, s) for s in target.slots)

    for slotname in source.slots if at_end else source.slots[::-1]:
        slotbase = alias_root(schema, slotname)
        if slotbase in target.slot_usage:
            slotname = slot_usage_name(slotbase, target)
        if slotbase not in target_base_slots:
            target.slots.append(slotname) if at_end else target.slots.insert(0, slotname)
            target_base_slots.add(slotbase)


def merge_enums(schema: SchemaDefinition, target: EnumDefinition, source: EnumDefinition,
                  at_end: bool = False) -> None:
    """ Merge the slots in source into target

    :param schema: Containing schema
    :param target: mergee
    :param source: enum to merge
    :param at_end: True means add mergee to the end.  False to the front
    """
    # TODO: Finish enumeration merge code
    pass
