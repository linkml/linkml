import inspect
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, Union

import jsonschema
import yaml
from jsonschema.exceptions import best_match
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition

from linkml.generators.jsonschemagen import JsonSchemaGenerator

from .. import LOCAL_METAMODEL_YAML_FILE
from .config.datamodel.config import Config, ExtendableConfigs, RuleLevel


@dataclass
class LinterProblem:
    message: str
    level: Union[RuleLevel, None] = None
    schema_name: Union[str, None] = None
    schema_source: Union[str, None] = None
    rule_name: Union[str, None] = None


@lru_cache
def get_named_config(name: str) -> Dict[str, Any]:
    config_path = str(Path(__file__).parent / f"config/{name}.yaml")
    with open(config_path) as config_file:
        return yaml.safe_load(config_file)


@lru_cache
def get_metamodel_validator() -> jsonschema.Validator:
    meta_json_gen = JsonSchemaGenerator(LOCAL_METAMODEL_YAML_FILE, not_closed=False)
    meta_json_schema = meta_json_gen.generate()
    validator_cls = jsonschema.validators.validator_for(meta_json_schema, default=jsonschema.Draft7Validator)
    validator = validator_cls(meta_json_schema, format_checker=validator_cls.FORMAT_CHECKER)
    return validator


def merge_configs(original: dict, other: dict):
    result = deepcopy(original)
    for key, value in other.items():
        if isinstance(value, dict):
            result[key] = merge_configs(result.get(key, {}), value)
        else:
            result[key] = value
    return result


def _format_path_component(value):
    if isinstance(value, int):
        return f"[{value}]"
    return value


def _format_path(path):
    if not path:
        return "<root>"
    return " > ".join(_format_path_component(p) for p in path)


class Linter:
    def __init__(self, config: Dict[str, Any] = {}) -> None:
        default_config = deepcopy(get_named_config("default"))
        merged_config = config
        if config.get("extends") == ExtendableConfigs.recommended.text:
            recommended_config = deepcopy(get_named_config(ExtendableConfigs.recommended.text))
            merged_config = merge_configs(recommended_config, merged_config)
        merged_config = merge_configs(default_config, merged_config)
        self.config = Config(**merged_config)

        from . import rules

        self._rules_map = dict(
            [
                (cls.id, cls)
                for _, cls in inspect.getmembers(rules, inspect.isclass)
                if issubclass(cls, rules.LinterRule)
            ]
        )

    @staticmethod
    def validate_schema(schema_path: str):
        with open(schema_path) as schema_file:
            schema = yaml.safe_load(schema_file)

        validator = get_metamodel_validator()
        for err in validator.iter_errors(schema):
            best_err = best_match([err])
            message = f"In {_format_path(best_err.absolute_path)}: {best_err.message}"
            if best_err.context:
                message += f" ({', '.join(e.message for e in best_err.context)})"
            yield LinterProblem(
                rule_name="valid-schema",
                message=message,
                level=RuleLevel(RuleLevel.error),
                schema_source=schema,
            )

    def lint(
        self,
        schema: Union[str, SchemaDefinition],
        fix: bool = False,
        validate_schema: bool = False,
        validate_only: bool = False,
    ) -> Iterable[LinterProblem]:
        if (validate_schema or validate_only) and isinstance(schema, str):
            yield from self.validate_schema(schema)

        if validate_only:
            return

        try:
            schema_view = SchemaView(schema)
        except Exception:
            if not validate_schema:
                yield LinterProblem(
                    message="File is not a valid LinkML schema. Use --validate for more details.",
                    level=RuleLevel(RuleLevel.error),
                    schema_source=(schema if isinstance(schema, str) else None),
                )
            return

        for rule_id, rule_config in self.config.rules.__dict__.items():
            rule_cls = self._rules_map.get(rule_id, None)
            if rule_cls is None:
                raise ValueError("Unknown rule id: " + rule_id)

            if str(rule_config.level) is RuleLevel.disabled.text:
                continue

            rule = rule_cls(rule_config)

            for problem in rule.check(schema_view, fix=fix):
                problem.level = rule.config.level
                problem.rule_name = rule.id
                problem.schema_name = schema_view.schema.name
                if isinstance(schema, str):
                    problem.schema_source = schema
                yield problem

        if fix and schema_view.schema.source_file:
            yaml_dumper.dump(schema_view.schema, schema_view.schema.source_file)
