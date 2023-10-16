import pytest

from linkml.generators.sqlddlgen import SQLDDLGenerator


@pytest.mark.parametrize("dialect", ["mssql+pyodbc", "sqlite+pysqlite", "mysql+pymysql", "postgresql+psycopg2"])
def test_sqlddlgen(dialect, input_path, snapshot):
    PATH = input_path("issue_273.yaml")

    gen = SQLDDLGenerator(PATH, dialect=dialect)
    ddl = gen.serialize()
    assert ddl == snapshot(f'issue_273_{dialect.replace("+","_")}.sql')
