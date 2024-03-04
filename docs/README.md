# Instructions for building LinkML documentation

These instructions are for the core developers of the LinkML framework.

Documentation source:

* [docs/ folder](https://github.com/linkml/linkml/tree/main/docs)
* deployed to: [https://linkml.io/linkml/](https://linkml.io/linkml/)

We use the sphinx framework.

## Instructions

To build the docs locally, first make sure you have the development dependencies installed which may not be the case if you pip-installed linkML. In the root folder of the linkML code, run

```bash
poetry install
```

Then use the make to build the documentation:

```bash
make docs
```

This will build docs in `_build/html/`. You can check these with your browser.

If you don't have make (on Windows) you can build the docs by:

```bash
cd docs
poetry run make html
```

New versions of the documentation are published to GitHub pages by a workflow job for every merge to main.

## IMPORTANT

**never** run `make html` directly

If you do this then docstrings from linkml will not be included.
Always check the generator docs to ensure command line options are present.
