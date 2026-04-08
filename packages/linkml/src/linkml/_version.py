try:
    from importlib import metadata
except ImportError:
    # Python < 3.8
    import importlib_metadata as metadata  # pragma: no cover

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # package is not installed
    __version__ = "0.0.0"  # pragma: no cover
