import os
from typing import Union, TextIO, Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import click
import logging
from contextlib import redirect_stdout

from sqlalchemy import *
from linkml_runtime.linkml_model.meta import ClassDefinition, SlotDefinition, SchemaDefinition, ClassDefinitionName, SlotDefinitionName
from linkml_runtime.utils.formatutils import underscore, camelcase
from linkml.utils.generator import Generator, shared_arguments

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
    'URI': Text(),
    'XSDTime': Time(),
    'XSDDateTime': DateTime(),
    'XSDDate': Date(),
}

def _quote(s: str) -> str:
    s = s.replace("'", "\\'")
    return f"'{s}'"

@dataclass
class Backref():
    original_column: "SQLColumn"
    backref_column: "SQLColumn"
    order_by: str = None


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
    mapped_to_alias: str = None
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
    backrefs: List[Backref ] = field(default_factory=list)

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
    def remove_column(self, c):
        del self.columns[c.name]

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

    The basic algorithm for mapping a linkml schema S is as follows:

     - Each schema S corresponds to one database schema D (see SQLSchema)
     - Each Class C in S is mapped to a table T (see SQLTable)
     - Each slot S in each C is mapped to a column Col (see SQLColumn)

    if the direct_mapping attribute is set to true, then no further transformations
    are applied. Note that this means:

     - inline objects are modeled as Text strings
     - multivalued fields are modeled as single Text strings

    this direct mapping is useful for simple spreadsheet/denormalized representations of complex data.
    however, for other applications, additional transformations should occur. these are:

    MULTIVALUED SLOTS

    The relational model does not have direct representation of lists. These are normalized as follows.

    If the range of the slot is a class, and there are no other slots whose range is this class,
    and the slot is for a class that has a singular primary key, then a backref is added.

    E.g. if we have User 0..* Address,
    then add a field User_id to Address.

    When SQLAlchemy bindings are created, a backref mapping is added

    If the range of the slot is an enum or type, then a new linktable is created, and a backref added

    E.g. if a class User has a multivalues slot alias whose range is a string,
    then create a table user_aliases, with two columns (1) alias [a string] and (2) a backref to user

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
    sqlschema: SQLSchema = SQLSchema()

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

    def _is_hidden(self, cls: ClassDefinition) -> bool:
        if cls.mixin or cls.abstract:
            return True

    def _class_name_to_table(self, cn: ClassDefinitionName) -> str:
        """
        https://stackoverflow.com/questions/1881123/table-naming-underscore-vs-camelcase-namespaces-singular-vs-plural
        """
        return underscore(cn)

    def end_schema(self, **kwargs) -> None:
        self._transform_sqlschema()
        self.generate_ddl()

    def visit_class(self, cls: ClassDefinition) -> bool:
        if self._is_hidden(cls):
            return False
        if cls.description:
            None ## TODO
        tname = self._class_name_to_table(cls.name)
        # add table
        self.sqlschema.tables[tname] = SQLTable(name=tname, mapped_to=cls)
        return True

    def end_class(self, cls: ClassDefinition) -> None:
        if self._is_hidden(cls):
            return False
        if self.use_inherits and cls.is_a:
            # postgresql supports inheritance
            # if you want to use plain SQL DDL then use sqlutils to unfold hierarchy
            # TODO: raise error if the target is standard SQL
            raise Exception(f'PostgreSQL Inheritance not yet supported')


    def visit_class_slot(self, cls: ClassDefinition, aliased_slot_name: str, slot: SlotDefinition) -> None:
        if self._is_hidden(cls):
            return False
        sqlschema = self.sqlschema
        #qual = 'repeated ' if slot.multivalued else 'optional ' if not slot.required or slot.key else ''
        colname = underscore(aliased_slot_name)
        sqltable = sqlschema.get_table_by_class_name(cls.name)
        slot_range = self.get_sql_range(slot)
        is_pk = slot.identifier
        sqlcol: SQLColumn
        sqlcol = SQLColumn(name=colname, mapped_to=slot,
                           mapped_to_alias=aliased_slot_name,
                           is_singular_primary_key=is_pk, description=slot.description,
                           table=sqltable)
        sqltable.columns[colname] = sqlcol
        sqlcol.base_type = slot_range

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
            is_primitive = ref is None
            #basic_type = 'Text'
            table_pk = table.get_singular_primary_key()
            if slot.multivalued:
                if is_primitive and table_pk is not None:
                    # primitive base type:
                    # create a linking table
                    linktable_name = f'{table.name}_{sqlcol.name}'
                    backref_col_name = 'backref_id'
                    linktable = SQLTable(name=linktable_name)
                    linktable.add_column(SQLColumn(name=backref_col_name, foreign_key=table_pk))
                    linktable.add_column(sqlcol)
                    sqlschema.add_table(linktable)
                    table.remove_column(sqlcol)
                if not is_primitive and table_pk is not None and len(ref.referenced_by) == 1:
                    # e.g. user->addresses
                    backref_col_name = f'{table.name}_{table_pk.name}'
                    backref_col = SQLColumn(name=backref_col_name, foreign_key=table_pk)
                    ref.add_column(backref_col)
                    table.remove_column(sqlcol)
                    table.backrefs.append(Backref(original_column=sqlcol, backref_column=backref_col))
            else:
                if not is_primitive:
                    ref_pk = ref.get_singular_primary_key()
                    if ref_pk is not None:
                        sqlcol.foreign_key=ref_pk
                    else:
                        logging.error(f'No PK for {ref.name}')
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
                return Enum(name=e.name, *vs)
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

    def _get_sqla_var_for_table(self, t: str) -> str:
        return f'tbl_{underscore(t)}'

    def generate_ddl(self) -> None:
        def dump(sql, *multiparams, **params):
            print(f"{str(sql.compile(dialect=engine.dialect)).rstrip()};")
        engine = create_mock_engine(
            f'{self.dialect}://./MyDb',
            strategy='mock',
            executor= dump)
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
                    col = Column(sqlcol.name, sqlcol.base_type, *args, primary_key=sqlcol.is_primary_key(), nullable=slot is None or not slot.required)

                    cols.append(col)
                alchemy_tbl = Table(t.name, schema_metadata, *cols)
        print()
        schema_metadata.create_all(engine)


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
from sqlalchemy import Integer
from sqlalchemy.orm import registry
from sqlalchemy.orm import relationship

