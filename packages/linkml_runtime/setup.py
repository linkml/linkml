#!/usr/bin/env python
import sys
from setuptools import setup
from warnings import warn

if sys.version_info < (3, 7, 0):
    warn(f"Some URL processing will fail with python 3.7.5 or earlier.  Current version: {sys.version_info}")

setup(
    setup_requires=['pbr'],
    pbr=True,
)
