"""Offline integrity check for the vendored linkml-model files.

``make update_model`` writes ``VENDORED_MANIFEST`` (sha256 per vendored file)
alongside ``UPSTREAM_SHA``. This test verifies the files on disk still match
it, so a vendored file edited without re-vendoring fails the PR immediately
and offline. The weekly ``upstream``-marked comparison against the pinned
upstream commit guards the manifest itself -- regenerating it by hand to make
this test pass still shows up as drift there.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[3] / "packages" / "linkml_runtime" / "generate_vendored_manifest.py"


def test_vendored_files_match_manifest():
    """Every vendored file matches its recorded checksum; none added or removed.

    Runs the same script ``make update_model`` uses to generate the manifest,
    in ``--check`` mode, so there is exactly one implementation of the hashing
    and normalisation rules.
    """
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--check"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        "Vendored linkml-model files do not match VENDORED_MANIFEST:\n"
        f"{result.stdout}"
        "If you intended to update the vendored files, run 'make update_model' in "
        "packages/linkml_runtime/ rather than editing them in place."
    )
