Markdown
========

Overview
--------

.. admonition:: Deprecated
    :class: warning

        We have two Markdown documentation generators within the linkml framework - ``gen-doc`` and ``gen-markdown``.
        It is important to note that while ``gen-markdown`` still works, it has been deprecated (no active development)
        in favour of the de facto ``gen-doc`` generator.

Docs
----

Command Line
^^^^^^^^^^^^

.. currentmodule:: linkml.generators.markdowngen

.. click:: linkml.generators.markdowngen:cli
    :prog: gen-markdown
    :nested: short

Code
^^^^

.. autoclass:: MarkdownGenerator
    :members: serialize
