import unittest

from rdflib import URIRef, Graph, Namespace
from rdflib.namespace import RDFS, DCTERMS

from linkml.generators.owlgen import OwlSchemaGenerator, MetadataProfile

from tests.utils.test_environment import TestEnvironmentTestCase
from tests.test_issues.environment import env

# reported in https://github.com/linkml/linkml/issues/711
# export custom annotations

schema_str = """
id: http://example.org/annotation-export
name: annotationexport

prefixes:
  pav: http://purl.org/pav/
  dce: http://purl.org/dc/elements/1.1/
  lego: http://geneontology.org/lego/
  linkml: https://w3id.org/linkml/
  biolink: https://w3id.org/biolink/
  RO: http://purl.obolibrary.org/obo/RO_
  BFO: http://purl.obolibrary.org/obo/BFO_
  CODE: http://example.org/code/
  ROR: http://example.org/ror/
  A: http://example.org/activities/
  P: http://example.org/person/
  skos: http://www.w3.org/2004/02/skos/core#
  bizcodes: https://example.org/bizcodes/
  schema: http://schema.org/
  ae: http://example.org/annotation-export#

default_prefix: ae
default_range: string

imports:
  - https://w3id.org/linkml/types

classes:
  Person:
    title: A person
    description: A person (alive, dead, undead, or fictional).
    slots:
      - name
      - family name
    annotations:
      ae:metadata: "Local prefixed annotation"
      is_current: Local unpredixed annotation
      err:non_existing: "This annotation will be skipped silently"
      oa:describing: "Annotation not in prefxes, but present in metamodel namespaces"
    
slots:
  is current:
    range: boolean
  metadata:
    range: string

  name:
    title: Name
    description: The name of the item.
    annotations:
      ae:metadata: "Local prefixed annotation"
      is_current: Local unpredixed annotation
      err:non_existing: "This annotation will be skipped silently"
      oa:describing: "Annotation not in prefxes, but present in metamodel namespaces"
  
  family name:
    title: Family name
    description: Family name. In the U.S., the last name of a Person.
"""

AE = Namespace('http://example.org/annotation-export#')
OA = Namespace('http://www.w3.org/ns/oa#')

class IssueAnnotationExportCase(TestEnvironmentTestCase):
    env = env

    def test_owlgen_annotation_export(self):
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
        graph = Graph(base=AE)
        graph.parse(data=output, format="ttl")

        # check annotations have been exported for class 'Person'
        self._test_subject_annotations(subject=AE.Person, 
                                       graph=graph)

        # check annotations have been exported for slot 'name'
        self._test_subject_annotations(subject=AE.name,
                                       graph=graph)
        


    def _test_subject_annotations(self, subject, graph):
        # annotation without a prefix in source YAML
        assert (subject, AE.is_current, None) in graph
        # annotation with default prefix
        assert (subject, AE.metadata, None) in graph
        # oa:describing is prefixed with prefix not in local scheme, but present in metamodel
        assert (subject, OA.describing, None) in graph
        # annotation with unknown prefix is skipped silently 
        # err:non_existing must not be present in the result
        predicates = list(graph.predicates(subject=subject, object=None))
        for pred in predicates:
            self.assertFalse("non_existing" in pred,
                             f"Annotation err:non_existing for {subject} should be skipped, but is present in the result.")



if __name__ == '__main__':
    unittest.main()
