from linkml_runtime.utils.curienamespace import CurieNamespace
from rdflib import RDF, RDFS, SKOS, XSD, OWL
import rdflib_shim
shim = rdflib_shim.RDFLIB_SHIM

LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
TCCM = CurieNamespace('tccm', 'https://ontologies.r.us/tccm/')
OWL = CurieNamespace('owl', OWL)
RDF = CurieNamespace('rdf', RDF)
RDFS = CurieNamespace('rdfs', RDFS)
SKOS = CurieNamespace('skos', SKOS)
XSD = CurieNamespace('xsd', XSD)

class MappingError(ValueError):
    """
    An error when mapping elements of a LinkML model to runtime objects
    """
    pass

class DataNotFoundError(ValueError):
    """
    An error in which data cannot be found
    """
    pass