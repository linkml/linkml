from collections import defaultdict
from typing import IO, Any, List, Optional

from linkml.linter.config.datamodel.config import RuleLevel
from linkml.linter.linter import LinterProblem

from .formatter import Formatter


class MarkdownFormatter(Formatter):
    def __init__(self, file: Optional[IO[Any]] = None) -> None:
        super().__init__(file)
        self.total = 0
        self.total_errors = 0
        self.total_warnings = 0
        self.schemas_with_error = set()
        self.schemas_with_warning = set()
        self.problems = defaultdict(list)

    def start_schema(self, name: str):
        self.total += 1
        self.current_schema = name

    def handle_problem(self, problem: LinterProblem):
        if str(problem.level) == RuleLevel.warning.text:
            self.total_warnings += 1
            self.schemas_with_warning.add(self.current_schema)
        elif str(problem.level) == RuleLevel.error.text:
            self.total_errors += 1
            self.schemas_with_error.add(self.current_schema)
        self.problems[self.current_schema].append(problem)

    def write_summary(self):
        self.write(
            f"""
## Summary

|                      | Count |
|----------------------|-------|
| Schemas Checked      | {self.total} |
| Schemas with Error   | {len(self.schemas_with_error)} |
| Schemas with Warning | {len(self.schemas_with_warning)} |
| Total Errors         | {self.total_errors} |
| Total Warnings       | {self.total_warnings} |

"""
        )

    def write_details(self):
        if len(self.problems):
            self.write("## Problems per Schema\n")
            for name, problems in self.problems.items():
                self.write(f"### {name}")
                self.write_schema_problems(problems)

    def write_schema_problems(self, problems: List[LinterProblem]):
        errors = [p for p in problems if str(p.level) == RuleLevel.error.text]
        warnings = [p for p in problems if str(p.level) == RuleLevel.warning.text]
        if errors:
            self.write("#### Errors")
            for error in errors:
                self.write_problem(error)

        if warnings:
            self.write("#### Warnings")
            for warning in warnings:
                self.write_problem(warning)

        self.write("")

    def write_problem(self, problem: LinterProblem):
        formatted = "* "
        if problem.rule_name:
            formatted += problem.rule_name + ": "
        formatted += problem.message
        self.write(formatted)

    def end_report(self):
        self.write_summary()
        self.write_details()
