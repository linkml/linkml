"""Fixtures shared by the notebook tests.

Notebooks are executed by ``nbconvert``'s ``ExecutePreprocessor``, which starts
a separate Jupyter kernel process. That process never imports ``tests/conftest.py``,
so the ``network_guard`` fixture does not reach it.
"""

import os
from pathlib import Path

import pytest

KERNEL_STARTUP_DIR = Path(__file__).resolve().parents[2] / "_kernel_startup"


@pytest.fixture(autouse=True)
def kernel_network_guard(pytestconfig, monkeypatch):
    """Give the notebook kernel the same offline network rules as the test process.

    The kernel inherits this environment, and Python imports ``sitecustomize``
    from ``PYTHONPATH`` at startup, so adding the startup directory there is
    enough to install the guard inside the kernel. Under ``--with-network``
    the directory is not added and the kernel runs live, matching how the
    flag treats every other ``network``-marked test.
    """
    if pytestconfig.getoption("--with-network"):
        return
    existing = os.environ.get("PYTHONPATH", "")
    entries = [str(KERNEL_STARTUP_DIR), *([existing] if existing else [])]
    monkeypatch.setenv("PYTHONPATH", os.pathsep.join(entries))
