"""Schema checks for generate_dashboard.py against the compliance test helper models.

If any test here fails, it means the Feature model or ValidationBehavior enum in
helper.py has changed in a way that generate_dashboard.py doesn't account for.
Update scripts/generate_dashboard.py to handle the changes.
"""

import importlib.util
from pathlib import Path

from tests.linkml.test_compliance.helper import Feature, ValidationBehavior

SCRIPT_PATH = Path(__file__).resolve().parents[3] / "scripts" / "generate_dashboard.py"
spec = importlib.util.spec_from_file_location("generate_dashboard", SCRIPT_PATH)
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)

# The fields that generate_dashboard.py reads from each feature dict
EXPECTED_FEATURE_FIELDS = {"name", "implementations", "category", "display_name"}


def test_dashboard_covers_all_validation_behaviors():
    """Every ValidationBehavior value must have an icon in STATUS_ICONS.

    If this fails, a new ValidationBehavior was added to helper.py but
    generate_dashboard.py doesn't know how to render it — update STATUS_ICONS
    in scripts/generate_dashboard.py.
    """
    missing = [v.value for v in ValidationBehavior if v.value not in dashboard.STATUS_ICONS]
    assert not missing, (
        f"ValidationBehavior values {missing} have no icon in "
        f"generate_dashboard.py STATUS_ICONS — update scripts/generate_dashboard.py"
    )


def test_feature_model_has_expected_fields():
    """The Feature model must still have the fields that generate_dashboard.py reads.

    If this fails, a field was removed or renamed in the Feature model in
    helper.py — update scripts/generate_dashboard.py to use the new field names.
    """
    actual_fields = set(Feature.model_fields.keys())
    missing = EXPECTED_FEATURE_FIELDS - actual_fields
    assert not missing, (
        f"Feature model no longer has fields {missing} that "
        f"generate_dashboard.py depends on — update scripts/generate_dashboard.py"
    )


def test_dashboard_roundtrip_from_feature_model():
    """A Feature instance serialized via model_dump (as summary.yaml does) must
    produce a dict that generate_dashboard.py can render without errors.

    If this fails, the serialization format has diverged from what the dashboard
    script expects — update scripts/generate_dashboard.py.
    """
    feature = Feature(
        name="test_roundtrip",
        display_name="Roundtrip check",
        category="Test",
        description="Verifies dashboard can consume Feature output",
        implementations={"pydantic": ValidationBehavior.IMPLEMENTS},
    )
    feature_dict = feature.model_dump(mode="json")

    # This is what generate_dashboard.py receives — it should not raise
    md = dashboard.generate_dashboard([feature_dict])
    assert "Roundtrip check" in md, (
        "generate_dashboard.py failed to render a Feature produced by "
        "model_dump(mode='json') — update scripts/generate_dashboard.py"
    )
