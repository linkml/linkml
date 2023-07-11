import logging
import sys
from dataclasses import dataclass
from typing import Union

import click
from linkml_runtime.linkml_model import SchemaDefinition
from linkml_runtime.utils.schemaview import SchemaView
from rdflib import Graph
from SPARQLWrapper import JSON, SPARQLWrapper

from linkml._version import __version__
from linkml.generators.sparqlgen import SparqlGenerator
from linkml.reporting import CheckResult, Report
from linkml.utils.datautils import _get_format, dumpers_loaders, get_dumper
from linkml.utils.datavalidator import DataValidator


def sparqljson2dict(row: dict):
    return {k: v["value"] for k, v in row.items()}


def _make_result(row):
    return CheckResult(
        type=row.get("check"),
        source=row.get("graph"),
        subject=row.get("subject"),
        predicate=row.get("predicate"),
    )


@dataclass
class SparqlDataValidator(DataValidator):
    schema: SchemaDefinition = None
    queries: dict = None

    def validate_file(self, input: str, format: str = "turtle", **kwargs):
        g = Graph()
        g.parse(input, format=format)
        return self.validate_graph(g, **kwargs)

    def validate_graph(self, g: Graph, **kwargs):
        if self.queries is None:
            self.queries = SparqlGenerator(self.schema, **kwargs).queries
        invalid = []
        for qn, q in self.queries.items():
            print(f"QUERY: {qn}")
            q: str

            # q = "\n".join([line for line in q.split('\n') if not line.lower().startswith('prefix')])
            print(q)
            qres = g.query(q)
            try:
                qres = g.query(q)
                for row in qres:
                    invalid += row
            except Exception:
                logging.error(f"FAILED: {qn}")
        return invalid

    def validate_endpoint(self, url: str, **kwargs):
        if self.queries is None:
            self.queries = SparqlGenerator(self.schema, **kwargs).queries
        invalid = []
        report = Report()
        for qn, q in self.queries.items():
            q += " LIMIT 20"
            logging.debug(f"QUERY: {qn}")
            logging.debug(f"{q}")
            sw = SPARQLWrapper(url)
            sw.setQuery(q)
            sw.setReturnFormat(JSON)
            sw_q = sw.query()
            results = sw_q.convert()
            for row in results["results"]["bindings"]:
                row = sparqljson2dict(row)
                report.results.append(_make_result(row))
                invalid += row
        return report

    def load_schema(self, schema: Union[str, SchemaDefinition]):
        self.schemaview = SchemaView(schema)
        self.schema = self.schemaview.schema
        # self.schema = YAMLGenerator(schema).schema
        return self.schema


@click.command()
@click.option("--named-graph", "-G", multiple=True, help="Constrain query to a named graph")
@click.option("--input", "-i", help="Input file to validate")
@click.option("--endpoint-url", "-U", help="URL of sparql endpoint")
@click.option("--limit", "-L", help="Max results per query")
@click.option("--output", "-o", help="Path to report file")
@click.option(
    "--input-format",
    "-f",
    type=click.Choice(list(dumpers_loaders.keys())),
    help="Input format. Inferred from input suffix if not specified",
)
@click.option(
    "--output-format",
    "-t",
    type=click.Choice(list(dumpers_loaders.keys())),
    help="Output format. Inferred from output suffix if not specified",
)
@click.option("--schema", "-s", help="Path to schema specified as LinkML yaml")
@click.version_option(__version__, "-V", "--version")
def cli(
    input,
    output=None,
    input_format=None,
    output_format=None,
    endpoint_url=None,
    limit=None,
    named_graph=None,
    schema=None,
) -> None:
    """
    Validates sparql

    Example:

        linkml-sparql-validate -U http://sparql.hegroup.org/sparql -s tests/test_validation/input/omo.yaml
    """
    validator = SparqlDataValidator(schema)
    if endpoint_url is not None:
        results = validator.validate_endpoint(endpoint_url, limit=limit, named_graphs=named_graph)
    else:
        if input is None:
            raise Exception("Must pass one of --endpoint-url OR --input")
        input_format = _get_format(input, input_format)
        results = validator.validate_file(input, format=input_format)
    output_format = _get_format(output, output_format, default="json")
    dumper = get_dumper(output_format)
    if output is not None:
        dumper.dump(results, output)
    else:
        print(dumper.dumps(results))


if __name__ == "__main__":
    cli(sys.argv[1:])
