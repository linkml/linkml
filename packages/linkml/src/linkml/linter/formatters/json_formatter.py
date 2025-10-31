import json
from typing import IO, Any, Optional

from ..config.datamodel.config import RuleLevel
from ..linter import LinterProblem
from .formatter import Formatter


class Encoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, LinterProblem):
            return o.__dict__
        if isinstance(o, RuleLevel):
            return str(o)
        return json.JSONEncoder.default(self, o)


class JsonFormatter(Formatter):
    def __init__(self, file: Optional[IO[Any]] = None) -> None:
        super().__init__(file)
        self.problems = []

    def handle_problem(self, problem: LinterProblem):
        self.problems.append(problem)

    def end_report(self):
        self.write(json.dumps(self.problems, indent=2, cls=Encoder))
