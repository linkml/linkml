import pytest


@pytest.fixture
def kitchen_sink_path(input_path):
    return str(input_path("kitchen_sink.yaml"))


class MyInjectedClass:
    classattr: str = "hey"

    def __init__(self, up: str = "doc"):
        self.what = up
