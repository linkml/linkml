"""Helper for compliance tests. See README.md for more information."""

import csv
import enum
import json
import logging
import os
import shutil
import subprocess
import tempfile
from collections import defaultdict
from copy import copy, deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Tuple, Type, Union

import linkml_runtime
import pydantic
import pytest
import rdflib
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import rdflib_dumper, yaml_dumper
from linkml_runtime.linkml_model import Decimal, SchemaDefinition
from linkml_runtime.linkml_model import meta as meta
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

try:
    from yaml import CSafeDumper as SafeDumper
except ImportError:
    from yaml import SafeDumper


import tests
from linkml import generators as generators
from linkml.generators import (
    ContextGenerator,
    JsonSchemaGenerator,
    OwlSchemaGenerator,
    PydanticGenerator,
    PythonGenerator,
    ShaclGenerator,
    ShExGenerator,
    sqlalchemygen,
)
from linkml.utils.generator import Generator
from linkml.utils.sqlutils import SQLStore
from linkml.validator import JsonschemaValidationPlugin, Validator
from linkml.validator.plugins.shacl_validation_plugin import ShaclValidationPlugin

THIS_DIR = Path(__file__).parent
OUTPUT_DIR = THIS_DIR / "output"

SCHEMA_NAME = str
FRAMEWORK = str  ## pydantic, java, etc

PYDANTIC_ROOT_CLASS = "ConfiguredBaseModel"
PYTHON_DATACLASSES_ROOT_CLASS = "YAMLRoot"
PYDANTIC = "pydantic"
PYDANTIC_STRICT = "pydantic_strict"  ## TODO: https://docs.pydantic.dev/latest/usage/types/strict_types/
PYTHON_DATACLASSES = "python_dataclasses"
JSON_SCHEMA = "jsonschema"
JAVA = "java"
SHACL = "shacl"
SHEX = "shex"
JSONLD_CONTEXT = "jsonld_context"
JSONLD = "jsonld"
SQL_ALCHEMY_IMPERATIVE = "sqlalchemy_imperative"
SQL_ALCHEMY_DECLARATIVE = "sqlalchemy_declarative"
SQL_DDL_SQLITE = "sql_ddl_sqlite"
SQL_DDL_POSTGRES = "sql_ddl_postgres"
OWL = "owl"
GENERATORS: Dict[FRAMEWORK, Union[Type[Generator], Tuple[Type[Generator], Dict[str, Any]]]] = {
    PYDANTIC: generators.PydanticGenerator,
    PYTHON_DATACLASSES: generators.PythonGenerator,
    JAVA: generators.JavaGenerator,
    JSON_SCHEMA: generators.JsonSchemaGenerator,
    SHACL: generators.ShaclGenerator,
    SHEX: generators.ShExGenerator,
    JSONLD: generators.JSONLDGenerator,
    JSONLD_CONTEXT: generators.ContextGenerator,
    SQL_ALCHEMY_IMPERATIVE: (
        generators.SQLAlchemyGenerator,
        {"template": sqlalchemygen.TemplateEnum.IMPERATIVE},
    ),
    SQL_ALCHEMY_DECLARATIVE: (
        generators.SQLAlchemyGenerator,
        {"template": sqlalchemygen.TemplateEnum.DECLARATIVE},
    ),
    SQL_DDL_SQLITE: (generators.SQLTableGenerator, {"dialect": "sqlite"}),
    SQL_DDL_POSTGRES: (generators.SQLTableGenerator, {"dialect": "postgresql"}),
    OWL: (
        generators.OwlSchemaGenerator,
        {
            "metaclasses": False,
            "type_objects": False,
            "use_native_uris": False,
        },
    ),
}


class ValidationBehavior(str, enum.Enum):
    IMPLEMENTS: str = "implements"
    IGNORES: str = "ignores"
    COERCES: str = "coerces"
    FALSE_POSITIVE: str = "false_positive"
    INCOMPLETE: str = "incomplete"
    NOT_APPLICABLE: str = "not_applicable"
    ACCEPTS: str = "accepts"
    MIXED: str = "mixed"
    UNTESTED: str = "untested"


class DataCheck(BaseModel):
    schema_name: str
    data_name: str
    framework: str
    expected_behavior: ValidationBehavior
    description: Optional[str] = None
    notes: Optional[str] = None


