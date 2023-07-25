import pytest

# https://stackoverflow.com/questions/41522767/pytest-assert-introspection-in-helper-function
# we want to have pytest assert introspection in the helpers
pytest.register_assert_rewrite("tests.test_compliance.helper")
