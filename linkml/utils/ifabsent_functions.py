import re
from typing import Callable, List, Match, Optional, Text, Tuple

from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import sfx

from linkml.utils.schemaloader import SchemaLoader


def strval(txt: str) -> str:
    txt = str(txt).replace('"', '\\"')
    return f'"{txt}"'


def default_uri_for(loader: SchemaLoader) -> str:
    dflt = (
        loader.schema.default_prefix
        if loader.schema.default_prefix
        else sfx(loader.schema.id)
    )
    return sfx(loader.namespaces.uri_for(dflt))


def default_curie_or_uri(loader: SchemaLoader) -> str:
    dflt = (
        loader.schema.default_prefix
        if loader.schema.default_prefix
        else sfx(loader.schema.id)
    )
    if ":/" in dflt:
        prefix = loader.namespaces.prefix_for(loader.schema.default_prefix)
        if prefix:
            dflt = prefix
    return dflt


def curie_for(loader: SchemaLoader, is_class: bool) -> Optional[str]:
    """Return the Curie for the schema in loader.  Return None if there is no curie form"""
    prefix = default_curie_or_uri(loader)
    suffix = (
        "camelcase(self.name)"
        if is_class
        else "underscore(self.alias if self.alias else self.name)"
    )
    if ":/" not in prefix:
        return '"' + prefix + ":" + '" + ' + suffix
    else:
        pn = loader.namespaces.curie_for(prefix, default_ok=False)
        return ('"' + pn + '" + ' + suffix) if pn else None


def uri_for(s: str, loader: SchemaLoader) -> str:
    uri = str(loader.namespaces.uri_for(s))
    return loader.namespaces.curie_for(uri, True, True) or strval(uri)


def default_ns_for(loader: SchemaLoader, cls: ClassDefinition) -> str:
    """Return code to produce the default namespace for the supplied class"""
    # TODO: figure out how to mark a slot as a namespace
    return "sfx(str(self.id))" if "id" in cls.slots else "None"
    # cls_id = None
    # for slotname in cls.slots:
    #     slot = loader.schema.slots[slotname]
    #     if slot.identifier:
    #         cls_id = slotname
    # return f"sfx(str(self.{cls_id}))" if cls_id else "None"


# Library of named default values -- this is here to prevent code injection
# Contents: Match text (as re),
#           flag that indicates whether we're generating a default value expression or postinig code
#           Function that takes the match string, SchemaLoader, ClassDefinition, and SlotDefinition and returns the
#           appropriate string
default_library: List[
    Tuple[
        Text,
        bool,
        Callable[[Match[str], SchemaLoader, ClassDefinition, SlotDefinition], str],
    ]
] = [
    (r"[Tt]rue", False, lambda _, __, ___, ____: "True"),
    (r"[Ff]alse", False, lambda _, __, ___, ____: "False"),
    (r"int\((-?[1-9][0-9]*)\)", False, lambda m, __, ___, ____: int(m[1])),
    # TODO: We have to make the real URI available before any of these can work
    # ("class_uri", True, lambda _, loader, ___, ____: f'"{default_uri_for(loader)}" + camelcase(self.name)'),
    # ("slot_uri", True, lambda _, loader, ___, ____: f'"{default_uri_for(loader)}" + underscore(self.alias if self.alias else self.name)'),
    # ("class_curie", True, lambda _, loader, ___, ____: curie_for(loader, True)),
    # ("slot_curie", True, lambda _, loader, ___, ____: curie_for(loader, False)),
    ("class_uri", True, lambda _, loader, ___, ____: "None"),
    ("slot_uri", True, lambda _, loader, ___, ____: "None"),
    ("class_curie", True, lambda _, loader, ___, ____: "None"),
    ("slot_curie", True, lambda _, loader, ___, ____: "None"),
    # TODO: If you assign a range in the constructor, mergeutils has no way of knowing whether the range
    #       was overridden or just defaulted.  We need to let the old code continue to work until we get
    #       this bit resolved
    # ("default_range", False, lambda _, loader, __, ____: f"ElementName({strval(loader.schema.default_range)})"),
    ("default_range", False, lambda _, __, ___, ____: "None"),
    ("bnode", False, lambda _, __, ___, ____: "bnode()"),
    (r"string\((.*)\)", False, lambda m, __, ___, ____: strval(m[1])),
    (r"uri\((.*)\)", False, lambda m, loader, _, __: uri_for(m[1], loader)),
    ("default_ns", True, lambda _, loader, cls, ____: default_ns_for(loader, cls)),
]


def isabsent_match(
    txt: Text,
) -> Optional[
    Tuple[
        Match[str],
        bool,
        Callable[[Match[str], SchemaLoader, ClassDefinition, SlotDefinition], str],
    ]
]:
    txt = str(txt)
    for pattern, postinit, f in default_library:
        m = re.match(pattern + "$", txt)
        if m:
            return m, postinit, f


def ifabsent_value_declaration(txt: Text, loader, cls, slot) -> Optional[str]:
    m, postinit, f = isabsent_match(txt)
    if m and not postinit:
        return f(m, loader, cls, slot)


def ifabsent_postinit_declaration(txt: Text, loader, cls, slot) -> Optional[str]:
    m, postinit, f = isabsent_match(txt)
    if m and postinit:
        return f(m, loader, cls, slot)
