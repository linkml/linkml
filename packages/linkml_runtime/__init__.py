from linkml_runtime.utils.curienamespace import CurieNamespace
from rdflib import RDF, RDFS, SKOS, XSD, OWL

LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TCCM = CurieNamespace('tccm', 'https://ontologies.r.us/tccm/')
OWL = CurieNamespace('owl', OWL)
RDF = CurieNamespace('rdf', RDF)
RDFS = CurieNamespace('rdfs', RDFS)
SKOS = CurieNamespace('skos', SKOS)
XSD = CurieNamespace('xsd', XSD)
