import unittest

import requests

from linkml.generators.yumlgen import YumlGenerator
from tests.test_issues.environment import env


class Issue12UnitTest(unittest.TestCase):
    def test_domain_slots(self):
        """ has_phenotype shouldn't appear in the UML graph """
        yuml = YumlGenerator(env.input_path('issue_12.yaml')).serialize()
        self.assertEqual('https://yuml.me/diagram/nofunky;dir:TB/class/[BiologicalEntity]++- '
                         'required thing 0..1>[PhenotypicFeature],[BiologicalEntity]', yuml)
        resp = requests.get(yuml)
        self.assertTrue(resp.ok)



if __name__ == '__main__':
    unittest.main()
