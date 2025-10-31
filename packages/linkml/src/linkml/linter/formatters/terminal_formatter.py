from collections import defaultdict
from typing import IO, Any, Optional

import click

from linkml.linter.config.datamodel.config import RuleLevel

from ..linter import LinterProblem
from .formatter import Formatter


def plural(word: str, count: int):
    return word + ("s" if count != 1 else "")


class TerminalFormatter(Formatter):
    def __init__(self, file: Optional[IO[Any]] = None, verbose: bool = False) -> None:
        super().__init__(file)
        self.verbose = verbose
        self.problem_counts = defaultdict(int)
        self.current_schema = None

    def start_schema(self, name: str):
        self.current_schema = name
        if self.verbose:
            self.write(click.style(name, underline=True))

    def handle_problem(self, problem: LinterProblem):
        key = self.current_schema
        if not self.verbose and key not in self.problem_counts:
            self.write(click.style(key, underline=True))

        self.problem_counts[key] += 1

        formatted = click.style(
            "  " + str(problem.level).ljust(9),
            fg="yellow" if str(problem.level) is RuleLevel.warning.text else "red",
        )
        formatted += problem.message
        if problem.rule_name:
            formatted += "  " + click.style(f"({problem.rule_name})", dim=True)
        self.write(formatted)

    def end_schema(self):
        if self.verbose or self.current_schema in self.problem_counts:
            self.write("")

    def end_report(self):
        total_problems = sum(self.problem_counts.values())
        if total_problems > 0:
            problem_schemas = len(self.problem_counts)
            self.write(
                click.style("\u2716", fg="red")
                + " Found "
                + str(total_problems)
                + " "
                + plural("problem", total_problems)
                + " in "
                + str(problem_schemas)
                + " "
                + plural("schema", problem_schemas)
            )
        else:
            self.write(click.style("\u2713", fg="green") + " No problems found")
