import logging
import os
from copy import copy
from dataclasses import dataclass, field
from enum import unique
from typing import List, Dict, Union, TextIO

from jinja2 import Template
from sqlalchemy import *

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, SlotDefinition, Annotation, \
    ClassDefinitionName, Prefix
from linkml_runtime.utils.formatutils import underscore, camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from linkml.utils.generator import Generator

template = """
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

from {{model_path}} import *

{% for c in classes %}
tbl_{{c.name}} = Table('{{c.name}}', metadata,
    {% for s in c.attributes.values() -%}
    Column('{{s.name}}',
           Text,
           {% if 'primary_key' in s.annotations -%} primary_key=True, {% endif %}
           {% if 'foreign_key' in s.annotations -%} foreign_key('{{ s.annotations['foreign_key'].value }}'), {% endif %}
           ) 
    {% endfor %}
)
{% endfor %}

# -- Mappings --

{% for c in classes %}
mapper_registry.map_imperatively({{c.name}}, tbl_{{c.name}}, properties = {
})
{% endfor %}

"""


class SQLAlchemyGenerator(Generator):
    """

    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['sqla']

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], dialect='sqlite',
                 **kwargs) -> None:
        self.schema = schema

    def generate_sqla(self,  **kwargs) -> str:
        sqltr = RelationalModelTransformer(SchemaView(self.schema))
        tr_result = sqltr.transform(**kwargs)
        schema = tr_result.schema
        print(f'MAPPINGS: {len(tr_result.mappings)}')
        for m in tr_result.mappings:
            print(f'M={m}')
        template_obj = Template(template)
        #for c in schema.classes.values():
        #    for s in c.attributes.values():
        #        print(f'{c.name}.{s.name} ANNs = {s.annotations}')
        code = template_obj.render(model_path=schema.name,
                                   classes=schema.classes.values())
        return code
