import pytest
from linkml_runtime import SchemaView

minimal_household_schema = """
name: minimal_household_schema
id: http://example.com/minimal_household_schema

classes:
    NamedThing:
        slots:
            - id
  
slots:
    id:
        identifier: true
"""

minimal_household_data = """
id: xxx
"""

minimal_view = SchemaView(minimal_household_schema)


def test_true_is_true():
    assert minimal_view is not None
