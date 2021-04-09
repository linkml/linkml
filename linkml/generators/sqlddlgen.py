import os
from typing import Union, TextIO, Dict

import click
import logging

from sqlalchemy import *
from linkml_model.meta import ClassDefinition, SlotDefinition, SchemaDefinition
from linkml.utils.formatutils import camelcase, lcamelcase, underscore
from linkml.utils.generator import Generator, shared_arguments

def _quote(s: str) -> str:
    s = s.replace("'", "\\'")
    return f"'{s}'"



class SQLDDLGenerator(Generator):
    """
    A `Generator` for creating SQL DDL
    TODO: allow configuration between camelcase and snake case for tanle names
    
    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['proto']
    visit_all_class_slots: bool = True
    use_inherits: bool = False  ## postgresql supports inheritance
    target_dbms: str = 'sqlite'
    #tables: Dict[str, Dict[str, str]] = {}

    # we maintain our own structure before feeding to sqlalchemy
    # https://stackoverflow.com/questions/52045695/sqlalchemy-remove-column-from-table-definition
    tables = {}
    columns = {}
    current_table = None
    engine = None
    schema_metadata = MetaData()
    current_cols = []

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.relative_slot_num = 0


    def end_schema(self, **kwargs) -> None:
        engine = create_engine(
            'sqlite://./MyDb',
            strategy='mock',
            executor= lambda sql, *multiparams, **params: print (sql))
        
        self.schema_metadata.create_all(engine)

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract or not cls.slots:
            return False
        if cls.description:
            None ## TODO
        tname = camelcase(cls.name)
        self.current_cols = []
        self.columns[tname] = {}
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        tname = camelcase(cls.name)
        t = Table(tname, self.schema_metadata,
                  *self.current_cols)
        if self.use_inherits and cls.is_a:
            # postgresql supports inheritance
            # if you want to use plain SQL DDL then use sqlutils to unfold hierarchy
            # TODO: raise error if the target is standard SQL
            p = camelcase(cls.is_a)
            logging.error("Not supported in sqlalchemy")

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        #qual = 'repeated ' if slot.multivalued else 'optional ' if not slot.required or slot.key else ''
        slotname = underscore(aliased_slot_name)
        slot_range = self.get_sql_range(slot)
        col = Column(slotname, Text())
        self.current_cols.append(col)

    def get_sql_range(self, slot: SlotDefinition) -> str:
        db = self.target_dbms
        ## https://www.sqlite.org/datatype3.html
        range = slot.range
        if range in self.schema.enums:
            if db == 'sqlite':
                return 'string'
            e = self.schema.enums[range]
            if e.permissible_values is not None:
                vs = [_quote(v) for v in e.permissible_values]
                vstr = ", ".join(vs)
                return f'enum({vstr})'

        if range == 'string':
            return 'string'
        elif range == 'integer':
            if db == 'sqlite':
                return 'integer'
            else:
                return 'int'
        elif range == 'boolean':
            if db == 'sqlite':
                return 'int'
            else:
                return 'bool'
        elif range == 'float':
            if db == 'sqlite':
                return 'real'
            else:
                return 'float'
        else:
            logging.warning(f'UNKNOWN: {range}')
            return 'string'


@shared_arguments(SQLDDLGenerator)
@click.command()
def cli(yamlfile, **args):
    """ Generate SQL DDL representation """
    print(ProtoGenerator(yamlfile, **args).serialize(**args))
