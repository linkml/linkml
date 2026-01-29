from __future__ import annotations

import os
from typing import Any, TextIO

import click
import yaml

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView

DEFAULT_SOURCE_JSON = "data.json~jsonpath"
DEFAULT_ITERATOR = "$.items[*]"


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
        self.iterator_template: str = it or DEFAULT_ITERATOR

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
        data = yaml.safe_dump(
            self.as_dict(), sort_keys=False, allow_unicode=True, default_flow_style=False, indent=2, width=120
        )
        return data

    def as_dict(self) -> dict[str, Any]:
        sv = self.schemaview
        mappings: dict[str, Any] = {}

        inline_targets: set[str] = set()
        non_inline_targets: set[str] = set()

        for owner in sv.all_classes().values():
            for s in sv.class_induced_slots(owner.name):
                if not s.range:
                    continue
                range_cls = sv.get_class(s.range)
                if range_cls is None:
                    continue

                decl = sv.get_slot(s.name)
                inlined = getattr(decl or s, "inlined", None)

                if inlined is None:
                    inlined = False

                if inlined:
                    inline_targets.add(range_cls.name)
                else:
                    non_inline_targets.add(range_cls.name)

        inline_only = inline_targets - non_inline_targets

        for cls in sv.all_classes().values():
            if cls.name in inline_only:
                if not sv.get_identifier_slot(cls.name) and not sv.get_key_slot(cls.name):
                    continue

            mapping_dict: dict[str, Any] = {}

            if self._is_json_source():
                mapping_dict["sources"] = [[self.source, self._iterator_for_class(cls)]]
            else:
                mapping_dict["sources"] = [[self.source]]

            mapping_dict["s"] = self._subject_template_for_class(cls)
            mapping_dict["po"] = self._po_list_for_class(cls)

            mappings[str(cls.name)] = mapping_dict

        prefixes = self._prefixes_with_defaults()
        return {"prefixes": prefixes, "mappings": mappings}

    # helpers
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

    def _subject_template_for_class(self, c: ClassDefinition) -> str:
        sv = self.schemaview
        default_prefix = sv.schema.default_prefix or "ex"
        id_slot = sv.get_identifier_slot(c.name)
        if id_slot:
            return f"{default_prefix}:$({id_slot.name})"
        key_slot = sv.get_key_slot(c.name)
        if key_slot:
            return f"{default_prefix}:$({key_slot.name})"
        return f"{default_prefix}:{c.name}/$(subject_id)"

    def _po_list_for_class(self, c: ClassDefinition) -> list[dict[str, Any]]:
        sv = self.schemaview
        po: list[dict[str, Any]] = []

        class_uri = sv.get_uri(c, expand=False)
        class_term = str(class_uri) if class_uri else f"{sv.schema.default_prefix or 'ex'}:{c.name}"
        po.append({"p": "rdf:type", "o": class_term})

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

            is_obj = sv.get_class(s.range) is not None if s.range else False
            if is_obj:
                inlined = getattr(decl or s, "inlined", None)
                multivalued = getattr(decl or s, "multivalued", False)

                if inlined is None:
                    inlined = False

                if inlined is False:
                    if multivalued:
                        po.append({"p": pred, "o": [{"value": f"$({var}[*])", "type": "iri"}]})
                    else:
                        po.append({"p": pred, "o": {"value": f"$({var})", "type": "iri"}})
                    continue

                range_class = sv.get_class(s.range)
                if range_class:
                    nested_po = []

                    for nested_slot in sv.class_induced_slots(s.range):
                        nested_decl = sv.get_slot(nested_slot.name)

                        nested_slot_uri = None
                        if nested_decl is not None and getattr(nested_decl, "slot_uri", None):
                            nested_slot_uri = nested_decl.slot_uri
                        elif getattr(nested_slot, "slot_uri", None):
                            nested_slot_uri = nested_slot.slot_uri

                        if nested_slot_uri:
                            nested_pred = str(nested_slot_uri)
                        else:
                            nested_pred_uri = sv.get_uri(nested_decl or nested_slot, expand=False)
                            nested_pred = (
                                str(nested_pred_uri)
                                if nested_pred_uri is not None
                                else f"{default_prefix}:{nested_slot.name}"
                            )

                        nested_alias = nested_decl.alias if nested_decl and nested_decl.alias else nested_slot.alias
                        nested_var = nested_alias or nested_slot.name
                        full_var = f"$({var}.{nested_var})"

                        nested_is_obj = sv.get_class(nested_slot.range) is not None if nested_slot.range else False
                        if nested_is_obj:
                            nested_inlined = getattr(nested_decl or nested_slot, "inlined", None)
                            if nested_inlined is False:
                                nested_po.append(
                                    {"p": nested_pred, "o": {"value": full_var, "type": "iri"}}
                                )
                            continue

                        nested_po.append({"p": nested_pred, "o": full_var})

                    if multivalued:
                        po.append({"p": pred, "o": [{"po": nested_po}]})
                    else:
                        po.append({"p": pred, "o": {"po": nested_po}})

                continue

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
    help='JSONPath iterator template; supports {Class}, default: "$.items[*]"',
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
