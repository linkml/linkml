import logging

from linkml.generators.docgen import DocGenerator
from tests.test_generators.test_docgen import assert_mdfile_contains

logger = logging.getLogger(__name__)


def test_deprecation(personinfo_path, tmp_path):
    gen = DocGenerator(personinfo_path, mergeimports=True, no_types_dir=True)
    gen.serialize(directory=str(tmp_path))

    # check that the slot markdown page for "deprecation_test_slot"
    # contains the expected deprecation banner
    assert_mdfile_contains(tmp_path / "deprecation_test_slot.md", "(DEPRECATED)")
