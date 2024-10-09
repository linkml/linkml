import pytest

from linkml.generators.rustgen import RustGenerator


@pytest.mark.rustgen
def test_generate_crate(kitchen_sink_path, temp_dir):
    gen = RustGenerator(kitchen_sink_path, mode="crate", output=temp_dir)
    _ = gen.serialize(force=True)
