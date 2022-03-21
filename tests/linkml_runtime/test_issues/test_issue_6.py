import unittest

import hbreader
import yaml

from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, TypedNode

inp_yaml = """
foo:
    x: 17
    y: I yam that I yam
    z: 12.43
"""


class Issue6TestCase(unittest.TestCase):
    def test_loc_function(self):
        inp = yaml.load(hbreader.hbread(inp_yaml), DupCheckYamlLoader)
        self.assertEqual('File "<unicode string>", line 3, col 8: ', TypedNode.yaml_loc(inp['foo']['x']))
        self.assertEqual('File "<unicode string>", line 3, col 8', TypedNode.yaml_loc(inp['foo']['x'], suffix=''))
        self.assertEqual('File "<unicode string>", line 4, col 8: ', TypedNode.yaml_loc(inp['foo']['y']))
        self.assertEqual('File "<unicode string>", line 4, col 8I yam that I yam',
                         TypedNode.yaml_loc(inp['foo']['y'], suffix=inp['foo']['y']))
        self.assertEqual('File "<unicode string>", line 5, col 8: ', TypedNode.yaml_loc(inp['foo']['z']))

        with self.assertWarns(DeprecationWarning) as cm:
            self.assertEqual('File "<unicode string>", line 3, col 8', TypedNode.loc(inp['foo']['x']))
        self.assertEqual('Call to deprecated method loc. (Use yaml_loc instead)', cm.warning.args[0])


        self.assertEqual('', TypedNode.yaml_loc(None))
        self.assertEqual('', TypedNode.yaml_loc("abc"))
        self.assertEqual('', TypedNode.yaml_loc(['a', 'b']))


if __name__ == '__main__':
    unittest.main()
