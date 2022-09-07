import json
import os
from dataclasses import dataclass
from typing import TextIO, Union

import click
from linkml_runtime.linkml_model.meta import (ClassDefinition,
                                              SchemaDefinition, SlotDefinition)
from linkml_runtime.utils.formatutils import be, camelcase, underscore
from terminusdb_client.woqlquery import WOQLQuery as WQ

from linkml.utils.generator import Generator, shared_arguments

# https://terminusdb.com/docs/terminusdb/#/reference/XSD_WHITELIST
XSD_Ok = {
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
        "integer",
        "long",
        "positiveInteger",
        "nonNegativeInteger",
        "negativeInteger",
        "nonPositiveInteger",
        "anyURI",
    ]
}

@dataclass
class TerminusdbGenerator(Generator):
    """
    Experimental generator for TerminusDB

    Generates JSON-LD to pass to `WOQLQuery()`.

    Assumes an "inference/main" graph if any slots have "is_a" values, because any statements with
    rdfs:subPropertyOf as the predicate must live in a TerminusDB "inference" graph rather than the
    "schema" graph. When creating a new TerminusDB database, only the "schema" and "instance" graphs
    are created. Thus, you may need to e.g. `WOQLClient.create_graph("inference", "main")`.

    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["json"]
    visit_all_class_slots = True
    uses_schemaloader = True

    # ObjectVars
    classes: List = None
    raw_additions: List = None
    clswq: str = None


    def visit_schema(self, inline: bool = False, **kwargs) -> None:
        self.classes = []
        self.raw_additions = []

    def end_schema(self, **_) -> None:
        print(
            json.dumps(
                WQ().woql_and(*self.classes, *self.raw_additions).to_dict(), indent=2
            )
        )

    def visit_class(self, cls: ClassDefinition) -> bool:
        self.clswq = (
            WQ()
            .add_class(camelcase(cls.name))
            .label(camelcase(cls.name))
            .description(be(cls.description))
        )
        if cls.is_a:
            self.clswq.parent(camelcase(cls.is_a))
        if cls.abstract:
            self.clswq.abstract()
        if cls.broad_mappings:
            if any(
                str(self.namespaces.uri_for(m))
                == "http://terminusdb.com/schema/system#Document"
                for m in cls.broad_mappings
            ):
                self.clswq.parent("Document")
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        self.classes.append(self.clswq)

    def visit_class_slot(
        self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition
    ) -> None:
        if slot.range in self.schema.classes:
            rng = camelcase(slot.range)
        elif slot.range in self.schema.types:
            # XXX Why does `linkml_runtime.utils.metamodelcore.Identifier` subclass `str`??
            rng = str(self.schema.types[slot.range].uri)
        else:
            rng = "xsd:string"

        name = (
            f"{cls.name} {aliased_slot_name}"
            if slot.is_usage_slot
            else aliased_slot_name
        )

        # translate to terminusdb xsd builtins:
        if rng == "xsd:int":
            rng = "xsd:integer"
        elif rng == "xsd:float":
            rng = "xsd:double"
        elif rng == "xsd:language":
            rng = "xsd:string"

        if rng not in XSD_Ok and slot.range not in self.schema.classes:
            raise Exception(
                f"slot range for {name} must be schema class or supported xsd type. "
                f"Range {rng} is of type {type(rng)}."
            )

        self.clswq.property(
            underscore(name), rng, label=name, description=slot.description
        )
        if not slot.multivalued:
            self.clswq.max(1)
        if slot.required:
            self.clswq.min(1)
        if slot.is_a:
            self.raw_additions.append(
                WQ().add_quad(
                    underscore(name),
                    "rdfs:subPropertyOf",
                    self.clswq.iri(underscore(slot.is_a)),
                    "inference/main",
                )
            )


@shared_arguments(TerminusdbGenerator)
@click.command()
def cli(yamlfile, **args):
    """Generate graphql representation of a LinkML model"""
    print(TerminusdbGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
