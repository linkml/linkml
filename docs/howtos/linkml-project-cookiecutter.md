# LinkML Project Cookiecutter

To start a new LinkML project, please use the [LinkML Project Cookiecutter](https://github.com/linkml/linkml-project-cookiecutter)
command line tool.  This tool will generate a LinkML project directory for you, including the directory structure 
and commands necessary to build and test your project.  For  step-by-step instructions on using the linkml-project-cookiecutter, please
[consult the documentation here](https://github.com/linkml/linkml-project-cookiecutter/blob/main/README.md).

## LinkML Project Cookiecutter Quickstart
In your poetry virtual environment:

```bash
poetry add cruft
```

## Use cruft to create your brand new LinkML project:

In your poetry virtual environment:

```bash
poetry shell
cruft create https://github.com/linkml/linkml-project-cookiecutter
```

Answer the prompted questions to customize your project.  More details on the prompts and how to answer 
them can be found [here](https://github.com/linkml/linkml-project-cookiecutter/blob/main/README.md).

## Build your LinkML project

```bash
cd linkml-projects/my-awesome-schema  # using the folder example above
make setup
```
