import pytest

from linkml.validator.plugins.pydantic_validation_plugin import PydanticValidationPlugin


@pytest.mark.parametrize(
    "instance,valid,skip",
    [
        ({"id": "1", "name": "Person One"}, True, False),
        ({"id": "1", "name": "Person One", "telephone": "1-555-555-5555"}, True, False),
        ({"id": "1", "name": "Person One", "not_a_field": "blah"}, True, False),
        ({}, False, False),
        ({"id": "1"}, False, False),
        ({"id": "1", "name": "Person One", "aliases": []}, True, False),
        ({"id": "1", "name": "Person One", "aliases": ["Person 1"]}, True, False),
        ({"id": "1", "name": "Person One", "aliases": "Person 1"}, False, False),
        ({"id": "1", "name": ["Person One"]}, False, False),
        ({"id": ["1"], "name": "Person One"}, False, False),
        ({"id": "1", "name": 1, "age": 100}, False, False),
        ({"id": "1", "name": 1, "age": "one hundred"}, False, False),
        ({"name": "Person One"}, False, False),
        # TODO
        ({"id": "1", "name": "Person One", "telephone": "not a number"}, False, True),
        ({"id": "1", "name": 1}, False, True),
        ({"id": "1", "name": 1, "age": "100"}, False, True),
    ],
)
def test_instance(validation_context, instance, valid, skip):
    if skip:
        pytest.skip()
    plugin = PydanticValidationPlugin()
    results = list(plugin.process(instance, validation_context))
    if valid:
        assert not results
    else:
        assert len(results) == 1


@pytest.mark.parametrize(
    "instance,closed,valid",
    [
        ({"id": "1", "name": "Person One", "not_a_field": "blah"}, False, True),
        ({"id": "1", "name": "Person One", "not_a_field": "blah"}, True, False),
    ],
)
def test_instance_closed(validation_context, instance, closed, valid):
    plugin = PydanticValidationPlugin(closed=closed)
    results = list(plugin.process(instance, validation_context))
    if valid:
        assert not results
    else:
        assert len(results) == 1
