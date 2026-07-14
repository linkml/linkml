Project Generator
=================

Overview
--------

The ProjectGenerator is a wrapper for all other generators, and will
generate a complete project folder, with subfolders for jsonschema,
python, etc

.. seealso:: `linkml-model-template <https://github.com/linkml/linkml-model-template>`_

Built-in generators
-------------------

By default ``gen-project`` runs every generator listed below and writes each
artefact to the shown path (relative to the output directory ``-d``). Use
``--include`` / ``--exclude`` to select a subset by key.

.. list-table::
   :header-rows: 1
   :widths: 15 20 65

   * - Key
     - Output path
     - Generator
   * - ``graphql``
     - ``graphql/{name}.graphql``
     - :class:`~linkml.generators.graphqlgen.GraphqlGenerator`
   * - ``jsonldcontext``
     - ``jsonld/{name}.context.jsonld``
     - :class:`~linkml.generators.jsonldcontextgen.ContextGenerator`
   * - ``jsonld``
     - ``jsonld/{name}.jsonld``
     - :class:`~linkml.generators.jsonldgen.JSONLDGenerator`
   * - ``jsonschema``
     - ``jsonschema/{name}.schema.json``
     - :class:`~linkml.generators.jsonschemagen.JsonSchemaGenerator`
   * - ``owl``
     - ``owl/{name}.owl.ttl``
     - :class:`~linkml.generators.owlgen.OwlSchemaGenerator`
   * - ``prefixmap``
     - ``prefixmap/{name}.yaml``
     - :class:`~linkml.generators.prefixmapgen.PrefixGenerator`
   * - ``proto``
     - ``protobuf/{name}.proto``
     - :class:`~linkml.generators.protogen.ProtoGenerator`
   * - ``python``
     - ``{name}.py``
     - :class:`~linkml.generators.pythongen.PythonGenerator`
   * - ``shex``
     - ``shex/{name}.shex``
     - :class:`~linkml.generators.shexgen.ShExGenerator`
   * - ``shacl``
     - ``shacl/{name}.shacl.ttl``
     - :class:`~linkml.generators.shaclgen.ShaclGenerator`
   * - ``sqltable``
     - ``sqlschema/{name}.sql``
     - :class:`~linkml.generators.sqltablegen.SQLTableGenerator`
   * - ``excel``
     - ``excel/{name}.xlsx``
     - :class:`~linkml.generators.excelgen.ExcelGenerator`

``{name}`` is the stem of the input schema file (e.g. ``personinfo`` for
``personinfo.yaml``).

Configuration file
------------------

Any :class:`ProjectConfiguration` field can be pre-set via ``--config-file``
(YAML). Fields map 1:1 onto the dataclass attributes:

.. code-block:: yaml

    # config.yaml
    directory: out
    mergeimports: true
    excludes: [shex]
    generator_args:
      jsonschema:
        top_class: Container
      owl:
        metaclasses: false
        type_objects: false

.. code-block:: bash

    gen-project --config-file config.yaml personinfo.yaml

See :ref:`the CLI reference <project-generator-cli>` below for the complete
option list, or ``gen-project --help``.

Python API
----------

The same behaviour is available programmatically via
:class:`ProjectConfiguration` and :class:`ProjectGenerator`:

.. code-block:: python

    from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator

    config = ProjectConfiguration(
        directory="out",
        mergeimports=True,
        includes=["python", "jsonschema"],
        generator_args={"jsonschema": {"top_class": "Container"}},
    )
    ProjectGenerator().generate("personinfo.yaml", config)

Extending with additional generators
------------------------------------

Generators that are not part of the built-in map (for example
:class:`~linkml.generators.javagen.JavaGenerator`, ``typedb``, ``typescript``,
``markdown``, ``dbml``, or any third-party generator) can be plugged in via
:attr:`ProjectConfiguration.generators`. Each entry is a
``(generator_class, output_path_template, default_gen_args)`` tuple, matching
the internal :data:`GEN_MAP` shape. User entries with the same key as a
built-in override it.

.. code-block:: python

    from linkml.generators.javagen import JavaGenerator
    from linkml.generators.projectgen import ProjectConfiguration, ProjectGenerator

    config = ProjectConfiguration(
        directory="out",
        generators={
            "java": (JavaGenerator, "java/{name}.java", {"directory": "{parent}"}),
        },
    )
    ProjectGenerator().generate("personinfo.yaml", config)

The path template supports ``{name}`` (schema stem) and, in
``default_gen_args`` string values, additionally ``{parent}`` (the output
subdirectory for that artefact).

Docs
----

Command Line
^^^^^^^^^^^^

.. _project-generator-cli:

.. currentmodule:: linkml.generators.projectgen

.. click:: linkml.generators.projectgen:cli
    :prog: gen-project
    :nested: short

Code
^^^^


.. autoclass:: ProjectGenerator
    :members:

.. autoclass:: ProjectConfiguration
    :members:
