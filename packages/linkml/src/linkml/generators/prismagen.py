"""
Generate Prisma schemas from LinkML schemas.

This generator transforms LinkML schemas into Prisma schema files (.prisma).
It uses the RelationalModelTransformer to normalize relationships and
handle foreign keys, then renders the result using a Jinja2 template.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from typing import Any, Optional

import click
from jinja2 import Template
from linkml_runtime import SchemaView
from linkml_runtime.linkml_model.meta import (
    ClassDefinition,
    EnumDefinition,
    PermissibleValue,
    SchemaDefinition,
    SlotDefinition,
)

from linkml._version import __version__
from linkml.generators.prisma.prisma_template import prisma_template_str
from linkml.generators.prisma.type_mappings import PRISMA_RANGEMAP, get_prisma_type, is_optional_field
from linkml.transformers.relmodel_transformer import ForeignKeyPolicy, RelationalModelTransformer
from linkml.utils.generator import Generator, shared_arguments

logger = logging.getLogger(__name__)


def to_camel_case(snake_str: str) -> str:
    """
    Convert snake_case to camelCase.

    Args:
        snake_str: String in snake_case format

    Returns:
        String in camelCase format
    """
    parts = snake_str.split('_')
    if not parts:
        return snake_str
    return parts[0].lower() + ''.join(p.capitalize() for p in parts[1:])


def pluralize(word: str) -> str:
    """
    Simple pluralization for generating reverse relation names.

    Args:
        word: Singular noun

    Returns:
        Plural form (simple heuristic)
    """
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith('s') or word.endswith('x') or word.endswith('ch') or word.endswith('sh'):
        return word + 'es'
    else:
        return word + 's'


def find_identifier_slot(cls: ClassDefinition) -> tuple[str, str]:
    """
    Find the identifier slot for a class.

    Args:
        cls: Class definition

    Returns:
        Tuple of (slot_name, prisma_type) for the identifier slot.
        Returns ('id', 'Int') as fallback if no identifier found.
    """
    for slot_name, slot in cls.attributes.items():
        if slot.identifier:
            # Determine the Prisma type
            slot_range = slot.range or 'string'
            prisma_type = PRISMA_RANGEMAP.get(slot_range, 'String')
            return (slot_name, prisma_type)
    return ('id', 'Int')


@dataclass
class PrismaFieldInfo:
    """Information about a Prisma field."""

    name: str
    """Field name"""

    prisma_type: str
    """Prisma type (e.g., String, Int, Person)"""

    modifiers: str = ""
    """Field modifiers (e.g., @id, @unique, @default(...))"""

    is_optional: bool = False
    """Whether the field is optional (adds ? in Prisma)"""

    is_relation: bool = False
    """Whether this field represents a relation to another model"""

    relation_fields: bool = False
    """Whether this relation requires FK fields"""

    fk_field_name: str = ""
    """Foreign key field name if this is a relation"""

    fk_type: str = ""
    """Foreign key field type"""

    linkml_metadata: str = ""
    """LinkML metadata preserved as comment"""


@dataclass
class UniqueConstraint:
    """Information about a unique constraint."""

    fields: str
    """Comma-separated field names"""

    name: str = ""
    """Constraint name"""


@dataclass
class PrismaModelInfo:
    """Information about a Prisma model."""

    name: str
    """Model name"""

    fields: list[PrismaFieldInfo]
    """Model fields"""

    description: str = ""
    """Model description"""

    is_a: str = ""
    """Parent class (for metadata preservation)"""

    mixins: str = ""
    """Mixins (for metadata preservation)"""

    abstract: bool = False
    """Whether this is an abstract class"""

    is_join_table: bool = False
    """Whether this is a join table"""

    composite_key: str = ""
    """Composite primary key fields"""

    unique_constraints: list[UniqueConstraint] = field(default_factory=list)
    """Unique constraints"""


@dataclass
class PrismaEnumValue:
    """Information about a Prisma enum value."""

    name: str
    """Value name"""

    description: str = ""
    """Value description"""


@dataclass
class PrismaEnumInfo:
    """Information about a Prisma enum."""

    name: str
    """Enum name"""

    values: list[PrismaEnumValue]
    """Enum values"""


def is_join_table(cls: ClassDefinition) -> bool:
    """
    Determine if a class is a join table created by the transformer.

    Args:
        cls: Class definition

    Returns:
        True if this is a join table
    """
    return "linkml:derived_from" in cls.annotations


def is_scalar_join_table(cls: ClassDefinition, all_classes: dict[str, ClassDefinition]) -> bool:
    """
    Determine if a class is a join table for a scalar array (not a relation).

    A scalar join table is one where the non-FK slot has a scalar range
    (string, integer, etc.) rather than a reference to another class.

    Args:
        cls: Class definition
        all_classes: All classes in the schema (to check if range is a class)

    Returns:
        True if this is a join table for scalar values
    """
    if not is_join_table(cls):
        return False

    # Check if any slot has a scalar (non-class) range
    for slot_name, slot in cls.attributes.items():
        # Skip the FK slot (which references a class)
        if slot.range in all_classes:
            continue
        # If we find a slot with a non-class range, it's a scalar join table
        return True

    return False


def is_value_object(cls: ClassDefinition) -> bool:
    """
    Determine if a class is a value object that should be flattened.

    Value objects are classes without an identifier that are typically
    embedded in other classes (e.g., QuantityValue with numeric_value and unit).

    Args:
        cls: Class definition

    Returns:
        True if this is a value object (no identifier)
    """
    for slot_name, slot in cls.attributes.items():
        if slot.identifier:
            return False
    return True


def get_value_object_fields(schemaview: SchemaView, cls_name: str) -> list[tuple[str, str]]:
    """
    Get the fields of a value object class from the ORIGINAL schema.

    Args:
        schemaview: SchemaView for the original (non-transformed) schema
        cls_name: Name of the value object class

    Returns:
        List of (field_name, range) tuples
    """
    fields = []
    for slot in schemaview.class_induced_slots(cls_name):
        # Skip identifier slots (shouldn't exist for value objects, but be safe)
        if slot.identifier:
            continue
        fields.append((slot.name, slot.range or "string"))
    return fields


def get_scalar_array_info(cls: ClassDefinition, all_classes: dict[str, ClassDefinition]) -> tuple[str, str, str] | None:
    """
    Extract scalar array information from a join table class.

    Returns:
        Tuple of (parent_class_name, field_name, scalar_type) or None if not a scalar join table
    """
    if not is_join_table(cls):
        return None

    parent_class = None
    scalar_field_name = None
    scalar_type = None

    for slot_name, slot in cls.attributes.items():
        if slot.range in all_classes:
            # This is the FK to the parent class
            parent_class = slot.range
        else:
            # This is the scalar value field
            scalar_field_name = slot_name
            scalar_type = slot.range

    if parent_class and scalar_field_name and scalar_type:
        return (parent_class, scalar_field_name, scalar_type)
    return None


def prepare_prisma_models(
    tr_schema: SchemaDefinition,
    schemaview: SchemaView,
    use_scalar_arrays: bool = True,
    skip_abstract: bool = True,
    empty_enums: set[str] | None = None,
    flatten_value_objects: bool = True,
) -> list[PrismaModelInfo]:
    """
    Convert a transformed LinkML schema to Prisma model data structures.

    This function is the core transformation logic, separate from template
    rendering for easier testing.

    Args:
        tr_schema: Transformed schema from RelationalModelTransformer
        schemaview: SchemaView for querying schema information
        use_scalar_arrays: Whether to use scalar arrays for multivalued slots
        skip_abstract: Whether to skip abstract classes (default True)
        empty_enums: Set of enum names that have no values (will be rendered as String)
        flatten_value_objects: Whether to flatten value objects (classes without identifiers)
            into parent models instead of creating separate tables (default True)

    Returns:
        List of PrismaModelInfo objects ready for template rendering
    """
    models = []
    models_by_name: dict[str, PrismaModelInfo] = {}
    empty_enums = empty_enums or set()

    # Identify value object classes (no identifier) that should be flattened
    # Important: Check against ORIGINAL schema (schemaview), not transformed schema,
    # because the transformer adds auto-generated IDs to classes without identifiers
    value_object_classes: set[str] = set()
    if flatten_value_objects:
        for cls_name in schemaview.all_classes():
            original_cls = schemaview.get_class(cls_name)
            # Check if the original class has an identifier slot
            id_slot = schemaview.get_identifier_slot(cls_name)
            if id_slot is None and cls_name in tr_schema.classes:
                # Also ensure it's not abstract or a mixin
                if not original_cls.abstract and not original_cls.mixin:
                    value_object_classes.add(cls_name)
                    logger.debug(f"Identified '{cls_name}' as a value object (will be flattened)")

    # Track forward relations for generating reverse relations later
    # Each entry: (source_class, source_field_name, target_class, is_optional)
    forward_relations: list[tuple[str, str, str, bool]] = []

    # When using scalar arrays, collect info from join tables to restore as array fields
    # Dict: parent_class -> list of (field_name, scalar_type)
    scalar_arrays_to_restore: dict[str, list[tuple[str, str]]] = {}
    if use_scalar_arrays:
        for cls_name, cls in tr_schema.classes.items():
            info = get_scalar_array_info(cls, tr_schema.classes)
            if info:
                parent_class, field_name, scalar_type = info
                if parent_class not in scalar_arrays_to_restore:
                    scalar_arrays_to_restore[parent_class] = []
                scalar_arrays_to_restore[parent_class].append((field_name, scalar_type))
                logger.debug(f"Will restore scalar array '{field_name}' ({scalar_type}[]) to '{parent_class}'")

    for cls_name, cls in tr_schema.classes.items():
        # Skip abstract classes if configured
        if skip_abstract and (cls.abstract or False):
            continue

        # Skip scalar join tables when using scalar arrays
        # (these are replaced by native String[], Int[], etc.)
        if use_scalar_arrays and is_scalar_join_table(cls, tr_schema.classes):
            logger.debug(f"Skipping scalar join table '{cls_name}' (using scalar arrays instead)")
            continue

        # Skip value object classes (they are flattened into parent models)
        if cls_name in value_object_classes:
            logger.debug(f"Skipping value object class '{cls_name}' (will be flattened into parent)")
            continue

        fields = []

        # Get identifier field if any
        identifier_slot = None
        for slot_name in cls.attributes:
            slot = cls.attributes[slot_name]
            if slot.identifier:
                identifier_slot = slot_name
                break

        # Process each slot/attribute
        for slot_name, slot in cls.attributes.items():
            # Determine if this is a relation (range is a class)
            target_class_name = slot.range
            is_relation = target_class_name in tr_schema.classes

            # Check if range is an empty enum (fall back to String)
            if target_class_name in empty_enums:
                slot.range = "string"  # Override range to string for empty enums

            # Determine if field is optional
            is_optional = is_optional_field(slot, slot.required)

            # Handle value object flattening: instead of creating a relation,
            # inline the value object's fields with the slot name as prefix
            if target_class_name in value_object_classes:
                # Get fields from ORIGINAL schema (not transformed) to avoid auto-generated id
                vo_fields = get_value_object_fields(schemaview, target_class_name)
                # Use the original slot name for prefix (strip _id suffix if transformer added it)
                base_name = slot_name.removesuffix("_id")
                for vo_field_name, vo_field_range in vo_fields:
                    # Create prefixed field name (e.g., prevalenceNumericValue, prevalenceUnit)
                    camel_vo_name = to_camel_case(vo_field_name)
                    prefixed_name = to_camel_case(base_name) + camel_vo_name[0].upper() + camel_vo_name[1:]
                    vo_prisma_type = get_prisma_type(vo_field_range, is_multivalued=False, use_scalar_arrays=False)
                    flattened_field = PrismaFieldInfo(
                        name=prefixed_name,
                        prisma_type=vo_prisma_type,
                        modifiers="",
                        is_optional=True,  # Flattened fields are typically optional
                        is_relation=False,
                        linkml_metadata=f"from {target_class_name}.{vo_field_name}",
                    )
                    fields.append(flattened_field)
                continue  # Skip normal slot processing for value objects

            # Get Prisma type
            prisma_type = get_prisma_type(
                slot.range,
                is_multivalued=slot.multivalued,
                use_scalar_arrays=use_scalar_arrays and not is_relation,
            )

            # Convert field name to camelCase
            field_name = to_camel_case(slot_name)

            # Generate modifiers
            modifiers = []
            is_primary_key = slot.identifier or slot_name == identifier_slot
            if is_primary_key:
                modifiers.append("@id")
                # Integer identifiers get autoincrement by default
                if slot.range == "integer":
                    modifiers.append("@default(autoincrement())")

            # Check for unique constraint (identifier but not primary)
            if slot.identifier and slot_name != identifier_slot:
                modifiers.append("@unique")

            # Handle relations with proper FK fields
            fk_field_name = ""
            fk_type = ""
            if is_relation:
                target_class = tr_schema.classes[target_class_name]
                target_pk_name, target_pk_type = find_identifier_slot(target_class)

                # Convert target PK name to camelCase to match generated field names
                target_pk_camel = to_camel_case(target_pk_name)

                # Generate FK field name in camelCase (e.g., studyId)
                fk_field_name = f"{to_camel_case(slot_name)}Id"
                fk_type = target_pk_type

                # Check for inlined/owned relationship for cascade
                is_inlined = slot.inlined or slot.inlined_as_list or False
                on_delete = "Cascade" if is_inlined else "SetNull"

                # Build the @relation directive with correct FK field and target PK (both in camelCase)
                relation_directive = f'@relation(fields: [{fk_field_name}], references: [{target_pk_camel}], onDelete: {on_delete})'
                modifiers.append(relation_directive)

                # Track this forward relation for generating reverse relation
                forward_relations.append((cls_name, field_name, target_class_name, is_optional))

                # First, add the FK field (must be declared before relation)
                # Note: Don't add @unique - that would make it one-to-one instead of one-to-many
                fk_field_info = PrismaFieldInfo(
                    name=fk_field_name,
                    prisma_type=fk_type,
                    modifiers="",
                    is_optional=is_optional,
                    is_relation=False,
                    linkml_metadata="",
                )
                fields.append(fk_field_info)

            modifier_str = " ".join(modifiers)

            # Create field info for the main field
            field_info = PrismaFieldInfo(
                name=field_name,
                prisma_type=prisma_type if not is_relation else target_class_name,
                modifiers=modifier_str,
                is_optional=is_optional if not is_relation else True,  # Relation objects are optional in Prisma
                is_relation=is_relation,
                fk_field_name=fk_field_name,
                fk_type=fk_type,
                linkml_metadata="",
            )

            fields.append(field_info)

        # Get class metadata
        description = cls.description or ""
        is_a = cls.is_a or ""
        mixins_list = cls.mixins or []
        mixins = str(mixins_list) if mixins_list else ""
        abstract = cls.abstract or False

        # Create model info
        model_info = PrismaModelInfo(
            name=cls_name,
            fields=fields,
            description=description,
            is_a=is_a,
            mixins=mixins,
            abstract=abstract,
            is_join_table=is_join_table(cls),
        )

        models.append(model_info)
        models_by_name[cls_name] = model_info

    # Add reverse relations to target models
    for source_class, source_field, target_class, is_optional in forward_relations:
        if target_class in models_by_name:
            target_model = models_by_name[target_class]
            # Generate reverse relation name (e.g., "experiments" for source_class="Experiment")
            reverse_name = to_camel_case(pluralize(source_class))

            # Check if reverse relation already exists
            existing_names = {f.name for f in target_model.fields}
            if reverse_name not in existing_names:
                reverse_field = PrismaFieldInfo(
                    name=reverse_name,
                    prisma_type=f"{source_class}[]",
                    modifiers="",
                    is_optional=False,  # Arrays don't use ? in Prisma
                    is_relation=True,
                    linkml_metadata="reverse relation",
                )
                target_model.fields.append(reverse_field)

    # Restore scalar array fields to parent models (from skipped join tables)
    for parent_class, scalar_arrays in scalar_arrays_to_restore.items():
        if parent_class in models_by_name:
            parent_model = models_by_name[parent_class]
            existing_names = {f.name for f in parent_model.fields}
            for field_name, scalar_type in scalar_arrays:
                camel_name = to_camel_case(field_name)
                if camel_name not in existing_names:
                    prisma_type = get_prisma_type(scalar_type, is_multivalued=True, use_scalar_arrays=True)
                    array_field = PrismaFieldInfo(
                        name=camel_name,
                        prisma_type=prisma_type,
                        modifiers="",
                        is_optional=True,  # Arrays are optional by default
                        is_relation=False,
                        linkml_metadata="",
                    )
                    parent_model.fields.append(array_field)
                    logger.debug(f"Restored scalar array field '{camel_name}' to model '{parent_class}'")

    return models


def prepare_prisma_enums(schema: SchemaDefinition) -> tuple[list[PrismaEnumInfo], set[str]]:
    """
    Convert LinkML enums to Prisma enum data structures.

    Args:
        schema: LinkML schema

    Returns:
        Tuple of (list of PrismaEnumInfo objects, set of empty enum names).
        Empty enums are excluded from the list but their names are tracked
        so fields referencing them can fall back to String type.
    """
    enums = []
    empty_enums: set[str] = set()

    for enum_name, enum_def in schema.enums.items():
        values = []

        for pv_text, pv in enum_def.permissible_values.items():
            if isinstance(pv, PermissibleValue):
                value_name = pv_text
                value_desc = pv.description or ""
            else:
                value_name = pv_text
                value_desc = ""

            values.append(PrismaEnumValue(name=value_name, description=value_desc))

        if values:
            enums.append(PrismaEnumInfo(name=enum_name, values=values))
        else:
            # Track empty enums - fields referencing these will use String type
            empty_enums.add(enum_name)
            logger.warning(
                f"Enum '{enum_name}' has no permissible values (may be an ontology-based enum). "
                f"Fields referencing this enum will use String type instead."
            )

    return enums, empty_enums


@dataclass
class PrismaGenerator(Generator):
    """
    Generates Prisma schema files from LinkML schemas.

    The generator uses the RelationalModelTransformer to normalize the schema
    (handling relationships, foreign keys, join tables), then renders a Prisma
    schema using a Jinja2 template.

    Example:
        >>> from linkml.generators.prismagen import PrismaGenerator
        >>> gen = PrismaGenerator("my_schema.yaml")
        >>> prisma_schema = gen.serialize()
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["prisma"]
    file_extension = "prisma"
    uses_schemaloader = False

    # ObjectVars
    datasource_provider: str = "postgresql"
    """Database provider (postgresql, mysql, sqlite, cockroachdb)"""

    use_scalar_arrays: bool = True
    """Whether to use scalar arrays for multivalued slots (PostgreSQL/CockroachDB only)"""

    foreign_key_policy: Optional[ForeignKeyPolicy] = None
    """Foreign key policy for transformer"""

    def __post_init__(self) -> None:
        """Initialize schema view and transformer."""
        self.schemaview = SchemaView(self.schema)
        self.transformer = RelationalModelTransformer(self.schemaview)

        # Set foreign key policy if provided
        if self.foreign_key_policy:
            self.transformer.foreign_key_policy = self.foreign_key_policy
        else:
            # Default policy for Prisma
            self.transformer.foreign_key_policy = ForeignKeyPolicy.INJECT_FK_FOR_NESTED

        # Check scalar array support for the provider
        if self.use_scalar_arrays and self.datasource_provider in ("mysql", "sqlite"):
            logger.warning(
                f"Scalar arrays not supported by {self.datasource_provider}. "
                f"Use --no-use-scalar-arrays to suppress this warning."
            )

        super().__post_init__()

    def serialize(self, **kwargs: Any) -> str:
        """
        Generate Prisma schema string.

        Args:
            **kwargs: Additional arguments passed to transformer

        Returns:
            Prisma schema as a string
        """
        # Transform schema using relational model transformer
        # Filter out generator-specific kwargs that the transformer doesn't need
        excluded_kwargs = {"format", "metadata", "useuris", "importmap", "log_level", "mergeimports", "stacktrace", "verbose"}
        transformer_kwargs = {k: v for k, v in kwargs.items() if k not in excluded_kwargs}
        logger.info("Transforming schema with RelationalModelTransformer")
        tr_result = self.transformer.transform(**transformer_kwargs)
        tr_schema = tr_result.schema

        # Prepare enums first (to identify empty enums)
        logger.info(f"Preparing {len(tr_schema.enums)} enums")
        enums, empty_enums = prepare_prisma_enums(tr_schema)
        if empty_enums:
            logger.info(f"Found {len(empty_enums)} empty enums (will use String type): {empty_enums}")

        # Prepare models
        logger.info(f"Preparing {len(tr_schema.classes)} models")
        models = prepare_prisma_models(
            tr_schema,
            self.schemaview,
            use_scalar_arrays=self.use_scalar_arrays,
            empty_enums=empty_enums,
        )

        # Render template
        logger.info("Rendering Prisma schema")
        template = Template(prisma_template_str)
        output = template.render(
            schema_name=self.schemaview.schema.name,
            schema_id=self.schemaview.schema.id,
            schema_description=self.schemaview.schema.description,
            datasource_provider=self.datasource_provider,
            models=models,
            enums=enums,
        )

        logger.debug(f"Generated Prisma schema:\n{output}")
        return output


@shared_arguments(PrismaGenerator)
@click.command(name="prisma")
@click.version_option(__version__, "-V", "--version")
@click.option(
    "--datasource-provider",
    default="postgresql",
    type=click.Choice(["postgresql", "mysql", "sqlite", "cockroachdb"]),
    help="Database provider",
)
@click.option(
    "--use-scalar-arrays/--no-use-scalar-arrays",
    default=True,
    help="Use scalar arrays for multivalued slots (PostgreSQL/CockroachDB only)",
)
def cli(yamlfile: str, datasource_provider: str = "postgresql", use_scalar_arrays: bool = True, **args: Any) -> None:
    """Generate Prisma schema from LinkML model."""
    gen = PrismaGenerator(
        yamlfile,
        datasource_provider=datasource_provider,
        use_scalar_arrays=use_scalar_arrays,
        **args,
    )
    print(gen.serialize(**args))


if __name__ == "__main__":
    cli()
