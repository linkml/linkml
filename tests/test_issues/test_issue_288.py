from linkml.generators.sqlddlgen import SQLDDLGenerator


def test_sqlddlgen(input_path, snapshot):
    PATH = input_path("issue_288.yaml")
    ddl = SQLDDLGenerator(PATH, dialect="mssql+pyodbc").serialize()
    assert ddl == snapshot("issue_288.sql")
