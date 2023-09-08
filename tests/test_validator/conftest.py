import pytest


@pytest.fixture
def tmp_file_factory(tmp_path):
    def factory(filename, contents):
        file_path = tmp_path / filename
        with open(file_path, "w") as file:
            file.write(contents)
        return str(file_path)

    return factory
