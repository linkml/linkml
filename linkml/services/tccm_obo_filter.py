import os
import pickle
from typing import Iterator, Optional, Union, Callable

from rdflib import Graph, URIRef, Namespace, RDFS, BNode, Literal, XSD, SKOS

from linkml_model.meta import RDF, OWL

# Namespaces pulled from the TCCM module
#
# xmlns="http://purl.obolibrary.org/obo/hp.owl#"
#      xml:base="http://purl.obolibrary.org/obo/hp.owl"
#      xmlns:dc="http://purl.org/dc/elements/1.1/"
#      xmlns:go="http://purl.obolibrary.org/obo/go#"
#      xmlns:hp="http://purl.obolibrary.org/obo/hp#"
#      xmlns:pr="http://purl.obolibrary.org/obo/pr#"
#      xmlns:obo="http://purl.obolibrary.org/obo/"
#      xmlns:owl="http://www.w3.org/2002/07/owl#"
#      xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
#      xmlns:xml="http://www.w3.org/XML/1998/namespace"
#      xmlns:xsd="http://www.w3.org/2001/XMLSchema#"
#      xmlns:cito="http://purl.org/spar/cito/"
#      xmlns:core="http://purl.obolibrary.org/obo/uberon/core#"
#      xmlns:foaf="http://xmlns.com/foaf/0.1/"
#      xmlns:pato="http://purl.obolibrary.org/obo/pato#"
#      xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
#      xmlns:swrl="http://www.w3.org/2003/11/swrl#"
#      xmlns:chebi="http://purl.obolibrary.org/obo/chebi/"
#      xmlns:core2="http://purl.obolibrary.org/obo/core#"
#      xmlns:swrla="http://swrl.stanford.edu/ontologies/3.3/swrla.owl#"
#      xmlns:swrlb="http://www.w3.org/2003/11/swrlb#"
#      xmlns:terms="http://purl.org/dc/terms/"
#      xmlns:chebi1="http://purl.obolibrary.org/obo/chebi#"
#      xmlns:chebi3="http://purl.obolibrary.org/obo/chebi#2"
#      xmlns:chebi4="http://purl.obolibrary.org/obo/chebi#3"
#      xmlns:chebi5="http://purl.obolibrary.org/obo/chebi#1"
#      xmlns:hsapdv="http://purl.obolibrary.org/obo/hsapdv#"
#      xmlns:ubprop="http://purl.obolibrary.org/obo/ubprop#"
#      xmlns:subsets="http://purl.obolibrary.org/obo/ro/subsets#"
#      xmlns:oboInOwl="http://www.geneontology.org/formats/oboInOwl#">

# Sample entry in the current HPO (Note that this example IS not an HPO concept
# <!-- http://purl.obolibrary.org/obo/UBERON_0006756 -->
#
#     <owl:Class rdf:about="http://purl.obolibrary.org/obo/UBERON_0006756">
#         <rdfs:subClassOf rdf:resource="http://purl.obolibrary.org/obo/UBERON_0002050"/>
#         <rdfs:subClassOf>
#             <owl:Restriction>
#                 <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/BFO_0000050"/>
#                 <owl:someValuesFrom rdf:resource="http://purl.obolibrary.org/obo/UBERON_0006260"/>
#             </owl:Restriction>
#         </rdfs:subClassOf>
#         <rdfs:subClassOf>
#             <owl:Restriction>
#                 <owl:onProperty rdf:resource="http://purl.obolibrary.org/obo/RO_0002202"/>
#                 <owl:someValuesFrom rdf:resource="http://purl.obolibrary.org/obo/UBERON_0004362"/>
#             </owl:Restriction>
#         </rdfs:subClassOf>
#         <obo:IAO_0000115>During the third week of embryological development there appears, immediately behind the ventral ends of the two halves of the mandibular arch, a rounded swelling named the tuberculum impar, which was described by His as undergoing enlargement to form the buccal part of the tongue. More recent researches, however, show that this part of the tongue is mainly, if not entirely, developed from a pair of lateral swellings which rise from the inner surface of the mandibular arch and meet in the middle line. The site of their meeting remains post-embryonically as the median sulcus of the tongue. The tuberculum impar is said to form the central part of the tongue immediately in front of the foramen cecum, but Hammar insists that it is purely a transitory structure and forms no part of the adult tongue[WP, Gray&apos;s].</obo:IAO_0000115>
#         <obo:UBPROP_0000003>Most adult amphibians have a tongue, as do all known reptiles, birds and mammals. Thus it is likely that the tongue appeared with the establishment of tetrapods and this structure seems to be related, to some extant, to the terrestrial lifestyle.[well established][VHOG]</obo:UBPROP_0000003>
#         <oboInOwl:hasDbXref rdf:resource="http://en.wikipedia.org/wiki/Tuberculum_impar"/>
#         <oboInOwl:hasDbXref rdf:resource="http://www.snomedbrowser.com/Codes/Details/308821003"/>
#         <oboInOwl:hasDbXref>EHDAA2:0001081</oboInOwl:hasDbXref>
#         <oboInOwl:hasDbXref>EMAPA:17187</oboInOwl:hasDbXref>
#         <oboInOwl:hasDbXref>FMA:312476</oboInOwl:hasDbXref>
#         <oboInOwl:hasDbXref>VHOG:0000730</oboInOwl:hasDbXref>
#         <oboInOwl:hasExactSynonym>median lingual swelling</oboInOwl:hasExactSynonym>
#         <oboInOwl:hasExactSynonym>median tongue bud</oboInOwl:hasExactSynonym>
#         <oboInOwl:hasExactSynonym>tuberculum impar</oboInOwl:hasExactSynonym>
#         <oboInOwl:hasExactSynonym>tuberculum linguale mediale</oboInOwl:hasExactSynonym>
#         <oboInOwl:hasOBONamespace>uberon</oboInOwl:hasOBONamespace>
#         <oboInOwl:id>UBERON:0006756</oboInOwl:id>
#         <rdfs:comment>The thyroid initially develops caudal to the tuberculum impar . This embryonic swelling arises from the first pharyngeal arch and occurs midline on the floor of the developing pharynx, eventually helping form the tongue as the 2 lateral lingual swellings overgrow it. [http://emedicine.medscape.com/article/845125-overview]</rdfs:comment>
#         <rdfs:label>median lingual swelling</rdfs:label>
#         <foaf:depicted_by rdf:datatype="http://www.w3.org/2001/XMLSchema#anyURI">http://upload.wikimedia.org/wikipedia/commons/5/5c/Gray979.png</foaf:depicted_by>
#     </owl:Class>