class Feature(BaseModel):
    """
    A category of tests that can be implemented by multiple frameworks.
    """

    name: str
    description: str
    implementations: Dict[FRAMEWORK, ValidationBehavior]
    num_tests: int = 0

    class Config:
        use_enum_values = True

    def set_framework_behavior(self, framework: FRAMEWORK, behavior: ValidationBehavior) -> ValidationBehavior:
        if framework not in self.implementations:
            self.implementations[framework] = behavior
            return behavior
        current = self.implementations[framework]
        if current == behavior:
            return behavior
        if current == ValidationBehavior.INCOMPLETE:
            return current
        if behavior == ValidationBehavior.INCOMPLETE:
            self.implementations[framework] = behavior
            return behavior
        if behavior == ValidationBehavior.COERCES:
            if current == ValidationBehavior.IMPLEMENTS:
                self.implementations[framework] = behavior
                return behavior
        self.implementations[framework] = ValidationBehavior.MIXED
        return self.implementations[framework]


class FeatureSet(BaseModel):
    """A collection of features."""

    features: List[Feature]


cached_generator_output: Dict[Tuple[SCHEMA_NAME, FRAMEWORK], Tuple[Generator, str, Optional[Path]]] = {}
"""Cache generators and their outputs to avoid repeated computation."""

all_test_results: List[DataCheck] = []
"""Result of each data check."""

feature_dict: Dict[str, Feature] = {}
"""Map from test name to feature."""

schema_name_to_feature: Dict[str, str] = {}
"""Map from schema name to feature."""

schema_name_to_metamodel_elements: Dict[SCHEMA_NAME, List[str]] = {}
"""Map from schema name all metamodels used in that schema."""


def _as_tsv(rows: List[Dict], path: Union[str, Path]) -> str:
    logging.info(f"Writing report to {path}")
    fn = f"{path}.tsv"
    if rows:
        fieldnames = []
        for row in rows:
            fieldnames.extend([k for k in row.keys() if k not in fieldnames])
        with open(OUTPUT_DIR / fn, "w", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=fieldnames, delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)


def report():
    """
    Generate final reports.

    Note: this is run on exit, so if this fails the test suite still
    shows as working; TODO: run in a different way

    Note: some of these are subject to change
    """
    logging.info(f"Generating reports for {len(all_test_results)} tests")
    fset = FeatureSet(features=list(feature_dict.values()))
    suffix = "" if len(fset.features) > 5 else "_partial"
    summary_base_name = f"summary{suffix}"
    with open(OUTPUT_DIR / f"{summary_base_name}.md", "w", encoding="utf-8") as stream:
        stream.write(f"# {summary_base_name}\n\n")
        stream.write("# Description\n\n")
        # stream.write(fset.description)
    path = OUTPUT_DIR / f"{summary_base_name}.yaml"
    with open(path, "w", encoding="utf-8") as stream:
        yaml.dump(fset.dict(), stream, sort_keys=False)
    for feature in fset.features:
        with open(OUTPUT_DIR / f"{feature.name}.yaml", "w", encoding="utf-8") as stream:
            yaml.dump(feature.dict(), stream, sort_keys=False)
    _as_tsv([{"name": f.name, **f.implementations} for f in fset.features], summary_base_name)
    _as_tsv([check.dict() for check in all_test_results], f"report{suffix}")
    pivoted = defaultdict(dict)
    for check in all_test_results:
        key = (check.schema_name, check.data_name)
        pivoted[key]["schema"] = check.schema_name
        pivoted[key]["data"] = check.data_name
        pivoted[key][check.framework] = check.expected_behavior
    _as_tsv(list(pivoted.values()), f"pivoted{suffix}")
    elements = set()
    for v in schema_name_to_metamodel_elements.values():
        elements.update(v)
    msv = metamodel_schemaview()
    all_elts = set([str(k) for k in msv.all_classes()]).union([str(k) for k in msv.all_slots()])
    coverage = len(elements.intersection(all_elts)) / len(all_elts)
    with open(OUTPUT_DIR / f"coverage{suffix}.txt", "w", encoding="utf-8") as stream:
        stream.write(f"Coverage: {coverage}")
        stream.write("\n".join(sorted(set(elements))))


## atexit.register(report)


def metamodel_schemaview() -> SchemaView:
    """
    Get a SchemaView for the LinkML metamodel.

    :return: view
    """
    return package_schemaview(meta.__name__)


def _get_metamodel_elements(obj: Any) -> Iterator[str]:
    if isinstance(obj, list):
        for elt in obj:
            yield from _get_metamodel_elements(elt)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _get_metamodel_elements(v)
    else:
        pass


