#!/usr/bin/env python
import sys
from setuptools import setup
from warnings import warn

if sys.version_info < (3, 7, 6):
    warn(f"Some URL processing will fail with python 3.7.5 or earlier.  Current version: {sys.version_info}")

setup(
    name='linkml',
    setup_requires=['pbr'],
    pbr=True,
)