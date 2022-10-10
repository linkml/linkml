import csv
import inspect
import logging
import os
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any, List, Optional, Type, Union

import click
import linkml_runtime.linkml_model.meta as metamodel
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import PermissibleValue, SchemaDefinition
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.associationproxy import _AssociationCollection
from sqlalchemy.orm import sessionmaker

from linkml.generators.pythongen import PythonGenerator
from linkml.generators.sqlalchemygen import SQLAlchemyGenerator, TemplateEnum
from linkml.generators.sqltablegen import SQLTableGenerator
from linkml.utils import datautils, validation
from linkml.utils.datautils import (_get_format, _is_xsv, dumpers_loaders,
                                    get_dumper, get_loader, infer_root_class)


@dataclass
class SQLStore:
    """
    A wrapper for a SQLLite database.

    This provides two core operations for storing and retrieving data

    - :meth:`dump`
    - :meth:`load`

    The wrapper transparently will take care of:

    - mapping your LinkML schema into SQL Tables
    - creating a SQL Alchemy ORM layer
    - mapping your data/objects in any LinkML compliant data format (json. yaml, rdf) into ORM objects
    """

    schema: Union[str, SchemaDefinition] = None
    schemaview: SchemaView = None
    engine: Engine = None
    database_path: str = None
    module: ModuleType = None
    native_module: ModuleType = None
    include_schema_in_database: bool = None

    def db_exists(self, create=True, force=False) -> str:
        """
        check if database exists, optionally create if not present

        :param create: create if does not exist
        :param force: recreate database, destroying any content if previously present
        :return: path
        """
        if not self.database_path:
            raise ValueError(f"database_path not set")
        db_exists = os.path.exists(self.database_path)
        if force or (create and not db_exists):
            if force:
                Path(self.database_path).unlink(missing_ok=True)
            self.engine = create_engine(f"sqlite:///{self.database_path}")
            con = sqlite3.connect(self.database_path)
            cur = con.cursor()
            ddl = SQLTableGenerator(self.schema).generate_ddl()
            cur.executescript(ddl)
            if self.include_schema_in_database:
                metamodel_sv = package_schemaview(metamodel.__name__)
                meta_ddl = SQLTableGenerator(metamodel_sv.schema).generate_ddl()
                cur.executescript(ddl)
        if not os.path.exists(self.database_path):
            raise ValueError(f"No database: {self.database_path}")
        return self.database_path

    def compile(self) -> ModuleType:
        """
        Compile SQLAlchemy object model

        Uses Declarative by default.

        Note that the SQLA model is different from the native dataclass model

        :return: compiled module
        """
        gen = SQLAlchemyGenerator(self.schema)
        self.module = gen.compile_sqla(template=TemplateEnum.DECLARATIVE)
        if self.schemaview is None:
            self.schemaview = SchemaView(self.schema)
        return self.module

    def compile_native(self) -> ModuleType:
        """
        Compile native python object model

        :return: compiled module
        """
        gen = PythonGenerator(yaml_dumper.dumps(self.schema))
        self.native_module = gen.compile_module()
        return self.native_module

    def load(self, target_class: Union[str, Type[YAMLRoot]] = None) -> YAMLRoot:
        """
        Loads a LinkML object from the wrapped SQLite database

        :param target_class:
        :return:
        """
        return self.load_all(target_class=target_class)[0]

    def load_all(
        self, target_class: Union[str, Type[YAMLRoot]] = None
    ) -> List[YAMLRoot]:
        if target_class == None:
            target_class_name = infer_root_class(self.schemaview)
            target_class = self.native_module.__dict__[target_class_name]
        if self.engine is None:
            self.engine = create_engine(f"sqlite:///{self.database_path}")
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        typ = self.to_sqla_type(target_class)
        q = session.query(typ)
        all_objs = q.all()
        return self.from_sqla(all_objs)

    def dump(self, element: YAMLRoot, append=True) -> None:
        """
        Store an element in the database

        :param element:
        :param append:
        :return:
        """
        if self.engine is None:
            raise ValueError(f"Must set self.engine")
        session_class = sessionmaker(bind=self.engine)
        session = session_class()
        nu_obj = self.to_sqla(element)
        if not append:
            session.query(type(nu_obj)).delete()
        session.add(nu_obj)
        session.commit()

    def to_sqla_type(self, target_class: Type[YAMLRoot]) -> Any:
        for n, nu_typ in inspect.getmembers(self.module):
            if n == target_class.__name__:
                return nu_typ
        raise ValueError(f"Could not find: {target_class}")

    def from_sqla_type(self, typ) -> Any:
        for n, nu_typ in inspect.getmembers(self.native_module):
            if n == typ.__name__:
                return nu_typ
        raise ValueError(f"Could not find: {typ}")

    def to_sqla(self, obj: Union[YAMLRoot, list]) -> Any:
        """
        Translate native LinkML object to SQLAlchemy declarative module

        :param obj:
        :return:
        """
        if self.module is None:
            self.compile()
        if isinstance(obj, list):
            nu_obj = [self.to_sqla(x) for x in obj]
            if nu_obj:
                return nu_obj
            else:
                return None
        elif isinstance(obj, dict):
            nu_obj = {}
            for k, v in obj.items():
                v2 = self.to_sqla(v)
                if v2 is not None:
                    nu_obj[k] = v2
            if nu_obj:
                return nu_obj
            else:
                return None
        # elif isinstance(obj, PermissibleValue):
        #    return str(obj.text)
        elif isinstance(obj, EnumDefinitionImpl):
            return str(obj)
        elif isinstance(obj, YAMLRoot) or isinstance(obj, BaseModel):
            typ = type(obj)
            inst_args = {}
            for k, v in vars(obj).items():
                v2 = self.to_sqla(v)
                if v2 is not None:
                    inst_args[k] = v2
            for n, nu_typ in inspect.getmembers(self.module):
                # TODO: make more efficient
                if n == typ.__name__:
                    # print(f'Creating {nu_typ} from: {inst_args}')
                    nu_obj = nu_typ(**inst_args)
                    return nu_obj
            raise ValueError(f"Cannot find {typ.__name__} in {self.module}")
        else:
            return obj

    def from_sqla(self, obj: Any) -> Optional[Union[YAMLRoot, List[YAMLRoot]]]:
        """
        Translate from SQLAlchemy declarative module to native LinkML

        :param obj: sqla object
        :return: native dataclass object
        """
        if self.schemaview is None:
            self.schemaview = SchemaView(self.schema)
        typ = type(obj)
        nm = self.schemaview.class_name_mappings()
        if typ.__name__ in nm:
            cls = nm[typ.__name__]
        else:
            cls = None
        try:
            kvs = vars(obj).items()
        except TypeError:
            kvs = None
        if isinstance(obj, list) or isinstance(obj, _AssociationCollection):
            nu_obj = [self.from_sqla(x) for x in obj]
            if nu_obj:
                return nu_obj
            else:
                return None
        elif cls:
            nu_cls = self.from_sqla_type(typ)
            inst_args = {}
            for sn in self.schemaview.class_slots(cls.name):
                sn = underscore(sn)
                v = getattr(obj, sn, None)
                v2 = self.from_sqla(v)
                if v2 is not None and v2 != [] and v2 != {}:
                    inst_args[sn] = v2
            for n, nu_typ in inspect.getmembers(self.native_module):
                # TODO: make more efficient
                if n == typ.__name__:
                    # print(f'CREATING {nu_typ} FROM {inst_args}')
                    nu_obj = nu_typ(**inst_args)
                    # print(f'CREATED {nu_obj}')
                    return nu_obj
            raise ValueError(f"Cannot find {typ.__name__} in {self.native_module}")
        else:
            return obj


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.option(
    "--csv-field-size-limit",
    type=int,
    help="""
              Increase the default limit for maximum field size.
              See https://docs.python.org/3/library/csv.html#csv.field_size_limit""",
)
def main(verbose: int, quiet: bool, csv_field_size_limit: int):
    """Run the LinkML SQL CLI."""
    if verbose >= 2:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose == 1:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)
    if quiet:
        logging.basicConfig(level=logging.ERROR)
    if csv_field_size_limit:
        csv.field_size_limit(csv_field_size_limit)


