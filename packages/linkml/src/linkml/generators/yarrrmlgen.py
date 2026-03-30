from __future__ import annotations

import os
from typing import Any, TextIO

import click
import yaml

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView


class FlowList(list):
    pass


def flow_list_representer(dumper, data):
    # Ensures that specific lists (like sources and condition parameters)
    # are serialized in flow style, e.g., [data.json~jsonpath, '$[*]']
    # This prevents unreadable block sequences that break some YAML parsers (like Matey).
    return dumper.represent_sequence(
        "tag:yaml.org,2002:seq",
        data,
        flow_style=True
    )


class YarrrmlDumper(yaml.SafeDumper):
    pass


YarrrmlDumper.add_representer(FlowList, flow_list_representer)

DEFAULT_SOURCE_JSON = "data.json~jsonpath"
DEFAULT_ITERATOR = "$[*]"


class YarrrmlGenerator(Generator):
    generatorname = os.path.basename(__file__)
    generatorversion = "0.3.0"
    valid_formats = ["yml", "yaml"]
    visit_all_class_slots = False

    def __init__(self, schema: str | TextIO | SchemaDefinition, format: str = "yml", **kwargs):
        raw_src = kwargs.pop("source", None)
        it = kwargs.pop("iterator_template", None)
        super().__init__(schema, **kwargs)

        self.schemaview = SchemaView(schema)
        self.schema: SchemaDefinition = self.schemaview.schema
        self.format = format
        self.source: str = self._infer_source_suffix(raw_src) if raw_src else DEFAULT_SOURCE_JSON
        if it:
            self.iterator_template = it
        else:
            has_tree_root = any(c.tree_root for c in self.schemaview.all_classes().values())
            self.iterator_template = "$" if has_tree_root else DEFAULT_ITERATOR

    def _infer_source_suffix(self, path: str) -> str:
        p = (path or "").lower()
        if "~" in p:
            return path
        if p.endswith(".json"):
            return f"{path}~jsonpath"
        if p.endswith(".csv") or p.endswith(".tsv"):
            return f"{path}~csv"
        return path

    def serialize(self, **args) -> str:
        data = yaml.dump(
            self.as_dict(), Dumper=YarrrmlDumper, sort_keys=False, allow_unicode=True, indent=2, width=120
        )
        return data

    def as_dict(self) -> dict[str, Any]:
        sv = self.schemaview
        mappings: dict[str, Any] = {}

        inline_owners: dict[str, list[tuple[str, str]]] = {}

        # Discover parent-child relationships for inlined objects
        for owner in sv.all_classes().values():
            for s in sv.class_induced_slots(owner.name):
                if not s.range:
                    continue

                range_cls = sv.get_class(s.range)
                if range_cls is None:
                    continue

                decl = sv.get_slot(s.name)
                inlined = s.inlined
                multivalued = getattr(decl or s, "multivalued", False)

                has_id = False
                if range_cls:
                    has_id = (
                        sv.get_identifier_slot(range_cls.name) is not None
                        or sv.get_key_slot(range_cls.name) is not None
                    )

                if inlined is None:
                    inlined = not has_id

                if inlined:
                    # Prevent generating mappings for multivalued inlined objects without an identifier,
                    # as this would result in merging multiple array elements into a single blank node.
                    if multivalued and not has_id:
                        raise ValueError(
                            f"Slot '{s.name}' in class '{owner.name}' is an inlined list (multivalued: true), "
                            f"but the target class '{range_cls.name}' lacks an identifier. "
                            f"Please add `identifier: true` to a slot in '{range_cls.name}'."
                        )

                    alias = decl.alias if decl and decl.alias else s.alias
                    var = alias or s.name
                    inline_owners.setdefault(range_cls.name, []).append((owner.name, var))

        # Validate that ID-less inline classes are strictly owned by a single parent class
        for child_class, owners in inline_owners.items():
            has_id = sv.get_identifier_slot(child_class) is not None or sv.get_key_slot(child_class) is not None
            if len(owners) > 1 and not has_id:
                owner_names = [o[0] for o in owners]
                raise ValueError(
                    f"Inline class '{child_class}' without an identifier is used by multiple owners: {owner_names}. "
                    f"This is not supported. Please assign an identifier to '{child_class}'."
                )

        has_tree_root_anywhere = any(c.tree_root for c in sv.all_classes().values())

        # Build YARRRML mappings blocks
        for cls in sv.all_classes().values():
            if cls.mixin:
                continue

            if self._is_json_source() and has_tree_root_anywhere:
                if not cls.tree_root and cls.name not in inline_owners:
                    continue

            mapping_dict: dict[str, Any] = {}
            has_own_id = sv.get_identifier_slot(cls.name) or sv.get_key_slot(cls.name)

            if self._is_json_source():
                if cls.name in inline_owners:
                    owners = inline_owners[cls.name]
                    sources = []

                    owner_name, slot_var = owners[0]

                    is_multi = False
                    for s in sv.class_induced_slots(owner_name):
                        if (s.alias or s.name) == slot_var:
                            is_multi = s.multivalued
                            break

                    if not has_own_id:
                        # Iterate over the parent's array, we will access child properties via dot notation
                        owner_cls = sv.get_class(owner_name)
                        iterator = self._iterator_for_class(owner_cls)
                    else:
                        # Iterate directly over the nested child array
                        iterator = f"$..{slot_var}[*]" if is_multi else f"$..{slot_var}"

                    sources.append(FlowList([self.source, iterator]))
                    mapping_dict["sources"] = sources

                else:
                    mapping_dict["sources"] = [FlowList([self.source, self._iterator_for_class(cls)])]
            else:
                mapping_dict["sources"] = [[self.source]]

            subject = self._subject_template_for_class(cls, inline_owners)
            if subject is not None:
                mapping_dict["s"] = subject

            mapping_dict["po"] = self._po_list_for_class(cls, inline_owners)

            mappings[str(cls.name)] = mapping_dict

        prefixes = self._prefixes_with_defaults()
        return {"prefixes": prefixes, "mappings": mappings}

    def _is_json_source(self) -> bool:
        return "~jsonpath" in (self.source or "")

    def _prefixes_with_defaults(self) -> dict[str, str]:
        px: dict[str, str] = {}

        if self.schema.prefixes:
            for p in self.schema.prefixes.values():
                if p.prefix_prefix and p.prefix_reference:
                    px[str(p.prefix_prefix)] = str(p.prefix_reference)

        px.setdefault("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

        has_user_prefix = any(k not in ("rdf", "linkml") for k in px)
        if not has_user_prefix:
            px.setdefault("ex", "https://example.org/default#")

        if not self.schema.default_prefix:
            if "ex" in px:
                self.schema.default_prefix = "ex"
            else:
                for k in px:
                    if k not in ("rdf", "linkml"):
                        self.schema.default_prefix = k
                        break

        return px

    def _iterator_for_class(self, c: ClassDefinition) -> str:
        return self.iterator_template.replace("{Class}", c.name)

    def _subject_template_for_class(self, c: ClassDefinition, inline_owners: dict) -> Any:
        sv = self.schemaview
        id_slot = sv.get_identifier_slot(c.name)
        prefix = self.schema.default_prefix or "ex"

        if id_slot:
            return f"{prefix}:$({id_slot.name})"

        key_slot = sv.get_key_slot(c.name)
        if key_slot:
            return f"{prefix}:$({key_slot.name})"

        # YARRRML parsers fail to execute RML Joins (`condition: equal`) on generated Blank Nodes.
        # For inlined objects lacking an ID, we synthesize a deterministic IRI using the parent's ID
        # to guarantee graph connectivity and avoid broken/orphaned triples during the RDF roundtrip.
        if c.name in inline_owners:
            owner_name, _ = inline_owners[c.name][0]
            parent_id = sv.get_identifier_slot(owner_name) or sv.get_key_slot(owner_name)
            if parent_id:
                return f"{prefix}:{c.name}_$({parent_id.name})"

        return f"{prefix}:{c.name}/$(id)"

    def _po_list_for_class(self, c: ClassDefinition, inline_owners: dict) -> list[dict[str, Any]]:
        sv = self.schemaview
        po: list[dict[str, Any]] = []

        types = []
        class_uri = sv.get_uri(c, expand=False)
        class_term = str(class_uri) if class_uri else f"{sv.schema.default_prefix or 'ex'}:{c.name}"
        types.append(class_term)

        for mixin_name in c.mixins:
            m_cls = sv.get_class(mixin_name)
            if m_cls:
                m_uri = sv.get_uri(m_cls, expand=False)
                m_term = str(m_uri) if m_uri else f"{sv.schema.default_prefix or 'ex'}:{m_cls.name}"
                if m_term not in types:
                    types.append(m_term)

        if len(types) == 1:
            po.append({"p": "a", "o": types[0]})
        else:
            po.append({"p": "a", "o": FlowList(types)})

        default_prefix = sv.schema.default_prefix or "ex"

        for s in sv.class_induced_slots(c.name):
            decl = sv.get_slot(s.name)

            slot_uri = None
            if decl is not None and getattr(decl, "slot_uri", None):
                slot_uri = decl.slot_uri
            elif getattr(s, "slot_uri", None):
                slot_uri = s.slot_uri

            if slot_uri:
                pred = str(slot_uri)
            else:
                pred_uri = sv.get_uri(decl or s, expand=False)
                pred = str(pred_uri) if pred_uri is not None else f"{default_prefix}:{s.name}"

            alias = decl.alias if decl and decl.alias else s.alias
            var = alias or s.name

            has_own_id = sv.get_identifier_slot(c.name) or sv.get_key_slot(c.name)
            if c.name in inline_owners and not has_own_id:
                # Adjust JSONPath variable resolution for inlined objects without an ID.
                # Since the iterator remains at the parent level, we access properties via dot notation (e.g. parent_slot.child_prop)
                owner_name, slot_var = inline_owners[c.name][0]
                var = f"{slot_var}.{var}"

            is_obj = sv.get_class(s.range) is not None if s.range else False

            # Interlinking mappings (Joins)
            if is_obj:
                inlined = s.inlined
                multivalued = getattr(decl or s, "multivalued", False)

                if inlined is None:
                    inlined = False

                if inlined is False:
                    if multivalued:
                        po.append({"p": pred, "o": [{"value": f"{default_prefix}:$({var})", "type": "iri"}]})
                    else:
                        po.append({"p": pred, "o": {"value": f"{default_prefix}:$({var})", "type": "iri"}})
                    continue

                range_name = s.range
                range_id = sv.get_identifier_slot(range_name) or sv.get_key_slot(range_name)
                parent_id = sv.get_identifier_slot(c.name) or sv.get_key_slot(c.name)

                if range_id:
                    if multivalued:
                        left = f"$({var}[*].{range_id.name})"
                    else:
                        left = f"$({var}.{range_id.name})"
                    right = f"$({range_id.name})"
                elif parent_id:
                    left = f"$({parent_id.name})"
                    right = f"$({parent_id.name})"
                else:
                    left = None

                if left:
                    po_obj = {
                        "mapping": str(range_name),
                        "condition": {
                            "function": "equal",
                            "parameters": [
                                FlowList(["str1", left, "s"]),
                                FlowList(["str2", right, "o"]),
                            ],
                        },
                    }
                    if multivalued:
                        po.append({"p": pred, "o": [po_obj]})
                    else:
                        po.append({"p": pred, "o": po_obj})
                else:
                    if multivalued:
                        po.append({"p": pred, "o": [{"mapping": str(range_name)}]})
                    else:
                        po.append({"p": pred, "o": {"mapping": str(range_name)}})
                continue

            # Scalar values and datatype mapping
            datatype = None
            t = sv.get_type(s.range) if s.range else None

            if t:
                datatype = sv.get_uri(t, expand=False)

            if datatype:
                po.append({
                    "p": pred,
                    "o": {
                        "value": f"$({var})",
                        "datatype": str(datatype)
                    }
                })
            else:
                po.append({"p": pred, "o": f"$({var})"})

        return po


@shared_arguments(YarrrmlGenerator)
@click.command(name="yarrrml")
@click.option(
    "--source",
    help="YARRRML source shorthand, e.g., data.json~jsonpath or data.csv~csv (TSV works too)",
)
@click.option(
    "--iterator-template",
    help='JSONPath iterator template; supports {Class}, default: "$[*]"',
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, source, iterator_template, **args):
    """Generate YARRRML mappings from a LinkML schema."""
    if source:
        args["source"] = source
    if iterator_template:
        args["iterator_template"] = iterator_template
    gen = YarrrmlGenerator(yamlfile, **args)
    print(gen.serialize(**args))


if __name__ == "__main__":
    cli()
