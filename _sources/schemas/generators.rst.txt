.. _topic_generators:

Generators
==========

LinkML comes with a number of *generators* which will generate a
representation of a schema using an alternative framework. This allows
LinkML users to leverage toolchains from these frameworks. For example,
LinkML can be compiled to JSON-Schema, and JSON-Schema validators can be
used for JSON data.

Note that there is often an impedance mismatch between LinkML and
other formalisms. For example, LinkML has a rich inheritance model
that is either partially supported or unsupported in other
languages. We employ techniques such as *rolling down* slots when
doing generation - e.g. generating JSON-Schema.

To see examples of generator outputs, see
`PersonSchema <https://github.com/linkml/linkml/tree/main/examples/PersonSchema>`_

See `generators docs <../generators>`_ for a full list of generators


