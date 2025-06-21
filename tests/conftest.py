import os
import re
import shutil
import sys
from abc import ABC, abstractmethod
from importlib.abc import MetaPathFinder
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Optional, Union

import docker
import pytest
import requests_cache
from _pytest.assertion.util import _diff_text
from linkml_runtime.linkml_model.meta import SchemaDefinition

import tests
from tests.utils.compare_rdf import compare_rdf
from tests.utils.dirutils import are_dir_trees_equal

KITCHEN_SINK_PATH = str(Path(__file__).parent / "test_generators" / "input" / "kitchen_sink.yaml")

# avoid an error from nbconvert -> jupyter_core. remove this after jupyter_core v6
os.environ["JUPYTER_PLATFORM_DIRS"] = "1"

UNSAFE_PATHS = re.compile(r"[^\w_.-]")


def normalize_line_endings(string: str):
    return string.replace("\r\n", "\n").replace("\r", "\n")


class Snapshot(ABC):
    def __init__(self, path: Path, config: pytest.Config) -> None:
        self.path = Path(path)
        self.config = config
        self.eq_state = ""

    def __eq__(self, other: object) -> bool:
        __tracebackhide__ = True
        if self.config.getoption("generate_snapshots"):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            return self.generate_snapshot(other)
        else:
            if not self.path.exists():
                raise FileNotFoundError(
                    f"snapshot {self.path} does not exist. To generate snapshot run test with --generate-snapshots"
                )
            return self.compare_to_snapshot(other)

    @abstractmethod
    def generate_snapshot(self, updated: object) -> bool:
        pass

    @abstractmethod
    def compare_to_snapshot(self, other: object) -> bool:
        pass


class SnapshotFile(Snapshot):
    def __init__(self, path: Path, config: pytest.Config, *, rdf_format: Optional[str] = None) -> None:
        super().__init__(path, config)
        self.rdf_format: Optional[bool] = rdf_format

    def __repr__(self):
        with open(self.path, encoding="utf-8") as snapshot_file:
            return snapshot_file.read()

    def generate_snapshot(self, source: object) -> bool:
        # if we got a path, copy it into the snapshot directory
        if isinstance(source, Path):
            shutil.copy2(source, self.path)
            return True
        # if we got a string, use that as the content for the snapshot file
        if isinstance(source, str):
            with open(self.path, "w", encoding="utf-8") as dest_file:
                dest_file.write(source)
            return True
        # we got something we don't know how to handle
        __tracebackhide__ = True
        raise TypeError(f"cannot generate snapshot from {source}")

    def compare_to_snapshot(self, other: object) -> bool:
        with open(self.path, encoding="utf-8") as snapshot_file:
            expected = snapshot_file.read()

        if isinstance(other, Path):
            with open(other, encoding="utf-8") as compare_file:
                actual = compare_file.read()
        elif isinstance(other, str):
            actual = other
        else:
            __tracebackhide__ = True
            raise TypeError(f"cannot compare snapshot to {other}")

        if self.rdf_format or self.path.suffix in (".ttl", ".owl", ".n3"):
            self.eq_state = compare_rdf(expected, actual, fmt=self.rdf_format if self.rdf_format else "turtle")
            return self.eq_state is None
        else:
            is_eq = normalize_line_endings(actual) == expected
            if not is_eq:
                # TODO: probably better to use something other than this pytest
                # private method. See https://docs.python.org/3/library/difflib.html
                self.eq_state = "\n".join(_diff_text(actual, expected, self.config.getoption("verbose")))
            return is_eq


class SnapshotDirectory(Snapshot):
    def __init__(self, path: Path, config: pytest.Config) -> None:
        super().__init__(path, config)

    def generate_snapshot(self, source: object) -> bool:
        # if we got a path, recursively copy the whole directory into the snapshot directory
        if isinstance(source, Path):
            shutil.rmtree(self.path, ignore_errors=True)
            shutil.copytree(source, self.path)
            return True
        # we got something we don't know how to handle
        __tracebackhide__ = True
        raise TypeError(f"cannot generate snapshot from {source}")

    def compare_to_snapshot(self, other: object) -> bool:
        if isinstance(other, Path):
            self.eq_state = are_dir_trees_equal(self.path, other)
            return self.eq_state is None
        else:
            __tracebackhide__ = True
            raise TypeError(f"cannot compare snapshot to {other}")


