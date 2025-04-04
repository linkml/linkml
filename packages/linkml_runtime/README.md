# linkml-runtime
[![Pyversions](https://img.shields.io/pypi/pyversions/linkml-runtime.svg)](https://pypi.python.org/pypi/linkml-runtime)
![](https://github.com/linkml/linkml-runtime/workflows/Build/badge.svg)
[![badge](https://img.shields.io/badge/launch-binder-579ACA.svg)](https://mybinder.org/v2/gh/linkml/linkml-runtime/main?filepath=notebooks)
[![PyPi](https://img.shields.io/pypi/v/linkml-runtime.svg)](https://pypi.python.org/pypi/linkml)
[![PyPIDownloadsTotal](https://pepy.tech/badge/linkml-runtime)](https://pepy.tech/project/linkml-runtime)
[![PyPIDownloadsMonth](https://img.shields.io/pypi/dm/linkml-runtime?logo=PyPI&color=blue)](https://pypi.org/project/linkml-runtime)
[![codecov](https://codecov.io/gh/linkml/linkml-runtime/branch/main/graph/badge.svg?token=FOBHNSK5WG)](https://codecov.io/gh/linkml/linkml-runtime)

Runtime support for linkml generated data classes.

## About

This python library provides runtime support for [LinkML](https://linkml.io/linkml/) datamodels.

See the [LinkML repo](https://github.com/linkml/linkml) for the [Python Dataclass Generator](https://linkml.io/linkml/generators/python.html) which will convert a schema into a Python object model. That model will have dependencies on functionality in this library.

The library also provides

* loaders: for loading from external formats such as json, yaml, rdf, tsv into LinkML instances
* dumpers: the reverse operation

See [working with data](https://linkml.io/linkml/data/index.html) in the documentation for more details

This repository also contains the Python dataclass representation of the [LinkML metamodel](https://github.com/linkml/linkml-model), and various utility functions that are useful for working with LinkML data and schemas.

It also includes the [SchemaView](https://linkml.io/linkml/developers/manipulating-schemas.html) class for working with LinkML schemas

## Notebooks

See the [notebooks](https://github.com/linkml/linkml-runtime/tree/main/notebooks) folder for examples
