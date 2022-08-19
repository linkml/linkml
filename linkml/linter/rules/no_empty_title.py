import re
from typing import Iterable

from linkml_runtime.utils.schemaview import SchemaView

from ..linter import LinterProblem, LinterRule


class NoEmptyTitleRule(LinterRule):
    id = "no_empty_title"

    def check(
        self, schema_view: SchemaView, fix: bool = False
    ) -> Iterable[LinterProblem]:
        for e in schema_view.all_elements(imports=False).values():
            if fix and e.title is None:
                title = e.name.replace("_", " ")
                title = self.uncamel(title).lower()
                e.title = title
            if e.title is None:
                problem = LinterProblem(
                    message=f'{type(e).__name__} "{e.name}" has no title'
                )
                yield problem
