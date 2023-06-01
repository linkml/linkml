sqlalchemy_declarative_template_str = """
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.schema import MetaData

metadata_obj = MetaData(schema="{{schemaname(model_path)}}")
Base = declarative_base(metadata=metadata_obj)
metadata = Base.metadata

{% for c in classes if is_join_table(c) %}
{{tablename(c.name)}} = Table(
    "{{tablename(c.name)}}",
    Base.metadata,
{% for s in c.attributes.values() -%}
     Column("{{columnname(s.alias)}}", {{s.annotations["sql_type"].value}}
           {%- if "foreign_key" in s.annotations -%}, ForeignKey("{{schemaname(model_path)}}.{{ columnname(s.annotations["foreign_key"].value) }}", deferrable=True,) {%- endif -%}
           {%- if "primary_key" in s.annotations -%}, primary_key=True {%- endif -%}
           {%- if "autoincrement" in s.annotations -%}, autoincrement=True {% endif -%}
           {%- if "required" in s.annotations -%}, nullable=False {% endif -%}
           ),
    {% endfor %}
    comment = \"\"\"{{c.comments[0]}}\"\"\",
)
{% endfor %}

{% for c in classes if not is_join_table(c) %}
class {{classname(c.name)}}({% if c.is_a %}{{ classname(c.is_a) }}{% else %}Base{% endif %}):
    \"\"\"
    {% if c.description %}{{c.description}}{% else %}{{c.alias}}{% endif %}
    \"\"\"
    __tablename__ = "{{tablename(c.name)}}"

    {% for s in c.attributes.values() -%}
    {{columnname(s.alias)}} = Column({{s.annotations["sql_type"].value}}
           {%- if 'foreign_key' in s.annotations -%}, ForeignKey('{{schemaname(model_path)}}.{{ columnname(s.annotations['foreign_key'].value) }}',  deferrable=True,) {%- endif -%}
           {%- if 'primary_key' in s.annotations -%}, primary_key=True {%- endif -%}
           {%- if 'autoincrement' in s.annotations -%}, autoincrement=True {% endif -%}
           {%- if "required" in s.annotations -%}, nullable=False {% endif -%}
           )
    {% if 'foreign_key' in s.annotations and 'original_slot' in s.annotations -%}
    {{columnname(s.annotations['original_slot'].value)}} = relationship("{{classname(s.range)}}", uselist=False)
    {% endif -%}
    {% endfor %}

    {%- for mapping in backrefs[c.name] %}
    {% if mapping.mapping_type == "ManyToMany" %}
    # ManyToMany
    {{columnname(mapping.source_slot)}} = relationship( "{{ classname(mapping.target_class) }}", secondary={{tablename(mapping.join_class)}})
    {% elif mapping.mapping_type == "MultivaluedScalar" %}
    {{columnname(mapping.source_slot)}}_rel = relationship( "{{ classname(mapping.join_class) }}" )
    {{columnname(mapping.source_slot)}} = association_proxy("{{mapping.source_slot}}_rel", "{{mapping.target_slot}}",
                                  creator=lambda x_: {{ classname(mapping.join_class) }}({{columnname(mapping.target_slot)}}=x_))
    {% else %}
    # One-To-Many: {{mapping}}
    {{columnname(mapping.source_slot)}} = relationship( "{{ classname(mapping.target_class) }}", foreign_keys="[{{ mapping.target_class }}.{{columnname(mapping.target_slot)}}]")
    {% endif -%}
    {%- endfor %}

    def __repr__(self):
        return f"{{c.name}}(
        {%- for s in c.attributes.values() -%}
        {{s.alias}}={self.{{s.alias}}},
        {%- endfor %})"



    {% if c.is_a or c.mixins %}
    # Using concrete inheritance: see https://docs.sqlalchemy.org/en/14/orm/inheritance.html
    __mapper_args__ = {
        'concrete': True
    }
    {% endif %}

{% endfor %}
"""
