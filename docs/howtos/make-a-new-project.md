# How to initialize a LinkML project

## Standard Protocol

### Step 1: Install cruft and poetry

1a: [install poetry](https://python-poetry.org/docs/):

`curl -sSL https://install.python-poetry.org | python3 -`

1b: [install cruft](https://cruft.github.io/cruft/):

`pip3 install cruft`

### Use cruft to generate a new project:

`cruft https://github.com/linkml/linkml-project-cookiecutter`

Then follow the instructions on the screen, answering questions as best you can.

General guidelines:

- projects should be in kebab-case, with no spaces

Note: if you don't intend to generate and release python classes, you can ignore
the question about PYPI.

If you intend to use schemasheets for your project, you will need the ID of your sheet,
plus the names of the tabs. We recommend using names with no spaces for the tabs.

If you are not using schemasheets, you can ignore this question.

See [linkml/linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter) for more docs.

### Setup the project

Change to the folder your generated project is in

type:

```bash
make setup
```

### Edit the schema

Edit the schema in the src folder

### Validate the schema

`make test`

### Test the documentation

`make server`

An look at the URL provided

### Create a github project

Go to https://github.com/new and follow the instructions

### Deploy documentation

`make deploy`

### Register the schema

See [How to register a schema](../faq/contributing)

## Alternative protocols

