from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass
from typing import Any

import click
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition, SlotDefinition
from linkml_runtime.utils.formatutils import camelcase, underscore
from linkml_runtime.utils.schemaview import SchemaView
from sqlalchemy import Column, ForeignKey, MetaData, Table, UniqueConstraint, create_mock_engine
from sqlalchemy.dialects.oracle import VARCHAR2
from sqlalchemy.types import Boolean, Date, DateTime, Enum, Float, Integer, Text, Time

from linkml._version import __version__
from linkml.transformers.relmodel_transformer import ForeignKeyPolicy, RelationalModelTransformer
from linkml.utils.generator import Generator, shared_arguments

logger = logging.getLogger(__name__)


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
    "String": Text(),
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


VARCHAR_REGEX = re.compile(r"VARCHAR2?(\((\d+)\))?")
ORACLE_MAX_VARCHAR_LENGTH = 4096


@dataclass
class SQLTableGenerator(Generator):
    """
    A :class:`~linkml.utils.generator.Generator` for creating SQL DDL.

    The basic algorithm for mapping a linkml schema S is as follows:

    - Each schema S corresponds to one database schema D (see SQLSchema)
    - Each Class C in S is mapped to a table T (see sqlalchemy.Table)
    - Each slot S in each C is mapped to a column Col (see sqlalchemy.Column)

    If the direct_mapping attribute is set to true, then no further transformations
    are applied. Note that this means:

    - inline objects are modeled as Text strings
    - multivalued fields are modeled as single Text strings

    This direct mapping is useful for simple spreadsheet/denormalized representations of complex data.
    However, for other applications, additional transformations should occur. These are:

    MULTIVALUED SLOTS

    The relational model does not have direct representation of lists. These are normalized as follows:

    If the range of the slot is a class, and there are no other slots whose range is this class,
    and the slot is for a class that has a singular primary key, then a backref is added.

    E.g. if we have User 0..* Address,
    then add a field User_id to Address.

    When SQLAlchemy bindings are created, a backref mapping is added.

    If the range of the slot is an enum or type, then a new linktable is created, and a backref added.

    E.g. if a class User has a multivalued slot alias whose range is a string,
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
    default_length_oracle: int = ORACLE_MAX_VARCHAR_LENGTH
    generate_abstract_class_ddl: bool = True

    def serialize(self, **kwargs: dict[str, Any]) -> str:
        return self.generate_ddl(**kwargs)

    def generate_ddl(self, naming_policy: SqlNamingPolicy = None, **kwargs: dict[str, Any]) -> str:
        """
        Generate a DDL using the schema in self.schema.

        :param naming_policy: naming policy for columns, defaults to None
        :type naming_policy: SqlNamingPolicy, optional
        :return: the DDL as a string
        :rtype: str
        """
        ddl_str = ""

        def dump(sql, *multiparams, **params):
            nonlocal ddl_str
            ddl_str += f"{str(sql.compile(dialect=engine.dialect)).rstrip()};"

        engine = create_mock_engine(f"{self.dialect}://./MyDb", strategy="mock", executor=dump)
        schema_metadata = MetaData()
        sqltr = RelationalModelTransformer(SchemaView(self.schema))
        if not self.use_foreign_keys:
            sqltr.foreign_key_policy = ForeignKeyPolicy.NO_FOREIGN_KEYS
        tr_result = sqltr.transform(tgt_schema_name=kwargs.get("tgt_schema_name"), top_class=kwargs.get("top_class"))
        schema = tr_result.schema

        def sql_name(n: str) -> str:
            if not naming_policy or naming_policy == SqlNamingPolicy.preserve:
                return n
            if naming_policy == SqlNamingPolicy.underscore:
                return underscore(n)
            if naming_policy == SqlNamingPolicy.camelcase:
                return camelcase(n)
            msg = f"Unknown: {naming_policy}"
            raise Exception(msg)

        def strip_newlines(txt: str | None) -> str:
            if txt is None:
                return ""
            return txt.replace("\n", "")

        # Currently SQLite dialect in SQLA does not generate comments; see
        # https://github.com/sqlalchemy/sqlalchemy/issues/1546#issuecomment-1067389172
        # As a workaround we add these as "--" comments via direct string manipulation
        include_comments = self.dialect == "sqlite"
        sv = SchemaView(schema)

        # Iterate through the attributes in each class, creating Column objects.
        # This includes generating the appropriate column name, converting the range
        # into an SQL type, and adding a foreign key notation if appropriate.
        for cn, c in schema.classes.items():
            if include_comments:
                if c.abstract:
                    ddl_str += f'-- # Abstract Class: "{cn}" Description: "{strip_newlines(c.description)}"\n'
                else:
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
                        fk = sql_name(self.get_id_or_key(s.range, sv))
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
                # convert unique_keys into a uniqueness constraint for the table
                for uc in c.unique_keys.values():
                    sql_names = [sql_name(sn) if sn in c.attributes else None for sn in uc.unique_key_slots]
                    if any(sn is None for sn in sql_names):
                        continue
                    sql_uc = UniqueConstraint(*sql_names)
                    cols.append(sql_uc)
            if not c.abstract or (c.abstract and self.generate_abstract_class_ddl):
                Table(sql_name(cn), schema_metadata, *cols, comment=str(c.description))
        schema_metadata.create_all(engine)
        return ddl_str

    def get_oracle_sql_range(self, slot: SlotDefinition) -> Text | VARCHAR2 | None:
        """
        Generate the appropriate range for Oracle SQL.

        :param slot: the slot under examination
        :type slot: SlotDefinition
        :return: appropriate type for Oracle SQL or None
        :rtype: Text | VARCHAR2 | None
        """
        slot_range = slot.range
        if not slot_range:
            return None

        if slot_range.lower() in ["str", "string"]:
            # string type data should be represented as a VARCHAR2
            return VARCHAR2(self.default_length_oracle)

        # check whether the slot range matches the regex "VARCHAR2?(\((\d+)\))?"
        match = re.match(VARCHAR_REGEX, slot_range)
        if match:
            # match.group(2) is the digits in brackets after VARCHAR
            # i.e. a defined length for the VARCHAR
            if match.group(2) and int(match.group(2)) > ORACLE_MAX_VARCHAR_LENGTH:
                msg = (
                    "Warning: range exceeds maximum Oracle VARCHAR length, "
                    f"CLOB type will be returned: {slot_range} for {slot.name} = {slot.range}"
                )
                logger.info(msg)
                return Text()
            # set the length to either the varchar length (as defined in the slot_range)
            # or the default
            return VARCHAR2(match.group(2) or self.default_length_oracle)

        # use standard SQL range matching for anything else
        return None

    def get_sql_range(self, slot: SlotDefinition, schema: SchemaDefinition = None):
        """Get the slot range as a SQL Alchemy column type."""
        slot_range = slot.range

        if self.dialect == "oracle":
            range_type = self.get_oracle_sql_range(slot)
            if range_type:
                return range_type

        if slot_range is None:
            return Text()

        # if no SchemaDefinition is explicitly provided as an argument
        # then simply use the schema that is provided to the SQLTableGenerator() object
        if not schema:
            schema = self.schema

        sv = SchemaView(schema)
        if slot_range in sv.all_classes():
            # FK type should be the same as the identifier of the foreign key
            fk = sv.get_identifier_slot(slot_range)
            if fk:
                return self.get_sql_range(fk, sv.schema)
            return Text()

        if slot_range in sv.all_enums():
            e = sv.all_enums()[slot_range]
            if e.permissible_values is not None:
                vs = [str(v) for v in e.permissible_values]
                return Enum(name=e.name, *vs)

        if slot_range in METAMODEL_TYPE_TO_BASE:
            range_base = METAMODEL_TYPE_TO_BASE[slot_range]
        elif slot_range in sv.all_types():
            range_base = sv.all_types()[slot_range].base
        else:
            logger.error(f"Unknown range: {slot_range} for {slot.name} = {slot.range}")
            return Text()

        if range_base in RANGEMAP:
            return RANGEMAP[range_base]

        logger.error(f"Unknown range base: {range_base} for {slot.name} = {slot.range}")
        return Text()

    @staticmethod
    def get_id_or_key(cn: str, sv: SchemaView) -> str:
        """Given a named class, retrieve the identifier or key slot."""
        pk = sv.get_identifier_slot(cn, use_key=True)
        if pk is None:
            msg = f"No PK for {cn}"
            raise Exception(msg)
        pk_name = pk.alias if pk.alias else pk.name
        return f"{cn}.{pk_name}"


@shared_arguments(SQLTableGenerator)
@click.command(name="sqltables")
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
@click.option(
    "--default_length_oracle",
    default=ORACLE_MAX_VARCHAR_LENGTH,
    show_default=True,
    help="Default length of varchar based arguments for oracle dialects",
)
@click.option(
    "--generate_abstract_class_ddl",
    default=True,
    show_default=True,
    help="A manual override to omit the abstract classes, set to true as a default for testing sake",
)
@click.version_option(__version__, "-V", "--version")
def cli(
    yamlfile: str,
    relmodel_output: str,
    sqla_file: str | None = None,
    python_import: str = None,
    dialect: str | None = None,
    use_foreign_keys: bool = True,
    **args,
):
    """Generate SQL DDL representation."""
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
