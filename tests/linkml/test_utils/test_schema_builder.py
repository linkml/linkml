from linkml_runtime.utils.schema_builder import SchemaBuilder


def test_deprecated_import_from_linkml():
    """
    Importing SchemaBuilder from linkml.utils.schema_builder should trigger
    the deprecation system and re-export the same class from linkml_runtime.
    """
    import linkml.utils.deprecation as dep_mod
    import linkml.utils.schema_builder as mod

    # Verify the deprecation was registered during module import
    assert "schema-builder-import-location" in dep_mod.EMITTED

    # Verify the re-exported class is the canonical one from linkml_runtime
    assert mod.SchemaBuilder is SchemaBuilder
