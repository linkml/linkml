import os
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set, Union

import click
import pydantic
from linkml_runtime.linkml_model.meta import ClassDefinitionName, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments

MERMAID_SERIALIZATION = str


class Attribute(pydantic.BaseModel):
    datatype: str = "string"
    name: str = None
    key: str = None
    comment: str = None

    def __str__(self):
        cmt = f'"{self.comment}"' if self.comment else ""
        return f'    {self.datatype} {self.name} {self.key if self.key else ""} {cmt}'


class IdentifyingType(str, Enum):
    """Identifying types.

    See: https://mermaid.js.org/syntax/entityRelationshipDiagram.html#identification"""

    IDENTIFYING = "--"
    NON_IDENTIFYING = ".."

    def __str__(self):
        return self.value


class Cardinality(pydantic.BaseModel):
    """Cardinality of a slot.

    See https://mermaid.js.org/syntax/entityRelationshipDiagram.html#relationship-syntax"""

    required: bool = True
    multivalued: bool = False
    is_left: bool = True

    def __str__(self):
        required_char = "|" if self.required else "o"
        if self.multivalued:
            multivalued_char = "}" if self.is_left else "{"
        else:
            multivalued_char = "|"
        if self.is_left:
            return f"{multivalued_char}{required_char}"
        else:
            return f"{required_char}{multivalued_char}"


class RelationshipType(pydantic.BaseModel):
    """Relationship type.
    See https://mermaid.js.org/syntax/entityRelationshipDiagram.html#relationship-syntax"""

    left_cardinality: Cardinality
    identifying: IdentifyingType = IdentifyingType.IDENTIFYING
    right_cardinality: Cardinality = None

    def __str__(self):
        return f"{self.left_cardinality}{self.identifying}{self.right_cardinality}"


class Entity(pydantic.BaseModel):
    """Entity in an ER diagram."""

    name: str
    attributes: List[Attribute] = []

    def __str__(self):
        attrs = "\n".join([str(a) for a in self.attributes])
        return f"{self.name} {{\n{attrs}\n}}"


class Relationship(pydantic.BaseModel):
    """Relationship in an ER diagram."""

    first_entity: str
    relationship_type: RelationshipType = None
    second_entity: str = None
    relationship_label: str = None

    def __str__(self):
        return f'{self.first_entity} {self.relationship_type} {self.second_entity} : "{self.relationship_label}"'


class ERDiagram(pydantic.BaseModel):
    """Represents an Diagram of Entities and Relationships"""

    entities: List[Entity] = []
    relationships: List[Relationship] = []

    def __str__(self):
        ents = "\n".join([str(e) for e in self.entities])
        rels = "\n".join([str(r) for r in self.relationships])
        return f"erDiagram\n{ents}\n\n{rels}\n"


