import unittest

from linkml.generators.sqlddlgen import SQLDDLGenerator
from tests.test_issues.environment import env
# from linkml.utils.sqlutils import SqlTransformer
from tests.utils.test_environment import TestEnvironmentTestCase


class IssueSQLGenTestCase(TestEnvironmentTestCase):
    env = env

    @unittest.skip("Issue 288 needs to be fixed")
    def test_sqlddlgen(self):
        PATH = env.input_path('issue_288.yaml')
        ddl = SQLDDLGenerator(PATH, dialect='mssql+pyodbc').serialize()
        with open(env.input_path('issue_288.sql'), "w") as io:
            io.write(ddl)
        print(ddl)





if __name__ == '__main__':
    unittest.main()
