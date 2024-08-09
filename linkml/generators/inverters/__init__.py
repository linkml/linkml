"""
Tools for inverting generated models back to linkml schemas, or deriving linkml schemas
from other formats
"""

from linkml.generators.inverters.dataclasses import DataclassInverter

__all__ = ["DataclassInverter"]
