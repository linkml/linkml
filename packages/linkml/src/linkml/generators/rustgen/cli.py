from pathlib import Path
from typing import Optional, get_args

import click

from linkml._version import __version__
from linkml.generators.rustgen import RUST_MODES, RustGenerator
from linkml.utils.generator import shared_arguments


@shared_arguments(RustGenerator)
@click.option(
    "-m",
    "--mode",
    type=click.Choice([a for a in get_args(RUST_MODES)]),
    default="crate",
    help="Generation mode: 'crate' (Cargo package) or 'file' (single .rs)",
)
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="Overwrite output if it already exists",
)
@click.option(
    "-p",
    "--pyo3",
    is_flag=True,
    help=(
        "Add 'pyo3' to Cargo.toml default features and emit Python module glue (cdylib + #[pymodule]). "
        'Source always includes #[cfg(feature="pyo3")] gates; this flag only enables the crate feature by default.'
    ),
)
@click.option(
    "-s",
    "--serde",
    is_flag=True,
    help=(
        "Add 'serde' to Cargo.toml default features. Source always includes #[cfg(feature=\"serde\")] derives/attrs; "
        "this flag only enables the crate feature by default."
    ),
)
@click.option(
    "--handwritten-lib/--no-handwritten-lib",
    default=False,
    help=(
        "When enabled, place generated sources under src/generated and create a shim lib.rs for handwritten code. "
        "The shim is only created on first run and left untouched on subsequent regenerations."
    ),
)
@click.option("-n", "--crate-name", type=str, default=None, help="Name of the generated crate/module")
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=True),
    help="Output directory (crate mode) or .rs file (file mode)",
)
@click.version_option(__version__, "-V", "--version")
@click.command(name="rust")
def cli(
    yamlfile: Path,
    mode: RUST_MODES = "crate",
    force: bool = False,
    pyo3: bool = False,
    serde: bool = False,
    crate_name: Optional[str] = None,
    handwritten_lib: bool = False,
    output: Optional[Path] = None,
    **kwargs,
):
    gen = RustGenerator(
        yamlfile,
        mode=mode,
        pyo3=pyo3,
        serde=serde,
        output=output,
        crate_name=crate_name,
        handwritten_lib=handwritten_lib,
        **kwargs,
    )
    serialized = gen.serialize(force=force)
    if output is None:
        print(serialized)
