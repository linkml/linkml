# LinkML Workspace Generator

## Pre-modeling Setup

This generator helps you get setup with a pre-defined project structure, 
or, a workspace, for when you want to start modeling your own LinkML 
model. To take full advantage of the contents of this project template, 
we recommend familiarizing yourself with the various targets provided in 
the Makefile. You can do so by running:

```bash
make help
```

Note: The default package manager that the generator sets you up with is 
[poetry](https://python-poetry.org/).

## Introduction

If you are a data modeler, and want to start authoring LinkML data models 
to describe the strcuture of your datasets, then the first step to do after 
installing the linkml library itself, is to let linkml do the heavy lifting 
and use it to generate a well defined directory structure for your project.

The workspace generator creates a directory structure is that is based off of 
this Github template: [linkml-project-structure](https://github.com/linkml/linkml-project-template)

## General Tips

Some important points to keep in mind about this structure:

* To take advantage of the directory structure, familiarize yourself with 
all the commands that are available at your disposal as Makefile targets, by 
running:

```bash
make help
```

* Configure the name of your data model and the path to your data model in 
the `about.yaml` file, since the Makefile targets pick variable names 
from there.

* The core LinkML YAML data model can be found at: `src > linkml > my_data_model.yaml`.

* The generator super charges your project with automatic documentation generation 
capabilities using [Mkdocs](https://www.mkdocs.org/), and package management 
using [poetry](https://python-poetry.org/).

* To extend the Makefile and add your own custom make targets, that may or may not be 
dependent on the already defined targets and variables, you can specify them in the 
`project.Makefile` file.


## Command Reference

```
✗ poetry run linkml-ws new --help

Usage: linkml-ws new [OPTIONS] NAME

  Create a new project

  This will use: https://github.com/linkml/linkml-project-template

  Example:

      linkml-ws new my-awesome-project

Options:
  -T, --template-directory TEXT  Path to a template directory. If empty, then
                                 the default linkml-project-template will be
                                 used
  -d, --directory TEXT           Path to a target directory
  -U, --organization TEXT        Name of github organization  [default:
                                 my_org]
  -V, --template-version TEXT    Version of template.
  -D, --description TEXT         Description of project  [default: my awesome
                                 datamodel is for awesome things]
  --force / --no-force           overwrite project dir if exists already
                                 [default: no-force]
  --help                         Show this message and exit.
```