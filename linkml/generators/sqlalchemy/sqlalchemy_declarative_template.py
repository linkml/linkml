sqlalchemy_declarative_template_str = """
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()
metadata = Base.metadata

{% for c in classes %}
class {{classname(c.name)}}({% if c.is_a %}{{ classname(c.is_a) }}{% else %}Base{% endif %}):
    \"\"\"
    {% if c.description %}{{c.description}}{% else %}{{c.alias}}{% endif %}
    \"\"\"
    __tablename__ = '{{c.name}}'
    
    {% for s in c.attributes.values() -%}
    {{s.alias}} = Column({{s.annotations['sql_type'].value}}
           {%- if 'foreign_key' in s.annotations -%}, ForeignKey('{{ s.annotations['foreign_key'].value }}') {%- endif -%}
           {%- if 'primary_key' in s.annotations -%}, primary_key=True {%- endif -%}
           {%- if 'autoincrement' in s.annotations -%}, autoincrement=True {% endif -%}
           )
    {% if 'foreign_key' in s.annotations and 'original_slot' in s.annotations -%}
    {{s.annotations['original_slot'].value}} = relationship("{{classname(s.range)}}", uselist=False, foreign_keys=[{{s.alias}}])
    {% endif -%}
    {% endfor %}
    
    {%- for mapping in backrefs[c.name] %}
    {% if mapping.mapping_type == "ManyToMany" %}
    # ManyToMany
    {{mapping.source_slot}} = relationship( "{{ classname(mapping.target_class) }}", secondary="{{ mapping.join_class }}")
    {% elif mapping.mapping_type == "MultivaluedScalar" %}
    {{mapping.source_slot}}_rel = relationship( "{{ classname(mapping.join_class) }}" )
    {{mapping.source_slot}} = association_proxy("{{mapping.source_slot}}_rel", "{{mapping.target_slot}}",
                                  creator=lambda x_: {{ classname(mapping.join_class) }}({{mapping.target_slot}}=x_))
    {% else %}
    # One-To-Many: {{mapping}}
    {{mapping.source_slot}} = relationship( "{{ classname(mapping.target_class) }}", foreign_keys="[{{ mapping.target_class }}.{{mapping.target_slot}}]")
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