def _generate_framework_output(
    schema: Dict, framework: str, mappings: List = None
) -> Tuple[Generator, str, Optional[Path]]:
    """
    Compile a schema using a framework (e.g. jsonschema generation).

    If mappings are present, check against these

    :param schema:
    :param framework:
    :param mappings: maps between framework and expected results.
    :return:
    """
    pair = (schema["name"], framework)
    if schema["name"] not in schema_name_to_metamodel_elements:
        schema_name_to_metamodel_elements[schema["name"]] = list(_get_metamodel_elements(schema))
    if pair not in cached_generator_output:
        if mappings is None:
            # this should only happen when executing individual pytest combos
            mappings = []
            logging.warning(f"No mappings for {pair} - called out of order?")
        gen_class = GENERATORS[framework]
        if isinstance(gen_class, tuple):
            gen_class, gen_args = gen_class
        else:
            gen_args = {}

        gen_args["base_dir"] = str(_schema_out_path(schema))
        gen = gen_class(schema=SchemaDefinition(**schema), **gen_args)
        if framework == JAVA:
            temp_dir = tempfile.TemporaryDirectory()
            gen.serialize(temp_dir.name)
            # walk all files in temp_dir and concatenate them
            output = ""
            for root, _dirs, files in os.walk(temp_dir.name):
                for file in files:
                    path = os.path.join(root, file)
                    with open(path, "r") as stream:
                        output += stream.read()
        else:
            output = gen.serialize()

        if tests.WITH_OUTPUT:
            out_dir = _schema_out_path(schema) / "generated"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{framework}.{gen.file_extension}"
            with open(out_path, "w", encoding="utf-8") as stream:
                stream.write(output)
        else:
            out_path = None

        cached_generator_output[pair] = (gen, output, out_path)
        for context, impdict in mappings:
            if framework in impdict:
                expected = impdict[framework]
                if expected is None:
                    continue
                if isinstance(expected, (list, str)) and framework in [SHACL, OWL]:
                    assert compare_rdf(expected, output, subsumes=framework in [OWL]) == set()
                elif isinstance(expected, str):
                    if "".join(expected.split()) not in "".join(output.split()):
                        pytest.fail(f"Not a substring when ignoring whitespace:\n'{expected}'\n'{output}'")
                    # assert expected in output
                elif isinstance(expected, dict):
                    output_obj = json.loads(output)
                    assert _obj_within_obj(expected, output_obj)
                    # assert expected.items() <= output_obj.items()
                else:
                    raise AssertionError
    else:
        logging.debug(f"Reusing {len(cached_generator_output.items())}")
    return cached_generator_output[pair]


TRIPLE = Tuple[rdflib.URIRef, rdflib.URIRef, Union[rdflib.URIRef, rdflib.Literal]]


def compare_rdf(expected: Union[str, List[TRIPLE]], actual: str, subsumes: bool = False) -> Optional[Set]:
    """
    Compares two rdf serializations.

    Note: comparison is incomplete, blank nodes are ignored

    :param expected:
    :param actual:
    :param subsumes: subsumption rather than equivalence check
    :return:
    """
    if isinstance(expected, str):
        g_expected = rdflib.Graph()
        g_expected.parse(data=expected, format="turtle")
    else:
        g_expected = rdflib.Graph()
        for t in expected:
            g_expected.add(t)
    g_actual = rdflib.Graph()
    g_actual.parse(data=actual, format="turtle")

    def _triple_minus_bnode(*elts):
        return tuple([x if not isinstance(x, rdflib.BNode) else None for x in elts])

    triples_expected = {_triple_minus_bnode(*t) for t in g_expected}
    triples_actual = {_triple_minus_bnode(*t) for t in g_actual}
    if subsumes:
        return triples_expected.difference(triples_actual)
    else:
        return triples_expected.union(triples_actual).difference(triples_expected.intersection(triples_actual))


def _obj_within_obj(expected: Dict, actual: Dict) -> bool:
    """
    Check if the expected object is within the actual object.

    :param expected:
    :param actual:
    :return:
    """
    if expected.items() <= actual.items():
        return True
    for k, v in actual.items():
        if isinstance(v, dict):
            if _obj_within_obj(expected, v):
                return True
        elif isinstance(v, list):
            for elt in v:
                if isinstance(elt, dict):
                    if _obj_within_obj(expected, elt):
                        return True
    return False


