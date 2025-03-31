import sys
import unittest
from dataclasses import dataclass
from typing import Optional
import pytest

# Only import the LinkML patch module on supported Python versions
# Python 3.13+ removed dataclasses._create_fn, which breaks this patch.
# The test will be skipped on versions > 3.13.0.
if sys.version_info < (3, 13):
    import linkml_runtime.utils.dataclass_extensions_376 as dc_tweak
    DC_IN = dc_tweak.DC_CREATE_FN
else:
    dc_tweak = None
    DC_IN = False


@pytest.mark.skipif(sys.version_info >= (3, 13), reason="LinkML dataclass patch no longer supported in Python 3.13+")
class DataclassExtensionsTestCase(unittest.TestCase):
    """Test the dataclass_extensions_376 module with Python <3.13"""

    @dataclass
    class TestClass:
        a: Optional[int] = 0
        b: Optional[str] = None

        def __post_init__(self, **kwargs):
            if kwargs:
                unknown_args = sorted(kwargs.keys())
                first_arg = unknown_args[0]
                raise ValueError(f"Unknown argument: {first_arg} = {repr(kwargs[first_arg])}")

    def test_kwargs_passed_to_post_init(self):
        self.TestClass(a=1, b="test")

        with self.assertRaises(ValueError) as e:
            self.TestClass(a=1, b="test", c="unknown")
        self.assertEqual("Unknown argument: c = 'unknown'", str(e.exception))

        with self.assertRaises(ValueError) as e:
            self.TestClass(a=1, b="test", c="unknown", z="also_unknown")
        self.assertEqual("Unknown argument: c = 'unknown'", str(e.exception))


if __name__ == '__main__':
    unittest.main()
