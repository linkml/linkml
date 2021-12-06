# Contribution Guidelines

When contributing to this repository, please first discuss the change you wish to make via an issue, email, or any other method, with the owners of this repository before issuing a pull request.

## How to contribute

### Reporting bugs or making feature requests

You can use the [Issues](https://github.com/linkml/linkml-runtime/issues) tab to create bug and feature requests. Providing enough details to the developers to verify and troubleshoot your issue is paramount:

* Provide a clear and descriptive title as well as a concise summary of the issue to identify the problem.
* Describe the exact steps which reproduce the problem in as many details as possible.
* Describe the behavior you observed after following the steps and point out what exactly is the problem with that behavior.
* Explain which behavior you expected to see instead and why.
* Provide screenshots of the expected or actual behaviour where applicable.

## General contribution instructions

1. Follow the [Github docs](https://docs.github.com/en/get-started/quickstart/fork-a-repo) to make a copy (a fork) of the repository to your own Github account.
2. [Clone the forked repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) to your local machine so you can begin making changes.
3. Make sure this repository is set as the [upstream remote repository](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/configuring-a-remote-for-a-fork) so you are able to fetch the latest commits.
4. Push all your changes to a development branch, which is ideally a copy of the `main` branch of this repository.
5. Create pull requests from the development branch into the `main` branch when the code is ready to be merged into production.

### The development lifecycle

1. Create a bug fix or feature development branch, based off the `main` branch of the upstream repo, and not your fork. Name the branch appropriately, briefly summarizing the bug fix or feature request. If none come to mind, you can include the issue number in the branch name. Some examples of branch names are, `bugfix/breaking-pipfile-error` or `feature/add-click-cli-layer`, or `bugfix/issue-414`
2. Make sure your development branch has all the latest commits from the `main` branch.
3. After completing work and testing locally, push the code to the appropriate branch on your fork.
4. Create a pull request from the bug/feature branch of your fork to the `main` branch of the upstream repository.

Note: All the development must be done on a branch on your fork.

> An LBL engineer must review and accept your pull request. A code review (which happens with both the contributor and the reviewer present) is required for contributing.

## Development environment setup

1. Install [poetry](https://python-poetry.org/docs/#installation).
2. Clone the [linkml-runtime](https://github.com/linkml/linkml-runtime) repository.

```
git clone https://github.com/linkml/linkml-runtime.git
```

3. Change directory to the cloned `linkml-runtime` repo.

```
cd linkml-runtime
```

4. Install all the dependencies from your project, which are typically specified in a `poetry.lock` file.

```
poetry install
```

5. Run any python scripts or CLI commands by prefixing with `poetry run`.

```
poetry run python your_script.py
poetry run pytest
```

## Release process

Once the code has been merged into the `main` branch on this repo, there are two processes that need to be completed to ensure a release is complete.

* You should create a Github [tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging), with the appropriate version number. The version numbers follow the [guidelines](https://semver.org/) laid by the semantic versioning community.
* You should push the package to PyPI. Schematic is on PyPI as [linkml-runtime](https://pypi.org/project/linkml-runtime/). You can go through the following two sections for that.

### Optional release to test PyPI

The purpose of this section is to verify that the package looks and works as intended, by viewing it on [Test PyPI](https://test.pypi.org/) and installing the test version in a separate virtual environment.

```
poetry build   # build the package
poetry config repositories.testpypi https://test.pypi.org/legacy/   # add Test PyPI as an alternate package repository
poetry publish -r testpypi   # publish the package to Test PyPI
```

Installing:

```
pip install --index-url https://test.pypi.org/simple/
```

### Release to PyPI

If the package looks great on Test PyPI and works well, the next step is to publish the package to PyPI:

```
poetry build    # build the package
poetry publish  # publish the package to PyPI
```

> You'll need to [register](https://pypi.org/account/register/) for a PyPI account before uploading packages to the package index. Similarly for [Test PyPI](https://test.pypi.org/account/register/) as well.

## Testing

All code added to the linkml-runtime source must have tests. The repo uses pytest to run tests. The test code is located in the tests subdirectory.

You can run the test suite in the following way:


```
poetry run pytest -vs tests/
```

## Code style

- Please consult the [Google Python Styleguide](https://google.github.io/styleguide/pyguide.html) prior to contributing to this project.
- Be consistent and follow existing conventions and spirit.