def _schema_out_path(schema: Dict, parent=False) -> Path:
    """
    Get the output path for a schema.

    This is derived from the schema name (which is already constrained to be
    filesystem safe).

    :param schema:
    :return:
    """
    toks = schema["name"].split("-")
    test_name = toks[0]
    schema_name = "-".join(toks[1:])
    out_dir = OUTPUT_DIR / test_name
    if not parent:
        out_dir = out_dir / schema_name
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


@lru_cache
def _get_linkml_types() -> dict:
    type_schema = yaml.safe_load(open(linkml_runtime.SCHEMA_DIRECTORY / "types.yaml"))
    for typ in type_schema.get("types", {}).values():
        typ["from_schema"] = "https://w3id.org/linkml/types"
    return type_schema


def _make_schema(
    test: Callable,
    name: str,
    schema: Dict = None,
    classes: Dict = None,
    slots: Dict = None,
    types: Dict = None,
    prefixes: Dict = None,
    core_elements: List = None,
    post_process: Callable = None,
    merge_type_imports=True,
    imported_schemas: List[Dict] = None,
    mappings: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Tuple[Dict, List]:
    """
    Create a schema for use in testing.

    :param test:
    :param name:
    :param schema:
    :param classes:
    :param slots:
    :param types:
    :param prefixes:
    :param core_elements:
    :param post_process:
    :param kwargs:
    :return: schema as dict, plus mappings between framework and expected output
    """
    schema_name = f"{test.__name__}-{name}"
    if schema is None:
        schema = {
            "id": f"http://example.org/{name}",
            "name": schema_name,
            "description": test.__doc__,
            "prefixes": {
                "ex": "http://example.org/",
            },
            "default_prefix": "ex",
            "default_range": "string",
            "classes": {},
            "slots": {},
            "types": {},
        }
        # Fetching the types.yaml file via an import each time this schema is
        # resolved takes too much time so we fetch it once manually and inline
        # the relevant parts here
        if merge_type_imports:
            linkml_types = _get_linkml_types()
            schema["prefixes"].update(linkml_types.get("prefixes", {}))
            schema["types"].update(linkml_types.get("types", {}))
        else:
            if "imports" not in schema:
                schema["imports"] = []
            schema["imports"].append("linkml:types")
            if "linkml:types" not in schema["prefixes"]:
                schema["prefixes"]["linkml"] = "https://w3id.org/linkml/"
    else:
        schema = deepcopy(schema)
    if mappings is not None:
        schema["_mappings"] = mappings
    if classes is not None:
        schema["classes"].update(classes)
    if slots is not None:
        schema["slots"].update(slots)
    if types is not None:
        schema["types"].update(types)
    for k, v in kwargs.items():
        schema[k] = v
    if prefixes:
        schema["prefixes"].update(prefixes)
    if core_elements:
        if "keywords" not in schema:
            schema["keywords"] = []
        schema["keywords"].extend(core_elements)
    if post_process is not None:
        post_process(schema)
    mappings = list(_extract_mappings(schema))
    out_dir = _schema_out_path(schema)
    parent_out_dir = _schema_out_path(schema, parent=True)
    schema["source_file"] = str(out_dir / "schema.yaml")

    if tests.WITH_OUTPUT:
        # Write top-level README (TODO: avoid doing this for each combination)
        with open(parent_out_dir / "README.md", "w", encoding="utf-8") as stream:
            dlines = [x.strip() for x in schema["description"].split("\n")]
            dlines = [x for x in dlines if not x.startswith(":")]
            desc = "\n".join(dlines)
            stream.write(f"# {test.__name__}\n\n")
            stream.write(f"{desc}\n\n")
            stream.write("## Elements Tested\n\n")
            if not core_elements:
                raise AssertionError(f"No core elements defined for for {schema_name}")
            for el in core_elements:
                stream.write(f"* [{el}](https://w3id.org/linkml/{el})\n")

        # Write README for this schema combo
        with open(out_dir / "README.md", "w", encoding="utf-8") as stream:
            dlines = [x.strip() for x in schema["description"].split("\n")]
            dlines = [x for x in dlines if not x.startswith(":")]
            desc = "\n".join(dlines)
            stream.write(f"# {schema_name.replace('test_', '')}\n\n")
            stream.write(f"{desc}\n\n")
            schema_minimal = deepcopy(schema)
            builtin = [
                tn
                for tn, t in schema_minimal.get("types", {}).items()
                if t.get("from_schema", None) == "https://w3id.org/linkml/types"
            ]
            for t in builtin:
                del schema_minimal["types"][t]
            if "imports" not in schema_minimal:
                schema_minimal["imports"] = []
            schema_minimal["imports"].append("linkml:types")
            stream.write("## Schema\n\n")
            stream.write("```yaml\n")
            yaml.safe_dump(schema_minimal, stream, sort_keys=False)
            stream.write("```\n\n")

        with open(out_dir / "mappings.txt", "w", encoding="utf-8") as stream:
            stream.write(str(mappings))

        with open(out_dir / "schema.yaml", "w", encoding="utf-8") as stream:
            yaml.safe_dump(schema, stream, sort_keys=False)

    if imported_schemas:
        for imp in imported_schemas:
            imp_path = f'{out_dir / imp["name"]}.yaml'
            with open(imp_path, "w", encoding="utf-8") as imp_stream:
                yaml.safe_dump(imp, imp_stream, sort_keys=False)

    if not schema["name"]:
        raise ValueError(f"Schema name not set: {schema}")
    return schema, mappings


def validated_schema(test: Callable, local_name: str, framework: str, **kwargs) -> Dict:
    """
    Generate a schema and validate it using the given framework.

    Validation is performed using `_mapping` keys in the schema; these are
    extracted out before schema compilation, and used to check the schema output.

    Note that this function performs in-memory caching of schema outputs, to
    avoid recomputation. It will also write out the schema and generated outputs to disk.
    The key for the cache and the base filename are controlled by two arguments:

    - the name of the test function (e.g. test_inlined)
    - a local name that represents a particular pytest parameter combination.

    The first argument specifies the test function that is calling this function.
    This is used to extract metadata about the test, including its name and
    its documentation. When authoring a test you must ensure this is correct, otherwise
    unexpected behavior may occur, such as saving the yaml files in the wrong place or
    incorrectly caching the schema generation.

    :param test: calling test function; MUST match name of test
    :param local_name: name for this particular test combination
    :param framework:
    :param kwargs:
    :return:
    """
    test_name = test.__name__
    if test_name not in feature_dict:
        if not test.__doc__:
            raise AssertionError(f"Test {test_name} has no docstring")
        feature_dict[test_name] = Feature(
            name=test_name,
            description=test.__doc__,
            implementations={},
        )
    schema, mappings = _make_schema(test, local_name, **kwargs)
    schema_name_to_feature[schema["name"]] = test_name
    # ensure this is cached
    _gen, _output, _ = _generate_framework_output(schema, framework, mappings=mappings)
    return schema


def _extract_mappings(schema: Dict) -> Iterator[Tuple[Dict, List]]:
    """
    Extract key-values injected into the schema to represent expected outputs per generator.

    :param schema: dict representation of schema
    :return: yields
    """
    if isinstance(schema, dict):
        if "_mappings" in schema:
            mappings = schema["_mappings"]
            yield schema, mappings
            del schema["_mappings"]
        for k, v in schema.items():
            yield from _extract_mappings(v)
    elif isinstance(schema, list):
        for v in schema:
            yield from _extract_mappings(v)
    else:
        pass


def _as_compact_yaml(obj: Union[YAMLRoot, BaseModel, Dict]) -> str:
    if isinstance(obj, dict):
        ys = yaml.dump(_clean_dict(obj), sort_keys=False, Dumper=SafeDumper)
        ys = ys.replace("{}", "")
        return ys
    return yaml_dumper.dumps(obj)


def _objects_are_equal(obj1: Union[YAMLRoot, BaseModel, Dict], obj2: Union[YAMLRoot, BaseModel, Dict]) -> bool:
    y1 = _as_compact_yaml(obj1)
    y2 = _as_compact_yaml(obj2)
    return y1 == y2


def _clean_dict(value: Any):
    """
    Remove None values from the given object.

    Also converts Decimal to float.

    :param value:
    :return:
    """
    if isinstance(value, list):
        return [_clean_dict(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {key: _clean_dict(val) for key, val in value.items() if val is not None}
    elif isinstance(value, Decimal):
        return float(value)
    else:
        return value


_sql_store_cache: Dict[str, SQLStore] = {}


def _get_sql_store(schema) -> SQLStore:
    schema_name = schema["name"]
    if schema_name not in _sql_store_cache:
        schema_obj = meta.SchemaDefinition(**schema)
        _schema_out_path(schema) / "temp.db"
        # store = SQLStore(schema_obj, database_path=db_path, include_schema_in_database=False)
        store = SQLStore(schema_obj, use_memory=True, include_schema_in_database=False)
        _, code, _ = _generate_framework_output(schema, PYTHON_DATACLASSES)
        store.native_module = compile_python(code)
        _sql_store_cache[schema_name] = store
        store.compile()
    return _sql_store_cache[schema_name]


def check_data(
    schema: Dict,
    data_name: str,
    framework: FRAMEWORK,
    object_to_validate: Dict,
    valid: bool,
    should_warn: bool = False,
    expected_behavior: Union[ValidationBehavior, Tuple[ValidationBehavior, str]] = ValidationBehavior.IMPLEMENTS,
    target_class: str = None,
    description: str = None,
    coerced: Dict = None,
    exclude_rdf=False,
):
    """
    Validate the given object against the given schema using the given framework.

    Note: this will attempt to use cached schema output to avoid repeated computation;
    it is important to ensure this is called *after* `validated_schema`

    Side effects: this will update various report objects

    :param schema: dict representation of schema to validate against
    :param data_name: a unique label for this dataset. Should be unix-friendly
    :param framework: name of framework to check (e.g pydantic)
    :param object_to_validate: dict representation of object to validate
    :param valid: is the object expected to be inferred valid
    :param should_warn: true if the object is valid but fails a recommended or SHOULD NOT case
    :param expected_behavior: is the framework expected to validate or coerce or ignore this scenario?
    :param target_class: the type of the object
    :param description: description of this particular test combination
    :param coerced: Dict representation of repaired/coerced form of object
    :return:
    """
    out_dir = _schema_out_path(schema)
    if valid:
        out_dir = out_dir / "valid"
    else:
        out_dir = out_dir / "invalid"
    out_dir.mkdir(parents=True, exist_ok=True)
    feature = feature_dict[schema_name_to_feature[schema["name"]]]
    feature.num_tests += 1
    # TODO: avoid repeated rewrites of same object shared across frameworks
    if tests.WITH_OUTPUT:
        with open(out_dir / f"README.{data_name}.md", "w", encoding="utf-8") as stream:
            stream.write(f"# {data_name}\n")
            if description:
                stream.write(f"_{description}_\n")
            stream.write("\n## Schema:\n")
            stream.write(" * [../schema.yaml](../schema.yaml)\n")
            stream.write("\n## Object:\n")
            stream.write("```yaml\n")
            yaml.safe_dump(object_to_validate, stream)
            stream.write("```\n")
            stream.write("\nExpected behavior:\n\n")
            if valid:
                stream.write("* valid (frameworks must accept the data object)\n")
            else:
                stream.write("* invalid (frameworks must flag the data object)\n")
        with open(out_dir / f"{data_name}.yaml", "w", encoding="utf-8") as stream:
            yaml.safe_dump(object_to_validate, stream)
    notes = None
    plugins = []
    if isinstance(expected_behavior, tuple):
        expected_behavior, notes = expected_behavior
    if expected_behavior is None:
        expected_behavior = ValidationBehavior.IMPLEMENTS
    if expected_behavior in [
        ValidationBehavior.INCOMPLETE,
        ValidationBehavior.NOT_APPLICABLE,
        ValidationBehavior.FALSE_POSITIVE,
    ]:
        logging.warning(f"Skipping test for {expected_behavior}")
    else:
        gen, output, output_path = _generate_framework_output(schema, framework)
        if isinstance(gen, (PydanticGenerator, PythonGenerator)):
            # Note: this duplicates some code with PydanticValidationPlugin;
            # but currently the validation framework doesn't support explicit
            # coercion detection and output of repaired objects
            mod = compile_python(output)
            py_cls = getattr(mod, target_class)
            logging.info(f"Validating {py_cls} against {object_to_validate}// {expected_behavior} {valid}")
            py_inst = None
            if valid:
                py_inst = py_cls(**object_to_validate)
            else:
                # TODO: to move this to a validator plugin, the plugin architecture must deal with coercion
                if expected_behavior == ValidationBehavior.COERCES:
                    try:
                        py_inst = py_cls(**object_to_validate)
                    except Exception as e:
                        assert True, f"could not coerce invalid object; exception: {e}"
                    if py_inst:
                        if coerced:
                            assert _as_compact_yaml(py_inst) == _as_compact_yaml(
                                coerced
                            ), f"coerced {py_inst} != {coerced}"
                        else:
                            logging.warning(f"INCOMPLETE TEST: did not check coerced: {py_inst}")
                else:
                    if isinstance(gen, PydanticGenerator):
                        with pytest.raises(pydantic.ValidationError):
                            py_inst = py_cls(**object_to_validate)
                            logging.info(f"Unexpectedly instantiated {py_inst} from {object_to_validate}")
                    else:
                        with pytest.raises(Exception):
                            py_inst = py_cls(**object_to_validate)
                            logging.info(f"Unexpectedly instantiated {py_inst}")
            if py_inst is not None:
                # assert roundtripped.items() == object_to_validate.items()
                if valid and not exclude_rdf:
                    if isinstance(gen, PythonGenerator):
                        ttl_path = out_dir / f"{data_name}.ttl"
                        _convert_data_to_rdf(schema, object_to_validate, target_class, ttl_path)
            logging.info(f"fwk: {framework}, cls: {target_class}, inst: {object_to_validate}, valid: {valid}")

        elif isinstance(gen, JsonSchemaGenerator):
            plugins = [JsonschemaValidationPlugin(closed=True, include_range_class_descendants=False)]
        elif isinstance(gen, ContextGenerator):
            context_dir = _schema_out_path(schema) / "generated" / "jsonld_context.context.jsonld"
            if not context_dir.exists() and tests.WITH_OUTPUT:
                raise AssertionError(f"Could not find {context_dir}")
            context = json.loads(cached_generator_output[(schema["name"], "jsonld_context")][1])["@context"]
            json_object = copy(object_to_validate)
            json_object["@context"] = context
            jsonld_path = out_dir / f"{data_name}.jsonld"
            if tests.WITH_OUTPUT:
                with open(jsonld_path, "w", encoding="utf-8") as stream:
                    json.dump(json_object, stream, indent=2, sort_keys=True, ensure_ascii=False)
            g = rdflib.Graph()
            g.parse(data=json.dumps(json_object, indent=2, sort_keys=True, ensure_ascii=False), format="json-ld")
            if not valid and expected_behavior == ValidationBehavior.IMPLEMENTS:
                logging.info(f"Skipping validation for {jsonld_path}")
        elif isinstance(gen, OwlSchemaGenerator):
            # TODO: make this a validator
            if not exclude_rdf:
                ttl_path = out_dir / f"{data_name}.ttl"
                _convert_data_to_rdf(schema, object_to_validate, target_class, ttl_path)
                # if not ttl_path.exists():
                #    raise ValueError(f"Could not convert {object_to_validate} to RDF")
                coherent = robot_check_coherency(ttl_path, output_path, str(ttl_path) + ".reasoned.owl")
                if coherent is not None:
                    if valid:
                        assert coherent, f"Coherency check failed for {ttl_path}"
                    else:
                        assert not coherent, f"Coherency check succeeded for {ttl_path}"
                else:
                    expected_behavior = ValidationBehavior.UNTESTED
            else:
                expected_behavior = ValidationBehavior.UNTESTED
        elif isinstance(gen, ShaclGenerator):
            # currently requires translating via python objects
            if not exclude_rdf:
                plugins = [ShaclValidationPlugin(closed=True)]
            else:
                expected_behavior = ValidationBehavior.UNTESTED
            # expected_behavior = ValidationBehavior.UNTESTED
        elif isinstance(gen, ShExGenerator):
            # TODO: use pyshex
            expected_behavior = ValidationBehavior.UNTESTED
        elif framework == SQL_DDL_SQLITE:
            # TODO: make this a validator
            endpoint = _get_sql_store(schema)
            endpoint.db_exists(force=True)
            py_cls = endpoint.native_module.__dict__[target_class]
            if valid:
                py_obj = py_cls(**object_to_validate)
                endpoint.dump(py_obj)
            else:
                with pytest.raises(Exception):
                    py_obj = py_cls(**object_to_validate)
                    endpoint.dump(py_obj)
        else:
            logging.warning(f"Unsupported generator {gen}")
            expected_behavior = ValidationBehavior.UNTESTED
    if plugins:
        validator = Validator(
            schema=schema,
            validation_plugins=plugins,
        )
        # validator = JsonSchemaDataValidator(schema=yaml.dump(schema))
        # errors = list(validator.iter_validate_dict(_clean_dict(object_to_validate), target_class, closed=True))

        errors = list(validator.iter_results(clean_null_terms(object_to_validate), target_class))
        logging.info(f"Expecting {valid}, Validating {object_to_validate} against {target_class}, errors: {errors}")
        if valid:
            assert errors == [], f"Errors found in json schema validation: {errors}"
        else:
            if expected_behavior == ValidationBehavior.ACCEPTS:
                logging.info("Does not flag exception for borderline case (e.g. matching an int to a float)")
            else:
                assert errors != [], "Expected errors in json schema validation, but none found"
        if should_warn:
            logging.warning("TODO: check for warnings")
    feature.set_framework_behavior(framework, expected_behavior)
    if not valid:
        all_test_results.append(
            DataCheck(
                schema_name=schema["name"],
                data_name=data_name,
                framework=framework,
                expected_behavior=expected_behavior,
                description=description,
                notes=str(notes),
            )
        )


def clean_null_terms(d):
    if type(d) is dict:  # noqa E721
        return dict((k, clean_null_terms(v)) for k, v in d.items() if v is not None)
    elif type(d) is list:  # noqa E721
        return [clean_null_terms(v) for v in d if v is not None]
    else:
        return d


def _convert_data_to_rdf(schema: dict, instance: dict, target_class: str, ttl_path: str) -> Optional[rdflib.Graph]:
    ttl_path = str(ttl_path)
    gen, output, _ = _generate_framework_output(schema, PYTHON_DATACLASSES)
    mod = compile_python(output)
    py_cls = getattr(mod, target_class)
    try:
        py_inst = py_cls(**instance)
    except Exception as e:
        logging.info(f"Could not instantiate {py_cls} from {instance}; exception: {e}")
        return None
    schemaview = SchemaView(SchemaDefinition(**schema))
    g = rdflib_dumper.as_rdf_graph(
        py_inst,
        schemaview=schemaview,
        prefix_map={
            "_base": "http://example.org/",
            "X": "http://example.org/X/",
            "P": "http://example.org/P/",
        },
    )
    ttl_output = g.serialize(format="turtle")
    g = rdflib.Graph()
    g.parse(data=ttl_output, format="turtle")
    roundtripped = rdflib_loader.load(ttl_output, target_class=py_cls, schemaview=schemaview)
    if tests.WITH_OUTPUT:
        yaml_dumper.dump(roundtripped, to_file=ttl_path + ".yaml")
    return g


@lru_cache
def robot_is_on_path():
    """
    Check if robot is on the path.

    If robot is not on the path, then OWL checks will be skipped.

    To ensure robot is on the path for pycharm

    .. code-block:: bash

        poetry run which python
        which robot

    Then execute something like this, ensuring you substitute your robot path and virtualenv path:

    .. code-block:: bash

        ln -s ~/repos/robot/bin/robot ~/Library/Caches/pypoetry/virtualenvs/linkml-lavaHNw6-py3.9/bin/robot

    :return:
    """
    return shutil.which("robot") is not None


def robot_check_coherency(data_path: str, ontology_path: str, output_path: str = None) -> Optional[bool]:
    """
    Check the data validates using an OWL reasoner, executed by robot.

    Note this requires robot being on your path; in future we may move to calling this via the robot
    py4j wrapper, but for now this is an optional add-on.

    :param data_path:
    :param ontology_path:
    :param output_path:
    :return:
    """
    if not robot_is_on_path():
        return None
    merged = str(data_path) + ".merged.owl"
    cmd = [
        "robot",
        "merge",
        "-i",
        data_path,
        "-i",
        ontology_path,
        "-o",
        merged,
        "merge",
        "-i",
        merged,
        "reason",
        "-r",
        "hermit",
    ]
    if output_path:
        cmd.extend(["-o", output_path])
    try:
        # print(f"Running robot: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if result.stderr:
            logging.warning(result.stderr)
        logging.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.info(f"Robot call failed, likely unsatisfiable: {e}")
        return False


TREE_NODE = Tuple[int]


def generate_tree_nodes(depth=3, num_siblings=2, path: List[int] = None) -> Iterator[TREE_NODE]:
    """
    Generate a tree of data names, with depth `depth`.

    :param depth:
    :return:
    """
    assert depth >= 0
    if path is None:
        path = [0]
    yield tuple(path)
    for i in range(1, num_siblings + 1):
        if depth > 0:
            yield from generate_tree_nodes(depth=depth - 1, num_siblings=num_siblings, path=path + [i])


def generate_tree(depth=3, num_siblings=2, prefix="N") -> Iterator[Tuple[str, List[str]]]:
    """
    Generate a tree of data names, with depth `depth`.

    :param depth:
    :return:
    """
    assert depth >= 0

    def node_id(path):
        return prefix + "".join(str(i) for i in path)

    for path in generate_tree_nodes(depth=depth, num_siblings=num_siblings):
        assert len(path) > 0
        if len(path) == 1:
            yield node_id(path), []
        else:
            yield node_id(path), [node_id(path[:-1])]
