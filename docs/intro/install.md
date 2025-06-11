# Quick Install Guide

There are multiple ways to installing LinkML.

## Local installation: Use the Python package

If you are developing locally you can install LinkML as a python package in your local environment.

### Install Python

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

You can verify that Python is installed by typing `python` from your shell; you should see something like:

```bash
Python 3.9.5 (v3.9.5:0a7dcbdb13, May  3 2021, 13:17:02)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### Install LinkML

The latest version can always be installed with:

```bash
pip install linkml
```

## Alternative: Use the official Docker/OCI image

You can also use the [official Docker/OCI image for LinkML](https://hub.docker.com/r/linkml/linkml):

To start a shell from the image:
```bash
docker run -v ./:/work -w /work/ --rm -ti docker.io/linkml/linkml
```

Then try some commands:

```{command-output} gen-project --help
---
ellipsis: 5
---
```

See the [generators](../generators/index.rst) section for more cli entrypoints, or
[continue to the tutorial](./tutorial.rst)

## Installation for contributors

*note for core developers and contributors*: consult the [developers guide](../developers/contributing-code) for using this codebase from GitHub
