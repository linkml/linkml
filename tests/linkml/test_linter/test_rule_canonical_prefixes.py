from linkml_runtime import SchemaView

from linkml.linter.config.datamodel.config import CanonicalPrefixesConfig, RuleLevel
from linkml.linter.rules import CanonicalPrefixesRule
from linkml.utils.schema_builder import SchemaBuilder


def test_default_merged_context():
    builder = SchemaBuilder()
    builder.add_prefix("CHEBI", "http://purl.obolibrary.org/obo/CHEBI_")
    builder.add_prefix("GEO", "http://purl.obolibrary.org/obo/GEO_")
    builder.add_prefix("UPHENO", "http://example.com/wrong/upheno_")
    builder.add_prefix("WRONG", "http://identifiers.org/orcid/")

    schema_view = SchemaView(builder.schema)
    config = CanonicalPrefixesConfig(level=RuleLevel.error, prefixmaps_contexts=["merged"])

    rule = CanonicalPrefixesRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 2

    messages = [p.message for p in problems]
    assert (
        "Schema maps prefix 'UPHENO' to namespace 'http://example.com/wrong/upheno_' "
        "instead of namespace 'http://purl.obolibrary.org/obo/UPHENO_'" in messages
    )
    assert (
        "Schema maps prefix 'WRONG' to namespace 'http://identifiers.org/orcid/' "
        "instead of using prefix 'ORCID'" in messages
    )


def test_custom_context():
    builder = SchemaBuilder()
    builder.add_prefix("CHEBI", "http://purl.obolibrary.org/obo/CHEBI_")
    builder.add_prefix("GEO", "http://identifiers.org/geo/")
    builder.add_prefix("UPHENO", "http://example.com/wrong/upheno_")
    builder.add_prefix("WRONG", "http://identifiers.org/orcid/")

    schema_view = SchemaView(builder.schema)
    config = CanonicalPrefixesConfig(
        level=RuleLevel.error,
        prefixmaps_contexts=["bioregistry.upper", "prefixcc", "obo"],
    )

    rule = CanonicalPrefixesRule(config)
    problems = list(rule.check(schema_view))

    assert len(problems) == 2
    messages = [p.message for p in problems]
    assert (
        "Schema maps prefix 'UPHENO' to namespace 'http://example.com/wrong/upheno_' "
        "instead of namespace 'http://purl.obolibrary.org/obo/UPHENO_'" in messages
    )
    assert (
        "Schema maps prefix 'WRONG' to namespace 'http://identifiers.org/orcid/' "
        "instead of using prefix 'ORCID'" in messages
    )
