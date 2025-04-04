import sys
import pytest
import importlib.util
import dataclasses


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

    # Check consistency with actual dataclasses module
    init_fn = getattr(dataclasses, "_init_fn", None)
    assert mod.dataclasses_init_fn_with_kwargs == init_fn


