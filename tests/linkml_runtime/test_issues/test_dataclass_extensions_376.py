import sys
import pytest
from dataclasses import dataclass
from typing import Optional
import importlib

# Only import the LinkML patch module on supported Python versions
# Python 3.13+ removed dataclasses._create_fn, which breaks this patch.
if sys.version_info < (3, 13):
    import linkml_runtime.utils.dataclass_extensions_376 as dc_tweak

    DC_IN = dc_tweak.DC_CREATE_FN
else:
    dc_tweak = None
    DC_IN = False


@pytest.mark.skipif(sys.version_info >= (3, 13), reason="LinkML dataclass patch no longer supported in Python 3.13+")
def test_kwargs_passed_to_post_init():
    """Test that kwargs are passed to __post_init__ in patched dataclass"""

    @dataclass
    class TestClass:
        a: Optional[int] = 0
        b: Optional[str] = None

        def __post_init__(self, **kwargs):
            if kwargs:
                unknown_args = sorted(kwargs.keys())
                first_arg = unknown_args[0]
                raise ValueError(f"Unknown argument: {first_arg} = {repr(kwargs[first_arg])}")

    # No extra kwargs – should not raise
    TestClass(a=1, b="test")

    # One unknown kwarg – should raise
    with pytest.raises(ValueError, match="Unknown argument: c = 'unknown'"):
        TestClass(a=1, b="test", c="unknown")

    # Multiple unknown kwargs – should raise, first alphabetically
    with pytest.raises(ValueError, match="Unknown argument: c = 'unknown'"):
        TestClass(a=1, b="test", c="unknown", z="also_unknown")


@pytest.mark.skipif(sys.version_info < (3, 13), reason="This test only applies to Python 3.13+")
def test_patch_module_is_ignored_on_python_3_13_plus():
    """Ensure the patch module is importable and emits a DeprecationWarning on Python 3.13+"""
    with pytest.warns(DeprecationWarning, match="deprecated and will be removed in a future release"):
        import importlib.util

        spec = importlib.util.find_spec("linkml_runtime.utils.dataclass_extensions_376")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

