import os
from typing import Union, TextIO, Dict, List, Tuple, Optional
from dataclasses import dataclass
import click
import logging

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
    'URI': Text()
}

def _quote(s: str) -> str:
    s = s.replace("'", "\\'")
    return f"'{s}'"

@dataclass
class Backref:
    """
    for a class C with multivalued slot S with range R
    (e.g C = user, S = addresses, R = Address)

    """
    backref_to_table: TABLENAME  ## tbl(C)
    relationship_to_class: ClassDefinitionName ## R
    slot: SlotDefinitionName ## col(C.S)
    secondary: Optional[TABLENAME] ## for many-to-many



@dataclass
class SQLMapping:
    """
    Holds an ORM mapping between a table/column and a class/slot
    """
    table_name: TABLENAME = None
    column_name: COLNAME = None
    class_name: ClassDefinitionName = None
    slot_name: SlotDefinitionName = None
    schema: SchemaDefinition = None

@dataclass
class ForeignKeyMapping:
    """
    Holds a pairing of a Foreign Key at the SQL level and a class/slot/range/pk at the LinkML class level
    """
    source: SQLMapping
    target: SQLMapping


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
    backrefs: Dict[TABLENAME, Backref] = {}

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
        self.mappings : List[SQLMapping] = []
        self.foreign_key_mappings : List[ForeignKeyMappings] = []
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
        if cls.mixin or cls.abstract or not cls.slots:
            return False

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
        engine = create_mock_engine(
            f'{self.dialect}://./MyDb',
            strategy='mock',
            executor= lambda sql, *multiparams, **params: print(f'{str(sql).rstrip()};'))
        schema_metadata = MetaData()
        for t, colmap in self.columns.items():
            cls = self.table_to_class.get(t, None)
            cols = colmap.values()
            if len(cols) > 0:
                tbl = Table(t, schema_metadata, *cols)
                if cls is None:
                    tbl.comment = 'Autogenerated linking table'
                else:
                    if cls.description:
                        tbl.comment = cls.description
                    else:
                        tbl.comment = f"Autogenerated from class: {cls.name}"
                sqla_lines = ['',
                    f'class {camelcase(t)}(Base):']
                if cls is not None:
                    desc = cls.description
                    if desc is not None and desc != '':
                        sqla_lines += [
                            '    """',
                            f'    {desc}',
                            '    """'
                        ]
                sqla_lines.append(
                    f"    __tablename__ = '{t}'")
                pks = [col for col in cols if col.primary_key]
                for col in cols:
                    args = ['Text']
                    if len(pks) == 0 or col.primary_key:
                        args.append('primary_key=True')
                    argstr = ", ".join(args)
                    line = f'    {underscore(col.name)} = Column({argstr})'
                    sqla_lines.append(line)
                self.sqla_python_lines += sqla_lines
        # Add comments at top (note most sqla generators do not support comments)
        for tn,t in schema_metadata.tables.items():
            if tn in self.table_to_class:
                cls = self.table_to_class[tn]
                if t.comment is not None:
                    cmt = t.comment.replace("\n","")
                else:
                    cmt = ''
                print(f'-- {tn} // {cmt}')
            for c in t.columns:
                if c.comment is not None:
                    cmt = c.comment.replace("\n","")
                else:
                    cmt = ''
                print(f'--   {c} // {cmt}')
        print()
        schema_metadata.create_all(engine)

    def visit_class(self, cls: ClassDefinition) -> bool:
        if self._is_hidden(cls):
            return False
        if cls.description:
            None ## TODO
        tname = self._class_name_to_table(cls.name)
        self.columns[tname] = {}
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
        #qual = 'repeated ' if slot.multivalued else 'optional ' if not slot.required or slot.key else ''
        colname = self._slot_name_to_column(aliased_slot_name)
        tname = self._class_name_to_table(cls.name)
        mapping = SQLMapping(table_name=tname, column_name=colname)
        slot_range = self.get_sql_range(slot)
        is_pk = slot.identifier
        if isinstance(slot_range, ForeignKey) and not self.use_foreign_keys:
            slot_range = Text()
        if isinstance(slot_range, ForeignKey) and self.use_foreign_keys and self.rename_foreign_keys:
            colname = f'{colname}_id'
        print(f'-- SLOT RANGE FOR {tname}.{colname} = {slot_range} // {self.use_foreign_keys}')

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
            if tname not in self.backrefs:
                self.backrefs[tname] = {}
            #self.backrefs[tname][slotname] = Backref(backref_to_table='x')
            #self.table_to_class[linktable_name] = ClassDefinition(name=linktable_name)
        else:
            col = Column(colname, slot_range, primary_key=is_pk, nullable=not slot.required)
            if slot.description:
                col.comment = slot.description
            self.columns[tname][colname] = col
            self.table_columns_to_slot[(tname, colname)] = slot
        self.mappings.append(mapping)

    def get_sql_range(self, slot: SlotDefinition):
        """
        returns a SQL Alchemy column type
        """
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
            print(f'-- translating ramge {range} / PKs = {pk}')
            if pk is not None:
                if self._is_hidden(rc):
                    logging.error(f"Creating non-FK ref for {slot.name} {pk}")
                    return Text()
                else:
                    return ForeignKey(f'{self._slot_name_to_column(range)}.{pk}')
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
                if t in self.backrefs:
                    for backref in self.backrefs[t]:
                        printf(f"    ''")
                print("})")

    def _get_primary_keys(self, t: str) -> List:
        cols = self.columns[t].values()
        pks = [col for col in cols if col.primary_key]
        if len(pks) == 0:
            pks = cols
        return pks

    def _get_sqla_var_for_table(self, t: str) -> str:
        return f'tbl_{underscore(t)}'


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
