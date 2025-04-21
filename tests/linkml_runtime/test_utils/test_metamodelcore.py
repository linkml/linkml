import datetime
import unittest
from dataclasses import dataclass

from jsonasobj2 import as_json
from rdflib import Literal, XSD, Graph, RDF, Namespace

from linkml_runtime.utils.metamodelcore import NCName, Bool, URIorCURIE, URI, XSDDate, XSDDateTime, XSDTime, Curie, \
    NodeIdentifier
from linkml_runtime.utils.namespaces import Namespaces
from linkml_runtime.utils.strictness import lax, strict
from linkml_runtime.utils.yamlutils import YAMLRoot, as_rdf


class MetamodelCoreTest(unittest.TestCase):
    def tearDown(self) -> None:
        strict()

    def test_ncname(self):
        self.assertEqual('A123', NCName('A123'))
        x = NCName('A1.B_C-')
        self.assertEqual('A1.B_C-', x)
        self.assertIsInstance(x, str)
        self.assertIsInstance(x, NCName)
        self.assertEqual(x, NCName(x))
        x = str(x)
        self.assertIsInstance(x, str)
        self.assertFalse(isinstance(x, NCName))
        with self.assertRaises(ValueError):
            NCName('1')
        with self.assertRaises(ValueError):
            NCName('A12!')

    def test_uriorcuries(self):
        """ Test the URI and URIorCURIE types """
        str1 = "https://google.com/test#file?abc=1&def=4"
        self.assertEqual(str1, URIorCURIE(str1))
        str2 = "abc:123"
        self.assertEqual(str2, URIorCURIE(str2))
        str3 = ":123"
        self.assertEqual(str3, URIorCURIE(str3))
        with self.assertRaises(ValueError):
            URIorCURIE("abc:[def]")
        with self.assertRaises(ValueError):
            URIorCURIE("1abc:def")
        with self.assertRaises(ValueError):
            URIorCURIE("1:def")
        with self.assertRaises(ValueError):
            URIorCURIE(" ")
        with self.assertRaises(ValueError):
            URIorCURIE("[")
        assert URIorCURIE.is_valid("NCIT:C176962")
        lax()
        URIorCURIE("1abc:def")
        URIorCURIE("1:def")
        self.assertFalse(URIorCURIE.is_valid(123))
        URIorCURIE.is_curie("abc:123")
        self.assertFalse(URIorCURIE.is_curie("http://example.org/path"))

    def test_curie(self):
        """ Test the CURIE type """
        self.assertEqual("rdf:type", Curie("rdf:type"))
        with self.assertRaises(ValueError):
            Curie("type")
        self.assertFalse(Curie.is_valid("type"))
        self.assertEqual(":type", Curie(":type"))
        self.assertTrue(Curie.is_valid(':type'))
        self.assertTrue(Curie.is_valid('WIKIDATA_PROPERTY:P854'))
        self.assertTrue(Curie.is_valid('WIKIDATA.PROPERTY:P854'))
        self.assertTrue(Curie.is_valid('CL:0000001'))
        with self.assertRaises(ValueError):
            Curie("1df:type")
        self.assertFalse(Curie.is_valid('1df:type'))
        self.assertTrue(Curie.is_valid('rdf:17'))
        nsm = Namespaces(Graph())
        self.assertEqual(RDF.type, Curie("rdf:type").as_uri(nsm))
        self.assertIsNone(Curie("ex:foo").as_uri(nsm))
        self.assertIsNone(Curie(":bar").as_uri(nsm))
        nsm._default = "http://example.org/test#"
        self.assertEqual(nsm._default['bear'], Curie(":bear").as_uri(nsm))


    def test_uri(self):
        """ Test the URI data type """
        str1 = "https://google.com/test#file?abc=1&def=4"
        self.assertEqual(str1, URI(str1))
        self.assertEqual("http://foo.org/bargles", URI("http://foo.org/bargles"))
        with self.assertRaises(ValueError):
            URI(":")
        with self.assertRaises(ValueError):
            URI(":123")
        # imports range is uriorcurie, so we allow file paths
        #URI("1")
        self.assertTrue(URI.is_valid("foo.bar"))
        self.assertTrue(URI.is_valid("../a/b"))
        self.assertTrue(URI.is_valid("abc:123"))
        #with self.assertRaises(ValueError):
        #    URI("x1")
        # an empty URI is a valid same-document URI reference
        self.assertTrue(URI.is_valid(""))
        x = URI("rdf:type")
        self.assertTrue(URI.is_valid(x))
        self.assertTrue(URI.is_valid("urn:abc:123"))
        self.assertTrue(URI.is_valid("https://john.doe@www.example.com:123/forum/questions/?tag=networking&order=newest#top"))
        self.assertTrue(URI.is_valid("ldap://[2001:db8::7]/c=GB?objectClass?one"))
        self.assertTrue(URI.is_valid("ldap://[2001:db8::7]/c=GB?objectClass?one"))
        self.assertTrue(URI.is_valid("mailto:John.Doe@example.com"))
        self.assertTrue(URI.is_valid("news:comp.infosystems.www.servers.unix"))
        self.assertTrue(URI.is_valid("tel:+1-816-555-1212"))
        self.assertTrue(URI.is_valid("telnet://192.0.2.16:80/"))
        self.assertTrue(URI.is_valid("urn:oasis:names:specification:docbook:dtd:xml:4.1.2"))
        self.assertTrue(URI.is_valid("file:///home/user/"))

    def test_bool(self):
        self.assertTrue(Bool(True))
        self.assertTrue(Bool("True"))
        self.assertTrue(Bool("true"))
        self.assertTrue(Bool(1))
        self.assertTrue(Bool("1"))
        self.assertTrue(Bool(Bool(True)))
        self.assertFalse(Bool(False))
        self.assertFalse(Bool("False"))
        self.assertFalse(Bool("false"))
        self.assertFalse(Bool(0))
        self.assertFalse(Bool("0"))
        self.assertFalse(Bool(Bool(0)))
        # Strict mode
        with self.assertRaises(ValueError):
            x = Bool(17)
        with self.assertRaises(ValueError):
            x = Bool("a")
        lax()
        x = Bool(17)
        self.assertFalse(Bool.is_valid(17))
        x = Bool("a")
        self.assertFalse(Bool.is_valid("a"))
        self.assertTrue(Bool.is_valid(True))
        self.assertTrue(Bool.is_valid(Bool(True)))

    def test_time(self):
        v = datetime.time(13, 17, 43, 279000)
        self.assertEqual('13:17:43.279000', XSDTime(v))                              # A date can be a datetime
        self.assertEqual('13:17:43.279000', XSDTime(Literal(v, datatype=XSD.time)))  # An RDFLIB Literal
        self.assertEqual('13:17:43.279000', v.isoformat())                           # A string
        self.assertEqual('13:17:43.279000', XSDTime(XSDTime(v)))                     # An existing date
        strict()
        with self.assertRaises(ValueError):
            XSDTime('Jan 12, 2019')
        with self.assertRaises(ValueError):
            XSDTime(datetime.datetime.now())
        lax()
        self.assertEqual('Jan 12, 2019', XSDTime('Jan 12, 2019'))
        XSDDate(datetime.datetime.now())
        self.assertFalse(XSDTime.is_valid('Jan 12, 2019'))
        self.assertFalse(XSDTime.is_valid(datetime.datetime.now()))
        self.assertFalse(XSDTime.is_valid("2019-07-06T17:22:39Z"))
        self.assertTrue(XSDTime.is_valid(v))

    def test_date(self):
        v = datetime.date(2019, 7, 6)
        self.assertEqual('2019-07-06', XSDDate(v))                              # A date can be a datetime
        self.assertEqual('2019-07-06', XSDDate(Literal(v, datatype=XSD.date)))  # An RDFLIB Literal
        self.assertEqual('2019-07-06', v.isoformat())                           # A string
        self.assertEqual('2019-07-06', XSDDate(XSDDate(v)))                     # An existing date
        strict()
        with self.assertRaises(ValueError):
            XSDDate('20190706')
        with self.assertRaises(ValueError):
            XSDDate('Jan 12, 2019')
        with self.assertRaises(ValueError):
            XSDDate(datetime.datetime.now())
        with self.assertRaises(ValueError):
            XSDDate("2019-07-06T17:22:39Z")

        lax()
        bv = XSDDate('Jan 12, 2019')
        self.assertEqual('Jan 12, 2019', bv)
        self.assertFalse(XSDDate.is_valid(bv))
        XSDDate(datetime.datetime.now())
        self.assertFalse(XSDDate.is_valid('Jan 12, 2019'))
        self.assertFalse(XSDDate.is_valid(datetime.datetime.now()))
        self.assertTrue(XSDDate.is_valid(XSDDate(datetime.datetime.now().date())))
        self.assertTrue(XSDDate.is_valid(v))

    def test_datetime(self):
        v = datetime.datetime(2019, 7, 6, 17, 22, 39, 7300)
        self.assertEqual('2019-07-06T17:22:39.007300', XSDDateTime(v))
        self.assertEqual('2019-07-06T17:22:39.007300', XSDDateTime(Literal(v, datatype=XSD.dateTime)))
        self.assertEqual('2019-07-06T17:22:39.007300', XSDDateTime(Literal(v).value))
        self.assertEqual('2019-07-06T17:22:39.007300', v.isoformat())
        self.assertEqual('2019-07-06T17:22:39.007300', XSDDateTime(XSDDateTime(v)))
        vstr = str(Literal(v).value)
        self.assertEqual('2019-07-06 17:22:39.007300', vstr)       # Note that this has no 'T'
        self.assertEqual('2019-07-06T17:22:39.007300', XSDDateTime(vstr))
        self.assertEqual('2019-07-06T17:22:39+00:00', XSDDateTime("2019-07-06T17:22:39Z"))
        self.assertEqual('2019-07-06T00:00:00', XSDDateTime("2019-07-06")) # Date as datetime
        with self.assertRaises(ValueError):
            XSDDateTime('Jan 12, 2019')

        lax()
        self.assertEqual('penguins', XSDDateTime('penguins'))
        XSDDateTime(datetime.datetime.now())
        self.assertFalse(XSDDateTime.is_valid('Jan 12, 2019'))
        self.assertTrue(XSDDateTime.is_valid(datetime.datetime.now()))
        self.assertTrue(XSDDateTime.is_valid(XSDDate(datetime.datetime.now().date())))
        self.assertTrue(XSDDateTime.is_valid(v))

    @unittest.skipIf(True, "Finish implementing this")
    def test_nodeidentifier(self):
        context = """{
            "@context": {
                "type": "@type",
                "OIO": "http://www.geneontology.org/formats/oboInOwl#",
                "dcterms": "http://purl.org/dc/terms/",
                "metatype": "https://w3id.org/linkml/type/",
                "owl": "http://www.w3.org/2002/07/owl#",
                "pav": "http://purl.org/pav/",
                "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                "skos": "http://www.w3.org/2004/02/skos/core#",
                "xsd": "http://www.w3.org/2001/XMLSchema#",
                "s": {
                    "@id": "rdfs:subject"
                },
                "t": {
                    "@id": "rdfs:object"
                }
            }
        }"""
        EX = Namespace("http://example.org/tests/")
        class Root(NodeIdentifier):
            pass

        class Child1(Root):
            pass

        class Child2(Root):
            pass

        class Desc1(Child1):
            pass

        class Unassoc(NodeIdentifier):
            pass

        @dataclass
        class Pair(YAMLRoot):
            s: Child1 = None
            t: Child2 = None

            def __post_init__(self):
                if not isinstance(self.s, Child1):
                    self.s = Child1(self.s)
                if not isinstance(self.t, Child2):
                    self.t = Child2(self.t)
                    super().__post_init__()

        s = Desc1(EX.descendant1)
        t = Child2(EX.child2)
        y = Pair(s, t)
        self.assertEqual("""{
   "s": "http://example.org/tests/descendant1",
   "t": "http://example.org/tests/child2"
}""", as_json(y))
        self.assertEqual("""@prefix OIO: <http://www.geneontology.org/formats/oboInOwl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix metatype: <https://w3id.org/linkml/type/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix pav: <http://purl.org/pav/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

[] a <linkml/tests/Pair> ;
    rdfs:object "http://example.org/tests/child2" ;
    rdfs:subject "http://example.org/tests/descendant1" .

""", as_rdf(y, context).serialize(format="turtle"))
        with self.assertRaises(ValueError):
            y = Pair(s, s)




if __name__ == '__main__':
    unittest.main()
