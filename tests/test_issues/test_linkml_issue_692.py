import unittest

from rdflib import URIRef, Graph
from rdflib.namespace import RDFS, DCTERMS

from linkml.generators.owlgen import OwlSchemaGenerator, MetadataProfile

from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

# reported in https://github.com/linkml/linkml/issues/692
# description metaproperty is not being exported with owl-gen

schema_str = """
id: http://example.org/description-export
name: descriptionexport
imports:
  - https://w3id.org/linkml/types
default_range: string

classes:
  Person:
    title: A person
    description: A person (alive, dead, undead, or fictional).
    slots:
        - name
        - family name
    
slots:
  name:
    title: Name
    description: The name of the item.
  
  family name:
    title: Family name
    description: Family name. In the U.S., the last name of a Person.
"""

class IssueDescriptionExportCase(TestEnvironmentTestCase):
    env = env

    def test_owlgen_rdfs_profile(self):
        # export the source schema containing both title and description
        gen = OwlSchemaGenerator(schema_str,
                                 ontology_uri_suffix=None,
                                 type_objects=False,
                                 metaclasses=False,
                                 add_ols_annotations=True,
                                 metadata_profile=MetadataProfile.rdfs,
                                 format="ttl")
        output = gen.serialize()

        # load back via rdflib
        graph = Graph(base="http://example.org/description-export")
        graph.parse(data=output, format="ttl")

        # check if graph contains dcterms:title for class 'Person'
        person_class = URIRef(f"{graph.base}/Person")
        assert (person_class, DCTERMS.title, None) in graph

        # check if graph contains dcterms:title for property 'name'
        name_prop = URIRef(f"{graph.base}/name")
        assert (name_prop, DCTERMS.title, None) in graph

        # now check rdfs:comment for class 'Person'
        assert (person_class, RDFS.comment, None) in graph

        # and check rdfs:comment for property 'name' too
        assert (name_prop, RDFS.comment, None) in graph



if __name__ == '__main__':
    unittest.main()
