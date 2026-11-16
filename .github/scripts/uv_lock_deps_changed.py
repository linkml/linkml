#!/usr/bin/env python3
"""Decide whether the resolved ``uv.lock`` dependency set changed between refs.

``uv.lock`` is regenerated non-deterministically: reordering, hashes, and
metadata can differ between two lockfiles that resolve to exactly the same
packages. ``uv audit`` only cares about the multiset of ``(name, version)``
pairs, so this script compares that set between a base ref and ``HEAD`` and
prints ``true`` only when it actually differs.

Usage:
    uv_lock_deps_changed.py <base_ref>

Prints ``true`` when the resolved ``(name, version)`` set at ``HEAD`` differs
from the one at ``<base_ref>`` (or when the lockfile is absent at either ref),
otherwise ``false``.
"""

from __future__ import annotations

import subprocess
import sys
import tomllib


def package_set(ref: str) -> set[tuple[str, str | None]] | None:
    """Return the ``{(name, version)}`` set from ``uv.lock`` at ``ref``.

    Args:
        ref: A git ref (SHA, branch, ``HEAD``) to read ``uv.lock`` from.

    Returns:
        The set of ``(name, version)`` tuples for every locked package, or
        ``None`` if ``uv.lock`` does not exist at ``ref``.
    """
    result = subprocess.run(
        ["git", "show", f"{ref}:uv.lock"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    data = tomllib.loads(result.stdout)
    return {(pkg["name"], pkg.get("version")) for pkg in data.get("package", [])}


def resolved_set_changed(base_ref: str) -> bool:
    """Return whether the resolved dependency set differs between refs.

    Args:
        base_ref: The ref to compare ``HEAD`` against.

    Returns:
        ``True`` if the ``(name, version)`` set differs, or if ``uv.lock`` is
        missing at either ref; ``False`` when the sets are identical.
    """
    base = package_set(base_ref)
    head = package_set("HEAD")
    return base is None or head is None or base != head


def main() -> None:
    """Print ``true``/``false`` for the base ref given as the sole argument."""
    print("true" if resolved_set_changed(sys.argv[1]) else "false")


if __name__ == "__main__":
    main()
