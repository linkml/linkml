import atexit
import enum
import json
import logging
from copy import deepcopy
from pathlib import Path
from typing import Dict, List, Tuple, Generator, Callable, Iterator, Union, Type

import pydantic
import pytest
import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import meta as meta
from linkml_runtime.utils.compile_python import compile_python
from linkml_runtime.utils.introspection import package_schemaview
from linkml_runtime.utils.yamlutils import YAMLRoot
from pydantic import BaseModel

from linkml import generators as generators
from linkml.generators import PydanticGenerator, PythonGenerator, JsonSchemaGenerator
from linkml.utils.generator import Generator
from linkml.validators import JsonSchemaDataValidator

THIS_DIR = Path(__file__).parent
OUTPUT_DIR = THIS_DIR / "output"

cached_generator_output = {}


def metamodel_schemaview() -> SchemaView:
    return package_schemaview(meta.__name__)


def _generate_framework_output(
    schema: Dict, framework: str, mappings: List = None
) -> Tuple[Generator, str]:
    pair = (schema["name"], framework)
    if pair not in cached_generator_output:
        gen_class = GENERATORS[framework]
        gen = gen_class(schema=yaml.dump(schema))
        output = gen.serialize()
        cached_generator_output[pair] = (gen, output)
        out_dir = _schema_out_path(schema) / "generated"
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / f"{framework}.{gen.file_extension}", "w", encoding="utf-8") as stream:
            stream.write(output)
        for context, impdict in mappings:
            if framework in impdict:
                expected = impdict[framework]
                if isinstance(expected, str):
                    assert impdict[framework] in output
                elif isinstance(expected, dict):
                    output_obj = json.loads(output)
                    assert expected.items() <= output_obj.items()
                else:
                    raise AssertionError
    else:
        print(f"XXX Reusing {len(cached_generator_output.items())}")
    return cached_generator_output[pair]


def report():
    path = OUTPUT_DIR / "report.txt"
    print(f"WRITING REPORT TO {path}")
    with open(path, "w", encoding="utf-8") as stream:
        for k, v in cached_generator_output.items():
            stream.write(f"{k}: {v}\n")

atexit.register(report)


def _schema_out_path(schema: Dict) -> Path:
    out_dir = OUTPUT_DIR / schema["name"]
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def _make_schema(
    test: Callable,
    name: str,
    schema: Dict = None,
    classes: Dict = None,
    slots: Dict = None,
    **kwargs,
) -> Tuple[Dict, List]:
    schema_name = f"{test.__name__}-{name}"
    if schema is None:
        schema = {
            "id": f"http://example.org/{name}",
            "name": schema_name,
            "description": test.__doc__,
            "prefixes": {
                "ex": "http://example.org/",
                "linkml": "https://w3id.org/linkml/",
            },
            "imports": [
                "linkml:types",
            ],
            "default_prefix": "ex",
            "default_range": "string",
        }
    else:
        schema = deepcopy(schema)
    if classes is not None:
        schema["classes"] = classes
    if slots is not None:
        schema["slots"] = slots
    for k, v in kwargs.items():
        schema[k] = v
    mappings = list(_extract_mappings(schema))
    print(mappings)
    out_dir = _schema_out_path(schema)
    with open(out_dir / "schema.yaml", "w", encoding="utf-8") as stream:
        yaml.safe_dump(schema, stream, sort_keys=False)
    with open(out_dir / "mappings.txt", "w", encoding="utf-8") as stream:
        stream.write(str(mappings))
    return schema, mappings


def validated_schema(test: Callable, name: str, framework: str, **kwargs) -> Dict:
    schema, mappings = _make_schema(test, name, **kwargs)
    _gen, output = _generate_framework_output(schema, framework, mappings=mappings)
    return schema


def _extract_mappings(schema: Dict) -> Iterator:
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
        ys = yaml.dump(obj, sort_keys=False)
        ys = ys.replace("{}", "")
        return ys
    return yaml_dumper.dumps(obj)


def _objects_are_equal(
    obj1: Union[YAMLRoot, BaseModel, Dict], obj2: Union[YAMLRoot, BaseModel, Dict]
) -> bool:
    y1 = _as_compact_yaml(obj1)
    y2 = _as_compact_yaml(obj2)
    return y1 == y2


@pytest.fixture()
def example_atomic_values():
    return ["", None, 1, 1.1, "1", True, False]


