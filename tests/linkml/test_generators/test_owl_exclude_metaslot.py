"""gen-owl leaves out the metadata of the metaslots named with ``exclude_metaslots``.

gen-owl writes the value of every metaslot that has a mapping outside ``linkml:``,
for example ``from_schema`` as ``skos:inScheme`` on every class and property.
``--exclude-metaslot`` leaves out selected metaslots; the default output is unchanged.
"""

import pytest
from click.testing import CliRunner
from rdflib import DCTERMS, OWL, RDF, RDFS, SKOS, Graph, Literal, URIRef

from linkml.generators.owlgen import OwlSchemaGenerator, cli

EX = "https://example.org/m/"

SCHEMA = """
id: https://example.org/m
name: m
title: My model
prefixes:
  ex: https://example.org/m/
  linkml: https://w3id.org/linkml/
imports: [linkml:types]
default_prefix: ex
default_range: string
slots:
  age:
    title: age in years
    description: The age.
classes:
  Person:
    title: Natural Person
    description: A person.
    slots: [age]
enums:
  Colour:
    permissible_values:
      red:
        title: Red colour
        description: The colour red.
"""


def _graph(**kwargs) -> Graph:
    """The generated ontology, parsed back from Turtle."""
    generator = OwlSchemaGenerator(SCHEMA, type_objects=False, metaclasses=False, **kwargs)
    return Graph().parse(data=generator.serialize(), format="turtle")


ELEMENTS = [URIRef(EX + "Person"), URIRef(EX + "age")]


def test_default_output_has_in_scheme():
    """Without the option, every class and property is in the scheme of its schema."""
    graph = _graph()
    for element in ELEMENTS:
        assert (element, SKOS.inScheme, URIRef("https://example.org/m")) in graph
    assert (SKOS.inScheme, RDF.type, OWL.AnnotationProperty) in graph


def test_exclude_from_schema():
    """Excluding ``from_schema`` removes ``skos:inScheme`` and its declaration, nothing else."""
    graph = _graph(exclude_metaslots=["from_schema"])
    assert not list(graph.triples((None, SKOS.inScheme, None)))
    assert (SKOS.inScheme, RDF.type, OWL.AnnotationProperty) not in graph
    assert (URIRef(EX + "Person"), DCTERMS.title, Literal("Natural Person")) in graph
    assert (URIRef(EX + "Person"), SKOS.definition, Literal("A person.")) in graph


@pytest.mark.parametrize(
    "subject",
    [
        URIRef(EX + "Person"),
        URIRef(EX + "age"),
        URIRef(EX + "Colour#red"),
        URIRef("https://example.org/m"),
    ],
)
def test_exclude_applies_to_every_element(subject):
    """The option applies to classes, slots, permissible values and the ontology header."""
    assert list(_graph().objects(subject, DCTERMS.title))
    graph = _graph(exclude_metaslots=["title", "description"])
    assert not list(graph.objects(subject, DCTERMS.title))
    assert not list(graph.objects(subject, SKOS.definition))
    assert list(graph.objects(subject, RDFS.label))


def test_unknown_metaslot_fails():
    """A name that is not a metamodel slot is an error, not a silent no-op."""
    with pytest.raises(ValueError, match="in_scheme"):
        OwlSchemaGenerator(SCHEMA, exclude_metaslots=["in_scheme"])


def test_cli_option_is_repeatable(tmp_path):
    """``--exclude-metaslot`` can be given several times."""
    schema = tmp_path / "m.yaml"
    schema.write_text(SCHEMA)
    result = CliRunner().invoke(cli, [str(schema), "--exclude-metaslot", "from_schema", "--exclude-metaslot", "title"])
    assert result.exit_code == 0, result.output
    graph = Graph().parse(data=result.output, format="turtle")
    assert not list(graph.triples((None, SKOS.inScheme, None)))
    assert not list(graph.triples((None, DCTERMS.title, None)))
    assert list(graph.triples((None, SKOS.definition, None)))
