sqlalchemy_declarative_2x_template_str = """
from typing import List, Optional
from decimal import Decimal
from datetime import date, datetime, time

from sqlalchemy import ForeignKey, Index, Table, String, Text, Integer, Float, Numeric, Boolean, Time, DateTime, Date, Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

class Base(DeclarativeBase):
    pass

metadata = Base.metadata

{% for c in classes %}
class {{classname(c.name)}}({% if c.is_a %}{{ classname(c.is_a) }}{% else %}Base{% endif %}):
    \"\"\"
    {% if c.description %}{{c.description}}{% else %}{{c.alias}}{% endif %}
    \"\"\"
    __tablename__ = '{{c.name}}'

    {% for s in c.attributes.values() -%}
    {% set pytype = python_type(s.annotations['sql_type'].value) -%}
    {% if 'primary_key' in s.annotations -%}
    {{s.alias}}: Mapped[{{pytype}}] = mapped_column(
           {{- s.annotations['sql_type'].value}}
           {%- if 'foreign_key' in s.annotations -%}, ForeignKey('{{ s.annotations['foreign_key'].value }}'){%- endif -%}
           , primary_key=True
           {%- if 'autoincrement' in s.annotations -%}, autoincrement=True{% endif -%}
           )
    {% else -%}
    {% if 'required' in s.annotations -%}
    {{s.alias}}: Mapped[{{pytype}}] = mapped_column(
           {{- s.annotations['sql_type'].value}}
           {%- if 'foreign_key' in s.annotations -%}, ForeignKey('{{ s.annotations['foreign_key'].value }}'){%- endif -%}
           )
    {% else -%}
    {{s.alias}}: Mapped[Optional[{{pytype}}]] = mapped_column(
           {{- s.annotations['sql_type'].value}}
           {%- if 'foreign_key' in s.annotations -%}, ForeignKey('{{ s.annotations['foreign_key'].value }}'){%- endif -%}
           )
    {% endif -%}
    {% endif -%}
    {% if 'foreign_key' in s.annotations and 'original_slot' in s.annotations -%}
    {{s.annotations['original_slot'].value}}: Mapped[Optional["{{classname(s.range)}}"]] = relationship(foreign_keys=[{{s.alias}}])
    {% endif -%}
    {% endfor %}

    {%- for mapping in backrefs[c.name] %}
    {% if mapping.mapping_type == "ManyToMany" %}
    # ManyToMany
    {{mapping.source_slot}}: Mapped[List["{{ classname(mapping.target_class) }}"]] = relationship(secondary="{{ mapping.join_class }}")
    {% elif mapping.mapping_type == "MultivaluedScalar" %}
    {{mapping.source_slot}}_rel: Mapped[List["{{ classname(mapping.join_class) }}"]] = relationship()
    {{mapping.source_slot}}: AssociationProxy[List[str]] = association_proxy("{{mapping.source_slot}}_rel", "{{mapping.target_slot}}",
                                  creator=lambda x_: {{ classname(mapping.join_class) }}({{mapping.target_slot}}=x_))
    {% else %}
    # One-To-Many: {{mapping}}
    {{mapping.source_slot}}: Mapped[List["{{ classname(mapping.target_class) }}"]] = relationship(foreign_keys="[{{ mapping.target_class }}.{{mapping.target_slot}}]")
    {% endif -%}
    {%- endfor %}

    def __repr__(self):
        return f"{{c.name}}(
        {%- for s in c.attributes.values() -%}
        {{s.alias}}={self.{{s.alias}}},
        {%- endfor %})"


    {% if c.is_a or c.mixins %}
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/20/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    {% endif %}

{% endfor %}
"""