@dataclass
class ERDiagramGenerator(Generator):
    """
    A generator for serializing schemas as Entity-Relationship diagrams.

    Currently this generates diagrams in mermaid syntax, but in future
    this could easily be extended to have for example a direct SVG or PNG
    generator using PyGraphViz, similar to erdantic.
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    valid_formats = ["markdown", "mermaid"]
    uses_schemaloader = False
    requires_metamodel = False

    structural: bool = True
    """If True, then only the tree_root and entities reachable from the root are drawn"""

    exclude_attributes: bool = False
    """If True, do not include attributes in entities"""

    genmeta: bool = False
    gen_classvars: bool = True
    gen_slots: bool = True
    no_types_dir: bool = False
    use_slot_uris: bool = False

    def __post_init__(self):
        self.schemaview = SchemaView(self.schema)
        super().__post_init__()

    def serialize(self) -> MERMAID_SERIALIZATION:
        """
        Serialize a schema as an ER Diagram.

        If a tree_root is present in the schema, then only Entities traversable
        from here will be included. Otherwise, all Entities will be included.

        :return: mermaid string
        """
        sv = self.schemaview
        structural_roots = [cn for cn, c in sv.all_classes().items() if c.tree_root]
        if self.structural and structural_roots:
            return self.serialize_classes(structural_roots, follow_references=True)
        else:
            diagram = ERDiagram()
            for cn in sv.all_classes():
                self.add_class(cn, diagram)
            return self.serialize_diagram(diagram)

    def serialize_classes(
        self,
        class_names: List[Union[str, ClassDefinitionName]],
        follow_references=False,
        max_hops: int = None,
        include_upstream: bool = False,
    ) -> MERMAID_SERIALIZATION:
        """
        Serialize a list of classes as an ER Diagram.

        This will also traverse the reference graph and include any Entities reachable from the
        specified classes.

        By default, all reachable Entities are included, unless max_hops is specified.

        :param class_names: initial seed
        :param follow_references: if True, follow references even if not inlined
        :param max_hops: maximum number of hops to follow references
        :return:
        """
        visited = set()
        sv = self.schemaview
        stack = [(cn, 0) for cn in class_names]
        diagram = ERDiagram()
        while stack:
            cn, depth = stack.pop()
            if cn in visited:
                continue
            self.add_class(cn, diagram)
            visited.add(cn)
            if max_hops is not None and depth >= max_hops:
                continue
            for slot in sv.class_induced_slots(cn):
                rng = slot.range
                if rng in sv.all_classes():
                    if follow_references or sv.is_inlined(slot):
                        if rng not in visited:
                            stack.append((rng, depth + 1))

        # Now Add upstream classes if needed
        if include_upstream:
            for sn in sv.all_slots():
                slot = sv.schema.slots.get(sn)
                if slot and slot.range in set(class_names):
                    for cl in sv.all_classes():
                        if slot.name in sv.get_class(cl).slots and cl not in visited:
                            self.add_upstream_class(cl, set(class_names), diagram)
        return self.serialize_diagram(diagram)

    def serialize_diagram(self, diagram: ERDiagram) -> str:
        """
        Serialize an ER Diagram, from the native pydantic schema.

        :param diagram: ER Diagram
        :return:
        """
        er = str(diagram)
        if self.format == "markdown":
            return f"```mermaid\n{er}\n```\n"
        else:
            return er

    def add_upstream_class(self, class_name: ClassDefinitionName, targets: Set[str], diagram: ERDiagram) -> None:
        sv = self.schemaview
        cls = sv.get_class(class_name)
        entity = Entity(name=camelcase(cls.name))
        diagram.entities.append(entity)
        for slot in sv.class_induced_slots(class_name):
            if slot.range in targets:
                self.add_relationship(entity, slot, diagram)

    def add_class(self, class_name: ClassDefinitionName, diagram: ERDiagram) -> None:
        """
        Add a class to the ER Diagram.

        :param class_name: ClassDefinitionName
        :param diagram: ER Diagram
        :return:
        """
        sv = self.schemaview
        cls = sv.get_class(class_name)
        entity = Entity(name=camelcase(cls.name))
        diagram.entities.append(entity)
        for slot in sv.class_induced_slots(class_name):
            # TODO: schemaview should infer this
            if slot.range is None:
                slot.range = sv.schema.default_range or "string"
            if slot.range in sv.all_classes():
                self.add_relationship(entity, slot, diagram)
            else:
                self.add_attribute(entity, slot)

    def add_relationship(self, entity: Entity, slot: SlotDefinition, diagram: ERDiagram) -> None:
        """
        Add a relationship to the ER Diagram.

        :param class_name: ClassDefinitionName
        :param slot: SlotDefinition
        :param diagram: ER Diagram
        :return:
        """
        sv = self.schemaview
        rel_type = RelationshipType(
            right_cardinality=Cardinality(
                required=slot.required is True, multivalued=slot.multivalued is True, is_left=True
            ),
            left_cardinality=Cardinality(is_left=False),
        )
        rel = Relationship(
            first_entity=entity.name,
            relationship_type=rel_type,
            second_entity=camelcase(sv.get_class(slot.range).name),
            relationship_label=slot.name,
        )
        diagram.relationships.append(rel)

    def add_attribute(self, entity: Entity, slot: SlotDefinition) -> None:
        """
        Add an attribute to the ER Diagram.

        :param class_name: Class
        :param slot: SlotDefinition
        :return:
        """
        if self.exclude_attributes:
            return
        dt = slot.range
        if slot.multivalued:
            # NOTE: mermaid does not support []s or *s in attribute types
            dt = f"{dt}List"
        attr = Attribute(name=underscore(slot.name), datatype=dt)
        entity.attributes.append(attr)


@shared_arguments(ERDiagramGenerator)
@click.option(
    "--structural/--no-structural",
    default=True,
    help="If True, then only the tree_root and entities reachable from the root are drawn",
)
@click.option(
    "--exclude-attributes/--no-exclude-attributes",
    default=False,
    help="If True, do not include attributes in entities",
)
@click.option(
    "--follow-references/--no-follow-references",
    default=False,
    help="If True, follow references even if not inlined",
)
@click.option("--max-hops", default=None, type=click.INT, help="Maximum number of hops")
@click.option("--classes", "-c", multiple=True, help="List of classes to serialize")
@click.option("--include-upstream", is_flag=True, help="Include upstream classes")
@click.version_option(__version__, "-V", "--version")
@click.command()
def cli(
    yamlfile,
    classes: List[str],
    max_hops: Optional[int],
    follow_references: bool,
    include_upstream: bool = False,
    **args,
):
    """Generate a mermaid ER diagram from a schema.

    By default, all entities traversable from the tree_root are included. If no tree_root is
    present, then all entities are included.

    To create an ER diagram for selected classes, use the --classes option.
    """
    gen = ERDiagramGenerator(
        yamlfile,
        **args,
    )
    if classes:
        print(
            gen.serialize_classes(
                classes,
                follow_references=follow_references,
                max_hops=max_hops,
                include_upstream=include_upstream,
            )
        )
    else:
        print(gen.serialize())


if __name__ == "__main__":
    cli()
