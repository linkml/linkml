import logging
import os
from collections import defaultdict
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

import click
from jinja2 import Template

from linkml._version import __version__
from linkml.generators.common.prefixes import (
    document_prefixes,
    normalize_prefixes_option,
    preferred_prefixes,
    standardize_prefix,
)
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import Element, Prefix
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

template = """
{% for pfxn, pfx in prefixes.items() -%}
PREFIX {{pfxn}}: <{{pfx}}>
{% endfor %}

{% for cn, c in schema.classes.items() if not c.mixin and not c.abstract %}

## --
## Checks for {{ cn }}
## --

# @CHECK permitted_{{cn}}
SELECT ?g ?s ?p WHERE {
 GRAPH ?g {
  ?s rdf:type {{ uri(cn) }} ;
     ?p ?o .
  FILTER ( ?p NOT IN (
   {% for sn in schema_view.class_slots(cn) -%}
   {{ uri(schema_view.get_slot(sn, attributes=True)) }},
   {% endfor -%}
   rdf:type ))
 }
 {{ extra }}
} {{ limit }}


{% for slot in schema_view.class_induced_slots(cn) -%}

{% if slot.required %}
# @CHECK required_{{cn}}_{{slot.name}}
SELECT
  ?check
  ?graph
  ?subject
  ?predicate WHERE {
 GRAPH ?graph {
  ?subject rdf:type {{ uri(cn) }} .
  FILTER NOT EXISTS { ?subject  {{ uri(slot) }} ?o  }
 }
 VALUES ?check { linkml:required }
 VALUES ?predicate { {{uri(slot)}} }
 {{ extra }}
}  {{ limit }}
{% endif %}

{% if slot.range in schema_view.all_classes() %}
# @CHECK object_range_{{cn}}_{{slot.name}}
SELECT
  ?check
  ?graph
  ?subject
  ?predicate
  ?object
WHERE {
 GRAPH ?graph {
  ?subject rdf:type {{ uri(cn) }} ;
     ?predicate ?object .
  FILTER NOT EXISTS {
    ?object rdf:type ?otype .
    FILTER ( ?otype IN (
      {% for a in schema_view.class_descendants(slot.range) -%}
      {{ uri(a) }}
      {{ ", " if not loop.last else "" }}
      {% endfor -%} ))
  }
 }
 VALUES ?check { linkml:range }
 VALUES ?predicate { {{ uri(slot) }}  }
 {{ extra }}
}  {{ limit }}
{% endif %}

{%- endfor %}


## -- End of checks for {{ cn }}
{% endfor %}
"""

x = """
{% for sn in schema_view.class_slots(c.name) %}
     {{ schema.slots[sn].slot_uri }}
   {% endfor %}
"""


def materialize_schema(schemaview: SchemaView):
    schema = schemaview.schema
    if "rdf" not in schema.prefixes:
        schema.prefixes["rdf"] = Prefix("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    for scn in schemaview.imports_closure():
        for pfxn, pfx in schemaview.schema_map[scn].prefixes.items():
            if pfxn not in schema:
                schema.prefixes[pfxn] = pfx
    for cn, c in schemaview.all_classes().items():
        for a in list(c.attributes.values()):
            schema.slots[a.name] = a
            c.slots.append(a.name)
            del c.attributes[a.name]
    schemaview.set_modified()
    for cn, c in schemaview.all_classes().items():
        for s in schemaview.class_induced_slots(cn):
            if s.name not in c.slots:
                c.slots.append(s.name)
            c.slot_usage[s.name] = s
            s.slot_uri = schemaview.get_uri(s)


@dataclass
class SparqlGenerator(Generator):
    """
    Generates SPARQL queries that can be used for delayed validation
    """

    # ClassVars
    generatorname = os.path.basename(__file__)
    valid_formats = ["sparql"]
    visit_all_class_slots = False
    uses_schemaloader = False

    # ObjectVars
    named_graphs: list[str] | None = None
    limit: int | None = None
    sparql: str | None = None
    normalize_prefixes: bool = False
    """Write the conventional prefix names of :mod:`linkml.generators.common.prefixes`,
    e.g. ``dc`` where the schema declares ``dce`` for ``http://purl.org/dc/elements/1.1/``."""

    def __post_init__(self):
        super().__post_init__()
        # The plan reads the schema as given, before materialization adds the imports' prefixes.
        self._prefix_plan = preferred_prefixes(self.schemaview) if self.normalize_prefixes else None
        # Materialization rewrites the schema (attributes -> slots, extra prefixes), so work on a
        # copy: mutating the shared SchemaView corrupts the input for any generator that runs after
        # us under gen-project (#3770). Copying the whole view preserves import-resolution context.
        self.schemaview = deepcopy(self.schemaview)
        materialize_schema(self.schemaview)
        self.schema = self.schemaview.schema
        self.queries = self.generate_sparql(named_graphs=self.named_graphs, limit=self.limit)

    def generate_sparql(self, named_graphs=None, limit: int = None):
        template_obj = Template(template)
        extra = ""
        if named_graphs is not None:
            extra += f"FILTER( ?graph in ( {','.join(named_graphs)} ))"
        logger.info(f"Named Graphs = {named_graphs} // extra={extra}")
        if limit is not None and isinstance(limit, int):
            limit = f"LIMIT {limit}"
        else:
            limit = ""
        sv = self.schemaview
        prefixes = {str(name): str(p.prefix_reference) for name, p in self.schema.prefixes.items()}
        plan = None
        if self._prefix_plan is not None:
            plan = document_prefixes(prefixes, self._prefix_plan)
            prefixes = {record.prefix: record.uri_prefix for record in plan.records}

        def uri(element: Element | str) -> str:
            curie = sv.get_uri(element)
            return curie if plan is None else standardize_prefix(curie, plan)

        sparql = template_obj.render(
            schema_view=sv, schema=self.schema, prefixes=prefixes, uri=uri, limit=limit, extra=extra
        )
        self.sparql = sparql
        queries = self.split_sparql(sparql)
        return queries

    def serialize(self, directory=None) -> str:
        if directory is not None:
            Path(directory).mkdir(parents=True, exist_ok=True)
            for qn, q in self.queries.items():
                qpath = os.path.join(directory, f"{qn}.rq")
                with open(qpath, "w", encoding="UTF-8") as stream:
                    stream.write(q)
        return self.sparql

    @staticmethod
    def split_sparql(sparql: str) -> dict[str, str]:
        lines = sparql.split("\n")
        prolog = ""
        queries = defaultdict(str)
        q = None
        for line in lines:
            if line.startswith("# @"):
                q = underscore(line.replace("# @", ""))
                queries[q] = prolog + "\n"
            elif q is None:
                if line.lower().startswith("prefix"):
                    prolog += line + "\n"
            else:
                queries[q] += line + "\n"
        return queries


@shared_arguments(SparqlGenerator)
@click.command(name="sparql")
@click.option("--dir", "-d", help="Directory in which queries will be deposited")
@normalize_prefixes_option
@click.version_option(__version__, "-V", "--version")
def cli(yamlfile, dir, **kwargs):
    """Generate SPARQL queries for validation

    This will generate a directory of queries that can be used for QC over a triplestore that
    is conformant to the same LinkML schema.

    Each query in the directory will be of the form

        CHECK_<ConstraintType>_<SchemaElement>.rq

    Example:

        gen-sparql -d ./sparql/ personinfo.yaml
    """
    SparqlGenerator(yamlfile, **kwargs).serialize(directory=dir)


if __name__ == "__main__":
    cli()
