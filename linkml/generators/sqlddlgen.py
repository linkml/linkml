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
    dialect: str

    # we maintain our own structure before feeding to sqlalchemy
    # https://stackoverflow.com/questions/52045695/sqlalchemy-remove-column-from-table-definition
    columns: Dict[str, Dict[str, Column]] = {}

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], dialect='sqlite', **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.relative_slot_num = 0
        self.dialect = dialect


    def end_schema(self, **kwargs) -> None:
        engine = create_engine(
            f'{self.dialect}://./MyDb',
            strategy='mock',
            executor= lambda sql, *multiparams, **params: print (sql))
        schema_metadata = MetaData()
        for t,colmap in self.columns.items():
            cols = colmap.values()
            Table(t, schema_metadata,
                  *cols)
        schema_metadata.create_all(engine)

    def visit_class(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract or not cls.slots:
            return False
        if cls.description:
            None ## TODO
        tname = camelcase(cls.name)
        self.columns[tname] = {}
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        tname = camelcase(cls.name)
        if self.use_inherits and cls.is_a:
            # postgresql supports inheritance
            # if you want to use plain SQL DDL then use sqlutils to unfold hierarchy
            # TODO: raise error if the target is standard SQL
            p = camelcase(cls.is_a)
            logging.error("Not supported in sqlalchemy")

    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        #qual = 'repeated ' if slot.multivalued else 'optional ' if not slot.required or slot.key else ''
        slotname = underscore(aliased_slot_name)
        tname = camelcase(cls.name)
        slot_range = self.get_sql_range(slot)
        if slot.multivalued:
            linktable_name = f'{tname}_to_{slotname}'
            pk = self._get_primary_key(cls)
            if pk is None:
                raise Exception(f'Cannot have multivalued on cols with no PK: {tname}')
            ref = f'ref_{tname}'
            linkrange = None
            if isinstance(slot_range, ForeignKey):
                linkrange = Text()
            else:
                linkrange = slot_range
            linktable_slot = slotname
            if slot.singular_name is not None:
                linktable_slot = underscore(slot.singular_name)
            self.columns[linktable_name] = {
                linktable_slot: Column(linktable_slot, linkrange),
                ref: Column(ref, ForeignKey(f'{tname}.{pk}'))
            }
        is_pk = slot.identifier
        col = Column(slotname, slot_range, primary_key=is_pk)
        self.columns[tname][slotname] = col

    def get_sql_range(self, slot: SlotDefinition) -> str:

        range = slot.range
        if range in self.schema.classes:
            rc = self.schema.classes[range]
            pk = None
            for sn in rc.slots:
                s = self.schema.slots[sn]
                if s.identifier:
                    if pk is not None:
                        logging.error(f"Multiple pks for {range}: {pk} AND {s}")
                    pk = s.alias if s.alias is not None else s.name
            if pk is not None:
                return ForeignKey(f'{camelcase(range)}.{pk}')
        if range in self.schema.types:
            range = self.schema.types[range].base

        if range in self.schema.enums:
            e = self.schema.enums[range]
            if e.permissible_values is not None:
                vs = [str(v) for v in e.permissible_values]
                return Enum(*vs)

        if range == 'string':
            return Text()
        elif range == 'integer':
            return Integer()
        elif range == 'boolean':
            return Boolean()
        elif range == 'float':
            return Float()
        else:
            logging.warning(f'UNKNOWN: {range}')
            return Text()

    def _get_primary_key(self, cls: ClassDefinition) -> SlotDefinition:
        pk = None
        for sn in cls.slots:
            s = self.schema.slots[sn]
            if s.identifier:
                if pk is not None:
                    logging.error(f"Multiple pks for {range}: {pk} AND {s}")
                pk = s.alias if s.alias is not None else s.name
        return pk

@shared_arguments(SQLDDLGenerator)
@click.command()
@click.option("--dialect", help="""
SQL-Alchemy dialect, e.g. sqlite, mysql+odbc
""")
def cli(yamlfile, **args):
    """ Generate SQL DDL representation """
    print(SQLDDLGenerator(yamlfile, **args).serialize(**args))
