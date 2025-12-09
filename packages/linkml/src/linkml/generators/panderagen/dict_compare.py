"""Dictionary comparison utilities with tolerance for float precision and null handling."""

import math
from typing import Any


def deep_compare_dicts(dict1: dict[str, Any], dict2: dict[str, Any], float_tolerance: float = 1e-7) -> bool:
    """
    Recursively compare two dictionaries for equality with special handling for:
    - Float precision differences (within tolerance)
    - Null values vs missing keys (treated as equivalent)

    Args:
        dict1: First dictionary to compare
        dict2: Second dictionary to compare
        float_tolerance: Tolerance for float comparisons (default: 1e-7)

    Returns:
        True if dictionaries are equivalent, False otherwise
    """
    all_keys = set(dict1.keys()) | set(dict2.keys())

    for key in all_keys:
        key1_exists = key in dict1
        key2_exists = key in dict2

        if not key1_exists:
            val1 = None
        else:
            val1 = dict1[key]
        if not key2_exists:
            val2 = None
        else:
            val2 = dict2[key]

        if not key1_exists and val2 is None:
            continue
        elif not key2_exists and val1 is None:
            continue
        elif not key1_exists or not key2_exists:
            return False

        if val1 is None and val2 is None:
            continue
        elif val1 is None or val2 is None:
            return False

        if isinstance(val1, dict) and isinstance(val2, dict):
            if not deep_compare_dicts(val1, val2, float_tolerance):
                return False
        elif isinstance(val1, list) and isinstance(val2, list):
            if len(val1) != len(val2):
                return False
            for item1, item2 in zip(val1, val2):
                if isinstance(item1, dict) and isinstance(item2, dict):
                    if not deep_compare_dicts(item1, item2, float_tolerance):
                        return False
                elif not _compare_values(item1, item2, float_tolerance):
                    return False
        else:
            if not _compare_values(val1, val2, float_tolerance):
                return False

    return True


def _compare_values(val1: Any, val2: Any, float_tolerance: float) -> bool:
    """Compare two values with float tolerance."""
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return math.isclose(val1, val2, abs_tol=float_tolerance)

    return val1 == val2
