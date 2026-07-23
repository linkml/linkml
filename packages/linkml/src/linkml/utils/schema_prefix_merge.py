"""Helper for merging prefixes from imported sub-schemas into a SchemaView's root schema.

The `SchemaLoader` path (used by generators with ``uses_schemaloader = True``) already
merges prefixes via :func:`linkml.utils.mergeutils.merge_namespaces`. However, generators
that work directly with a :class:`linkml_runtime.utils.schemaview.SchemaView` (i.e.,
``uses_schemaloader = False``) only see the prefixes declared on the *root* schema —
prefixes contributed by imported sub-schemas are not propagated onto
``schemaview.schema.prefixes``.

This module provides :func:`materialize_prefixes`, which walks the SchemaView import
closure and copies absolute prefix declarations from imported schemas onto the root
schema. The operation is idempotent and never overwrites an existing prefix.

Typical usage in a generator::

    from linkml.utils.schema_prefix_merge import materialize_prefixes

    self.schemaview = SchemaView(schema)
    materialize_prefixes(self.schemaview)
"""

from __future__ import annotations

from linkml_runtime.linkml_model.meta import Prefix
from linkml_runtime.utils.schemaview import SchemaView


def materialize_prefixes(schemaview: SchemaView) -> None:
    """Merge prefixes from imported sub-schemas onto the root schema in-place.

    For every schema in ``schemaview.imports_closure()``, each absolute prefix
    (i.e., one whose reference contains ``://``) declared on that schema is copied
    onto ``schemaview.schema.prefixes`` if it is not already present. Existing
    prefixes are never overwritten, and relative prefix references are skipped.

    :param schemaview: SchemaView whose root schema should receive merged prefixes.
    """
    root = schemaview.schema
    if root.prefixes is None:
        root.prefixes = {}
    schema_map = schemaview.schema_map
    for schema_name in schemaview.imports_closure():
        imported = schema_map.get(schema_name)
        if imported is None or not imported.prefixes:
            continue
        for pfx_name, pfx in imported.prefixes.items():
            if pfx_name in root.prefixes:
                continue
            reference = pfx.prefix_reference
            if reference is None or "://" not in reference:
                continue
            root.prefixes[pfx_name] = Prefix(pfx_name, reference)
