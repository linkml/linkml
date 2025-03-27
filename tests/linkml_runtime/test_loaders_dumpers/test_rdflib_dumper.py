import os
import unittest
import logging
from pathlib import Path

from curies import Converter
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, SKOS, XSD
from rdflib import Namespace

from linkml_runtime import MappingError, DataNotFoundError
from linkml_runtime.dumpers import rdflib_dumper, yaml_dumper
from linkml_runtime.linkml_model import Prefix
from linkml_runtime.loaders import yaml_loader
from linkml_runtime.loaders import rdflib_loader
from linkml_runtime.utils.schemaview import SchemaView
from tests.test_loaders_dumpers import INPUT_DIR, OUTPUT_DIR
from tests.test_loaders_dumpers.models.personinfo import Container, Person, Address, Organization, OrganizationType
from tests.test_loaders_dumpers.models.node_object import NodeObject, Triple
from tests.test_loaders_dumpers.models.phenopackets import PhenotypicFeature, OntologyClass, Phenopacket, MetaData, \
    Resource

logger = logging.getLogger(__name__)


SCHEMA = os.path.join(INPUT_DIR, 'personinfo.yaml')
DATA = os.path.join(INPUT_DIR, 'example_personinfo_data.yaml')
DATA_TTL = os.path.join(INPUT_DIR, 'example_personinfo_data.ttl')
OUT = os.path.join(OUTPUT_DIR, 'example_personinfo_data.ttl')
DATA_ROUNDTRIP = os.path.join(OUTPUT_DIR, 'example_personinfo_data.roundtrip-rdf.yaml')
UNMAPPED_ROUNDTRIP = os.path.join(OUTPUT_DIR, 'example_personinfo_data.unmapped-preds.yaml')

PREFIX_MAP = {
    'CODE': 'http://example.org/code/',
    'ROR': 'http://example.org/ror/',
    'P': 'http://example.org/P/',
    'GEO': 'http://example.org/GEO/',
}

unmapped_predicates_test_ttl = """
@prefix P: <http://example.org/P/> .
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix sdo: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix unmapped: <http://example.org/unmapped/> .

P:001 a sdo:Person ;
    sdo:email "fred.bloggs@example.com" ;
    sdo:gender <http://purl.obolibrary.org/obo/GSSO_000371> ;
    sdo:name "fred bloggs" ;
    unmapped:foo "foo" ;
    personinfo:age_in_years 33 .
"""

unmapped_type_test_ttl = """
@prefix P: <http://example.org/P/> .
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix sdo: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix unmapped: <http://example.org/unmapped/> .

P:001 a unmapped:Person ;
    sdo:email "fred.bloggs@example.com" ;
    sdo:gender <http://purl.obolibrary.org/obo/GSSO_000371> ;
    sdo:name "fred bloggs" ;
    personinfo:age_in_years 33 .
"""

enum_union_type_test_ttl = """
@prefix P: <http://example.org/P/> .
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix sdo: <http://schema.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix famrel: <https://example.org/FamilialRelations#> .

P:001 a sdo:Person ;
    sdo:email "fred.bloggs@example.com" ;
    sdo:name "fred bloggs" ;
    personinfo:age_in_years 33 ;
    personinfo:has_interpersonal_relationships [ 
      a personinfo:InterpersonalRelationship ;
      personinfo:type famrel:70 ;
      personinfo:related_to P:002 
    ] ,
    [ 
      a personinfo:InterpersonalRelationship ;
      personinfo:type "BEST_FRIEND_OF" ;
      personinfo:related_to P:003 
    ] .
"""

blank_node_test_ttl = """
@prefix personinfo: <https://w3id.org/linkml/examples/personinfo/> .
@prefix sdo: <http://schema.org/> .

[ a sdo:PostalAddress ;
            personinfo:city "foo city" ;
            personinfo:street "1 foo street" ] .
"""

P = Namespace('http://example.org/P/')
ROR = Namespace('http://example.org/ror/')
CODE = Namespace('http://example.org/code/')
INFO = Namespace('https://w3id.org/linkml/examples/personinfo/')
SDO = Namespace('http://schema.org/')
GSSO = Namespace('http://purl.obolibrary.org/obo/GSSO_')
HP = Namespace('http://purl.obolibrary.org/obo/HP_')
SYMP = Namespace('http://purl.obolibrary.org/obo/SYMP_')
WD = Namespace('http://www.wikidata.org/entity/')

class RdfLibDumperTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.prefix_map = PREFIX_MAP

    def test_rdflib_dumper(self):
        view = SchemaView(SCHEMA)
        container = yaml_loader.load(DATA, target_class=Container)
        self._check_objs(view, container)
        rdflib_dumper.dump(container, schemaview=view, to_file=OUT, prefix_map=self.prefix_map)
        g = Graph()
        g.parse(OUT, format='ttl')

        self.assertIn((P['001'], RDF.type, SDO.Person), g)
        self.assertIn((P['001'], SDO.name, Literal("fred bloggs")), g)
        self.assertIn((P['001'], SDO.email, Literal("fred.bloggs@example.com")), g)
        self.assertIn((P['001'], INFO.age_in_years, Literal(33)), g)
        self.assertIn((P['001'], SDO.gender, GSSO['000371']), g)
        self.assertIn((P['001'], INFO.depicted_by, Literal('https://example.org/pictures/fred.jpg', datatype=XSD.anyURI)), g)
        self.assertNotIn((P['001'], INFO.depicted_by, Literal('https://example.org/pictures/fred.jpg', datatype=XSD.string)), g)
        #for (s,p,o) in g.triples((None, None, None)):
        #    print(f'{s} {p} {o}')
        self.assertIn((CODE['D0001'], RDF.type, INFO.DiagnosisConcept), g)
        self.assertIn((CODE['D0001'], RDF.type, INFO.DiagnosisConcept), g)
        self.assertIn((CODE['D0001'], SKOS.exactMatch, HP['0002315']), g)
        self.assertIn((CODE['D0001'], SKOS.exactMatch, WD.Q86), g)
        self.assertIn((CODE['D0001'], SKOS.exactMatch, SYMP['0000504']), g)
        self.assertNotIn((CODE['D0001'], SKOS.exactMatch, Literal(HP['0002315'])), g)
        [container] = g.subjects(RDF.type, INFO.Container)
        self.assertIn((container, INFO.organizations, ROR['1']), g)
        self.assertIn((container, INFO.organizations, ROR['2']), g)
        self.assertIn((container, INFO.persons, P['001']), g)
        self.assertIn((container, INFO.persons, P['002']), g)
        container: Container = rdflib_loader.load(OUT, target_class=Container, schemaview=view, prefix_map=self.prefix_map)
        self._check_objs(view, container)
        #print(yaml_dumper.dumps(container))
        #person = next(p for p in container.persons if p.id == 'P:002')
        #mh = person.has_medical_history[0]

    def test_enums(self):
        view = SchemaView(SCHEMA)
        org1type1 = OrganizationType('non profit')  ## no meaning declared
        org1type2 = OrganizationType('charity')     ## meaning URI is declared
        assert not org1type1.meaning
        assert org1type2.meaning
        org1 = Organization('ROR:1', categories=[org1type1, org1type2])
        print(org1.categories)
        g = rdflib_dumper.as_rdf_graph(org1, schemaview=view, prefix_map=self.prefix_map)
        print(g)
        cats = list(g.objects(ROR['1'], INFO['categories']))
        print(cats)
        self.assertCountEqual([Literal('non profit'), URIRef('https://example.org/bizcodes/001')], cats)
        orgs = rdflib_loader.from_rdf_graph(g, target_class=Organization, schemaview=view)
        assert len(orgs) == 1
        [org1x] = orgs
        catsx = org1x.categories
        print(catsx)
        self.assertCountEqual([org1type1, org1type2], catsx)

    def test_undeclared_prefix_raises_error(self):
        view = SchemaView(SCHEMA)
        org1 = Organization('foo')  # not a CURIE or URI
        with self.assertRaises(Exception) as context:
            rdflib_dumper.as_rdf_graph(org1, schemaview=view)
        org1 = Organization('http://example.org/foo/o1')
        rdflib_dumper.as_rdf_graph(org1, schemaview=view)

    def test_base_prefix(self):
        view = SchemaView(SCHEMA)
        view.schema.prefixes["_base"] = Prefix("_base", "http://example.org/")
        org1 = Organization('foo')  # not a CURIE or URI
        g = rdflib_dumper.as_rdf_graph(org1, schemaview=view)
        assert (URIRef('http://example.org/foo'), RDF.type, SDO.Organization) in g

    def test_rdflib_loader(self):
        """
        tests loading from an RDF graph
        """
        view = SchemaView(SCHEMA)
        container: Container = rdflib_loader.load(DATA_TTL, target_class=Container, schemaview=view, prefix_map=self.prefix_map)
        self._check_objs(view, container)
        yaml_dumper.dump(container, to_file=DATA_ROUNDTRIP)

    def test_unmapped_predicates(self):
        """
        By default, the presence of predicates in rdf that have no mapping to slots
        should raise a MappingError
        """
        view = SchemaView(SCHEMA)
        # default behavior is to raise error on unmapped predicates
        with self.assertRaises(MappingError) as context:
            rdflib_loader.loads(unmapped_predicates_test_ttl, target_class=Person,
                                schemaview=view, prefix_map=self.prefix_map)
        # called can explicitly allow unmapped predicates to be dropped
        person: Person = rdflib_loader.loads(unmapped_predicates_test_ttl, target_class=Person,
                                                   schemaview=view, prefix_map=self.prefix_map,
                                                   ignore_unmapped_predicates=True)
        self.assertEqual(person.id, 'P:001')
        self.assertEqual(person.age_in_years, 33)
        self.assertEqual(str(person.gender), "cisgender man")
        yaml_dumper.dump(person, to_file=UNMAPPED_ROUNDTRIP)


    def test_any_of_enum(self):
        """
        Tests https://github.com/linkml/linkml/issues/1023
        """
        view = SchemaView(SCHEMA)
        # default behavior is to raise error on unmapped predicates
        person = rdflib_loader.loads(enum_union_type_test_ttl, target_class=Person,
                                schemaview=view, prefix_map=self.prefix_map)
        self.assertEqual(person.id, 'P:001')
        self.assertEqual(person.age_in_years, 33)
        yaml_dumper.dump(person, to_file=UNMAPPED_ROUNDTRIP)
        cases = [
            ("P:002", "COWORKER_OF"),
            ("P:003", "BEST_FRIEND_OF"),
        ]
        tups = []
        for r in person.has_interpersonal_relationships:
            tups.append((r.related_to, r.type))
        self.assertCountEqual(cases, tups)

    def test_unmapped_type(self):
        """
        If a type cannot be mapped then no objects will be returned by load/from_rdf_graph
        """
        view = SchemaView(SCHEMA)
        # default behavior is to raise error on unmapped predicates
        with self.assertRaises(DataNotFoundError) as context:
            rdflib_loader.loads(unmapped_type_test_ttl, target_class=Person,
                                schemaview=view, prefix_map=self.prefix_map)
        graph = Graph()
        graph.parse(data=unmapped_type_test_ttl, format='ttl')
        objs = rdflib_loader.from_rdf_graph(graph, target_class=Person,
                                     schemaview=view, prefix_map=self.prefix_map)
        self.assertEqual(len(objs), 0)

    def test_blank_node(self):
        """
        blank nodes should be retrievable
        """
        view = SchemaView(SCHEMA)
        address: Address = rdflib_loader.loads(blank_node_test_ttl, target_class=Address,
                                             schemaview=view, prefix_map=self.prefix_map,
                                             ignore_unmapped_predicates=True)
        self.assertEqual(address.city, 'foo city')
        ttl = rdflib_dumper.dumps(address, schemaview=view)
        print(ttl)
        g = Graph()
        g.parse(data=ttl, format='ttl')
        INFO = Namespace('https://w3id.org/linkml/examples/personinfo/')
        SDO = Namespace('http://schema.org/')
        [bn] = g.subjects(RDF.type, SDO.PostalAddress)
        self.assertIn((bn, RDF.type, SDO.PostalAddress), g)
        self.assertIn((bn, INFO.city, Literal("foo city")), g)
        self.assertIn((bn, INFO.street, Literal("1 foo street")), g)

    def _check_objs(self, view: SchemaView, container: Container):
        persons = container.persons
        orgs = container.organizations.values()
        [p1] = [p for p in persons if p.id == 'P:001']
        [p2] = [p for p in persons if p.id == 'P:002']
        [o1] = [o for o in orgs if o.id == 'ROR:1']
        [o2] = [o for o in orgs if o.id == 'ROR:2']
        o1cats = [c.code.text for c in o1.categories]
        o2cats = [c.code.text for c in o2.categories]
        self.assertEqual(p1.name, 'fred bloggs')
        self.assertEqual(p2.name, 'joe schmö')
        self.assertEqual(p1.age_in_years, 33)
        self.assertEqual(p1.gender.code.text, 'cisgender man')
        self.assertEqual(p2.gender.code.text, 'transgender man')
        self.assertCountEqual(o1cats, ['non profit', 'charity'])
        self.assertCountEqual(o2cats, ['shell company'])
        p2: Person
        emp = p2.has_employment_history[0]
        self.assertEqual(emp.started_at_time, '2019-01-01')
        self.assertEqual(emp.is_current, True)
        self.assertEqual(emp.employed_at, o1.id)
        frel = p2.has_familial_relationships[0]
        self.assertEqual(frel.related_to, p1.id)
        # TODO: check PV vs PVText
        self.assertEqual(str(frel.type), 'SIBLING_OF')
        med = p2.has_medical_history[0]
        self.assertEqual(med.in_location, 'GEO:1234')
        self.assertEqual(med.diagnosis.id, 'CODE:D0001')
        self.assertEqual(med.diagnosis.name, 'headache')
        self.assertEqual(med.diagnosis.code_system, 'CODE:D')

    def test_edge_cases(self):
        """
        Tests various edge cases:

         - unprocessed triples (triples that cannot be reached via root objects)
         - mismatch between expected range categories (Type vs Class) and value (Literal vs Node)
         - complex range expressions (e.g. modeling a range as being EITHER string OR object
        """
        # schema with following characterics:
        #  - reified triples
        #  - object has a complex union range (experimental new feature)
        view = SchemaView(os.path.join(INPUT_DIR, 'complex_range_example.yaml'))
        graph = Graph()
        taxon_prefix_map = {
            'NCBITaxon': 'http://purl.obolibrary.org/obo/NCBITaxon_',
            'RO': 'http://purl.obolibrary.org/obo/RO_',
        }
        # this graph has the following characteristics
        #  - blank nodes to represent statements
        #  - some triples not reachable from roots
        #  - implicit schema with complex ranges (rdf:object has range of either node or literal)
        graph.parse(os.path.join(INPUT_DIR, 'bacteria-taxon-class.ttl'), format='ttl')
        objs = rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                            schemaview=view,
                                            cast_literals=False,    ## strict
                                            allow_unprocessed_triples=True,  ## known issue
                                            prefix_map=taxon_prefix_map)
        [obj] = objs
        for x in obj.statements:
            assert x.subject is None
            assert x.predicate is not None
            assert x.object is not None
            logger.info(f'  x={x}')
        # ranges that are objects are contracted
        assert Triple(subject=None, predicate='rdfs:subClassOf', object='owl:Thing') in obj.statements
        assert Triple(subject=None, predicate='rdfs:subClassOf', object='NCBITaxon:1') in obj.statements
        # string ranges
        assert Triple(subject=None, predicate='rdfs:label', object='Bacteria') in obj.statements
        with self.assertRaises(ValueError) as context:
            rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                         schemaview=view,
                                         cast_literals=False,
                                         allow_unprocessed_triples=False,
                                         prefix_map=taxon_prefix_map)
            logger.error(f'Passed unexpectedly: there are known to be unreachable triples')
        # removing complex range, object has a range of string
        view.schema.slots['object'].exactly_one_of = []
        view.set_modified()
        rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                     schemaview=view,
                                     cast_literals=True,   ## required to pass
                                     allow_unprocessed_triples=True,
                                     prefix_map=taxon_prefix_map)
        with self.assertRaises(ValueError) as context:
            rdflib_loader.from_rdf_graph(graph, target_class=NodeObject,
                                         schemaview=view,
                                         cast_literals=False,
                                         allow_unprocessed_triples=True,
                                         prefix_map=taxon_prefix_map)
            logger.error(f'Passed unexpectedly: rdf:object is known to have a mix of literals and nodes')

    def test_phenopackets(self):
        view = SchemaView(str(Path(INPUT_DIR) / "phenopackets"/ "phenopackets.yaml"))
        test_label = 'test label'
        with self.assertRaises(ValueError) as e:
            c = OntologyClass(id='NO_SUCH_PREFIX:1', label=test_label)
            rdflib_dumper.dumps(c, view)
        cases = [
            ("HP:1", "http://purl.obolibrary.org/obo/HP_1", None),
            ("FOO:1", "http://example.org/FOO_1", {'FOO': 'http://example.org/FOO_',
                                                   "@base": "http://example.org/base/"}),
        ]
        for id, expected_uri, prefix_map in cases:

            c = OntologyClass(id=id, label=test_label)
            ttl = rdflib_dumper.dumps(c, view, prefix_map=prefix_map)
            g = Graph()
            g.parse(data=ttl, format='ttl')
            self.assertEqual(len(g), 2)
            self.assertIn(Literal(test_label), list(g.objects(URIRef(expected_uri))),
                          f'Expected label {test_label} for {expected_uri} in {ttl}')
            pf = PhenotypicFeature(type=c)
            pkt = Phenopacket(id='id with spaces',
                              metaData=MetaData(resources=[Resource(id='id with spaces')]),
                              phenotypicFeatures=[pf])
            ttl = rdflib_dumper.dumps(pkt, view, prefix_map=self.prefix_map)
            g = Graph()
            g.parse(data=ttl, format='ttl')
            self.assertIn(Literal(test_label), list(g.objects(URIRef(expected_uri))),
                          f'Expected label {test_label} for {expected_uri} in {ttl}')
            if prefix_map and "@base" in prefix_map:
                resource_uri = URIRef(prefix_map["@base"] + "id%20with%20spaces")
                self.assertEqual(1, len(list(g.objects(resource_uri))))




class RDFLibConverterDumperTestCase(RdfLibDumperTestCase):
    """A test case that uses a :class:`curies.Converter` for testing loading and dumping with RDFLib."""

    def setUp(self) -> None:
        """Set up the test case using a :class:`curies.Converter` instead of a simple prefix map."""
        self.prefix_map = Converter.from_prefix_map(PREFIX_MAP)



if __name__ == '__main__':
    unittest.main()
