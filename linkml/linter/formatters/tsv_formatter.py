import csv
import io
from typing import IO, Any, Optional

from ..linter import LinterProblem
from .formatter import Formatter


class TsvFormatter(Formatter):
    def __init__(self, file: Optional[IO[Any]] = None) -> None:
        super().__init__(file)
        self.output = io.StringIO()
        self.writer = csv.writer(self.output, delimiter="\t", quoting=csv.QUOTE_MINIMAL)

    def start_report(self):
        self.writer.writerow(["source", "schema name", "rule name", "level", "message"])

    def handle_problem(self, problem: LinterProblem):
        self.writer.writerow(
            [
                problem.schema_source,
                problem.schema_name,
                problem.rule_name,
                str(problem.level),
                problem.message,
            ]
        )

    def end_report(self):
        self.write(self.output.getvalue())
