"""Install the transient-network retry into a Jupyter kernel subprocess.

The notebook tests execute each notebook through ``nbconvert``'s
``ExecutePreprocessor``, which launches a *separate* kernel process. Neither
the ``retry_transient_network`` fixture nor ``requests_cache`` reaches that
process -- it never imports ``tests/conftest.py`` -- so notebooks fetching over
the network have always done so live and unprotected. That is how a dropped
connection to raw.githubusercontent.com fails ``context_issue.ipynb``.

The notebook test fixture puts this directory on ``PYTHONPATH``, so Python
imports this module during kernel startup and the retry applies inside the
kernel too.

``tests/network_retry.py`` is loaded by path rather than as ``tests.network_retry``
because importing the ``tests`` package would execute ``tests/__init__.py``,
pulling all of ``linkml`` into every kernel before ``site`` has finished.
"""

import importlib.util
from pathlib import Path

_SOURCE = Path(__file__).resolve().parent.parent / "network_retry.py"

_spec = importlib.util.spec_from_file_location("_linkml_test_network_retry", _SOURCE)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

# Never uninstalled: the kernel process exists only to run one notebook.
_module.install()
