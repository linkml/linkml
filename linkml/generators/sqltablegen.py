import logging
import os
from dataclasses import dataclass
from typing import Optional

import click
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy import Column, ForeignKey, MetaData, Table, UniqueConstraint, create_mock_engine
from sqlalchemy.types import Boolean, Date, DateTime, Enum, Float, Integer, Text, Time

from linkml._version import __version__
from linkml.transformers.relmodel_transformer import ForeignKeyPolicy, RelationalModelTransformer
from linkml.utils.generator import Generator, shared_arguments
from linkml.utils.schemaloader import SchemaLoader


class SqlNamingPolicy(Enum):
    preserve = "preserve"
    underscore = "underscore"
    camelcase = "camelcase"


# TODO: move this up
METAMODEL_TYPE_TO_BASE = {
    "string": "str",
    "integer": "int",
    "boolean": "Bool",
    "float": "float",
    "double": "double",
    "decimal": "Decimal",
    "time": "XSDTime",
    "date": "XSDDate",
    "datetime": "XSDDateTime",
    "uriorcurie": "URIorCURIE",
    "uri": "URI",
    "ncname": "NCName",
    "objectidentifier": "ElementIdentifier",
    "nodeidentifier": "NodeIdentifier",
}

RANGEMAP = {
    "str": Text(),
    "string": Text(),
    "NCName": Text(),
    "URIorCURIE": Text(),
    "int": Integer(),
    "Decimal": Integer(),
    "double": Float(),
    "float": Float(),
    "Bool": Boolean(),
    "URI": Text(),
    "XSDTime": Time(),
    "XSDDateTime": DateTime(),
    "XSDDate": Date(),
}


