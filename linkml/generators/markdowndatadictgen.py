"""
Markdown Data Dictionary Generator

Generates comprehensive markdown documentation for LinkML schemas,
including class diagrams, ERD diagrams, and detailed documentation
for all schema elements.
"""

import logging
import os
import re
from dataclasses import dataclass
from typing import Any, Optional, Union

import click
import pydantic
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    ClassDefinitionName,
    Element,
    EnumDefinition,
    SlotDefinition,
    SubsetDefinition,
    TypeDefinition,
)
from linkml_runtime.utils.formatutils import be, camelcase

from linkml._version import __version__
from linkml.generators.erdiagramgen import ERDiagramGenerator
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.typereferences import References

logger = logging.getLogger(__name__)


class MarkdownTable:
    """Simple markdown table generator to replace py_markdown_table dependency"""

    def __init__(self, data: list[dict[str, str]]):
        self.data = data
        self.quote = True
        self.row_sep = "default"

    def set_params(self, quote: bool = True, row_sep: str = "default"):
        """Set table formatting parameters"""
        self.quote = quote
        self.row_sep = row_sep
        return self

    def get_markdown(self) -> str:
        """Generate markdown table from data"""
        if not self.data:
            return ""

        # Get column headers from first row
        headers = list(self.data[0].keys())

        # Build header row
        header_row = "| " + " | ".join(headers) + " |"

        # Build separator row
        separator_row = "|" + "|".join([" --- " for _ in headers]) + "|"

        # Build data rows
        rows = []
        for row_data in self.data:
            cells = []
            for header in headers:
                cell_value = str(row_data.get(header, ""))
                # Clean up cell content - remove newlines and excessive whitespace
                cell_value = " ".join(cell_value.split())
                # Escape pipe characters in cell content
                cell_value = cell_value.replace("|", "\\|")
                cells.append(cell_value)
            rows.append("| " + " | ".join(cells) + " |")

        # Combine all parts
        table_parts = [header_row, separator_row] + rows

        if self.row_sep == "markdown":
            return "\n".join(table_parts)
        else:
            return "\n".join(table_parts)


def markdown_table(data: list[dict[str, str]]) -> MarkdownTable:
    """Create a markdown table from list of dictionaries - replacement for py_markdown_table"""
    return MarkdownTable(data)


def _sanitize_class_name_for_mermaid(name: str) -> str:
    """Sanitize class name for mermaid diagram compatibility"""
    # Replace spaces and special characters with underscores
    # Mermaid doesn't like spaces in class names
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


class ClassRelationship(pydantic.BaseModel):
    base: str
    derived: str
    relationship_type: str = "inheritance"  # "inheritance" or "mixin"

    def __str__(self) -> str:
        safe_base = _sanitize_class_name_for_mermaid(self.base)
        safe_derived = _sanitize_class_name_for_mermaid(self.derived)
        if self.relationship_type == "mixin":
            return f"{safe_base} ..> {safe_derived}"  # ClassA ..> MixinB (ClassA uses MixinB)
        else:
            return f"{safe_base} <|-- {safe_derived}"  # inheritance

    def __hash__(self):
        return hash((self.base, self.derived, self.relationship_type))


class ClassDiagram(pydantic.BaseModel):
    relationships: set[ClassRelationship] = set({})

    def add_relationship(self, base, derived, relationship_type="inheritance"):
        self.relationships |= {ClassRelationship(base=base, derived=derived, relationship_type=relationship_type)}

    def __str__(self) -> str:
        # Sort relationships for deterministic output
        sorted_rels = sorted(self.relationships, key=lambda r: (r.relationship_type, r.base, r.derived))
        rels = "\n".join([str(r) for r in sorted_rels])
        return f"classDiagram\n{rels}\n"