OBO = Namespace("http://purl.obolibrary.org/obo/")
OBOinOWL = Namespace("http://www.geneontology.org/formats/oboInOwl#")
IAO = Namespace(OBO.IAO_)
HPO = Namespace(OBO.HP_)


def tccm_filter(g: Graph, ns: Namespace, target_file: str, target_format: Optional[str] = "turtle",
                id_xlator: Optional[Callable[[str], str]] = None) -> None:
    target_graph = Graph()

    def fix_literal(l: Union[BNode, URIRef, Literal]) -> Union[BNode, URIRef, Literal]:
        """ Remove those annoying string datatypes we get from XML serialization """
        if isinstance(l, Literal):
            if l.datatype == XSD.string:
                return Literal(str(l))
        return l

    def xfer_triples(tg: Iterator, new_p: Optional[URIRef] = None) -> int:
        nxferred = 0
        if new_p:
            for t in tg:
                target_graph.add((t[0], new_p, fix_literal(t[2])))
                nxferred += 1
                if isinstance(t[2], BNode):
                    nxferred += xfer_triples(g.triples((t[2], None, None)), new_p)
        else:
            for t in tg:
                target_graph.add((t[0], t[1], fix_literal(t[2])))
                nxferred += 1
                if isinstance(t[2], BNode):
                    nxferred += xfer_triples(g.triples((t[2], None, None)), new_p)
        return nxferred

    def xfer_subject_predicate(s: URIRef, p:URIRef, new_p: Optional[URIRef] = None) -> int:
        return xfer_triples(g.triples((s, p, None)), new_p)

    def xfer_codes(s: URIRef) -> None:
        for o in g.objects(s, OBOinOWL.id):
            target_graph.add((s, SKOS.notation, id_xlator(str(o)) if id_xlator else fix_literal(o)))

    def xfer_subject(s: Union[URIRef, BNode]) -> None:
        if not isinstance(s, BNode):
            if str(s).startswith(nsbase):
                xfer_subject_predicate(s, RDF.type)         # rdf:type
                xfer_codes(s)                               # skos:notation
                xfer_subject_predicate(s, RDFS.label, SKOS.prefLabel)       # Associated text
                if not xfer_subject_predicate(s, IAO['0000115'], SKOS.definition):
                    xfer_subject_predicate(s, RDFS.comment, SKOS.definition)  # Descriptions

    # Copy the minimal information needed to support a simple TCCM server from an obo style graph
    nsbase = str(ns)
    ontologies = list(g.subjects(RDF.type, OWL.Ontology))
    if len(ontologies) != 1:
        raise ValueError("Ontology not found" if len(ontologies) == 0 else "Multiple ontologies")
    ontology = ontologies[0]

    # Transfer all the ontology metadata to the target
    xfer_triples(g.triples((ontology, None, None)))

    # Transfer all classes
    for c in g.subjects(RDF.type, OWL.Class):
        xfer_subject(c)

    # Transfer all object and data properties
    for p in g.subjects(RDF.type, OWL.Dataproperty):
        xfer_subject(p)

    for p in g.subjects(RDF.type, OWL.Objectproperty):
        xfer_subject(p)

    for ns in g.namespaces():
        target_graph.bind(*ns)
    target_graph.bind("skos", SKOS)

    target_graph.serialize(target_file, format=target_format)


def hpo_id_xlator(code: Literal) -> Literal:
    return Literal(str(code).replace('HP:', 'HP_'))

if __name__ == '__main__':
    from tests.environment import env

    # g = Graph()
    # g.load(os.path.join(env.cwd, 'data', 'hp.ttl'), format="turtle")
    outf = os.path.join(env.cwd, 'data', 'hp.dill')
    # with open(outf, 'wb') as f:
    #     pickle.dump(g, f)
    with open(outf, 'rb') as f:
        g = pickle.load(f)
    tccm_filter(g, HPO, os.path.join(env.cwd, 'data', 'hp_f.ttl'), id_xlator=hpo_id_xlator)
