import unittest
import sys
import dataclasses
from dataclasses import dataclass, InitVar, field, fields
from typing import Optional, ClassVar, Dict, Any

import yaml

from linkml_runtime.utils.yamlutils import YAMLRoot, TypedNode, DupCheckYamlLoader

from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs


class Issue83TestCase(unittest.TestCase):
    # The goal is to provide line numbers on error messages.   We've tweaked the parser so that it returns augmented
    # str's and int's with the line numbers on them.  The problem we are trying to address now is that the dataclass
    # constructor doesn't support **argv out of the box.  We can certainly tweak the generator to emit the __init__
    # method to do this, but it would be really handy

    @dataclass
    class FesterBesterTester(YAMLRoot):
        cv: ClassVar[int] = 42

        a: Optional[int] = 0
        b: Optional[str] = None

    def test_initvar(self):
        with self.assertRaises(ValueError) as e:
            Issue83TestCase.FesterBesterTester(a=12, b="Sell", c="buy")
        self.assertEqual("Unknown argument: c = 'buy'", str(e.exception).strip())
        yaml_str = """base:
        a: 17
        b: Ice Cream
        c: sell
"""
        parsed_yaml = yaml.load(yaml_str, DupCheckYamlLoader)
        with self.assertRaises(ValueError) as e:
            Issue83TestCase.FesterBesterTester(**parsed_yaml['base'])
        self.assertEqual('File "<unicode string>", line 4, col 9:  Unknown argument: c = \'sell\'',
                         str(e.exception).strip())

        parsed_yaml['base'].pop('c', None)
        try:
            Issue83TestCase.FesterBesterTester(**parsed_yaml['base'])
        except Exception as e:
            self.fail(f'Raised exception unexpectedly: {str(e.exception)}')


if __name__ == '__main__':
    unittest.main()
