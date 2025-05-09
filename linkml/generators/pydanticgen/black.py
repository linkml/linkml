"""
Utilities for formatting pydanticgen outputs

Kept separate in case we decide we don't want it/we want it to be moved to a place
that's better for other generators to use.
"""

from typing import Optional

try:
    from black import Mode, TargetVersion, format_str
except ImportError:
    import warnings

    warnings.warn("Black is an optional dependency, install it with the extra 'black' like `pip install linkml[black]`")


def _default_mode() -> "Mode":
    return Mode(target_versions={TargetVersion.PY311}, line_length=120)


def format_black(code: str, mode: Optional["Mode"] = None) -> str:
    if mode is None:
        mode = _default_mode()

    formatted = format_str(code, mode=mode)
    return formatted
