sqlalchemy_imperative_template_str = """
from dataclasses import dataclass
from dataclasses import field
from typing import List

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

{% if not no_model_import %}
from {{model_path}} import *
{% endif %}

{% for c in classes %}
tbl_{{classname(c.name)}} = Table('{{c.name}}', metadata,
    {%- for s in c.attributes.values() %}
    Column('{{s.name}}',
          Text,
          {% if 'foreign_key' in s.annotations -%}
            ForeignKey('{{ s.annotations['foreign_key'].value }}'),
          {% endif -%}
          {% if 'primary_key' in s.annotations -%}
            primary_key=True
          {%- endif -%}
          ),
    {%- endfor %}
)
{% endfor -%}

# -- Mappings --

{% for c in classes if not is_join_table(c) %}
mapper_registry.map_imperatively({{classname(c.name)}}, tbl_{{classname(c.name)}}, properties = {
  ## NOTE: mapping omitted for now, see https://stackoverflow.com/questions/11746922/sqlalchemy-object-has-no-attribute-sa-adapter
  {% for mapping in backrefs[c.name] %}
  {% if mapping.uses_join_table %}
  {% else %}
  #'{{mapping.source_slot}}': relationship( {{ mapping.target_class }}, backref='{{c.name}}' ),
  {% endif %}
  #'{mapping.source_slot}': relationship()
  ## {{ mapping }}
  {% endfor %}
})
{% endfor %}
"""
