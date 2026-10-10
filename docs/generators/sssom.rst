SSSOM
=====

Generation of Mappings in SSSOM (Simple Standard for Sharing
Ontological Mappings) format

.. seealso:: `SSSOM <https://w3id.org/sssom>`_
             For details of the SSSOM standard

Overview
--------

The output is a SSSOM 1.x mapping set in the SSSOM/TSV format: a YAML
header behind ``#`` lines, then one row per mapping. Each entry in a class,
slot or permissible value's ``exact_mappings``, ``close_mappings``,
``related_mappings``, ``narrow_mappings`` or ``broad_mappings`` becomes a
row whose ``predicate_id`` is the matching SKOS property. A ``class_uri``
or ``slot_uri`` that differs from the element's own URI is written as an
exact mapping to it; one that equals it produces no row. A permissible
value with a ``meaning`` is identified by that term, as it is in the OWL
generator, and labelled with its text or title. Every row carries a
``mapping_justification``, ``semapv:ManualMappingCuration`` unless
``--mapping-justification`` names another term the SSSOM schema admits.
The header carries ``mapping_set_id`` (the schema id with ``mappings``
appended unless ``--mapping-set-id`` says otherwise), ``license`` as a URL
(a SPDX identifier such as ``CC0-1.0`` is mapped to its licence URL; a
value that is neither is reported as
``https://w3id.org/sssom/license/unspecified`` with a ``comment``),
``mapping_provider`` (the schema id), ``mapping_date`` when
``--generation-date`` is set, and a ``curie_map`` covering every prefix
the rows use. The file passes ``sssom validate`` from sssom-py.

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
