import os
from typing import Union, TextIO, Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import click
import logging

from sqlalchemy import *
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition, SchemaDefinition, ClassDefinitionName, SlotDefinitionName
from linkml_runtime.utils.formatutils import underscore, camelcase
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int

TABLENAME = str
COLNAME = str
SQL_STR = str

RANGEMAP = {
    'str': Text(),
    'NCName': Text(),
    'URIorCURIE': Text(),
    'int': Integer(),
    'double': Float(),
    'float': Float(),
    'Bool': Boolean(),
    'URI': Text()
}

def _quote(s: str) -> str:
    s = s.replace("'", "\\'")
    return f"'{s}'"


@dataclass(unsafe_hash=True)
class DDLEntity():
    """
    abstract grouping
    """
    description: str = None

@dataclass
class SQLColumn(DDLEntity):
    """
    represents a Relational Table Column
    """
    name: COLNAME = None
    mapped_to: SlotDefinition = None
    table: "SQLTable" = None
    base_type: str = None
    is_singular_primary_key: bool = False
    foreign_key: Optional["SQLColumn"] = None

    def as_ddlstr(self):
        return f'{self.table.name}.{self.name}'

    def is_primary_key(self):
        return self in self.table.primary_keys

@dataclass
class SQLTable(DDLEntity):
    """
    represents a Relational Table
    """
    name: TABLENAME = None
    mapped_to: ClassDefinition = None
    columns: Dict[COLNAME, SQLColumn] = field(default_factory=dict)
    in_schema: "SQLSchema" = None
    referenced_by: List["SQLColumn"] = field(default_factory=list)
    primary_keys: List["SQLColumn"] = field(default_factory=list)

    def as_var(self) -> str:
        return f'tbl_{self.name}'

    def get_singular_primary_key(self) -> Optional[SQLColumn]:
        for c in self.columns.values():
            if c.is_singular_primary_key:
                return c
        return None

    def add_column(self, c: SQLColumn):
        self.columns[c.name] = c
        c.table = self


@dataclass
class SQLSchema(DDLEntity):
    """
    represents a Relational Schema
    """
    name: str = None
    mapped_to: SchemaDefinition = None
    tables: Dict[TABLENAME, SQLTable] = field(default_factory=dict)

    def all_columns(self) -> List[SQLColumn]:
        for t in self.tables.values():
            for c in t.columns.values():
                yield c

    def get_table_by_class_name(self, cn: ClassDefinitionName) -> Optional[SQLTable]:
        for t in self.tables.values():
            if t.mapped_to is not None and t.mapped_to.name == cn:
                return t
        return None

    def add_table(self, t: SQLTable):
        self.tables[t.name] = t
        for c in t.columns.values():
            c.table = t


# TODO: allow configuration between camelcase and snake case for table names

