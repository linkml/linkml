import os
import shutil
from pathlib import Path

import freezegun
import pytest
from _pytest.assertion.util import _diff_text

from tests.utils.compare_rdf import compare_rdf
from tests.utils.dirutils import are_dir_trees_equal


class Snapshot:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.compare_result = None

    def _write_file_content_to_path(self, content):
        with open(self.path, "w") as snapshot_file:
            snapshot_file.write(content)

    def _copy_directory_to_path(self, src):
        shutil.rmtree(self.path)
        shutil.copytree(src, self.path)

    def _copy_file_to_path(self, src):
        shutil.copy2(src, self.path)

    def __eq__(self, other) -> None:
        if os.getenv("GENERATE_SNAPSHOTS", False):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(other, str):
                self._write_file_content_to_path(other)
            elif isinstance(other, Path):
                if other.is_dir:
                    self._copy_directory_to_path()
                else:
                    self._copy_file_to_path()
            return True
        else:
            if isinstance(other, str):
                try:
                    with open(self.path, "r") as snapshot_file:
                        self.data = snapshot_file.read()
                except FileNotFoundError:
                    raise RuntimeError(
                        f"File {self.path} does not exist. To generate snapshots run tests with GENERATE_SNAPSHOTS=true"
                    )

                if self.path.suffix == ".ttl":
                    self.compare_result = compare_rdf(other, self.data)
                    return self.compare_result is None
                else:
                    return other == self.data
            elif isinstance(other, Path):
                if not self.path.exists():
                    raise RuntimeError(
                        f"File {self.path} does not exist. To generate snapshots run tests with GENERATE_SNAPSHOTS=true"
                    )
                if other.is_dir():
                    self.compare_result = are_dir_trees_equal(self.path, other)
                    return self.compare_result is None
            else:
                return False


@pytest.fixture
def snapshot_path(request):
    def get_path(filename):
        return request.path.parent / "__snapshots__" / filename

    return get_path


@pytest.fixture
def snapshot(snapshot_path):
    def get_snapshot(filename):
        return Snapshot(snapshot_path(filename))

    return get_snapshot


@pytest.fixture
def input_path(request):
    def get_path(filename):
        return str(request.path.parent / "input" / filename)

    return get_path


@pytest.fixture(autouse=True)
def frozen_time():
    with freezegun.freeze_time("2000-01-01") as ft:
        yield ft


def pytest_assertrepr_compare(config, op, left, right):
    if op == "==" and isinstance(right, Snapshot):
        messages = [f"value matches snapshot {right.path}"]
        if right.compare_result:
            messages += right.compare_result.split("\n")
        elif right.data and isinstance(left, str):
            messages += _diff_text(left, right.data, config.getoption("verbose"))
        return messages
