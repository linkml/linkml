# Instructions for building LinkML documentation

These instructions are for the core developers of the LinkML framework.

Documentation source:

 * [sphinx/ folder](https://github.com/linkml/linkml/tree/main/sphinx)
 * deployed to: [https://linkml.io/linkml/](https://linkml.io/linkml/)

We use the sphinx framework.

## Instructions

To build the doc locally:

```bash
pipenv run make html
```

This will build docs in `_build/html/`. You can check these with your browser.

After you are satisfied they look good run:

```bash
make deploy
```

(this is a simple copy and doesn't need to be done in pipenv)

This will copy to [docs/](https://github.com/linkml/linkml/tree/main/docs) where they can be committed

**NOTE**: remember to `git add` any new HTML files or assets

Currently we do not do these steps by github actions. It is recommended you commit changes to docs in a separate PR. The PRs can be more easily evaluated if they are only the source change, and conflicts are easier to resolve.

## IMPORTANT

**never** run `make html` directly

**always** run this from inside the pipenv shell or via:

```bash
pipenv run make html
```

If you don't do this then docstrings from linkml will not be included. Always check the generator docs to ensure command line options are present.