class SQLDDLGenerator(Generator):
    """
    A `Generator` for creating SQL DDL

     - Each Class C is mapped to a table T, where T = map_class_to_table(C)
     - Each slot S in C is mapped to a column Col, where Col = map_slot_to_column(CS)

     Mapping ranges:

     Each mapped slot C.S has a range R

     ranges that are types (literals):
       - If R is a type, and the slot is NOT multivalued, do a direct type conversion
       - If R is a type, and the slot is multivalued:
         * do not include the mapped column
         * create a new table T_S, with 2 columns: S, and a backref to T
      ranges that are classes:
       Ref = map_class_to_table(R)
       - if R is a class, and the slot is NOT multivalued, and Ref has a singular primary key:
         * Col.type = ForeignKey(Ref.PK)
       - if R is a class, and the slot is NOT multivalued, and Ref has NO singular primary key:
         * add a foreign key C.pk to Ref
         * add a backref C.S => Ref, C.pk
         * remove Col from T
       - If R is a class, and the slot IS multivalued

    """
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ['proto']
    visit_all_class_slots: bool = True
    use_inherits: bool = False  ## postgresql supports inheritance
    dialect: str
    inject_primary_keys: bool = True
    sqla_python_lines: List[str] = []
    sqlschema: SQLSchema = SQLSchema()

    # we maintain our own structure before feeding to sqlalchemy
    # tablename -> colname -> Column
    # https://stackoverflow.com/questions/52045695/sqlalchemy-remove-column-from-table-definition
    columns: Dict[TABLENAME, Dict[COLNAME, Column]] = {}

    mapped_foreign_keys: Dict[Tuple[TABLENAME, COLNAME], COLNAME] = {}

    table_to_class: Dict[TABLENAME, ClassDefinition] = {}
    table_columns_to_slot: Dict[Tuple[TABLENAME, COLNAME], SlotDefinition] = {}

    def __init__(self, schema: Union[str, TextIO, SchemaDefinition], dialect='sqlite',
                 use_foreign_keys = True,
                 rename_foreign_keys = False,
                 direct_mapping = False,
                 **kwargs) -> None:
        super().__init__(schema, **kwargs)
        self.relative_slot_num = 0
        self.dialect = dialect
        self.use_foreign_keys = use_foreign_keys
        self.rename_foreign_keys = rename_foreign_keys
        self.direct_mapping = direct_mapping
        self.sqlschema = SQLSchema()
        self.sqla_python_lines = [
            'from sqlalchemy import Column, Index, Table, Text',
            'from sqlalchemy.sql.sqltypes import NullType',
            'from sqlalchemy.ext.declarative import declarative_base',
            '',
            'Base = declarative_base()',
            'metadata = Base.metadata']

    def to_sqla_python(self) -> str:
        """
        declarative mapping:
        https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#declarative-mapping
        """
        return "\n".join(self.sqla_python_lines)



    def _is_hidden(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract:
            return True

    def _class_name_to_table(self, cn: ClassDefinitionName) -> str:
        """
        https://stackoverflow.com/questions/1881123/table-naming-underscore-vs-camelcase-namespaces-singular-vs-plural
        """
        return underscore(cn)

    def _slot_name_to_column(self, sn: SlotDefinitionName) -> str:
        """
        use underscore by default
        """
        return underscore(sn)

    def end_schema(self, **kwargs) -> None:
        self._transform_sqlschema()
        self.generate_ddl()

    def visit_class(self, cls: ClassDefinition) -> bool:
        if self._is_hidden(cls):
            return False
        if cls.description:
            None ## TODO
        tname = self._class_name_to_table(cls.name)
        self.columns[tname] = {}
        # add table
        self.sqlschema.tables[tname] = SQLTable(name=tname, mapped_to=cls)
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        if self._is_hidden(cls):
            return False
        tname = self._class_name_to_table(cls.name)
        if self.use_inherits and cls.is_a:
            # postgresql supports inheritance
            # if you want to use plain SQL DDL then use sqlutils to unfold hierarchy
            # TODO: raise error if the target is standard SQL
            p = self._class_name_to_table(cls.is_a)
            logging.error("Not supported in sqlalchemy")
        self.table_to_class[tname] = cls


    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        if self._is_hidden(cls):
            return False
        sqlschema = self.sqlschema
        #qual = 'repeated ' if slot.multivalued else 'optional ' if not slot.required or slot.key else ''
        colname = self._slot_name_to_column(aliased_slot_name)
        tname = self._class_name_to_table(cls.name)
        sqltable = sqlschema.tables[tname]
        #mapping = SQLMapping(table_name=tname, column_name=colname)
        slot_range = self.get_sql_range(slot)
        is_pk = slot.identifier
        sqlcol: SQLColumn
        sqlcol = SQLColumn(name=colname, mapped_to=slot,
                           is_singular_primary_key=is_pk, description=slot.description,
                           table=sqlschema.tables[tname])
        sqltable.columns[colname] = sqlcol
        sqlcol.base_type = slot_range

        if isinstance(slot_range, ForeignKey) and not self.use_foreign_keys:
            slot_range = Text()
        if isinstance(slot_range, ForeignKey) and self.use_foreign_keys and self.rename_foreign_keys:
            colname = f'{colname}_id'

        if slot.multivalued:
            ## create a linking table for any multi-valued slot
            ## TODO: only do this for many-to-many
            linktable_name = f'{tname}_to_{colname}'
            pk = self._get_primary_key(cls)
            if pk is None:
                if self.inject_primary_keys:
                    pk = 'id'
                    self.columns[tname][pk] = Column(pk, Text(), primary_key=True)
                else:
                    raise Exception(f'Cannot have multivalued on cols with no PK: {tname} . {colname}')
            ref = f'backlink_{tname}'
            #if isinstance(slot_range, ForeignKey):
            #    linkrange = Text()
            #else:
            #    linkrange = slot_range
            linktable_slot = colname
            if slot.singular_name is not None:
                linktable_slot = self._class_name_to_table(slot.singular_name)
            self.columns[linktable_name] = {
                linktable_slot: Column(linktable_slot, slot_range, nullable=False),
                ref: Column(ref, ForeignKey(f'{tname}.{pk}'), nullable=False)
            }
            #if tname not in self.backrefs:
            #    self.backrefs[tname] = {}
            #self.backrefs[tname][slotname] = Backref(backref_to_table='x')
            #self.table_to_class[linktable_name] = ClassDefinition(name=linktable_name)
        else:
            col = Column(colname, slot_range, primary_key=is_pk, nullable=not slot.required)
            if slot.description:
                col.comment = slot.description
            self.columns[tname][colname] = col
            self.table_columns_to_slot[(tname, colname)] = slot
        #self.mappings.append(mapping)

    def _transform_sqlschema(self):
        sqlschema = self.sqlschema
        if self.direct_mapping:
            return
        # index all referenced tables
        for sqlcol in sqlschema.all_columns():
            slot = sqlcol.mapped_to
            range = slot.range
            ref = sqlschema.get_table_by_class_name(range)
            if ref is not None:
                ref.referenced_by.append(sqlcol)
        # add autoincrement primary keys
        for t in sqlschema.tables.values():
            n_refs = len(t.referenced_by)
            if n_refs > 0:
                pkcol = t.get_singular_primary_key()
                if pkcol is None:
                    # TODO: add primary key column
                    None
        for sqlcol in list(sqlschema.all_columns()):
            table = sqlcol.table
            slot = sqlcol.mapped_to
            range = slot.range
            ref = sqlschema.get_table_by_class_name(range)
            basic_type = 'Text'
            table_pk = table.get_singular_primary_key()
            if slot.multivalued:
                if ref is None and table_pk is not None:
                    # primitive base type:
                    # create a linking table
                    linktable_name = f'{table.name}_{sqlcol.name}'
                    backref_col_name = 'backref_id'
                    linktable = SQLTable(name=linktable_name)
                    linktable.add_column(SQLColumn(name=backref_col_name, foreign_key=table_pk))
                    linktable.add_column(sqlcol)
                    sqlschema.add_table(linktable)
                    del table.columns[sqlcol.name]
                if ref is not None and table_pk is not None:
                    backref_col_name = f'{table.name}_{table_pk.name}'
                    ref.add_column(SQLColumn(name=backref_col_name, foreign_key=table_pk))
            else:
                if ref is not None:
                    ref_pk = ref.get_singular_primary_key()
                    if ref_pk is not None:
                        sqlcol.foreign_key=ref_pk
                    else:
                        logging.error(f'No PK for {ref}')
        for t in sqlschema.tables.values():
            pk = t.get_singular_primary_key()
            if pk is None:
                pks = t.columns.values()
            else:
                pks = [pk]
            t.primary_keys = pks


    def get_sql_range(self, slot: SlotDefinition):
        """
        returns a SQL Alchemy column type
        """
        range = slot.range
        if range in self.schema.classes:
            return Text()
        if range in self.schema.types:
            range = self.schema.types[range].base

        if range in self.schema.enums:
            e = self.schema.enums[range]
            if e.permissible_values is not None:
                vs = [str(v) for v in e.permissible_values]
                return Enum(*vs)
        if range in RANGEMAP:
            return RANGEMAP[range]
        else:
            logging.warning(f'UNKNOWN: {range} // {type(range)}')
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

    def write_sqla_python_imperative(self, model_path: str) -> str:
        """
        imperative mapping:
        https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#imperative-mapping-with-dataclasses-and-attrs

        maps to the python classes generated using PythonGenerator

        ```
        output = StringIO()
        with redirect_stdout(output):
           gen.write_sqla_python_imperative()
        """
        print(f'''
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
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

from {model_path} import *

''')
        for t, colmap in self.columns.items():
            cols = colmap.values()
            if len(cols) == 0:
                continue
            var = self._get_sqla_var_for_table(t)
            print(f"{var} = Table('{t}', metadata, ")
            pks = self._get_primary_keys(t)
            for col in cols:
                #print(f"    {col.__repr__()},")
                range = 'Text'
                print(f"    Column('{underscore(col.name)}', {range}", end='')
                for fk in col.foreign_keys:
                    print(f", {fk}", end='')
                if col in pks:
                    print(', primary_key=True', end='')
                print("),")
            print(")")
        for t in self.columns.keys():
            if t in self.table_to_class:
                # non-linking table
                var = self._get_sqla_var_for_table(t)
                cls = self.table_to_class[t]
                cn = camelcase(cls.name)
                print(f"mapper_registry.map_imperatively({cn}, {var}, properties={{")
                for ((xt, orig_colname), mapped_cn) in self.mapped_foreign_keys.items():
                    if xt == t:
                        #fk_table = self._get_sqla_var_for_table(t)
                        print(f"    '{orig_colname}': relationship('TODO', foreign_keys=")
                        None
                for colname, col in self.columns[t].items():
                    if isinstance(col, ForeignKey):
                        None
                #if t in self.backrefs:
                #    for backref in self.backrefs[t]:
                #        printf(f"    ''")
                print("})")


    def _get_primary_keys(self, t: str) -> List:
        cols = self.columns[t].values()
        pks = [col for col in cols if col.primary_key]
        if len(pks) == 0:
            pks = cols
        return pks

    def _get_sqla_var_for_table(self, t: str) -> str:
        return f'tbl_{underscore(t)}'

    def generate_ddl(self) -> None:
        engine = create_mock_engine(
            f'{self.dialect}://./MyDb',
            strategy='mock',
            executor= lambda sql, *multiparams, **params: print(f'{str(sql).rstrip()};'))
        schema_metadata = MetaData()
        for t in self.sqlschema.tables.values():
            cls = t.mapped_to
            sqlcols = t.columns.values()
            if len(sqlcols) > 0:
                cols = []
                for sqlcol in sqlcols:
                    slot = sqlcol.mapped_to
                    args = []
                    if sqlcol.foreign_key:
                        args = [ForeignKey(sqlcol.foreign_key.as_ddlstr())]
                    col = Column(sqlcol.name, Text(), *args, primary_key=sqlcol.is_primary_key(), nullable=slot is None or not slot.required)

                    cols.append(col)
                alchemy_tbl = Table(t.name, schema_metadata, *cols)
        print()
        schema_metadata.create_all(engine)


    def NEW_write_sqla_python_imperative(self, model_path: str) -> str:
        """
        imperative mapping:
        https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#imperative-mapping-with-dataclasses-and-attrs

        maps to the python classes generated using PythonGenerator

        ```
        output = StringIO()
        with redirect_stdout(output):
           gen.write_sqla_python_imperative()
        """
        print(f'''
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
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

from {model_path} import *

''')
        for sqltable in self.sqlschema.tables.values():
            cols = sqltable.columns.values()
            if len(cols) == 0:
                logging.warning(f'No colums for {t.name}')
                continue

            var = sqltable.as_var()
            print(f"{var} = Table('{sqltable.name}', metadata, ")

            pks = sqltable.primary_keys
            for col in cols:
                range = col.base_type
                print(f"    Column('{col.name}', {range}", end='')
                fk = col.foreign_key
                if fk is not None:
                    print(f", ForeignKey({fk.as_ddlstr()})", end='')
                if col in pks:
                    print(', primary_key=True', end='')
                print("),")
            print(")")
        for t in self.sqlschema.tables.values():
            cls = t.mapped_to
            if cls is not None:
                # non-linking table
                var = t.as_var()
                cn = camelcase(cls.name)
                print(f"mapper_registry.map_imperatively({cn}, {var}, properties={{")
                print("})")

@shared_arguments(SQLDDLGenerator)
@click.command()
@click.option("--dialect", default='sqlite', help="""
SQL-Alchemy dialect, e.g. sqlite, mysql+odbc
""")
@click.option("--sqla-file",  help="""
Path to sqlalchemy generated python
""")
@click.option("--use-foreign-keys/--no-use-foreign-keys", default=True, help="Emit FK declarations")
def cli(yamlfile, sqla_file:str = None, **args):
    """ Generate SQL DDL representation """
    gen = SQLDDLGenerator(yamlfile, **args)
    print(gen.serialize(**args))
    if sqla_file is not None:
        with open(sqla_file, "w") as stream:
            stream.write(gen.to_sqla_python())

if __name__ == '__main__':
    cli()
