from pathlib import Path
from typing import get_args

import click

from linkml._version import __version__
from linkml.generators.rustgen import RUST_MODES, RustGenerator
from linkml.utils.generator import apply_config_defaults, read_generator_config, shared_arguments


@shared_arguments(RustGenerator)
@click.option(
    "-m",
    "--mode",
    type=click.Choice([a for a in get_args(RUST_MODES)]),
    default="crate",
    help="Generation mode: 'crate' (Cargo package) or 'file' (single .rs)",
)
@click.option(
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
    "--config-file",
    "-C",
    type=click.File("rb"),
    help="Path to a YAML config file supplying defaults under "
    "'generator_args: {rust: {crate_name: ...}}'. Keys are this command's own option "
    "names with dashes as underscores; explicit command-line options always take "
    "precedence over the config file.",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=True),
    help="Output directory (crate mode) or .rs file (file mode)",
)
@click.version_option(__version__, "-V", "--version")
@click.command(name="rust")
@click.pass_context
def cli(ctx: click.Context, yamlfile: Path, config_file=None, **kwargs):
    """Generate Rust types from a LinkML model"""
    config = read_generator_config(config_file, RustGenerator.config_section_name)
    apply_config_defaults(ctx, config, kwargs)
    RustGenerator.validate_generator_args(kwargs)
    # every option but --force is a constructor argument; --force is a serialize() one
    force = kwargs.pop("force")
    gen = RustGenerator(yamlfile, **kwargs)
    serialized = gen.serialize(force=force)
    if gen.output is None:
        print(serialized)
