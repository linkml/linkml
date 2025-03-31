import sys
import pytest
import importlib.util


def import_patch_module():
    """Fresh import to ensure warning is triggered"""
    spec = importlib.util.find_spec("linkml_runtime.utils.dataclass_extensions_376")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_patch_module_emits_deprecation_warning():
    """All Python versions: emits DeprecationWarning and defines compatibility symbols"""
    with pytest.warns(DeprecationWarning):
        mod = import_patch_module()

    assert hasattr(mod, "DC_CREATE_FN")
    assert hasattr(mod, "dataclasses_init_fn_with_kwargs")
    assert mod.DC_CREATE_FN is False
    assert mod.dataclasses_init_fn_with_kwargs is None


@pytest.mark.skipif(sys.version_info >= (3, 13), reason="dataclass patch behavior was only relevant pre-3.13")
def test_behavior_without_patch_pre_3_13():
    """Ensure standard dataclass behavior (no patch) in <3.13"""
    import dataclasses

    with pytest.raises(TypeError):
        @dataclasses.dataclass
        class Example:
            a: int
            def __post_init__(self, **kwargs): pass

        # This will fail because unknown kwarg 'extra' is not accepted
        Example(a=1, extra="not allowed")
