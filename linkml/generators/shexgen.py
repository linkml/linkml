"""Generate ShEx definition of a model

"""

import os
import urllib.parse as urlparse
from dataclasses import dataclass, field
from typing import List, Optional, Union

import click
from jsonasobj import as_json as as_json_1
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ElementName,
    EnumDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
)
from linkml_runtime.linkml_model.types import SHEX
from linkml_runtime.utils.formatutils import camelcase, sfx
from linkml_runtime.utils.metamodelcore import URIorCURIE
from rdflib import OWL, RDF, XSD, Graph, Namespace
from ShExJSG import ShExC
from ShExJSG.SchemaWithContext import Schema
from ShExJSG.ShExJ import IRIREF, EachOf, NodeConstraint, Shape, ShapeOr, TripleConstraint

from linkml import METAMODEL_NAMESPACE, METAMODEL_NAMESPACE_NAME
from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


@dataclass
class ShExGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = ["shex", "json", "rdf"]
    file_extension = "shex.rdf"
    visit_all_class_slots = False
    uses_schemaloader = True

    # ObjectVars
    shex: Schema = field(default_factory=lambda: Schema())  # ShEx Schema being generated
    shapes: List = field(default_factory=lambda: [])
    shape: Optional[Shape] = None  # Current shape being defined
    list_shapes: List[IRIREF] = field(default_factory=lambda: [])  # Shapes that have been defined as lists

    def __post_init__(self):
        super().__post_init__()

        if METAMODEL_NAMESPACE_NAME not in self.namespaces:
            self.namespaces[METAMODEL_NAMESPACE_NAME] = METAMODEL_NAMESPACE
        self.meta = Namespace(
            self.namespaces.join(self.namespaces[METAMODEL_NAMESPACE_NAME], "")
        )  # URI for the metamodel
        self.base = Namespace(self.namespaces.join(self.namespaces._base, ""))  # Base URI for what is being modeled

    def generate_header(self) -> str:
        out = f"# metamodel_version: {self.schema.metamodel_version}\n"
        if self.schema.version:
            out += f"# version: {self.schema.version}\n"
        return out

    def visit_schema(self, **_):
        # Adjust the schema context to include the base model URI
        context = self.shex["@context"]
        self.shex["@context"] = [context, {"@base": self.namespaces._base}]
        # Emit all of the type definitions
        for typ in self.schema.types.values():
            model_uri = self._class_or_type_uri(typ)
            if typ.uri:
                typ_type_uri = self.namespaces.uri_for(typ.uri)
                if typ_type_uri in (XSD.anyURI, SHEX.iri):
                    self.shapes.append(NodeConstraint(id=model_uri, nodeKind="iri"))
                elif typ_type_uri == SHEX.nonLiteral:
                    self.shapes.append(NodeConstraint(id=model_uri, nodeKind="nonliteral"))
                else:
                    self.shapes.append(NodeConstraint(id=model_uri, datatype=self.namespaces.uri_for(typ.uri)))
            else:
                typeof_uri = self._class_or_type_uri(typ.typeof)
                self.shapes.append(Shape(id=model_uri, expression=typeof_uri))
        if self.format != "json":
            return self.generate_header()

    def visit_class(self, cls: ClassDefinition) -> bool:
        self.shape = Shape()

        # Start with all the parent classes, mixins and appytos
        struct_ref_list = [cls.is_a] if cls.is_a else []
        struct_ref_list += cls.mixins
        if cls.name in self.synopsis.applytorefs:
            for applier in self.synopsis.applytorefs[cls.name].classrefs:
                struct_ref_list.append(applier)
        for sr in struct_ref_list:
            self._add_constraint(self._class_or_type_uri(sr, "_tes"))
            self._add_constraint(self._type_arc(self.schema.classes[sr].class_uri, opt=True))
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        # On entry self.shape contains all of the triple expressions that define the body of the shape

        # Finish off the shape definition itself

        # If there is nothing yet, we're at the very root of things.  Add in a final catch-all for any additional
        # type arcs.  NOTE: Here is where you can sink other things as well if you want to ignore categories of things
        if self.shape.expression is None:
            self._add_constraint(TripleConstraint(predicate=RDF.type, min=0, max=-1))
        self.shape.expression.id = self._class_or_type_uri(cls, "_tes")
        self.shape.expression = EachOf(
            expressions=[
                self.shape.expression,
                self._type_arc(cls.class_uri, not bool(self.class_identifier(cls))),
            ]
        )
        self.shape.closed = not (cls.abstract or cls.mixin)

        # If this class has subtypes, define the class as the union of its subtypes and itself (if not abstract)
        if cls.name in self.synopsis.isarefs:
            childrenExprs = []
            for child_classname in sorted(list(self.synopsis.isarefs[cls.name].classrefs)):
                childrenExprs.append(self._class_or_type_uri(child_classname))
            if not (cls.mixin or cls.abstract) or len(childrenExprs) == 1:
                childrenExprs.insert(0, self.shape)
                self.shapes.append(ShapeOr(id=self._class_or_type_uri(cls), shapeExprs=childrenExprs))
            else:
                self.shapes.append(ShapeOr(id=self._class_or_type_uri(cls), shapeExprs=childrenExprs))
                self.shape.id = self._class_or_type_uri(cls, "_struct")
                self.shapes.append(self.shape)
        else:
            self.shape.id = self._class_or_type_uri(cls)
            self.shapes.append(self.shape)

    def visit_class_slot(
        self,
        cls: ClassDefinition,
        aliased_slot_name: SlotDefinitionName,
        slot: SlotDefinition,
    ) -> None:
        if not (slot.identifier or slot.abstract or slot.mixin):
            constraint = TripleConstraint()
            self._add_constraint(constraint)
            constraint.predicate = self.namespaces.uri_for(slot.slot_uri)
            constraint.min = int(bool(slot.required))
            constraint.max = 1 if not slot.multivalued else -1
            if slot.range in self.schema.enums:
                # Handle permissible values from enums
                enum = self.schema.enums[slot.range]
                values = []
                for value in enum.permissible_values.values():
                    if value.meaning:
                        values.append(self.namespaces.uri_for(value.meaning))
                    else:
                        value_uri = f"{self._class_or_type_uri(enum.name)}#{urlparse.quote(value.text)}"
                        values.append(value_uri)
                if values:
                    node_constraint = NodeConstraint(
                        # id=self._class_or_type_uri(slot.range),
                        values=values,
                    )
                    constraint.valueExpr = node_constraint
            else:
                constraint.valueExpr = self._class_or_type_uri(slot.range)

    def end_schema(self, output: Optional[str] = None, **_) -> str:
        self.shex.shapes = self.shapes if self.shapes else [Shape()]
        shex = as_json_1(self.shex)
        if self.format == "rdf":
            g = Graph()
            g.parse(data=shex, format="json-ld", version="1.1")
            g.bind("owl", OWL)
            shex = g.serialize(format="turtle")
        elif self.format == "shex":
            g = Graph()
            self.namespaces.load_graph(g)
            shex = str(ShExC(self.shex, base=sfx(self.namespaces._base), namespaces=g))

        if output:
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(shex)
        return shex

    def _class_or_type_uri(
        self,
        item: Union[TypeDefinition, ClassDefinition, ElementName],
        suffix: Optional[str] = "",
    ) -> URIorCURIE:
        # TODO: enums - figure this out
        if isinstance(item, (TypeDefinition, ClassDefinition, EnumDefinition)):
            cls_or_type = item
        else:
            cls_or_type = self.class_or_type_for(item)
        return self.namespaces.uri_for(
            self.namespaces.uri_or_curie_for(
                self.schema_defaults[cls_or_type.from_schema],
                camelcase(cls_or_type.name) + suffix,
            )
        )

    def _slot_uri(self, name: str, suffix: Optional[str] = "") -> URIorCURIE:
        slot = self.schema.slots[name]
        return self.namespaces.uri_for(
            self.namespaces.uri_or_curie_for(self.schema_defaults[slot.from_schema], camelcase(name) + suffix)
        )

    def _add_constraint(self, constraint) -> None:
        # No constraints
        if not self.shape.expression:
            self.shape.expression = constraint
        # One constraint
        elif not isinstance(self.shape.expression, EachOf):
            self.shape.expression = EachOf(expressions=[self.shape.expression, constraint])
        # Two or more constraints
        else:
            self.shape.expression.expressions.append(constraint)

    def _type_arc(self, target: URIorCURIE, opt: bool = False) -> TripleConstraint:
        return TripleConstraint(
            predicate=RDF.type,
            valueExpr=NodeConstraint(values=[IRIREF(self.namespaces.uri_for(target))]),
            min=0 if opt else 1,
        )


@shared_arguments(ShExGenerator)
@click.command()
@click.option("-o", "--output", help="Output file name")
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate a ShEx Schema for a  LinkML model"""
    print(ShExGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
