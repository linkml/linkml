SSSOM
=====

Generation of Mappings in SSSOM (Simple Standard for Sharing
Ontological Mappings) format

.. seealso:: `SSSOM <https://w3id.org/sssom>`_
             For details of the SSSOM standard

Overview
--------

The output is a SSSOM 1.x mapping set in the SSSOM/TSV format: a YAML header on
lines that start with ``#``, then one row per mapping.

The generator writes one row for each entry in the ``exact_mappings``,
``close_mappings``, ``related_mappings``, ``narrow_mappings`` or
``broad_mappings`` of a class, slot or permissible value, with the matching SKOS
property as its ``predicate_id``. An entry in the generic ``mappings`` slot
becomes a ``skos:mappingRelation`` row, unless a more specific row already
relates the same two terms. A ``class_uri`` or ``slot_uri`` that differs from
the element's own URI is written as an exact mapping to it. One that equals the
element's own URI produces no row.

A permissible value is identified by its enum's URI, a ``#`` and its text, which
is how the OWL generator names a value without a ``meaning``. It is labelled
with its title or text, and its ``meaning`` is written as an exact mapping. Full
URIs that a declared prefix covers are written as CURIEs. Every row carries a
``mapping_justification``: ``semapv:ManualMappingCuration``, unless
``--mapping-justification`` names another term that the SSSOM schema admits.

The header carries these keys:

* ``mapping_set_id``: the schema id with ``mappings`` appended, unless
  ``--mapping-set-id`` gives another id.
* ``license``: a URL. A CURIE is expanded, and an SPDX identifier such as
  ``CC0-1.0`` is mapped to its licence URL. Any other value is reported as
  ``https://w3id.org/sssom/license/unspecified``, with a ``comment``.
* ``mapping_provider``: the schema id.
* ``publication_date``: written when ``--generation-date`` is set.
* ``curie_map``: a map that covers every prefix the rows use.

The file passes ``sssom validate`` from sssom-py when the schema declares every
prefix that its mappings use. The generator warns about any prefix it cannot
declare.

Docs
----

Command Line
^^^^^^^^^^^^

.. click:: linkml.generators.sssomgen:cli
    :prog: gen-sssom
    :nested: full

Code
^^^^

.. currentmodule:: linkml.generators.sssomgen
