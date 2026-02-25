"""
Backward compatibility module for golanggen.

This module provides backward compatibility by re-exporting the new
golanggen package implementation.
"""

from linkml.generators.golanggen.golanggen import GolangGenerator, cli

__all__ = ["GolangGenerator", "cli"]

if __name__ == "__main__":
    cli()
