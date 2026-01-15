import logging
import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

import click
import pydantic

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import ClassDefinition, ClassDefinitionName, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

MERMAID_SERIALIZATION = str


class Attribute(pydantic.BaseModel):
    datatype: str = "string"
    name: str = None
    key: str = None
    comment: str = None

    def __str__(self):
        cmt = f'"{self.comment}"' if self.comment else ""
        return f"    {self.datatype} {self.name} {self.key if self.key else ''} {cmt}"


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
    attributes: list[Attribute] = []

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

    entities: list[Entity] = []
    relationships: list[Relationship] = []

    def _collapse_relationships(self, relationships: list[Relationship]) -> list[Relationship]:
        """
        Collapse multiple relationships between the same two entities into a single relationship
        with comma-separated labels.

        Only relationships with the same cardinality (relationship_type) are collapsed together,
        preserving semantic differences between required/optional and single/multivalued relationships.

        :param relationships: List of relationships
        :return: List of collapsed relationships
        """
        # Group relationships by (first_entity, second_entity, relationship_type) tuple
        # This preserves different cardinalities as separate relationships
        relationship_groups = {}
        for rel in relationships:
            # Use string representation of relationship_type for grouping
            rel_type_key = str(rel.relationship_type) if rel.relationship_type else ""
            key = (rel.first_entity, rel.second_entity, rel_type_key)
            if key not in relationship_groups:
                relationship_groups[key] = []
            relationship_groups[key].append(rel)

        # Collapse groups with multiple relationships
        collapsed = []
        for key, group in relationship_groups.items():
            if len(group) == 1:
                # Single relationship, keep as is
                collapsed.append(group[0])
            else:
                # Multiple relationships with same cardinality, combine labels
                base_rel = group[0]
                labels = [rel.relationship_label for rel in group if rel.relationship_label]
                combined_label = ", ".join(sorted(labels))

                # Create new collapsed relationship
                collapsed_rel = Relationship(
                    first_entity=base_rel.first_entity,
                    relationship_type=base_rel.relationship_type,
                    second_entity=base_rel.second_entity,
                    relationship_label=combined_label,
                )
                collapsed.append(collapsed_rel)

        return collapsed

    def __str__(self):
        # Sort entities and relationships for stable output
        sorted_entities = sorted(self.entities, key=lambda e: e.name)

        # Collapse multiple relationships between same entities
        collapsed_relationships = self._collapse_relationships(self.relationships)
        sorted_relationships = sorted(collapsed_relationships, key=str)

        ents = "\n".join([str(e) for e in sorted_entities])
        rels = "\n".join([str(r) for r in sorted_relationships])
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

    exclude_abstract_classes: bool = False
    """If True, do not include abstract classes in the diagram"""

    genmeta: bool = False
    gen_classvars: bool = True
    gen_slots: bool = True
    no_types_dir: bool = False
    use_slot_uris: bool = False

    preserve_names: bool = False
    """If true, preserve LinkML element names (classes/slots) in diagram labels."""

    def __post_init__(self):
        self.schemaview = SchemaView(self.schema)
        super().__post_init__()

    # Mermaid ERD reserved keywords that conflict with entity names
    # See: https://mermaid.js.org/syntax/entityRelationshipDiagram.html
    # "Class" confirmed as reserved; others may exist but are undocumented
    _MERMAID_ERD_RESERVED_KEYWORDS = {"Class"}

    def _sanitize_class_name_for_erd(self, name: str) -> str:
        """
        Sanitize class name for ERD diagram output.

        Mermaid ERD syntax has reserved keywords that conflict with common class names.
        This method prefixes problematic names with '__' to avoid conflicts.

        :param name: Original class name
        :return: Sanitized class name safe for ERD diagrams
        """
        if name in self._MERMAID_ERD_RESERVED_KEYWORDS:
            return f"__{name}"
        return name

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
        class_names: list[Union[str, ClassDefinitionName]],
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

    def add_upstream_class(self, class_name: ClassDefinitionName, targets: set[str], diagram: ERDiagram) -> None:
        sv = self.schemaview
        cls = sv.get_class(class_name)
        if self.exclude_abstract_classes and cls.abstract:
            return
        entity_name = cls.name if self.preserve_names else camelcase(cls.name)
        entity = Entity(name=self._sanitize_class_name_for_erd(entity_name))
        diagram.entities.append(entity)
        for slot in sv.class_induced_slots(class_name):
            if slot.range in targets:
                self.add_relationship(entity, slot, diagram)

    def _create_attribute_sort_key(self, slot: SlotDefinition, cls: ClassDefinition):
        """
        Create a sort key for attributes for stable, deterministic output.

        Attributes are sorted by:
        1. Source type (own/direct slots first, then inherited)
        2. Priority slots (id, name, description)
        3. Rank (if defined)
        4. Alphabetically

        :param slot: The slot to create a sort key for
        :param cls: The class this slot belongs to
        :return: Sort key tuple
        """
        sv = self.schemaview
        priority_slots = ["id", "name", "description"]

        # Determine if slot is inherited or own
        # A slot is inherited if it's in domain_of of a parent class AND not overridden
        # in the current class's slot_usage (which makes it "own")
        is_inherited = False
        domain_of = slot.domain_of if hasattr(slot, "domain_of") and slot.domain_of else []

        # Check if slot is explicitly customized in current class's slot_usage
        slot_overridden_in_current = cls.slot_usage and slot.name in cls.slot_usage

        if domain_of and hasattr(cls, "name") and cls.name and not slot_overridden_in_current:
            # Use class_ancestors for efficiency (includes is_a and mixins)
            for ancestor in sv.class_ancestors(cls.name, reflexive=False):
                if ancestor in domain_of:
                    is_inherited = True
                    break

        # Primary sort: own/direct (0) vs inherited (1)
        primary_sort = 1 if is_inherited else 0

        # Secondary sort: priority slots come first
        if slot.name in priority_slots:
            secondary_sort = priority_slots.index(slot.name)
        else:
            secondary_sort = len(priority_slots)

        # Tertiary sort: by rank if exists
        rank = getattr(slot, "rank", None)
        rank_value = rank if rank is not None else float("inf")

        # Quaternary sort: alphabetically
        alphabetical_sort = slot.name

        return (primary_sort, secondary_sort, rank_value, alphabetical_sort)

    def add_class(self, class_name: ClassDefinitionName, diagram: ERDiagram) -> None:
        """
        Add a class to the ER Diagram.

        :param class_name: ClassDefinitionName
        :param diagram: ER Diagram
        :return:
        """
        sv = self.schemaview
        cls = sv.get_class(class_name)
        if self.exclude_abstract_classes and cls.abstract:
            return
        entity_name = cls.name if self.preserve_names else camelcase(cls.name)
        entity = Entity(name=self._sanitize_class_name_for_erd(entity_name))
        diagram.entities.append(entity)

        # Collect all slots first (to enable sorting before adding)
        all_slots = {}  # slot_name -> SlotDefinition
        relationship_slots = []
        attribute_slots = []

        # Process regular induced slots
        for slot in sv.class_induced_slots(class_name):
            # TODO: schemaview should infer this
            if slot.range is None:
                slot.range = sv.schema.default_range or "string"
            all_slots[slot.name] = slot

        # Also process slots defined in slot_usage (which may not appear in induced_slots)
        # This includes slot_usage from the current class and all ancestors (including mixins)
        slot_usage_to_check = set()

        # Collect slot_usage from current class
        if cls.slot_usage:
            slot_usage_to_check.update(cls.slot_usage.keys())

        # Collect slot_usage from all ancestor classes (includes is_a and mixins)
        for ancestor_name in sv.class_ancestors(class_name, reflexive=False):
            ancestor_cls = sv.get_class(ancestor_name)
            if ancestor_cls and ancestor_cls.slot_usage:
                slot_usage_to_check.update(ancestor_cls.slot_usage.keys())

        # Process all slot_usage entries
        for slot_name in slot_usage_to_check:
            if slot_name not in all_slots:
                # Get the induced slot to get the properly overridden range
                try:
                    slot = sv.induced_slot(slot_name, class_name)
                    if slot.range is None:
                        slot.range = sv.schema.default_range or "string"
                    all_slots[slot_name] = slot
                except (KeyError, AttributeError, ValueError) as e:
                    # Slot might not exist, have missing attributes, or not be a valid induced slot, skip it
                    logger.debug(f"Could not get induced slot '{slot_name}' for class '{class_name}': {e}")

        # Separate into relationships and attributes
        for slot in all_slots.values():
            if slot.range in sv.all_classes():
                relationship_slots.append(slot)
            else:
                attribute_slots.append(slot)

        # Sort attribute slots using the same logic as the markdown data dictionary
        attribute_slots.sort(key=lambda s: self._create_attribute_sort_key(s, cls))

        # Add sorted attributes to entity
        for slot in attribute_slots:
            self.add_attribute(entity, slot)

        # Add relationships (order doesn't matter as much for relationships)
        for slot in relationship_slots:
            self.add_relationship(entity, slot, diagram)

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
        second_entity_name = (
            sv.get_class(slot.range).name if self.preserve_names else camelcase(sv.get_class(slot.range).name)
        )
        rel = Relationship(
            first_entity=entity.name,
            relationship_type=rel_type,
            second_entity=self._sanitize_class_name_for_erd(second_entity_name),
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
        attr = Attribute(name=(slot.name if self.preserve_names else underscore(slot.name)), datatype=dt)
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
    "--exclude-abstract-classes/--no-exclude-abstract-classes",
    default=False,
    help="If True, do not include abstract classes in the diagram",
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
@click.command(name="erdiagram")
def cli(
    yamlfile,
    classes: list[str],
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
