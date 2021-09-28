JSON-LD Contexts
================

.. warning ::

    The JSON-LD context generator does not yet include ``@embed``
    directives necessary for conversion *from* RDF.

.. warning ::

    The JSON-LD context generator does not yet include ``@type``
    directives except at the top level.

Overview
--------

`JSON-LD context <https://www.w3.org/TR/json-ld/#the-context>`__
provides mapping from JSON to RDF.

.. code:: bash

   gen-jsonld-context personinfo.yaml > personinfo.context.jsonld

You can control the output via
`prefixes <https://linkml.io/linkml-model/docs/prefixes.html>`__
declarations and
`default_curi_maps <https://linkml.io/linkml-model/docs/default_curi_maps.html>`__.

Any JSON that conforms to the derived JSON Schema (see above) can be
converted to RDF using this context.

You can also combine a JSON instance file with a JSON-LD context using
simple code or a tool like
`jq <https://stackoverflow.com/questions/19529688/how-to-merge-2-json-objects-from-2-files-using-jq>`__:

.. code:: bash

   jq -s '.[0] * .[1]' examples/organization-data.json examples/organization.context.jsonld > examples/organization-data.jsonld

The above generated `JSON-LD <examples/organization-data.jsonld>`__ file
can be converted to other RDF serialization formats such as
`N-Triples <examples/organization-data.nt>`__. For example we can use
`Apache Jena <https://jena.apache.org/documentation/io/>`__ as follows:

.. code:: bash

   riot examples/organization-data.jsonld > examples/organization-data.nt


Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.jsonld-contextgen

.. click:: linkml.generators.jsonld-contextgen:cli
    :prog: gen-jsonld-context
    :nested: short

Code
^^^^

                   
.. autoclass:: Jsonld-ContextGenerator
    :members: serialize