def _clean_nones(value):
    """
    Recursively remove all None values from dictionaries and lists, and returns
    the result as a new dictionary or list.
    """
    if isinstance(value, list):
        return [_clean_nones(x) for x in value if x is not None]
    elif isinstance(value, dict):
        return {key: _clean_nones(val) for key, val in value.items() if val is not None}
    else:
        return value


class ValidationBehavior(str, enum.Enum):
    IMPLEMENTS: str = "implements"
    IGNORES: str = "ignores"
    COERCES: str = "coerces"
    FALSE_POSITIVE: str = "false_positive"
    INCOMPLETE: str = "incomplete"
    ACCEPTS: str = "accepts"


def _check_data(
    schema: Dict,
    data_name: str,
    framework: str,
    object_to_validate: Dict,
    valid: bool,
    should_warn: bool = False,
    expected_behavior: ValidationBehavior = ValidationBehavior.IMPLEMENTS,
    target_class: str = None,
    description: str = None,
    coerced: Dict = None,
):
    out_dir = _schema_out_path(schema)
    if valid:
        out_dir = out_dir / "valid"
    else:
        out_dir = out_dir / "invalid"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / f"{data_name}.yaml", "w", encoding="utf-8") as stream:
        yaml.safe_dump(object_to_validate, stream)
    # print(f"Validating {target_class} against {framework}, gen: {gen}")
    if expected_behavior == ValidationBehavior.INCOMPLETE:
        logging.warning(f"Skipping incomplete test")
        return
    gen, output = _generate_framework_output(schema, framework)
    if isinstance(gen, (PydanticGenerator, PythonGenerator)):
        mod = compile_python(output)
        py_cls = getattr(mod, target_class)
        print(f"Validating {py_cls} against {object_to_validate}// {expected_behavior} {valid}")
        # print(instance_check)
        py_inst = None
        if valid:
            py_inst = py_cls(**object_to_validate)
        else:
            if expected_behavior == ValidationBehavior.COERCES:
                try:
                    py_inst = py_cls(**object_to_validate)
                except Exception as e:
                    assert True, "could not coerce invalid object"
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
                        print(f"Unexpectedly instantiated {py_inst} from {object_to_validate}")
                else:
                    with pytest.raises(Exception):
                        py_inst = py_cls(**object_to_validate)
                        print(f"Unexpectedly instantiated {py_inst}")
        if py_inst is not None:
            roundtripped = yaml.safe_load(yaml_dumper.dumps(py_inst))
            # assert roundtripped.items() == object_to_validate.items()
        print(f"fwk: {framework}, cls: {target_class}, inst: {object_to_validate}, valid: {valid}")
    elif isinstance(gen, JsonSchemaGenerator):
        validator = JsonSchemaDataValidator(schema=yaml.dump(schema))
        errors = list(
            validator.iter_validate_dict(
                _clean_nones(object_to_validate), target_class, closed=True
            )
        )
        print(
            f"Expecting {valid}, Validating {object_to_validate} against {target_class}, errors: {errors}"
        )
        if valid:
            assert errors == [], f"Errors found in json schema validation: {errors}"
        else:
            if expected_behavior == ValidationBehavior.ACCEPTS:
                logging.info(
                    f"Does not flag exception for borderline case (e.g. matching an int to a float)"
                )
            else:
                assert errors != [], f"Expected errors in json schema validation, but none found"
        if should_warn:
            logging.warning("TODO: check for warnings")
    else:
        logging.warning(f"Unsupported generator {gen}")


PYDANTIC_ROOT_CLASS = "ConfiguredBaseModel"
PYTHON_DATACLASSES_ROOT_CLASS = "YAMLRoot"
PYDANTIC = "pydantic"
PYDANTIC_STRICT = (
    "pydantic_strict"  ## TODO: https://docs.pydantic.dev/latest/usage/types/strict_types/
)
PYTHON_DATACLASSES = "python_dataclasses"
JSON_SCHEMA = "jsonschema"
FRAMEWORK = str  ## pydantic, java, etc
GENERATORS: Dict[FRAMEWORK, Type[Generator]] = {
    PYDANTIC: generators.PydanticGenerator,
    PYTHON_DATACLASSES: generators.PythonGenerator,
    JSON_SCHEMA: generators.JsonSchemaGenerator,
}
