import unittest
from unittest import TestCase
from linkml_runtime.utils.schemaview import SchemaView

from tests.test_issues.environment import env


class Issue478TestCase(TestCase):
    """
    https://github.com/linkml/linkml/issues/478
    """
    env = env

    def test_issue_478(self):
        view = SchemaView(env.input_path('linkml_issue_478.yaml'))
        for c in view.all_classes():
            print(f'c={c}')
        cnames = list(view.class_name_mappings().keys())
        snames = list(view.slot_name_mappings().keys())
        print(cnames)
        print(snames)
        cnames.remove("5'Sequencing")  ## TODO
        self.assertCountEqual(['FooBar', 'NamedThing', 'BiosampleProcessing', 'TooMuchWhitespace'], cnames)
        snames.remove("5'_sequence")  ## TODO
        self.assertCountEqual(['id', 'preferred_label', 'SOURCE', 'processingMethod'], snames)




if __name__ == "__main__":
    unittest.main()
