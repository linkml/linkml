import json
import os
from dataclasses import dataclass, field

import click

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, EnumDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import be, camelcase, underscore

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

# Map LinkML XSD types not natively supported by TerminusDB to supported equivalents.
XSD_TRANSLATE = {
    "xsd:int": "xsd:integer",
    "xsd:language": "xsd:string",
    "xsd:date": "xsd:dateTime",
    "xsd:time": "xsd:dateTime",
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
    uses_schemaloader = False

    # ObjectVars
    documents: list = field(default_factory=list)
    current_class_doc: dict = field(default_factory=dict)

    def serialize(self, **kwargs) -> str:
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

        for cls in sorted(self.schemaview.all_classes().values(), key=lambda c: c.name.lower()):
            self.documents.append(self._class_doc(cls))

        # Emit enum documents
        for enum_def in self.schemaview.all_enums().values():
            self._emit_enum(enum_def)
        return json.dumps(self.documents, indent=2) + "\n"

    def _emit_enum(self, enum_def: EnumDefinition) -> None:
        """Produce a TerminusDB Enum document."""
        doc = {
            "@type": "Enum",
            "@id": camelcase(enum_def.name),
            "@value": [str(pv) for pv in enum_def.permissible_values],
        }
        self.documents.append(doc)

    def _class_doc(self, cls: ClassDefinition) -> dict:
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
        for slot in self.induced_slots_legacy_order(cls.name):
            self._add_class_slot(slot)
        return doc

    def _add_class_slot(self, slot: SlotDefinition) -> None:
        rng = self._resolve_range(slot)
        prop_name = underscore(slot.alias if slot.alias else slot.name)

        # Determine cardinality wrapper
        if slot.multivalued:
            # references to classes without identifiers are always inlined as
            # list; SchemaLoader materialized this onto the resolved slot
            inlined_as_list = slot.inlined_as_list or (
                slot.range in self.schemaview.all_classes()
                and self.schemaview.is_inlined(slot)
                and self.schemaview.get_identifier_slot(slot.range, use_key=True) is None
            )
            if inlined_as_list:
                prop_value = {"@type": "List", "@class": rng}
            else:
                prop_value = {"@type": "Set", "@class": rng}
        elif not slot.required:
            prop_value = {"@type": "Optional", "@class": rng}
        else:
            prop_value = rng

        self.current_class_doc[prop_name] = prop_value

        # Add property documentation, lazily initializing @documentation if needed
        if slot.description:
            doc = self.current_class_doc.setdefault("@documentation", {"@comment": "", "@properties": {}})
            doc.setdefault("@properties", {})[prop_name] = slot.description

    def _resolve_range(self, slot: SlotDefinition) -> str:
        """Resolve a slot range to a TerminusDB type string."""
        if slot.range in self.schemaview.all_classes():
            return camelcase(slot.range)
        if slot.range in self.schemaview.all_enums():
            return camelcase(slot.range)
        if slot.range in self.schemaview.all_types():
            rng = str(self.schemaview.induced_type(slot.range).uri)
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
