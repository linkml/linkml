"""Test remote imports using SchemaView.

See https://github.com/linkml/linkml/issues/1317
"""

import pytest

from linkml_runtime.utils.schemaview import SchemaView

URL = (
    "https://raw.githubusercontent.com/linkml/linkml-runtime/"
    "2a46c65fe2e7db08e5e524342e5ff2ffb94bec92/tests/test_utils/input/kitchen_sink.yaml"
)

MIXS_URL = (
    "https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/"
    "83be82a99d0a210e83b371b20b3dadb6423ec612/model/schema/mixs.yaml"
)


def test_view_created() -> None:
    """Test_remote_modular_schema_view."""
    sv = SchemaView(URL)
    assert sv.schema.name == "kitchen_sink"


def test_imported_classes_present() -> None:
    """Test_remote_modular_schema_view."""
    sv = SchemaView(URL)
    class_count = len(sv.all_classes())
    assert class_count > 0
    assert "activity" in sv.all_classes()
    assert "activity" in sv.all_classes(imports=True)
    assert "activity" not in sv.all_classes(imports=False)


def test_mixs() -> None:
    """Test loading from a remote repo.

    Note this test case involves using an external github repo.

    We use commit hashes to avoid false positive test fails caused by repo changes,
    but in theory this test could break if the mixs repo is deleted or changes its
    name or org.

    We will likely keep skipping this for now, but once stabilized it can be unskipped

    Note that the sam functionality is likely captured in the other tests that use
    a more stable repo.
    """
    pytest.skip("Test is slow and may be fragile")
    sv = SchemaView(MIXS_URL)
    assert len(sv.all_classes()) > 0
