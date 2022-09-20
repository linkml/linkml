import inspect
from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, Union

import yaml
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.linkml_model import SchemaDefinition

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


def merge_configs(original: dict, other: dict):
    result = deepcopy(original)
    for key, value in other.items():
        if isinstance(value, dict):
            result[key] = merge_configs(result.get(key, {}), value)
        else:
            result[key] = value
    return result


class Linter:
    def __init__(self, config: Dict[str, Any] = {}) -> None:
        default_config = deepcopy(get_named_config("default"))
        merged_config = config
        if config.get("extends") == ExtendableConfigs.recommended.text:
            recommended_config = deepcopy(
                get_named_config(ExtendableConfigs.recommended.text)
            )
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

    def lint(
        self, schema=Union[str, SchemaDefinition], fix: bool = False
    ) -> Iterable[LinterProblem]:
        try:
            schema_view = SchemaView(schema)
        except:
            yield LinterProblem(
                message="File is not a valid LinkML schema",
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
