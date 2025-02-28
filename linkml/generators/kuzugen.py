from pydantic import BaseModel, model_validator
from enum import Enum
from jinja2 import Template

## jinja template for kuzu schema generation

class KuzuTableTypeEnum(Enum):
    NODE = 'NODE'
    REL = 'REL'

class KuzuFieldTypeEnum(Enum):
    STRING = 'STRING'
    INT = 'INT64'
    FLOAT = 'FLOAT'
    BOOL = 'BOOLEAN'
    DATETIME = 'TIMESTAMP'
    DATE = 'DATE'
    TIME = 'TIME'

class KuzuField(BaseModel):
    name: str
    type: KuzuFieldTypeEnum

    class Config:
        schema_extra = {
            "required": ["name", "type"]
        }

    @model_validator(mode='before')
    def check_field_name_is_valid(self):
        name = self.get('name')
        if not name.isidentifier():
            raise ValueError('Field name {name} is not a valid identifier')
        return self


class KuzuTable(BaseModel):
    type: KuzuTableTypeEnum
    name: str
    fields: list[KuzuField]
    primary_key: str

    class Config:
        schema_extra = {
            "required": ["type", "name", "fields", "primary_key"]
        }

    @model_validator(mode='before')
    def check_primary_key_in_fields(self):
        primary_key = self.get('primary_key')
        fields = self.get('fields', [])
        field_names = [field.name for field in fields]
        if primary_key not in field_names:
            raise ValueError('primary_key must be one of the fields')
        return self
    
    @model_validator(mode='before')
    def check_class_name_is_valid(self):
        name = self.get('name')
        if not name.isidentifier():
            raise ValueError('Table name {name} is not a valid identifier')
        return self    


template = Template("""
{% for table in tables %}
CREATE {{ table.type.value }} TABLE {{ table.name }} (
    {%- for field in table.fields %}
    {{ field.name }} {{ field.type }},
    {%- endfor %}
    PRIMARY KEY ({{ table.primary_key }})
);
{% endfor %}
""")


person_table = KuzuTable(
    type=KuzuTableTypeEnum.NODE,
    name='Person',
    fields=[
        KuzuField(name='name', type=KuzuFieldTypeEnum.STRING),
        KuzuField(name='age', type=KuzuFieldTypeEnum.INT),
    ],
    primary_key='name'
)

knows_table = KuzuTable(
    type=KuzuTableTypeEnum.REL,
    name='Knows',
    fields=[
        KuzuField(name='from', type=KuzuFieldTypeEnum.STRING),
        KuzuField(name='to', type=KuzuFieldTypeEnum.STRING),
    ],
    primary_key='from'
)

tables = [person_table, knows_table]

print(template.render(tables=tables))
