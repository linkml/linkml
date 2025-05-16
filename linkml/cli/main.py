"""
Main ``linkml`` entrypoint

Gathers all the other linkml click entrypoints and puts them under ``linkml`` :)
"""

import click

from linkml._version import __version__
from linkml.generators.csvgen import cli as gen_csv
from linkml.generators.dbmlgen import cli as gen_dbml
from linkml.generators.docgen import cli as gen_doc
from linkml.generators.dotgen import cli as gen_graphviz
from linkml.generators.erdiagramgen import cli as gen_erdiagram
from linkml.generators.excelgen import cli as gen_excel
from linkml.generators.golanggen import cli as gen_golang
from linkml.generators.golrgen import cli as gen_golr_views
from linkml.generators.graphqlgen import cli as gen_graphql
from linkml.generators.javagen import cli as gen_java
from linkml.generators.jsonldcontextgen import cli as gen_jsonld_context
from linkml.generators.jsonldgen import cli as gen_jsonld
from linkml.generators.jsonschemagen import cli as gen_json_schema
from linkml.generators.linkmlgen import cli as gen_linkml
from linkml.generators.markdowngen import cli as gen_markdown
from linkml.generators.namespacegen import cli as gen_namespaces
from linkml.generators.owlgen import cli as gen_owl
from linkml.generators.panderagen import cli as gen_pandera
from linkml.generators.plantumlgen import cli as gen_plantuml
from linkml.generators.prefixmapgen import cli as gen_prefix_map
from linkml.generators.projectgen import cli as gen_project
from linkml.generators.protogen import cli as gen_proto
from linkml.generators.pydanticgen import cli as gen_pydantic
from linkml.generators.pythongen import cli as gen_python
from linkml.generators.rdfgen import cli as gen_rdf
from linkml.generators.shaclgen import cli as gen_shacl
from linkml.generators.shexgen import cli as gen_shex
from linkml.generators.sparqlgen import cli as gen_sparql
from linkml.generators.sqlalchemygen import cli as gen_sqla
from linkml.generators.sqltablegen import cli as gen_sqltables
from linkml.generators.sssomgen import cli as gen_sssom
from linkml.generators.summarygen import cli as gen_summary
from linkml.generators.terminusdbgen import cli as gen_terminusdb
from linkml.generators.typescriptgen import cli as gen_typescript
from linkml.generators.yamlgen import cli as gen_yaml
from linkml.generators.yumlgen import cli as gen_yuml
from linkml.linter.cli import main as linkml_lint
from linkml.utils.converter import cli as linkml_convert
from linkml.utils.execute_tutorial import cli as run_tutorial
from linkml.utils.schema_fixer import main as linkml_schema_fixer
from linkml.utils.sqlutils import main as linkml_sqldb
from linkml.validator.cli import cli as linkml_validate
from linkml.workspaces.example_runner import cli as linkml_run_examples

# --------------------------------------------------
# Command groups
# --------------------------------------------------


@click.group()
@click.version_option(__version__, "-V", "--version")
def linkml():
    """
    LinkML: A flexible linked data modeling language
    """


@linkml.group()
@click.version_option(__version__, "-V", "--version")
def generate():
    """
    Generate formats from a LinkML schema
    """


@linkml.group()
@click.version_option(__version__, "-V", "--version")
def dev():
    """
    Helper tools for linkml development
    """


# --------------------------------------------------
# Add commands to groups
# --------------------------------------------------

# Top-level linkml commands
linkml.add_command(linkml_convert, name="convert")
linkml.add_command(linkml_lint, name="lint")
linkml.add_command(linkml_sqldb, name="sqldb")
linkml.add_command(linkml_schema_fixer, name="fix")
linkml.add_command(linkml_run_examples, name="examples")
linkml.add_command(linkml_validate, name="validate")

# Generators
generate.add_command(gen_jsonld_context, name="jsonld-context")
generate.add_command(gen_prefix_map, name="prefix-map")
generate.add_command(gen_csv, name="csv")
generate.add_command(gen_graphviz, name="graphviz")
generate.add_command(gen_golang, name="golang")
generate.add_command(gen_golr_views, name="golr-views")
generate.add_command(gen_graphql, name="graphql")
generate.add_command(gen_java, name="java")
generate.add_command(gen_jsonld, name="jsonld")
generate.add_command(gen_json_schema, name="json-schema")
generate.add_command(gen_markdown, name="markdown")
generate.add_command(gen_doc, name="doc")
generate.add_command(gen_namespaces, name="namespaces")
generate.add_command(gen_owl, name="owl")
generate.add_command(gen_plantuml, name="plantuml")
generate.add_command(gen_proto, name="proto")
generate.add_command(gen_python, name="python")
generate.add_command(gen_pydantic, name="pydantic")
generate.add_command(gen_pandera, name="pandera")
generate.add_command(gen_rdf, name="rdf")
generate.add_command(gen_shex, name="shex")
generate.add_command(gen_shacl, name="shacl")
generate.add_command(gen_sparql, name="sparql")
generate.add_command(gen_typescript, name="typescript")
generate.add_command(gen_terminusdb, name="terminusdb")
generate.add_command(gen_yuml, name="yuml")
generate.add_command(gen_yaml, name="yaml")
generate.add_command(gen_erdiagram, name="erdiagram")
generate.add_command(gen_sqla, name="sqla")
generate.add_command(gen_sqltables, name="sqltables")
generate.add_command(gen_summary, name="summary")
generate.add_command(gen_project, name="project")
generate.add_command(gen_excel, name="excel")
generate.add_command(gen_sssom, name="sssom")
generate.add_command(gen_linkml, name="linkml")
generate.add_command(gen_dbml, name="dbml")

# Dev helpers
dev.add_command(run_tutorial, name="tutorial")
