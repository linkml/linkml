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
`prefixes <https://linkml.io/linkml-model/docs/prefixes/>`__
declarations and
`default_curi_maps <https://linkml.io/linkml-model/docs/default_curi_maps/>`__.

Any JSON that conforms to the derived JSON Schema (see above) can be
converted to RDF using this context.

Treatment of OBO prefixes
-------------------------

All OBO ontologies use prefixes that end in underscores (for example
``http://purl.obolibrary.org/obo/PATO_``). Note that the JSON-LD 1.1
spec doesn't allow trailing underscores on simple "flat" prefix maps,
i.e this is not correct:

.. code:: json

   "@context": {
       "PATO": "http://purl.obolibrary.org/obo/PATO_",
        }

It must be represented as:
        
.. code:: json

   "@context": {
       "PATO": {
            "@id": "http://purl.obolibrary.org/obo/PATO_",
             "@prefix": true
        }

However, the former can still be convenient, so this can be done with
a flag:

.. code:: bash

   gen-jsonld-context --flatprefixes personinfo.yaml > personinfo.context.jsonld

However, this is not recommended and newer applications should switch
to gen-prefix-map:

.. code:: bash

   gen-prefix-map --flatprefixes personinfo.yaml > personinfo.prefixmap.json


Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.jsonldcontextgen

.. click:: linkml.generators.jsonldcontextgen:cli
    :prog: gen-jsonld-context
    :nested: short

Code
^^^^

                   
.. autoclass:: ContextGenerator
    :members: serialize
