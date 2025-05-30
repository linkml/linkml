import os
import re
from abc import ABC
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

import click
from jinja2 import Template
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView
from pydantic import BaseModel, model_validator

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments


class KuzuFieldTypeEnum(Enum):
    STRING = "STRING"
    INT64 = "INT64"
    FLOAT = "FLOAT"
    BOOL = "BOOLEAN"
    TIMESTAMP = "TIMESTAMP"
    DATE = "DATE"
    TIME = "TIME"


class KuzuField(BaseModel):
    name: str
    type: KuzuFieldTypeEnum

    class Config:
        schema_extra = {"required": ["name", "type"]}

    @model_validator(mode="before")
    def check_field_name_is_valid(self):
        name = self.get("name")
        if not name.isidentifier():
            raise ValueError(f"Field name {name} is not a valid identifier")
        return self


class KuzuTable(BaseModel, ABC):
    name: str
    fields: list[KuzuField]

    class Config:
        schema_extra = {"required": ["name", "fields"]}

    @model_validator(mode="before")
    def check_class_name_is_valid(self):
        name = self.get("name")
        if not name.isidentifier():
            raise ValueError(f"Table name {name} is not a valid identifier")
        return self


class KuzuNodeTable(KuzuTable):
    primary_key: str

    class Config:
        schema_extra = {"required": ["name", "fields", "primary_key"]}
    
    def get_schema_fields(self):
        """Return all fields for schema generation"""
        return self.fields


class KuzuRelationship(BaseModel):
    from_table: str
    to_table: str
    
    class Config:
        schema_extra = {"required": ["from_table", "to_table"]}


class KuzuRelTable(KuzuTable):
    relationships: list[KuzuRelationship]
    
    class Config:
        schema_extra = {"required": ["name", "fields", "relationships"]}
    
    def get_schema_fields(self):
        """Return all fields for schema generation"""
        return self.fields


template = Template(
    """
{% for table in tables %}
{% if table.__class__.__name__ == 'KuzuNodeTable' %}
CREATE NODE TABLE {{ table.name }} (
    {%- for field in table.get_schema_fields() %}
    {{ field.name }} {{ field.type.value }},
    {%- endfor %}
    PRIMARY KEY ({{ table.primary_key }})
);
{% else %}
CREATE REL TABLE {{ table.name }} (
    {%- for field in table.get_schema_fields() %}
    {{ field.name }} {{ field.type.value }}{% if not loop.last or table.relationships %},{% endif %}
    {%- endfor %}
    {%- for rel in table.relationships %}
    FROM {{ rel.from_table }} TO {{ rel.to_table }}{% if not loop.last %},{% endif %}
    {%- endfor %}
);
{% endif %}
{% endfor %}
"""
)


person_table = KuzuNodeTable(
    name="Person",
    fields=[
        KuzuField(name="name", type=KuzuFieldTypeEnum.STRING),
        KuzuField(name="age", type=KuzuFieldTypeEnum.INT64),
    ],
    primary_key="name",
)

city_table = KuzuNodeTable(
    name="City",
    fields=[
        KuzuField(name="name", type=KuzuFieldTypeEnum.STRING),
        KuzuField(name="population", type=KuzuFieldTypeEnum.INT64),
    ],
    primary_key="name",
)

knows_table = KuzuRelTable(
    name="Knows",
    fields=[
        KuzuField(name="since", type=KuzuFieldTypeEnum.DATE),
        KuzuField(name="strength", type=KuzuFieldTypeEnum.INT64),
    ],
    relationships=[
        KuzuRelationship(from_table="Person", to_table="Person"),
    ],
)

lives_in_table = KuzuRelTable(
    name="LivesIn",
    fields=[
        KuzuField(name="since", type=KuzuFieldTypeEnum.DATE),
    ],
    relationships=[
        KuzuRelationship(from_table="Person", to_table="City"),
    ],
)

multi_rel_table = KuzuRelTable(
    name="MultiRel",
    fields=[
        KuzuField(name="type", type=KuzuFieldTypeEnum.STRING),
        KuzuField(name="weight", type=KuzuFieldTypeEnum.FLOAT),
    ],
    relationships=[
        KuzuRelationship(from_table="Person", to_table="Person"),
        KuzuRelationship(from_table="Person", to_table="City"),
    ],
)

tables = [person_table, city_table, knows_table, lives_in_table, multi_rel_table]

