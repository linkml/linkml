import json
import os
from dataclasses import dataclass, field

import click

from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import be, camelcase, underscore

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

# TerminusDB XSD types supported as property ranges.
# https://terminusdb.com/docs/terminusdb/#/reference/XSD_WHITELIST
XSD_OK = {
    f"xsd:{t}"
    for t in [
        "string",
        "boolean",
        "decimal",
        "integer",
        "double",
        "float",
        "dateTime",
        "byte",
        "short",
        "long",
        "positiveInteger",
        "nonNegativeInteger",
        "negativeInteger",
        "nonPositiveInteger",
        "anyURI",
    ]
}

# Map LinkML XSD types that don't exist in TerminusDB to supported equivalents.
XSD_TRANSLATE = {
    "xsd:int": "xsd:integer",
    "xsd:float": "xsd:double",
    "xsd:language": "xsd:string",
    "xsd:date": "xsd:dateTime",
    "xsd:time": "xsd:dateTime",
    "xsd:nonNegativeInteger": "xsd:integer",
    "xsd:positiveInteger": "xsd:integer",
}


@dataclass
class TerminusdbGenerator(Generator):
    """Generator for TerminusDB JSON-LD schema documents.

    Produces a JSON array of schema documents compatible with the
    TerminusDB v10+ document interface.  The output can be loaded via
    ``client.insert_document(docs, graph_type="schema")``.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.2.0"
    valid_formats = ["json"]
    visit_all_class_slots = True
    uses_schemaloader = True

    # ObjectVars
    documents: list = field(default_factory=list)
    current_class_doc: dict = field(default_factory=dict)

    def visit_schema(self, inline: bool = False, **kwargs) -> None:
        self.documents = []
        schema_id = str(self.schema.id) if self.schema.id else "terminusdb:///schema"
        schema_base = schema_id.rstrip("/").rstrip("#") + "#"
        data_base = schema_id.rstrip("/").rstrip("#").rsplit("/", 1)[0] + "/data/"
        self.documents.append(
            {
                "@type": "@context",
                "@documentation": {
                    "@title": self.schema.title or self.schema.name or "",
                    "@description": be(self.schema.description) or "",
                },
                "@schema": schema_base,
                "@base": data_base,
            }
        )

    def end_schema(self, **_) -> str:
        # Emit enum documents
        for enum_def in self.schema.enums.values():
            self._emit_enum(enum_def)
        return json.dumps(self.documents, indent=2)

    def _emit_enum(self, enum_def: EnumDefinition) -> None:
        """Produce a TerminusDB Enum document."""
        doc = {
            "@type": "Enum",
            "@id": camelcase(enum_def.name),
            "@value": [str(pv) for pv in enum_def.permissible_values],
        }
        self.documents.append(doc)

    def visit_class(self, cls: ClassDefinition) -> bool:
        doc = {
            "@type": "Class",
            "@id": camelcase(cls.name),
        }
        if cls.description:
            doc["@documentation"] = {"@comment": be(cls.description), "@properties": {}}
        if cls.is_a:
            doc["@inherits"] = [camelcase(cls.is_a)]
        if cls.abstract:
            doc["@abstract"] = []
        if cls.broad_mappings:
            if any(
                str(self.namespaces.uri_for(m)) == "http://terminusdb.com/schema/system#Document"
                for m in cls.broad_mappings
            ):
                doc.setdefault("@inherits", []).append("Document")
        self.current_class_doc = doc
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        self.documents.append(self.current_class_doc)

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        rng = self._resolve_range(slot)
        prop_name = underscore(aliased_slot_name)

        # Determine cardinality wrapper
        if slot.multivalued:
            if slot.inlined_as_list:
                prop_value = {"@type": "List", "@class": rng}
            else:
                prop_value = {"@type": "Set", "@class": rng}
        elif not slot.required:
            prop_value = {"@type": "Optional", "@class": rng}
        else:
            prop_value = rng

        self.current_class_doc[prop_name] = prop_value

        # Add property documentation
        if slot.description and "@documentation" in self.current_class_doc:
            self.current_class_doc["@documentation"]["@properties"][prop_name] = slot.description

    def _resolve_range(self, slot: SlotDefinition) -> str:
        """Resolve a slot range to a TerminusDB type string."""
        if slot.range in self.schema.classes:
            return camelcase(slot.range)
        if slot.range in self.schema.enums:
            return camelcase(slot.range)
        if slot.range in self.schema.types:
            rng = str(self.schema.types[slot.range].uri)
        else:
            rng = "xsd:string"

        rng = XSD_TRANSLATE.get(rng, rng)

        if rng not in XSD_OK:
            rng = "xsd:string"

        return rng


@shared_arguments(TerminusdbGenerator)
@click.version_option(__version__, "-V", "--version")
@click.command(name="terminusdb")
def cli(yamlfile, **args):
    """Generate TerminusDB JSON-LD schema from a LinkML model"""
    print(TerminusdbGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
