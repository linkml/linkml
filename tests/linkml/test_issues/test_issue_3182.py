"""Regression tests for issue #3182: unhashable type 'list' in yamlutils.order_up.

When a class has no explicit key/identifier, pythongen falls back to using the
first required non-class-ranged slot as the key_name for _normalize_inlined_as_list.
If that slot is multivalued (e.g. applied_roles: range CreditEnum, multivalued: true),
its value is a list, which is unhashable.

This was exposed by #3165 which extended the fallback logic to inlined_as_list slots
(previously only inlined_as_dict used it). The yamlutils fix in the same commit
moved cooked_keys.add(key) inside the ``if keyed:`` block, preventing the crash
when keyed=False.

Schema and data patterns are derived from nmdc-schema's CreditAssociation class:
https://github.com/microbiomedata/nmdc-schema

See: https://github.com/linkml/linkml/issues/3182
"""

import pytest
import yaml

from linkml.generators.pythongen import PythonGenerator
from linkml.validator import _get_default_validator
from linkml.workspaces.example_runner import ExampleRunner
from linkml_runtime import SchemaView
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.utils.compile_python import compile_python

# -- Inline data matching the nmdc-schema CreditAssociation pattern --

STUDY_SINGLE_ROLE = """\
id: ex:study-1
has_credit_associations:
  - applied_roles:
      - Data curation
    applies_to_person:
      orcid: 'orcid:0000-0002-1825-00'
    type: prov:Association
  - applied_roles:
      - Software
    applies_to_person:
      orcid: 'orcid:0000-0001-9076-6066'
    type: prov:Association
"""

STUDY_MULTIPLE_ROLES = """\
id: ex:study-2
has_credit_associations:
  - applied_roles:
      - Supervision
      - Conceptualization
      - Funding acquisition
    applies_to_person:
      orcid: 'orcid:0000-0002-7086-765X'
      name: J. Craig Venter
    type: prov:Association
  - applied_roles:
      - Data curation
      - Software
    applies_to_person:
      orcid: 'orcid:0000-0001-9999-0000'
      name: Jane Doe
    type: prov:Association
"""

STUDY_DUPLICATE_ROLES = """\
id: ex:study-3
has_credit_associations:
  - applied_roles:
      - Data curation
    applies_to_person:
      orcid: 'orcid:0000-0000-0000-0001'
    type: prov:Association
  - applied_roles:
      - Data curation
    applies_to_person:
      orcid: 'orcid:0000-0000-0000-0002'
    type: prov:Association
"""


def _compile(schema_source):
    """Compile a schema (file path or string) to a Python module."""
    gen = PythonGenerator(schema_source)
    return compile_python(gen.serialize())


# ---- pythongen: verify generated __post_init__ ----


def test_normalize_inlined_as_list_emitted_for_multivalued_key(input_path):
    """The generated code should call _normalize_inlined_as_list with applied_roles as key.

    This is the change from #3165 that extended normalization to inlined_as_list slots.
    """
    gen = PythonGenerator(input_path("issue_3182.yaml"))
    pystr = gen.serialize()
    assert '_normalize_inlined_as_list(slot_name="has_credit_associations"' in pystr
    assert 'key_name="applied_roles"' in pystr
    assert "keyed=False" in pystr


def test_fallback_key_is_not_class_ranged(input_path):
    """The fallback should skip applies_to_person (class range) and pick applied_roles."""
    gen = PythonGenerator(input_path("issue_3182.yaml"))
    pystr = gen.serialize()
    assert 'key_name="applies_to_person"' not in pystr


# ---- yaml_loader: direct object construction ----


@pytest.mark.parametrize(
    "data_str,expected_count",
    [
        (STUDY_SINGLE_ROLE, 2),
        (STUDY_MULTIPLE_ROLES, 2),
        (STUDY_DUPLICATE_ROLES, 2),
    ],
    ids=["single-role", "multiple-roles", "duplicate-roles"],
)
def test_yaml_loader_with_multivalued_key(input_path, data_str, expected_count):
    """yaml_loader.loads should handle multivalued fallback keys without TypeError."""
    module = _compile(input_path("issue_3182.yaml"))
    obj = yaml_loader.loads(data_str, target_class=module.Study)
    assert len(obj.has_credit_associations) == expected_count


def test_yaml_loader_preserves_roles(input_path):
    """Verify that multivalued role values are preserved after normalization."""
    module = _compile(input_path("issue_3182.yaml"))
    obj = yaml_loader.loads(STUDY_MULTIPLE_ROLES, target_class=module.Study)
    roles_0 = [str(r) for r in obj.has_credit_associations[0].applied_roles]
    assert set(roles_0) == {"Supervision", "Conceptualization", "Funding acquisition"}
    roles_1 = [str(r) for r in obj.has_credit_associations[1].applied_roles]
    assert set(roles_1) == {"Data curation", "Software"}


def test_yaml_loader_duplicate_roles_allowed(input_path):
    """With keyed=False, duplicate key values across entries are allowed."""
    module = _compile(input_path("issue_3182.yaml"))
    obj = yaml_loader.loads(STUDY_DUPLICATE_ROLES, target_class=module.Study)
    assert len(obj.has_credit_associations) == 2
    for ca in obj.has_credit_associations:
        assert str(ca.applied_roles[0]) == "Data curation"


# ---- linkml-validate: JSON Schema validation ----


