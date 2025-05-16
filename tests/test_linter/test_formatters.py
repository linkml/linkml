import io

from linkml.linter.config.datamodel.config import RuleLevel
from linkml.linter.formatters import (
    JsonFormatter,
    MarkdownFormatter,
    TerminalFormatter,
    TsvFormatter,
)
from linkml.linter.linter import LinterProblem


def populate_report(formatter):
    formatter.start_report()

    formatter.start_schema("a.yaml")
    formatter.handle_problem(
        LinterProblem(
            message="this is an error",
            level=RuleLevel(RuleLevel.error),
            schema_name="a name",
            schema_source="a.yaml",
            rule_name="rule_1",
        )
    )
    formatter.handle_problem(
        LinterProblem(
            message="this is a warning",
            level=RuleLevel(RuleLevel.warning),
            schema_name="a name",
            schema_source="a.yaml",
            rule_name="rule_2",
        )
    )
    formatter.end_schema()

    formatter.start_schema("no_problems.yaml")
    formatter.end_schema()

    formatter.start_schema("b.yaml")
    formatter.handle_problem(
        LinterProblem(
            message="this is another error",
            level=RuleLevel(RuleLevel.error),
            schema_name="b name",
            schema_source="b.yaml",
            rule_name="rule_3",
        )
    )
    formatter.end_schema()

    formatter.end_report()


def test_terminal_formatter():
    output = io.StringIO()
    formatter = TerminalFormatter(file=output)
    populate_report(formatter)

    expected = """
a.yaml
  error    this is an error  (rule_1)
  warning  this is a warning  (rule_2)

b.yaml
  error    this is another error  (rule_3)

✖ Found 3 problems in 2 schemas
"""
    assert output.getvalue().strip() == expected.strip()


def test_terminal_formatter_verbose():
    output = io.StringIO()
    formatter = TerminalFormatter(file=output, verbose=True)
    populate_report(formatter)

    expected = """
a.yaml
  error    this is an error  (rule_1)
  warning  this is a warning  (rule_2)

no_problems.yaml

b.yaml
  error    this is another error  (rule_3)

✖ Found 3 problems in 2 schemas
"""
    assert output.getvalue().strip() == expected.strip()


def test_markdown_formatter():
    output = io.StringIO()
    formatter = MarkdownFormatter(file=output)
    populate_report(formatter)

    expected = """
## Summary

|                      | Count |
|----------------------|-------|
| Schemas Checked      | 3 |
| Schemas with Error   | 2 |
| Schemas with Warning | 1 |
| Total Errors         | 2 |
| Total Warnings       | 1 |


## Problems per Schema

### a.yaml
#### Errors
* rule_1: this is an error
#### Warnings
* rule_2: this is a warning

### b.yaml
#### Errors
* rule_3: this is another error
"""
    assert output.getvalue().strip() == expected.strip()


def test_json_formatter():
    output = io.StringIO()
    formatter = JsonFormatter(file=output)
    populate_report(formatter)

    expected = """
[
  {
    "message": "this is an error",
    "level": "error",
    "schema_name": "a name",
    "schema_source": "a.yaml",
    "rule_name": "rule_1"
  },
  {
    "message": "this is a warning",
    "level": "warning",
    "schema_name": "a name",
    "schema_source": "a.yaml",
    "rule_name": "rule_2"
  },
  {
    "message": "this is another error",
    "level": "error",
    "schema_name": "b name",
    "schema_source": "b.yaml",
    "rule_name": "rule_3"
  }
]
"""
    assert output.getvalue().strip() == expected.strip()


def test_tsv_formatter():
    output = io.StringIO()
    formatter = TsvFormatter(file=output)
    populate_report(formatter)

    expected = """
source	schema name	rule name	level	message
a.yaml	a name	rule_1	error	this is an error
a.yaml	a name	rule_2	warning	this is a warning
b.yaml	b name	rule_3	error	this is another error
"""
    actual = output.getvalue()
    actual_normalized = actual.strip().replace("\r\n", "\n").replace("\r", "\n")
    assert actual_normalized == expected.strip()