# Example LinkML schema in YAML format - for reference (used for documentation only)
SOCIAL_NETWORK_SCHEMA = """
id: https://example.org/linkml/social-network
name: social-network-schema
description: Example schema for social network with people and cities
imports:
  - linkml:types
prefixes:
  linkml: https://w3id.org/linkml/
  SN: https://example.org/linkml/social-network/
  rdf: http://www.w3.org/1999/02/22-rdf-syntax-ns#
default_prefix: SN
default_range: string

classes:
  Node:
    abstract: true
    description: Abstract base class for all nodes in the graph
    attributes:
      id:
        identifier: true
        description: Unique identifier for the node

  Person:
    is_a: Node
    description: A person in the system
    attributes:
      name:
        description: Name of the person
        required: true
      age:
        description: Age of the person in years
        range: integer
        minimum_value: 0

  City:
    is_a: Node
    description: A city where people live
    attributes:
      name:
        description: Name of the city
        required: true
      population:
        description: Population of the city
        range: integer
        minimum_value: 0

  Edge:
    abstract: true
    class_uri: rdf:Statement
    description: Abstract base class for all relationships/edges in the graph
    attributes:
      from_node:
        slot_uri: rdf:subject
        description: Source node of the relationship
        range: Node
        required: true
      relationship_type:
        slot_uri: rdf:predicate
        description: Type of the relationship
        range: uriorcurie
        required: true
      to_node:
        slot_uri: rdf:object
        description: Target node of the relationship
        range: Node
        required: true

  Knows:
    is_a: Edge
    description: Relationship between people who know each other
    slot_usage:
      from_node:
        range: Person
      to_node:
        range: Person
    attributes:
      since:
        description: Date when the relationship began
        range: date
      strength:
        description: Strength of the relationship
        range: integer
        minimum_value: 1
        maximum_value: 10

  LivesIn:
    is_a: Edge
    description: Relationship between a person and the city they live in
    slot_usage:
      from_node:
        range: Person
      to_node:
        range: City
    attributes:
      since:
        description: Date when the person moved to the city
        range: date
"""

# Actual implementation of LinkML schema to KuzuDB conversion
# This uses a simplified dictionary-based approach without requiring linkml_runtime

# Attempt to import YAML - this is used for demonstration and testing
try:
    import yaml
except ImportError:
    # Define a minimal implementation for demonstration purposes
    class MockYAML:
        @staticmethod
        def safe_load(yaml_str):
            # This is a simplified mock that doesn't actually parse YAML
            print("WARNING: PyYAML not installed - using mock implementation")
            return {"classes": {}}
    yaml = MockYAML()

# Type mapping between LinkML types and KuzuDB types
LINKML_TO_KUZU_TYPE_MAP = {
    "string": KuzuFieldTypeEnum.STRING,
    "integer": KuzuFieldTypeEnum.INT64,
    "float": KuzuFieldTypeEnum.FLOAT,
    "boolean": KuzuFieldTypeEnum.BOOL,
    "date": KuzuFieldTypeEnum.DATE,
    "datetime": KuzuFieldTypeEnum.TIMESTAMP,
    "time": KuzuFieldTypeEnum.TIME,
}

def is_relationship_class(schema_dict, class_name):
    """
    Check if a class is a relationship class by determining if it or any of its 
    ancestors has class_uri = rdf:Statement.
    """
    if class_name not in schema_dict.get("classes", {}):
        return False
    
    cls = schema_dict["classes"][class_name]
    
    # Check if this class has class_uri = rdf:Statement
    if cls.get("class_uri") == "rdf:Statement":
        return True
    
    # Check ancestors recursively
    if "is_a" in cls:
        return is_relationship_class(schema_dict, cls["is_a"])
    
    return False

class KuzuGenerator(Generator):
    """
    A generator that creates KuzuDB schema from a LinkML model.
    
    KuzuDB (https://github.com/kuzudb/kuzu) is a graph database with both node and 
    relationship tables. This generator produces DDL statements to create KuzuDB tables.
    
    Node classes are mapped to NODE TABLE declarations with PRIMARY KEY.
    Edge classes (with class_uri: rdf:Statement) are mapped to REL TABLE
    declarations with FROM/TO relationships.
    """
    
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.0"
    valid_formats = ["kuzu", "kuzudb"]
    file_extension = "kuzu"
    node_classes = None
    relationship_classes = None
    
    # Python keywords to avoid for identifiers
    PYTHON_KEYWORDS = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 
        'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 
        'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 
        'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield'
    }
    
    def __init__(self, 
                 schema, 
                 node_classes: Optional[List[str]] = None,
                 relationship_classes: Optional[List[str]] = None,
                 subject_slot: Optional[str] = None,
                 object_slot: Optional[str] = None,
                 ):
        
        # super(KuzuGenerator, self).__init__(schema)        
        self.schemaview = SchemaView(schema)
        self.node_classes = list(node_classes)
        self.relationship_classes = list(relationship_classes)
        self.subject_slot = subject_slot
        self.object_slot = object_slot
        
    def _sanitize_identifier(self, name: str) -> str:
        """
        Sanitize a name to ensure it is a valid KuzuDB identifier.
        
        This follows similar patterns to the pydanticgen:
        1. Convert CamelCase to snake_case
        2. Replace spaces and other non-alphanumeric chars with underscores
        3. Ensure the name doesn't conflict with Python keywords
        4. Ensure the name is a valid identifier
        
        Args:
            name: The name to sanitize
        
        Returns:
            A valid identifier
        """
        if not name:
            return "field"
            
        # Convert to snake_case
        sanitized = underscore(name)
        
        # Replace any remaining non-alphanumeric characters with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', sanitized)
        
        # Ensure it starts with a letter or underscore
        if sanitized[0].isdigit():
            sanitized = f"_{sanitized}"
            
        # Handle Python keywords by appending underscore
        if sanitized in self.PYTHON_KEYWORDS:
            sanitized = f"{sanitized}_"
            
        return sanitized
        
    #TODO: use instantiates slot rather than class_uri to determine relationship / subject / edge    
    def _is_relationship_class(self, class_name: str) -> bool:
        """Determines if a class is a relationship class by checking for rdf:Statement"""
        # skip the inference if the class has been explicitly marked as a relationship class
        if class_name in self.relationship_classes:
            return True        

        try:
            cls = self.schemaview.get_class(class_name)
            if cls is None:
                return False
                
            # Check if this class has class_uri = rdf:Statement
            if cls.class_uri == "rdf:Statement":
                return True
                
            # Check ancestors recursively
            if cls.is_a:
                return self._is_relationship_class(cls.is_a)
        except Exception:
            # If any error occurs during checking, assume it's not a relationship class
            return False
            
        return False
    
    def _convert_to_kuzu_tables(self) -> List[Union[KuzuNodeTable, KuzuRelTable]]:
        """
        Convert the LinkML schema to KuzuDB tables
        """
        tables = []
        
        # Process all classes in the schema that aren't abstract
        all_classes = self.schemaview.all_classes()

        if isinstance(all_classes, list):
            # If all_classes returns a list, convert it to a dict
            all_classes = {cls.name: cls for cls in all_classes}

        print("node classes: ", self.node_classes)
        print("relationship classes: ", self.relationship_classes)

        # reduce all_classes to only node and relationship classes
        classes_to_generate = {c.name: c for c in all_classes.values() if c.name in self.node_classes or c.name in self.relationship_classes}

        for class_name, class_def in classes_to_generate.items():

            if class_def.abstract:
                print(f"Skipping abstract class: {class_name}")
                continue
                
            # Determine if this is a node or relationship class
            is_rel = self._is_relationship_class(class_name) or class_name in self.relationship_classes
                        
            # Process slots differently based on class type
            if is_rel:
                tables.append(self._generate_relationship_table(class_def))
            else:
                tables.append(self._generate_node_table(class_def))
        
        return tables
    
    def _generate_relationship_table(self, class_definition) -> KuzuRelTable:
        class_name = class_definition.name
        relationships = []
        fields = []
        subject_range = None
        object_range = None
        
        # Process each slot in the class
        try:
            slots = self.schemaview.class_induced_slots(class_name)
            if isinstance(slots, list):
                # Convert list to dict for consistent processing
                slots = {slot.name: slot for slot in slots}
        except Exception:
            # If we can't get slots, use an empty dict
            slots = {}
            
        for slot_name, slot_def in slots.items():
            # Check the slot_uri to determine the role
            try:
                if slot_def.slot_uri == "rdf:subject" or slot_name == self.subject_slot:
                    # Get the range of the subject slot
                    subject_range = slot_def.range
                    continue
                elif slot_def.slot_uri == "rdf:object" or slot_name == self.object_slot:
                    # Get the range of the object slot
                    object_range = slot_def.range
                    continue
                elif slot_def.slot_uri == "rdf:predicate":
                    # Skip predicate slot
                    continue
            except AttributeError:
                # If slot doesn't have slot_uri, just treat as a regular field
                pass
            
            # For all other slots, create fields
            field_type = self._get_kuzu_type(slot_def.range)
            # Ensure field name is a valid identifier
            sanitized_slot_name = self._sanitize_identifier(slot_name)
            field = KuzuField(name=sanitized_slot_name, type=field_type)
            fields.append(field)
        
        # Add relationship if subject and object ranges were found
        if subject_range and object_range:
            # Ensure from_table and to_table are valid identifiers
            sanitized_from_table = self._sanitize_identifier(subject_range)
            sanitized_to_table = self._sanitize_identifier(object_range)
            relationships.append(KuzuRelationship(
                from_table=sanitized_from_table, 
                to_table=sanitized_to_table
            ))
        sanitized_class_name = self._sanitize_identifier(class_name)
        return KuzuRelTable(
                name=sanitized_class_name,
                fields=fields,
                relationships=relationships
            )
    

    def _generate_node_table(self, class_definition) -> KuzuNodeTable:        
        class_name = class_definition.name
        fields = []
        # For node classes, create a node table
        # Get slots with error handling
        try:
            slots = self.schemaview.class_induced_slots(class_name)
            if isinstance(slots, list):
                # Convert list to dict for consistent processing
                slots = {slot.name: slot for slot in slots}
        except Exception:
            # If we can't get slots, use an empty dict
            slots = {}
        
        # First identify the primary key
        for slot_name, slot_def in slots.items():
            print("slot name: ", slot_name)
            try:
                if slot_def.identifier:
                    primary_key = slot_name
                    break
            except AttributeError:
                continue
                
        # Process all slots as fields
        for slot_name, slot_def in slots.items():
            try:
                field_type = self._get_kuzu_type(slot_def.range)
                # Ensure field name is a valid identifier
                sanitized_slot_name = self._sanitize_identifier(slot_name)
                print("slot name: ", slot_name)
                print("sanitized slot name: ", sanitized_slot_name)
                field = KuzuField(name=sanitized_slot_name, type=field_type)
                fields.append(field)
            except (AttributeError, TypeError):
                # Use string as default type if range is missing
                # Ensure field name is a valid identifier
                sanitized_slot_name = self._sanitize_identifier(slot_name)
                field = KuzuField(name=sanitized_slot_name, type=KuzuFieldTypeEnum.STRING)
                fields.append(field)
        
        # If no primary key found, use first field or create id field
        if primary_key is None:
            if fields:
                primary_key = fields[0].name
            else:
                primary_key = "id"
                id_field = KuzuField(name="id", type=KuzuFieldTypeEnum.STRING)
                fields.append(id_field)
        # If primary key was found but field wasn't created
        elif not any(field.name == self._sanitize_identifier(primary_key) for field in fields):
            sanitized_pk = self._sanitize_identifier(primary_key)
            pk_field = KuzuField(name=sanitized_pk, type=KuzuFieldTypeEnum.STRING)
            fields.append(pk_field)
        
        # Create node table
        # Ensure table name and primary key are valid identifiers
        sanitized_class_name = self._sanitize_identifier(class_name)
        sanitized_primary_key = self._sanitize_identifier(primary_key)
        return KuzuNodeTable(
            name=sanitized_class_name,
            fields=fields,
            primary_key=sanitized_primary_key
        )

    def _get_kuzu_type(self, range_name: str) -> KuzuFieldTypeEnum:
        """Map LinkML types to KuzuDB types"""
        # Handle None case
        if range_name is None:
            return KuzuFieldTypeEnum.STRING
        
        # Handle built-in primitive types
        type_mapping = {
            "string": KuzuFieldTypeEnum.STRING,
            "integer": KuzuFieldTypeEnum.INT64,
            "float": KuzuFieldTypeEnum.FLOAT,
            "boolean": KuzuFieldTypeEnum.BOOL,
            "date": KuzuFieldTypeEnum.DATE,
            "datetime": KuzuFieldTypeEnum.TIMESTAMP,
            "time": KuzuFieldTypeEnum.TIME,
        }
        
        if range_name in type_mapping:
            return type_mapping[range_name]
            
        # Check if it's a LinkML built-in type
        try:
            t = self.schemaview.get_type(range_name)
            if t and hasattr(t, 'typeof') and t.typeof in type_mapping:
                return type_mapping[t.typeof]
        except Exception:
            # If type lookup fails for any reason, default to string
            pass
                
        # Default to STRING for enums, classes, etc.
        return KuzuFieldTypeEnum.STRING
    
    def serialize(self) -> str:
        """Generate KuzuDB DDL statements"""
        
        tables = self._convert_to_kuzu_tables()
        print("Generating KuzuDB DDL statements...")
        print(tables)
        return template.render(tables=tables)



@click.command(name="kuzu")
@click.argument("yamlfile", type=click.Path(exists=True, dir_okay=False, readable=True))
@click.option(
    "--node-classes", "-n", multiple=True, help="Node classes to include"
)
@click.option(
    "--relationship-classes", "-r", multiple=True, help="Relationship classes to include"
)
@click.option(
    "--subject-slot", "-s", help="Slot to use as subject in relationships"
)
@click.option(
    "--object-slot", "-o", help="Slot to use as object in relationships"
)
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, 
        node_classes: Optional[List[str]] = None, 
        relationship_classes: Optional[List[str]] = None,
        subject_slot: Optional[str] = None,
        object_slot: Optional[str] = None,
        ):
    """Generate KuzuDB DDL statements to create tables for a LinkML model"""
    gen = KuzuGenerator(yamlfile, 
                        node_classes=node_classes, 
                        relationship_classes=relationship_classes,
                        subject_slot=subject_slot,
                        object_slot=object_slot)    
    print(gen.serialize())


if __name__ == "__main__":
    cli()