@main.command()
@click.option("--module", "-m", help="Path to python datamodel module")
@click.option("--db", "-D", help="Path to SQLite database file")
@click.option(
    "--input-format",
    "-f",
    type=click.Choice(list(dumpers_loaders.keys())),
    help="Input format. Inferred from input suffix if not specified",
)
@click.option(
    "--target-class",
    "-C",
    help="name of class in datamodel that the root node instantiates",
)
@click.option(
    "--index-slot", "-S", help="top level slot. Required for CSV dumping/loading"
)
@click.option("--schema", "-s", help="Path to schema specified as LinkML yaml")
@click.option(
    "--validate/--no-validate",
    default=True,
    show_default=True,
    help="Validate against the schema",
)
@click.option(
    "--force/--no-force",
    default=True,
    show_default=True,
    help="Force creation of a database if it does not exist",
)
@click.argument("input")
def dump(
    input,
    module,
    db,
    target_class,
    input_format=None,
    schema=None,
    validate=None,
    force: bool = None,
    index_slot=None,
) -> None:
    """
    Dumps data to a SQL store

    Examples:

        linkml-sqldb dump -s personinfo.yaml -D my_person_database.db personinfo_data01.yaml
    """
    if module is None:
        if schema is None:
            raise Exception("must pass one of module OR schema")
        else:
            python_module = PythonGenerator(schema).compile_module()
    else:
        python_module = compile_python(module)
    if schema is not None:
        sv = SchemaView(schema)
    if target_class is None:
        if sv is None:
            raise ValueError(f"Must specify schema if not target class is specified")
        target_class = infer_root_class(sv)
    if target_class is None:
        raise Exception(f"target class not specified and could not be inferred")
    py_target_class = python_module.__dict__[target_class]
    input_format = _get_format(input, input_format)
    loader = get_loader(input_format)

    inargs = {}
    if datautils._is_rdf_format(input_format):
        if sv is None:
            raise Exception(f"Must pass schema arg")
        inargs["schemaview"] = sv
        inargs["fmt"] = input_format
    if _is_xsv(input_format):
        if index_slot is None:
            index_slot = infer_index_slot(sv, target_class)
            if index_slot is None:
                raise Exception("--index-slot is required for CSV input")
        inargs["index_slot"] = index_slot
        inargs["schema"] = schema
    obj = loader.load(source=input, target_class=py_target_class, **inargs)
    if validate:
        if schema is None:
            raise Exception(
                "--schema must be passed in order to validate. Suppress with --no-validate"
            )
        # TODO: use validator framework
        validation.validate_object(obj, schema)

    endpoint = SQLStore(schema, database_path=db, include_schema_in_database=False)
    endpoint.native_module = python_module
    endpoint.db_exists(force=force)
    endpoint.compile()
    endpoint.dump(obj)


