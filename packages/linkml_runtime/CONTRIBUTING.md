# Contribution Guidelines

When contributing to this repository, please first discuss the changes you wish to make via an issue, email, or any other method, with the owners of this repository before issuing a pull request.

## How to contribute

### Reporting bugs or making feature requests

To report a bug or suggest a new feature, please go to the [linkml/linkml issue tracker](https://github.com/linkml/linkml/issues), as we are
consolidating issues there.

Please supply enough details to the developers to enable them to verify and troubleshoot your issue:

* Provide a clear and descriptive title as well as a concise summary of the issue to identify the problem.
* Describe the exact steps which reproduce the problem in as many details as possible.
* Describe the behavior you observed after following the steps and point out what exactly is the problem with that behavior.
* Explain which behavior you expected to see instead and why.
* Provide screenshots of the expected or actual behaviour where applicable.
* Tag the issue with appropriate label names. For example, if your issue is about a bug that needs to be fixed in the repo, tag the issue with the `bug` label from the list of [labels](https://github.com/linkml/linkml-runtime/labels). If an appropriate label doesn't exist, create one, with a name that clearly encapsulates the topic of the issue.

### The development lifecycle

1. Create a bug fix or feature development branch, based off the `main` branch of the upstream repo, and not your fork. Name the branch appropriately, briefly summarizing the bug fix or feature request. If none come to mind, you can include the issue number in the branch name. Some examples of branch names are, `bugfix/breaking-pipfile-error` or `feature/add-click-cli-layer`, or `bugfix/issue-414`
2. Make sure your development branch has all the latest commits from the `main` branch.
3. After completing work and testing locally, push the code to the appropriate branch on your fork.
4. Create a pull request from the bug/feature branch of your fork to the `main` branch of the upstream repository.

Note: All the development must be done on a branch on your fork.

ALSO NOTE: github.com lets you create a pull request from the main branch, automating the steps above.

> A code review (which happens with both the contributor and the reviewer present) is required for contributing.

## Pull Requests

### Upstream Testing

`linkml-runtime` is tightly coupled to upstream `linkml`, 
so all pull requests have their changes tested by running the upstream tests
against the PR version of `linkml-runtime`.

In some circumstances, paired changes need to be made against *both*
`linkml` and `linkml-runtime`, where testing against the `main` branch
of `linkml` is insufficient. 

When opening a pull request, you can specify that your PR needs to be
tested against a specific upstream branch and repository by specifying it
in the first two lines of your pull request like this:

> upstream_repo: my-cool-username/linkml
> upstream_branch: some-complicated-feature
> 
> Hey everyone what up it's me your boy MC spongebob here with another banger
> ... (PR continues)

The order of the `upstream_repo` and `upstream_branch` tags doesn't matter,
but they must be on the first two lines of the pull request comment and separated with a colon.

Maintainers can also specify upstream branches to test against when 
dispatching the `test-upstream` workflow manually via the GUI prompt.

Testing against an unverified upstream branch is not necessarily dangerous,
since the [input is stored as a variable first and not executed as untrusted code](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions#using-an-intermediate-environment-variable),
but maintainers should take care to verify that the upstream branch and repo
are correct and expected given the context of the PR.

## Development environment setup

1. Install [poetry](https://python-poetry.org/docs/#installation).
2. Install all the dependencies from your project, which are typically specified in a `poetry.lock` file.

```
poetry install
```

3. Run any python scripts or CLI commands by prefixing with `poetry run`.

```
poetry run python your_script.py  # ex of how to run standalone python script
poetry run pytest # ex of how to invoke CLI tools
```

4. Refer to the poetry docs for details on how to use the [add](https://python-poetry.org/docs/cli/#add), [update](https://python-poetry.org/docs/cli/#update) and [remove](https://python-poetry.org/docs/cli/#remove) commands.

## Release process

Once the code has been merged into the `main` branch on this repo, there are a few steps that need to be completed to ensure a release is complete.

### Creating a release

* Use the [releases](https://github.com/linkml/linkml-runtime/releases) section of the Github interface to draft a new release.
* Conventionally tags are prefixed with `v` so choose an appropriately versioned tag number. Ex., `v1.1.9` and such.
* Leave the default `main` branch as the target. Use the same tag number for the release title as well. After that, use Github's autogenerated CHANGELOG button to generate release notes. If it's possible to simplify the notes and make it more succinct, you should. 
* Once a release is created, a [Github Action](.github/workflows/pypi-publish.yaml) will take care of publishing the package to PyPI for you.

* Navigate to the [Actions](https://github.com/linkml/linkml-runtime/actions) tab, and verify that there is a ✅ next to the release tag that was just created. For ex., [v1.1.15](https://github.com/linkml/linkml-runtime/actions/runs/1656285916).
* Finally, check the package page on [PyPI](https://pypi.org/project/linkml-runtime/) to make sure the latest release was published.

## Testing

All code added to the linkml-runtime source must have tests. The repo uses the native `unittest` module to run tests. The test code is located in the tests subdirectory.

You can run the test suite in the following way:

```
poetry run python -m pytest
```

### Upstream Testing

To run the upstream `linkml` tests against your branch,
install `linkml` locally with poetry, and then manually install your
local copy of `linkml-runtime`

```shell
git clone https://github.com/linkml/linkml
cd linkml
poetry install --all-extras --with tests
poetry run pip install -e ~/location/of/linkml-runtime
poetry run pytest
```

## Code style

- Please consult the [Google Python Styleguide](https://google.github.io/styleguide/pyguide.html) prior to contributing to this project.
- Be consistent and follow existing conventions and spirit.
