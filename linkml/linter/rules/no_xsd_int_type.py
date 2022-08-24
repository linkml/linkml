from linkml_runtime import SchemaView

from ..linter import LinterProblem, LinterRule


class NoXsdIntTypeRule(LinterRule):
    id = "no_xsd_int_type"

    def check(self, schema_view: SchemaView, fix: bool = False):
        for type_name, type_definition in schema_view.all_types(imports=False).items():
            if type_definition.uri == "xsd:int":
                if fix:
                    type_definition.uri = "xsd:integer"
                else:
                    yield LinterProblem(f"Type '{type_name}' has uri xsd:int")
