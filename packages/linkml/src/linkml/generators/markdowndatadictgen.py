"""
Markdown Data Dictionary Generator

Generates comprehensive markdown documentation for LinkML schemas,
including class diagrams, ERD diagrams, and detailed documentation
for all schema elements.
"""

import base64
import hashlib
import logging
import os
import re
import urllib.request
import zlib
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.dom import minidom

import click
import pydantic
import yaml

from linkml._version import __version__
from linkml.generators.erdiagramgen import ERDiagramGenerator
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.typereferences import References
from linkml_runtime import SchemaView
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
from linkml_runtime.utils.yamlutils import extended_str

logger = logging.getLogger(__name__)


class MarkdownTable:
    """Simple markdown table generator."""

    def __init__(self, data: list[dict[str, str]]):
        self.data = data

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
        return "\n".join(table_parts)


def _sanitize_class_name_for_mermaid(name: str) -> str:
    """Sanitize class name for mermaid diagram compatibility"""
    # Replace spaces and special characters with underscores
    # Mermaid doesn't like spaces in class names
    return re.sub(r"[^a-zA-Z0-9_]", "_", name)


class SvgCache:
    """Cache for SVG diagrams using git-like 2-level directory hierarchy."""

    def __init__(self, cache_dir: str | None = None):
        self.cache_dir = cache_dir

    def get_cache_path(self, content_hash: str) -> tuple[str, str] | None:
        """Get cache file path for content hash using git-like 2-level hierarchy."""
        if not self.cache_dir:
            return None

        # Use .kroki-cache subdirectory within cache_dir
        cache_base = Path(self.cache_dir) / ".kroki-cache"

        # Git-like structure: first 2 chars / next 2 chars / rest.svg
        # Example: ab2345acdef -> ab/23/45acdef.svg
        if len(content_hash) < 4:
            # Fallback for short hashes
            level1 = content_hash
            level2 = "00"
            rest = content_hash
        else:
            level1 = content_hash[:2]
            level2 = content_hash[2:4]
            rest = content_hash[4:]

        cache_path = cache_base / level1 / level2 / f"{rest}.svg"

        # Return absolute cache path and path relative to cache_dir for reading
        relative_to_cache = f".kroki-cache/{level1}/{level2}/{rest}.svg"
        return (str(cache_path), relative_to_cache)

    def get(self, diagram_source: str) -> str | None:
        """Return cached SVG content if found, None otherwise."""
        content_hash = hashlib.sha256(diagram_source.encode("utf-8")).hexdigest()

        cache_info = self.get_cache_path(content_hash)
        if not cache_info:
            return None

        cache_file, _ = cache_info
        cache_path = Path(cache_file)

        if cache_path.exists():
            logging.debug(f"Cache hit for diagram (hash: {content_hash[:12]}...)")
            try:
                with open(cache_path, encoding="utf-8") as f:
                    return f.read()
            except Exception as e:
                logging.warning(f"Failed to read cached SVG: {e}")
                return None

        return None

    def save(self, diagram_source: str, svg_content: str) -> None:
        """Save generated SVG to cache."""
        content_hash = hashlib.sha256(diagram_source.encode("utf-8")).hexdigest()

        cache_info = self.get_cache_path(content_hash)
        if not cache_info:
            return

        cache_file, _ = cache_info
        cache_path = Path(cache_file)

        # Create parent directories
        cache_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            with open(cache_path, "w", encoding="utf-8") as f:
                f.write(svg_content)
            logging.debug(f"Cached SVG for diagram (hash: {content_hash[:12]}...)")
        except Exception as e:
            logging.warning(f"Failed to cache SVG: {e}")


