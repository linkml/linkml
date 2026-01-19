from typing import IO, Any, Optional

import click

from ..linter import LinterProblem


class Formatter:
    def __init__(self, file: Optional[IO[Any]] = None) -> None:
        self.file = file

    def write(self, message: str):
        click.echo(message, file=self.file)

    def start_report(self):
        pass

    def start_schema(self, name: str):
        pass

    def handle_problem(self, problem: LinterProblem):
        pass

    def end_schema(self):
        pass

    def end_report(self):
        pass
