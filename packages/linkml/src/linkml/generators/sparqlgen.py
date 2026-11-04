import logging
import os
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import click
from jinja2 import Template

from linkml._version import __version__
from linkml.utils.generator import Generator, shared_arguments
from linkml_runtime.linkml_model.meta import Prefix, SlotDefinition
from linkml_runtime.utils.formatutils import underscore
from linkml_runtime.utils.schemaview import SchemaView

logger = logging.getLogger(__name__)

template = """
{% for pfxn, pfx in prefixes.items() -%}
PREFIX {{pfxn}}: <{{pfx.prefix_reference}}>
{% endfor %}

{% for cn, c in schema_view.all_classes(imports=imports).items() if not c.mixin and not c.abstract %}

## --
## Checks for {{ cn }}
## --

# @CHECK permitted_{{cn}}
SELECT ?g ?s ?p WHERE {
 GRAPH ?g {
  ?s rdf:type {{ schema_view.get_uri(cn) }} ;
     ?p ?o .
  FILTER ( ?p NOT IN (
   {% for slot in schema_view.class_induced_slots(cn) -%}
   {{ slot_uri(schema_view, cn, slot) }},
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
  ?subject rdf:type {{ schema_view.get_uri(cn) }} .
  FILTER NOT EXISTS { ?subject  {{ slot_uri(schema_view, cn, slot) }} ?o  }
 }
 VALUES ?check { linkml:required }
 VALUES ?predicate { {{ slot_uri(schema_view, cn, slot) }} }
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
  ?subject rdf:type {{ schema_view.get_uri(cn) }} ;
     ?predicate ?object .
  FILTER NOT EXISTS {
    ?object rdf:type ?otype .
    FILTER ( ?otype IN (
      {% for a in schema_view.class_descendants(slot.range) -%}
      {{ schema_view.get_uri(a) }}
      {{ ", " if not loop.last else "" }}
      {% endfor -%} ))
  }
 }
 VALUES ?check { linkml:range }
 VALUES ?predicate { {{ slot_uri(schema_view, cn, slot) }}  }
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


def query_prefixes(schemaview: SchemaView) -> dict[str, Prefix]:
    """Return the prefixes that the queries declare.

    A query can name a class or slot from any imported schema, even when no query is written for
    that class, so the prefixes of every imported schema are included. When two schemas declare the
    same prefix, the schema given to the generator comes first, and then the order of the imports.
    """
    prefixes = dict(schemaview.schema.prefixes)
    prefixes.setdefault("rdf", Prefix("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#"))
    for schema in schemaview.all_schema():
        for name, prefix in schema.prefixes.items():
            prefixes.setdefault(name, prefix)
    return prefixes


def slot_uri(schemaview: SchemaView, class_name: str, slot: SlotDefinition) -> str:
    """Return the URI of an induced slot of a class.

    A slot with no declared URI takes the default prefix of the schema that defines it. An induced
    slot cannot name that schema, because a ``slot_usage`` in another schema replaces its
    ``from_schema``, so this function finds the definition again. An attribute of the class or of an
    ancestor comes before a schema-level slot of the same name, as in ``SchemaView.induced_slot``.
    """
    if slot.slot_uri:
        return slot.slot_uri
    for ancestor in schemaview.class_ancestors(class_name):
        attributes = schemaview.get_class(ancestor).attributes
        if slot.name in attributes:
            return schemaview.get_uri(attributes[slot.name])
    return schemaview.get_uri(schemaview.get_slot(slot.name, attributes=False))


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

    def __post_init__(self):
        super().__post_init__()
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
        sparql = template_obj.render(
            schema_view=self.schemaview,
            prefixes=query_prefixes(self.schemaview),
            slot_uri=slot_uri,
            limit=limit,
            extra=extra,
            imports=bool(self.mergeimports),
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