mapper_registry = registry()
metadata = MetaData()

from {model_path} import *

''')
        for sqltable in self.sqlschema.tables.values():
            cols = sqltable.columns.values()
            if len(cols) == 0:
                logging.warning(f'No columns for {t.name}')
                continue

            var = sqltable.as_var()
            print(f"{var} = Table('{sqltable.name}', metadata, ")

            pks = sqltable.primary_keys
            for col in cols:
                #range = col.base_type
                range = 'Text'
                #if isinstance(col.base_type, Integer):
                #    range = 'Integer'
                print(f"    Column('{col.name}', {range}", end='')
                fk = col.foreign_key
                if fk is not None:
                    print(f", ForeignKey('{fk.as_ddlstr()}')", end='')
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
                for backref in t.backrefs:
                    original_col = backref.original_column
                    backref_slot = original_col.mapped_to
                    backref_slot_range = camelcase(backref_slot.range)
                    print(f"""
    '{underscore(original_col.mapped_to_alias)}': 
        relationship({backref_slot_range}, 
                      foreign_keys={backref.backref_column.table.as_var()}.columns["{backref.backref_column.name}"],
                      backref='{cn}'),
""")
                print("})")

@shared_arguments(SQLDDLGenerator)
@click.command()
@click.option("--dialect", default='sqlite', help="""
SQL-Alchemy dialect, e.g. sqlite, mysql+odbc
""")
@click.option("--sqla-file",  help="""
Path to sqlalchemy generated python
""")
@click.option("--python-import",  help="""
Python import header for generated sql-alchemy code
""")
@click.option("--direct-mapping/--no-direct-mapping", default=False, help="""
Map classes directly to 
""")
@click.option("--use-foreign-keys/--no-use-foreign-keys", default=True, help="Emit FK declarations")
def cli(yamlfile, sqla_file:str = None, python_import: str = None, **args):
    """ Generate SQL DDL representation """
    gen = SQLDDLGenerator(yamlfile, **args)
    print(gen.serialize(**args))
    if sqla_file is not None:
        if python_import is None:
            python_import = gen.schema.name
        with open(sqla_file, "w") as stream:
            with redirect_stdout(stream):
                gen.write_sqla_python_imperative(python_import)

if __name__ == '__main__':
    cli()
