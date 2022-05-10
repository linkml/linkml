New Workspace
=============

Overview
--------
If you are a data modeler, and want to start authoring LinkML data models 
to describe the strcuture of your datasets, then the first step to do after 
installing the linkml library itself, is to let linkml do the heavy lifting 
and use it to generate a well defined directory structure for your project.

The workspace generator creates a directory structure is that is based off of 
this Github template: `linkml-project-structure <https://github.com/linkml/linkml-project-template>`_

Some important points to keep in mind about this structure:

* To take advantage of the directory structure, familiarize yourself with 
all the commands that are available at your disposal as Makefile targets, by 
running: 

.. code:: bash
    make help

* Configure the name of your data model and the path to your data model in 
the ::code::`about.yaml` file, since the Makefile targets pick variable names 
from there.

* The core LinkML YAML data model can be found at: ::code::`src > linkml > my_data_model.yaml`.

* The generator super charges your project with automatic documentation generation 
capabilities using `Mkdocs <https://www.mkdocs.org/>`_, and package management 
using `poetry <https://python-poetry.org/>`_.

* To extend the Makefile and add your own custom make targets, that may or may not be 
dependent on the already defined targets and variables, you can specify them in the 
::code::`project.Makefile` file.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.workspaces.cli

.. click:: linkml.workspaces.cli:main
    :prog: linkml-ws new
    :nested: short

Code
^^^^

.. autoclass:: Project
    :members: serialize