class DiagramRenderer:
    """Renders diagrams via Kroki server with caching and SVG post-processing."""

    def __init__(
        self,
        kroki_server: str | None = None,
        diagram_dir: str | None = None,
        pretty_format: bool = False,
    ):
        self.kroki_server = kroki_server
        self.diagram_dir = diagram_dir
        self.pretty_format = pretty_format
        self._diagram_counter = 0

    def format_svg(self, svg_content: str) -> str:
        """Pretty-format SVG content with proper indentation."""
        try:
            dom = minidom.parseString(svg_content)
            pretty_xml = dom.toprettyxml(indent="  ", encoding=None)

            # Remove the XML declaration line if present
            lines = pretty_xml.split("\n")
            if lines and lines[0].startswith("<?xml"):
                lines = lines[1:]

            # Remove extra blank lines that minidom sometimes adds
            cleaned_lines = []
            prev_blank = False
            for line in lines:
                is_blank = not line.strip()
                if is_blank and prev_blank:
                    continue
                cleaned_lines.append(line)
                prev_blank = is_blank

            return "\n".join(cleaned_lines).strip() + "\n"

        except Exception as e:
            logging.debug(f"Failed to pretty-format SVG: {e}")
            return svg_content

    def render(self, diagram_source: str, diagram_type: str = "mermaid", diagram_name: str | None = None) -> str:
        """Render diagram via Kroki server with caching, or return mermaid code block if no server."""
        clean_source = diagram_source.strip()
        if clean_source.startswith(f"```{diagram_type}"):
            lines = clean_source.split("\n")
            clean_source = "\n".join(lines[1:-1]) if len(lines) > 2 else clean_source

        if not self.kroki_server:
            return f"```{diagram_type}\n{clean_source}\n```"

        try:
            svg_content = None
            cache = SvgCache(self.diagram_dir)

            cached_svg = cache.get(clean_source)
            if cached_svg:
                svg_content = cached_svg
            else:
                logging.debug(f"Cache miss for diagram '{diagram_name or 'unnamed'}', fetching from Kroki")
                source_size_kb = len(clean_source.encode("utf-8")) / 1024

                if source_size_kb > 1.0:
                    logging.debug(f"Diagram '{diagram_name or 'unnamed'}' is {source_size_kb:.1f}KB, using POST")
                    kroki_url = f"{self.kroki_server.rstrip('/')}/{diagram_type}/svg"
                    req = urllib.request.Request(
                        kroki_url,
                        data=clean_source.encode("utf-8"),
                        headers={"Content-Type": "text/plain; charset=utf-8"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req, timeout=60) as response:
                        svg_content = response.read().decode("utf-8")
                else:
                    compressed = zlib.compress(clean_source.encode("utf-8"), level=9)
                    encoded = base64.urlsafe_b64encode(compressed).decode("utf-8")
                    kroki_url = f"{self.kroki_server.rstrip('/')}/{diagram_type}/svg/{encoded}"
                    req = urllib.request.Request(kroki_url, method="GET")
                    with urllib.request.urlopen(req, timeout=30) as response:
                        svg_content = response.read().decode("utf-8")

                if svg_content:
                    cache.save(clean_source, svg_content)

            if svg_content is None:
                raise Exception("Failed to get SVG content from Kroki")

            if self.pretty_format:
                svg_content = self.format_svg(svg_content)

            if self.diagram_dir:
                diagram_path = Path(self.diagram_dir)
                diagram_path.mkdir(parents=True, exist_ok=True)

                if diagram_name:
                    filename = f"{diagram_name}.svg"
                else:
                    self._diagram_counter += 1
                    filename = f"diagram_{self._diagram_counter}.svg"

                svg_file = diagram_path / filename
                with open(svg_file, "w", encoding="utf-8") as f:
                    f.write(svg_content)

                relative_dir = Path(self.diagram_dir).name
                relative_path = f"{relative_dir}/{filename}"
                return f"![{diagram_name or 'Diagram'}]({relative_path})"
            else:
                return svg_content

        except Exception as e:
            diagram_desc = f"'{diagram_name}'" if diagram_name else "unnamed diagram"
            logging.warning(f"Failed to render {diagram_desc} with Kroki: {e}")
            return f"```{diagram_type}\n{clean_source}\n```"


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

    def __hash__(self) -> int:
        return hash((self.base, self.derived, self.relationship_type))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ClassRelationship):
            return NotImplemented
        return (self.base, self.derived, self.relationship_type) == (other.base, other.derived, other.relationship_type)


class ClassDiagram(pydantic.BaseModel):
    relationships: set[ClassRelationship] = set({})

    def add_relationship(self, base: str, derived: str, relationship_type: str = "inheritance") -> None:
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
    output: str | None = None
    image_directory: str | None = None
    classes: set[ClassDefinitionName] = None
    image_dir: bool = False
    index_file: str = "index.md"
    noimages: bool = False
    noyuml: bool = False
    no_types_dir: bool = False
    warn_on_exist: bool = False
    gen_classes: set[ClassDefinitionName] | None = None
    gen_classes_neighborhood: References | None = None
    separate_erd_components: bool = True
    omit_standalone_classes: bool = False
    debug: bool = False
    kroki_server: str | None = None
    diagram_dir: str | None = None
    pretty_format_svg: bool = False
    _diagram_counter: int = 0

    schema_classes = set[ClassDefinition]

    def visit_schema(
        self,
        output: str | None = None,
        classes: set[ClassDefinitionName] | None = None,
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
        items.extend(self._generate_slot_sections())
        items.extend(self._generate_enum_sections())

        # Filter out None items and join
        items = [item for item in items if item is not None]
        output = "\n".join(items) + "\n"
        return pad_heading(output)

    def _initialize_generation(self, output: str, classes: set[ClassDefinitionName]) -> None:
        """Initialize generation parameters and validate inputs."""
        self.gen_classes = classes if classes else []
        for cls in self.gen_classes:
            if cls not in self.schema.classes:
                raise ValueError(f"Unknown class name: {cls}")

        if self.gen_classes:
            self.gen_classes_neighborhood = self.neighborhood(list(self.gen_classes))

        self.output = output
        self.schema_class_names = {c.name for c in self.schema.classes.values()}
        self._diagram_renderer = DiagramRenderer(
            kroki_server=self.kroki_server,
            diagram_dir=self.diagram_dir,
            pretty_format=self.pretty_format_svg,
        )

    def _generate_header(self) -> list[str]:
        """Generate the document header with metadata."""
        return [
            self.frontmatter(f"{self.schema.name.upper()}"),
            self.para(f"**metamodel version:** {self.schema.metamodel_version}\n\n**version:** {self.schema.version}"),
            self.para(be(self.schema.description)),
        ]

    def _generate_diagrams(self) -> list[str | None]:
        """Generate class and ERD diagrams."""
        items: list[str | None] = []

        # Class Diagram
        items.append(self.header(2, "Class Diagram"))
        items.append(self._diagram_renderer.render(str(self.full_class_diagram()), diagram_name="class_diagram"))

        # ERD Diagram(s)
        if self.separate_erd_components:
            items.extend(self._generate_component_erd_diagrams())
        else:
            # Original single ERD diagram
            erd_gen = ERDiagramGenerator(self.schema_location, exclude_abstract_classes=True, exclude_attributes=False)
            items.append(self.header(2, "ERD Diagram"))
            items.append(self._diagram_renderer.render(erd_gen.serialize(), diagram_name="erd_diagram"))

        return items

    def _generate_component_erd_diagrams(self) -> list[str | None]:
        """Generate separate ERD diagrams for each connected component."""
        items: list[str | None] = []

        connected_components, base_classes, truly_standalone_classes = self._detect_erd_connected_components()

        # Generate diagrams for connected components
        if connected_components:
            if len(connected_components) == 1:
                items.append(self.header(2, "ERD Diagram"))
            else:
                items.append(self.header(2, "ERD Diagrams"))

            for i, component in enumerate(connected_components, 1):
                # Sort component classes for consistent output
                sorted_classes = sorted(component)
                if len(connected_components) > 1:
                    component_name = (
                        f"Component {i} ({', '.join(sorted_classes[:3])}{'...' if len(sorted_classes) > 3 else ''})"
                    )
                    items.append(self.header(3, component_name))

                erd_gen = ERDiagramGenerator(
                    self.schema_location, exclude_abstract_classes=True, exclude_attributes=False
                )
                component_diagram = erd_gen.serialize_classes(list(component), follow_references=False, max_hops=0)

                # Use "erd_diagram" for single component (main ERD), otherwise use component-specific names
                if len(connected_components) == 1:
                    diagram_name = "erd_diagram"
                else:
                    diagram_name = f"erd_{sorted_classes[0].lower()}" if sorted_classes else f"erd_component_{i}"

                items.append(self._diagram_renderer.render(component_diagram, diagram_name=diagram_name))

        # Generate section for base classes (classes used as parents but have no direct relationships)
        if base_classes and not self.omit_standalone_classes:
            items.append(self.header(2, "Base Classes"))
            items.append(
                self.para("Foundational classes in the hierarchy (root classes and direct children of Thing):")
            )
            items.append(self._generate_classes_table(base_classes))

        # Generate section for truly standalone classes
        if truly_standalone_classes and not self.omit_standalone_classes:
            items.append(self.header(2, "Standalone Classes"))
            items.append(
                self.para(
                    "These classes are completely isolated with no relationships and are not used as base classes:"
                )
            )
            items.append(self._generate_classes_table(truly_standalone_classes))

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

    def _categorize_classes(self) -> tuple[list[ClassDefinition], list[ClassDefinition], list[ClassDefinition]]:
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

    def _generate_slot_sections(self) -> list[str]:
        """Generate documentation for all slots as a comprehensive table."""
        items = []

        # Sort slots with priority slots (id, name, description) first, then by rank, then alphabetically
        def slot_sort_key(slot):
            priority_slots = ["id", "name", "description"]

            # Primary sort by priority slots
            if slot.name in priority_slots:
                primary_sort = priority_slots.index(slot.name)
            else:
                primary_sort = len(priority_slots)

            # Secondary sort by rank (if exists)
            rank = getattr(slot, "rank", None)
            rank_value = rank if rank is not None else float("inf")

            # Tertiary sort alphabetically
            return (primary_sort, rank_value, slot.name)

        slots = sorted(self.schema.slots.values(), key=slot_sort_key)

        if slots:
            items.append(self.header(2, "Slots"))

            # Build table data
            table_data = []
            for slot in slots:
                # Get classes that use this slot
                classes_using_slot = []
                for cls in self.schema.classes.values():
                    all_class_slots = self._collect_all_class_slots(cls)
                    if any(s.name == slot.name for s in all_class_slots):
                        classes_using_slot.append(cls.name)

                # Format used by as comma-separated links
                used_by_links = ", ".join([self.class_link(cls_name) for cls_name in sorted(classes_using_slot)])
                if not used_by_links:
                    used_by_links = ""

                # Format slot name with anchor

                slot_name = slot.name

                # Create anchor for linking from class attribute tables
                def make_anchor(name: str) -> str:
                    if self.anchor_style == "mkdocs":
                        return name.lower()
                    else:
                        return camelcase(name)

                anchor = make_anchor(slot.name)
                # Add HTML anchor tag before the slot name, with description underneath (not bold)
                name_with_anchor = f'<a id="{anchor}"></a>**{slot_name}**'
                if slot.description:
                    desc = slot.description.strip()
                    # Add description on new line without bold
                    name_with_anchor += f"<br/>{desc}"

                # Get range/type
                range_display = self.class_type_link(slot.range) if slot.range else ""

                # Get cardinality
                cardinality = self.predicate_cardinality(slot)

                # Combine cardinality and range on separate lines
                type_info = f"{cardinality}<br/>{range_display}" if range_display else cardinality

                table_data.append({"Name": name_with_anchor, "Cardinality/Range": type_info, "Used By": used_by_links})

            # Create and add the table
            if table_data:
                table = MarkdownTable(table_data)
                items.append(table.get_markdown())

        return items

    def _generate_classes_table(self, class_names: set[str]) -> str:
        """Generate a markdown table of classes with their descriptions and links."""
        table_data = []

        # Sort class names alphabetically for consistent output
        for class_name in sorted(class_names):
            cls = self.schema.classes.get(class_name)
            if cls:
                # Create link to the class anchor
                class_link = self.class_link(cls, use_desc=False)
                description = cls.description if cls.description else ""
                # Clean up description - remove newlines and excessive whitespace
                description = " ".join(description.split()) if description else ""

                table_data.append({"Class": class_link, "Description": description})

        if table_data:
            table = MarkdownTable(table_data)
            return table.get_markdown()
        else:
            return ""

    def _detect_erd_connected_components(self) -> tuple[list[set[str]], set[str], set[str]]:
        """Detect connected components in ERD graph, returning (components, base_classes, standalone_classes)."""
        # Build adjacency list of class relationships
        adjacency = {}
        all_classes = set()

        # Get all concrete classes (non-abstract, non-mixin)
        for cls in self.schema.classes.values():
            if not cls.abstract and not cls.mixin:
                all_classes.add(cls.name)
                adjacency[cls.name] = set()

        # Add edges based on slot relationships
        for cls in self.schema.classes.values():
            if not cls.abstract and not cls.mixin:
                # Check all slots for this class
                for slot_name in cls.slots:
                    slot = self.schema.slots.get(slot_name)
                    if slot and slot.range in all_classes:
                        # Add bidirectional edge
                        adjacency[cls.name].add(slot.range)
                        adjacency[slot.range].add(cls.name)

                # Also check attributes (inline slots)
                if cls.attributes:
                    for attr_name, attr_def in cls.attributes.items():
                        if attr_def.range in all_classes:
                            adjacency[cls.name].add(attr_def.range)
                            adjacency[attr_def.range].add(cls.name)

        # Find connected components using DFS
        visited = set()
        components = []

        def dfs(node, component):
            if node in visited:
                return
            visited.add(node)
            component.add(node)
            for neighbor in adjacency.get(node, set()):
                dfs(neighbor, component)

        for cls_name in sorted(all_classes):
            if cls_name not in visited:
                component = set()
                dfs(cls_name, component)
                components.append(component)

        # Separate connected components from singleton components
        connected_components = []
        singleton_classes = set()

        for component in components:
            if len(component) == 1:
                singleton_classes.update(component)
            else:
                connected_components.append(component)

        # Sort connected components by their first class name (alphabetically) for deterministic ordering
        connected_components.sort(key=min)

        # Now classify singleton classes into base classes vs truly standalone
        base_classes = set()
        truly_standalone_classes = set()

        # Get all classes that are in connected components (have relationships)
        classes_with_relationships = set()
        for component in connected_components:
            classes_with_relationships.update(component)

        # Helper function to check if a class has children
        def has_children(class_name: str) -> bool:
            for cls in self.schema.classes.values():
                if cls.is_a == class_name:
                    return True
            return False

        # First, add base classes to the set (regardless of relationships):
        # 1. Thing itself
        # 2. Direct children of Thing (is_a == "Thing")
        # 3. Root classes with no parent (no is_a) that have children
        for cls_name, cls_def in self.schema.classes.items():
            if cls_name == "Thing":
                base_classes.add(cls_name)
            elif cls_def and cls_def.is_a == "Thing":
                base_classes.add(cls_name)
            elif cls_def and not cls_def.is_a:
                # Root classes with no parent - only include if they have children
                if has_children(cls_name):
                    base_classes.add(cls_name)

        # Now classify singleton classes
        for singleton_class in singleton_classes:
            # Skip if already in base classes
            if singleton_class in base_classes:
                continue

            # All other singleton classes are truly standalone
            truly_standalone_classes.add(singleton_class)

        return connected_components, base_classes, truly_standalone_classes

    def _class_descendants_have_relationships(self, class_name: str, classes_with_relationships: set[str]) -> bool:
        """Check if any descendants of a class have relationships (recursively)."""
        for cls in self.schema.classes.values():
            if not cls.abstract and not cls.mixin and cls.is_a == class_name:
                if cls.name in classes_with_relationships:
                    return True
                # Recursively check descendants
                if self._class_descendants_have_relationships(cls.name, classes_with_relationships):
                    return True
        return False

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

    def _add_ancestor_relationships(self, cls: ClassDefinition, diagram: ClassDiagram) -> None:
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
        items.append(self.element_header(enu, camelcase(enu.name), class_curi, class_uri))

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
            table = MarkdownTable(attributes)
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
        items.append(self.element_header(cls, camelcase(cls.name), class_curi, class_uri))

        # Add YAML definition if debug mode is enabled
        if self.debug:
            items.extend(self._generate_class_yaml_definition(cls))

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

    def _clean_extended_str(self, obj: Any) -> Any:
        """Recursively convert extended_str objects to plain strings."""

        if isinstance(obj, extended_str):
            # Convert extended_str to plain string
            return str(obj)
        elif isinstance(obj, dict):
            # Recursively clean dictionary values
            return {k: self._clean_extended_str(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            # Recursively clean list items
            return [self._clean_extended_str(item) for item in obj]
        else:
            # Return other types as-is
            return obj

    def _generate_class_yaml_definition(self, cls: ClassDefinition) -> list[str]:
        """Generate collapsible YAML definition of the class for debugging."""

        items = []

        # Create a simplified dict representation of the class
        class_dict = {}

        # Add key class properties
        if cls.is_a:
            class_dict["is_a"] = str(cls.is_a)
        if cls.mixins:
            class_dict["mixins"] = [str(m) for m in cls.mixins]
        if cls.abstract:
            class_dict["abstract"] = cls.abstract
        if cls.mixin:
            class_dict["mixin"] = cls.mixin
        if cls.description:
            class_dict["description"] = str(cls.description)
        if cls.slots:
            class_dict["slots"] = [str(s) for s in cls.slots]
        if cls.slot_usage:
            slot_usage_dict = {}
            for k, v in cls.slot_usage.items():
                slot_dict = {}
                if v.range:
                    slot_dict["range"] = str(v.range)
                if v.required is not None:
                    slot_dict["required"] = v.required
                if v.multivalued is not None:
                    slot_dict["multivalued"] = v.multivalued
                if v.description:
                    slot_dict["description"] = str(v.description)
                if slot_dict:
                    slot_usage_dict[str(k)] = slot_dict
            if slot_usage_dict:
                class_dict["slot_usage"] = slot_usage_dict
        if cls.attributes:
            attrs = {}
            for attr_name, attr_def in cls.attributes.items():
                attr_dict = {}
                if attr_def.range:
                    attr_dict["range"] = str(attr_def.range)
                if attr_def.required is not None:
                    attr_dict["required"] = attr_def.required
                if attr_def.multivalued is not None:
                    attr_dict["multivalued"] = attr_def.multivalued
                if attr_def.description:
                    attr_dict["description"] = str(attr_def.description)
                if attr_dict:
                    attrs[str(attr_name)] = attr_dict
            if attrs:
                class_dict["attributes"] = attrs

        # Clean extended_str objects before dumping to YAML
        clean_dict = self._clean_extended_str({str(cls.name): class_dict})

        # Add YAML section with collapsible details
        items.append(self.header(4, "YAML Definition"))
        items.append("<details>")
        items.append("<summary>Click to expand</summary>\n")
        items.append("```yaml")
        items.append(yaml.dump(clean_dict, default_flow_style=False, sort_keys=False))
        items.append("```")
        items.append("</details>\n")

        return items

    def _gather_class_relationships(self, cls: ClassDefinition) -> dict[str, Any]:
        """Gather all relationship information for a class."""
        class_refs = self.synopsis.classrefs.get(cls.name)

        # Check if there are actually any slots that reference this class
        has_references_to = False
        if class_refs is not None and class_refs.slotrefs:
            for slot_name in class_refs.slotrefs:
                slot = self.schema.slots[slot_name]
                if slot.range == cls.name:
                    has_references_to = True
                    break

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
        if class_refs is not None and class_refs.slotrefs:
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
            diagram_name = f"class_{cls.name.lower()}_erd"
            items.append(self._diagram_renderer.render(diagram, diagram_name=diagram_name))
        elif children or cls.is_a:
            items.append(self.header(4, "Local class diagram"))
            diagram_name = f"class_{cls.name.lower()}_local"
            items.append(self._diagram_renderer.render(str(self.local_class_diagram(cls)), diagram_name=diagram_name))

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

    def slots_table(self, cls: ClassDefinition) -> str | None:
        """Generate a markdown table of class attributes/slots including inherited ones."""
        all_slots = self._collect_all_class_slots(cls)
        if not all_slots:
            return None

        attributes = []

        for slot in all_slots:
            # Determine slot source for styling
            source_info = self._get_slot_source(slot, cls)

            # Create link to slot in comprehensive slots table
            slot_link_text = self.slot_link(slot, add_subset=False)

            # Add source styling (inherited, from mixin, etc.)
            if source_info["source"] == "parent":
                name_display = f"*{slot_link_text}*"
            elif source_info["source"] == "mixin":
                name_display = f"_{slot_link_text}_"
            else:
                name_display = f"**{slot_link_text}**"

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

        return MarkdownTable(attributes).get_markdown()

    def _collect_all_class_slots(self, cls: ClassDefinition) -> list[SlotDefinition]:
        """Collect all slots for a class using SchemaView, handling inheritance and slot_usage."""
        # Use SchemaView to get the canonical set of induced slots for this class
        # This automatically handles inheritance, mixins, and deduplication

        if not hasattr(self, "_schema_view"):
            self._schema_view = SchemaView(self.schema_location)

        # Track which slots we've already processed to avoid duplicates
        processed_slots = {}  # slot_name -> SlotDefinition

        # First, process regular induced slots
        induced_slots = self._schema_view.class_induced_slots(cls.name)
        for slot in induced_slots:
            processed_slots[slot.name] = slot

        # Also process slots defined in slot_usage (which may not appear in induced_slots)
        # This includes slot_usage from the current class and all ancestors
        slot_usage_to_check = set()

        # Collect slot_usage from current class
        if cls.slot_usage:
            slot_usage_to_check.update(cls.slot_usage.keys())

        # Collect slot_usage from all ancestor classes
        if cls.is_a:
            current = cls.is_a
            while current:
                parent_cls = self.schema.classes.get(current)
                if parent_cls:
                    if parent_cls.slot_usage:
                        slot_usage_to_check.update(parent_cls.slot_usage.keys())
                    current = parent_cls.is_a
                else:
                    break

        # Process all slot_usage entries
        for slot_name in slot_usage_to_check:
            if slot_name not in processed_slots:
                # Get the induced slot to get the properly overridden properties
                try:
                    slot = self._schema_view.induced_slot(slot_name, cls.name)
                    processed_slots[slot_name] = slot
                except Exception:
                    # Slot might not exist, skip it
                    pass

        return list(processed_slots.values())

    def _get_slot_source(self, slot: SlotDefinition, cls: ClassDefinition) -> dict[str, Any]:
        """Determine slot source: own, mixin, or inherited."""
        if not hasattr(self, "_schema_view"):
            self._schema_view = SchemaView(self.schema_location)

        # Use SchemaView to determine slot ownership
        slot_definition = self._schema_view.induced_slot(slot.name, cls.name)

        # Check if it's directly defined in this class
        # A slot is "own" if this class is in its domain_of
        if cls.name in slot_definition.domain_of:
            return {"type": "own", "source": cls.name}

        # Check if it's a direct attribute of this class
        if cls.attributes and slot.name in cls.attributes:
            return {"type": "own", "source": cls.name}

        # Check if it's in this class's slot_usage (which means it's customized for this class)
        if cls.slot_usage and slot.name in cls.slot_usage:
            return {"type": "own", "source": cls.name}

        # Use SchemaView to get all ancestors (mixins + inheritance chain)
        ancestors = []

        # Add mixins first
        if cls.mixins:
            ancestors.extend(cls.mixins)

        # Add inheritance chain
        if cls.is_a:
            inheritance_chain = []
            current = cls.is_a
            while current:
                inheritance_chain.append(current)
                parent_cls = self.schema.classes.get(current)
                current = parent_cls.is_a if parent_cls else None
            ancestors.extend(inheritance_chain)

        # Check each ancestor to find the source
        for ancestor_name in ancestors:
            ancestor_cls = self.schema.classes.get(ancestor_name)
            if ancestor_cls:
                # Check if slot is defined in this ancestor
                if ancestor_name in slot_definition.domain_of:
                    # Determine if this ancestor is a mixin or inheritance
                    if ancestor_name in (cls.mixins or []):
                        return {"type": "mixin", "source": ancestor_name}
                    else:
                        return {"type": "inherited", "source": ancestor_name}

                # Check if it's a direct attribute of this ancestor
                if ancestor_cls.attributes and slot.name in ancestor_cls.attributes:
                    if ancestor_name in (cls.mixins or []):
                        return {"type": "mixin", "source": ancestor_name}
                    else:
                        return {"type": "inherited", "source": ancestor_name}

                # Check if it's in this ancestor's slot_usage
                if ancestor_cls.slot_usage and slot.name in ancestor_cls.slot_usage:
                    if ancestor_name in (cls.mixins or []):
                        return {"type": "mixin", "source": ancestor_name}
                    else:
                        return {"type": "inherited", "source": ancestor_name}

        return {"type": "unknown", "source": "unknown"}

    def _create_slot_sort_key(self, cls: ClassDefinition) -> Callable[[dict], tuple]:
        """Create sort key for slots: priority (id/name/description), then source, rank, alphabetical."""
        priority_slots = ["id", "name", "description"]

        def sort_key(attr):
            slot_name = attr["_slot_name"]
            slot = next((s for s in self._collect_all_class_slots(cls) if s.name == slot_name), None)

            if not slot:
                return (99, 0, float("inf"), slot_name)  # Unknown slots go last

            # Primary sort by priority slots (id, name, description first)
            if slot_name in priority_slots:
                primary_sort = priority_slots.index(slot_name)
            else:
                primary_sort = len(priority_slots)  # Non-priority slots come after

            source_info = self._get_slot_source(slot, cls)
            source_type = source_info["type"]

            # Secondary sort by source type: inherited (parents) -> mixins -> own
            if source_type == "inherited":
                secondary_sort = 0
            elif source_type == "mixin":
                secondary_sort = 1
            elif source_type == "own":
                secondary_sort = 2
            else:
                secondary_sort = 3  # unknown

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
                    # Strip class name prefix from slot name for cleaner display
                    # e.g., "Enumeration_default" -> "default"
                    slot_display_name = slot.name
                    if "_" in slot.name:
                        # Check if it starts with the domain class name
                        prefix = domain + "_"
                        if slot.name.startswith(prefix):
                            slot_display_name = slot.name[len(prefix) :]

                    items.append(
                        self.bullet(
                            f" **{self.class_link(domain)}** : {slot_display_name}{self.predicate_cardinality(slot)} "
                        )
                    )

    def visit_subset(self, subset: SubsetDefinition) -> str | None:
        # TODO: Implement subset documentation generation
        return None

    def element_header(self, obj: Element, name: str, curie: str, uri: str) -> str:
        header_label = f"~~{name}~~ _(deprecated)_" if obj.deprecated else f"{name}"
        out = self.header(3, header_label)

        out += self.para(be(obj.description))

        # Also include comments if present
        if hasattr(obj, "comments") and obj.comments:
            for comment in obj.comments:
                # Remove ^^rdf:HTML and similar type annotations
                comment_text = re.sub(r"\^\^[\w:]+$", "", comment).strip()
                out += self.para(be(comment_text))

        # out = "\n".join([out, f"URI: [{curie}]({uri})", ""])
        return out

    def is_secondary_ref(self, en: str) -> bool:
        """Check if element is in the neighborhood of requested classes."""
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
    def anchor(id_: str) -> str:
        return f'<a name="{id_}">'

    @staticmethod
    def anchorend() -> str:
        return "</a>"

    def header(self, level: int, txt: str) -> str:
        txt = self.get_metamodel_slot_name(txt)
        return f"\n{'#' * level} {txt}\n"

    @staticmethod
    def para(txt: str) -> str:
        return f"\n{txt}\n"

    @staticmethod
    def bullet(txt: str, level: int = 0) -> str:
        return f"{'    ' * level} * {txt}"

    def frontmatter(self, thingtype: str, layout: str = "default") -> str:
        return self.header(1, thingtype)
        # print(f'---\nlayout: {layout}\n---\n')

    def bbin(self, obj: Element) -> str:
        """Boldify built-in types."""
        return obj.name if isinstance(obj, Element) else f"**{obj}**" if obj in self.synopsis.typebases else obj

    def desc_for(self, obj: Element, doing_descs: bool) -> str:
        """Return description if unique (different from parent), empty string otherwise."""
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
        obj: Element | None,
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        """Create a markdown link to the element."""

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
        elif isinstance(obj, SlotDefinition):
            link_name = obj.name
            link_ref = make_anchor(obj.name)
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
        ref: str | TypeDefinition | None,
        *,
        after_link: str = None,
        use_desc: bool = False,
        add_subset: bool = True,
    ) -> str:
        return ref

    def slot_link(
        self,
        ref: str | SlotDefinition | None,
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
        ref: str | ClassDefinition | None,
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
        ref: str | ClassDefinition | TypeDefinition | EnumDefinition | None,
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
        ref: str | EnumDefinition | None,
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
        ref: str | SubsetDefinition | None,
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
@click.option(
    "--separate-erd-components/--single-erd",
    default=True,
    help="Generate separate ERD diagrams for each connected component (default: True)",
)
@click.option(
    "--omit-standalone-classes",
    is_flag=True,
    default=False,
    help="Omit standalone classes (classes with no relationships) from ERD diagrams",
)
@click.option(
    "--debug",
    is_flag=True,
    default=False,
    help="Include YAML class definitions in the output for debugging",
)
@click.option(
    "--kroki-server",
    type=str,
    default=None,
    help="URL of Kroki server to render diagrams as SVG (e.g., http://localhost:8000)",
)
@click.option(
    "--diagram-dir",
    type=str,
    default=None,
    help="Directory to save diagram files (requires --kroki-server). "
    "Diagrams will be saved as SVG files and referenced in markdown.",
)
@click.option(
    "--pretty-format-svg",
    is_flag=True,
    default=False,
    help="Pretty-format SVG files with proper HTML-style indentation (2 spaces). "
    "Makes SVGs more readable but increases file size.",
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, **kwargs):
    """Generate markdown documentation of a LinkML model"""
    gen = MarkdownDataDictGen(yamlfile, **kwargs)
    print(gen.serialize(**kwargs))


if __name__ == "__main__":
    cli()
