import logging
import os
#import sys
from collections import defaultdict
from copy import copy
from dataclasses import dataclass, field
from enum import unique
from types import ModuleType
from typing import List, Dict, Union, TextIO

from jinja2 import Template
from linkml_runtime.utils.compile_python import compile_python, file_text
from sqlalchemy import *

from linkml_runtime.linkml_model import SchemaDefinition, ClassDefinition, SlotDefinition, Annotation, \
    ClassDefinitionName, Prefix
from linkml_runtime.utils.formatutils import underscore, camelcase
from linkml_runtime.utils.schemaview import SchemaView

from linkml.generators.sqlalchemy import sqlalchemy_imperative_template_str, sqlalchemy_declarative_template_str
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.transformers.relmodel_transformer import RelationalModelTransformer
from linkml.utils.generator import Generator

class TemplateEnum(Enum):
    DECLARATIVE = "declarative"
    IMPERATIVE = "imperative"

class SQLAlchemyGenerator(Generator):
    """

    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['sqla']

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], dialect='sqlite',
                 **kwargs) -> None:
        self.original_schema = schema
        super().__init__(schema, **kwargs)
        self.schemaview = SchemaView(schema)

    def generate_sqla(self,
                      model_path: str = None,
                      no_model_import = False,
                      template: TemplateEnum = TemplateEnum.IMPERATIVE,
                      **kwargs) -> str:
        #src_sv = SchemaView(self.schema)
        #self.schema = src_sv.schema
        sqltr = RelationalModelTransformer(self.schemaview)
        tgen = SQLTableGenerator(self.schemaview.schema)
        tr_result = sqltr.transform(**kwargs)
        tr_schema = tr_result.schema
        for c in tr_schema.classes.values():
            for a in c.attributes.values():
                sql_range = tgen.get_sql_range(a, tr_schema)
                sql_type = sql_range.__repr__()
                ann = Annotation('sql_type', sql_type)
                a.annotations[ann.tag] = ann
                #a.sql_type = sql_type
        if template == TemplateEnum.IMPERATIVE:
            template_str = sqlalchemy_imperative_template_str
        elif template == TemplateEnum.DECLARATIVE:
            template_str = sqlalchemy_declarative_template_str
        else:
            raise Exception(f'Unknown template type: {template}')
        template_obj = Template(template_str)
        self.add_safe_aliases(tr_schema)
        if model_path is None:
            model_path = self.schema.name
        logging.info(f'Package for dataclasses ==  {model_path}')
        backrefs = defaultdict(list)
        for m in tr_result.mappings:
            backrefs[m.source_class].append(m)
        code = template_obj.render(model_path=model_path,
                                   mappings=tr_result.mappings,
                                   backrefs=backrefs,
                                   no_model_import=no_model_import,
                                   is_join_table=lambda c: any(tag for tag in c.annotations.keys() if tag == 'linkml:derived_from'),
                                   classes=tr_schema.classes.values())
        return code

    def compile_sqla(self,
                     compile_python_dataclasses=False,
                     model_path=None,
                     template: TemplateEnum = TemplateEnum.IMPERATIVE,
                     **kwargs) -> ModuleType:

        if model_path is None:
            model_path = self.schema.name

        if template == TemplateEnum.DECLARATIVE:
            sqla_code = self.generate_sqla(model_path=None, no_model_import=True, template=template, **kwargs)
            return compile_python(sqla_code, package_path=model_path)
        elif compile_python_dataclasses:
            # concatenate the python dataclasses with the sqla code
            pygen = PythonGenerator(self.original_schema)
            dc_code = pygen.serialize()
            sqla_code = self.generate_sqla(model_path=None, no_model_import=True, **kwargs)
            return compile_python(f'{dc_code}\n{sqla_code}', package_path=model_path)
        else:
            code = self.generate_sqla(model_path=model_path, **kwargs)
            return compile_python(code, package_path=model_path)

    def add_safe_aliases(self, schema: SchemaDefinition) -> None:
        for c in schema.classes.values():
            c.alias = underscore(c.name)
            for a in c.attributes.values():
                a.alias = underscore(a.name)
