"""Tests for various parts of the schema synopsis file"""

from pathlib import Path
from typing import Union

from linkml import LOCAL_METAMODEL_YAML_FILE
from linkml.utils.schemaloader import SchemaLoader


def eval_synopsis(source: Union[str, Path], errs_snapshot, synopsis_snapshot) -> str:
    schema = SchemaLoader(source)
    schema.resolve()

    errs = "\n".join(schema.synopsis.errors())
    assert errs == errs_snapshot

    assert schema.synopsis.summary() == synopsis_snapshot

    return schema.synopsis.summary()


def test_meta_synopsis(input_path, snapshot):
    """Raise a flag if the number of classes, slots, types or other elements change in the model"""
    eval_synopsis(
        source=LOCAL_METAMODEL_YAML_FILE,
        errs_snapshot=snapshot("meta.errs"),
        synopsis_snapshot=snapshot("meta.synopsis"),
    )


def test_unitialized_domain(input_path, snapshot):
    summary = eval_synopsis(
        source=input_path("synopsis1.yaml"),
        errs_snapshot=snapshot("synopsis1.errs"),
        synopsis_snapshot=snapshot("synopsis1.synopsis"),
    )
    # Double check because it is easy to lose the target in the file updates
    assert "Domain unspecified: 1" in summary


def test_applyto(input_path, snapshot):
    summary = eval_synopsis(
        source=input_path("synopsis2.yaml"),
        errs_snapshot=snapshot("synopsis2.errs"),
        synopsis_snapshot=snapshot("synopsis2.synopsis"),
    )
    assert "* Unowned slots: s1, s2" in summary
