import os
import unittest

from linkml_runtime.dumpers import yaml_dumper
from linkml_runtime.loaders.yaml_loader import YAMLLoader
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.utils.ruleutils import subclass_to_rules, get_range_as_disjunction

from tests.test_utils import INPUT_DIR

SCHEMA = os.path.join(INPUT_DIR, 'rules-example.yaml')

yaml_loader = YAMLLoader()


class RuleUtilsTestCase(unittest.TestCase):

    def test_disjunction(self):
        # no import schema
        view = SchemaView(SCHEMA)
        analyte = view.induced_slot('analyte', 'Sample')
        #print(analyte)
        #print(analyte.any_of)
        disj = get_range_as_disjunction(analyte)
        #print(disj)
        self.assertCountEqual(disj, {'MissingValueEnum', 'AnalyteEnum'})
        for s in view.all_slots().values():
            disj = get_range_as_disjunction(s)
            print(f'{s.name} DISJ: {disj}')

    def test_roll_up(self):
        # no import schema
        view = SchemaView(SCHEMA)
        c = view.get_class('ProteinCodingGene')
        rules = subclass_to_rules(view, 'ProteinCodingGene', 'SeqFeature')
        rule = rules[0]
        print(f'IF: {rule.preconditions}')
        print(f'THEN: {rule.postconditions}')
        print(yaml_dumper.dumps(rule))




if __name__ == '__main__':
    unittest.main()
