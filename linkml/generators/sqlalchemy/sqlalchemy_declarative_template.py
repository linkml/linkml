sqlalchemy_declarative_template_str = """
from sqlalchemy import Column, Index, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

{% for c in classes %}
class {{c.alias}}(Base):
    __tablename__ = '{{c.name}}'
    
    {% for s in c.attributes.values() -%}
    {{s.alias}} = Column({{s.annotations['sql_type'].value}}
           {%- if 'foreign_key' in s.annotations -%}, ForeignKey('{{ s.annotations['foreign_key'].value }}') {%- endif -%}
           {%- if 'primary_key' in s.annotations -%}, primary_key=True {%- endif -%}
           {%- if 'autoincrement' in s.annotations -%}, autoincrement=True {% endif -%}
           )
    {% if 'foreign_key' in s.annotations and 'original_slot' in s.annotations -%}
    {{s.annotations['original_slot'].value}} = relationship("{{s.range}}", uselist=False)
    {% endif -%}
    {% endfor %}
    
    {%- for mapping in backrefs[c.name] %}
    {%- if mapping.uses_join_table -%}
    # TODO
    {%- else -%}
    {{mapping.source_slot}} = relationship( "{{ mapping.target_class }}", backref='{{c.alias}}')
    {% endif -%}
    {%- endfor %}
    
    def __repr__(self):
        return f"{{c.name}}(
        {%- for s in c.attributes.values() -%}
        {{s.alias}}={self.{{s.alias}}}, 
        {%- endfor %})"

{% endfor %}
"""