@pytest.fixture
def snapshot_path(request) -> Callable[[Union[str, Path]], Path]:
    def get_path(relative_path: Union[str, Path]):
        return request.path.parent / "__snapshots__" / relative_path

    return get_path


@pytest.fixture
def snapshot(snapshot_path, pytestconfig, monkeypatch) -> Callable[[Union[str, Path]], Snapshot]:
    # Patching SchemaDefinition's setter here prevents metadata that can be variable
    # between systems from entering the snapshot files. This could be part of its own
    # fixture but it's not clear if it would be useful outside of tests that
    # compare/produce snapshots
    locked = {
        "source_file_date": "2000-01-01T00:00:00",
        "source_file_size": 1,
        "generation_date": "2000-01-01T00:00:00",
    }
    orig = SchemaDefinition.__setattr__

    def patched(self, name, value):
        new_value = locked.get(name, value)
        orig(self, name, new_value)

    monkeypatch.setattr(SchemaDefinition, "__setattr__", patched)

    def get_snapshot(relative_path: Union[str, Path], **kwargs):
        path = snapshot_path(relative_path)
        if not path.suffix:
            return SnapshotDirectory(path, pytestconfig)
        else:
            return SnapshotFile(path, pytestconfig, **kwargs)

    return get_snapshot


@pytest.fixture(scope="module")
def input_path(request) -> Callable[[str], Path]:
    def get_path(filename):
        return str(request.path.parent / "input" / filename)

    return get_path


@pytest.fixture(scope="function")
def temp_dir(request) -> Path:
    base = Path(request.path.parent) / "temp"
    test_dir = base / UNSAFE_PATHS.sub("_", request.node.name)
    test_dir.mkdir(exist_ok=True, parents=True)
    yield test_dir
    if not request.config.getoption("with_output"):
        shutil.rmtree(test_dir, ignore_errors=True)


def pytest_addoption(parser):
    parser.addoption(
        "--generate-snapshots",
        action="store_true",
        help="Generate new files into __snapshot__ directories instead of checking against existing files",
    )
    parser.addoption("--with-slow", action="store_true", help="include tests marked slow")
    parser.addoption("--with-network", action="store_true", help="include tests marked network")
    parser.addoption(
        "--with-output", action="store_true", help="dump output in compliance test for richer debugging information"
    )
    parser.addoption("--without-cache", action="store_true", help="Don't use a sqlite cache for network requests")
    parser.addoption("--with-biolink", action="store_true", help="Include tests marked as for the biolink model")


def pytest_collection_modifyitems(config, items: list[pytest.Item]):
    if not config.getoption("--with-slow"):
        skip_slow = pytest.mark.skip(reason="need --with-slow option to run")
        for item in items:
            if item.get_closest_marker("slow"):
                item.add_marker(skip_slow)

    if not config.getoption("--with-biolink"):
        skip_biolink = pytest.mark.skip(reason="need --with-biolink option to run")
        for item in items:
            if item.get_closest_marker("biolink"):
                item.add_marker(skip_biolink)

    if not config.getoption("--with-network"):
        skip_network = pytest.mark.skip(reason="need --with-network option to run")
        for item in items:
            if item.get_closest_marker("network"):
                item.add_marker(skip_network)

    # make sure deprecation test happens at the end
    test_deps = [i for i in items if i.name == "test_removed_are_removed"]
    if len(test_deps) == 1:
        items.remove(test_deps[0])
        items.append(test_deps[0])

    # numpydantic only supported python>=3.9
    if sys.version_info.minor < 9 or version("pydantic").startswith("1"):
        skip_npd = pytest.mark.skip(reason="Numpydantic is only supported in python>=3.9 and with pydantic>=2")
        for item in items:
            if item.get_closest_marker("pydanticgen_npd"):
                item.add_marker(skip_npd)

    # skip docker tests when docker server not present on the system
    if not _docker_server_running():
        skip_docker = pytest.mark.skip(reason="Docker server not running on host machine")
        for item in items:
            if item.get_closest_marker("docker"):
                item.add_marker(skip_docker)

    # the fixture that mocks black import failures should always come all the way last
    # see: https://github.com/linkml/linkml/pull/2209#issuecomment-2231548078
    # this causes really hard to diagnose errors, but we can't fail a test run if
    # it's not found because then we can't run a subset of the tests.
    # so special care should be taken not to change this test in particular :)
    test_black = [i for i in items if i.name == "test_template_noblack"]
    if len(test_black) == 1:
        items.remove(test_black[0])
        items.append(test_black[0])


