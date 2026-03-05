# LinkML Project Copier Template

```{tip}
If you have an existing project based on the old cookiecutter template, see the
[migration guide](https://github.com/linkml/linkml-project-copier#migrating-an-existing-project-to-use-this-template).
```

To start a new LinkML project, use the [LinkML Project Copier](https://github.com/linkml/linkml-project-copier)
template. This template generates a LinkML project directory for you, including the directory structure
and commands necessary to build and test your project. For step-by-step instructions, please
[consult the documentation here](https://github.com/linkml/linkml-project-copier/blob/main/README.md).

## Prerequisites

You need the following tools installed:

- [copier](https://copier.readthedocs.io/) (version 9.4.0 or later)
- [uv](https://docs.astral.sh/uv/) (for Python package management)
- [just](https://just.systems/) (command runner)

## Quickstart

### Create your new LinkML project

```bash
mkdir my-awesome-schema
cd my-awesome-schema
copier copy --trust https://github.com/linkml/linkml-project-copier .
```

Answer the prompted questions to customize your project. More details on the prompts and how to answer
them can be found [here](https://github.com/linkml/linkml-project-copier/blob/main/README.md).

The `--trust` flag is required because the template uses Jinja2 extensions.

### Set up your project

```bash
just setup
```

### Build and test your project

```bash
just test
```

## Updating your project from the template

One key advantage of Copier over the previous Cookiecutter-based template is lifecycle management.
When the template is updated, you can pull in those changes:

```bash
copier update --trust
```

This will re-apply the template with your existing answers, using git-style conflict markers
where your local changes conflict with template updates.
