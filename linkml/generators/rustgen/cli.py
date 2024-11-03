from pathlib import Path
from typing import Optional, get_args

import click

from linkml._version import __version__
from linkml.generators.rustgen import RUST_MODES, RustGenerator
from linkml.utils.generator import shared_arguments


@shared_arguments(RustGenerator)
@click.option("-m", "--mode", type=click.Choice([a for a in get_args(RUST_MODES)]), default="crate")
@click.option("-f", "--force", type=bool, default=False)
@click.option("-p", "--pyo3", type=bool, default=False)
@click.option("-s", "--serde", type=bool, default=False)
@click.option("-o", "--output", type=click.Path(dir_okay=True))
@click.version_option(__version__, "-V", "--version")
@click.command(name="pydantic")
def cli(
    yamlfile: Path,
    mode: RUST_MODES = "crate",
    force: bool = False,
    pyo3: bool = False,
    serde: bool = False,
    output: Optional[Path] = None,
    **kwargs,
):

    gen = RustGenerator(yamlfile, mode=mode, pyo3=pyo3, serde=serde, output=output, **kwargs)
    serialized = gen.serialize(force=force)
    if output is None:
        print(serialized)
