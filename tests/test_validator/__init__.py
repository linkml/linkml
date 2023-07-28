import os
import tempfile
from contextlib import contextmanager


@contextmanager
def data_file(test_data: str, *args, **kwargs):
    file = tempfile.NamedTemporaryFile(mode="w+", delete=False, *args, **kwargs)
    file.write(test_data)
    file.close()

    yield file.name

    os.unlink(file.name)
