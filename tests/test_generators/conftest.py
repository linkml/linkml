import pytest


@pytest.fixture
def kitchen_sink_path(input_path):
    return str(input_path("kitchen_sink.yaml"))
