Prefix Generator
================

Overview
--------

The prefix generator can be used to create a mapping between prefixes and URIs or IRIs. Prefixes
are essentially shorthands or aliases to these longer URIs or IRIs. The aliases and their corresponding
expansions are specified as key value pairs under the :code:`prefixes` section of a LinkML schema.
You can read more about `prefixes <https://linkml.io/linkml/schemas/uris-and-mappings.html?highlight=prefixes#uri-prefixes>`__ and
`URIs, IRIs and CURIEs <https://linkml.io/linkml/schemas/uris-and-mappings.html?highlight=prefixes#background-uris-iris-and-curies>`__ in the
`URIs and Mappings <https://linkml.io/linkml/schemas/uris-and-mappings.html?highlight=prefixes#uris-and-mappings>`__ section of
the docs.

Example Output
--------------

`personinfo.json <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/prefixmap/personinfo.json>`_
`personinfo.tsv <https://github.com/linkml/linkml/tree/main/examples/PersonSchema/personinfo/prefixmap/personinfo.tsv>`_

To generate a JSON style mapping, run:

.. code:: bash

   gen-prefix-map examples/personinfo.yaml --output examples/personinfo.json

To generate a simple TSV style mapping, run:

.. code:: bash

   gen-prefix-map examples/personinfo.yaml --output examples/personinfo.tsv

If you want to simply view the data in the format of your choice, use the :code:`--format` option.

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.prefixmapgen:cli
    :prog: gen-prefix-map
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.prefixmapgen
