from enum import Enum
from abc import ABC

from jinja2 import Template
from pydantic import BaseModel, model_validator

## jinja template for kuzu schema generation


class KuzuFieldTypeEnum(Enum):
    STRING = "STRING"
    INT = "INT64"
    FLOAT = "FLOAT"
    BOOL = "BOOLEAN"
    DATETIME = "TIMESTAMP"
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
            raise ValueError("Field name {name} is not a valid identifier")
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
            raise ValueError("Table name {name} is not a valid identifier")
        return self


class KuzuNodeTable(KuzuTable):
    primary_key: str

    class Config:
        schema_extra = {"required": ["name", "fields", "primary_key"]}
    
    @model_validator(mode="before")
    def check_primary_key_in_fields(self):
        primary_key = self.get("primary_key")
        fields = self.get("fields", [])
        field_names = [field.name for field in fields]
        if primary_key not in field_names:
            raise ValueError("primary_key must be one of the fields")
        return self
    
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



neo4j_cypher = """
MATCH (g:Gene)-[:has_phenotype]->(p:PhenotypicFeature)
"""

kuzu_cypher = """
MATCH (g:Gene)-[:Association {predicate: 'biolink:has_phenotype'}]->(p:PhenotypicFeature)
"""



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
        KuzuField(name="age", type=KuzuFieldTypeEnum.INT),
    ],
    primary_key="name",
)

city_table = KuzuNodeTable(
    name="City",
    fields=[
        KuzuField(name="name", type=KuzuFieldTypeEnum.STRING),
        KuzuField(name="population", type=KuzuFieldTypeEnum.INT),
    ],
    primary_key="name",
)

knows_table = KuzuRelTable(
    name="Knows",
    fields=[
        KuzuField(name="since", type=KuzuFieldTypeEnum.DATE),
        KuzuField(name="strength", type=KuzuFieldTypeEnum.INT),
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

print(template.render(tables=tables))
