"""Root conftest to register pytest options for monorepo workspace."""


def pytest_addoption(parser):
    """Register CLI options that are used by package-level tests."""
    parser.addoption(
        "--generate-snapshots",
        action="store_true",
        dest="generate_snapshots",
        default=False,
        help="Generate new files into __snapshot__ directories instead of checking against existing files",
    )
    parser.addoption(
        "--with-slow",
        action="store_true",
        dest="with_slow",
        default=False,
        help="include tests marked slow",
    )
    parser.addoption(
        "--with-network",
        action="store_true",
        dest="with_network",
        default=False,
        help="include tests marked network",
    )
    parser.addoption(
        "--with-output",
        action="store_true",
        dest="with_output",
        default=False,
        help="dump output in compliance test for richer debugging information",
    )
    parser.addoption(
        "--without-cache",
        action="store_true",
        dest="without_cache",
        default=False,
        help="Don't use a sqlite cache for network requests",
    )
    parser.addoption(
        "--with-biolink",
        action="store_true",
        dest="with_biolink",
        default=False,
        help="Include tests marked as for the biolink model",
    )
    parser.addoption(
        "--with-rustgen",
        action="store_true",
        dest="with_rustgen",
        default=False,
        help="Include tests marked as rustgen (Rust codegen/maturin)",
    )
