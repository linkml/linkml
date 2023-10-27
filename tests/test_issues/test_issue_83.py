import dataclasses
from dataclasses import dataclass
from typing import ClassVar, Optional

import pytest
import yaml
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.yamlutils import DupCheckYamlLoader, YAMLRoot

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs


# The goal is to provide line numbers on error messages.   We've tweaked the parser so that it returns augmented
# str's and int's with the line numbers on them.  The problem we are trying to address now is that the dataclass
# constructor doesn't support **argv out of the box.  We can certainly tweak the generator to emit the __init__
# method to do this, but it would be really handy


@dataclass
class FesterBesterTester(YAMLRoot):
    cv: ClassVar[int] = 42

    a: Optional[int] = 0
    b: Optional[str] = None


def test_initvar():
    with pytest.raises(ValueError, match=r"Unknown argument: c = 'buy'"):
        FesterBesterTester(a=12, b="Sell", c="buy")
    yaml_str = """base:
    a: 17
    b: Ice Cream
    c: sell
"""
    parsed_yaml = yaml.load(yaml_str, DupCheckYamlLoader)
    with pytest.raises(ValueError, match="File \"<unicode string>\", line 4, col 5:  Unknown argument: c = 'sell'"):
        FesterBesterTester(**parsed_yaml["base"])

    parsed_yaml["base"].pop("c", None)
    FesterBesterTester(**parsed_yaml["base"])
