from linkml_runtime.utils.schemaview import SchemaView
from tests.test_issues.environment import env


def test_issue_478() -> None:
    """Test the retrieval of normalised names and the original versions.

    See https://github.com/linkml/linkml/issues/478
    """
    view = SchemaView(env.input_path("linkml_issue_478.yaml"))

    # class names => normalised class names:
    class_names = {
        "foo bar": "FooBar",
        "named thing": "NamedThing",
        "biosample_processing": "BiosampleProcessing",
        "too   much   whitespace": "TooMuchWhitespace",
        "5' sequencing": "5'Sequencing",
    }

    assert set(view.all_classes()) == set(class_names)
    assert set(view.class_name_mappings()) == set(class_names.values())
    assert {cnm_def.name: cnm for cnm, cnm_def in view.class_name_mappings().items()} == class_names

    slot_names = {
        "id": "id",
        "preferred label": "preferred_label",
        "5' sequence": "5'_sequence",
        # note that these slot names are unchanged
        "SOURCE": "SOURCE",
        "processingMethod": "processingMethod",
    }

    assert set(view.all_slots()) == set(slot_names)
    assert set(view.slot_name_mappings()) == set(slot_names.values())
    assert {snm_def.name: snm for snm, snm_def in view.slot_name_mappings().items()} == slot_names
