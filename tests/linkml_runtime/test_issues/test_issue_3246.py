from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.processing.referencevalidator import ReferenceValidator, Report
from tests.linkml_runtime.test_issues.environment import env

# https://github.com/linkml/linkml/issues/3246


def test_issue_3246() -> None:
    """Test that the normalizer correctly recognizes linkml:Any.

    A class that "takes the role of `linkml:Any`" is explicitly
    intended to hold arbitrary data. The normalizer should recognize
    that and not flag the presence of undeclared slots as an error.
    """

    sv = SchemaView(env.input_path("issue_3246.yaml"))
    normalizer = ReferenceValidator(sv)
    sample = {"name": "something", "extra": {"foo": "bar"}, "extras": [{"foo": "bar"}]}
    report = Report()
    normalizer.normalize(sample, report=report)
    assert not report.errors()
