# Quick Install Guide

There are multiple ways to installing LinkML.

## Local installation: Use the Python package

If you are developing locally you can install LinkML as a python package in your local environment.

### Install Python

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

You can verify that Python is installed by typing `python` from your shell; you should see something like:

```bash
Python 3.13.11 (tags/v3.13.11:6278944, Dec  5 2025, 16:26:58) [MSC v.1944 64 bit (AMD64)] on win32
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

*note for core developers and contributors*: consult the [maintainers guide](../maintainers/contributing) for using this codebase from GitHub
