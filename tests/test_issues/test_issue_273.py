import unittest

from linkml.generators.sqlddlgen import SQLDDLGenerator
from tests.test_issues.environment import env
# from linkml.utils.sqlutils import SqlTransformer
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueSQLGenTestCase(TestEnvironmentTestCase):
    env = env

    def test_sqlddlgen(self):
        PATH = env.input_path('issue_273.yaml')
        dialects = ['mssql+pyodbc', 'sqlite+pysqlite', 'mysql+pymysql', 'postgresql+pygresql']
        for dialect in dialects:
            gen = SQLDDLGenerator(PATH, dialect=dialect)
            ddl = gen.serialize()
            with open(env.expected_path(f'issue_273_{dialect.replace("+","_")}.sql'), "w") as io:
                io.write(ddl)
            gen.write_sqla_python_imperative('test_schema')
        print(ddl)





if __name__ == '__main__':
    unittest.main()
