#!/usr/bin/env python
import sys
from setuptools import setup, find_packages
from warnings import warn

if sys.version_info < (3, 7, 6):
    warn(f"Some URL processing will fail with python 3.7.5 or earlier.  Current version: {sys.version_info}")

with open("requirements.txt", "r") as FH:
    REQUIREMENTS = FH.readlines()

NAME = 'linkml'
DESCRIPTION = 'Linked Open Data Modeling Language'
URL = 'http://linkml.github.io/linkml'
AUTHOR = 'Harold Solbrig'
EMAIL = 'solbrig@jhu.edu'
REQUIRES_PYTHON = '>=3.7'
LICENSE = 'CC0 1.0 Universal'
VERSION = '1.1.1'

setup(
    name=NAME,
    author=AUTHOR,
    version=VERSION,
    license=LICENSE,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=[r for r in REQUIREMENTS if not r.startswith("#")],
    keywords='linkml biolink metamodel',
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Console',
                 'Intended Audience :: Developers',
                 'Intended Audience :: Science/Research',
                 'Intended Audience :: Healthcare Industry',
                 'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
                 'Programming Language :: Python :: 3 :: Only',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9'
                 ],
)