# Quick Install Guide

## Install Python

Get the latest version of Python at https://www.python.org/downloads/ or with your operating system’s package manager.

You can verify that Python is installed by typing `python` from your shell; you should see something like:

```bash
Python 3.9.5 (v3.9.5:0a7dcbdb13, May  3 2021, 13:17:02) 
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>>
```


## Install LinkML

The latest version can always be installed with:

```bash
python -m pip install linkml
```

## Install with Pipenv

We can use [pipenv](https://pipenv-fork.readthedocs.io/en/latest/) to install the package for local testing as shown in the following code block. Some IDE's like PyCharm also have direct [support](https://www.jetbrains.com/help/pycharm/pipenv.html) for pipenv.

```bash
pipenv install --dev -e .
```


## Alternative protocol: Use Docker

You can also use the Docker image, courtesy of the Monarch Initiative:

```bash
docker run -v $(PWD):/work -w /work/ --rm -ti monarchinitiative/linkml
```

This comes with LinkML already installed

## Installation for contributors

*note for core developers and contributors*: consult the [developers guide](../developers/contributing-code) for using this codebase from GitHub
