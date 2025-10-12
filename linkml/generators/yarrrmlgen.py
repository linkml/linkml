from __future__ import annotations

import os
from typing import Any, TextIO

import click
import yaml
from linkml_runtime.linkml_model.meta import ClassDefinition, SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

# defaults
DEFAULT_SOURCE_JSON = "data.json~jsonpath"
DEFAULT_SOURCE_CSV = "data.csv~csv"
DEFAULT_ITERATOR = "$.items[*]"  # generic top-level array


class _YamlDumper(yaml.Dumper):
    # keep list indentation stable
    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)


class YarrrmlGenerator(Generator):
    """LinkML -> YARRRML exporter."""

    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["yml", "yaml"]
    visit_all_class_slots = False

    def __init__(self, schema: str | TextIO | SchemaDefinition, format: str = "yml", **kwargs):
        def _infer_source_suffix(path: str) -> str:
            p = (path or "").lower()
            if "~" in p:
                return path  # already has ~jsonpath or ~csv
            if p.endswith(".json"):
                return f"{path}~jsonpath"
            if p.endswith(".csv") or p.endswith(".tsv"):
                return f"{path}~csv"
            return path

        # in __init__ right after you read src:
        raw_src = kwargs.pop("source", None)
        it = kwargs.pop("iterator_template", None)

        super().__init__(schema, **kwargs)

        self.schemaview = SchemaView(schema)
        self.schema: SchemaDefinition = self.schemaview.schema

        self.format = format

        # normalize source: if user passed file without "~csv/~jsonpath", infer it
        if raw_src:
            self.source = _infer_source_suffix(raw_src)
        else:
            self.source = DEFAULT_SOURCE_JSON

        self.iterator_template: str = it or DEFAULT_ITERATOR

    # public
    def serialize(self, **args) -> str:
        data = yaml.dump(
            self.as_dict(),
            Dumper=_YamlDumper,
            sort_keys=False,
            default_flow_style=False,
            allow_unicode=True,
        )
        return data

    def as_dict(self) -> dict[str, Any]:
        sv = self.schemaview
        mappings = {}
        for cls in sv.all_classes().values():
            if not (sv.get_identifier_slot(cls.name) or sv.get_key_slot(cls.name)):
                continue

            mapping = {
                "s": self._subject_template_for_class(cls),
                "po": self._po_list_for_class(cls),
            }
            if self._is_json_source():
                mapping["sources"] = [[self.source, self._iterator_for_class(cls)]]
            else:
                mapping["sources"] = [[self.source]]

            mappings[str(cls.name)] = mapping

        return {"prefixes": self._prefixes(), "mappings": mappings}

    # helpers
    def _is_json_source(self) -> bool:
        return "~jsonpath" in (self.source or "")

    def _prefixes(self) -> dict[str, str]:
        px: dict[str, str] = {}
        if self.schema.prefixes:
            for p in self.schema.prefixes.values():
                if p.prefix_prefix and p.prefix_reference:
                    px[str(p.prefix_prefix)] = str(p.prefix_reference)
        px.setdefault("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
        return px

    def _iterator_for_class(self, c: ClassDefinition) -> str:
        # supports {Class}
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
        return f"{default_prefix}:{c.name}/$(subject_id)"  # safe fallback

    def _po_list_for_class(self, c: ClassDefinition) -> list[dict[str, Any]]:
        sv = self.schemaview
        po = []
        class_curie = sv.get_uri(c, expand=False)
        if class_curie:
            po.append({"p": "rdf:type", "o": str(class_curie)})

        default_prefix = sv.schema.default_prefix or "ex"

        for s in sv.class_induced_slots(c.name):
            pred = sv.get_uri(s, expand=False) or f"{default_prefix}:{s.name}"
            decl = sv.get_slot(s.name)
            alias = decl.alias if decl and decl.alias else s.alias
            var = alias or s.name

            is_obj = sv.get_class(s.range) is not None if s.range else False
            if is_obj:
                inlined = None
                if decl and decl.inlined is not None:
                    inlined = decl.inlined
                if inlined is False:
                    po.append({"p": pred, "o": {"value": f"$({var})", "type": "iri"}})
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