@dataclass
class SQLTableGenerator(Generator):
    """
    A :class:`~linkml.utils.generator.Generator` for creating SQL DDL

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

    * If R is a type, and the slot is NOT multivalued, do a direct type conversion
    * If R is a type, and the slot is multivalued:

        * do not include the mapped column
        * create a new table T_S, with 2 columns: S, and a backref to T

    ranges that are classes:

    * Ref = map_class_to_table(R)
    * if R is a class, and the slot is NOT multivalued, and Ref has a singular primary key:

        * Col.type = ForeignKey(Ref.PK)

    * if R is a class, and the slot is NOT multivalued, and Ref has NO singular primary key:

        * add a foreign key C.pk to Ref
        * add a backref C.S => Ref, C.pk
        * remove Col from T

    * If R is a class, and the slot IS multivalued

    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    generatorversion = "0.1.1"
    valid_formats = ["sql"]
    file_extension = "sql"
    uses_schemaloader = False

    # ObjectVars
    use_inherits: bool = False  # postgresql supports inheritance
    dialect: str = "sqlite"
    inject_primary_keys: bool = True
    use_foreign_keys: bool = True
    rename_foreign_keys: bool = False
    direct_mapping: bool = False
    relative_slot_num: bool = False

    def serialize(self, **kwargs) -> str:
        return self.generate_ddl(**kwargs)

    def generate_ddl(self, naming_policy: SqlNamingPolicy = None, **kwargs) -> str:
        ddl_str = ""

        def dump(sql, *multiparams, **params):
            nonlocal ddl_str
            ddl_str += f"{str(sql.compile(dialect=engine.dialect)).rstrip()};"

        engine = create_mock_engine(f"{self.dialect}://./MyDb", strategy="mock", executor=dump)
        schema_metadata = MetaData()
        sqltr = RelationalModelTransformer(SchemaView(self.schema))
        if not self.use_foreign_keys:
            sqltr.foreign_key_policy = ForeignKeyPolicy.NO_FOREIGN_KEYS
        tr_result = sqltr.transform(
            tgt_schema_name=kwargs.get("tgt_schema_name", None), top_class=kwargs.get("top_class", None)
        )
        schema = tr_result.schema

        def sql_name(n: str) -> str:
            if naming_policy is not None:
                if naming_policy == SqlNamingPolicy.underscore:
                    return underscore(n)
                elif naming_policy == SqlNamingPolicy.camelcase:
                    return camelcase(n)
                elif naming_policy == SqlNamingPolicy.preserve:
                    return n
                else:
                    raise Exception(f"Unknown: {naming_policy}")
            else:
                return n

        def strip_newlines(txt: Optional[str]) -> str:
            if txt is None:
                return ""
            return txt.replace("\n", "")

        # Currently SQLite dialect in SQLA does not generate comments; see
        # https://github.com/sqlalchemy/sqlalchemy/issues/1546#issuecomment-1067389172
        # As a workaround we add these as "--" comments via direct string manipulation
        include_comments = self.dialect == "sqlite"
        sv = SchemaView(schema)
        for cn, c in schema.classes.items():
            if include_comments:
                ddl_str += f'-- # Class: "{cn}" Description: "{strip_newlines(c.description)}"\n'
            pk_slot = sv.get_identifier_slot(cn)
            if c.attributes:
                cols = []
                for sn, s in c.attributes.items():
                    is_pk = "primary_key" in s.annotations
                    if pk_slot:
                        is_pk = sn == pk_slot.name
                    # else:
                    #    is_pk = True  ## TODO: use unique key
                    args = []
                    if s.range in schema.classes and self.use_foreign_keys:
                        fk = sql_name(self.get_foreign_key(s.range, sv))
                        args = [ForeignKey(fk)]
                    field_type = self.get_sql_range(s, schema)
                    col = Column(
                        sql_name(sn),
                        field_type,
                        *args,
                        primary_key=is_pk,
                        nullable=not s.required,
                    )
                    if include_comments:
                        ddl_str += f"--     * Slot: {sn} Description: {strip_newlines(s.description)}\n"
                    if s.description:
                        col.comment = s.description
                    cols.append(col)
                for uc_name, uc in c.unique_keys.items():

                    def _sql_name(sn: str):
                        if sn in c.attributes:
                            return sql_name(sn)
                        else:
                            # for candidate in c.attributes.values():
                            #    if "original_slot" in candidate.annotations:
                            #        original = candidate.annotations["original_slot"]
                            #        if original.value == sn:
                            #            return sql_name(candidate.name)
                            return None

                    sql_names = [_sql_name(sn) for sn in uc.unique_key_slots]
                    if any(sn is None for sn in sql_names):
                        continue
                    sql_uc = UniqueConstraint(*sql_names)
                    cols.append(sql_uc)
                Table(sql_name(cn), schema_metadata, *cols, comment=str(c.description))
        schema_metadata.create_all(engine)
        return ddl_str

    def get_sql_range(self, slot: SlotDefinition, schema: SchemaDefinition = None):
        """
        returns a SQL Alchemy column type
        """
        range = slot.range

        # if no SchemaDefinition is explicitly provided as an argument
        # then simply use the schema that is provided to the SQLTableGenerator() object
        if not schema:
            schema = SchemaLoader(data=self.schema).resolve()

        if range in schema.classes:
            # FK type should be the same as the identifier of the foreign key
            fk = SchemaView(schema).get_identifier_slot(range)
            if fk:
                return self.get_sql_range(fk, schema)
            else:
                return Text()
        if range in schema.enums:
            e = schema.enums[range]
            if e.permissible_values is not None:
                vs = [str(v) for v in e.permissible_values]
                return Enum(name=e.name, *vs)
        if range in METAMODEL_TYPE_TO_BASE:
            range_base = METAMODEL_TYPE_TO_BASE[range]
        elif range in schema.types:
            range_base = schema.types[range].base
        elif range is None:
            return Text()
        else:
            logging.error(f"Unknown range: {range} for {slot.name} = {slot.range}")
            return Text()
        if range_base in RANGEMAP:
            return RANGEMAP[range_base]
        else:
            logging.error(f"UNKNOWN range base: {range_base} for {slot.name} = {slot.range}")
            return Text()

    @staticmethod
    def get_foreign_key(cn: str, sv: SchemaView) -> str:
        pk = sv.get_identifier_slot(cn)
        # TODO: move this to SV
        if pk is None:
            for sn in sv.class_slots(cn):
                s = sv.induced_slot(sn, cn)
                if s.key:
                    pk = s
                    break
        if pk is None:
            raise Exception(f"No PK for {cn}")
        if pk.alias:
            pk_name = pk.alias
        else:
            pk_name = pk.name
        return f"{cn}.{pk_name}"


@shared_arguments(SQLTableGenerator)
@click.command()
@click.option(
    "--dialect",
    default="sqlite",
    show_default=True,
    help="SQL-Alchemy dialect, e.g. sqlite, mysql+odbc",
)
@click.option("--sqla-file", help="Path to sqlalchemy generated python")
@click.option(
    "--relmodel-output",
    help="Path to intermediate LinkML YAML of transformed relational model",
)
@click.option("--python-import", help="Python import header for generated sql-alchemy code")
@click.option(
    "--use-foreign-keys/--no-use-foreign-keys",
    default=True,
    show_default=True,
    help="Emit FK declarations",
)
@click.version_option(__version__, "-V", "--version")
def cli(
    yamlfile,
    relmodel_output,
    sqla_file: str = None,
    python_import: str = None,
    dialect=None,
    use_foreign_keys=True,
    **args,
):
    """Generate SQL DDL representation"""
    if relmodel_output:
        sv = SchemaView(yamlfile)
        rtr = RelationalModelTransformer(sv)
        if not use_foreign_keys:
            rtr.foreign_key_policy = ForeignKeyPolicy.NO_FOREIGN_KEYS
        rtr_result = rtr.transform("foo")
        relmodel_schema = rtr_result.schema
        yaml_dumper.dump(relmodel_schema, to_file=relmodel_output)
    gen = SQLTableGenerator(yamlfile, use_foreign_keys=use_foreign_keys, **args)
    if dialect:
        gen.dialect = dialect
    print(gen.generate_ddl())
    if sqla_file is not None:
        raise NotImplementedError("SQLAGen not implemented")


if __name__ == "__main__":
    cli()