@dataclass
class MarkdownDataDictGen(Generator):
    """
    Generates single page data dictionary for a LinkML schema

    All schema elements (class, slot, type, enum) are placed into a single document, with a ERD diagram at the top

    The markdown is suitable to create discussion documents used while developing a new data model
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.0.1"
    directory_output = True
    valid_formats = ["md"]
    visit_all_class_slots = False
    uses_schemaloader = True

    # ObjectVars
    anchor_style: str = "mkdocs"
    output: Optional[str] = None
    image_directory: Optional[str] = None
    classes: set[ClassDefinitionName] = None
    image_dir: bool = False
    index_file: str = "index.md"
    noimages: bool = False
    noyuml: bool = False
    no_types_dir: bool = False
    warn_on_exist: bool = False
    gen_classes: Optional[set[ClassDefinitionName]] = None
    gen_classes_neighborhood: Optional[References] = None

    schema_classes = set[ClassDefinition]

    def visit_schema(
        self,
        output: str = None,
        classes: set[ClassDefinitionName] = None,
        image_dir: bool = False,
        index_file: str = "index.md",
        noimages: bool = False,
        **_,
    ) -> str:
        """Generate markdown documentation for the entire schema."""
        self._initialize_generation(output, classes)

        items = []
        items.extend(self._generate_header())
        items.extend(self._generate_diagrams())
        items.extend(self._generate_class_sections())
        items.extend(self._generate_enum_sections())

        # Filter out None items and join
        items = [item for item in items if item is not None]
        output = "\n".join(items) + "\n"
        return pad_heading(output)

    def _initialize_generation(self, output: str, classes: set[ClassDefinitionName]):
        """Initialize generation parameters and validate inputs."""
        self.gen_classes = classes if classes else []
        for cls in self.gen_classes:
            if cls not in self.schema.classes:
                raise ValueError(f"Unknown class name: {cls}")

        if self.gen_classes:
            self.gen_classes_neighborhood = self.neighborhood(list(self.gen_classes))

        self.output = output
        self.schema_class_names = {c.name for c in self.schema.classes.values()}

    def _generate_header(self) -> list[str]:
        """Generate the document header with metadata."""
        return [
            self.frontmatter(f"{self.schema.name.upper()}"),
            self.para(f"**metamodel version:** {self.schema.metamodel_version}\n\n**version:** {self.schema.version}"),
            self.para(be(self.schema.description)),
        ]

    def _generate_diagrams(self) -> list[str]:
        """Generate class and ERD diagrams."""
        items = []

        # Class Diagram
        items.append(self.header(2, "Class Diagram"))
        items.append(f"```mermaid\n{self.full_class_diagram()}\n```")

        # ERD Diagram
        erd_gen = ERDiagramGenerator(self.schema_location, exclude_abstract_classes=True, exclude_attributes=False)
        items.append(self.header(2, "ERD Diagram"))
        items.append(erd_gen.serialize())

        return items

    def _generate_class_sections(self) -> list[str]:
        """Generate documentation for all class types."""
        items = []
        abstract_classes, concrete_classes, mixins = self._categorize_classes()

        # Abstract Classes
        if abstract_classes:
            items.append(self.header(2, "Abstract Classes"))
            for cls in abstract_classes:
                logger.info(f"Processing abstract class {cls.name}")
                items.extend(self.describe_class(cls))
                items.append("\n\n")

        # Concrete Classes
        if concrete_classes:
            items.append(self.header(2, "Classes"))
            for cls in concrete_classes:
                logger.info(f"Processing class {cls.name}")
                items.extend(self.describe_class(cls))
                items.append("\n\n")

        # Mixins
        if mixins:
            items.append(self.header(2, "Mixins"))
            for cls in mixins:
                items.extend(self.describe_class(cls))

        return items

    def _categorize_classes(self):
        """Categorize classes into abstract, concrete, and mixins with rank-based sorting."""
        abstract_classes = []
        concrete_classes = []
        mixins = []

        # Sort classes by rank (if exists) then alphabetically
        def class_sort_key(cls):
            rank = getattr(cls, "rank", None)
            rank_value = rank if rank is not None else float("inf")
            return (rank_value, cls.name)

        for cls in sorted(self.schema.classes.values(), key=class_sort_key):
            if cls.mixin:
                mixins.append(cls)
            elif cls.abstract:
                abstract_classes.append(cls)
            else:
                concrete_classes.append(cls)

        return abstract_classes, concrete_classes, mixins

    def _generate_enum_sections(self) -> list[str]:
        """Generate documentation for enums with rank-based sorting."""
        items = []

        # Sort enums by rank (if exists) then alphabetically
        def enum_sort_key(enum):
            rank = getattr(enum, "rank", None)
            rank_value = rank if rank is not None else float("inf")
            return (rank_value, enum.name)

        enums = sorted(self.schema.enums.values(), key=enum_sort_key)

        if enums:
            items.append(self.header(2, "Enums"))
            for enum in enums:
                items.extend(self.describe_enum(enum))

        return items

    def local_class_diagram(self, cls: ClassDefinition) -> ClassDiagram:
        """Generate a local class diagram showing relationships for a specific class."""
        class_diagram = ClassDiagram()

        # Add inheritance relationships (ancestors)
        self._add_ancestor_relationships(cls, class_diagram)

        # Add mixin relationships
        if cls.mixins:
            for mixin in sorted(cls.mixins):
                class_diagram.add_relationship(base=cls.name, derived=mixin, relationship_type="mixin")

        # Add child relationships
        children = self.get_class_children(cls.name)
        for child in children:
            class_diagram.add_relationship(base=cls.name, derived=child)

        return class_diagram

    def _add_ancestor_relationships(self, cls: ClassDefinition, diagram: ClassDiagram):
        """Recursively add ancestor relationships to the diagram."""
        if cls.is_a:
            diagram.add_relationship(base=cls.is_a, derived=cls.name)
            parent_cls = self.schema.classes.get(cls.is_a)
            if parent_cls:
                self._add_ancestor_relationships(parent_cls, diagram)

    def full_class_diagram(self) -> ClassDiagram:
        """Generate a diagram showing all inheritance relationships in the schema."""
        class_diagram = ClassDiagram()
        for cls in sorted(self.schema.classes.values(), key=lambda c: c.name):
            if cls.is_a:
                class_diagram.add_relationship(base=cls.is_a, derived=cls.name)
        return class_diagram

    def describe_enum(self, enu: EnumDefinition) -> list[str]:
        """Generate comprehensive documentation for an enum."""
        items = []

        # Basic enum information
        class_curi = self.namespaces.uri_or_curie_for(str(self.namespaces._base), camelcase(enu.name))
        class_uri = self.namespaces.uri_for(class_curi)
        items.append(self.element_header(enu, enu.name, class_curi, class_uri))

        # Enum values table
        items.extend(self._generate_enum_values_table(enu))

        # Usage information
        items.extend(self._generate_enum_usage_section(enu))

        return items

    def _generate_enum_values_table(self, enu: EnumDefinition) -> list[str]:
        """Generate table of enum values with rank-based sorting."""
        items = []
        attributes = []

        # Sort enum values by rank (if exists) then by text
        def value_sort_key(value):
            rank = getattr(value, "rank", None)
            rank_value = rank if rank is not None else float("inf")
            return (rank_value, value.text or "")

        for value in sorted(enu.permissible_values.values(), key=value_sort_key):
            attributes.append(
                {
                    "Text": value.text,
                    "Meaning:": value.meaning,
                    "Description": value.description if value.description else "",
                }
            )

        if attributes:
            table = markdown_table(attributes).set_params(quote=False, row_sep="markdown")
            items.append(table.get_markdown())

        return items

    def _generate_enum_usage_section(self, enu: EnumDefinition) -> list[str]:
        """Generate the 'Used by' section for an enum."""
        items = []

        if enu.name in self.synopsis.enumrefs:
            enu_refs = self.synopsis.enumrefs.get(enu.name)
            if enu_refs:
                items.append(self.header(4, "Used by"))
                for slot_name in sorted(enu_refs.slotrefs):
                    slot = self.schema.slots[slot_name]
                    for domain in sorted(slot.domain_of):
                        items.append(
                            self.bullet(
                                f" **{self.class_link(domain)}** "
                                f"*{self.slot_link(slot, add_subset=False)}*{self.predicate_cardinality(slot)} "
                            )
                        )

        return items

    def describe_class(self, cls: ClassDefinition) -> list[str]:
        """Generate comprehensive documentation for a class."""
        items = []

        # Basic class information
        class_curi = self.namespaces.uri_or_curie_for(str(self.namespaces._base), camelcase(cls.name))
        class_uri = self.namespaces.uri_for(class_curi)
        items.append(self.element_header(cls, cls.name, class_curi, class_uri))

        # Gather class relationships
        class_relationships = self._gather_class_relationships(cls)

        # Add class diagram
        items.extend(self._generate_class_diagram(cls, class_relationships))

        # Add identifier prefixes
        if cls.id_prefixes:
            items.append(self.header(3, "Identifier prefixes"))
            for prefix in cls.id_prefixes:
                items.append(self.bullet(f"{prefix}"))

        # Add attributes section
        items.extend(self._generate_attributes_section(cls))

        # Add relationship sections
        items.extend(self._generate_relationship_sections(cls, class_relationships))

        return items

    def _gather_class_relationships(self, cls: ClassDefinition) -> dict[str, Any]:
        """Gather all relationship information for a class."""
        class_refs = self.synopsis.classrefs.get(cls.name)
        has_references_to = class_refs is not None and bool(class_refs.slotrefs)
        children = set(self.get_class_children(cls.name))

        mixin_refs = self.synopsis.mixinrefs.get(cls.name)
        used_as_mixin_by = sorted(mixin_refs.classrefs) if mixin_refs else []

        # Collect range classes for ERD
        range_classes = []
        for slot_name in sorted(cls.slots):
            slot = self.schema.slots[slot_name]
            if slot.range in self.schema.classes:
                range_classes.append(slot.range)

        # Build ERD classes list
        erd_classes = []
        if has_references_to:
            for c in sorted(class_refs.classrefs):
                if c not in children and c not in used_as_mixin_by:
                    erd_classes.append(c)
            for c in class_refs.slotrefs:
                if self.schema.slots[c].range == cls.name:
                    erd_classes.extend(self.schema.slots[c].domain_of)
        erd_classes.extend(range_classes)

        return {
            "class_refs": class_refs,
            "has_references_to": has_references_to,
            "children": children,
            "used_as_mixin_by": used_as_mixin_by,
            "erd_classes": erd_classes,
        }

    def _generate_class_diagram(self, cls: ClassDefinition, relationships: dict[str, Any]) -> list[str]:
        """Generate appropriate diagram for the class."""
        items = []
        erd_classes = relationships["erd_classes"]
        children = relationships["children"]

        if erd_classes:
            erd_gen = ERDiagramGenerator(self.schema_location, exclude_attributes=True, structural=False)
            erd_classes.append(cls.name)
            diagram = erd_gen.serialize_classes(erd_classes, follow_references=False, max_hops=0)
            items.append(diagram)
        elif children or cls.is_a:
            items.append(self.header(4, "Local class diagram"))
            items.append(f"```mermaid\n{self.local_class_diagram(cls)}\n```")

        return items

    def _generate_attributes_section(self, cls: ClassDefinition) -> list[str]:
        """Generate the attributes section for a class."""
        items = []
        slots_table = self.slots_table(cls)

        if slots_table:
            items.append(self.header(4, "Attributes"))
            items.append(slots_table)
        else:
            items.append(self.para("This class has no attributes"))

        return items

    def _generate_relationship_sections(self, cls: ClassDefinition, relationships: dict[str, Any]) -> list[str]:
        """Generate all relationship sections for a class."""
        items = []

        # Parents
        if cls.is_a is not None:
            items.append(self.header(4, "Parents"))
            items.append(self.bullet(f"{self.class_link(cls.is_a, use_desc=True)}"))

        # Children
        if relationships["children"]:
            items.append(self.header(4, "Children"))
            self.list_children(relationships["children"], items)

        # Uses (mixins)
        if cls.mixins:
            items.append(self.header(4, "Uses"))
            for mixin in sorted(cls.mixins):
                items.append(self.bullet(f" mixin: {self.class_link(mixin, use_desc=True)}"))

        # Used as mixin by
        if relationships["used_as_mixin_by"]:
            items.append(self.header(4, "Used as mixin by"))
            for mixin in relationships["used_as_mixin_by"]:
                items.append(self.bullet(f"{self.class_link(mixin, use_desc=True)}"))

        # Referenced by
        if relationships["has_references_to"]:
            items.append(self.header(4, "Referenced by:"))
            self.list_classes(relationships["class_refs"], cls, items)

        return items

    def slots_table(self, cls: ClassDefinition) -> Optional[str]:
        """Generate a markdown table of class attributes/slots including inherited ones."""
        all_slots = self._collect_all_class_slots(cls)
        if not all_slots:
            return None

        attributes = []

        for slot in all_slots:
            # Determine slot source for styling
            source_info = self._get_slot_source(slot, cls)
            name_display = self._format_slot_name(slot.name, source_info)

            attributes.append(
                {
                    "Name": name_display,
                    "Cardinality:": self.predicate_cardinality(slot),
                    "Type": self.class_type_link(slot.range),
                    "Description": slot.description if slot.description else "",
                    "_slot_name": slot.name,  # Keep original name for sorting
                }
            )

        # Custom sort: parents, mixins, own, then alphabetical within each group
        attributes.sort(key=self._create_slot_sort_key(cls))

        # Remove the _slot_name field before creating table
        for attr in attributes:
            del attr["_slot_name"]

        return markdown_table(attributes).set_params(quote=False, row_sep="markdown").get_markdown()

    def _collect_all_class_slots(self, cls: ClassDefinition) -> list[SlotDefinition]:
        """Collect all slots for a class including those from mixins and inheritance."""
        all_slot_names = set()
        all_slots = []

        # Add direct slots
        for slot_name in cls.slots:
            if slot_name not in all_slot_names:
                all_slot_names.add(slot_name)
                all_slots.append(self.schema.slots[slot_name])

        # Add direct attributes (slots defined inline)
        if cls.attributes:
            for attr_name, attr_def in cls.attributes.items():
                if attr_name not in all_slot_names:
                    all_slot_names.add(attr_name)
                    all_slots.append(attr_def)

        # Add slots from mixins
        if cls.mixins:
            for mixin_name in cls.mixins:
                mixin_cls = self.schema.classes.get(mixin_name)
                if mixin_cls:
                    # Add mixin slots
                    for slot_name in mixin_cls.slots:
                        if slot_name not in all_slot_names:
                            all_slot_names.add(slot_name)
                            all_slots.append(self.schema.slots[slot_name])

                    # Add mixin attributes (inline slots)
                    if mixin_cls.attributes:
                        for attr_name, attr_def in mixin_cls.attributes.items():
                            if attr_name not in all_slot_names:
                                all_slot_names.add(attr_name)
                                all_slots.append(attr_def)

        # Add slots from parent classes (inheritance)
        if cls.is_a:
            parent_cls = self.schema.classes.get(cls.is_a)
            if parent_cls:
                parent_slots = self._collect_all_class_slots(parent_cls)
                for slot in parent_slots:
                    if slot.name not in all_slot_names:
                        all_slot_names.add(slot.name)
                        all_slots.append(slot)

        return all_slots

    def _get_slot_source(self, slot: SlotDefinition, cls: ClassDefinition) -> dict[str, Any]:
        """Determine where a slot comes from (own, mixin, or inheritance)."""
        # Check if it's directly owned by this class (in domain_of or attributes)
        if cls.name in slot.domain_of:
            return {"type": "own", "source": cls.name}

        # Check if it's a direct attribute of this class
        if cls.attributes and slot.name in cls.attributes:
            return {"type": "own", "source": cls.name}

        # Check if it comes from a mixin
        if cls.mixins:
            for mixin_name in cls.mixins:
                mixin_cls = self.schema.classes.get(mixin_name)
                if mixin_cls:
                    # Check mixin slots
                    if slot.name in mixin_cls.slots:
                        return {"type": "mixin", "source": mixin_name}
                    # Check mixin attributes
                    if mixin_cls.attributes and slot.name in mixin_cls.attributes:
                        return {"type": "mixin", "source": mixin_name}

        # Check if it comes from inheritance
        if cls.is_a:
            parent_cls = self.schema.classes.get(cls.is_a)
            if parent_cls:
                parent_source = self._get_slot_source(slot, parent_cls)
                if parent_source["type"] == "own":
                    return {"type": "inherited", "source": parent_source["source"]}
                else:
                    return parent_source

        return {"type": "unknown", "source": "unknown"}

    def _format_slot_name(self, slot_name: str, source_info: dict[str, Any]) -> str:
        """Format slot name based on its source."""
        if source_info["type"] == "own":
            return f"**{slot_name}**"  # Bold for own attributes
        elif source_info["type"] == "mixin":
            return f"*{slot_name}*"  # Italics for mixin attributes
        elif source_info["type"] == "inherited":
            return slot_name  # Regular for inherited attributes
        else:
            return f"*{slot_name}*"  # Default to italics for unknown

    def _create_slot_sort_key(self, cls: ClassDefinition):
        """Create a sort key function for slot attributes based on source, priority, rank, and name."""
        priority_slots = ["id", "name", "description"]

        def sort_key(attr):
            slot_name = attr["_slot_name"]
            slot = next((s for s in self._collect_all_class_slots(cls) if s.name == slot_name), None)

            if not slot:
                return (99, 0, float("inf"), slot_name)  # Unknown slots go last

            source_info = self._get_slot_source(slot, cls)
            source_type = source_info["type"]

            # Primary sort by source type: inherited (parents) -> mixins -> own
            if source_type == "inherited":
                primary_sort = 0
            elif source_type == "mixin":
                primary_sort = 1
            elif source_type == "own":
                primary_sort = 2
            else:
                primary_sort = 3  # unknown

            # Secondary sort by priority slots (id, name, description first)
            if slot_name in priority_slots:
                secondary_sort = priority_slots.index(slot_name)
            else:
                secondary_sort = len(priority_slots)  # Non-priority slots come after

            # Tertiary sort by rank (if exists)
            rank = getattr(slot, "rank", None)
            rank_value = rank if rank is not None else float("inf")

            # Quaternary sort alphabetically
            alphabetical_sort = slot_name

            return (primary_sort, secondary_sort, rank_value, alphabetical_sort)

        return sort_key

    def get_class_children(self, class_name: str) -> set[ClassDefinitionName]:
        """Get all direct children of a class."""
        if class_name in self.synopsis.classrefs:
            isa_refs = self.synopsis.isarefs.get(class_name)
            if isa_refs and isa_refs.classrefs:
                return isa_refs.classrefs
        return set()

    def list_children(self, class_refs: set[str], items: list[str]) -> None:
        """Add child class references to the items list."""
        for cls in sorted(class_refs):
            items.append(self.bullet(f"{self.class_link(cls, use_desc=True)}"))

    def list_classes(self, class_refs, cls: ClassDefinition, items: list[str]) -> None:
        """Add class references to the items list."""
        for slot_name in sorted(class_refs.slotrefs):
            slot = self.schema.slots[slot_name]
            if slot.range == cls.name:
                for domain in sorted(slot.domain_of):
                    items.append(
                        self.bullet(
                            f" **{self.class_link(domain)}** : "
                            f"*{self.slot_link(slot, add_subset=False)}*{self.predicate_cardinality(slot)} "
                        )
                    )

    def element_header(self, obj: Element, name: str, curie: str, uri: str) -> str:
        header_label = f"~~{name}~~ _(deprecated)_" if obj.deprecated else f"{name}"
        out = self.header(3, header_label)
        out += self.para(be(obj.description))
        return out

    def class_hier(self, cls: ClassDefinition, level=0) -> str:
        items = []
        items.append(self.bullet(self.class_link(cls, use_desc=True), level))
        if cls.name in sorted(self.synopsis.isarefs):
            for child in sorted(self.synopsis.isarefs[cls.name].classrefs):
                items.append(self.class_hier(self.schema.classes[child], level + 1))
        return "\n".join(items) if items else None

    def is_secondary_ref(self, en: str) -> bool:
        """Determine whether 'en' is the name of something in the neighborhood of the requested classes

        @param en: element name
        @return: True if 'en' is the name of a slot, class or type in the immediate neighborhood of of what we are
        building
        """
        if not self.gen_classes:
            return True
        elif en in self.schema.classes:
            return en in self.gen_classes_neighborhood.classrefs
        elif en in self.schema.slots:
            return en in self.gen_classes_neighborhood.slotrefs
        elif en in self.schema.types:
            return en in self.gen_classes_neighborhood.typerefs
        else:
            return True

    # --
    # FORMATTING
    # --
    @staticmethod
    def predicate_cardinality(slot: SlotDefinition) -> str:
        """Emit cardinality for a suffix on a predicate"""
        if slot.multivalued:
            card_str = "1..\\*" if slot.required else "0..\\*"
        else:
            card_str = "1..1" if slot.required else "0..1"
        return f"  <sub>{card_str}</sub>"

    @staticmethod
    def range_cardinality(slot: SlotDefinition) -> str:
        """Emits cardinality decorator at end of type"""
        if slot.multivalued:
            card_str = "1..\\*" if slot.required else "0..\\*"
        else:
            card_str = "1..1" if slot.required else "0..1"
        return f"  <sub><b>{card_str}</b></sub>"

    @staticmethod
    def anchor(id_: str) -> str:
        return f'<a name="{id_}">'

    @staticmethod
    def anchorend() -> str:
        return "</a>"

    def header(self, level: int, txt: str) -> str:
        txt = self.get_metamodel_slot_name(txt)
        out = f"\n{'#' * level} {txt}\n"
        return out

    @staticmethod
    def para(txt: str) -> str:
        return f"\n{txt}\n"

    @staticmethod
    def bullet(txt: str, level=0) -> str:
        return f"{'    ' * level} * {txt}"

    def frontmatter(self, thingtype: str, layout="default") -> str:
        return self.header(1, thingtype)
        # print(f'---\nlayout: {layout}\n---\n')

    def bbin(self, obj: Element) -> str:
        """Boldify built in types

        @param obj: object name or id
        @return:
        """
        return obj.name if isinstance(obj, Element) else f"**{obj}**" if obj in self.synopsis.typebases else obj

    def desc_for(self, obj: Element, doing_descs: bool) -> str:
        """Return a description for object if it is unique (different than its parent)

        @param obj: object to be described
        @param doing_descs: If false, always return an empty string
        @return: text or empty string
        """
        if obj.description and doing_descs:
            if isinstance(obj, SlotDefinition) and obj.is_a:
                parent = self.schema.slots[obj.is_a]
            elif isinstance(obj, ClassDefinition) and obj.is_a:
                parent = self.schema.classes[obj.is_a]
            else:
                parent = None
            return "" if parent and obj.description == parent.description else obj.description
        return ""

    def _link(
        self,
        obj: Optional[Element],
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        """Create a link to ref if appropriate.

        @param ref: the name or value of a class, slot, type or the name of a built in type.
        @param after_link: Text to put between link and description
        @param use_desc: True means append a description after the link if available
        @param add_subset: True means add any subset information that is available
        @return:
        """

        def make_anchor(name: str) -> str:
            if self.anchor_style == "mkdocs":
                return name.lower()
            else:
                return camelcase(name)

        nl = "\n"
        if obj is None or not self.is_secondary_ref(obj.name):
            return self.bbin(obj)
        if isinstance(obj, TypeDefinition):
            link_name = camelcase(obj.name)
            link_ref = f"types/{link_name}" if not self.no_types_dir else f"{link_name}"
        elif isinstance(obj, ClassDefinition):
            link_name = camelcase(obj.name)
            link_ref = make_anchor(link_name)
        elif isinstance(obj, EnumDefinition):
            link_name = camelcase(obj.name)
            link_ref = make_anchor(link_name)
        elif isinstance(obj, SubsetDefinition):
            link_name = camelcase(obj.name)
            link_ref = make_anchor(link_name)
        else:
            link_name = obj.name
            link_ref = link_name
        desc = self.desc_for(obj, use_desc)
        return (
            f"[{link_name}]"
            f"(#{link_ref})" + (f" {after_link} " if after_link else "") + (f" - {desc.split(nl)[0]}" if desc else "")
        )

    def type_link(
        self,
        ref: Optional[Union[str, TypeDefinition]],
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        return ref

    def slot_link(
        self,
        ref: Optional[Union[str, SlotDefinition]],
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        return self._link(
            self.schema.slots[ref] if isinstance(ref, str) else ref,
            after_link=after_link,
            use_desc=use_desc,
            add_subset=add_subset,
        )

    def class_link(
        self,
        ref: Optional[Union[str, ClassDefinition]],
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        return self._link(
            self.schema.classes[ref] if isinstance(ref, str) else ref,
            after_link=after_link,
            use_desc=use_desc,
            add_subset=add_subset,
        )

    def class_type_link(
        self,
        ref: Optional[Union[str, ClassDefinition, TypeDefinition, EnumDefinition]],
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        if isinstance(ref, ClassDefinition):
            return self.class_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif isinstance(ref, TypeDefinition):
            return self.type_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif isinstance(ref, EnumDefinition):
            return self.type_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif ref in self.schema.classes:
            return self.class_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        elif ref in self.schema.enums:
            return self.enum_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)
        else:
            return self.type_link(ref, after_link=after_link, use_desc=use_desc, add_subset=add_subset)

    def enum_link(
        self,
        ref: Optional[Union[str, EnumDefinition]],
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        return self._link(
            self.schema.enums[ref] if isinstance(ref, str) else ref,
            after_link=after_link,
            use_desc=use_desc,
            add_subset=add_subset,
        )

    def subset_link(
        self,
        ref: Optional[Union[str, SubsetDefinition]],
        *,
        after_link: str = None,
        use_desc: bool = False,
    ) -> str:
        return self._link(
            self.schema.subsets[ref] if isinstance(ref, str) else ref,
            after_link=after_link,
            use_desc=use_desc,
        )


def pad_heading(text: str) -> str:
    """Add an extra newline to a non-top-level header that doesn't have one preceding it"""
    return re.sub(r"(?<!\n)\n##", "\n\n##", text)


@shared_arguments(MarkdownDataDictGen)
@click.command()
@click.option("--classes", "-c", multiple=True, help="Class(es) to emit")
@click.option(
    "--anchor-style",
    type=click.Choice(["mkdocs", "confluence"], case_sensitive=False),
    default="confluence",
    help="Choose anchor style: 'mkdocs' for lowercase markdown link anchors, 'confluence' to keep as is",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate markdown documentation of a LinkML model"""
    gen = MarkdownDataDictGen(yamlfile, **kwargs)
    print(gen.serialize(**kwargs))


if __name__ == "__main__":
    cli()