@pytest.mark.parametrize(
    "data_str",
    [STUDY_SINGLE_ROLE, STUDY_MULTIPLE_ROLES, STUDY_DUPLICATE_ROLES],
    ids=["single-role", "multiple-roles", "duplicate-roles"],
)
def test_validator_accepts_valid_data(input_path, data_str):
    """linkml-validate should accept data with multivalued slots in inlined_as_list classes."""
    validator = _get_default_validator(input_path("issue_3182.yaml"))
    input_dict = yaml.safe_load(data_str)
    report = validator.validate(input_dict, "Study")
    assert not report.results, f"Validation errors: {[r.message for r in report.results]}"


def test_validator_rejects_missing_required_roles(input_path):
    """Counter-example: applied_roles is required and must not be omitted."""
    bad_data = yaml.safe_load("""\
id: ex:study-bad
has_credit_associations:
  - applies_to_person:
      orcid: 'orcid:0000-0000-0000-0000'
    type: prov:Association
""")
    validator = _get_default_validator(input_path("issue_3182.yaml"))
    report = validator.validate(bad_data, "Study")
    assert report.results, "Expected validation failure for missing applied_roles"


# ---- ExampleRunner._load_from_dict: the path that triggered #3182 ----


@pytest.mark.parametrize(
    "data_str,expected_count",
    [
        (STUDY_SINGLE_ROLE, 2),
        (STUDY_MULTIPLE_ROLES, 2),
        (STUDY_DUPLICATE_ROLES, 2),
    ],
    ids=["single-role", "multiple-roles", "duplicate-roles"],
)
def test_load_from_dict_with_multivalued_key(input_path, data_str, expected_count):
    """ExampleRunner._load_from_dict should handle multivalued fallback keys.

    This is the code path that crashed with TypeError: unhashable type 'list'
    before the yamlutils fix in commit 4586572f5.
    """
    runner = ExampleRunner(schemaview=SchemaView(input_path("issue_3182.yaml")))
    input_dict = yaml.safe_load(data_str)
    obj = runner._load_from_dict(input_dict)
    assert len(obj.has_credit_associations) == expected_count


def test_load_from_dict_preserves_structure(input_path):
    """Verify full object structure through the ExampleRunner path."""
    runner = ExampleRunner(schemaview=SchemaView(input_path("issue_3182.yaml")))
    input_dict = yaml.safe_load(STUDY_MULTIPLE_ROLES)
    obj = runner._load_from_dict(input_dict)
    ca0 = obj.has_credit_associations[0]
    assert ca0.applies_to_person is not None
    assert ca0.applies_to_person.orcid == "orcid:0000-0002-7086-765X"
    roles = [str(r) for r in ca0.applied_roles]
    assert "Supervision" in roles
    assert "Conceptualization" in roles
    assert "Funding acquisition" in roles


# ---- ExampleRunner.process_examples: full end-to-end ----


def test_example_runner_process_examples(input_path, tmp_path):
    """Full ExampleRunner pipeline with multivalued inlined_as_list slots.

    This exercises the same code path as ``linkml-run-examples`` CLI.
    Writes example files to tmp_path to avoid checked-in data directories.
    """
    examples_dir = tmp_path / "examples"
    counter_examples_dir = tmp_path / "counter_examples"
    examples_dir.mkdir()
    counter_examples_dir.mkdir()

    (examples_dir / "Study-credit-1.yaml").write_text(STUDY_SINGLE_ROLE)
    (examples_dir / "Study-credit-2.yaml").write_text(STUDY_MULTIPLE_ROLES)
    (counter_examples_dir / "Study-missing-roles.yaml").write_text("""\
id: ex:study-bad
has_credit_associations:
  - applies_to_person:
      orcid: 'orcid:0000-0000-0000-0000'
    type: prov:Association
""")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    runner = ExampleRunner(
        schemaview=SchemaView(input_path("issue_3182.yaml")),
        input_directory=examples_dir,
        counter_example_input_directory=counter_examples_dir,
        output_directory=output_dir,
        output_formats=["yaml", "json"],
    )
    runner.process_examples()
    assert "Study-credit-1" in runner.summary.inputs
    assert "Study-credit-2" in runner.summary.inputs
    assert "Study-credit-1.yaml" in runner.summary.outputs
    assert "Study-credit-1.json" in runner.summary.outputs
    assert "Study-credit-2.yaml" in runner.summary.outputs
    assert "Study-credit-2.json" in runner.summary.outputs


# ---- Mechanism test: direct constructor exercises _normalize_inlined_as_list ----


def test_direct_constructor_with_list_valued_key(input_path):
    """Verify that _normalize_inlined handles list-valued keys when keyed=False.

    Before commit 4586572f5, cooked_keys.add(key) ran unconditionally, which
    crashed with TypeError for list-valued keys. The fix moved it inside
    ``if keyed:``, so with keyed=False (the fallback for classes without
    an explicit identifier), the set add is skipped entirely.

    This test constructs a Study directly to exercise _normalize_inlined_as_list
    with list-valued applied_roles as the key_name.
    """
    module = _compile(input_path("issue_3182.yaml"))
    study = module.Study(
        id="ex:study-direct",
        has_credit_associations=[
            {
                "applied_roles": ["Data curation", "Software"],
                "applies_to_person": {"orcid": "orcid:0000-0000-0000-0001"},
                "type": "prov:Association",
            },
            {
                "applied_roles": ["Supervision"],
                "applies_to_person": {"orcid": "orcid:0000-0000-0000-0002"},
                "type": "prov:Association",
            },
        ],
    )
    assert len(study.has_credit_associations) == 2
    roles_0 = [str(r) for r in study.has_credit_associations[0].applied_roles]
    assert "Data curation" in roles_0
    assert "Software" in roles_0
