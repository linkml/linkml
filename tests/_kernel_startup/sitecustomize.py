"""Install the offline network guard into a Jupyter kernel subprocess.

The notebook tests execute each notebook through ``nbconvert``'s
``ExecutePreprocessor``, which launches a *separate* kernel process. The
``network_guard`` fixture in ``tests/conftest.py`` never reaches that process
-- it does not import ``tests/conftest.py`` -- so notebook fetches would
otherwise go out live and unguarded. That is how a dropped connection to
raw.githubusercontent.com used to fail ``context_issue.ipynb``.

The notebook test fixture puts this directory on ``PYTHONPATH`` (unless
``--with-network`` asked for live access), so Python imports this module
during kernel startup and the same stub-or-error rules apply inside the
kernel: mapped URLs are served from the repo, anything else raises.

``tests/offline_network.py`` is loaded by path rather than as
``tests.offline_network`` because importing the ``tests`` package would
execute ``tests/__init__.py``, pulling all of linkml into every kernel before
``site`` has finished. The guard module keeps its own ``linkml_runtime``
import lazy for the same reason.
"""

import importlib.util
from pathlib import Path

_SOURCE = Path(__file__).resolve().parent.parent / "offline_network.py"

_spec = importlib.util.spec_from_file_location("_linkml_test_offline_network", _SOURCE)
if _spec is None or _spec.loader is None:
    raise ImportError(f"could not load the offline network guard from {_SOURCE}")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)

# Never uninstalled: the kernel process exists only to run one notebook.
_module.install("stub")
