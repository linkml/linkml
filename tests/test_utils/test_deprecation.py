import pytest
from operator import le, lt, gt, ge, eq
import warnings
from copy import deepcopy

from linkml.utils import deprecation as dep_mod
from linkml.utils.deprecation import SemVer, DEPRECATIONS, Deprecation, deprecation_warning, EMITTED

all_ops = {le, lt, gt, ge, eq}


@pytest.fixture(scope="function")
def patch_deprecations():
    save_deps = deepcopy(dep_mod.DEPRECATIONS)
    yield dep_mod.DEPRECATIONS
    dep_mod.DEPRECATIONS = save_deps


@pytest.mark.parametrize(
    "v1,v2,ops",
    [
        ["1.0.0", "2.0.0", [le, lt]],
        ["2.0.0", "1.0.0", [ge, gt]],
        ["0.1.0", "0.2.0", [le, lt]],
        ["0.2.0", "0.1.0", [ge, gt]],
        ["0.0.1", "0.0.2", [le, lt]],
        ["0.0.2", "0.0.1", [ge, gt]],
        ["1.1.1", "1.1.1", [le, ge, eq]],
        ["1.2.3", "3.2.1", [le, lt]],
        ["3.2.1", "1.2.3", [ge, gt]],
        ["v1.2.3", "1.2.3", [le, ge, eq]],
        ["0.0.0.post2223.dev0+0c3afa90", "0.0.0.post9999.dev9+0c3afa90", [le, ge, eq]],
    ],
)
def test_semver(v1, v2, ops):
    v1 = SemVer.from_str(v1)
    v2 = SemVer.from_str(v2)
    for op in ops:
        assert op(v1, v2)
    for false_op in all_ops - set(ops):
        assert not false_op(v1, v2)


def test_deprecation(patch_deprecations):
    current_ver = SemVer.from_package("linkml")
    not_dep_yet = Deprecation(
        name="test-not-dep-yet",
        deprecated_in=SemVer(major=current_ver.major + 1, minor=0, patch=0),
        message="not deprecated yet",
    )
    is_dep = Deprecation(
        name="test-is-deprecated",
        deprecated_in=SemVer(major=current_ver.major - 1, minor=0, patch=0),
        removed_in=SemVer(major=current_ver.major + 1, minor=0, patch=0),
        message="is deprecated but not removed",
        recommendation="do nothing because this is a test",
    )
    is_removed = Deprecation(
        name="test-is-removed",
        deprecated_in=SemVer(major=current_ver.major - 2, minor=0, patch=0),
        removed_in=SemVer(major=current_ver.major - 1, minor=0, patch=0),
        message="is removed and deprecated",
        recommendation="you are fine, this is still a test",
    )
    dep_mod.DEPRECATIONS = (not_dep_yet, is_dep, is_removed)

    # no warnings emitted for not deprecated
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        deprecation_warning("test-not-dep-yet")

    # deprecation warning emitted only once for deprecated feature
    with pytest.warns() as record:
        deprecation_warning("test-is-deprecated")
        deprecation_warning("test-is-deprecated")
        assert len(record) == 1
        assert isinstance(record[0].message, DeprecationWarning)
        msg = str(record[0].message)
        for part in ("DEPRECATED", "Deprecated In:", "Removed In:", "Recommendation:", is_dep.message):
            assert part in msg

    # removed behaves similarly
    with pytest.warns() as record:
        deprecation_warning("test-is-removed")
        deprecation_warning("test-is-removed")
        assert len(record) == 1
        assert isinstance(record[0].message, DeprecationWarning)
        msg = str(record[0].message)
        for part in ("REMOVED", "Deprecated In:", "Removed In:", "Recommendation:", is_removed.message):
            assert part in msg

    # emitted deprecation warnings are added to the emitted set
    assert "test-is-deprecated" in EMITTED
    assert "test-is-removed" in EMITTED


def test_removed_are_removed():
    """
    Test that any Deprecation marked as having been removed in this version have been.

    If the tests are being run after having been checked out without tags, then will emit a warning.

    This test should not be renamed, see ``conftest.pytest_collection_modifyitems`` , which uses its
    name to ensure that it runs last
    """

    ver = SemVer.from_package("linkml")
    if ver.major == 0 and ver.minor == 0 and ver.patch == 0:
        warnings.warn(f"Version detected as {str(ver)}, deprecations will not be tested")
        return

    removed = [dep for dep in DEPRECATIONS if dep.removed and not dep.name.startswith("test-")]
    for removed in removed:
        assert removed.name not in EMITTED
