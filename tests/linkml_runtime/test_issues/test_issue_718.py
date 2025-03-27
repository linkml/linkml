import pytest
from dataclasses import dataclass
from typing import Optional, ClassVar

import yaml

from linkml_runtime.utils.yamlutils import YAMLRoot, DupCheckYamlLoader


@pytest.mark.xfail(reason='Reporting line numbers should happen at load time not when instantiating dataclasses')
def test_issue_38():
    # The goal is to provide line numbers on error messages.   We've tweaked the parser so that it returns augmented
    # str's and int's with the line numbers on them.  The problem we are trying to address now is that the dataclass
    # constructor doesn't support **argv out of the box.  We can certainly tweak the generator to emit the __init__
    # method to do this, but it would be really handy

    @dataclass
    class FesterBesterTester(YAMLRoot):
        cv: ClassVar[int] = 42

        a: Optional[int] = 0
        b: Optional[str] = None

    with pytest.raises(TypeError, match="unexpected keyword argument 'c'"):
        FesterBesterTester(a=12, b="Sell", c="buy")

    yaml_str = """base:
        a: 17
        b: Ice Cream
        c: sell"""

    parsed_yaml = yaml.load(yaml_str, DupCheckYamlLoader)
    with pytest.raises(TypeError, match="File \"<unicode string>\", line 4, col 9"):
        FesterBesterTester(**parsed_yaml['base'])

    parsed_yaml['base'].pop('c', None)

    instance = FesterBesterTester(**parsed_yaml['base'])
    assert instance.a == 17
    assert instance.b == "Ice Cream"