def pytest_sessionstart(session: pytest.Session):
    tests.WITH_OUTPUT = session.config.getoption("--with-output")
    if session.config.getoption("--generate-snapshots"):
        tests.DEFAULT_MISMATCH_ACTION = "MismatchAction.Ignore"

    _monkeypatch_pyshex()


def _monkeypatch_pyshex():
    import sys
    import typing
    from importlib.metadata import version
    from types import ModuleType
    from typing import TextIO

    if version("pyshexc") != "0.9.1":
        raise RuntimeError(
            "Pyshex has been updated, remove this monkeypatch:\n"
            "- remove this function\n"
            "- remove the call to `_monkeypatch_pyshex in `pytest_sessionstart`\n"
            "- remove the skipif mark on test_notebooks/test_nodebooks.py:test_redo_notebook\n"
        )
    typing_io = ModuleType("io")
    typing_io.TextIO = TextIO
    typing.io = typing_io
    sys.modules["typing.io"] = typing_io


def pytest_assertrepr_compare(config, op, left, right):
    if op == "==" and isinstance(right, Snapshot):
        return [f"value matches snapshot {right.path}"] + right.eq_state.split("\n")


@pytest.fixture(scope="session", autouse=True)
def patch_requests_cache(pytestconfig):
    """
    Cache network requests - for each unique network request, store it in
    an sqlite cache. only do unique requests once per session.
    """
    if pytestconfig.getoption("--without-cache"):
        yield
        return
    cache_file = Path(__file__).parent / "output" / "requests-cache.sqlite"
    requests_cache.install_cache(
        str(cache_file),
        backend="sqlite",
        urls_expire_after={"localhost": requests_cache.DO_NOT_CACHE},
    )
    requests_cache.clear()
    with requests_cache.enabled():
        yield
    requests_cache.uninstall_cache()
    # delete cache file unless we have requested it to persist for inspection
    if not pytestconfig.getoption("--with-output"):
        cache_file.unlink(missing_ok=True)


class MockImportErrorFinder(MetaPathFinder):
    """
    Fake like we don't have a module when we really do.

    see the ``mock_black_import`` fixture for example usage.

    .. note::

        you will also have to reimport any modules that potentially import the module you are removing -
        see tests/test_generators/test_pydanticgen.py:test_template_noblack for an example

    """

    def __init__(self, module: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.module = module

    def find_spec(self, fullname, path, target):
        if fullname.startswith(self.module):
            raise ImportError(f"module with name {fullname} could not be found")
        else:
            return None


@pytest.fixture(scope="function")
def mock_black_import():
    """
    Pretend like we don't have black even if we do
    """
    removed = {}
    for k, v in sys.modules.items():
        if k.startswith("black"):
            removed[k] = v
    for k in removed.keys():
        del sys.modules[k]
    meta_finder = MockImportErrorFinder("black")
    sys.meta_path.insert(0, meta_finder)

    yield removed

    sys.modules.update(removed)
    sys.meta_path.remove(meta_finder)


# --------------------------------------------------
# Helper functions ~only~
# --------------------------------------------------


def _docker_server_running() -> bool:
    try:
        _ = docker.from_env()
        return True
    except docker.errors.DockerException:
        return False
