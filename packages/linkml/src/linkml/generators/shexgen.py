"""Generate ShEx definition of a model"""

import os
import urllib.parse as urlparse
from dataclasses import dataclass, field

import click
from jsonasobj import as_json as as_json_1
from rdflib import OWL, RDF, XSD, Graph, Namespace
from ShExJSG import ShExC
from ShExJSG.SchemaWithContext import Schema
from ShExJSG.ShExJ import IRIREF, EachOf, NodeConstraint, Shape, ShapeOr, TripleConstraint

from linkml import METAMODEL_NAMESPACE, METAMODEL_NAMESPACE_NAME
from linkml._version import __version__
from linkml.generators.common.subproperty import get_subproperty_values
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ElementName,
    EnumDefinition,
    SlotDefinition,
    SlotDefinitionName,
    TypeDefinition,
)
from linkml_runtime.linkml_model.types import SHEX
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import URIorCURIE
from linkml_runtime.utils.rdf_canonicalize import canonicalize_rdf_graph


@dataclass
class ShExGenerator(Generator):
    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.2"
    valid_formats = ["shex", "json", "rdf"]
    file_extension = "shex.rdf"
    uses_schemaloader = False

    # ObjectVars
    shex: Schema = field(default_factory=lambda: Schema())  # ShEx Schema being generated
    shapes: list = field(default_factory=lambda: [])
    shape: Shape | None = None  # Current shape being defined
    list_shapes: list[IRIREF] = field(default_factory=lambda: [])  # Shapes that have been defined as lists
    expand_subproperty_of: bool = True
    """If True, expand subproperty_of to NodeConstraint value lists with slot descendants"""

    def __post_init__(self):
        super().__post_init__()

        # load (not merge) the closure so imported prefixes/types resolve;
        # CURIE-form imports cache namespaces() mid-closure, so invalidate
        # before rebuilding (imports_closure does not set_modified itself)
        self.schemaview.imports_closure()
        self.schemaview.set_modified()
        self.namespaces = self.schemaview.namespaces()
        # the loader anchored _base on the default prefix expansion
        if self.schema.default_prefix:
            self.namespaces._base = (
                self.schema.default_prefix
                if ":" in self.schema.default_prefix
                else self.namespaces[self.schema.default_prefix]
            )
        else:
            self.namespaces._base = sfx(str(self.schema.id))
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

    def serialize(self, output: str | None = None, **kwargs) -> str:
        # Adjust the schema context to include the base model URI
        context = self.shex["@context"]
        self.shex["@context"] = [context, {"@base": self.namespaces._base}]
        # Emit all of the type definitions
        for typ in sorted(self.schemaview.all_types(imports=self.mergeimports).values(), key=lambda t: t.name.lower()):
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

        for cls in sorted(self.schemaview.all_classes(imports=self.mergeimports).values(), key=lambda c: c.name.lower()):
            self._add_class(cls)

        out = self._build_output(output)
        if self.format != "json":
            out = self.generate_header() + out
        return out.rstrip() + "\n"

    def _class_uri_of(self, cls: ClassDefinition) -> str:
        """Declared class_uri, or the derived CURIE the loader would have filled in."""
        return cls.class_uri if cls.class_uri else self.schemaview.get_uri(cls)

    def _add_class(self, cls: ClassDefinition) -> None:
        sv = self.schemaview
        self.shape = Shape()

        # Start with all the parent classes, mixins and appytos
        struct_ref_list = [cls.is_a] if cls.is_a else []
        struct_ref_list += cls.mixins
        # classes that declare apply_to this class (synopsis.applytorefs)
        struct_ref_list += sorted(c.name for c in sv.all_classes().values() if cls.name in c.apply_to)
        for sr in struct_ref_list:
            self._add_constraint(self._class_or_type_uri(sr, "_tes"))
            self._add_constraint(self._type_arc(self._class_uri_of(sv.get_class(sr)), opt=True))

        # own slots: not inherited from the is_a parent, unless redefined via slot_usage
        parent_slot_names = set(sv.class_slots(cls.is_a)) if cls.is_a else set()
        for slot in self.induced_slots_legacy_order(cls.name):
            if slot.name not in parent_slot_names or slot.name in cls.slot_usage:
                self._add_class_slot(slot)

        self._end_class(cls)

    def _end_class(self, cls: ClassDefinition) -> None:
        # On entry self.shape contains all of the triple expressions that define the body of the shape

        # Finish off the shape definition itself

        # If there is nothing yet, we're at the very root of things.  Add in a final catch-all for any additional
        # type arcs.  NOTE: Here is where you can sink other things as well if you want to ignore categories of things
        if self.shape.expression is None:
            self._add_constraint(TripleConstraint(predicate=RDF.type, min=0, max=-1))
        self.shape.expression.id = self._class_or_type_uri(cls, "_tes")
        identifier_slot = self.schemaview.get_identifier_slot(cls.name, use_key=True)
        self.shape.expression = EachOf(
            expressions=[
                self.shape.expression,
                self._type_arc(self._class_uri_of(cls), not bool(identifier_slot)),
            ]
        )
        self.shape.closed = not (cls.abstract or cls.mixin)

        # If this class has subtypes, define the class as the union of its subtypes and itself (if not abstract)
        is_a_children = sorted(c.name for c in self.schemaview.all_classes().values() if c.is_a == cls.name)
        if is_a_children:
            childrenExprs = []
            for child_classname in is_a_children:
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

    def _add_class_slot(self, slot: SlotDefinition) -> None:
        if not (slot.identifier or slot.abstract or slot.mixin):
            constraint = TripleConstraint()
            self._add_constraint(constraint)
            if slot.slot_uri:
                slot_uri = slot.slot_uri
            else:
                # the loader derived missing slot_uris from the aliased name
                try:
                    prefix = self._defining_prefix(slot)
                except ValueError:
                    prefix = self.schema.default_prefix
                slot_uri = self.namespaces.uri_or_curie_for(
                    prefix, underscore(slot.alias if slot.alias else slot.name)
                )
            constraint.predicate = self.namespaces.uri_for(slot_uri)
            constraint.min = int(bool(slot.required))
            constraint.max = 1 if not slot.multivalued else -1
            if slot.range in self.schemaview.all_enums():
                # Handle permissible values from enums
                enum = self.schemaview.all_enums()[slot.range]
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
            elif self.expand_subproperty_of and slot.subproperty_of:
                # Handle subproperty_of constraint - restrict to slot descendants
                values = self._get_subproperty_values(slot)
                if values:
                    constraint.valueExpr = NodeConstraint(values=values)
                else:
                    constraint.valueExpr = self._class_or_type_uri(slot.range)
            else:
                constraint.valueExpr = self._class_or_type_uri(slot.range)

    def _build_output(self, output: str | None = None) -> str:
        self.shex.shapes = self.shapes if self.shapes else [Shape()]
        shex = as_json_1(self.shex)
        if self.format == "rdf":
            g = Graph()
            g.parse(data=shex, format="json-ld", version="1.1")
            g.bind("owl", OWL)
            shex = canonicalize_rdf_graph(g, output_format="turtle")
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
        item: TypeDefinition | ClassDefinition | ElementName,
        suffix: str | None = "",
    ) -> URIorCURIE:
        # TODO: enums - figure this out
        if isinstance(item, TypeDefinition | ClassDefinition | EnumDefinition):
            cls_or_type = item
        else:
            sv = self.schemaview
            cls_or_type = (
                (sv.get_class(item) if item else None)
                or (sv.get_type(item) if item else None)
                or (sv.get_enum(item) if item else None)
            )
            if cls_or_type is None:
                # absent/unresolvable ranges defaulted to string under the loader
                cls_or_type = sv.get_type(self.schema.default_range or "string")
        return self.namespaces.uri_for(
            self.namespaces.uri_or_curie_for(
                self._defining_prefix(cls_or_type),
                camelcase(cls_or_type.name) + suffix,
            )
        )

    def _defining_prefix(self, element) -> str:
        """Default prefix of the schema defining element (loader's schema_defaults)."""
        return self.defining_schema(element).default_prefix

    def _slot_uri(self, name: str, suffix: str | None = "") -> URIorCURIE:
        slot = self.schemaview.get_slot(name)
        return self.namespaces.uri_for(
            self.namespaces.uri_or_curie_for(self._defining_prefix(slot), camelcase(name) + suffix)
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

    def _get_subproperty_values(self, slot: SlotDefinition) -> list:
        """
        Get all valid values from slot hierarchy for subproperty_of constraint.

        Following metamodel semantics: "any ontological child (related to X via
        an is_a relationship), is a valid value for the slot"

        Values are formatted as URIs for ShEx compatibility.

        :param slot: SlotDefinition with subproperty_of set
        :return: List of URI strings for NodeConstraint values
        """
        # ShEx always uses full URIs
        return get_subproperty_values(self.schemaview, slot, expand_uri=True)


@shared_arguments(ShExGenerator)
@click.command(name="shex")
@click.option("-o", "--output", help="Output file name")
@click.option(
    "--expand-subproperty-of/--no-expand-subproperty-of",
    default=True,
    show_default=True,
    help="If --expand-subproperty-of (default), slots with subproperty_of will generate NodeConstraint "
    "values containing all slot descendants. Use --no-expand-subproperty-of to disable this behavior.",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **args):
    """Generate a ShEx Schema for a  LinkML model"""
    print(ShExGenerator(yamlfile, **args).serialize(**args))


if __name__ == "__main__":
    cli()
