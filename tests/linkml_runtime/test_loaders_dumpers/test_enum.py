import unittest
import json
import yaml

from linkml_runtime.loaders import json_loader
from linkml_runtime.dumpers import json_dumper, yaml_dumper
from tests.test_loaders_dumpers.models.enum_model import Organism, StateEnum


class EnumTestCase(unittest.TestCase):

    def test_enum(self):
        """
        Tests that enums are encoded as json correctly

        * https://github.com/linkml/linkml/issues/337
        * https://github.com/linkml/linkml/issues/119
        """
        i = Organism(state='LIVING')
        print(i)
        print(i.state)
        print(i.state.code)
        print(i.state.code.text)
        print(type(i.state))
        print(StateEnum.LIVING)
        assert str(i.state) == 'LIVING'
        assert i.state.code == StateEnum.LIVING
        obj = json.loads(json_dumper.dumps(i))
        assert obj['state'] == 'LIVING'
        obj = yaml.safe_load(yaml_dumper.dumps(i))
        assert obj['state'] == 'LIVING'
        reconstituted = json_loader.loads(json_dumper.dumps(i), target_class=Organism)
        print(f'RECONSTITUTED = {reconstituted}')
        assert reconstituted.state.code == StateEnum.LIVING







if __name__ == '__main__':
    unittest.main()