@main.command()
@click.option("--module", "-m", help="Path to python datamodel module")
@click.option("--db", "-D", help="Path to SQLite database file")
@click.option("--output", "-o", help="Path to output file")
@click.option(
    "--output-format",
    "-t",
    type=click.Choice(list(dumpers_loaders.keys())),
    help="Output format. Inferred from output suffix if not specified",
)
@click.option(
    "--target-class",
    "-C",
    help="name of class in datamodel that the root node instantiates",
)
@click.option(
    "--index-slot", "-S", help="top level slot. Required for CSV dumping/loading"
)
@click.option("--schema", "-s", help="Path to schema specified as LinkML yaml")
@click.option(
    "--validate/--no-validate",
    default=True,
    show_default=True,
    help="Validate against the schema",
)
@click.option(
    "--force/--no-force",
    default=True,
    show_default=True,
    help="Force creation of a database if it does not exist",
)
def load(
    output,
    output_format,
    module,
    db,
    target_class,
    input_format=None,
    schema=None,
    validate=None,
    force: bool = None,
    index_slot=None,
) -> None:
    """
    Loads data from a SQL store

    Examples:

        linkml-sqldb load -s personinfo.yaml -D my_person_database.db -o my_data.yaml
    """
    if module is None:
        if schema is None:
            raise Exception("must pass one of module OR schema")
        else:
            python_module = PythonGenerator(schema).compile_module()
    else:
        python_module = compile_python(module)
    if schema is not None:
        sv = SchemaView(schema)
    if target_class is not None:
        py_target_class = python_module.__dict__[target_class]
    else:
        py_target_class = None

    endpoint = SQLStore(schema, database_path=db, include_schema_in_database=False)
    endpoint.native_module = python_module
    endpoint.compile()
    obj = endpoint.load(py_target_class)
    output_format = _get_format(output, output_format, default="json")
    outargs = {}
    if output_format == "json-ld":
        if len(context) == 0:
            if schema is not None:
                context = [_get_context(schema)]
            else:
                raise Exception("Must pass in context OR schema for RDF output")
        outargs["contexts"] = list(context)
        outargs["fmt"] = "json-ld"
    if output_format == "rdf" or output_format == "ttl":
        if sv is None:
            raise Exception(f"Must pass schema arg")
        outargs["schemaview"] = sv
    if _is_xsv(output_format):
        if index_slot is None:
            index_slot = infer_index_slot(sv, target_class)
            if index_slot is None:
                raise Exception("--index-slot is required for CSV output")
        outargs["index_slot"] = index_slot
        outargs["schema"] = schema
    dumper = get_dumper(output_format)
    if output is not None:
        dumper.dump(obj, output, **outargs)
    else:
        print(dumper.dumps(obj, **outargs))


if __name__ == "__main__":
    main()
