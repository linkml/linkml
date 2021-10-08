# Auto generated from biolink-model.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-10-08 17:02
# Schema: Biolink-Model
#
# id: https://w3id.org/biolink/biolink-model
# description: Entity and association taxonomy and datamodel for life-sciences data
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Date, Double, Float, Integer, String, Time, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, URIorCURIE, XSDDate, XSDTime

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
APO = CurieNamespace('APO', 'http://purl.obolibrary.org/obo/APO_')
AEOLUS = CurieNamespace('Aeolus', 'http://translator.ncats.nih.gov/Aeolus_')
BFO = CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_')
BIOGRID = CurieNamespace('BIOGRID', 'http://identifiers.org/biogrid/')
BIOSAMPLE = CurieNamespace('BIOSAMPLE', 'http://identifiers.org/biosample/')
BSPO = CurieNamespace('BSPO', 'http://purl.obolibrary.org/obo/BSPO_')
BTO = CurieNamespace('BTO', 'http://purl.obolibrary.org/obo/BTO_')
CAID = CurieNamespace('CAID', 'http://reg.clinicalgenome.org/redmine/projects/registry/genboree_registry/by_caid?caid=')
CAS = CurieNamespace('CAS', 'http://identifiers.org/cas/')
CATH = CurieNamespace('CATH', 'http://identifiers.org/cath/')
CATH_SUPERFAMILY = CurieNamespace('CATH_SUPERFAMILY', 'http://identifiers.org/cath.superfamily/')
CDD = CurieNamespace('CDD', 'http://identifiers.org/cdd/')
CHADO = CurieNamespace('CHADO', 'http://gmod.org/wiki/Chado/')
CHEBI = CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_')
CHEMBL_COMPOUND = CurieNamespace('CHEMBL_COMPOUND', 'http://identifiers.org/chembl.compound/')
CHEMBL_MECHANISM = CurieNamespace('CHEMBL_MECHANISM', 'https://www.ebi.ac.uk/chembl/mechanism/inspect/')
CHEMBL_TARGET = CurieNamespace('CHEMBL_TARGET', 'http://identifiers.org/chembl.target/')
CID = CurieNamespace('CID', 'http://pubchem.ncbi.nlm.nih.gov/compound/')
CIO = CurieNamespace('CIO', 'http://purl.obolibrary.org/obo/CIO_')
CL = CurieNamespace('CL', 'http://purl.obolibrary.org/obo/CL_')
CLINVAR = CurieNamespace('CLINVAR', 'http://identifiers.org/clinvar/')
CLO = CurieNamespace('CLO', 'http://purl.obolibrary.org/obo/CLO_')
COAR_RESOURCE = CurieNamespace('COAR_RESOURCE', 'http://purl.org/coar/resource_type/')
CPT = CurieNamespace('CPT', 'https://www.ama-assn.org/practice-management/cpt/')
CTD = CurieNamespace('CTD', 'http://translator.ncats.nih.gov/CTD_')
CHEMBANK = CurieNamespace('ChemBank', 'http://chembank.broadinstitute.org/chemistry/viewMolecule.htm?cbid=')
CLINVARVARIANT = CurieNamespace('ClinVarVariant', 'http://www.ncbi.nlm.nih.gov/clinvar/variation/')
DBSNP = CurieNamespace('DBSNP', 'http://identifiers.org/dbsnp/')
DDANAT = CurieNamespace('DDANAT', 'http://purl.obolibrary.org/obo/DDANAT_')
DGIDB = CurieNamespace('DGIdb', 'https://www.dgidb.org/interaction_types')
DOID = CurieNamespace('DOID', 'http://purl.obolibrary.org/obo/DOID_')
DRUGBANK = CurieNamespace('DRUGBANK', 'http://identifiers.org/drugbank/')
DRUGCENTRAL = CurieNamespace('DrugCentral', 'http://translator.ncats.nih.gov/DrugCentral_')
EC = CurieNamespace('EC', 'http://www.enzyme-database.org/query.php?ec=')
ECO = CurieNamespace('ECO', 'http://purl.obolibrary.org/obo/ECO_')
ECTO = CurieNamespace('ECTO', 'http://purl.obolibrary.org/obo/ECTO_')
EDAM_DATA = CurieNamespace('EDAM-DATA', 'http://edamontology.org/data_')
EDAM_FORMAT = CurieNamespace('EDAM-FORMAT', 'http://edamontology.org/format_')
EDAM_OPERATION = CurieNamespace('EDAM-OPERATION', 'http://edamontology.org/operation_')
EDAM_TOPIC = CurieNamespace('EDAM-TOPIC', 'http://edamontology.org/topic_')
EFO = CurieNamespace('EFO', 'http://www.ebi.ac.uk/efo/EFO_')
EGGNOG = CurieNamespace('EGGNOG', 'http://identifiers.org/eggnog/')
ENSEMBL = CurieNamespace('ENSEMBL', 'http://identifiers.org/ensembl/')
ENVO = CurieNamespace('ENVO', 'http://purl.obolibrary.org/obo/ENVO_')
EXO = CurieNamespace('ExO', 'http://purl.obolibrary.org/obo/ExO_')
FAO = CurieNamespace('FAO', 'http://purl.obolibrary.org/obo/FAO_')
FB = CurieNamespace('FB', 'http://identifiers.org/fb/')
FBCV = CurieNamespace('FBcv', 'http://purl.obolibrary.org/obo/FBcv_')
FMA = CurieNamespace('FMA', 'http://purl.obolibrary.org/obo/FMA_')
FOODON = CurieNamespace('FOODON', 'http://purl.obolibrary.org/obo/FOODON_')
GAMMA = CurieNamespace('GAMMA', 'http://translator.renci.org/GAMMA_')
GENEPIO = CurieNamespace('GENEPIO', 'http://purl.obolibrary.org/obo/GENEPIO_')
GENO = CurieNamespace('GENO', 'http://purl.obolibrary.org/obo/GENO_')
GO = CurieNamespace('GO', 'http://purl.obolibrary.org/obo/GO_')
GOLD_META = CurieNamespace('GOLD_META', 'http://identifiers.org/gold.meta/')
GOP = CurieNamespace('GOP', 'http://purl.obolibrary.org/obo/go#')
GOREL = CurieNamespace('GOREL', 'http://purl.obolibrary.org/obo/GOREL_')
GSID = CurieNamespace('GSID', 'https://scholar.google.com/citations?user=')
GTEX = CurieNamespace('GTEx', 'https://www.gtexportal.org/home/gene/')
GTOPDB = CurieNamespace('GTOPDB', 'https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId=')
HAMAP = CurieNamespace('HAMAP', 'http://identifiers.org/hamap/')
HANCESTRO = CurieNamespace('HANCESTRO', 'http://www.ebi.ac.uk/ancestro/ancestro_')
HCPCS = CurieNamespace('HCPCS', 'http://purl.bioontology.org/ontology/HCPCS/')
HGNC = CurieNamespace('HGNC', 'http://identifiers.org/hgnc/')
HGNC_FAMILY = CurieNamespace('HGNC_FAMILY', 'http://identifiers.org/hgnc.family/')
HMDB = CurieNamespace('HMDB', 'http://identifiers.org/hmdb/')
HP = CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_')
HSAPDV = CurieNamespace('HsapDv', 'http://purl.obolibrary.org/obo/HsapDv_')
IAO = CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_')
ICD0 = CurieNamespace('ICD0', 'http://translator.ncats.nih.gov/ICD0_')
ICD10 = CurieNamespace('ICD10', 'http://translator.ncats.nih.gov/ICD10_')
ICD9 = CurieNamespace('ICD9', 'http://translator.ncats.nih.gov/ICD9_')
IDO = CurieNamespace('IDO', 'http://purl.obolibrary.org/obo/IDO_')
INCHI = CurieNamespace('INCHI', 'http://identifiers.org/inchi/')
INCHIKEY = CurieNamespace('INCHIKEY', 'http://identifiers.org/inchikey/')
INO = CurieNamespace('INO', 'http://purl.obolibrary.org/obo/INO_')
INTACT = CurieNamespace('INTACT', 'http://identifiers.org/intact/')
IUPHAR_FAMILY = CurieNamespace('IUPHAR_FAMILY', 'http://identifiers.org/iuphar.family/')
KEGG = CurieNamespace('KEGG', 'http://identifiers.org/kegg/')
KEGG_BRITE = CurieNamespace('KEGG_BRITE', 'http://www.kegg.jp/entry/')
KEGG_COMPOUND = CurieNamespace('KEGG_COMPOUND', 'http://identifiers.org/kegg.compound/')
KEGG_DGROUP = CurieNamespace('KEGG_DGROUP', 'http://www.kegg.jp/entry/')
KEGG_DISEASE = CurieNamespace('KEGG_DISEASE', 'http://identifiers.org/kegg.disease/')
KEGG_DRUG = CurieNamespace('KEGG_DRUG', 'http://identifiers.org/kegg.drug/')
KEGG_ENVIRON = CurieNamespace('KEGG_ENVIRON', 'http://identifiers.org/kegg.environ/')
KEGG_ENZYME = CurieNamespace('KEGG_ENZYME', 'http://www.kegg.jp/entry/')
KEGG_GENE = CurieNamespace('KEGG_GENE', 'http://www.kegg.jp/entry/')
KEGG_GLYCAN = CurieNamespace('KEGG_GLYCAN', 'http://identifiers.org/kegg.glycan/')
KEGG_MODULE = CurieNamespace('KEGG_MODULE', 'http://identifiers.org/kegg.module/')
KEGG_ORTHOLOGY = CurieNamespace('KEGG_ORTHOLOGY', 'http://identifiers.org/kegg.orthology/')
KEGG_RCLASS = CurieNamespace('KEGG_RCLASS', 'http://www.kegg.jp/entry/')
KEGG_REACTION = CurieNamespace('KEGG_REACTION', 'http://identifiers.org/kegg.reaction/')
LOINC = CurieNamespace('LOINC', 'http://loinc.org/rdf/')
MEDDRA = CurieNamespace('MEDDRA', 'http://identifiers.org/meddra/')
MESH = CurieNamespace('MESH', 'http://identifiers.org/mesh/')
MGI = CurieNamespace('MGI', 'http://identifiers.org/mgi/')
MI = CurieNamespace('MI', 'http://purl.obolibrary.org/obo/MI_')
MIR = CurieNamespace('MIR', 'http://identifiers.org/mir/')
MONDO = CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_')
MP = CurieNamespace('MP', 'http://purl.obolibrary.org/obo/MP_')
MPATH = CurieNamespace('MPATH', 'http://purl.obolibrary.org/obo/MPATH_')
MSIGDB = CurieNamespace('MSigDB', 'https://www.gsea-msigdb.org/gsea/msigdb/')
METACYC = CurieNamespace('MetaCyc', 'http://translator.ncats.nih.gov/MetaCyc_')
NBO = CurieNamespace('NBO', 'http://purl.obolibrary.org/obo/NBO_')
NCBIGENE = CurieNamespace('NCBIGene', 'http://identifiers.org/ncbigene/')
NCBITAXON = CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_')
NCIT = CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_')
NDC = CurieNamespace('NDC', 'http://identifiers.org/ndc/')
NDDF = CurieNamespace('NDDF', 'http://purl.bioontology.org/ontology/NDDF/')
NLMID = CurieNamespace('NLMID', 'https://www.ncbi.nlm.nih.gov/nlmcatalog/?term=')
OBAN = CurieNamespace('OBAN', 'http://purl.org/oban/')
OBI = CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_')
OBO = CurieNamespace('OBO', 'http://purl.obolibrary.org/obo/')
OBOREL = CurieNamespace('OBOREL', 'http://purl.obolibrary.org/obo/RO_')
OGMS = CurieNamespace('OGMS', 'http://purl.obolibrary.org/obo/OGMS_')
OIO = CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#')
OMIM = CurieNamespace('OMIM', 'http://purl.obolibrary.org/obo/OMIM_')
ORCID = CurieNamespace('ORCID', 'https://orcid.org/')
ORPHA = CurieNamespace('ORPHA', 'http://www.orpha.net/ORDO/Orphanet_')
ORPHANET = CurieNamespace('ORPHANET', 'http://identifiers.org/orphanet/')
PANTHER_FAMILY = CurieNamespace('PANTHER_FAMILY', 'http://identifiers.org/panther.family/')
PANTHER_PATHWAY = CurieNamespace('PANTHER_PATHWAY', 'http://identifiers.org/panther.pathway/')
PATO = CurieNamespace('PATO', 'http://purl.obolibrary.org/obo/PATO_')
PATO_PROPERTY = CurieNamespace('PATO-PROPERTY', 'http://purl.obolibrary.org/obo/pato#')
PCO = CurieNamespace('PCO', 'http://purl.obolibrary.org/obo/PCO_')
PDQ = CurieNamespace('PDQ', 'https://www.cancer.gov/publications/pdq#')
PFAM = CurieNamespace('PFAM', 'http://identifiers.org/pfam/')
PHARMGKB_DRUG = CurieNamespace('PHARMGKB_DRUG', 'http://identifiers.org/pharmgkb.drug/')
PHARMGKB_PATHWAYS = CurieNamespace('PHARMGKB_PATHWAYS', 'http://identifiers.org/pharmgkb.pathways/')
PHAROS = CurieNamespace('PHAROS', 'http://pharos.nih.gov')
PIRSF = CurieNamespace('PIRSF', 'http://identifiers.org/pirsf/')
PMID = CurieNamespace('PMID', 'http://www.ncbi.nlm.nih.gov/pubmed/')
PO = CurieNamespace('PO', 'http://purl.obolibrary.org/obo/PO_')
POMBASE = CurieNamespace('POMBASE', 'http://identifiers.org/pombase/')
PR = CurieNamespace('PR', 'http://purl.obolibrary.org/obo/PR_')
PRINTS = CurieNamespace('PRINTS', 'http://identifiers.org/prints/')
PRODOM = CurieNamespace('PRODOM', 'http://identifiers.org/prodom/')
PROSITE = CurieNamespace('PROSITE', 'http://identifiers.org/prosite/')
PUBCHEM_COMPOUND = CurieNamespace('PUBCHEM_COMPOUND', 'http://identifiers.org/pubchem.compound/')
PUBCHEM_SUBSTANCE = CurieNamespace('PUBCHEM_SUBSTANCE', 'http://identifiers.org/pubchem.substance/')
PW = CurieNamespace('PW', 'http://purl.obolibrary.org/obo/PW_')
PATHWHIZ = CurieNamespace('PathWhiz', 'http://smpdb.ca/pathways/#')
REACT = CurieNamespace('REACT', 'http://www.reactome.org/PathwayBrowser/#/')
REPODB = CurieNamespace('REPODB', 'http://apps.chiragjpgroup.org/repoDB/')
RFAM = CurieNamespace('RFAM', 'http://identifiers.org/rfam/')
RGD = CurieNamespace('RGD', 'http://identifiers.org/rgd/')
RHEA = CurieNamespace('RHEA', 'http://identifiers.org/rhea/')
RNACENTRAL = CurieNamespace('RNACENTRAL', 'http://identifiers.org/rnacentral/')
RO = CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_')
RTXKG1 = CurieNamespace('RTXKG1', 'http://kg1endpoint.rtx.ai/')
RXCUI = CurieNamespace('RXCUI', 'https://mor.nlm.nih.gov/RxNav/search?searchBy=RXCUI&searchTerm=')
RXNORM = CurieNamespace('RXNORM', 'http://purl.bioontology.org/ontology/RXNORM/')
RESEARCHID = CurieNamespace('ResearchID', 'https://publons.com/researcher/')
SEMMEDDB = CurieNamespace('SEMMEDDB', 'https://skr3.nlm.nih.gov/SemMedDB')
SEPIO = CurieNamespace('SEPIO', 'http://purl.obolibrary.org/obo/SEPIO_')
SGD = CurieNamespace('SGD', 'http://identifiers.org/sgd/')
SIDER_DRUG = CurieNamespace('SIDER_DRUG', 'http://identifiers.org/sider.drug/')
SIO = CurieNamespace('SIO', 'http://semanticscience.org/resource/SIO_')
SMART = CurieNamespace('SMART', 'http://identifiers.org/smart/')
SMPDB = CurieNamespace('SMPDB', 'http://identifiers.org/smpdb/')
SNOMED = CurieNamespace('SNOMED', 'http://purl.obolibrary.org/obo/SNOMED_')
SNOMEDCT = CurieNamespace('SNOMEDCT', 'http://identifiers.org/snomedct/')
SNPEFF = CurieNamespace('SNPEFF', 'http://translator.ncats.nih.gov/SNPEFF_')
SO = CurieNamespace('SO', 'http://purl.obolibrary.org/obo/SO_')
STATO = CurieNamespace('STATO', 'http://purl.obolibrary.org/obo/STATO_')
SUPFAM = CurieNamespace('SUPFAM', 'http://identifiers.org/supfam/')
SCOPUSID = CurieNamespace('ScopusID', 'https://www.scopus.com/authid/detail.uri?authorId=')
TAXRANK = CurieNamespace('TAXRANK', 'http://purl.obolibrary.org/obo/TAXRANK_')
TCDB = CurieNamespace('TCDB', 'http://identifiers.org/tcdb/')
TIGRFAM = CurieNamespace('TIGRFAM', 'http://identifiers.org/tigrfam/')
UBERGRAPH = CurieNamespace('UBERGRAPH', 'http://translator.renci.org/ubergraph-axioms.ofn#')
UBERON = CurieNamespace('UBERON', 'http://purl.obolibrary.org/obo/UBERON_')
UBERON_CORE = CurieNamespace('UBERON_CORE', 'http://purl.obolibrary.org/obo/uberon/core#')
UMLS = CurieNamespace('UMLS', 'http://identifiers.org/umls/')
UMLSSC = CurieNamespace('UMLSSC', 'https://metamap.nlm.nih.gov/Docs/SemanticTypes_2018AB.txt/code#')
UMLSSG = CurieNamespace('UMLSSG', 'https://metamap.nlm.nih.gov/Docs/SemGroups_2018.txt/group#')
UMLSST = CurieNamespace('UMLSST', 'https://metamap.nlm.nih.gov/Docs/SemanticTypes_2018AB.txt/type#')
UNII = CurieNamespace('UNII', 'http://identifiers.org/unii/')
UNIPROT_ISOFORM = CurieNamespace('UNIPROT_ISOFORM', 'http://identifiers.org/uniprot.isoform/')
UO = CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_')
UPHENO = CurieNamespace('UPHENO', 'http://purl.obolibrary.org/obo/UPHENO_')
UNIPROTKB = CurieNamespace('UniProtKB', 'http://identifiers.org/uniprot/')
VANDF = CurieNamespace('VANDF', 'https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/VANDF/')
VMC = CurieNamespace('VMC', 'https://github.com/ga4gh/vr-spec/')
WB = CurieNamespace('WB', 'http://identifiers.org/wb/')
WBPHENOTYPE = CurieNamespace('WBPhenotype', 'http://purl.obolibrary.org/obo/WBPhenotype_')
WBVOCAB = CurieNamespace('WBVocab', 'http://bio2rdf.org/wormbase_vocabulary')
WIKIDATA = CurieNamespace('WIKIDATA', 'https://www.wikidata.org/wiki/')
WIKIDATA_PROPERTY = CurieNamespace('WIKIDATA_PROPERTY', 'https://www.wikidata.org/wiki/Property:')
WIKIPATHWAYS = CurieNamespace('WIKIPATHWAYS', 'http://identifiers.org/wikipathways/')
WORMBASE = CurieNamespace('WormBase', 'https://www.wormbase.org/get?name=')
XCO = CurieNamespace('XCO', 'http://purl.obolibrary.org/obo/XCO_')
ZFIN = CurieNamespace('ZFIN', 'http://identifiers.org/zfin/')
ZP = CurieNamespace('ZP', 'http://purl.obolibrary.org/obo/ZP_')
ALLIANCEGENOME = CurieNamespace('alliancegenome', 'https://www.alliancegenome.org/')
BIOLINK = CurieNamespace('biolink', 'https://w3id.org/biolink/vocab/')
CHEMBIO = CurieNamespace('chembio', 'http://translator.ncats.nih.gov/chembio_')
DCAT = CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#')
DCT = CurieNamespace('dct', 'http://purl.org/dc/terms/')
DCTYPES = CurieNamespace('dctypes', 'http://purl.org/dc/dcmitype/')
DICTYBASE = CurieNamespace('dictyBase', 'http://dictybase.org/gene/')
DOI = CurieNamespace('doi', 'https://doi.org/')
FABIO = CurieNamespace('fabio', 'http://purl.org/spar/fabio/')
FALDO = CurieNamespace('faldo', 'http://biohackathon.org/resource/faldo#')
FOAF = CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/')
FOODB_COMPOUND = CurieNamespace('foodb_compound', 'http://foodb.ca/compounds/')
GFF3 = CurieNamespace('gff3', 'https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md#')
GPI = CurieNamespace('gpi', 'https://github.com/geneontology/go-annotation/blob/master/specs/gpad-gpi-2-0.md#')
GTPO = CurieNamespace('gtpo', 'https://rdf.guidetopharmacology.org/ns/gtpo#')
HETIO = CurieNamespace('hetio', 'http://translator.ncats.nih.gov/hetio_')
INTERPRO = CurieNamespace('interpro', 'https://www.ebi.ac.uk/interpro/entry/')
ISBN = CurieNamespace('isbn', 'https://www.isbn-international.org/identifier/')
ISNI = CurieNamespace('isni', 'https://isni.org/isni/')
ISSN = CurieNamespace('issn', 'https://portal.issn.org/resource/ISSN/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MEDGEN = CurieNamespace('medgen', 'https://www.ncbi.nlm.nih.gov/medgen/')
OBOINOWL = CurieNamespace('oboInOwl', 'http://www.geneontology.org/formats/oboInOwl#')
OBOFORMAT = CurieNamespace('oboformat', 'http://www.geneontology.org/formats/oboInOWL#')
OS = CurieNamespace('os', 'https://github.com/cmungall/owlstar/blob/master/owlstar.ttl')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
PAV = CurieNamespace('pav', 'http://purl.org/pav/')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QUD = CurieNamespace('qud', 'http://qudt.org/1.1/schema/qudt#')
RDF = CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
SKOS = CurieNamespace('skos', 'https://www.w3.org/TR/skos-reference/#')
WGS = CurieNamespace('wgs', 'http://www.w3.org/2003/01/geo/wgs84_pos')
XSD = CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#')
DEFAULT_ = BIOLINK


# Types
class ChemicalFormulaValue(str):
    """ A chemical formula """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "chemical formula value"
    type_model_uri = BIOLINK.ChemicalFormulaValue


class CategoryType(Uriorcurie):
    """ A primitive type in which the value denotes a class within the biolink model. The value must be a URI or a CURIE. In a Neo4j representation, the value should be the CURIE for the biolink class, for example biolink:Gene. For an RDF representation, the value should be a URI such as https://w3id.org/biolink/vocab/Gene """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "category type"
    type_model_uri = BIOLINK.CategoryType


class IriType(Uriorcurie):
    """ An IRI """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "iri type"
    type_model_uri = BIOLINK.IriType


class LabelType(String):
    """ A string that provides a human-readable name for an entity """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "label type"
    type_model_uri = BIOLINK.LabelType


class PredicateType(Uriorcurie):
    """ A CURIE from the biolink related_to hierarchy. For example, biolink:related_to, biolink:causes, biolink:treats. """
    type_class_uri = XSD.anyURI
    type_class_curie = "xsd:anyURI"
    type_name = "predicate type"
    type_model_uri = BIOLINK.PredicateType


class NarrativeText(String):
    """ A string that provides a human-readable description of something """
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "narrative text"
    type_model_uri = BIOLINK.NarrativeText


class SymbolType(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "symbol type"
    type_model_uri = BIOLINK.SymbolType


class FrequencyValue(String):
    type_class_uri = UO["0000105"]
    type_class_curie = "UO:0000105"
    type_name = "frequency value"
    type_model_uri = BIOLINK.FrequencyValue


class PercentageFrequencyValue(Double):
    type_class_uri = UO["0000187"]
    type_class_curie = "UO:0000187"
    type_name = "percentage frequency value"
    type_model_uri = BIOLINK.PercentageFrequencyValue


class Quotient(Double):
    type_class_uri = UO["0010006"]
    type_class_curie = "UO:0010006"
    type_name = "quotient"
    type_model_uri = BIOLINK.Quotient


class Unit(String):
    type_class_uri = UO["0000000"]
    type_class_curie = "UO:0000000"
    type_name = "unit"
    type_model_uri = BIOLINK.Unit


class TimeType(Time):
    type_class_uri = XSD.dateTime
    type_class_curie = "xsd:dateTime"
    type_name = "time type"
    type_model_uri = BIOLINK.TimeType


class BiologicalSequence(String):
    type_class_uri = XSD.string
    type_class_curie = "xsd:string"
    type_name = "biological sequence"
    type_model_uri = BIOLINK.BiologicalSequence


# Class references
class EntityId(extended_str):
    pass


class NamedThingId(EntityId):
    pass


class OrganismTaxonId(NamedThingId):
    pass


class AdministrativeEntityId(NamedThingId):
    pass


class AgentId(AdministrativeEntityId):
    pass


class InformationContentEntityId(NamedThingId):
    pass


class DatasetId(InformationContentEntityId):
    pass


class DatasetDistributionId(InformationContentEntityId):
    pass


class DatasetVersionId(InformationContentEntityId):
    pass


class DatasetSummaryId(InformationContentEntityId):
    pass


class ConfidenceLevelId(InformationContentEntityId):
    pass


class EvidenceTypeId(InformationContentEntityId):
    pass


class PublicationId(InformationContentEntityId):
    pass


class BookId(PublicationId):
    pass


class BookChapterId(PublicationId):
    pass


class SerialId(PublicationId):
    pass


class ArticleId(PublicationId):
    pass


class PhysicalEntityId(NamedThingId):
    pass


class ActivityId(NamedThingId):
    pass


class ProcedureId(NamedThingId):
    pass


class PhenomenonId(NamedThingId):
    pass


class DeviceId(NamedThingId):
    pass


class MaterialSampleId(PhysicalEntityId):
    pass


class PlanetaryEntityId(NamedThingId):
    pass


class EnvironmentalProcessId(PlanetaryEntityId):
    pass


class EnvironmentalFeatureId(PlanetaryEntityId):
    pass


class GeographicLocationId(PlanetaryEntityId):
    pass


class GeographicLocationAtTimeId(GeographicLocationId):
    pass


class BiologicalEntityId(NamedThingId):
    pass


class MolecularEntityId(BiologicalEntityId):
    pass


class BiologicalProcessOrActivityId(BiologicalEntityId):
    pass


class MolecularActivityId(BiologicalProcessOrActivityId):
    pass


class BiologicalProcessId(BiologicalProcessOrActivityId):
    pass


class PathwayId(BiologicalProcessId):
    pass


class PhysiologicalProcessId(BiologicalProcessId):
    pass


class BehaviorId(BiologicalProcessId):
    pass


class DeathId(BiologicalProcessId):
    pass


class ChemicalSubstanceId(MolecularEntityId):
    pass


class CarbohydrateId(ChemicalSubstanceId):
    pass


class ProcessedMaterialId(ChemicalSubstanceId):
    pass


class DrugId(MolecularEntityId):
    pass


class FoodComponentId(ChemicalSubstanceId):
    pass


class EnvironmentalFoodContaminantId(ChemicalSubstanceId):
    pass


class FoodAdditiveId(ChemicalSubstanceId):
    pass


class NutrientId(ChemicalSubstanceId):
    pass


class MacronutrientId(NutrientId):
    pass


class MicronutrientId(NutrientId):
    pass


class VitaminId(MicronutrientId):
    pass


class FoodId(MolecularEntityId):
    pass


class MetaboliteId(ChemicalSubstanceId):
    pass


class OrganismalEntityId(BiologicalEntityId):
    pass


class LifeStageId(OrganismalEntityId):
    pass


class IndividualOrganismId(OrganismalEntityId):
    pass


class PopulationOfIndividualOrganismsId(OrganismalEntityId):
    pass


class StudyPopulationId(PopulationOfIndividualOrganismsId):
    pass


class DiseaseOrPhenotypicFeatureId(BiologicalEntityId):
    pass


class DiseaseId(DiseaseOrPhenotypicFeatureId):
    pass


class PhenotypicFeatureId(DiseaseOrPhenotypicFeatureId):
    pass


class BehavioralFeatureId(PhenotypicFeatureId):
    pass


class AnatomicalEntityId(OrganismalEntityId):
    pass


class CellularComponentId(AnatomicalEntityId):
    pass


class CellId(AnatomicalEntityId):
    pass


class CellLineId(OrganismalEntityId):
    pass


class GrossAnatomicalStructureId(AnatomicalEntityId):
    pass


class GenomicEntityId(MolecularEntityId):
    pass


class GeneId(GenomicEntityId):
    pass


class GenomeId(GenomicEntityId):
    pass


class ExonId(GenomicEntityId):
    pass


class TranscriptId(GenomicEntityId):
    pass


class CodingSequenceId(GenomicEntityId):
    pass


class ProteinId(GenomicEntityId):
    pass


class ProteinIsoformId(ProteinId):
    pass


class RNAProductId(TranscriptId):
    pass


class RNAProductIsoformId(RNAProductId):
    pass


class NoncodingRNAProductId(RNAProductId):
    pass


class MicroRNAId(NoncodingRNAProductId):
    pass


class SiRNAId(NoncodingRNAProductId):
    pass


class GeneFamilyId(MolecularEntityId):
    pass


class GenotypeId(GenomicEntityId):
    pass


class HaplotypeId(GenomicEntityId):
    pass


class SequenceVariantId(GenomicEntityId):
    pass


class SnvId(SequenceVariantId):
    pass


class ReagentTargetedGeneId(GenomicEntityId):
    pass


class ClinicalEntityId(NamedThingId):
    pass


class ClinicalTrialId(ClinicalEntityId):
    pass


class ClinicalInterventionId(ClinicalEntityId):
    pass


class ClinicalFindingId(PhenotypicFeatureId):
    pass


class HospitalizationId(ClinicalInterventionId):
    pass


class CaseId(IndividualOrganismId):
    pass


class CohortId(StudyPopulationId):
    pass


class GenomicBackgroundExposureId(GenomicEntityId):
    pass


class PathologicalProcessId(BiologicalProcessId):
    pass


class PathologicalProcessExposureId(PathologicalProcessId):
    pass


class PathologicalAnatomicalStructureId(AnatomicalEntityId):
    pass


class PathologicalAnatomicalExposureId(PathologicalAnatomicalStructureId):
    pass


class DiseaseOrPhenotypicFeatureExposureId(DiseaseOrPhenotypicFeatureId):
    pass


class ChemicalExposureId(ChemicalSubstanceId):
    pass


class ComplexChemicalExposureId(ChemicalExposureId):
    pass


class DrugExposureId(DrugId):
    pass


class DrugToGeneInteractionExposureId(DrugExposureId):
    pass


class TreatmentId(NamedThingId):
    pass


class BioticExposureId(OrganismTaxonId):
    pass


class GeographicExposureId(GeographicLocationId):
    pass


class EnvironmentalExposureId(EnvironmentalProcessId):
    pass


class BehavioralExposureId(BehaviorId):
    pass


class SocioeconomicExposureId(BehaviorId):
    pass


class PathologicalProcessOutcomeId(PathologicalProcessId):
    pass


class PathologicalAnatomicalOutcomeId(PathologicalAnatomicalStructureId):
    pass


class DiseaseOrPhenotypicFeatureOutcomeId(DiseaseOrPhenotypicFeatureId):
    pass


class BehavioralOutcomeId(BehaviorId):
    pass


class HospitalizationOutcomeId(HospitalizationId):
    pass


class MortalityOutcomeId(DeathId):
    pass


class EpidemiologicalOutcomeId(BiologicalEntityId):
    pass


class SocioeconomicOutcomeId(BehaviorId):
    pass


class AssociationId(EntityId):
    pass


class ContributorAssociationId(AssociationId):
    pass


class GenotypeToGenotypePartAssociationId(AssociationId):
    pass


class GenotypeToGeneAssociationId(AssociationId):
    pass


class GenotypeToVariantAssociationId(AssociationId):
    pass


class GeneToGeneAssociationId(AssociationId):
    pass


class GeneToGeneHomologyAssociationId(GeneToGeneAssociationId):
    pass


class GeneToGeneCoexpressionAssociationId(GeneToGeneAssociationId):
    pass


class PairwiseGeneToGeneInteractionId(GeneToGeneAssociationId):
    pass


class PairwiseMolecularInteractionId(PairwiseGeneToGeneInteractionId):
    pass


class CellLineToDiseaseOrPhenotypicFeatureAssociationId(AssociationId):
    pass


class ChemicalToChemicalAssociationId(AssociationId):
    pass


class ChemicalToChemicalDerivationAssociationId(ChemicalToChemicalAssociationId):
    pass


class ChemicalToDiseaseOrPhenotypicFeatureAssociationId(AssociationId):
    pass


class ChemicalToPathwayAssociationId(AssociationId):
    pass


class ChemicalToGeneAssociationId(AssociationId):
    pass


class DrugToGeneAssociationId(AssociationId):
    pass


class MaterialSampleDerivationAssociationId(AssociationId):
    pass


class MaterialSampleToDiseaseOrPhenotypicFeatureAssociationId(AssociationId):
    pass


class DiseaseToExposureEventAssociationId(AssociationId):
    pass


class ExposureEventToOutcomeAssociationId(AssociationId):
    pass


class DiseaseOrPhenotypicFeatureAssociationToLocationAssociationId(AssociationId):
    pass


class DiseaseOrPhenotypicFeatureToLocationAssociationId(AssociationId):
    pass


class GenotypeToPhenotypicFeatureAssociationId(AssociationId):
    pass


class ExposureEventToPhenotypicFeatureAssociationId(AssociationId):
    pass


class DiseaseToPhenotypicFeatureAssociationId(AssociationId):
    pass


class CaseToPhenotypicFeatureAssociationId(AssociationId):
    pass


class BehaviorToBehavioralFeatureAssociationId(AssociationId):
    pass


class GeneToPhenotypicFeatureAssociationId(AssociationId):
    pass


class GeneToDiseaseAssociationId(AssociationId):
    pass


class VariantToGeneAssociationId(AssociationId):
    pass


class VariantToGeneExpressionAssociationId(VariantToGeneAssociationId):
    pass


class VariantToPopulationAssociationId(AssociationId):
    pass


class PopulationToPopulationAssociationId(AssociationId):
    pass


class VariantToPhenotypicFeatureAssociationId(AssociationId):
    pass


class VariantToDiseaseAssociationId(AssociationId):
    pass


class GenotypeToDiseaseAssociationId(AssociationId):
    pass


class GeneAsAModelOfDiseaseAssociationId(GeneToDiseaseAssociationId):
    pass


class VariantAsAModelOfDiseaseAssociationId(VariantToDiseaseAssociationId):
    pass


class GenotypeAsAModelOfDiseaseAssociationId(GenotypeToDiseaseAssociationId):
    pass


class CellLineAsAModelOfDiseaseAssociationId(CellLineToDiseaseOrPhenotypicFeatureAssociationId):
    pass


class OrganismalEntityAsAModelOfDiseaseAssociationId(AssociationId):
    pass


class GeneHasVariantThatContributesToDiseaseAssociationId(GeneToDiseaseAssociationId):
    pass


class GeneToExpressionSiteAssociationId(AssociationId):
    pass


class SequenceVariantModulatesTreatmentAssociationId(AssociationId):
    pass


class FunctionalAssociationId(AssociationId):
    pass


class MacromolecularMachineToMolecularActivityAssociationId(FunctionalAssociationId):
    pass


class MacromolecularMachineToBiologicalProcessAssociationId(FunctionalAssociationId):
    pass


class MacromolecularMachineToCellularComponentAssociationId(FunctionalAssociationId):
    pass


class GeneToGoTermAssociationId(FunctionalAssociationId):
    pass


class SequenceAssociationId(AssociationId):
    pass


class GenomicSequenceLocalizationId(SequenceAssociationId):
    pass


class SequenceFeatureRelationshipId(AssociationId):
    pass


class TranscriptToGeneRelationshipId(SequenceFeatureRelationshipId):
    pass


class GeneToGeneProductRelationshipId(SequenceFeatureRelationshipId):
    pass


class ExonToTranscriptRelationshipId(SequenceFeatureRelationshipId):
    pass


class GeneRegulatoryRelationshipId(AssociationId):
    pass


class AnatomicalEntityToAnatomicalEntityAssociationId(AssociationId):
    pass


class AnatomicalEntityToAnatomicalEntityPartOfAssociationId(AnatomicalEntityToAnatomicalEntityAssociationId):
    pass


class AnatomicalEntityToAnatomicalEntityOntogenicAssociationId(AnatomicalEntityToAnatomicalEntityAssociationId):
    pass


class OrganismTaxonToOrganismTaxonAssociationId(AssociationId):
    pass


class OrganismTaxonToOrganismTaxonSpecializationId(OrganismTaxonToOrganismTaxonAssociationId):
    pass


class OrganismTaxonToOrganismTaxonInteractionId(OrganismTaxonToOrganismTaxonAssociationId):
    pass


class OrganismTaxonToEnvironmentAssociationId(AssociationId):
    pass


class OntologyClass(YAMLRoot):
    """
    a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be
    considered both instances of biolink classes, and OWL classes in their own right. In general you should not need
    to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of
    endocytosis (GO:0006897), use bl:BiologicalProcess as the type.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OntologyClass
    class_class_curie: ClassVar[str] = "biolink:OntologyClass"
    class_name: ClassVar[str] = "ontology class"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OntologyClass


class Annotation(YAMLRoot):
    """
    Biolink Model root class for entity annotations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Annotation
    class_class_curie: ClassVar[str] = "biolink:Annotation"
    class_name: ClassVar[str] = "annotation"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Annotation


@dataclass
class QuantityValue(Annotation):
    """
    A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric
    value
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.QuantityValue
    class_class_curie: ClassVar[str] = "biolink:QuantityValue"
    class_name: ClassVar[str] = "quantity value"
    class_model_uri: ClassVar[URIRef] = BIOLINK.QuantityValue

    has_unit: Optional[Union[str, Unit]] = None
    has_numeric_value: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_unit is not None and not isinstance(self.has_unit, Unit):
            self.has_unit = Unit(self.has_unit)

        if self.has_numeric_value is not None and not isinstance(self.has_numeric_value, float):
            self.has_numeric_value = float(self.has_numeric_value)

        super().__post_init__(**kwargs)


@dataclass
class Attribute(Annotation):
    """
    A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age,
    crispiness. An environmental sample may have attributes such as depth, lat, long, material.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Attribute
    class_class_curie: ClassVar[str] = "biolink:Attribute"
    class_name: ClassVar[str] = "attribute"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Attribute

    has_attribute_type: Union[dict, OntologyClass] = None
    name: Optional[Union[str, LabelType]] = None
    has_quantitative_value: Optional[Union[Union[dict, QuantityValue], List[Union[dict, QuantityValue]]]] = empty_list()
    has_qualitative_value: Optional[Union[str, NamedThingId]] = None
    iri: Optional[Union[str, IriType]] = None
    source: Optional[Union[str, LabelType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_attribute_type):
            self.MissingRequiredField("has_attribute_type")
        if not isinstance(self.has_attribute_type, OntologyClass):
            self.has_attribute_type = OntologyClass()

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        if not isinstance(self.has_quantitative_value, list):
            self.has_quantitative_value = [self.has_quantitative_value] if self.has_quantitative_value is not None else []
        self.has_quantitative_value = [v if isinstance(v, QuantityValue) else QuantityValue(**as_dict(v)) for v in self.has_quantitative_value]

        if self.has_qualitative_value is not None and not isinstance(self.has_qualitative_value, NamedThingId):
            self.has_qualitative_value = NamedThingId(self.has_qualitative_value)

        if self.iri is not None and not isinstance(self.iri, IriType):
            self.iri = IriType(self.iri)

        if self.source is not None and not isinstance(self.source, LabelType):
            self.source = LabelType(self.source)

        super().__post_init__(**kwargs)


@dataclass
class BiologicalSex(Attribute):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.BiologicalSex
    class_class_curie: ClassVar[str] = "biolink:BiologicalSex"
    class_name: ClassVar[str] = "biological sex"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BiologicalSex

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class PhenotypicSex(BiologicalSex):
    """
    An attribute corresponding to the phenotypic sex of the individual, based upon the reproductive organs present.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhenotypicSex
    class_class_curie: ClassVar[str] = "biolink:PhenotypicSex"
    class_name: ClassVar[str] = "phenotypic sex"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhenotypicSex

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class GenotypicSex(BiologicalSex):
    """
    An attribute corresponding to the genotypic sex of the individual, based upon genotypic composition of sex
    chromosomes.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypicSex
    class_class_curie: ClassVar[str] = "biolink:GenotypicSex"
    class_name: ClassVar[str] = "genotypic sex"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypicSex

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class SeverityValue(Attribute):
    """
    describes the severity of a phenotypic feature or disease
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SeverityValue
    class_class_curie: ClassVar[str] = "biolink:SeverityValue"
    class_name: ClassVar[str] = "severity value"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SeverityValue

    has_attribute_type: Union[dict, OntologyClass] = None

class RelationshipQuantifier(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.RelationshipQuantifier
    class_class_curie: ClassVar[str] = "biolink:RelationshipQuantifier"
    class_name: ClassVar[str] = "relationship quantifier"
    class_model_uri: ClassVar[URIRef] = BIOLINK.RelationshipQuantifier


class SensitivityQuantifier(RelationshipQuantifier):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SensitivityQuantifier
    class_class_curie: ClassVar[str] = "biolink:SensitivityQuantifier"
    class_name: ClassVar[str] = "sensitivity quantifier"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SensitivityQuantifier


class SpecificityQuantifier(RelationshipQuantifier):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SpecificityQuantifier
    class_class_curie: ClassVar[str] = "biolink:SpecificityQuantifier"
    class_name: ClassVar[str] = "specificity quantifier"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SpecificityQuantifier


class PathognomonicityQuantifier(SpecificityQuantifier):
    """
    A relationship quantifier between a variant or symptom and a disease, which is high when the presence of the
    feature implies the existence of the disease
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathognomonicityQuantifier
    class_class_curie: ClassVar[str] = "biolink:PathognomonicityQuantifier"
    class_name: ClassVar[str] = "pathognomonicity quantifier"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathognomonicityQuantifier


@dataclass
class FrequencyQuantifier(RelationshipQuantifier):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.FrequencyQuantifier
    class_class_curie: ClassVar[str] = "biolink:FrequencyQuantifier"
    class_name: ClassVar[str] = "frequency quantifier"
    class_model_uri: ClassVar[URIRef] = BIOLINK.FrequencyQuantifier

    has_count: Optional[int] = None
    has_total: Optional[int] = None
    has_quotient: Optional[float] = None
    has_percentage: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.has_count is not None and not isinstance(self.has_count, int):
            self.has_count = int(self.has_count)

        if self.has_total is not None and not isinstance(self.has_total, int):
            self.has_total = int(self.has_total)

        if self.has_quotient is not None and not isinstance(self.has_quotient, float):
            self.has_quotient = float(self.has_quotient)

        if self.has_percentage is not None and not isinstance(self.has_percentage, float):
            self.has_percentage = float(self.has_percentage)

        super().__post_init__(**kwargs)


class ChemicalOrDrugOrTreatment(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalOrDrugOrTreatment
    class_class_curie: ClassVar[str] = "biolink:ChemicalOrDrugOrTreatment"
    class_name: ClassVar[str] = "chemical or drug or treatment"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalOrDrugOrTreatment


@dataclass
class Entity(YAMLRoot):
    """
    Root Biolink Model class for all things and informational relationships, real or imagined.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Entity
    class_class_curie: ClassVar[str] = "biolink:Entity"
    class_name: ClassVar[str] = "entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Entity

    id: Union[str, EntityId] = None
    iri: Optional[Union[str, IriType]] = None
    category: Optional[Union[Union[str, CategoryType], List[Union[str, CategoryType]]]] = empty_list()
    type: Optional[str] = None
    name: Optional[Union[str, LabelType]] = None
    description: Optional[Union[str, NarrativeText]] = None
    source: Optional[Union[str, LabelType]] = None
    provided_by: Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]] = empty_list()
    has_attribute: Optional[Union[Union[dict, Attribute], List[Union[dict, Attribute]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntityId):
            self.id = EntityId(self.id)

        if self.iri is not None and not isinstance(self.iri, IriType):
            self.iri = IriType(self.iri)

        if not isinstance(self.category, list):
            self.category = [self.category] if self.category is not None else []
        self.category = [v if isinstance(v, CategoryType) else CategoryType(v) for v in self.category]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        if self.description is not None and not isinstance(self.description, NarrativeText):
            self.description = NarrativeText(self.description)

        if self.source is not None and not isinstance(self.source, LabelType):
            self.source = LabelType(self.source)

        if not isinstance(self.provided_by, list):
            self.provided_by = [self.provided_by] if self.provided_by is not None else []
        self.provided_by = [v if isinstance(v, AgentId) else AgentId(v) for v in self.provided_by]

        self._normalize_inlined_as_dict(slot_name="has_attribute", slot_type=Attribute, key_name="has attribute type", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class NamedThing(Entity):
    """
    a databased entity or concept/class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.NamedThing
    class_class_curie: ClassVar[str] = "biolink:NamedThing"
    class_name: ClassVar[str] = "named thing"
    class_model_uri: ClassVar[URIRef] = BIOLINK.NamedThing

    id: Union[str, NamedThingId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self._is_empty(self.category):
            self.MissingRequiredField("category")
        if not isinstance(self.category, list):
            self.category = [self.category] if self.category is not None else []
        self.category = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.category]

        super().__post_init__(**kwargs)


class RelationshipType(OntologyClass):
    """
    An OWL property used as an edge label
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.RelationshipType
    class_class_curie: ClassVar[str] = "biolink:RelationshipType"
    class_name: ClassVar[str] = "relationship type"
    class_model_uri: ClassVar[URIRef] = BIOLINK.RelationshipType


class GeneOntologyClass(OntologyClass):
    """
    an ontology class that describes a functional aspect of a gene, gene prodoct or complex
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneOntologyClass
    class_class_curie: ClassVar[str] = "biolink:GeneOntologyClass"
    class_name: ClassVar[str] = "gene ontology class"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneOntologyClass


class UnclassifiedOntologyClass(OntologyClass):
    """
    this is used for nodes that are taken from an ontology but are not typed using an existing biolink class
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.UnclassifiedOntologyClass
    class_class_curie: ClassVar[str] = "biolink:UnclassifiedOntologyClass"
    class_name: ClassVar[str] = "unclassified ontology class"
    class_model_uri: ClassVar[URIRef] = BIOLINK.UnclassifiedOntologyClass


class TaxonomicRank(OntologyClass):
    """
    A descriptor for the rank within a taxonomic classification. Example instance: TAXRANK:0000017 (kingdom)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.TaxonomicRank
    class_class_curie: ClassVar[str] = "biolink:TaxonomicRank"
    class_name: ClassVar[str] = "taxonomic rank"
    class_model_uri: ClassVar[URIRef] = BIOLINK.TaxonomicRank


@dataclass
class OrganismTaxon(NamedThing):
    """
    A classification of a set of organisms. Example instances: NCBITaxon:9606 (Homo sapiens), NCBITaxon:2 (Bacteria).
    Can also be used to represent strains or subspecies.
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxon
    class_class_curie: ClassVar[str] = "biolink:OrganismTaxon"
    class_name: ClassVar[str] = "organism taxon"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxon

    id: Union[str, OrganismTaxonId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_taxonomic_rank: Optional[Union[dict, TaxonomicRank]] = None
    subclass_of: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganismTaxonId):
            self.id = OrganismTaxonId(self.id)

        if self.has_taxonomic_rank is not None and not isinstance(self.has_taxonomic_rank, TaxonomicRank):
            self.has_taxonomic_rank = TaxonomicRank()

        if not isinstance(self.subclass_of, list):
            self.subclass_of = [self.subclass_of] if self.subclass_of is not None else []
        self.subclass_of = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.subclass_of]

        super().__post_init__(**kwargs)


@dataclass
class AdministrativeEntity(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.AdministrativeEntity
    class_class_curie: ClassVar[str] = "biolink:AdministrativeEntity"
    class_name: ClassVar[str] = "administrative entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.AdministrativeEntity

    id: Union[str, AdministrativeEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

@dataclass
class Agent(AdministrativeEntity):
    """
    person, group, organization or project that provides a piece of information (i.e. a knowledge association)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Agent
    class_class_curie: ClassVar[str] = "biolink:Agent"
    class_name: ClassVar[str] = "agent"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Agent

    id: Union[str, AgentId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    affiliation: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    address: Optional[str] = None
    name: Optional[Union[str, LabelType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AgentId):
            self.id = AgentId(self.id)

        if not isinstance(self.affiliation, list):
            self.affiliation = [self.affiliation] if self.affiliation is not None else []
        self.affiliation = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.affiliation]

        if self.address is not None and not isinstance(self.address, str):
            self.address = str(self.address)

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        super().__post_init__(**kwargs)


@dataclass
class InformationContentEntity(NamedThing):
    """
    a piece of information that typically describes some topic of discourse or is used as support.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.InformationContentEntity
    class_class_curie: ClassVar[str] = "biolink:InformationContentEntity"
    class_name: ClassVar[str] = "information content entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.InformationContentEntity

    id: Union[str, InformationContentEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    license: Optional[str] = None
    rights: Optional[str] = None
    format: Optional[str] = None
    creation_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.license is not None and not isinstance(self.license, str):
            self.license = str(self.license)

        if self.rights is not None and not isinstance(self.rights, str):
            self.rights = str(self.rights)

        if self.format is not None and not isinstance(self.format, str):
            self.format = str(self.format)

        if self.creation_date is not None and not isinstance(self.creation_date, XSDDate):
            self.creation_date = XSDDate(self.creation_date)

        super().__post_init__(**kwargs)


@dataclass
class Dataset(InformationContentEntity):
    """
    an item that refers to a collection of data from a data source.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Dataset
    class_class_curie: ClassVar[str] = "biolink:Dataset"
    class_name: ClassVar[str] = "dataset"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Dataset

    id: Union[str, DatasetId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetId):
            self.id = DatasetId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DatasetDistribution(InformationContentEntity):
    """
    an item that holds distribution level information about a dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DatasetDistribution
    class_class_curie: ClassVar[str] = "biolink:DatasetDistribution"
    class_name: ClassVar[str] = "dataset distribution"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DatasetDistribution

    id: Union[str, DatasetDistributionId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    distribution_download_url: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetDistributionId):
            self.id = DatasetDistributionId(self.id)

        if self.distribution_download_url is not None and not isinstance(self.distribution_download_url, str):
            self.distribution_download_url = str(self.distribution_download_url)

        super().__post_init__(**kwargs)


@dataclass
class DatasetVersion(InformationContentEntity):
    """
    an item that holds version level information about a dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DatasetVersion
    class_class_curie: ClassVar[str] = "biolink:DatasetVersion"
    class_name: ClassVar[str] = "dataset version"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DatasetVersion

    id: Union[str, DatasetVersionId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_dataset: Optional[Union[str, DatasetId]] = None
    ingest_date: Optional[str] = None
    has_distribution: Optional[Union[str, DatasetDistributionId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetVersionId):
            self.id = DatasetVersionId(self.id)

        if self.has_dataset is not None and not isinstance(self.has_dataset, DatasetId):
            self.has_dataset = DatasetId(self.has_dataset)

        if self.ingest_date is not None and not isinstance(self.ingest_date, str):
            self.ingest_date = str(self.ingest_date)

        if self.has_distribution is not None and not isinstance(self.has_distribution, DatasetDistributionId):
            self.has_distribution = DatasetDistributionId(self.has_distribution)

        super().__post_init__(**kwargs)


@dataclass
class DatasetSummary(InformationContentEntity):
    """
    an item that holds summary level information about a dataset.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DatasetSummary
    class_class_curie: ClassVar[str] = "biolink:DatasetSummary"
    class_name: ClassVar[str] = "dataset summary"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DatasetSummary

    id: Union[str, DatasetSummaryId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    source_web_page: Optional[str] = None
    source_logo: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DatasetSummaryId):
            self.id = DatasetSummaryId(self.id)

        if self.source_web_page is not None and not isinstance(self.source_web_page, str):
            self.source_web_page = str(self.source_web_page)

        if self.source_logo is not None and not isinstance(self.source_logo, str):
            self.source_logo = str(self.source_logo)

        super().__post_init__(**kwargs)


@dataclass
class ConfidenceLevel(InformationContentEntity):
    """
    Level of confidence in a statement
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ConfidenceLevel
    class_class_curie: ClassVar[str] = "biolink:ConfidenceLevel"
    class_name: ClassVar[str] = "confidence level"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ConfidenceLevel

    id: Union[str, ConfidenceLevelId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ConfidenceLevelId):
            self.id = ConfidenceLevelId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class EvidenceType(InformationContentEntity):
    """
    Class of evidence that supports an association
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EvidenceType
    class_class_curie: ClassVar[str] = "biolink:EvidenceType"
    class_name: ClassVar[str] = "evidence type"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EvidenceType

    id: Union[str, EvidenceTypeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EvidenceTypeId):
            self.id = EvidenceTypeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Publication(InformationContentEntity):
    """
    Any published piece of information. Can refer to a whole publication, its encompassing publication (i.e. journal
    or book) or to a part of a publication, if of significant knowledge scope (e.g. a figure, figure legend, or
    section highlighted by NLP). The scope is intended to be general and include information published on the web, as
    well as printed materials, either directly or in one of the Publication Biolink category subclasses.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Publication
    class_class_curie: ClassVar[str] = "biolink:Publication"
    class_name: ClassVar[str] = "publication"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Publication

    id: Union[str, PublicationId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    type: str = None
    authors: Optional[Union[str, List[str]]] = empty_list()
    pages: Optional[Union[str, List[str]]] = empty_list()
    summary: Optional[str] = None
    keywords: Optional[Union[str, List[str]]] = empty_list()
    mesh_terms: Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]] = empty_list()
    xref: Optional[Union[Union[str, IriType], List[Union[str, IriType]]]] = empty_list()
    name: Optional[Union[str, LabelType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PublicationId):
            self.id = PublicationId(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [v if isinstance(v, str) else str(v) for v in self.authors]

        if not isinstance(self.pages, list):
            self.pages = [self.pages] if self.pages is not None else []
        self.pages = [v if isinstance(v, str) else str(v) for v in self.pages]

        if self.summary is not None and not isinstance(self.summary, str):
            self.summary = str(self.summary)

        if not isinstance(self.keywords, list):
            self.keywords = [self.keywords] if self.keywords is not None else []
        self.keywords = [v if isinstance(v, str) else str(v) for v in self.keywords]

        if not isinstance(self.mesh_terms, list):
            self.mesh_terms = [self.mesh_terms] if self.mesh_terms is not None else []
        self.mesh_terms = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.mesh_terms]

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, IriType) else IriType(v) for v in self.xref]

        if self.name is not None and not isinstance(self.name, LabelType):
            self.name = LabelType(self.name)

        super().__post_init__(**kwargs)


@dataclass
class Book(Publication):
    """
    This class may rarely be instantiated except if use cases of a given knowledge graph support its utility.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Book
    class_class_curie: ClassVar[str] = "biolink:Book"
    class_name: ClassVar[str] = "book"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Book

    id: Union[str, BookId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    type: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BookId):
            self.id = BookId(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass
class BookChapter(Publication):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.BookChapter
    class_class_curie: ClassVar[str] = "biolink:BookChapter"
    class_name: ClassVar[str] = "book chapter"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BookChapter

    id: Union[str, BookChapterId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    type: str = None
    published_in: Union[str, URIorCURIE] = None
    volume: Optional[str] = None
    chapter: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BookChapterId):
            self.id = BookChapterId(self.id)

        if self._is_empty(self.published_in):
            self.MissingRequiredField("published_in")
        if not isinstance(self.published_in, URIorCURIE):
            self.published_in = URIorCURIE(self.published_in)

        if self.volume is not None and not isinstance(self.volume, str):
            self.volume = str(self.volume)

        if self.chapter is not None and not isinstance(self.chapter, str):
            self.chapter = str(self.chapter)

        super().__post_init__(**kwargs)


@dataclass
class Serial(Publication):
    """
    This class may rarely be instantiated except if use cases of a given knowledge graph support its utility.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Serial
    class_class_curie: ClassVar[str] = "biolink:Serial"
    class_name: ClassVar[str] = "serial"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Serial

    id: Union[str, SerialId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    type: str = None
    iso_abbreviation: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SerialId):
            self.id = SerialId(self.id)

        if self._is_empty(self.type):
            self.MissingRequiredField("type")
        if not isinstance(self.type, str):
            self.type = str(self.type)

        if self.iso_abbreviation is not None and not isinstance(self.iso_abbreviation, str):
            self.iso_abbreviation = str(self.iso_abbreviation)

        if self.volume is not None and not isinstance(self.volume, str):
            self.volume = str(self.volume)

        if self.issue is not None and not isinstance(self.issue, str):
            self.issue = str(self.issue)

        super().__post_init__(**kwargs)


@dataclass
class Article(Publication):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Article
    class_class_curie: ClassVar[str] = "biolink:Article"
    class_name: ClassVar[str] = "article"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Article

    id: Union[str, ArticleId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    type: str = None
    published_in: Union[str, URIorCURIE] = None
    iso_abbreviation: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ArticleId):
            self.id = ArticleId(self.id)

        if self._is_empty(self.published_in):
            self.MissingRequiredField("published_in")
        if not isinstance(self.published_in, URIorCURIE):
            self.published_in = URIorCURIE(self.published_in)

        if self.iso_abbreviation is not None and not isinstance(self.iso_abbreviation, str):
            self.iso_abbreviation = str(self.iso_abbreviation)

        if self.volume is not None and not isinstance(self.volume, str):
            self.volume = str(self.volume)

        if self.issue is not None and not isinstance(self.issue, str):
            self.issue = str(self.issue)

        super().__post_init__(**kwargs)


class PhysicalEssenceOrOccurrent(YAMLRoot):
    """
    Either a physical or processual entity.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhysicalEssenceOrOccurrent
    class_class_curie: ClassVar[str] = "biolink:PhysicalEssenceOrOccurrent"
    class_name: ClassVar[str] = "physical essence or occurrent"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhysicalEssenceOrOccurrent


class PhysicalEssence(PhysicalEssenceOrOccurrent):
    """
    Semantic mixin concept.  Pertains to entities that have physical properties such as mass, volume, or charge.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhysicalEssence
    class_class_curie: ClassVar[str] = "biolink:PhysicalEssence"
    class_name: ClassVar[str] = "physical essence"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhysicalEssence


@dataclass
class PhysicalEntity(NamedThing):
    """
    An entity that has material reality (a.k.a. physical essence).
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhysicalEntity
    class_class_curie: ClassVar[str] = "biolink:PhysicalEntity"
    class_name: ClassVar[str] = "physical entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhysicalEntity

    id: Union[str, PhysicalEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PhysicalEntityId):
            self.id = PhysicalEntityId(self.id)

        super().__post_init__(**kwargs)


class Occurrent(PhysicalEssenceOrOccurrent):
    """
    A processual entity.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Occurrent
    class_class_curie: ClassVar[str] = "biolink:Occurrent"
    class_name: ClassVar[str] = "occurrent"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Occurrent


class ActivityAndBehavior(Occurrent):
    """
    Activity or behavior of any independent integral living, organization or mechanical actor in the world
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ActivityAndBehavior
    class_class_curie: ClassVar[str] = "biolink:ActivityAndBehavior"
    class_name: ClassVar[str] = "activity and behavior"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ActivityAndBehavior


@dataclass
class Activity(NamedThing):
    """
    An activity is something that occurs over a period of time and acts upon or with entities; it may include
    consuming, processing, transforming, modifying, relocating, using, or generating entities.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Activity
    class_class_curie: ClassVar[str] = "biolink:Activity"
    class_name: ClassVar[str] = "activity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Activity

    id: Union[str, ActivityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ActivityId):
            self.id = ActivityId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Procedure(NamedThing):
    """
    A series of actions conducted in a certain order or manner
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Procedure
    class_class_curie: ClassVar[str] = "biolink:Procedure"
    class_name: ClassVar[str] = "procedure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Procedure

    id: Union[str, ProcedureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcedureId):
            self.id = ProcedureId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Phenomenon(NamedThing):
    """
    a fact or situation that is observed to exist or happen, especially one whose cause or explanation is in question
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Phenomenon
    class_class_curie: ClassVar[str] = "biolink:Phenomenon"
    class_name: ClassVar[str] = "phenomenon"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Phenomenon

    id: Union[str, PhenomenonId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PhenomenonId):
            self.id = PhenomenonId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Device(NamedThing):
    """
    A thing made or adapted for a particular purpose, especially a piece of mechanical or electronic equipment
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Device
    class_class_curie: ClassVar[str] = "biolink:Device"
    class_name: ClassVar[str] = "device"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Device

    id: Union[str, DeviceId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DeviceId):
            self.id = DeviceId(self.id)

        super().__post_init__(**kwargs)


class SubjectOfInvestigation(YAMLRoot):
    """
    An entity that has the role of being studied in an investigation, study, or experiment
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SubjectOfInvestigation
    class_class_curie: ClassVar[str] = "biolink:SubjectOfInvestigation"
    class_name: ClassVar[str] = "subject of investigation"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SubjectOfInvestigation


@dataclass
class MaterialSample(PhysicalEntity):
    """
    A sample is a limited quantity of something (e.g. an individual or set of individuals from a population, or a
    portion of a substance) to be used for testing, analysis, inspection, investigation, demonstration, or trial use.
    [SIO]
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MaterialSample
    class_class_curie: ClassVar[str] = "biolink:MaterialSample"
    class_name: ClassVar[str] = "material sample"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MaterialSample

    id: Union[str, MaterialSampleId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MaterialSampleId):
            self.id = MaterialSampleId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PlanetaryEntity(NamedThing):
    """
    Any entity or process that exists at the level of the whole planet
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PlanetaryEntity
    class_class_curie: ClassVar[str] = "biolink:PlanetaryEntity"
    class_name: ClassVar[str] = "planetary entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PlanetaryEntity

    id: Union[str, PlanetaryEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PlanetaryEntityId):
            self.id = PlanetaryEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class EnvironmentalProcess(PlanetaryEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalProcess
    class_class_curie: ClassVar[str] = "biolink:EnvironmentalProcess"
    class_name: ClassVar[str] = "environmental process"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalProcess

    id: Union[str, EnvironmentalProcessId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EnvironmentalProcessId):
            self.id = EnvironmentalProcessId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class EnvironmentalFeature(PlanetaryEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalFeature
    class_class_curie: ClassVar[str] = "biolink:EnvironmentalFeature"
    class_name: ClassVar[str] = "environmental feature"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalFeature

    id: Union[str, EnvironmentalFeatureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EnvironmentalFeatureId):
            self.id = EnvironmentalFeatureId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class GeographicLocation(PlanetaryEntity):
    """
    a location that can be described in lat/long coordinates
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeographicLocation
    class_class_curie: ClassVar[str] = "biolink:GeographicLocation"
    class_name: ClassVar[str] = "geographic location"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeographicLocation

    id: Union[str, GeographicLocationId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeographicLocationId):
            self.id = GeographicLocationId(self.id)

        if self.latitude is not None and not isinstance(self.latitude, float):
            self.latitude = float(self.latitude)

        if self.longitude is not None and not isinstance(self.longitude, float):
            self.longitude = float(self.longitude)

        super().__post_init__(**kwargs)


@dataclass
class GeographicLocationAtTime(GeographicLocation):
    """
    a location that can be described in lat/long coordinates, for a particular time
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeographicLocationAtTime
    class_class_curie: ClassVar[str] = "biolink:GeographicLocationAtTime"
    class_name: ClassVar[str] = "geographic location at time"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeographicLocationAtTime

    id: Union[str, GeographicLocationAtTimeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeographicLocationAtTimeId):
            self.id = GeographicLocationAtTimeId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class BiologicalEntity(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.BiologicalEntity
    class_class_curie: ClassVar[str] = "biolink:BiologicalEntity"
    class_name: ClassVar[str] = "biological entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BiologicalEntity

    id: Union[str, BiologicalEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

@dataclass
class ThingWithTaxon(YAMLRoot):
    """
    A mixin that can be used on any entity that can be taxonomically classified. This includes individual organisms;
    genes, their products and other molecular entities; body parts; biological processes
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ThingWithTaxon
    class_class_curie: ClassVar[str] = "biolink:ThingWithTaxon"
    class_name: ClassVar[str] = "thing with taxon"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ThingWithTaxon

    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class MolecularEntity(BiologicalEntity):
    """
    A gene, gene product, small molecule or macromolecule (including protein complex)"
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.MolecularEntity
    class_class_curie: ClassVar[str] = "biolink:MolecularEntity"
    class_name: ClassVar[str] = "molecular entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MolecularEntity

    id: Union[str, MolecularEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MolecularEntityId):
            self.id = MolecularEntityId(self.id)

        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class BiologicalProcessOrActivity(BiologicalEntity):
    """
    Either an individual molecular activity, or a collection of causally connected molecular activities in a
    biological system.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.BiologicalProcessOrActivity
    class_class_curie: ClassVar[str] = "biolink:BiologicalProcessOrActivity"
    class_name: ClassVar[str] = "biological process or activity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BiologicalProcessOrActivity

    id: Union[str, BiologicalProcessOrActivityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_input: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()
    has_output: Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]] = empty_list()
    enabled_by: Optional[Union[Union[str, PhysicalEntityId], List[Union[str, PhysicalEntityId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiologicalProcessOrActivityId):
            self.id = BiologicalProcessOrActivityId(self.id)

        if not isinstance(self.has_input, list):
            self.has_input = [self.has_input] if self.has_input is not None else []
        self.has_input = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.has_input]

        if not isinstance(self.has_output, list):
            self.has_output = [self.has_output] if self.has_output is not None else []
        self.has_output = [v if isinstance(v, NamedThingId) else NamedThingId(v) for v in self.has_output]

        if not isinstance(self.enabled_by, list):
            self.enabled_by = [self.enabled_by] if self.enabled_by is not None else []
        self.enabled_by = [v if isinstance(v, PhysicalEntityId) else PhysicalEntityId(v) for v in self.enabled_by]

        super().__post_init__(**kwargs)


@dataclass
class MolecularActivity(BiologicalProcessOrActivity):
    """
    An execution of a molecular function carried out by a gene product or macromolecular complex.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.MolecularActivity
    class_class_curie: ClassVar[str] = "biolink:MolecularActivity"
    class_name: ClassVar[str] = "molecular activity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MolecularActivity

    id: Union[str, MolecularActivityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_input: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()
    has_output: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()
    enabled_by: Optional[Union[Union[dict, "MacromolecularMachineMixin"], List[Union[dict, "MacromolecularMachineMixin"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MolecularActivityId):
            self.id = MolecularActivityId(self.id)

        if not isinstance(self.has_input, list):
            self.has_input = [self.has_input] if self.has_input is not None else []
        self.has_input = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_input]

        if not isinstance(self.has_output, list):
            self.has_output = [self.has_output] if self.has_output is not None else []
        self.has_output = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_output]

        if not isinstance(self.enabled_by, list):
            self.enabled_by = [self.enabled_by] if self.enabled_by is not None else []
        self.enabled_by = [v if isinstance(v, MacromolecularMachineMixin) else MacromolecularMachineMixin(**as_dict(v)) for v in self.enabled_by]

        super().__post_init__(**kwargs)


@dataclass
class BiologicalProcess(BiologicalProcessOrActivity):
    """
    One or more causally connected executions of molecular functions
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.BiologicalProcess
    class_class_curie: ClassVar[str] = "biolink:BiologicalProcess"
    class_name: ClassVar[str] = "biological process"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BiologicalProcess

    id: Union[str, BiologicalProcessId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BiologicalProcessId):
            self.id = BiologicalProcessId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Pathway(BiologicalProcess):
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Pathway
    class_class_curie: ClassVar[str] = "biolink:Pathway"
    class_name: ClassVar[str] = "pathway"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Pathway

    id: Union[str, PathwayId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathwayId):
            self.id = PathwayId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PhysiologicalProcess(BiologicalProcess):
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhysiologicalProcess
    class_class_curie: ClassVar[str] = "biolink:PhysiologicalProcess"
    class_name: ClassVar[str] = "physiological process"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhysiologicalProcess

    id: Union[str, PhysiologicalProcessId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PhysiologicalProcessId):
            self.id = PhysiologicalProcessId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Behavior(BiologicalProcess):
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Behavior
    class_class_curie: ClassVar[str] = "biolink:Behavior"
    class_name: ClassVar[str] = "behavior"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Behavior

    id: Union[str, BehaviorId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BehaviorId):
            self.id = BehaviorId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Death(BiologicalProcess):
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Death
    class_class_curie: ClassVar[str] = "biolink:Death"
    class_name: ClassVar[str] = "death"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Death

    id: Union[str, DeathId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DeathId):
            self.id = DeathId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Mixture(YAMLRoot):
    """
    The physical combination of two or more molecular entities in which the identities are retained and are mixed in
    the form of solutions, suspensions and colloids.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Mixture
    class_class_curie: ClassVar[str] = "biolink:Mixture"
    class_name: ClassVar[str] = "mixture"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Mixture

    has_constituent: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_constituent, list):
            self.has_constituent = [self.has_constituent] if self.has_constituent is not None else []
        self.has_constituent = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_constituent]

        super().__post_init__(**kwargs)


@dataclass
class ChemicalSubstance(MolecularEntity):
    """
    May be a chemical entity or a formulation with a chemical entity as active ingredient, or a complex material with
    multiple chemical entities as part
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalSubstance
    class_class_curie: ClassVar[str] = "biolink:ChemicalSubstance"
    class_name: ClassVar[str] = "chemical substance"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalSubstance

    id: Union[str, ChemicalSubstanceId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    is_metabolite: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalSubstanceId):
            self.id = ChemicalSubstanceId(self.id)

        if self.is_metabolite is not None and not isinstance(self.is_metabolite, Bool):
            self.is_metabolite = Bool(self.is_metabolite)

        super().__post_init__(**kwargs)


@dataclass
class Carbohydrate(ChemicalSubstance):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Carbohydrate
    class_class_curie: ClassVar[str] = "biolink:Carbohydrate"
    class_name: ClassVar[str] = "carbohydrate"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Carbohydrate

    id: Union[str, CarbohydrateId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CarbohydrateId):
            self.id = CarbohydrateId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ProcessedMaterial(ChemicalSubstance):
    """
    A chemical substance (often a mixture) processed for consumption for nutritional, medical or technical use.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ProcessedMaterial
    class_class_curie: ClassVar[str] = "biolink:ProcessedMaterial"
    class_name: ClassVar[str] = "processed material"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ProcessedMaterial

    id: Union[str, ProcessedMaterialId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_constituent: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessedMaterialId):
            self.id = ProcessedMaterialId(self.id)

        if not isinstance(self.has_constituent, list):
            self.has_constituent = [self.has_constituent] if self.has_constituent is not None else []
        self.has_constituent = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_constituent]

        super().__post_init__(**kwargs)


@dataclass
class Drug(MolecularEntity):
    """
    A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Drug
    class_class_curie: ClassVar[str] = "biolink:Drug"
    class_name: ClassVar[str] = "drug"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Drug

    id: Union[str, DrugId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_constituent: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DrugId):
            self.id = DrugId(self.id)

        if not isinstance(self.has_constituent, list):
            self.has_constituent = [self.has_constituent] if self.has_constituent is not None else []
        self.has_constituent = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_constituent]

        super().__post_init__(**kwargs)


@dataclass
class FoodComponent(ChemicalSubstance):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.FoodComponent
    class_class_curie: ClassVar[str] = "biolink:FoodComponent"
    class_name: ClassVar[str] = "food component"
    class_model_uri: ClassVar[URIRef] = BIOLINK.FoodComponent

    id: Union[str, FoodComponentId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FoodComponentId):
            self.id = FoodComponentId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class EnvironmentalFoodContaminant(ChemicalSubstance):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalFoodContaminant
    class_class_curie: ClassVar[str] = "biolink:EnvironmentalFoodContaminant"
    class_name: ClassVar[str] = "environmental food contaminant"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalFoodContaminant

    id: Union[str, EnvironmentalFoodContaminantId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EnvironmentalFoodContaminantId):
            self.id = EnvironmentalFoodContaminantId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class FoodAdditive(ChemicalSubstance):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.FoodAdditive
    class_class_curie: ClassVar[str] = "biolink:FoodAdditive"
    class_name: ClassVar[str] = "food additive"
    class_model_uri: ClassVar[URIRef] = BIOLINK.FoodAdditive

    id: Union[str, FoodAdditiveId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FoodAdditiveId):
            self.id = FoodAdditiveId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Nutrient(ChemicalSubstance):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Nutrient
    class_class_curie: ClassVar[str] = "biolink:Nutrient"
    class_name: ClassVar[str] = "nutrient"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Nutrient

    id: Union[str, NutrientId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NutrientId):
            self.id = NutrientId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Macronutrient(Nutrient):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Macronutrient
    class_class_curie: ClassVar[str] = "biolink:Macronutrient"
    class_name: ClassVar[str] = "macronutrient"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Macronutrient

    id: Union[str, MacronutrientId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MacronutrientId):
            self.id = MacronutrientId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Micronutrient(Nutrient):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Micronutrient
    class_class_curie: ClassVar[str] = "biolink:Micronutrient"
    class_name: ClassVar[str] = "micronutrient"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Micronutrient

    id: Union[str, MicronutrientId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MicronutrientId):
            self.id = MicronutrientId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Vitamin(Micronutrient):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Vitamin
    class_class_curie: ClassVar[str] = "biolink:Vitamin"
    class_name: ClassVar[str] = "vitamin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Vitamin

    id: Union[str, VitaminId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VitaminId):
            self.id = VitaminId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Food(MolecularEntity):
    """
    A substance consumed by a living organism as a source of nutrition
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Food
    class_class_curie: ClassVar[str] = "biolink:Food"
    class_name: ClassVar[str] = "food"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Food

    id: Union[str, FoodId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_constituent: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FoodId):
            self.id = FoodId(self.id)

        if not isinstance(self.has_constituent, list):
            self.has_constituent = [self.has_constituent] if self.has_constituent is not None else []
        self.has_constituent = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_constituent]

        super().__post_init__(**kwargs)


@dataclass
class Metabolite(ChemicalSubstance):
    """
    Any intermediate or product resulting from metabolism. Includes primary and secondary metabolites.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Metabolite
    class_class_curie: ClassVar[str] = "biolink:Metabolite"
    class_name: ClassVar[str] = "metabolite"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Metabolite

    id: Union[str, MetaboliteId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MetaboliteId):
            self.id = MetaboliteId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class OrganismAttribute(Attribute):
    """
    describes a characteristic of an organismal entity.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismAttribute
    class_class_curie: ClassVar[str] = "biolink:OrganismAttribute"
    class_name: ClassVar[str] = "organism attribute"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismAttribute

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class PhenotypicQuality(OrganismAttribute):
    """
    A property of a phenotype
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhenotypicQuality
    class_class_curie: ClassVar[str] = "biolink:PhenotypicQuality"
    class_name: ClassVar[str] = "phenotypic quality"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhenotypicQuality

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class Inheritance(OrganismAttribute):
    """
    The pattern or 'mode' in which a particular genetic trait or disorder is passed from one generation to the next,
    e.g. autosomal dominant, autosomal recessive, etc.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Inheritance
    class_class_curie: ClassVar[str] = "biolink:Inheritance"
    class_name: ClassVar[str] = "inheritance"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Inheritance

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class OrganismalEntity(BiologicalEntity):
    """
    A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding
    molecular entities
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismalEntity
    class_class_curie: ClassVar[str] = "biolink:OrganismalEntity"
    class_name: ClassVar[str] = "organismal entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismalEntity

    id: Union[str, OrganismalEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_attribute: Optional[Union[Union[dict, Attribute], List[Union[dict, Attribute]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="has_attribute", slot_type=Attribute, key_name="has attribute type", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class LifeStage(OrganismalEntity):
    """
    A stage of development or growth of an organism, including post-natal adult stages
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.LifeStage
    class_class_curie: ClassVar[str] = "biolink:LifeStage"
    class_name: ClassVar[str] = "life stage"
    class_model_uri: ClassVar[URIRef] = BIOLINK.LifeStage

    id: Union[str, LifeStageId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LifeStageId):
            self.id = LifeStageId(self.id)

        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class IndividualOrganism(OrganismalEntity):
    """
    An instance of an organism. For example, Richard Nixon, Charles Darwin, my pet cat. Example ID:
    ORCID:0000-0002-5355-2576
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.IndividualOrganism
    class_class_curie: ClassVar[str] = "biolink:IndividualOrganism"
    class_name: ClassVar[str] = "individual organism"
    class_model_uri: ClassVar[URIRef] = BIOLINK.IndividualOrganism

    id: Union[str, IndividualOrganismId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndividualOrganismId):
            self.id = IndividualOrganismId(self.id)

        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class PopulationOfIndividualOrganisms(OrganismalEntity):
    """
    A collection of individuals from the same taxonomic class distinguished by one or more characteristics.
    Characteristics can include, but are not limited to, shared geographic location, genetics, phenotypes [Alliance
    for Genome Resources]
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PopulationOfIndividualOrganisms
    class_class_curie: ClassVar[str] = "biolink:PopulationOfIndividualOrganisms"
    class_name: ClassVar[str] = "population of individual organisms"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PopulationOfIndividualOrganisms

    id: Union[str, PopulationOfIndividualOrganismsId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PopulationOfIndividualOrganismsId):
            self.id = PopulationOfIndividualOrganismsId(self.id)

        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class StudyPopulation(PopulationOfIndividualOrganisms):
    """
    A group of people banded together or treated as a group as participants in a research study.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.StudyPopulation
    class_class_curie: ClassVar[str] = "biolink:StudyPopulation"
    class_name: ClassVar[str] = "study population"
    class_model_uri: ClassVar[URIRef] = BIOLINK.StudyPopulation

    id: Union[str, StudyPopulationId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudyPopulationId):
            self.id = StudyPopulationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseOrPhenotypicFeature(BiologicalEntity):
    """
    Either one of a disease or an individual phenotypic feature. Some knowledge resources such as Monarch treat these
    as distinct, others such as MESH conflate.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeature
    class_class_curie: ClassVar[str] = "biolink:DiseaseOrPhenotypicFeature"
    class_name: ClassVar[str] = "disease or phenotypic feature"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeature

    id: Union[str, DiseaseOrPhenotypicFeatureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseOrPhenotypicFeatureId):
            self.id = DiseaseOrPhenotypicFeatureId(self.id)

        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class Disease(DiseaseOrPhenotypicFeature):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Disease
    class_class_curie: ClassVar[str] = "biolink:Disease"
    class_name: ClassVar[str] = "disease"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Disease

    id: Union[str, DiseaseId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseId):
            self.id = DiseaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PhenotypicFeature(DiseaseOrPhenotypicFeature):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PhenotypicFeature
    class_class_curie: ClassVar[str] = "biolink:PhenotypicFeature"
    class_name: ClassVar[str] = "phenotypic feature"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PhenotypicFeature

    id: Union[str, PhenotypicFeatureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PhenotypicFeatureId):
            self.id = PhenotypicFeatureId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class BehavioralFeature(PhenotypicFeature):
    """
    A phenotypic feature which is behavioral in nature.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.BehavioralFeature
    class_class_curie: ClassVar[str] = "biolink:BehavioralFeature"
    class_name: ClassVar[str] = "behavioral feature"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BehavioralFeature

    id: Union[str, BehavioralFeatureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BehavioralFeatureId):
            self.id = BehavioralFeatureId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class AnatomicalEntity(OrganismalEntity):
    """
    A subcellular location, cell type or gross anatomical part
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntity
    class_class_curie: ClassVar[str] = "biolink:AnatomicalEntity"
    class_name: ClassVar[str] = "anatomical entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntity

    id: Union[str, AnatomicalEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    in_taxon: Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnatomicalEntityId):
            self.id = AnatomicalEntityId(self.id)

        if not isinstance(self.in_taxon, list):
            self.in_taxon = [self.in_taxon] if self.in_taxon is not None else []
        self.in_taxon = [v if isinstance(v, OrganismTaxonId) else OrganismTaxonId(v) for v in self.in_taxon]

        super().__post_init__(**kwargs)


@dataclass
class CellularComponent(AnatomicalEntity):
    """
    A location in or around a cell
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.CellularComponent
    class_class_curie: ClassVar[str] = "biolink:CellularComponent"
    class_name: ClassVar[str] = "cellular component"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CellularComponent

    id: Union[str, CellularComponentId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellularComponentId):
            self.id = CellularComponentId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Cell(AnatomicalEntity):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Cell
    class_class_curie: ClassVar[str] = "biolink:Cell"
    class_name: ClassVar[str] = "cell"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Cell

    id: Union[str, CellId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellId):
            self.id = CellId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class CellLine(OrganismalEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.CellLine
    class_class_curie: ClassVar[str] = "biolink:CellLine"
    class_name: ClassVar[str] = "cell line"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CellLine

    id: Union[str, CellLineId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellLineId):
            self.id = CellLineId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class GrossAnatomicalStructure(AnatomicalEntity):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.GrossAnatomicalStructure
    class_class_curie: ClassVar[str] = "biolink:GrossAnatomicalStructure"
    class_name: ClassVar[str] = "gross anatomical structure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GrossAnatomicalStructure

    id: Union[str, GrossAnatomicalStructureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GrossAnatomicalStructureId):
            self.id = GrossAnatomicalStructureId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class MacromolecularMachineMixin(YAMLRoot):
    """
    A union of gene locus, gene product, and macromolecular complex mixin. These are the basic units of function in a
    cell. They either carry out individual biological activities, or they encode molecules which do this.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineMixin
    class_class_curie: ClassVar[str] = "biolink:MacromolecularMachineMixin"
    class_name: ClassVar[str] = "macromolecular machine mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineMixin

    name: Optional[Union[str, SymbolType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, SymbolType):
            self.name = SymbolType(self.name)

        super().__post_init__(**kwargs)


class GeneOrGeneProduct(MacromolecularMachineMixin):
    """
    A union of gene loci or gene products. Frequently an identifier for one will be used as proxy for another
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneOrGeneProduct
    class_class_curie: ClassVar[str] = "biolink:GeneOrGeneProduct"
    class_name: ClassVar[str] = "gene or gene product"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneOrGeneProduct


@dataclass
class GeneProductMixin(GeneOrGeneProduct):
    """
    The functional molecular product of a single gene locus. Gene products are either proteins or functional RNA
    molecules.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneProductMixin
    class_class_curie: ClassVar[str] = "biolink:GeneProductMixin"
    class_name: ClassVar[str] = "gene product mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneProductMixin

    synonym: Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]] = empty_list()
    xref: Optional[Union[Union[str, IriType], List[Union[str, IriType]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.synonym, list):
            self.synonym = [self.synonym] if self.synonym is not None else []
        self.synonym = [v if isinstance(v, LabelType) else LabelType(v) for v in self.synonym]

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, IriType) else IriType(v) for v in self.xref]

        super().__post_init__(**kwargs)


class GeneProductIsoformMixin(GeneProductMixin):
    """
    This is an abstract class that can be mixed in with different kinds of gene products to indicate that the gene
    product is intended to represent a specific isoform rather than a canonical or reference or generic product. The
    designation of canonical or reference may be arbitrary, or it may represent the superclass of all isoforms.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneProductIsoformMixin
    class_class_curie: ClassVar[str] = "biolink:GeneProductIsoformMixin"
    class_name: ClassVar[str] = "gene product isoform mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneProductIsoformMixin


class MacromolecularComplexMixin(MacromolecularMachineMixin):
    """
    A stable assembly of two or more macromolecules, i.e. proteins, nucleic acids, carbohydrates or lipids, in which
    at least one component is a protein and the constituent parts function together.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MacromolecularComplexMixin
    class_class_curie: ClassVar[str] = "biolink:MacromolecularComplexMixin"
    class_name: ClassVar[str] = "macromolecular complex mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MacromolecularComplexMixin


@dataclass
class GenomicEntity(MolecularEntity):
    """
    an entity that can either be directly located on a genome (gene, transcript, exon, regulatory region) or is
    encoded in a genome (protein)
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenomicEntity
    class_class_curie: ClassVar[str] = "biolink:GenomicEntity"
    class_name: ClassVar[str] = "genomic entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenomicEntity

    id: Union[str, GenomicEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_biological_sequence: Optional[Union[str, BiologicalSequence]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenomicEntityId):
            self.id = GenomicEntityId(self.id)

        if self.has_biological_sequence is not None and not isinstance(self.has_biological_sequence, BiologicalSequence):
            self.has_biological_sequence = BiologicalSequence(self.has_biological_sequence)

        super().__post_init__(**kwargs)


@dataclass
class Gene(GenomicEntity):
    """
    A region (or regions) that includes all of the sequence elements necessary to encode a functional transcript. A
    gene locus may include regulatory regions, transcribed regions and/or other functional sequence regions.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Gene
    class_class_curie: ClassVar[str] = "biolink:Gene"
    class_name: ClassVar[str] = "gene"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Gene

    id: Union[str, GeneId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    symbol: Optional[str] = None
    synonym: Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]] = empty_list()
    xref: Optional[Union[Union[str, IriType], List[Union[str, IriType]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneId):
            self.id = GeneId(self.id)

        if self.symbol is not None and not isinstance(self.symbol, str):
            self.symbol = str(self.symbol)

        if not isinstance(self.synonym, list):
            self.synonym = [self.synonym] if self.synonym is not None else []
        self.synonym = [v if isinstance(v, LabelType) else LabelType(v) for v in self.synonym]

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, IriType) else IriType(v) for v in self.xref]

        super().__post_init__(**kwargs)


@dataclass
class Genome(GenomicEntity):
    """
    A genome is the sum of genetic material within a cell or virion.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Genome
    class_class_curie: ClassVar[str] = "biolink:Genome"
    class_name: ClassVar[str] = "genome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Genome

    id: Union[str, GenomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenomeId):
            self.id = GenomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Exon(GenomicEntity):
    """
    A region of the transcript sequence within a gene which is not removed from the primary RNA transcript by RNA
    splicing.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Exon
    class_class_curie: ClassVar[str] = "biolink:Exon"
    class_name: ClassVar[str] = "exon"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Exon

    id: Union[str, ExonId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExonId):
            self.id = ExonId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Transcript(GenomicEntity):
    """
    An RNA synthesized on a DNA or RNA template by an RNA polymerase.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Transcript
    class_class_curie: ClassVar[str] = "biolink:Transcript"
    class_name: ClassVar[str] = "transcript"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Transcript

    id: Union[str, TranscriptId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TranscriptId):
            self.id = TranscriptId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class CodingSequence(GenomicEntity):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.CodingSequence
    class_class_curie: ClassVar[str] = "biolink:CodingSequence"
    class_name: ClassVar[str] = "coding sequence"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CodingSequence

    id: Union[str, CodingSequenceId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CodingSequenceId):
            self.id = CodingSequenceId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Protein(GenomicEntity):
    """
    A gene product that is composed of a chain of amino acid sequences and is produced by ribosome-mediated
    translation of mRNA
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Protein
    class_class_curie: ClassVar[str] = "biolink:Protein"
    class_name: ClassVar[str] = "protein"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Protein

    id: Union[str, ProteinId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    synonym: Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]] = empty_list()
    xref: Optional[Union[Union[str, IriType], List[Union[str, IriType]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProteinId):
            self.id = ProteinId(self.id)

        if not isinstance(self.synonym, list):
            self.synonym = [self.synonym] if self.synonym is not None else []
        self.synonym = [v if isinstance(v, LabelType) else LabelType(v) for v in self.synonym]

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, IriType) else IriType(v) for v in self.xref]

        super().__post_init__(**kwargs)


@dataclass
class ProteinIsoform(Protein):
    """
    Represents a protein that is a specific isoform of the canonical or reference protein. See
    https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4114032/
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ProteinIsoform
    class_class_curie: ClassVar[str] = "biolink:ProteinIsoform"
    class_name: ClassVar[str] = "protein isoform"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ProteinIsoform

    id: Union[str, ProteinIsoformId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProteinIsoformId):
            self.id = ProteinIsoformId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class RNAProduct(Transcript):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.RNAProduct
    class_class_curie: ClassVar[str] = "biolink:RNAProduct"
    class_name: ClassVar[str] = "RNA product"
    class_model_uri: ClassVar[URIRef] = BIOLINK.RNAProduct

    id: Union[str, RNAProductId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    synonym: Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]] = empty_list()
    xref: Optional[Union[Union[str, IriType], List[Union[str, IriType]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RNAProductId):
            self.id = RNAProductId(self.id)

        if not isinstance(self.synonym, list):
            self.synonym = [self.synonym] if self.synonym is not None else []
        self.synonym = [v if isinstance(v, LabelType) else LabelType(v) for v in self.synonym]

        if not isinstance(self.xref, list):
            self.xref = [self.xref] if self.xref is not None else []
        self.xref = [v if isinstance(v, IriType) else IriType(v) for v in self.xref]

        super().__post_init__(**kwargs)


@dataclass
class RNAProductIsoform(RNAProduct):
    """
    Represents a protein that is a specific isoform of the canonical or reference RNA
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.RNAProductIsoform
    class_class_curie: ClassVar[str] = "biolink:RNAProductIsoform"
    class_name: ClassVar[str] = "RNA product isoform"
    class_model_uri: ClassVar[URIRef] = BIOLINK.RNAProductIsoform

    id: Union[str, RNAProductIsoformId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, RNAProductIsoformId):
            self.id = RNAProductIsoformId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class NoncodingRNAProduct(RNAProduct):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.NoncodingRNAProduct
    class_class_curie: ClassVar[str] = "biolink:NoncodingRNAProduct"
    class_name: ClassVar[str] = "noncoding RNA product"
    class_model_uri: ClassVar[URIRef] = BIOLINK.NoncodingRNAProduct

    id: Union[str, NoncodingRNAProductId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NoncodingRNAProductId):
            self.id = NoncodingRNAProductId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class MicroRNA(NoncodingRNAProduct):
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.MicroRNA
    class_class_curie: ClassVar[str] = "biolink:MicroRNA"
    class_name: ClassVar[str] = "microRNA"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MicroRNA

    id: Union[str, MicroRNAId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MicroRNAId):
            self.id = MicroRNAId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class SiRNA(NoncodingRNAProduct):
    """
    A small RNA molecule that is the product of a longer exogenous or endogenous dsRNA, which is either a bimolecular
    duplex or very long hairpin, processed (via the Dicer pathway) such that numerous siRNAs accumulate from both
    strands of the dsRNA. SRNAs trigger the cleavage of their target molecules.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.SiRNA
    class_class_curie: ClassVar[str] = "biolink:SiRNA"
    class_name: ClassVar[str] = "siRNA"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SiRNA

    id: Union[str, SiRNAId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SiRNAId):
            self.id = SiRNAId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class GeneGroupingMixin(YAMLRoot):
    """
    any grouping of multiple genes or gene products
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneGroupingMixin
    class_class_curie: ClassVar[str] = "biolink:GeneGroupingMixin"
    class_name: ClassVar[str] = "gene grouping mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneGroupingMixin

    has_gene_or_gene_product: Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.has_gene_or_gene_product, list):
            self.has_gene_or_gene_product = [self.has_gene_or_gene_product] if self.has_gene_or_gene_product is not None else []
        self.has_gene_or_gene_product = [v if isinstance(v, GeneId) else GeneId(v) for v in self.has_gene_or_gene_product]

        super().__post_init__(**kwargs)


@dataclass
class GeneFamily(MolecularEntity):
    """
    any grouping of multiple genes or gene products related by common descent
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneFamily
    class_class_curie: ClassVar[str] = "biolink:GeneFamily"
    class_name: ClassVar[str] = "gene family"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneFamily

    id: Union[str, GeneFamilyId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_gene_or_gene_product: Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneFamilyId):
            self.id = GeneFamilyId(self.id)

        if not isinstance(self.has_gene_or_gene_product, list):
            self.has_gene_or_gene_product = [self.has_gene_or_gene_product] if self.has_gene_or_gene_product is not None else []
        self.has_gene_or_gene_product = [v if isinstance(v, GeneId) else GeneId(v) for v in self.has_gene_or_gene_product]

        super().__post_init__(**kwargs)


@dataclass
class Zygosity(Attribute):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Zygosity
    class_class_curie: ClassVar[str] = "biolink:Zygosity"
    class_name: ClassVar[str] = "zygosity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Zygosity

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class Genotype(GenomicEntity):
    """
    An information content entity that describes a genome by specifying the total variation in genomic sequence and/or
    gene expression, relative to some established background
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Genotype
    class_class_curie: ClassVar[str] = "biolink:Genotype"
    class_name: ClassVar[str] = "genotype"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Genotype

    id: Union[str, GenotypeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_zygosity: Optional[Union[dict, Zygosity]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeId):
            self.id = GenotypeId(self.id)

        if self.has_zygosity is not None and not isinstance(self.has_zygosity, Zygosity):
            self.has_zygosity = Zygosity(**as_dict(self.has_zygosity))

        super().__post_init__(**kwargs)


@dataclass
class Haplotype(GenomicEntity):
    """
    A set of zero or more Alleles on a single instance of a Sequence[VMC]
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Haplotype
    class_class_curie: ClassVar[str] = "biolink:Haplotype"
    class_name: ClassVar[str] = "haplotype"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Haplotype

    id: Union[str, HaplotypeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HaplotypeId):
            self.id = HaplotypeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class SequenceVariant(GenomicEntity):
    """
    An allele that varies in its sequence from what is considered the reference allele at that locus.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.SequenceVariant
    class_class_curie: ClassVar[str] = "biolink:SequenceVariant"
    class_name: ClassVar[str] = "sequence variant"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SequenceVariant

    id: Union[str, SequenceVariantId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_gene: Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]] = empty_list()
    has_biological_sequence: Optional[Union[str, BiologicalSequence]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SequenceVariantId):
            self.id = SequenceVariantId(self.id)

        if not isinstance(self.has_gene, list):
            self.has_gene = [self.has_gene] if self.has_gene is not None else []
        self.has_gene = [v if isinstance(v, GeneId) else GeneId(v) for v in self.has_gene]

        if self.has_biological_sequence is not None and not isinstance(self.has_biological_sequence, BiologicalSequence):
            self.has_biological_sequence = BiologicalSequence(self.has_biological_sequence)

        super().__post_init__(**kwargs)


@dataclass
class Snv(SequenceVariant):
    """
    SNVs are single nucleotide positions in genomic DNA at which different sequence alternatives exist
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Snv
    class_class_curie: ClassVar[str] = "biolink:Snv"
    class_name: ClassVar[str] = "snv"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Snv

    id: Union[str, SnvId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SnvId):
            self.id = SnvId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ReagentTargetedGene(GenomicEntity):
    """
    A gene altered in its expression level in the context of some experiment as a result of being targeted by
    gene-knockdown reagent(s) such as a morpholino or RNAi.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ReagentTargetedGene
    class_class_curie: ClassVar[str] = "biolink:ReagentTargetedGene"
    class_name: ClassVar[str] = "reagent targeted gene"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ReagentTargetedGene

    id: Union[str, ReagentTargetedGeneId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ReagentTargetedGeneId):
            self.id = ReagentTargetedGeneId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ClinicalAttribute(Attribute):
    """
    Attributes relating to a clinical manifestation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalAttribute
    class_class_curie: ClassVar[str] = "biolink:ClinicalAttribute"
    class_name: ClassVar[str] = "clinical attribute"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalAttribute

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class ClinicalMeasurement(ClinicalAttribute):
    """
    A clinical measurement is a special kind of attribute which results from a laboratory observation from a subject
    individual or sample. Measurements can be connected to their subject by the 'has attribute' slot.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalMeasurement
    class_class_curie: ClassVar[str] = "biolink:ClinicalMeasurement"
    class_name: ClassVar[str] = "clinical measurement"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalMeasurement

    has_attribute_type: Union[dict, OntologyClass] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.has_attribute_type):
            self.MissingRequiredField("has_attribute_type")
        if not isinstance(self.has_attribute_type, OntologyClass):
            self.has_attribute_type = OntologyClass()

        super().__post_init__(**kwargs)


@dataclass
class ClinicalModifier(ClinicalAttribute):
    """
    Used to characterize and specify the phenotypic abnormalities defined in the phenotypic abnormality sub-ontology,
    with respect to severity, laterality, and other aspects
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalModifier
    class_class_curie: ClassVar[str] = "biolink:ClinicalModifier"
    class_name: ClassVar[str] = "clinical modifier"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalModifier

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class ClinicalCourse(ClinicalAttribute):
    """
    The course a disease typically takes from its onset, progression in time, and eventual resolution or death of the
    affected individual
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalCourse
    class_class_curie: ClassVar[str] = "biolink:ClinicalCourse"
    class_name: ClassVar[str] = "clinical course"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalCourse

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class Onset(ClinicalCourse):
    """
    The age group in which (disease) symptom manifestations appear
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Onset
    class_class_curie: ClassVar[str] = "biolink:Onset"
    class_name: ClassVar[str] = "onset"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Onset

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class ClinicalEntity(NamedThing):
    """
    Any entity or process that exists in the clinical domain and outside the biological realm. Diseases are placed
    under biological entities
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalEntity
    class_class_curie: ClassVar[str] = "biolink:ClinicalEntity"
    class_name: ClassVar[str] = "clinical entity"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalEntity

    id: Union[str, ClinicalEntityId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClinicalEntityId):
            self.id = ClinicalEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ClinicalTrial(ClinicalEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalTrial
    class_class_curie: ClassVar[str] = "biolink:ClinicalTrial"
    class_name: ClassVar[str] = "clinical trial"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalTrial

    id: Union[str, ClinicalTrialId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClinicalTrialId):
            self.id = ClinicalTrialId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ClinicalIntervention(ClinicalEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalIntervention
    class_class_curie: ClassVar[str] = "biolink:ClinicalIntervention"
    class_name: ClassVar[str] = "clinical intervention"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalIntervention

    id: Union[str, ClinicalInterventionId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClinicalInterventionId):
            self.id = ClinicalInterventionId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ClinicalFinding(PhenotypicFeature):
    """
    this category is currently considered broad enough to tag clinical lab measurements and other biological
    attributes taken as 'clinical traits' with some statistical score, for example, a p value in genetic associations.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ClinicalFinding
    class_class_curie: ClassVar[str] = "biolink:ClinicalFinding"
    class_name: ClassVar[str] = "clinical finding"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ClinicalFinding

    id: Union[str, ClinicalFindingId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_attribute: Optional[Union[Union[dict, ClinicalAttribute], List[Union[dict, ClinicalAttribute]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ClinicalFindingId):
            self.id = ClinicalFindingId(self.id)

        self._normalize_inlined_as_dict(slot_name="has_attribute", slot_type=ClinicalAttribute, key_name="has attribute type", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Hospitalization(ClinicalIntervention):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Hospitalization
    class_class_curie: ClassVar[str] = "biolink:Hospitalization"
    class_name: ClassVar[str] = "hospitalization"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Hospitalization

    id: Union[str, HospitalizationId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HospitalizationId):
            self.id = HospitalizationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class SocioeconomicAttribute(Attribute):
    """
    Attributes relating to a socioeconomic manifestation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SocioeconomicAttribute
    class_class_curie: ClassVar[str] = "biolink:SocioeconomicAttribute"
    class_name: ClassVar[str] = "socioeconomic attribute"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SocioeconomicAttribute

    has_attribute_type: Union[dict, OntologyClass] = None

@dataclass
class Case(IndividualOrganism):
    """
    An individual (human) organism that has a patient role in some clinical context.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Case
    class_class_curie: ClassVar[str] = "biolink:Case"
    class_name: ClassVar[str] = "case"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Case

    id: Union[str, CaseId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CaseId):
            self.id = CaseId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Cohort(StudyPopulation):
    """
    A group of people banded together or treated as a group who share common characteristics. A cohort 'study' is a
    particular form of longitudinal study that samples a cohort, performing a cross-section at intervals through time.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.Cohort
    class_class_curie: ClassVar[str] = "biolink:Cohort"
    class_name: ClassVar[str] = "cohort"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Cohort

    id: Union[str, CohortId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CohortId):
            self.id = CohortId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ExposureEvent(YAMLRoot):
    """
    A (possibly time bounded) incidence of a feature of the environment of an organism that influences one or more
    phenotypic features of that organism, potentially mediated by genes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ExposureEvent
    class_class_curie: ClassVar[str] = "biolink:ExposureEvent"
    class_name: ClassVar[str] = "exposure event"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ExposureEvent

    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class GenomicBackgroundExposure(GenomicEntity):
    """
    A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or
    other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing
    an outcome.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenomicBackgroundExposure
    class_class_curie: ClassVar[str] = "biolink:GenomicBackgroundExposure"
    class_name: ClassVar[str] = "genomic background exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenomicBackgroundExposure

    id: Union[str, GenomicBackgroundExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None
    has_gene_or_gene_product: Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenomicBackgroundExposureId):
            self.id = GenomicBackgroundExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        if not isinstance(self.has_gene_or_gene_product, list):
            self.has_gene_or_gene_product = [self.has_gene_or_gene_product] if self.has_gene_or_gene_product is not None else []
        self.has_gene_or_gene_product = [v if isinstance(v, GeneId) else GeneId(v) for v in self.has_gene_or_gene_product]

        super().__post_init__(**kwargs)


class PathologicalEntityMixin(YAMLRoot):
    """
    A pathological (abnormal) structure or process.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalEntityMixin
    class_class_curie: ClassVar[str] = "biolink:PathologicalEntityMixin"
    class_name: ClassVar[str] = "pathological entity mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalEntityMixin


@dataclass
class PathologicalProcess(BiologicalProcess):
    """
    A biologic function or a process having an abnormal or deleterious effect at the subcellular, cellular,
    multicellular, or organismal level.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalProcess
    class_class_curie: ClassVar[str] = "biolink:PathologicalProcess"
    class_name: ClassVar[str] = "pathological process"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalProcess

    id: Union[str, PathologicalProcessId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathologicalProcessId):
            self.id = PathologicalProcessId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PathologicalProcessExposure(PathologicalProcess):
    """
    A pathological process, when viewed as an exposure, representing an precondition, leading to or influencing an
    outcome, e.g. autoimmunity leading to disease.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalProcessExposure
    class_class_curie: ClassVar[str] = "biolink:PathologicalProcessExposure"
    class_name: ClassVar[str] = "pathological process exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalProcessExposure

    id: Union[str, PathologicalProcessExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathologicalProcessExposureId):
            self.id = PathologicalProcessExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class PathologicalAnatomicalStructure(AnatomicalEntity):
    """
    An anatomical structure with the potential of have an abnormal or deleterious effect at the subcellular, cellular,
    multicellular, or organismal level.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalAnatomicalStructure
    class_class_curie: ClassVar[str] = "biolink:PathologicalAnatomicalStructure"
    class_name: ClassVar[str] = "pathological anatomical structure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalAnatomicalStructure

    id: Union[str, PathologicalAnatomicalStructureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathologicalAnatomicalStructureId):
            self.id = PathologicalAnatomicalStructureId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PathologicalAnatomicalExposure(PathologicalAnatomicalStructure):
    """
    An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or
    influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalAnatomicalExposure
    class_class_curie: ClassVar[str] = "biolink:PathologicalAnatomicalExposure"
    class_name: ClassVar[str] = "pathological anatomical exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalAnatomicalExposure

    id: Union[str, PathologicalAnatomicalExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathologicalAnatomicalExposureId):
            self.id = PathologicalAnatomicalExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseOrPhenotypicFeatureExposure(DiseaseOrPhenotypicFeature):
    """
    A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or
    influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin
    pigmentation predisposing an individual to skin cancer.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureExposure
    class_class_curie: ClassVar[str] = "biolink:DiseaseOrPhenotypicFeatureExposure"
    class_name: ClassVar[str] = "disease or phenotypic feature exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureExposure

    id: Union[str, DiseaseOrPhenotypicFeatureExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseOrPhenotypicFeatureExposureId):
            self.id = DiseaseOrPhenotypicFeatureExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class ChemicalExposure(ChemicalSubstance):
    """
    A chemical exposure is an intake of a particular chemical substance, other than a drug.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalExposure
    class_class_curie: ClassVar[str] = "biolink:ChemicalExposure"
    class_name: ClassVar[str] = "chemical exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalExposure

    id: Union[str, ChemicalExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalExposureId):
            self.id = ChemicalExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class ComplexChemicalExposure(ChemicalExposure):
    """
    A complex chemical exposure is an intake of a chemical mixture (e.g. gasoline), other than a drug.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.ComplexChemicalExposure
    class_class_curie: ClassVar[str] = "biolink:ComplexChemicalExposure"
    class_name: ClassVar[str] = "complex chemical exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ComplexChemicalExposure

    id: Union[str, ComplexChemicalExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_constituent: Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComplexChemicalExposureId):
            self.id = ComplexChemicalExposureId(self.id)

        if not isinstance(self.has_constituent, list):
            self.has_constituent = [self.has_constituent] if self.has_constituent is not None else []
        self.has_constituent = [v if isinstance(v, ChemicalSubstanceId) else ChemicalSubstanceId(v) for v in self.has_constituent]

        super().__post_init__(**kwargs)


@dataclass
class DrugExposure(Drug):
    """
    A drug exposure is an intake of a particular drug.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.DrugExposure
    class_class_curie: ClassVar[str] = "biolink:DrugExposure"
    class_name: ClassVar[str] = "drug exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DrugExposure

    id: Union[str, DrugExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DrugExposureId):
            self.id = DrugExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class DrugToGeneInteractionExposure(DrugExposure):
    """
    drug to gene interaction exposure is a drug exposure is where the interactions of the drug with specific genes are
    known to constitute an 'exposure' to the organism, leading to or influencing an outcome.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.DrugToGeneInteractionExposure
    class_class_curie: ClassVar[str] = "biolink:DrugToGeneInteractionExposure"
    class_name: ClassVar[str] = "drug to gene interaction exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DrugToGeneInteractionExposure

    id: Union[str, DrugToGeneInteractionExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_gene_or_gene_product: Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DrugToGeneInteractionExposureId):
            self.id = DrugToGeneInteractionExposureId(self.id)

        if not isinstance(self.has_gene_or_gene_product, list):
            self.has_gene_or_gene_product = [self.has_gene_or_gene_product] if self.has_gene_or_gene_product is not None else []
        self.has_gene_or_gene_product = [v if isinstance(v, GeneId) else GeneId(v) for v in self.has_gene_or_gene_product]

        super().__post_init__(**kwargs)


@dataclass
class Treatment(NamedThing):
    """
    A treatment is targeted at a disease or phenotype and may involve multiple drug 'exposures', medical devices
    and/or procedures
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Treatment
    class_class_curie: ClassVar[str] = "biolink:Treatment"
    class_name: ClassVar[str] = "treatment"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Treatment

    id: Union[str, TreatmentId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_drug: Optional[Union[Union[str, DrugId], List[Union[str, DrugId]]]] = empty_list()
    has_device: Optional[Union[Union[str, DeviceId], List[Union[str, DeviceId]]]] = empty_list()
    has_procedure: Optional[Union[Union[str, ProcedureId], List[Union[str, ProcedureId]]]] = empty_list()
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TreatmentId):
            self.id = TreatmentId(self.id)

        if not isinstance(self.has_drug, list):
            self.has_drug = [self.has_drug] if self.has_drug is not None else []
        self.has_drug = [v if isinstance(v, DrugId) else DrugId(v) for v in self.has_drug]

        if not isinstance(self.has_device, list):
            self.has_device = [self.has_device] if self.has_device is not None else []
        self.has_device = [v if isinstance(v, DeviceId) else DeviceId(v) for v in self.has_device]

        if not isinstance(self.has_procedure, list):
            self.has_procedure = [self.has_procedure] if self.has_procedure is not None else []
        self.has_procedure = [v if isinstance(v, ProcedureId) else ProcedureId(v) for v in self.has_procedure]

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class BioticExposure(OrganismTaxon):
    """
    An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).
    """
    _inherited_slots: ClassVar[List[str]] = ["subclass_of"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.BioticExposure
    class_class_curie: ClassVar[str] = "biolink:BioticExposure"
    class_name: ClassVar[str] = "biotic exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BioticExposure

    id: Union[str, BioticExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BioticExposureId):
            self.id = BioticExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class GeographicExposure(GeographicLocation):
    """
    A geographic exposure is a factor relating to geographic proximity to some impactful entity.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeographicExposure
    class_class_curie: ClassVar[str] = "biolink:GeographicExposure"
    class_name: ClassVar[str] = "geographic exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeographicExposure

    id: Union[str, GeographicExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeographicExposureId):
            self.id = GeographicExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class EnvironmentalExposure(EnvironmentalProcess):
    """
    A environmental exposure is a factor relating to abiotic processes in the environment including sunlight (UV-B),
    atmospheric (heat, cold, general pollution) and water-born contaminants.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalExposure
    class_class_curie: ClassVar[str] = "biolink:EnvironmentalExposure"
    class_name: ClassVar[str] = "environmental exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EnvironmentalExposure

    id: Union[str, EnvironmentalExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EnvironmentalExposureId):
            self.id = EnvironmentalExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class BehavioralExposure(Behavior):
    """
    A behavioral exposure is a factor relating to behavior impacting an individual.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.BehavioralExposure
    class_class_curie: ClassVar[str] = "biolink:BehavioralExposure"
    class_name: ClassVar[str] = "behavioral exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BehavioralExposure

    id: Union[str, BehavioralExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BehavioralExposureId):
            self.id = BehavioralExposureId(self.id)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


@dataclass
class SocioeconomicExposure(Behavior):
    """
    A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g.
    poverty).
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.SocioeconomicExposure
    class_class_curie: ClassVar[str] = "biolink:SocioeconomicExposure"
    class_name: ClassVar[str] = "socioeconomic exposure"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SocioeconomicExposure

    id: Union[str, SocioeconomicExposureId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None
    has_attribute: Union[Union[dict, SocioeconomicAttribute], List[Union[dict, SocioeconomicAttribute]]] = None
    timepoint: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SocioeconomicExposureId):
            self.id = SocioeconomicExposureId(self.id)

        if self._is_empty(self.has_attribute):
            self.MissingRequiredField("has_attribute")
        self._normalize_inlined_as_dict(slot_name="has_attribute", slot_type=SocioeconomicAttribute, key_name="has attribute type", keyed=False)

        if self.timepoint is not None and not isinstance(self.timepoint, TimeType):
            self.timepoint = TimeType(self.timepoint)

        super().__post_init__(**kwargs)


class Outcome(YAMLRoot):
    """
    An entity that has the role of being the consequence of an exposure event. This is an abstract mixin grouping of
    various categories of possible biological or non-biological (e.g. clinical) outcomes.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Outcome
    class_class_curie: ClassVar[str] = "biolink:Outcome"
    class_name: ClassVar[str] = "outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Outcome


@dataclass
class PathologicalProcessOutcome(PathologicalProcess):
    """
    An outcome resulting from an exposure event which is the manifestation of a pathological process.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalProcessOutcome
    class_class_curie: ClassVar[str] = "biolink:PathologicalProcessOutcome"
    class_name: ClassVar[str] = "pathological process outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalProcessOutcome

    id: Union[str, PathologicalProcessOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathologicalProcessOutcomeId):
            self.id = PathologicalProcessOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class PathologicalAnatomicalOutcome(PathologicalAnatomicalStructure):
    """
    An outcome resulting from an exposure event which is the manifestation of an abnormal anatomical structure.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.PathologicalAnatomicalOutcome
    class_class_curie: ClassVar[str] = "biolink:PathologicalAnatomicalOutcome"
    class_name: ClassVar[str] = "pathological anatomical outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PathologicalAnatomicalOutcome

    id: Union[str, PathologicalAnatomicalOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PathologicalAnatomicalOutcomeId):
            self.id = PathologicalAnatomicalOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseOrPhenotypicFeatureOutcome(DiseaseOrPhenotypicFeature):
    """
    Physiological outcomes resulting from an exposure event which is the manifestation of a disease or other
    characteristic phenotype.
    """
    _inherited_slots: ClassVar[List[str]] = ["in_taxon"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureOutcome
    class_class_curie: ClassVar[str] = "biolink:DiseaseOrPhenotypicFeatureOutcome"
    class_name: ClassVar[str] = "disease or phenotypic feature outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureOutcome

    id: Union[str, DiseaseOrPhenotypicFeatureOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseOrPhenotypicFeatureOutcomeId):
            self.id = DiseaseOrPhenotypicFeatureOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class BehavioralOutcome(Behavior):
    """
    An outcome resulting from an exposure event which is the manifestation of human behavior.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.BehavioralOutcome
    class_class_curie: ClassVar[str] = "biolink:BehavioralOutcome"
    class_name: ClassVar[str] = "behavioral outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BehavioralOutcome

    id: Union[str, BehavioralOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BehavioralOutcomeId):
            self.id = BehavioralOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class HospitalizationOutcome(Hospitalization):
    """
    An outcome resulting from an exposure event which is the increased manifestation of acute (e.g. emergency room
    visit) or chronic (inpatient) hospitalization.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.HospitalizationOutcome
    class_class_curie: ClassVar[str] = "biolink:HospitalizationOutcome"
    class_name: ClassVar[str] = "hospitalization outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.HospitalizationOutcome

    id: Union[str, HospitalizationOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, HospitalizationOutcomeId):
            self.id = HospitalizationOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class MortalityOutcome(Death):
    """
    An outcome of death from resulting from an exposure event.
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.MortalityOutcome
    class_class_curie: ClassVar[str] = "biolink:MortalityOutcome"
    class_name: ClassVar[str] = "mortality outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MortalityOutcome

    id: Union[str, MortalityOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MortalityOutcomeId):
            self.id = MortalityOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class EpidemiologicalOutcome(BiologicalEntity):
    """
    An epidemiological outcome, such as societal disease burden, resulting from an exposure event.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EpidemiologicalOutcome
    class_class_curie: ClassVar[str] = "biolink:EpidemiologicalOutcome"
    class_name: ClassVar[str] = "epidemiological outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EpidemiologicalOutcome

    id: Union[str, EpidemiologicalOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EpidemiologicalOutcomeId):
            self.id = EpidemiologicalOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class SocioeconomicOutcome(Behavior):
    """
    An general social or economic outcome, such as healthcare costs, utilization, etc., resulting from an exposure
    event
    """
    _inherited_slots: ClassVar[List[str]] = ["has_input", "has_output", "enabled_by"]

    class_class_uri: ClassVar[URIRef] = BIOLINK.SocioeconomicOutcome
    class_class_curie: ClassVar[str] = "biolink:SocioeconomicOutcome"
    class_name: ClassVar[str] = "socioeconomic outcome"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SocioeconomicOutcome

    id: Union[str, SocioeconomicOutcomeId] = None
    category: Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SocioeconomicOutcomeId):
            self.id = SocioeconomicOutcomeId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Association(Entity):
    """
    A typed association between two entities, supported by evidence
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.Association
    class_class_curie: ClassVar[str] = "biolink:Association"
    class_name: ClassVar[str] = "association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.Association

    id: Union[str, AssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    negated: Optional[Union[bool, Bool]] = None
    qualifiers: Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]] = empty_list()
    publications: Optional[Union[Union[str, PublicationId], List[Union[str, PublicationId]]]] = empty_list()
    type: Optional[str] = None
    category: Optional[Union[Union[str, CategoryType], List[Union[str, CategoryType]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AssociationId):
            self.id = AssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NamedThingId):
            self.subject = NamedThingId(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NamedThingId):
            self.object = NamedThingId(self.object)

        if self._is_empty(self.relation):
            self.MissingRequiredField("relation")
        if not isinstance(self.relation, URIorCURIE):
            self.relation = URIorCURIE(self.relation)

        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        if not isinstance(self.qualifiers, list):
            self.qualifiers = [self.qualifiers] if self.qualifiers is not None else []
        self.qualifiers = [v if isinstance(v, OntologyClass) else OntologyClass(**as_dict(v)) for v in self.qualifiers]

        if not isinstance(self.publications, list):
            self.publications = [self.publications] if self.publications is not None else []
        self.publications = [v if isinstance(v, PublicationId) else PublicationId(v) for v in self.publications]

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        if not isinstance(self.category, list):
            self.category = [self.category] if self.category is not None else []
        self.category = [v if isinstance(v, CategoryType) else CategoryType(v) for v in self.category]

        super().__post_init__(**kwargs)


@dataclass
class ContributorAssociation(Association):
    """
    Any association between an entity (such as a publication) and various agents that contribute to its realisation
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ContributorAssociation
    class_class_curie: ClassVar[str] = "biolink:ContributorAssociation"
    class_name: ClassVar[str] = "contributor association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ContributorAssociation

    id: Union[str, ContributorAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, InformationContentEntityId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, AgentId] = None
    qualifiers: Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ContributorAssociationId):
            self.id = ContributorAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, InformationContentEntityId):
            self.subject = InformationContentEntityId(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AgentId):
            self.object = AgentId(self.object)

        if not isinstance(self.qualifiers, list):
            self.qualifiers = [self.qualifiers] if self.qualifiers is not None else []
        self.qualifiers = [v if isinstance(v, OntologyClass) else OntologyClass(**as_dict(v)) for v in self.qualifiers]

        super().__post_init__(**kwargs)


@dataclass
class GenotypeToGenotypePartAssociation(Association):
    """
    Any association between one genotype and a genotypic entity that is a sub-component of it
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeToGenotypePartAssociation
    class_class_curie: ClassVar[str] = "biolink:GenotypeToGenotypePartAssociation"
    class_name: ClassVar[str] = "genotype to genotype part association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeToGenotypePartAssociation

    id: Union[str, GenotypeToGenotypePartAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    subject: Union[str, GenotypeId] = None
    object: Union[str, GenotypeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeToGenotypePartAssociationId):
            self.id = GenotypeToGenotypePartAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenotypeId):
            self.subject = GenotypeId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GenotypeId):
            self.object = GenotypeId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GenotypeToGeneAssociation(Association):
    """
    Any association between a genotype and a gene. The genotype have have multiple variants in that gene or a single
    one. There is no assumption of cardinality
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeToGeneAssociation
    class_class_curie: ClassVar[str] = "biolink:GenotypeToGeneAssociation"
    class_name: ClassVar[str] = "genotype to gene association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeToGeneAssociation

    id: Union[str, GenotypeToGeneAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    subject: Union[str, GenotypeId] = None
    object: Union[str, GeneId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeToGeneAssociationId):
            self.id = GenotypeToGeneAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenotypeId):
            self.subject = GenotypeId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneId):
            self.object = GeneId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GenotypeToVariantAssociation(Association):
    """
    Any association between a genotype and a sequence variant.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeToVariantAssociation
    class_class_curie: ClassVar[str] = "biolink:GenotypeToVariantAssociation"
    class_name: ClassVar[str] = "genotype to variant association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeToVariantAssociation

    id: Union[str, GenotypeToVariantAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    subject: Union[str, GenotypeId] = None
    object: Union[str, SequenceVariantId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeToVariantAssociationId):
            self.id = GenotypeToVariantAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenotypeId):
            self.subject = GenotypeId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, SequenceVariantId):
            self.object = SequenceVariantId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GeneToGeneAssociation(Association):
    """
    abstract parent class for different kinds of gene-gene or gene product to gene product relationships. Includes
    homology and interaction.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToGeneAssociation"
    class_name: ClassVar[str] = "gene to gene association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneAssociation

    id: Union[str, GeneToGeneAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    object: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneOrGeneProduct):
            self.object = GeneOrGeneProduct(**as_dict(self.object))

        super().__post_init__(**kwargs)


@dataclass
class GeneToGeneHomologyAssociation(GeneToGeneAssociation):
    """
    A homology association between two genes. May be orthology (in which case the species of subject and object should
    differ) or paralogy (in which case the species may be the same)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneHomologyAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToGeneHomologyAssociation"
    class_name: ClassVar[str] = "gene to gene homology association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneHomologyAssociation

    id: Union[str, GeneToGeneHomologyAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    object: Union[dict, GeneOrGeneProduct] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToGeneHomologyAssociationId):
            self.id = GeneToGeneHomologyAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class GeneExpressionMixin(YAMLRoot):
    """
    Observed gene expression intensity, context (site, stage) and associated phenotypic status within which the
    expression occurs.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneExpressionMixin
    class_class_curie: ClassVar[str] = "biolink:GeneExpressionMixin"
    class_name: ClassVar[str] = "gene expression mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneExpressionMixin

    quantifier_qualifier: Optional[Union[dict, OntologyClass]] = None
    expression_site: Optional[Union[str, AnatomicalEntityId]] = None
    stage_qualifier: Optional[Union[str, LifeStageId]] = None
    phenotypic_state: Optional[Union[str, DiseaseOrPhenotypicFeatureId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.quantifier_qualifier is not None and not isinstance(self.quantifier_qualifier, OntologyClass):
            self.quantifier_qualifier = OntologyClass()

        if self.expression_site is not None and not isinstance(self.expression_site, AnatomicalEntityId):
            self.expression_site = AnatomicalEntityId(self.expression_site)

        if self.stage_qualifier is not None and not isinstance(self.stage_qualifier, LifeStageId):
            self.stage_qualifier = LifeStageId(self.stage_qualifier)

        if self.phenotypic_state is not None and not isinstance(self.phenotypic_state, DiseaseOrPhenotypicFeatureId):
            self.phenotypic_state = DiseaseOrPhenotypicFeatureId(self.phenotypic_state)

        super().__post_init__(**kwargs)


@dataclass
class GeneToGeneCoexpressionAssociation(GeneToGeneAssociation):
    """
    Indicates that two genes are co-expressed, generally under the same conditions.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneCoexpressionAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToGeneCoexpressionAssociation"
    class_name: ClassVar[str] = "gene to gene coexpression association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneCoexpressionAssociation

    id: Union[str, GeneToGeneCoexpressionAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    object: Union[dict, GeneOrGeneProduct] = None
    predicate: Union[str, PredicateType] = None
    quantifier_qualifier: Optional[Union[dict, OntologyClass]] = None
    expression_site: Optional[Union[str, AnatomicalEntityId]] = None
    stage_qualifier: Optional[Union[str, LifeStageId]] = None
    phenotypic_state: Optional[Union[str, DiseaseOrPhenotypicFeatureId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToGeneCoexpressionAssociationId):
            self.id = GeneToGeneCoexpressionAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self.quantifier_qualifier is not None and not isinstance(self.quantifier_qualifier, OntologyClass):
            self.quantifier_qualifier = OntologyClass()

        if self.expression_site is not None and not isinstance(self.expression_site, AnatomicalEntityId):
            self.expression_site = AnatomicalEntityId(self.expression_site)

        if self.stage_qualifier is not None and not isinstance(self.stage_qualifier, LifeStageId):
            self.stage_qualifier = LifeStageId(self.stage_qualifier)

        if self.phenotypic_state is not None and not isinstance(self.phenotypic_state, DiseaseOrPhenotypicFeatureId):
            self.phenotypic_state = DiseaseOrPhenotypicFeatureId(self.phenotypic_state)

        super().__post_init__(**kwargs)


@dataclass
class PairwiseGeneToGeneInteraction(GeneToGeneAssociation):
    """
    An interaction between two genes or two gene products. May be physical (e.g. protein binding) or genetic (between
    genes). May be symmetric (e.g. protein interaction) or directed (e.g. phosphorylation)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PairwiseGeneToGeneInteraction
    class_class_curie: ClassVar[str] = "biolink:PairwiseGeneToGeneInteraction"
    class_name: ClassVar[str] = "pairwise gene to gene interaction"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PairwiseGeneToGeneInteraction

    id: Union[str, PairwiseGeneToGeneInteractionId] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    object: Union[dict, GeneOrGeneProduct] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PairwiseGeneToGeneInteractionId):
            self.id = PairwiseGeneToGeneInteractionId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.relation):
            self.MissingRequiredField("relation")
        if not isinstance(self.relation, URIorCURIE):
            self.relation = URIorCURIE(self.relation)

        super().__post_init__(**kwargs)


@dataclass
class PairwiseMolecularInteraction(PairwiseGeneToGeneInteraction):
    """
    An interaction at the molecular level between two physical entities
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PairwiseMolecularInteraction
    class_class_curie: ClassVar[str] = "biolink:PairwiseMolecularInteraction"
    class_name: ClassVar[str] = "pairwise molecular interaction"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PairwiseMolecularInteraction

    id: Union[str, PairwiseMolecularInteractionId] = None
    subject: Union[str, MolecularEntityId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, MolecularEntityId] = None
    interacting_molecules_category: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PairwiseMolecularInteractionId):
            self.id = PairwiseMolecularInteractionId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, MolecularEntityId):
            self.subject = MolecularEntityId(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.relation):
            self.MissingRequiredField("relation")
        if not isinstance(self.relation, URIorCURIE):
            self.relation = URIorCURIE(self.relation)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, MolecularEntityId):
            self.object = MolecularEntityId(self.object)

        if self.interacting_molecules_category is not None and not isinstance(self.interacting_molecules_category, OntologyClass):
            self.interacting_molecules_category = OntologyClass()

        super().__post_init__(**kwargs)


@dataclass
class CellLineToEntityAssociationMixin(YAMLRoot):
    """
    An relationship between a cell line and another entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.CellLineToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:CellLineToEntityAssociationMixin"
    class_name: ClassVar[str] = "cell line to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CellLineToEntityAssociationMixin

    subject: Union[str, CellLineId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, CellLineId):
            self.subject = CellLineId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class CellLineToDiseaseOrPhenotypicFeatureAssociation(Association):
    """
    An relationship between a cell line and a disease or a phenotype, where the cell line is derived from an
    individual with that disease or phenotype.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.CellLineToDiseaseOrPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:CellLineToDiseaseOrPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "cell line to disease or phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CellLineToDiseaseOrPhenotypicFeatureAssociation

    id: Union[str, CellLineToDiseaseOrPhenotypicFeatureAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, DiseaseOrPhenotypicFeatureId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellLineToDiseaseOrPhenotypicFeatureAssociationId):
            self.id = CellLineToDiseaseOrPhenotypicFeatureAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, DiseaseOrPhenotypicFeatureId):
            self.subject = DiseaseOrPhenotypicFeatureId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class MolecularEntityToEntityAssociationMixin(YAMLRoot):
    """
    An interaction between a molecular entity and another entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MolecularEntityToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:MolecularEntityToEntityAssociationMixin"
    class_name: ClassVar[str] = "molecular entity to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MolecularEntityToEntityAssociationMixin

    subject: Union[str, MolecularEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, MolecularEntityId):
            self.subject = MolecularEntityId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class DrugToEntityAssociationMixin(MolecularEntityToEntityAssociationMixin):
    """
    An interaction between a drug and another entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DrugToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:DrugToEntityAssociationMixin"
    class_name: ClassVar[str] = "drug to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DrugToEntityAssociationMixin

    subject: Union[str, DrugId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, DrugId):
            self.subject = DrugId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class ChemicalToEntityAssociationMixin(MolecularEntityToEntityAssociationMixin):
    """
    An interaction between a chemical entity and another entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:ChemicalToEntityAssociationMixin"
    class_name: ClassVar[str] = "chemical to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalToEntityAssociationMixin

    subject: Union[str, ChemicalSubstanceId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, ChemicalSubstanceId):
            self.subject = ChemicalSubstanceId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class CaseToEntityAssociationMixin(YAMLRoot):
    """
    An abstract association for use where the case is the subject
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.CaseToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:CaseToEntityAssociationMixin"
    class_name: ClassVar[str] = "case to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CaseToEntityAssociationMixin

    subject: Union[str, CaseId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, CaseId):
            self.subject = CaseId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class ChemicalToChemicalAssociation(Association):
    """
    A relationship between two chemical entities. This can encompass actual interactions as well as temporal causal
    edges, e.g. one chemical converted to another.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalToChemicalAssociation
    class_class_curie: ClassVar[str] = "biolink:ChemicalToChemicalAssociation"
    class_name: ClassVar[str] = "chemical to chemical association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalToChemicalAssociation

    id: Union[str, ChemicalToChemicalAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, ChemicalSubstanceId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalToChemicalAssociationId):
            self.id = ChemicalToChemicalAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, ChemicalSubstanceId):
            self.object = ChemicalSubstanceId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class ChemicalToChemicalDerivationAssociation(ChemicalToChemicalAssociation):
    """
    A causal relationship between two chemical entities, where the subject represents the upstream entity and the
    object represents the downstream. For any such association there is an implicit reaction:
    IF
    R has-input C1 AND
    R has-output C2 AND
    R enabled-by P AND
    R type Reaction
    THEN
    C1 derives-into C2 <<catalyst qualifier P>>
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalToChemicalDerivationAssociation
    class_class_curie: ClassVar[str] = "biolink:ChemicalToChemicalDerivationAssociation"
    class_name: ClassVar[str] = "chemical to chemical derivation association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalToChemicalDerivationAssociation

    id: Union[str, ChemicalToChemicalDerivationAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, ChemicalSubstanceId] = None
    object: Union[str, ChemicalSubstanceId] = None
    predicate: Union[str, PredicateType] = None
    catalyst_qualifier: Optional[Union[Union[dict, MacromolecularMachineMixin], List[Union[dict, MacromolecularMachineMixin]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalToChemicalDerivationAssociationId):
            self.id = ChemicalToChemicalDerivationAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, ChemicalSubstanceId):
            self.subject = ChemicalSubstanceId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, ChemicalSubstanceId):
            self.object = ChemicalSubstanceId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if not isinstance(self.catalyst_qualifier, list):
            self.catalyst_qualifier = [self.catalyst_qualifier] if self.catalyst_qualifier is not None else []
        self.catalyst_qualifier = [v if isinstance(v, MacromolecularMachineMixin) else MacromolecularMachineMixin(**as_dict(v)) for v in self.catalyst_qualifier]

        super().__post_init__(**kwargs)


@dataclass
class ChemicalToDiseaseOrPhenotypicFeatureAssociation(Association):
    """
    An interaction between a chemical entity and a phenotype or disease, where the presence of the chemical gives rise
    to or exacerbates the phenotype.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalToDiseaseOrPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:ChemicalToDiseaseOrPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "chemical to disease or phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalToDiseaseOrPhenotypicFeatureAssociation

    id: Union[str, ChemicalToDiseaseOrPhenotypicFeatureAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, DiseaseOrPhenotypicFeatureId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalToDiseaseOrPhenotypicFeatureAssociationId):
            self.id = ChemicalToDiseaseOrPhenotypicFeatureAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, DiseaseOrPhenotypicFeatureId):
            self.object = DiseaseOrPhenotypicFeatureId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class ChemicalToPathwayAssociation(Association):
    """
    An interaction between a chemical entity and a biological process or pathway.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalToPathwayAssociation
    class_class_curie: ClassVar[str] = "biolink:ChemicalToPathwayAssociation"
    class_name: ClassVar[str] = "chemical to pathway association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalToPathwayAssociation

    id: Union[str, ChemicalToPathwayAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, PathwayId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalToPathwayAssociationId):
            self.id = ChemicalToPathwayAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, PathwayId):
            self.object = PathwayId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class ChemicalToGeneAssociation(Association):
    """
    An interaction between a chemical entity and a gene or gene product.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ChemicalToGeneAssociation
    class_class_curie: ClassVar[str] = "biolink:ChemicalToGeneAssociation"
    class_name: ClassVar[str] = "chemical to gene association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ChemicalToGeneAssociation

    id: Union[str, ChemicalToGeneAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ChemicalToGeneAssociationId):
            self.id = ChemicalToGeneAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneOrGeneProduct):
            self.object = GeneOrGeneProduct(**as_dict(self.object))

        super().__post_init__(**kwargs)


@dataclass
class DrugToGeneAssociation(Association):
    """
    An interaction between a drug and a gene or gene product.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DrugToGeneAssociation
    class_class_curie: ClassVar[str] = "biolink:DrugToGeneAssociation"
    class_name: ClassVar[str] = "drug to gene association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DrugToGeneAssociation

    id: Union[str, DrugToGeneAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DrugToGeneAssociationId):
            self.id = DrugToGeneAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneOrGeneProduct):
            self.object = GeneOrGeneProduct(**as_dict(self.object))

        super().__post_init__(**kwargs)


@dataclass
class MaterialSampleToEntityAssociationMixin(YAMLRoot):
    """
    An association between a material sample and something.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MaterialSampleToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:MaterialSampleToEntityAssociationMixin"
    class_name: ClassVar[str] = "material sample to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MaterialSampleToEntityAssociationMixin

    subject: Union[str, MaterialSampleId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, MaterialSampleId):
            self.subject = MaterialSampleId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class MaterialSampleDerivationAssociation(Association):
    """
    An association between a material sample and the material entity from which it is derived.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MaterialSampleDerivationAssociation
    class_class_curie: ClassVar[str] = "biolink:MaterialSampleDerivationAssociation"
    class_name: ClassVar[str] = "material sample derivation association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MaterialSampleDerivationAssociation

    id: Union[str, MaterialSampleDerivationAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, MaterialSampleId] = None
    object: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MaterialSampleDerivationAssociationId):
            self.id = MaterialSampleDerivationAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, MaterialSampleId):
            self.subject = MaterialSampleId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NamedThingId):
            self.object = NamedThingId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class MaterialSampleToDiseaseOrPhenotypicFeatureAssociation(Association):
    """
    An association between a material sample and a disease or phenotype.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MaterialSampleToDiseaseOrPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:MaterialSampleToDiseaseOrPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "material sample to disease or phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MaterialSampleToDiseaseOrPhenotypicFeatureAssociation

    id: Union[str, MaterialSampleToDiseaseOrPhenotypicFeatureAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MaterialSampleToDiseaseOrPhenotypicFeatureAssociationId):
            self.id = MaterialSampleToDiseaseOrPhenotypicFeatureAssociationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseToEntityAssociationMixin(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:DiseaseToEntityAssociationMixin"
    class_name: ClassVar[str] = "disease to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseToEntityAssociationMixin

    subject: Union[str, DiseaseId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, DiseaseId):
            self.subject = DiseaseId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class EntityToExposureEventAssociationMixin(YAMLRoot):
    """
    An association between some entity and an exposure event.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EntityToExposureEventAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:EntityToExposureEventAssociationMixin"
    class_name: ClassVar[str] = "entity to exposure event association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EntityToExposureEventAssociationMixin

    object: Union[dict, ExposureEvent] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, ExposureEvent):
            self.object = ExposureEvent(**as_dict(self.object))

        super().__post_init__(**kwargs)


@dataclass
class DiseaseToExposureEventAssociation(Association):
    """
    An association between an exposure event and a disease.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseToExposureEventAssociation
    class_class_curie: ClassVar[str] = "biolink:DiseaseToExposureEventAssociation"
    class_name: ClassVar[str] = "disease to exposure event association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseToExposureEventAssociation

    id: Union[str, DiseaseToExposureEventAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseToExposureEventAssociationId):
            self.id = DiseaseToExposureEventAssociationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ExposureEventToEntityAssociationMixin(YAMLRoot):
    """
    An association between some exposure event and some entity.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ExposureEventToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:ExposureEventToEntityAssociationMixin"
    class_name: ClassVar[str] = "exposure event to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ExposureEventToEntityAssociationMixin

    subject: Union[dict, ExposureEvent] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, ExposureEvent):
            self.subject = ExposureEvent(**as_dict(self.subject))

        super().__post_init__(**kwargs)


@dataclass
class EntityToOutcomeAssociationMixin(YAMLRoot):
    """
    An association between some entity and an outcome
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EntityToOutcomeAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:EntityToOutcomeAssociationMixin"
    class_name: ClassVar[str] = "entity to outcome association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EntityToOutcomeAssociationMixin

    object: Union[dict, Outcome] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, Outcome):
            self.object = Outcome()

        super().__post_init__(**kwargs)


@dataclass
class ExposureEventToOutcomeAssociation(Association):
    """
    An association between an exposure event and an outcome.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ExposureEventToOutcomeAssociation
    class_class_curie: ClassVar[str] = "biolink:ExposureEventToOutcomeAssociation"
    class_name: ClassVar[str] = "exposure event to outcome association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ExposureEventToOutcomeAssociation

    id: Union[str, ExposureEventToOutcomeAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    has_population_context: Optional[Union[str, PopulationOfIndividualOrganismsId]] = None
    has_temporal_context: Optional[Union[str, TimeType]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExposureEventToOutcomeAssociationId):
            self.id = ExposureEventToOutcomeAssociationId(self.id)

        if self.has_population_context is not None and not isinstance(self.has_population_context, PopulationOfIndividualOrganismsId):
            self.has_population_context = PopulationOfIndividualOrganismsId(self.has_population_context)

        if self.has_temporal_context is not None and not isinstance(self.has_temporal_context, TimeType):
            self.has_temporal_context = TimeType(self.has_temporal_context)

        super().__post_init__(**kwargs)


@dataclass
class FrequencyQualifierMixin(YAMLRoot):
    """
    Qualifier for frequency type associations
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.FrequencyQualifierMixin
    class_class_curie: ClassVar[str] = "biolink:FrequencyQualifierMixin"
    class_name: ClassVar[str] = "frequency qualifier mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.FrequencyQualifierMixin

    frequency_qualifier: Optional[Union[str, FrequencyValue]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.frequency_qualifier is not None and not isinstance(self.frequency_qualifier, FrequencyValue):
            self.frequency_qualifier = FrequencyValue(self.frequency_qualifier)

        super().__post_init__(**kwargs)


@dataclass
class EntityToFeatureOrDiseaseQualifiersMixin(FrequencyQualifierMixin):
    """
    Qualifiers for entity to disease or phenotype associations.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EntityToFeatureOrDiseaseQualifiersMixin
    class_class_curie: ClassVar[str] = "biolink:EntityToFeatureOrDiseaseQualifiersMixin"
    class_name: ClassVar[str] = "entity to feature or disease qualifiers mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EntityToFeatureOrDiseaseQualifiersMixin

    severity_qualifier: Optional[Union[dict, SeverityValue]] = None
    onset_qualifier: Optional[Union[dict, Onset]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.severity_qualifier is not None and not isinstance(self.severity_qualifier, SeverityValue):
            self.severity_qualifier = SeverityValue(**as_dict(self.severity_qualifier))

        if self.onset_qualifier is not None and not isinstance(self.onset_qualifier, Onset):
            self.onset_qualifier = Onset(**as_dict(self.onset_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class EntityToPhenotypicFeatureAssociationMixin(EntityToFeatureOrDiseaseQualifiersMixin):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EntityToPhenotypicFeatureAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:EntityToPhenotypicFeatureAssociationMixin"
    class_name: ClassVar[str] = "entity to phenotypic feature association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EntityToPhenotypicFeatureAssociationMixin

    object: Union[str, PhenotypicFeatureId] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None
    description: Optional[Union[str, NarrativeText]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, PhenotypicFeatureId):
            self.object = PhenotypicFeatureId(self.object)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        if self.description is not None and not isinstance(self.description, NarrativeText):
            self.description = NarrativeText(self.description)

        super().__post_init__(**kwargs)


@dataclass
class EntityToDiseaseAssociationMixin(EntityToFeatureOrDiseaseQualifiersMixin):
    """
    mixin class for any association whose object (target node) is a disease
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EntityToDiseaseAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:EntityToDiseaseAssociationMixin"
    class_name: ClassVar[str] = "entity to disease association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EntityToDiseaseAssociationMixin

    object: Union[str, DiseaseId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, DiseaseId):
            self.object = DiseaseId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseOrPhenotypicFeatureToEntityAssociationMixin(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:DiseaseOrPhenotypicFeatureToEntityAssociationMixin"
    class_name: ClassVar[str] = "disease or phenotypic feature to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureToEntityAssociationMixin

    subject: Union[str, DiseaseOrPhenotypicFeatureId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, DiseaseOrPhenotypicFeatureId):
            self.subject = DiseaseOrPhenotypicFeatureId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseOrPhenotypicFeatureAssociationToLocationAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureAssociationToLocationAssociation
    class_class_curie: ClassVar[str] = "biolink:DiseaseOrPhenotypicFeatureAssociationToLocationAssociation"
    class_name: ClassVar[str] = "disease or phenotypic feature association to location association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureAssociationToLocationAssociation

    id: Union[str, DiseaseOrPhenotypicFeatureAssociationToLocationAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, AnatomicalEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseOrPhenotypicFeatureAssociationToLocationAssociationId):
            self.id = DiseaseOrPhenotypicFeatureAssociationToLocationAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AnatomicalEntityId):
            self.object = AnatomicalEntityId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class DiseaseOrPhenotypicFeatureToLocationAssociation(Association):
    """
    An association between either a disease or a phenotypic feature and an anatomical entity, where the
    disease/feature manifests in that site.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureToLocationAssociation
    class_class_curie: ClassVar[str] = "biolink:DiseaseOrPhenotypicFeatureToLocationAssociation"
    class_name: ClassVar[str] = "disease or phenotypic feature to location association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseOrPhenotypicFeatureToLocationAssociation

    id: Union[str, DiseaseOrPhenotypicFeatureToLocationAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, AnatomicalEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseOrPhenotypicFeatureToLocationAssociationId):
            self.id = DiseaseOrPhenotypicFeatureToLocationAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AnatomicalEntityId):
            self.object = AnatomicalEntityId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class EntityToDiseaseOrPhenotypicFeatureAssociationMixin(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.EntityToDiseaseOrPhenotypicFeatureAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:EntityToDiseaseOrPhenotypicFeatureAssociationMixin"
    class_name: ClassVar[str] = "entity to disease or phenotypic feature association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.EntityToDiseaseOrPhenotypicFeatureAssociationMixin

    object: Union[str, DiseaseOrPhenotypicFeatureId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, DiseaseOrPhenotypicFeatureId):
            self.object = DiseaseOrPhenotypicFeatureId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GenotypeToEntityAssociationMixin(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:GenotypeToEntityAssociationMixin"
    class_name: ClassVar[str] = "genotype to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeToEntityAssociationMixin

    subject: Union[str, GenotypeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenotypeId):
            self.subject = GenotypeId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class GenotypeToPhenotypicFeatureAssociation(Association):
    """
    Any association between one genotype and a phenotypic feature, where having the genotype confers the phenotype,
    either in isolation or through environment
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeToPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:GenotypeToPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "genotype to phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeToPhenotypicFeatureAssociation

    id: Union[str, GenotypeToPhenotypicFeatureAssociationId] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    subject: Union[str, GenotypeId] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeToPhenotypicFeatureAssociationId):
            self.id = GenotypeToPhenotypicFeatureAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenotypeId):
            self.subject = GenotypeId(self.subject)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class ExposureEventToPhenotypicFeatureAssociation(Association):
    """
    Any association between an environment and a phenotypic feature, where being in the environment influences the
    phenotype.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ExposureEventToPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:ExposureEventToPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "exposure event to phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ExposureEventToPhenotypicFeatureAssociation

    id: Union[str, ExposureEventToPhenotypicFeatureAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, ExposureEvent] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExposureEventToPhenotypicFeatureAssociationId):
            self.id = ExposureEventToPhenotypicFeatureAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, ExposureEvent):
            self.subject = ExposureEvent(**as_dict(self.subject))

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class DiseaseToPhenotypicFeatureAssociation(Association):
    """
    An association between a disease and a phenotypic feature in which the phenotypic feature is associated with the
    disease in some way.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.DiseaseToPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:DiseaseToPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "disease to phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.DiseaseToPhenotypicFeatureAssociation

    id: Union[str, DiseaseToPhenotypicFeatureAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DiseaseToPhenotypicFeatureAssociationId):
            self.id = DiseaseToPhenotypicFeatureAssociationId(self.id)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class CaseToPhenotypicFeatureAssociation(Association):
    """
    An association between a case (e.g. individual patient) and a phenotypic feature in which the individual has or
    has had the phenotype.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.CaseToPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:CaseToPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "case to phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CaseToPhenotypicFeatureAssociation

    id: Union[str, CaseToPhenotypicFeatureAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CaseToPhenotypicFeatureAssociationId):
            self.id = CaseToPhenotypicFeatureAssociationId(self.id)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class BehaviorToBehavioralFeatureAssociation(Association):
    """
    An association between an aggregate behavior and a behavioral feature manifested by the individual exhibited or
    has exhibited the behavior.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.BehaviorToBehavioralFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:BehaviorToBehavioralFeatureAssociation"
    class_name: ClassVar[str] = "behavior to behavioral feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.BehaviorToBehavioralFeatureAssociation

    id: Union[str, BehaviorToBehavioralFeatureAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, BehaviorId] = None
    object: Union[str, BehavioralFeatureId] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BehaviorToBehavioralFeatureAssociationId):
            self.id = BehaviorToBehavioralFeatureAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, BehaviorId):
            self.subject = BehaviorId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, BehavioralFeatureId):
            self.object = BehavioralFeatureId(self.object)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class GeneToEntityAssociationMixin(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:GeneToEntityAssociationMixin"
    class_name: ClassVar[str] = "gene to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToEntityAssociationMixin

    subject: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        super().__post_init__(**kwargs)


@dataclass
class VariantToEntityAssociationMixin(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:VariantToEntityAssociationMixin"
    class_name: ClassVar[str] = "variant to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantToEntityAssociationMixin

    subject: Union[str, SequenceVariantId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, SequenceVariantId):
            self.subject = SequenceVariantId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class GeneToPhenotypicFeatureAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "gene to phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToPhenotypicFeatureAssociation

    id: Union[str, GeneToPhenotypicFeatureAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToPhenotypicFeatureAssociationId):
            self.id = GeneToPhenotypicFeatureAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class GeneToDiseaseAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToDiseaseAssociation"
    class_name: ClassVar[str] = "gene to disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToDiseaseAssociation

    id: Union[str, GeneToDiseaseAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToDiseaseAssociationId):
            self.id = GeneToDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        super().__post_init__(**kwargs)


@dataclass
class VariantToGeneAssociation(Association):
    """
    An association between a variant and a gene, where the variant has a genetic association with the gene (i.e. is in
    linkage disequilibrium)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantToGeneAssociation
    class_class_curie: ClassVar[str] = "biolink:VariantToGeneAssociation"
    class_name: ClassVar[str] = "variant to gene association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantToGeneAssociation

    id: Union[str, VariantToGeneAssociationId] = None
    subject: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, GeneId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VariantToGeneAssociationId):
            self.id = VariantToGeneAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneId):
            self.object = GeneId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class VariantToGeneExpressionAssociation(VariantToGeneAssociation):
    """
    An association between a variant and expression of a gene (i.e. e-QTL)
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantToGeneExpressionAssociation
    class_class_curie: ClassVar[str] = "biolink:VariantToGeneExpressionAssociation"
    class_name: ClassVar[str] = "variant to gene expression association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantToGeneExpressionAssociation

    id: Union[str, VariantToGeneExpressionAssociationId] = None
    subject: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    object: Union[str, GeneId] = None
    predicate: Union[str, PredicateType] = None
    quantifier_qualifier: Optional[Union[dict, OntologyClass]] = None
    expression_site: Optional[Union[str, AnatomicalEntityId]] = None
    stage_qualifier: Optional[Union[str, LifeStageId]] = None
    phenotypic_state: Optional[Union[str, DiseaseOrPhenotypicFeatureId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VariantToGeneExpressionAssociationId):
            self.id = VariantToGeneExpressionAssociationId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self.quantifier_qualifier is not None and not isinstance(self.quantifier_qualifier, OntologyClass):
            self.quantifier_qualifier = OntologyClass()

        if self.expression_site is not None and not isinstance(self.expression_site, AnatomicalEntityId):
            self.expression_site = AnatomicalEntityId(self.expression_site)

        if self.stage_qualifier is not None and not isinstance(self.stage_qualifier, LifeStageId):
            self.stage_qualifier = LifeStageId(self.stage_qualifier)

        if self.phenotypic_state is not None and not isinstance(self.phenotypic_state, DiseaseOrPhenotypicFeatureId):
            self.phenotypic_state = DiseaseOrPhenotypicFeatureId(self.phenotypic_state)

        super().__post_init__(**kwargs)


@dataclass
class VariantToPopulationAssociation(Association):
    """
    An association between a variant and a population, where the variant has particular frequency in the population
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantToPopulationAssociation
    class_class_curie: ClassVar[str] = "biolink:VariantToPopulationAssociation"
    class_name: ClassVar[str] = "variant to population association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantToPopulationAssociation

    id: Union[str, VariantToPopulationAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, SequenceVariantId] = None
    object: Union[str, PopulationOfIndividualOrganismsId] = None
    has_quotient: Optional[float] = None
    has_count: Optional[int] = None
    has_total: Optional[int] = None
    has_percentage: Optional[float] = None
    frequency_qualifier: Optional[Union[str, FrequencyValue]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VariantToPopulationAssociationId):
            self.id = VariantToPopulationAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, SequenceVariantId):
            self.subject = SequenceVariantId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, PopulationOfIndividualOrganismsId):
            self.object = PopulationOfIndividualOrganismsId(self.object)

        if self.has_quotient is not None and not isinstance(self.has_quotient, float):
            self.has_quotient = float(self.has_quotient)

        if self.has_count is not None and not isinstance(self.has_count, int):
            self.has_count = int(self.has_count)

        if self.has_total is not None and not isinstance(self.has_total, int):
            self.has_total = int(self.has_total)

        if self.has_percentage is not None and not isinstance(self.has_percentage, float):
            self.has_percentage = float(self.has_percentage)

        if self.frequency_qualifier is not None and not isinstance(self.frequency_qualifier, FrequencyValue):
            self.frequency_qualifier = FrequencyValue(self.frequency_qualifier)

        super().__post_init__(**kwargs)


@dataclass
class PopulationToPopulationAssociation(Association):
    """
    An association between a two populations
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.PopulationToPopulationAssociation
    class_class_curie: ClassVar[str] = "biolink:PopulationToPopulationAssociation"
    class_name: ClassVar[str] = "population to population association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.PopulationToPopulationAssociation

    id: Union[str, PopulationToPopulationAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, PopulationOfIndividualOrganismsId] = None
    object: Union[str, PopulationOfIndividualOrganismsId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PopulationToPopulationAssociationId):
            self.id = PopulationToPopulationAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, PopulationOfIndividualOrganismsId):
            self.subject = PopulationOfIndividualOrganismsId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, PopulationOfIndividualOrganismsId):
            self.object = PopulationOfIndividualOrganismsId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class VariantToPhenotypicFeatureAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantToPhenotypicFeatureAssociation
    class_class_curie: ClassVar[str] = "biolink:VariantToPhenotypicFeatureAssociation"
    class_name: ClassVar[str] = "variant to phenotypic feature association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantToPhenotypicFeatureAssociation

    id: Union[str, VariantToPhenotypicFeatureAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, SequenceVariantId] = None
    sex_qualifier: Optional[Union[dict, BiologicalSex]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VariantToPhenotypicFeatureAssociationId):
            self.id = VariantToPhenotypicFeatureAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, SequenceVariantId):
            self.subject = SequenceVariantId(self.subject)

        if self.sex_qualifier is not None and not isinstance(self.sex_qualifier, BiologicalSex):
            self.sex_qualifier = BiologicalSex(**as_dict(self.sex_qualifier))

        super().__post_init__(**kwargs)


@dataclass
class VariantToDiseaseAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantToDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:VariantToDiseaseAssociation"
    class_name: ClassVar[str] = "variant to disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantToDiseaseAssociation

    id: Union[str, VariantToDiseaseAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VariantToDiseaseAssociationId):
            self.id = VariantToDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NamedThingId):
            self.subject = NamedThingId(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NamedThingId):
            self.object = NamedThingId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GenotypeToDiseaseAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeToDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:GenotypeToDiseaseAssociation"
    class_name: ClassVar[str] = "genotype to disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeToDiseaseAssociation

    id: Union[str, GenotypeToDiseaseAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeToDiseaseAssociationId):
            self.id = GenotypeToDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NamedThingId):
            self.subject = NamedThingId(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NamedThingId):
            self.object = NamedThingId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class ModelToDiseaseAssociationMixin(YAMLRoot):
    """
    This mixin is used for any association class for which the subject (source node) plays the role of a 'model', in
    that it recapitulates some features of the disease in a way that is useful for studying the disease outside a
    patient carrying the disease
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ModelToDiseaseAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:ModelToDiseaseAssociationMixin"
    class_name: ClassVar[str] = "model to disease association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ModelToDiseaseAssociationMixin

    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NamedThingId):
            self.subject = NamedThingId(self.subject)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class GeneAsAModelOfDiseaseAssociation(GeneToDiseaseAssociation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneAsAModelOfDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneAsAModelOfDiseaseAssociation"
    class_name: ClassVar[str] = "gene as a model of disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneAsAModelOfDiseaseAssociation

    id: Union[str, GeneAsAModelOfDiseaseAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneAsAModelOfDiseaseAssociationId):
            self.id = GeneAsAModelOfDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        super().__post_init__(**kwargs)


@dataclass
class VariantAsAModelOfDiseaseAssociation(VariantToDiseaseAssociation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.VariantAsAModelOfDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:VariantAsAModelOfDiseaseAssociation"
    class_name: ClassVar[str] = "variant as a model of disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.VariantAsAModelOfDiseaseAssociation

    id: Union[str, VariantAsAModelOfDiseaseAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    subject: Union[str, SequenceVariantId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, VariantAsAModelOfDiseaseAssociationId):
            self.id = VariantAsAModelOfDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, SequenceVariantId):
            self.subject = SequenceVariantId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class GenotypeAsAModelOfDiseaseAssociation(GenotypeToDiseaseAssociation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenotypeAsAModelOfDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:GenotypeAsAModelOfDiseaseAssociation"
    class_name: ClassVar[str] = "genotype as a model of disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenotypeAsAModelOfDiseaseAssociation

    id: Union[str, GenotypeAsAModelOfDiseaseAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    subject: Union[str, GenotypeId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenotypeAsAModelOfDiseaseAssociationId):
            self.id = GenotypeAsAModelOfDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenotypeId):
            self.subject = GenotypeId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class CellLineAsAModelOfDiseaseAssociation(CellLineToDiseaseOrPhenotypicFeatureAssociation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.CellLineAsAModelOfDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:CellLineAsAModelOfDiseaseAssociation"
    class_name: ClassVar[str] = "cell line as a model of disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.CellLineAsAModelOfDiseaseAssociation

    id: Union[str, CellLineAsAModelOfDiseaseAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, CellLineId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CellLineAsAModelOfDiseaseAssociationId):
            self.id = CellLineAsAModelOfDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, CellLineId):
            self.subject = CellLineId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class OrganismalEntityAsAModelOfDiseaseAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismalEntityAsAModelOfDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:OrganismalEntityAsAModelOfDiseaseAssociation"
    class_name: ClassVar[str] = "organismal entity as a model of disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismalEntityAsAModelOfDiseaseAssociation

    id: Union[str, OrganismalEntityAsAModelOfDiseaseAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, OrganismalEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganismalEntityAsAModelOfDiseaseAssociationId):
            self.id = OrganismalEntityAsAModelOfDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, OrganismalEntityId):
            self.subject = OrganismalEntityId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class GeneHasVariantThatContributesToDiseaseAssociation(GeneToDiseaseAssociation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneHasVariantThatContributesToDiseaseAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneHasVariantThatContributesToDiseaseAssociation"
    class_name: ClassVar[str] = "gene has variant that contributes to disease association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneHasVariantThatContributesToDiseaseAssociation

    id: Union[str, GeneHasVariantThatContributesToDiseaseAssociationId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    sequence_variant_qualifier: Optional[Union[str, SequenceVariantId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneHasVariantThatContributesToDiseaseAssociationId):
            self.id = GeneHasVariantThatContributesToDiseaseAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        if self.sequence_variant_qualifier is not None and not isinstance(self.sequence_variant_qualifier, SequenceVariantId):
            self.sequence_variant_qualifier = SequenceVariantId(self.sequence_variant_qualifier)

        super().__post_init__(**kwargs)


@dataclass
class GeneToExpressionSiteAssociation(Association):
    """
    An association between a gene and an expression site, possibly qualified by stage/timing info.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToExpressionSiteAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToExpressionSiteAssociation"
    class_name: ClassVar[str] = "gene to expression site association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToExpressionSiteAssociation

    id: Union[str, GeneToExpressionSiteAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    object: Union[str, AnatomicalEntityId] = None
    predicate: Union[str, PredicateType] = None
    stage_qualifier: Optional[Union[str, LifeStageId]] = None
    quantifier_qualifier: Optional[Union[dict, OntologyClass]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToExpressionSiteAssociationId):
            self.id = GeneToExpressionSiteAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AnatomicalEntityId):
            self.object = AnatomicalEntityId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self.stage_qualifier is not None and not isinstance(self.stage_qualifier, LifeStageId):
            self.stage_qualifier = LifeStageId(self.stage_qualifier)

        if self.quantifier_qualifier is not None and not isinstance(self.quantifier_qualifier, OntologyClass):
            self.quantifier_qualifier = OntologyClass()

        super().__post_init__(**kwargs)


@dataclass
class SequenceVariantModulatesTreatmentAssociation(Association):
    """
    An association between a sequence variant and a treatment or health intervention. The treatment object itself
    encompasses both the disease and the drug used.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SequenceVariantModulatesTreatmentAssociation
    class_class_curie: ClassVar[str] = "biolink:SequenceVariantModulatesTreatmentAssociation"
    class_name: ClassVar[str] = "sequence variant modulates treatment association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SequenceVariantModulatesTreatmentAssociation

    id: Union[str, SequenceVariantModulatesTreatmentAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, SequenceVariantId] = None
    object: Union[str, TreatmentId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, SequenceVariantId):
            self.subject = SequenceVariantId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, TreatmentId):
            self.object = TreatmentId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class FunctionalAssociation(Association):
    """
    An association between a macromolecular machine mixin (gene, gene product or complex of gene products) and either
    a molecular activity, a biological process or a cellular location in which a function is executed.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.FunctionalAssociation
    class_class_curie: ClassVar[str] = "biolink:FunctionalAssociation"
    class_name: ClassVar[str] = "functional association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.FunctionalAssociation

    id: Union[str, FunctionalAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, MacromolecularMachineMixin] = None
    object: Union[dict, GeneOntologyClass] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, FunctionalAssociationId):
            self.id = FunctionalAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, MacromolecularMachineMixin):
            self.subject = MacromolecularMachineMixin(**as_dict(self.subject))

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneOntologyClass):
            self.object = GeneOntologyClass()

        super().__post_init__(**kwargs)


@dataclass
class MacromolecularMachineToEntityAssociationMixin(YAMLRoot):
    """
    an association which has a macromolecular machine mixin as a subject
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToEntityAssociationMixin
    class_class_curie: ClassVar[str] = "biolink:MacromolecularMachineToEntityAssociationMixin"
    class_name: ClassVar[str] = "macromolecular machine to entity association mixin"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToEntityAssociationMixin

    subject: Union[str, NamedThingId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, NamedThingId):
            self.subject = NamedThingId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class MacromolecularMachineToMolecularActivityAssociation(FunctionalAssociation):
    """
    A functional association between a macromolecular machine (gene, gene product or complex) and a molecular activity
    (as represented in the GO molecular function branch), where the entity carries out the activity, or contributes to
    its execution.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToMolecularActivityAssociation
    class_class_curie: ClassVar[str] = "biolink:MacromolecularMachineToMolecularActivityAssociation"
    class_name: ClassVar[str] = "macromolecular machine to molecular activity association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToMolecularActivityAssociation

    id: Union[str, MacromolecularMachineToMolecularActivityAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, MacromolecularMachineMixin] = None
    object: Union[str, MolecularActivityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MacromolecularMachineToMolecularActivityAssociationId):
            self.id = MacromolecularMachineToMolecularActivityAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, MolecularActivityId):
            self.object = MolecularActivityId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class MacromolecularMachineToBiologicalProcessAssociation(FunctionalAssociation):
    """
    A functional association between a macromolecular machine (gene, gene product or complex) and a biological process
    or pathway (as represented in the GO biological process branch), where the entity carries out some part of the
    process, regulates it, or acts upstream of it.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToBiologicalProcessAssociation
    class_class_curie: ClassVar[str] = "biolink:MacromolecularMachineToBiologicalProcessAssociation"
    class_name: ClassVar[str] = "macromolecular machine to biological process association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToBiologicalProcessAssociation

    id: Union[str, MacromolecularMachineToBiologicalProcessAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, MacromolecularMachineMixin] = None
    object: Union[str, BiologicalProcessId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MacromolecularMachineToBiologicalProcessAssociationId):
            self.id = MacromolecularMachineToBiologicalProcessAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, BiologicalProcessId):
            self.object = BiologicalProcessId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class MacromolecularMachineToCellularComponentAssociation(FunctionalAssociation):
    """
    A functional association between a macromolecular machine (gene, gene product or complex) and a cellular component
    (as represented in the GO cellular component branch), where the entity carries out its function in the cellular
    component.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToCellularComponentAssociation
    class_class_curie: ClassVar[str] = "biolink:MacromolecularMachineToCellularComponentAssociation"
    class_name: ClassVar[str] = "macromolecular machine to cellular component association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.MacromolecularMachineToCellularComponentAssociation

    id: Union[str, MacromolecularMachineToCellularComponentAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[dict, MacromolecularMachineMixin] = None
    object: Union[str, CellularComponentId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MacromolecularMachineToCellularComponentAssociationId):
            self.id = MacromolecularMachineToCellularComponentAssociationId(self.id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, CellularComponentId):
            self.object = CellularComponentId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GeneToGoTermAssociation(FunctionalAssociation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToGoTermAssociation
    class_class_curie: ClassVar[str] = "biolink:GeneToGoTermAssociation"
    class_name: ClassVar[str] = "gene to go term association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToGoTermAssociation

    id: Union[str, GeneToGoTermAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, MolecularEntityId] = None
    object: Union[dict, GeneOntologyClass] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToGoTermAssociationId):
            self.id = GeneToGoTermAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, MolecularEntityId):
            self.subject = MolecularEntityId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneOntologyClass):
            self.object = GeneOntologyClass()

        super().__post_init__(**kwargs)


@dataclass
class SequenceAssociation(Association):
    """
    An association between a sequence feature and a genomic entity it is localized to.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SequenceAssociation
    class_class_curie: ClassVar[str] = "biolink:SequenceAssociation"
    class_name: ClassVar[str] = "sequence association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SequenceAssociation

    id: Union[str, SequenceAssociationId] = None
    subject: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None
    object: Union[str, NamedThingId] = None
    relation: Union[str, URIorCURIE] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SequenceAssociationId):
            self.id = SequenceAssociationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class GenomicSequenceLocalization(SequenceAssociation):
    """
    A relationship between a sequence feature and a genomic entity it is localized to. The reference entity may be a
    chromosome, chromosome region or information entity such as a contig.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GenomicSequenceLocalization
    class_class_curie: ClassVar[str] = "biolink:GenomicSequenceLocalization"
    class_name: ClassVar[str] = "genomic sequence localization"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GenomicSequenceLocalization

    id: Union[str, GenomicSequenceLocalizationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, GenomicEntityId] = None
    object: Union[str, GenomicEntityId] = None
    predicate: Union[str, PredicateType] = None
    start_interbase_coordinate: Optional[int] = None
    end_interbase_coordinate: Optional[int] = None
    genome_build: Optional[str] = None
    strand: Optional[str] = None
    phase: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GenomicSequenceLocalizationId):
            self.id = GenomicSequenceLocalizationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenomicEntityId):
            self.subject = GenomicEntityId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GenomicEntityId):
            self.object = GenomicEntityId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self.start_interbase_coordinate is not None and not isinstance(self.start_interbase_coordinate, int):
            self.start_interbase_coordinate = int(self.start_interbase_coordinate)

        if self.end_interbase_coordinate is not None and not isinstance(self.end_interbase_coordinate, int):
            self.end_interbase_coordinate = int(self.end_interbase_coordinate)

        if self.genome_build is not None and not isinstance(self.genome_build, str):
            self.genome_build = str(self.genome_build)

        if self.strand is not None and not isinstance(self.strand, str):
            self.strand = str(self.strand)

        if self.phase is not None and not isinstance(self.phase, str):
            self.phase = str(self.phase)

        super().__post_init__(**kwargs)


@dataclass
class SequenceFeatureRelationship(Association):
    """
    For example, a particular exon is part of a particular transcript or gene
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.SequenceFeatureRelationship
    class_class_curie: ClassVar[str] = "biolink:SequenceFeatureRelationship"
    class_name: ClassVar[str] = "sequence feature relationship"
    class_model_uri: ClassVar[URIRef] = BIOLINK.SequenceFeatureRelationship

    id: Union[str, SequenceFeatureRelationshipId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, GenomicEntityId] = None
    object: Union[str, GenomicEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SequenceFeatureRelationshipId):
            self.id = SequenceFeatureRelationshipId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GenomicEntityId):
            self.subject = GenomicEntityId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GenomicEntityId):
            self.object = GenomicEntityId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class TranscriptToGeneRelationship(SequenceFeatureRelationship):
    """
    A gene is a collection of transcripts
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.TranscriptToGeneRelationship
    class_class_curie: ClassVar[str] = "biolink:TranscriptToGeneRelationship"
    class_name: ClassVar[str] = "transcript to gene relationship"
    class_model_uri: ClassVar[URIRef] = BIOLINK.TranscriptToGeneRelationship

    id: Union[str, TranscriptToGeneRelationshipId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, TranscriptId] = None
    object: Union[str, GeneId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TranscriptToGeneRelationshipId):
            self.id = TranscriptToGeneRelationshipId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, TranscriptId):
            self.subject = TranscriptId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneId):
            self.object = GeneId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GeneToGeneProductRelationship(SequenceFeatureRelationship):
    """
    A gene is transcribed and potentially translated to a gene product
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneProductRelationship
    class_class_curie: ClassVar[str] = "biolink:GeneToGeneProductRelationship"
    class_name: ClassVar[str] = "gene to gene product relationship"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneToGeneProductRelationship

    id: Union[str, GeneToGeneProductRelationshipId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, GeneId] = None
    object: Union[dict, GeneProductMixin] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneToGeneProductRelationshipId):
            self.id = GeneToGeneProductRelationshipId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneId):
            self.subject = GeneId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneProductMixin):
            self.object = GeneProductMixin(**as_dict(self.object))

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class ExonToTranscriptRelationship(SequenceFeatureRelationship):
    """
    A transcript is formed from multiple exons
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.ExonToTranscriptRelationship
    class_class_curie: ClassVar[str] = "biolink:ExonToTranscriptRelationship"
    class_name: ClassVar[str] = "exon to transcript relationship"
    class_model_uri: ClassVar[URIRef] = BIOLINK.ExonToTranscriptRelationship

    id: Union[str, ExonToTranscriptRelationshipId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, ExonId] = None
    object: Union[str, TranscriptId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ExonToTranscriptRelationshipId):
            self.id = ExonToTranscriptRelationshipId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, ExonId):
            self.subject = ExonId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, TranscriptId):
            self.object = TranscriptId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class GeneRegulatoryRelationship(Association):
    """
    A regulatory relationship between two genes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.GeneRegulatoryRelationship
    class_class_curie: ClassVar[str] = "biolink:GeneRegulatoryRelationship"
    class_name: ClassVar[str] = "gene regulatory relationship"
    class_model_uri: ClassVar[URIRef] = BIOLINK.GeneRegulatoryRelationship

    id: Union[str, GeneRegulatoryRelationshipId] = None
    relation: Union[str, URIorCURIE] = None
    predicate: Union[str, PredicateType] = None
    subject: Union[dict, GeneOrGeneProduct] = None
    object: Union[dict, GeneOrGeneProduct] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeneRegulatoryRelationshipId):
            self.id = GeneRegulatoryRelationshipId(self.id)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, GeneOrGeneProduct):
            self.subject = GeneOrGeneProduct(**as_dict(self.subject))

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, GeneOrGeneProduct):
            self.object = GeneOrGeneProduct(**as_dict(self.object))

        super().__post_init__(**kwargs)


@dataclass
class AnatomicalEntityToAnatomicalEntityAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntityToAnatomicalEntityAssociation
    class_class_curie: ClassVar[str] = "biolink:AnatomicalEntityToAnatomicalEntityAssociation"
    class_name: ClassVar[str] = "anatomical entity to anatomical entity association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntityToAnatomicalEntityAssociation

    id: Union[str, AnatomicalEntityToAnatomicalEntityAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, AnatomicalEntityId] = None
    object: Union[str, AnatomicalEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, AnatomicalEntityId):
            self.subject = AnatomicalEntityId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AnatomicalEntityId):
            self.object = AnatomicalEntityId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class AnatomicalEntityToAnatomicalEntityPartOfAssociation(AnatomicalEntityToAnatomicalEntityAssociation):
    """
    A relationship between two anatomical entities where the relationship is mereological, i.e the two entities are
    related by parthood. This includes relationships between cellular components and cells, between cells and tissues,
    tissues and whole organisms
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntityToAnatomicalEntityPartOfAssociation
    class_class_curie: ClassVar[str] = "biolink:AnatomicalEntityToAnatomicalEntityPartOfAssociation"
    class_name: ClassVar[str] = "anatomical entity to anatomical entity part of association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntityToAnatomicalEntityPartOfAssociation

    id: Union[str, AnatomicalEntityToAnatomicalEntityPartOfAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, AnatomicalEntityId] = None
    object: Union[str, AnatomicalEntityId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnatomicalEntityToAnatomicalEntityPartOfAssociationId):
            self.id = AnatomicalEntityToAnatomicalEntityPartOfAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, AnatomicalEntityId):
            self.subject = AnatomicalEntityId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AnatomicalEntityId):
            self.object = AnatomicalEntityId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class AnatomicalEntityToAnatomicalEntityOntogenicAssociation(AnatomicalEntityToAnatomicalEntityAssociation):
    """
    A relationship between two anatomical entities where the relationship is ontogenic, i.e. the two entities are
    related by development. A number of different relationship types can be used to specify the precise nature of the
    relationship.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntityToAnatomicalEntityOntogenicAssociation
    class_class_curie: ClassVar[str] = "biolink:AnatomicalEntityToAnatomicalEntityOntogenicAssociation"
    class_name: ClassVar[str] = "anatomical entity to anatomical entity ontogenic association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.AnatomicalEntityToAnatomicalEntityOntogenicAssociation

    id: Union[str, AnatomicalEntityToAnatomicalEntityOntogenicAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, AnatomicalEntityId] = None
    object: Union[str, AnatomicalEntityId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, AnatomicalEntityToAnatomicalEntityOntogenicAssociationId):
            self.id = AnatomicalEntityToAnatomicalEntityOntogenicAssociationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, AnatomicalEntityId):
            self.subject = AnatomicalEntityId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, AnatomicalEntityId):
            self.object = AnatomicalEntityId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class OrganismTaxonToEntityAssociation(YAMLRoot):
    """
    An association between an organism taxon and another entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToEntityAssociation
    class_class_curie: ClassVar[str] = "biolink:OrganismTaxonToEntityAssociation"
    class_name: ClassVar[str] = "organism taxon to entity association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToEntityAssociation

    subject: Union[str, OrganismTaxonId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, OrganismTaxonId):
            self.subject = OrganismTaxonId(self.subject)

        super().__post_init__(**kwargs)


@dataclass
class OrganismTaxonToOrganismTaxonAssociation(Association):
    """
    A relationship between two organism taxon nodes
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToOrganismTaxonAssociation
    class_class_curie: ClassVar[str] = "biolink:OrganismTaxonToOrganismTaxonAssociation"
    class_name: ClassVar[str] = "organism taxon to organism taxon association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToOrganismTaxonAssociation

    id: Union[str, OrganismTaxonToOrganismTaxonAssociationId] = None
    predicate: Union[str, PredicateType] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, OrganismTaxonId] = None
    object: Union[str, OrganismTaxonId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, OrganismTaxonId):
            self.subject = OrganismTaxonId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, OrganismTaxonId):
            self.object = OrganismTaxonId(self.object)

        super().__post_init__(**kwargs)


@dataclass
class OrganismTaxonToOrganismTaxonSpecialization(OrganismTaxonToOrganismTaxonAssociation):
    """
    A child-parent relationship between two taxa. For example: Homo sapiens subclass_of Homo
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToOrganismTaxonSpecialization
    class_class_curie: ClassVar[str] = "biolink:OrganismTaxonToOrganismTaxonSpecialization"
    class_name: ClassVar[str] = "organism taxon to organism taxon specialization"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToOrganismTaxonSpecialization

    id: Union[str, OrganismTaxonToOrganismTaxonSpecializationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, OrganismTaxonId] = None
    object: Union[str, OrganismTaxonId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganismTaxonToOrganismTaxonSpecializationId):
            self.id = OrganismTaxonToOrganismTaxonSpecializationId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, OrganismTaxonId):
            self.subject = OrganismTaxonId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, OrganismTaxonId):
            self.object = OrganismTaxonId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


@dataclass
class OrganismTaxonToOrganismTaxonInteraction(OrganismTaxonToOrganismTaxonAssociation):
    """
    An interaction relationship between two taxa. This may be a symbiotic relationship (encompassing mutualism and
    parasitism), or it may be non-symbiotic. Example: plague transmitted_by flea; cattle domesticated_by Homo sapiens;
    plague infects Homo sapiens
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToOrganismTaxonInteraction
    class_class_curie: ClassVar[str] = "biolink:OrganismTaxonToOrganismTaxonInteraction"
    class_name: ClassVar[str] = "organism taxon to organism taxon interaction"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToOrganismTaxonInteraction

    id: Union[str, OrganismTaxonToOrganismTaxonInteractionId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, OrganismTaxonId] = None
    object: Union[str, OrganismTaxonId] = None
    predicate: Union[str, PredicateType] = None
    associated_environmental_context: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, OrganismTaxonToOrganismTaxonInteractionId):
            self.id = OrganismTaxonToOrganismTaxonInteractionId(self.id)

        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, OrganismTaxonId):
            self.subject = OrganismTaxonId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, OrganismTaxonId):
            self.object = OrganismTaxonId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        if self.associated_environmental_context is not None and not isinstance(self.associated_environmental_context, str):
            self.associated_environmental_context = str(self.associated_environmental_context)

        super().__post_init__(**kwargs)


@dataclass
class OrganismTaxonToEnvironmentAssociation(Association):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToEnvironmentAssociation
    class_class_curie: ClassVar[str] = "biolink:OrganismTaxonToEnvironmentAssociation"
    class_name: ClassVar[str] = "organism taxon to environment association"
    class_model_uri: ClassVar[URIRef] = BIOLINK.OrganismTaxonToEnvironmentAssociation

    id: Union[str, OrganismTaxonToEnvironmentAssociationId] = None
    relation: Union[str, URIorCURIE] = None
    subject: Union[str, OrganismTaxonId] = None
    object: Union[str, NamedThingId] = None
    predicate: Union[str, PredicateType] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.subject):
            self.MissingRequiredField("subject")
        if not isinstance(self.subject, OrganismTaxonId):
            self.subject = OrganismTaxonId(self.subject)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, NamedThingId):
            self.object = NamedThingId(self.object)

        if self._is_empty(self.predicate):
            self.MissingRequiredField("predicate")
        if not isinstance(self.predicate, PredicateType):
            self.predicate = PredicateType(self.predicate)

        super().__post_init__(**kwargs)


# Enumerations
class LogicalInterpretationEnum(EnumDefinitionImpl):

    SomeSome = PermissibleValue(text="SomeSome",
                                       description="A modifier on a triple that causes the triple to be interpreted as a some-some statement",
                                       meaning=OS.SomeSomeInterpretation)
    AllSome = PermissibleValue(text="AllSome",
                                     description="A modifier on a triple that causes the triple to be interpreted as an all-some statement.",
                                     meaning=OS.AllSomeInterpretation)
    InverseAllSome = PermissibleValue(text="InverseAllSome")

    _defn = EnumDefinition(
        name="LogicalInterpretationEnum",
    )

# Slots
class slots:
    pass

slots.has_attribute = Slot(uri=BIOLINK.has_attribute, name="has attribute", curie=BIOLINK.curie('has_attribute'),
                   model_uri=BIOLINK.has_attribute, domain=Entity, range=Optional[Union[Union[dict, Attribute], List[Union[dict, Attribute]]]])

slots.has_attribute_type = Slot(uri=BIOLINK.has_attribute_type, name="has attribute type", curie=BIOLINK.curie('has_attribute_type'),
                   model_uri=BIOLINK.has_attribute_type, domain=Attribute, range=Union[dict, OntologyClass])

slots.has_qualitative_value = Slot(uri=BIOLINK.has_qualitative_value, name="has qualitative value", curie=BIOLINK.curie('has_qualitative_value'),
                   model_uri=BIOLINK.has_qualitative_value, domain=Attribute, range=Optional[Union[str, NamedThingId]])

slots.has_quantitative_value = Slot(uri=BIOLINK.has_quantitative_value, name="has quantitative value", curie=BIOLINK.curie('has_quantitative_value'),
                   model_uri=BIOLINK.has_quantitative_value, domain=Attribute, range=Optional[Union[Union[dict, QuantityValue], List[Union[dict, QuantityValue]]]])

slots.has_numeric_value = Slot(uri=BIOLINK.has_numeric_value, name="has numeric value", curie=BIOLINK.curie('has_numeric_value'),
                   model_uri=BIOLINK.has_numeric_value, domain=QuantityValue, range=Optional[float])

slots.has_unit = Slot(uri=BIOLINK.has_unit, name="has unit", curie=BIOLINK.curie('has_unit'),
                   model_uri=BIOLINK.has_unit, domain=QuantityValue, range=Optional[Union[str, Unit]])

slots.node_property = Slot(uri=BIOLINK.node_property, name="node property", curie=BIOLINK.curie('node_property'),
                   model_uri=BIOLINK.node_property, domain=NamedThing, range=Optional[str])

slots.id = Slot(uri=BIOLINK.id, name="id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.id, domain=None, range=URIRef)

slots.iri = Slot(uri=BIOLINK.iri, name="iri", curie=BIOLINK.curie('iri'),
                   model_uri=BIOLINK.iri, domain=None, range=Optional[Union[str, IriType]])

slots.type = Slot(uri=RDF.type, name="type", curie=RDF.curie('type'),
                   model_uri=BIOLINK.type, domain=None, range=Optional[str])

slots.category = Slot(uri=BIOLINK.category, name="category", curie=BIOLINK.curie('category'),
                   model_uri=BIOLINK.category, domain=Entity, range=Optional[Union[Union[str, CategoryType], List[Union[str, CategoryType]]]])

slots.name = Slot(uri=RDFS.label, name="name", curie=RDFS.curie('label'),
                   model_uri=BIOLINK.name, domain=None, range=Optional[Union[str, LabelType]])

slots.source = Slot(uri=BIOLINK.source, name="source", curie=BIOLINK.curie('source'),
                   model_uri=BIOLINK.source, domain=None, range=Optional[Union[str, LabelType]])

slots.filler = Slot(uri=BIOLINK.filler, name="filler", curie=BIOLINK.curie('filler'),
                   model_uri=BIOLINK.filler, domain=NamedThing, range=Optional[Union[str, NamedThingId]])

slots.symbol = Slot(uri=BIOLINK.symbol, name="symbol", curie=BIOLINK.curie('symbol'),
                   model_uri=BIOLINK.symbol, domain=NamedThing, range=Optional[str])

slots.synonym = Slot(uri=BIOLINK.synonym, name="synonym", curie=BIOLINK.curie('synonym'),
                   model_uri=BIOLINK.synonym, domain=NamedThing, range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]])

slots.has_topic = Slot(uri=BIOLINK.has_topic, name="has topic", curie=BIOLINK.curie('has_topic'),
                   model_uri=BIOLINK.has_topic, domain=NamedThing, range=Optional[Union[dict, OntologyClass]])

slots.xref = Slot(uri=BIOLINK.xref, name="xref", curie=BIOLINK.curie('xref'),
                   model_uri=BIOLINK.xref, domain=NamedThing, range=Optional[Union[Union[str, IriType], List[Union[str, IriType]]]])

slots.full_name = Slot(uri=BIOLINK.full_name, name="full name", curie=BIOLINK.curie('full_name'),
                   model_uri=BIOLINK.full_name, domain=NamedThing, range=Optional[Union[str, LabelType]])

slots.description = Slot(uri=DCT.description, name="description", curie=DCT.curie('description'),
                   model_uri=BIOLINK.description, domain=None, range=Optional[Union[str, NarrativeText]])

slots.systematic_synonym = Slot(uri=GOP.systematic_synonym, name="systematic synonym", curie=GOP.curie('systematic_synonym'),
                   model_uri=BIOLINK.systematic_synonym, domain=NamedThing, range=Optional[Union[Union[str, LabelType], List[Union[str, LabelType]]]])

slots.affiliation = Slot(uri=BIOLINK.affiliation, name="affiliation", curie=BIOLINK.curie('affiliation'),
                   model_uri=BIOLINK.affiliation, domain=Agent, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.address = Slot(uri=BIOLINK.address, name="address", curie=BIOLINK.curie('address'),
                   model_uri=BIOLINK.address, domain=NamedThing, range=Optional[str])

slots.latitude = Slot(uri=BIOLINK.latitude, name="latitude", curie=BIOLINK.curie('latitude'),
                   model_uri=BIOLINK.latitude, domain=NamedThing, range=Optional[float])

slots.longitude = Slot(uri=BIOLINK.longitude, name="longitude", curie=BIOLINK.curie('longitude'),
                   model_uri=BIOLINK.longitude, domain=NamedThing, range=Optional[float])

slots.timepoint = Slot(uri=BIOLINK.timepoint, name="timepoint", curie=BIOLINK.curie('timepoint'),
                   model_uri=BIOLINK.timepoint, domain=NamedThing, range=Optional[Union[str, TimeType]])

slots.creation_date = Slot(uri=BIOLINK.creation_date, name="creation date", curie=BIOLINK.curie('creation_date'),
                   model_uri=BIOLINK.creation_date, domain=NamedThing, range=Optional[Union[str, XSDDate]])

slots.update_date = Slot(uri=BIOLINK.update_date, name="update date", curie=BIOLINK.curie('update_date'),
                   model_uri=BIOLINK.update_date, domain=NamedThing, range=Optional[Union[str, XSDDate]])

slots.aggregate_statistic = Slot(uri=BIOLINK.aggregate_statistic, name="aggregate statistic", curie=BIOLINK.curie('aggregate_statistic'),
                   model_uri=BIOLINK.aggregate_statistic, domain=NamedThing, range=Optional[str])

slots.has_count = Slot(uri=BIOLINK.has_count, name="has count", curie=BIOLINK.curie('has_count'),
                   model_uri=BIOLINK.has_count, domain=NamedThing, range=Optional[int])

slots.has_total = Slot(uri=BIOLINK.has_total, name="has total", curie=BIOLINK.curie('has_total'),
                   model_uri=BIOLINK.has_total, domain=NamedThing, range=Optional[int])

slots.has_quotient = Slot(uri=BIOLINK.has_quotient, name="has quotient", curie=BIOLINK.curie('has_quotient'),
                   model_uri=BIOLINK.has_quotient, domain=NamedThing, range=Optional[float])

slots.has_percentage = Slot(uri=BIOLINK.has_percentage, name="has percentage", curie=BIOLINK.curie('has_percentage'),
                   model_uri=BIOLINK.has_percentage, domain=NamedThing, range=Optional[float])

slots.has_dataset = Slot(uri=DCT.source, name="has dataset", curie=DCT.curie('source'),
                   model_uri=BIOLINK.has_dataset, domain=DatasetVersion, range=Optional[Union[str, DatasetId]])

slots.source_web_page = Slot(uri=BIOLINK.source_web_page, name="source web page", curie=BIOLINK.curie('source_web_page'),
                   model_uri=BIOLINK.source_web_page, domain=DatasetSummary, range=Optional[str])

slots.source_logo = Slot(uri=SCHEMA.logo, name="source logo", curie=SCHEMA.curie('logo'),
                   model_uri=BIOLINK.source_logo, domain=DatasetSummary, range=Optional[str])

slots.retrieved_on = Slot(uri=BIOLINK.retrieved_on, name="retrieved on", curie=BIOLINK.curie('retrieved_on'),
                   model_uri=BIOLINK.retrieved_on, domain=Dataset, range=Optional[Union[str, XSDDate]])

slots.version_of = Slot(uri=BIOLINK.version_of, name="version of", curie=BIOLINK.curie('version_of'),
                   model_uri=BIOLINK.version_of, domain=DatasetVersion, range=Optional[Union[str, DatasetSummaryId]])

slots.version = Slot(uri=BIOLINK.version, name="version", curie=BIOLINK.curie('version'),
                   model_uri=BIOLINK.version, domain=Dataset, range=Optional[str])

slots.license = Slot(uri=BIOLINK.license, name="license", curie=BIOLINK.curie('license'),
                   model_uri=BIOLINK.license, domain=InformationContentEntity, range=Optional[str])

slots.rights = Slot(uri=BIOLINK.rights, name="rights", curie=BIOLINK.curie('rights'),
                   model_uri=BIOLINK.rights, domain=InformationContentEntity, range=Optional[str])

slots.format = Slot(uri=BIOLINK.format, name="format", curie=BIOLINK.curie('format'),
                   model_uri=BIOLINK.format, domain=InformationContentEntity, range=Optional[str])

slots.created_with = Slot(uri=BIOLINK.created_with, name="created_with", curie=BIOLINK.curie('created_with'),
                   model_uri=BIOLINK.created_with, domain=Dataset, range=Optional[str])

slots.download_url = Slot(uri=DCAT.downloadURL, name="download url", curie=DCAT.curie('downloadURL'),
                   model_uri=BIOLINK.download_url, domain=InformationContentEntity, range=Optional[str])

slots.dataset_download_url = Slot(uri=DCAT.downloadURL, name="dataset download url", curie=DCAT.curie('downloadURL'),
                   model_uri=BIOLINK.dataset_download_url, domain=Dataset, range=Optional[str])

slots.distribution_download_url = Slot(uri=BIOLINK.distribution_download_url, name="distribution download url", curie=BIOLINK.curie('distribution_download_url'),
                   model_uri=BIOLINK.distribution_download_url, domain=DatasetDistribution, range=Optional[str])

slots.ingest_date = Slot(uri=PAV.version, name="ingest date", curie=PAV.curie('version'),
                   model_uri=BIOLINK.ingest_date, domain=DatasetVersion, range=Optional[str])

slots.has_distribution = Slot(uri=DCT.distribution, name="has distribution", curie=DCT.curie('distribution'),
                   model_uri=BIOLINK.has_distribution, domain=DatasetVersion, range=Optional[Union[str, DatasetDistributionId]])

slots.published_in = Slot(uri=BIOLINK.published_in, name="published in", curie=BIOLINK.curie('published_in'),
                   model_uri=BIOLINK.published_in, domain=Publication, range=Optional[Union[str, URIorCURIE]])

slots.iso_abbreviation = Slot(uri=BIOLINK.iso_abbreviation, name="iso abbreviation", curie=BIOLINK.curie('iso_abbreviation'),
                   model_uri=BIOLINK.iso_abbreviation, domain=Publication, range=Optional[str])

slots.authors = Slot(uri=BIOLINK.authors, name="authors", curie=BIOLINK.curie('authors'),
                   model_uri=BIOLINK.authors, domain=Publication, range=Optional[Union[str, List[str]]])

slots.volume = Slot(uri=BIOLINK.volume, name="volume", curie=BIOLINK.curie('volume'),
                   model_uri=BIOLINK.volume, domain=Publication, range=Optional[str])

slots.chapter = Slot(uri=BIOLINK.chapter, name="chapter", curie=BIOLINK.curie('chapter'),
                   model_uri=BIOLINK.chapter, domain=BookChapter, range=Optional[str])

slots.issue = Slot(uri=BIOLINK.issue, name="issue", curie=BIOLINK.curie('issue'),
                   model_uri=BIOLINK.issue, domain=Publication, range=Optional[str])

slots.pages = Slot(uri=BIOLINK.pages, name="pages", curie=BIOLINK.curie('pages'),
                   model_uri=BIOLINK.pages, domain=Publication, range=Optional[Union[str, List[str]]])

slots.summary = Slot(uri=BIOLINK.summary, name="summary", curie=BIOLINK.curie('summary'),
                   model_uri=BIOLINK.summary, domain=Publication, range=Optional[str])

slots.keywords = Slot(uri=BIOLINK.keywords, name="keywords", curie=BIOLINK.curie('keywords'),
                   model_uri=BIOLINK.keywords, domain=Publication, range=Optional[Union[str, List[str]]])

slots.mesh_terms = Slot(uri=BIOLINK.mesh_terms, name="mesh terms", curie=BIOLINK.curie('mesh_terms'),
                   model_uri=BIOLINK.mesh_terms, domain=Publication, range=Optional[Union[Union[str, URIorCURIE], List[Union[str, URIorCURIE]]]])

slots.has_biological_sequence = Slot(uri=BIOLINK.has_biological_sequence, name="has biological sequence", curie=BIOLINK.curie('has_biological_sequence'),
                   model_uri=BIOLINK.has_biological_sequence, domain=NamedThing, range=Optional[Union[str, BiologicalSequence]])

slots.has_gene_or_gene_product = Slot(uri=BIOLINK.has_gene_or_gene_product, name="has gene or gene product", curie=BIOLINK.curie('has_gene_or_gene_product'),
                   model_uri=BIOLINK.has_gene_or_gene_product, domain=NamedThing, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.has_gene = Slot(uri=BIOLINK.has_gene, name="has gene", curie=BIOLINK.curie('has_gene'),
                   model_uri=BIOLINK.has_gene, domain=NamedThing, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.has_zygosity = Slot(uri=BIOLINK.has_zygosity, name="has zygosity", curie=BIOLINK.curie('has_zygosity'),
                   model_uri=BIOLINK.has_zygosity, domain=GenomicEntity, range=Optional[Union[dict, "Zygosity"]])

slots.has_chemical_formula = Slot(uri=BIOLINK.has_chemical_formula, name="has chemical formula", curie=BIOLINK.curie('has_chemical_formula'),
                   model_uri=BIOLINK.has_chemical_formula, domain=NamedThing, range=Optional[str])

slots.is_metabolite = Slot(uri=BIOLINK.is_metabolite, name="is metabolite", curie=BIOLINK.curie('is_metabolite'),
                   model_uri=BIOLINK.is_metabolite, domain=ChemicalSubstance, range=Optional[Union[bool, Bool]])

slots.has_constituent = Slot(uri=BIOLINK.has_constituent, name="has constituent", curie=BIOLINK.curie('has_constituent'),
                   model_uri=BIOLINK.has_constituent, domain=NamedThing, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.has_drug = Slot(uri=BIOLINK.has_drug, name="has drug", curie=BIOLINK.curie('has_drug'),
                   model_uri=BIOLINK.has_drug, domain=NamedThing, range=Optional[Union[Union[str, DrugId], List[Union[str, DrugId]]]])

slots.has_device = Slot(uri=BIOLINK.has_device, name="has device", curie=BIOLINK.curie('has_device'),
                   model_uri=BIOLINK.has_device, domain=NamedThing, range=Optional[Union[Union[str, DeviceId], List[Union[str, DeviceId]]]])

slots.has_procedure = Slot(uri=BIOLINK.has_procedure, name="has procedure", curie=BIOLINK.curie('has_procedure'),
                   model_uri=BIOLINK.has_procedure, domain=NamedThing, range=Optional[Union[Union[str, ProcedureId], List[Union[str, ProcedureId]]]])

slots.has_receptor = Slot(uri=BIOLINK.has_receptor, name="has receptor", curie=BIOLINK.curie('has_receptor'),
                   model_uri=BIOLINK.has_receptor, domain=None, range=Optional[Union[str, OrganismalEntityId]])

slots.has_stressor = Slot(uri=BIOLINK.has_stressor, name="has stressor", curie=BIOLINK.curie('has_stressor'),
                   model_uri=BIOLINK.has_stressor, domain=None, range=Optional[str])

slots.has_route = Slot(uri=BIOLINK.has_route, name="has route", curie=BIOLINK.curie('has_route'),
                   model_uri=BIOLINK.has_route, domain=None, range=Optional[str])

slots.has_population_context = Slot(uri=BIOLINK.has_population_context, name="has population context", curie=BIOLINK.curie('has_population_context'),
                   model_uri=BIOLINK.has_population_context, domain=Association, range=Optional[Union[str, PopulationOfIndividualOrganismsId]])

slots.has_temporal_context = Slot(uri=BIOLINK.has_temporal_context, name="has temporal context", curie=BIOLINK.curie('has_temporal_context'),
                   model_uri=BIOLINK.has_temporal_context, domain=Association, range=Optional[Union[str, TimeType]])

slots.related_to = Slot(uri=BIOLINK.related_to, name="related to", curie=BIOLINK.curie('related_to'),
                   model_uri=BIOLINK.related_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.superclass_of = Slot(uri=BIOLINK.superclass_of, name="superclass of", curie=BIOLINK.curie('superclass_of'),
                   model_uri=BIOLINK.superclass_of, domain=None, range=Optional[Union[Union[dict, "OntologyClass"], List[Union[dict, "OntologyClass"]]]])

slots.subclass_of = Slot(uri=BIOLINK.subclass_of, name="subclass of", curie=BIOLINK.curie('subclass_of'),
                   model_uri=BIOLINK.subclass_of, domain=None, range=Optional[Union[Union[dict, "OntologyClass"], List[Union[dict, "OntologyClass"]]]])

slots.same_as = Slot(uri=BIOLINK.same_as, name="same as", curie=BIOLINK.curie('same_as'),
                   model_uri=BIOLINK.same_as, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.close_match = Slot(uri=BIOLINK.close_match, name="close match", curie=BIOLINK.curie('close_match'),
                   model_uri=BIOLINK.close_match, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.exact_match = Slot(uri=BIOLINK.exact_match, name="exact match", curie=BIOLINK.curie('exact_match'),
                   model_uri=BIOLINK.exact_match, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.broad_match = Slot(uri=BIOLINK.broad_match, name="broad match", curie=BIOLINK.curie('broad_match'),
                   model_uri=BIOLINK.broad_match, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.narrow_match = Slot(uri=BIOLINK.narrow_match, name="narrow match", curie=BIOLINK.curie('narrow_match'),
                   model_uri=BIOLINK.narrow_match, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.opposite_of = Slot(uri=BIOLINK.opposite_of, name="opposite of", curie=BIOLINK.curie('opposite_of'),
                   model_uri=BIOLINK.opposite_of, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.contributor = Slot(uri=BIOLINK.contributor, name="contributor", curie=BIOLINK.curie('contributor'),
                   model_uri=BIOLINK.contributor, domain=InformationContentEntity, range=Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]])

slots.provider = Slot(uri=BIOLINK.provider, name="provider", curie=BIOLINK.curie('provider'),
                   model_uri=BIOLINK.provider, domain=InformationContentEntity, range=Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]])

slots.publisher = Slot(uri=BIOLINK.publisher, name="publisher", curie=BIOLINK.curie('publisher'),
                   model_uri=BIOLINK.publisher, domain=Publication, range=Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]])

slots.editor = Slot(uri=BIOLINK.editor, name="editor", curie=BIOLINK.curie('editor'),
                   model_uri=BIOLINK.editor, domain=Publication, range=Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]])

slots.author = Slot(uri=BIOLINK.author, name="author", curie=BIOLINK.curie('author'),
                   model_uri=BIOLINK.author, domain=Publication, range=Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]])

slots.interacts_with = Slot(uri=BIOLINK.interacts_with, name="interacts with", curie=BIOLINK.curie('interacts_with'),
                   model_uri=BIOLINK.interacts_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.physically_interacts_with = Slot(uri=BIOLINK.physically_interacts_with, name="physically interacts with", curie=BIOLINK.curie('physically_interacts_with'),
                   model_uri=BIOLINK.physically_interacts_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.molecularly_interacts_with = Slot(uri=BIOLINK.molecularly_interacts_with, name="molecularly interacts with", curie=BIOLINK.curie('molecularly_interacts_with'),
                   model_uri=BIOLINK.molecularly_interacts_with, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.genetically_interacts_with = Slot(uri=BIOLINK.genetically_interacts_with, name="genetically interacts with", curie=BIOLINK.curie('genetically_interacts_with'),
                   model_uri=BIOLINK.genetically_interacts_with, domain=Gene, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.affects = Slot(uri=BIOLINK.affects, name="affects", curie=BIOLINK.curie('affects'),
                   model_uri=BIOLINK.affects, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.affected_by = Slot(uri=BIOLINK.affected_by, name="affected by", curie=BIOLINK.curie('affected_by'),
                   model_uri=BIOLINK.affected_by, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.chemical_role_mixin = Slot(uri=BIOLINK.chemical_role_mixin, name="chemical role mixin", curie=BIOLINK.curie('chemical_role_mixin'),
                   model_uri=BIOLINK.chemical_role_mixin, domain=None, range=Optional[str])

slots.biological_role_mixin = Slot(uri=BIOLINK.biological_role_mixin, name="biological role mixin", curie=BIOLINK.curie('biological_role_mixin'),
                   model_uri=BIOLINK.biological_role_mixin, domain=None, range=Optional[str])

slots.affects_abundance_of = Slot(uri=BIOLINK.affects_abundance_of, name="affects abundance of", curie=BIOLINK.curie('affects_abundance_of'),
                   model_uri=BIOLINK.affects_abundance_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_abundance_of = Slot(uri=BIOLINK.increases_abundance_of, name="increases abundance of", curie=BIOLINK.curie('increases_abundance_of'),
                   model_uri=BIOLINK.increases_abundance_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_abundance_of = Slot(uri=BIOLINK.decreases_abundance_of, name="decreases abundance of", curie=BIOLINK.curie('decreases_abundance_of'),
                   model_uri=BIOLINK.decreases_abundance_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_activity_of = Slot(uri=BIOLINK.affects_activity_of, name="affects activity of", curie=BIOLINK.curie('affects_activity_of'),
                   model_uri=BIOLINK.affects_activity_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_activity_of = Slot(uri=BIOLINK.increases_activity_of, name="increases activity of", curie=BIOLINK.curie('increases_activity_of'),
                   model_uri=BIOLINK.increases_activity_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_activity_of = Slot(uri=BIOLINK.decreases_activity_of, name="decreases activity of", curie=BIOLINK.curie('decreases_activity_of'),
                   model_uri=BIOLINK.decreases_activity_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_expression_of = Slot(uri=BIOLINK.affects_expression_of, name="affects expression of", curie=BIOLINK.curie('affects_expression_of'),
                   model_uri=BIOLINK.affects_expression_of, domain=MolecularEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.increases_expression_of = Slot(uri=BIOLINK.increases_expression_of, name="increases expression of", curie=BIOLINK.curie('increases_expression_of'),
                   model_uri=BIOLINK.increases_expression_of, domain=MolecularEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.decreases_expression_of = Slot(uri=BIOLINK.decreases_expression_of, name="decreases expression of", curie=BIOLINK.curie('decreases_expression_of'),
                   model_uri=BIOLINK.decreases_expression_of, domain=MolecularEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.affects_folding_of = Slot(uri=BIOLINK.affects_folding_of, name="affects folding of", curie=BIOLINK.curie('affects_folding_of'),
                   model_uri=BIOLINK.affects_folding_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_folding_of = Slot(uri=BIOLINK.increases_folding_of, name="increases folding of", curie=BIOLINK.curie('increases_folding_of'),
                   model_uri=BIOLINK.increases_folding_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_folding_of = Slot(uri=BIOLINK.decreases_folding_of, name="decreases folding of", curie=BIOLINK.curie('decreases_folding_of'),
                   model_uri=BIOLINK.decreases_folding_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_localization_of = Slot(uri=BIOLINK.affects_localization_of, name="affects localization of", curie=BIOLINK.curie('affects_localization_of'),
                   model_uri=BIOLINK.affects_localization_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_localization_of = Slot(uri=BIOLINK.increases_localization_of, name="increases localization of", curie=BIOLINK.curie('increases_localization_of'),
                   model_uri=BIOLINK.increases_localization_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_localization_of = Slot(uri=BIOLINK.decreases_localization_of, name="decreases localization of", curie=BIOLINK.curie('decreases_localization_of'),
                   model_uri=BIOLINK.decreases_localization_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_metabolic_processing_of = Slot(uri=BIOLINK.affects_metabolic_processing_of, name="affects metabolic processing of", curie=BIOLINK.curie('affects_metabolic_processing_of'),
                   model_uri=BIOLINK.affects_metabolic_processing_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_metabolic_processing_of = Slot(uri=BIOLINK.increases_metabolic_processing_of, name="increases metabolic processing of", curie=BIOLINK.curie('increases_metabolic_processing_of'),
                   model_uri=BIOLINK.increases_metabolic_processing_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_metabolic_processing_of = Slot(uri=BIOLINK.decreases_metabolic_processing_of, name="decreases metabolic processing of", curie=BIOLINK.curie('decreases_metabolic_processing_of'),
                   model_uri=BIOLINK.decreases_metabolic_processing_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_molecular_modification_of = Slot(uri=BIOLINK.affects_molecular_modification_of, name="affects molecular modification of", curie=BIOLINK.curie('affects_molecular_modification_of'),
                   model_uri=BIOLINK.affects_molecular_modification_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_molecular_modification_of = Slot(uri=BIOLINK.increases_molecular_modification_of, name="increases molecular modification of", curie=BIOLINK.curie('increases_molecular_modification_of'),
                   model_uri=BIOLINK.increases_molecular_modification_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_molecular_modification_of = Slot(uri=BIOLINK.decreases_molecular_modification_of, name="decreases molecular modification of", curie=BIOLINK.curie('decreases_molecular_modification_of'),
                   model_uri=BIOLINK.decreases_molecular_modification_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_synthesis_of = Slot(uri=BIOLINK.affects_synthesis_of, name="affects synthesis of", curie=BIOLINK.curie('affects_synthesis_of'),
                   model_uri=BIOLINK.affects_synthesis_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_synthesis_of = Slot(uri=BIOLINK.increases_synthesis_of, name="increases synthesis of", curie=BIOLINK.curie('increases_synthesis_of'),
                   model_uri=BIOLINK.increases_synthesis_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_synthesis_of = Slot(uri=BIOLINK.decreases_synthesis_of, name="decreases synthesis of", curie=BIOLINK.curie('decreases_synthesis_of'),
                   model_uri=BIOLINK.decreases_synthesis_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_degradation_of = Slot(uri=BIOLINK.affects_degradation_of, name="affects degradation of", curie=BIOLINK.curie('affects_degradation_of'),
                   model_uri=BIOLINK.affects_degradation_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_degradation_of = Slot(uri=BIOLINK.increases_degradation_of, name="increases degradation of", curie=BIOLINK.curie('increases_degradation_of'),
                   model_uri=BIOLINK.increases_degradation_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_degradation_of = Slot(uri=BIOLINK.decreases_degradation_of, name="decreases degradation of", curie=BIOLINK.curie('decreases_degradation_of'),
                   model_uri=BIOLINK.decreases_degradation_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_mutation_rate_of = Slot(uri=BIOLINK.affects_mutation_rate_of, name="affects mutation rate of", curie=BIOLINK.curie('affects_mutation_rate_of'),
                   model_uri=BIOLINK.affects_mutation_rate_of, domain=MolecularEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.increases_mutation_rate_of = Slot(uri=BIOLINK.increases_mutation_rate_of, name="increases mutation rate of", curie=BIOLINK.curie('increases_mutation_rate_of'),
                   model_uri=BIOLINK.increases_mutation_rate_of, domain=MolecularEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.decreases_mutation_rate_of = Slot(uri=BIOLINK.decreases_mutation_rate_of, name="decreases mutation rate of", curie=BIOLINK.curie('decreases_mutation_rate_of'),
                   model_uri=BIOLINK.decreases_mutation_rate_of, domain=MolecularEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.affects_response_to = Slot(uri=BIOLINK.affects_response_to, name="affects response to", curie=BIOLINK.curie('affects_response_to'),
                   model_uri=BIOLINK.affects_response_to, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_response_to = Slot(uri=BIOLINK.increases_response_to, name="increases response to", curie=BIOLINK.curie('increases_response_to'),
                   model_uri=BIOLINK.increases_response_to, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_response_to = Slot(uri=BIOLINK.decreases_response_to, name="decreases response to", curie=BIOLINK.curie('decreases_response_to'),
                   model_uri=BIOLINK.decreases_response_to, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_splicing_of = Slot(uri=BIOLINK.affects_splicing_of, name="affects splicing of", curie=BIOLINK.curie('affects_splicing_of'),
                   model_uri=BIOLINK.affects_splicing_of, domain=MolecularEntity, range=Optional[Union[Union[str, TranscriptId], List[Union[str, TranscriptId]]]])

slots.increases_splicing_of = Slot(uri=BIOLINK.increases_splicing_of, name="increases splicing of", curie=BIOLINK.curie('increases_splicing_of'),
                   model_uri=BIOLINK.increases_splicing_of, domain=MolecularEntity, range=Optional[Union[Union[str, TranscriptId], List[Union[str, TranscriptId]]]])

slots.decreases_splicing_of = Slot(uri=BIOLINK.decreases_splicing_of, name="decreases splicing of", curie=BIOLINK.curie('decreases_splicing_of'),
                   model_uri=BIOLINK.decreases_splicing_of, domain=MolecularEntity, range=Optional[Union[Union[str, TranscriptId], List[Union[str, TranscriptId]]]])

slots.affects_stability_of = Slot(uri=BIOLINK.affects_stability_of, name="affects stability of", curie=BIOLINK.curie('affects_stability_of'),
                   model_uri=BIOLINK.affects_stability_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_stability_of = Slot(uri=BIOLINK.increases_stability_of, name="increases stability of", curie=BIOLINK.curie('increases_stability_of'),
                   model_uri=BIOLINK.increases_stability_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_stability_of = Slot(uri=BIOLINK.decreases_stability_of, name="decreases stability of", curie=BIOLINK.curie('decreases_stability_of'),
                   model_uri=BIOLINK.decreases_stability_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_transport_of = Slot(uri=BIOLINK.affects_transport_of, name="affects transport of", curie=BIOLINK.curie('affects_transport_of'),
                   model_uri=BIOLINK.affects_transport_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_transport_of = Slot(uri=BIOLINK.increases_transport_of, name="increases transport of", curie=BIOLINK.curie('increases_transport_of'),
                   model_uri=BIOLINK.increases_transport_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_transport_of = Slot(uri=BIOLINK.decreases_transport_of, name="decreases transport of", curie=BIOLINK.curie('decreases_transport_of'),
                   model_uri=BIOLINK.decreases_transport_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_secretion_of = Slot(uri=BIOLINK.affects_secretion_of, name="affects secretion of", curie=BIOLINK.curie('affects_secretion_of'),
                   model_uri=BIOLINK.affects_secretion_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_secretion_of = Slot(uri=BIOLINK.increases_secretion_of, name="increases secretion of", curie=BIOLINK.curie('increases_secretion_of'),
                   model_uri=BIOLINK.increases_secretion_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_secretion_of = Slot(uri=BIOLINK.decreases_secretion_of, name="decreases secretion of", curie=BIOLINK.curie('decreases_secretion_of'),
                   model_uri=BIOLINK.decreases_secretion_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_uptake_of = Slot(uri=BIOLINK.affects_uptake_of, name="affects uptake of", curie=BIOLINK.curie('affects_uptake_of'),
                   model_uri=BIOLINK.affects_uptake_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_uptake_of = Slot(uri=BIOLINK.increases_uptake_of, name="increases uptake of", curie=BIOLINK.curie('increases_uptake_of'),
                   model_uri=BIOLINK.increases_uptake_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.decreases_uptake_of = Slot(uri=BIOLINK.decreases_uptake_of, name="decreases uptake of", curie=BIOLINK.curie('decreases_uptake_of'),
                   model_uri=BIOLINK.decreases_uptake_of, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.regulates = Slot(uri=BIOLINK.regulates, name="regulates", curie=BIOLINK.curie('regulates'),
                   model_uri=BIOLINK.regulates, domain=None, range=Optional[Union[dict, "PhysicalEssenceOrOccurrent"]])

slots.regulated_by = Slot(uri=BIOLINK.regulated_by, name="regulated by", curie=BIOLINK.curie('regulated_by'),
                   model_uri=BIOLINK.regulated_by, domain=None, range=Optional[Union[dict, "PhysicalEssenceOrOccurrent"]])

slots.positively_regulates = Slot(uri=BIOLINK.positively_regulates, name="positively regulates", curie=BIOLINK.curie('positively_regulates'),
                   model_uri=BIOLINK.positively_regulates, domain=None, range=Optional[Union[dict, "PhysicalEssenceOrOccurrent"]])

slots.positively_regulated_by = Slot(uri=BIOLINK.positively_regulated_by, name="positively regulated by", curie=BIOLINK.curie('positively_regulated_by'),
                   model_uri=BIOLINK.positively_regulated_by, domain=None, range=Optional[Union[dict, "PhysicalEssenceOrOccurrent"]])

slots.negatively_regulates = Slot(uri=BIOLINK.negatively_regulates, name="negatively regulates", curie=BIOLINK.curie('negatively_regulates'),
                   model_uri=BIOLINK.negatively_regulates, domain=None, range=Optional[Union[dict, "PhysicalEssenceOrOccurrent"]])

slots.negatively_regulated_by = Slot(uri=BIOLINK.negatively_regulated_by, name="negatively regulated by", curie=BIOLINK.curie('negatively_regulated_by'),
                   model_uri=BIOLINK.negatively_regulated_by, domain=None, range=Optional[Union[dict, "PhysicalEssenceOrOccurrent"]])

slots.process_regulates_process = Slot(uri=BIOLINK.process_regulates_process, name="process regulates process", curie=BIOLINK.curie('process_regulates_process'),
                   model_uri=BIOLINK.process_regulates_process, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.process_regulated_by_process = Slot(uri=BIOLINK.process_regulated_by_process, name="process regulated by process", curie=BIOLINK.curie('process_regulated_by_process'),
                   model_uri=BIOLINK.process_regulated_by_process, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.process_positively_regulates_process = Slot(uri=BIOLINK.process_positively_regulates_process, name="process positively regulates process", curie=BIOLINK.curie('process_positively_regulates_process'),
                   model_uri=BIOLINK.process_positively_regulates_process, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.process_positively_regulated_by_process = Slot(uri=BIOLINK.process_positively_regulated_by_process, name="process positively regulated by process", curie=BIOLINK.curie('process_positively_regulated_by_process'),
                   model_uri=BIOLINK.process_positively_regulated_by_process, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.process_negatively_regulates_process = Slot(uri=BIOLINK.process_negatively_regulates_process, name="process negatively regulates process", curie=BIOLINK.curie('process_negatively_regulates_process'),
                   model_uri=BIOLINK.process_negatively_regulates_process, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.process_negatively_regulated_by_process = Slot(uri=BIOLINK.process_negatively_regulated_by_process, name="process negatively regulated by process", curie=BIOLINK.curie('process_negatively_regulated_by_process'),
                   model_uri=BIOLINK.process_negatively_regulated_by_process, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.entity_regulates_entity = Slot(uri=BIOLINK.entity_regulates_entity, name="entity regulates entity", curie=BIOLINK.curie('entity_regulates_entity'),
                   model_uri=BIOLINK.entity_regulates_entity, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.entity_regulated_by_entity = Slot(uri=BIOLINK.entity_regulated_by_entity, name="entity regulated by entity", curie=BIOLINK.curie('entity_regulated_by_entity'),
                   model_uri=BIOLINK.entity_regulated_by_entity, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.entity_positively_regulates_entity = Slot(uri=BIOLINK.entity_positively_regulates_entity, name="entity positively regulates entity", curie=BIOLINK.curie('entity_positively_regulates_entity'),
                   model_uri=BIOLINK.entity_positively_regulates_entity, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.entity_positively_regulated_by_entity = Slot(uri=BIOLINK.entity_positively_regulated_by_entity, name="entity positively regulated by entity", curie=BIOLINK.curie('entity_positively_regulated_by_entity'),
                   model_uri=BIOLINK.entity_positively_regulated_by_entity, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.entity_negatively_regulates_entity = Slot(uri=BIOLINK.entity_negatively_regulates_entity, name="entity negatively regulates entity", curie=BIOLINK.curie('entity_negatively_regulates_entity'),
                   model_uri=BIOLINK.entity_negatively_regulates_entity, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.entity_negatively_regulated_by_entity = Slot(uri=BIOLINK.entity_negatively_regulated_by_entity, name="entity negatively regulated by entity", curie=BIOLINK.curie('entity_negatively_regulated_by_entity'),
                   model_uri=BIOLINK.entity_negatively_regulated_by_entity, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.disrupts = Slot(uri=BIOLINK.disrupts, name="disrupts", curie=BIOLINK.curie('disrupts'),
                   model_uri=BIOLINK.disrupts, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.disrupted_by = Slot(uri=BIOLINK.disrupted_by, name="disrupted by", curie=BIOLINK.curie('disrupted_by'),
                   model_uri=BIOLINK.disrupted_by, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.gene_product_of = Slot(uri=BIOLINK.gene_product_of, name="gene product of", curie=BIOLINK.curie('gene_product_of'),
                   model_uri=BIOLINK.gene_product_of, domain=None, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.has_gene_product = Slot(uri=BIOLINK.has_gene_product, name="has gene product", curie=BIOLINK.curie('has_gene_product'),
                   model_uri=BIOLINK.has_gene_product, domain=Gene, range=Optional[Union[Union[dict, "GeneProductMixin"], List[Union[dict, "GeneProductMixin"]]]])

slots.transcribed_to = Slot(uri=BIOLINK.transcribed_to, name="transcribed to", curie=BIOLINK.curie('transcribed_to'),
                   model_uri=BIOLINK.transcribed_to, domain=Gene, range=Optional[Union[Union[str, TranscriptId], List[Union[str, TranscriptId]]]])

slots.transcribed_from = Slot(uri=BIOLINK.transcribed_from, name="transcribed from", curie=BIOLINK.curie('transcribed_from'),
                   model_uri=BIOLINK.transcribed_from, domain=Transcript, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.translates_to = Slot(uri=BIOLINK.translates_to, name="translates to", curie=BIOLINK.curie('translates_to'),
                   model_uri=BIOLINK.translates_to, domain=Transcript, range=Optional[Union[Union[str, ProteinId], List[Union[str, ProteinId]]]])

slots.translation_of = Slot(uri=BIOLINK.translation_of, name="translation of", curie=BIOLINK.curie('translation_of'),
                   model_uri=BIOLINK.translation_of, domain=Protein, range=Optional[Union[Union[str, TranscriptId], List[Union[str, TranscriptId]]]])

slots.homologous_to = Slot(uri=BIOLINK.homologous_to, name="homologous to", curie=BIOLINK.curie('homologous_to'),
                   model_uri=BIOLINK.homologous_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.paralogous_to = Slot(uri=BIOLINK.paralogous_to, name="paralogous to", curie=BIOLINK.curie('paralogous_to'),
                   model_uri=BIOLINK.paralogous_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.orthologous_to = Slot(uri=BIOLINK.orthologous_to, name="orthologous to", curie=BIOLINK.curie('orthologous_to'),
                   model_uri=BIOLINK.orthologous_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.xenologous_to = Slot(uri=BIOLINK.xenologous_to, name="xenologous to", curie=BIOLINK.curie('xenologous_to'),
                   model_uri=BIOLINK.xenologous_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.coexists_with = Slot(uri=BIOLINK.coexists_with, name="coexists with", curie=BIOLINK.curie('coexists_with'),
                   model_uri=BIOLINK.coexists_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.in_pathway_with = Slot(uri=BIOLINK.in_pathway_with, name="in pathway with", curie=BIOLINK.curie('in_pathway_with'),
                   model_uri=BIOLINK.in_pathway_with, domain=None, range=Optional[Union[Union[dict, "GeneOrGeneProduct"], List[Union[dict, "GeneOrGeneProduct"]]]])

slots.in_complex_with = Slot(uri=BIOLINK.in_complex_with, name="in complex with", curie=BIOLINK.curie('in_complex_with'),
                   model_uri=BIOLINK.in_complex_with, domain=None, range=Optional[Union[Union[dict, "GeneOrGeneProduct"], List[Union[dict, "GeneOrGeneProduct"]]]])

slots.in_cell_population_with = Slot(uri=BIOLINK.in_cell_population_with, name="in cell population with", curie=BIOLINK.curie('in_cell_population_with'),
                   model_uri=BIOLINK.in_cell_population_with, domain=None, range=Optional[Union[Union[dict, "GeneOrGeneProduct"], List[Union[dict, "GeneOrGeneProduct"]]]])

slots.colocalizes_with = Slot(uri=BIOLINK.colocalizes_with, name="colocalizes with", curie=BIOLINK.curie('colocalizes_with'),
                   model_uri=BIOLINK.colocalizes_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.genetic_association = Slot(uri=BIOLINK.genetic_association, name="genetic association", curie=BIOLINK.curie('genetic_association'),
                   model_uri=BIOLINK.genetic_association, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.gene_associated_with_condition = Slot(uri=BIOLINK.gene_associated_with_condition, name="gene associated with condition", curie=BIOLINK.curie('gene_associated_with_condition'),
                   model_uri=BIOLINK.gene_associated_with_condition, domain=Gene, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.condition_associated_with_gene = Slot(uri=BIOLINK.condition_associated_with_gene, name="condition associated with gene", curie=BIOLINK.curie('condition_associated_with_gene'),
                   model_uri=BIOLINK.condition_associated_with_gene, domain=DiseaseOrPhenotypicFeature, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.affects_risk_for = Slot(uri=BIOLINK.affects_risk_for, name="affects risk for", curie=BIOLINK.curie('affects_risk_for'),
                   model_uri=BIOLINK.affects_risk_for, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.predisposes = Slot(uri=BIOLINK.predisposes, name="predisposes", curie=BIOLINK.curie('predisposes'),
                   model_uri=BIOLINK.predisposes, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.contributes_to = Slot(uri=BIOLINK.contributes_to, name="contributes to", curie=BIOLINK.curie('contributes_to'),
                   model_uri=BIOLINK.contributes_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.causes = Slot(uri=BIOLINK.causes, name="causes", curie=BIOLINK.curie('causes'),
                   model_uri=BIOLINK.causes, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.caused_by = Slot(uri=BIOLINK.caused_by, name="caused by", curie=BIOLINK.curie('caused_by'),
                   model_uri=BIOLINK.caused_by, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.ameliorates = Slot(uri=BIOLINK.ameliorates, name="ameliorates", curie=BIOLINK.curie('ameliorates'),
                   model_uri=BIOLINK.ameliorates, domain=BiologicalEntity, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.exacerbates = Slot(uri=BIOLINK.exacerbates, name="exacerbates", curie=BIOLINK.curie('exacerbates'),
                   model_uri=BIOLINK.exacerbates, domain=BiologicalEntity, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.treats = Slot(uri=BIOLINK.treats, name="treats", curie=BIOLINK.curie('treats'),
                   model_uri=BIOLINK.treats, domain=None, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.treated_by = Slot(uri=BIOLINK.treated_by, name="treated by", curie=BIOLINK.curie('treated_by'),
                   model_uri=BIOLINK.treated_by, domain=DiseaseOrPhenotypicFeature, range=Optional[Union[Union[str, TreatmentId], List[Union[str, TreatmentId]]]])

slots.approved_to_treat = Slot(uri=BIOLINK.approved_to_treat, name="approved to treat", curie=BIOLINK.curie('approved_to_treat'),
                   model_uri=BIOLINK.approved_to_treat, domain=None, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.approved_for_treatment_by = Slot(uri=BIOLINK.approved_for_treatment_by, name="approved for treatment by", curie=BIOLINK.curie('approved_for_treatment_by'),
                   model_uri=BIOLINK.approved_for_treatment_by, domain=DiseaseOrPhenotypicFeature, range=Optional[Union[Union[str, TreatmentId], List[Union[str, TreatmentId]]]])

slots.prevents = Slot(uri=BIOLINK.prevents, name="prevents", curie=BIOLINK.curie('prevents'),
                   model_uri=BIOLINK.prevents, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.prevented_by = Slot(uri=BIOLINK.prevented_by, name="prevented by", curie=BIOLINK.curie('prevented_by'),
                   model_uri=BIOLINK.prevented_by, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.correlated_with = Slot(uri=BIOLINK.correlated_with, name="correlated with", curie=BIOLINK.curie('correlated_with'),
                   model_uri=BIOLINK.correlated_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.positively_correlated_with = Slot(uri=BIOLINK.positively_correlated_with, name="positively correlated with", curie=BIOLINK.curie('positively_correlated_with'),
                   model_uri=BIOLINK.positively_correlated_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.negatively_correlated_with = Slot(uri=BIOLINK.negatively_correlated_with, name="negatively correlated with", curie=BIOLINK.curie('negatively_correlated_with'),
                   model_uri=BIOLINK.negatively_correlated_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.coexpressed_with = Slot(uri=BIOLINK.coexpressed_with, name="coexpressed with", curie=BIOLINK.curie('coexpressed_with'),
                   model_uri=BIOLINK.coexpressed_with, domain=None, range=Optional[Union[Union[dict, "GeneOrGeneProduct"], List[Union[dict, "GeneOrGeneProduct"]]]])

slots.has_biomarker = Slot(uri=BIOLINK.has_biomarker, name="has biomarker", curie=BIOLINK.curie('has_biomarker'),
                   model_uri=BIOLINK.has_biomarker, domain=DiseaseOrPhenotypicFeature, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.biomarker_for = Slot(uri=BIOLINK.biomarker_for, name="biomarker for", curie=BIOLINK.curie('biomarker_for'),
                   model_uri=BIOLINK.biomarker_for, domain=MolecularEntity, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.expressed_in = Slot(uri=BIOLINK.expressed_in, name="expressed in", curie=BIOLINK.curie('expressed_in'),
                   model_uri=BIOLINK.expressed_in, domain=None, range=Optional[Union[Union[str, AnatomicalEntityId], List[Union[str, AnatomicalEntityId]]]])

slots.expresses = Slot(uri=BIOLINK.expresses, name="expresses", curie=BIOLINK.curie('expresses'),
                   model_uri=BIOLINK.expresses, domain=AnatomicalEntity, range=Optional[Union[Union[dict, "GeneOrGeneProduct"], List[Union[dict, "GeneOrGeneProduct"]]]])

slots.has_phenotype = Slot(uri=BIOLINK.has_phenotype, name="has phenotype", curie=BIOLINK.curie('has_phenotype'),
                   model_uri=BIOLINK.has_phenotype, domain=BiologicalEntity, range=Optional[Union[Union[str, PhenotypicFeatureId], List[Union[str, PhenotypicFeatureId]]]])

slots.phenotype_of = Slot(uri=BIOLINK.phenotype_of, name="phenotype of", curie=BIOLINK.curie('phenotype_of'),
                   model_uri=BIOLINK.phenotype_of, domain=PhenotypicFeature, range=Optional[Union[Union[str, BiologicalEntityId], List[Union[str, BiologicalEntityId]]]])

slots.occurs_in = Slot(uri=BIOLINK.occurs_in, name="occurs in", curie=BIOLINK.curie('occurs_in'),
                   model_uri=BIOLINK.occurs_in, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.located_in = Slot(uri=BIOLINK.located_in, name="located in", curie=BIOLINK.curie('located_in'),
                   model_uri=BIOLINK.located_in, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.location_of = Slot(uri=BIOLINK.location_of, name="location of", curie=BIOLINK.curie('location_of'),
                   model_uri=BIOLINK.location_of, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.similar_to = Slot(uri=BIOLINK.similar_to, name="similar to", curie=BIOLINK.curie('similar_to'),
                   model_uri=BIOLINK.similar_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.chemically_similar_to = Slot(uri=BIOLINK.chemically_similar_to, name="chemically similar to", curie=BIOLINK.curie('chemically_similar_to'),
                   model_uri=BIOLINK.chemically_similar_to, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_sequence_location = Slot(uri=BIOLINK.has_sequence_location, name="has sequence location", curie=BIOLINK.curie('has_sequence_location'),
                   model_uri=BIOLINK.has_sequence_location, domain=GenomicEntity, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.model_of = Slot(uri=BIOLINK.model_of, name="model of", curie=BIOLINK.curie('model_of'),
                   model_uri=BIOLINK.model_of, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.overlaps = Slot(uri=BIOLINK.overlaps, name="overlaps", curie=BIOLINK.curie('overlaps'),
                   model_uri=BIOLINK.overlaps, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_part = Slot(uri=BIOLINK.has_part, name="has part", curie=BIOLINK.curie('has_part'),
                   model_uri=BIOLINK.has_part, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.part_of = Slot(uri=BIOLINK.part_of, name="part of", curie=BIOLINK.curie('part_of'),
                   model_uri=BIOLINK.part_of, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_input = Slot(uri=BIOLINK.has_input, name="has input", curie=BIOLINK.curie('has_input'),
                   model_uri=BIOLINK.has_input, domain=None, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_output = Slot(uri=BIOLINK.has_output, name="has output", curie=BIOLINK.curie('has_output'),
                   model_uri=BIOLINK.has_output, domain=None, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_participant = Slot(uri=BIOLINK.has_participant, name="has participant", curie=BIOLINK.curie('has_participant'),
                   model_uri=BIOLINK.has_participant, domain=None, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.participates_in = Slot(uri=BIOLINK.participates_in, name="participates in", curie=BIOLINK.curie('participates_in'),
                   model_uri=BIOLINK.participates_in, domain=NamedThing, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.actively_involved_in = Slot(uri=BIOLINK.actively_involved_in, name="actively involved in", curie=BIOLINK.curie('actively_involved_in'),
                   model_uri=BIOLINK.actively_involved_in, domain=NamedThing, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.capable_of = Slot(uri=BIOLINK.capable_of, name="capable of", curie=BIOLINK.curie('capable_of'),
                   model_uri=BIOLINK.capable_of, domain=NamedThing, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.enables = Slot(uri=BIOLINK.enables, name="enables", curie=BIOLINK.curie('enables'),
                   model_uri=BIOLINK.enables, domain=PhysicalEntity, range=Optional[Union[Union[str, BiologicalProcessOrActivityId], List[Union[str, BiologicalProcessOrActivityId]]]])

slots.enabled_by = Slot(uri=BIOLINK.enabled_by, name="enabled by", curie=BIOLINK.curie('enabled_by'),
                   model_uri=BIOLINK.enabled_by, domain=BiologicalProcessOrActivity, range=Optional[Union[Union[str, PhysicalEntityId], List[Union[str, PhysicalEntityId]]]])

slots.derives_into = Slot(uri=BIOLINK.derives_into, name="derives into", curie=BIOLINK.curie('derives_into'),
                   model_uri=BIOLINK.derives_into, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.derives_from = Slot(uri=BIOLINK.derives_from, name="derives from", curie=BIOLINK.curie('derives_from'),
                   model_uri=BIOLINK.derives_from, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.is_metabolite_of = Slot(uri=BIOLINK.is_metabolite_of, name="is metabolite of", curie=BIOLINK.curie('is_metabolite_of'),
                   model_uri=BIOLINK.is_metabolite_of, domain=ChemicalSubstance, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.has_metabolite = Slot(uri=BIOLINK.has_metabolite, name="has metabolite", curie=BIOLINK.curie('has_metabolite'),
                   model_uri=BIOLINK.has_metabolite, domain=ChemicalSubstance, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.food_component_of = Slot(uri=BIOLINK.food_component_of, name="food component of", curie=BIOLINK.curie('food_component_of'),
                   model_uri=BIOLINK.food_component_of, domain=ChemicalSubstance, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.has_food_component = Slot(uri=BIOLINK.has_food_component, name="has food component", curie=BIOLINK.curie('has_food_component'),
                   model_uri=BIOLINK.has_food_component, domain=ChemicalSubstance, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.nutrient_of = Slot(uri=BIOLINK.nutrient_of, name="nutrient of", curie=BIOLINK.curie('nutrient_of'),
                   model_uri=BIOLINK.nutrient_of, domain=ChemicalSubstance, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.has_nutrient = Slot(uri=BIOLINK.has_nutrient, name="has nutrient", curie=BIOLINK.curie('has_nutrient'),
                   model_uri=BIOLINK.has_nutrient, domain=ChemicalSubstance, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.is_active_ingredient_of = Slot(uri=BIOLINK.is_active_ingredient_of, name="is active ingredient of", curie=BIOLINK.curie('is_active_ingredient_of'),
                   model_uri=BIOLINK.is_active_ingredient_of, domain=ChemicalSubstance, range=Optional[Union[Union[str, DrugId], List[Union[str, DrugId]]]], mappings = [OBOREL["0002249"]])

slots.has_active_ingredient = Slot(uri=BIOLINK.has_active_ingredient, name="has active ingredient", curie=BIOLINK.curie('has_active_ingredient'),
                   model_uri=BIOLINK.has_active_ingredient, domain=Drug, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]], mappings = [OBOREL["0002248"]])

slots.is_excipient_of = Slot(uri=BIOLINK.is_excipient_of, name="is excipient of", curie=BIOLINK.curie('is_excipient_of'),
                   model_uri=BIOLINK.is_excipient_of, domain=ChemicalSubstance, range=Optional[Union[Union[str, DrugId], List[Union[str, DrugId]]]], mappings = [WIKIDATA.Q902638])

slots.has_excipient = Slot(uri=BIOLINK.has_excipient, name="has excipient", curie=BIOLINK.curie('has_excipient'),
                   model_uri=BIOLINK.has_excipient, domain=Drug, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]], mappings = [WIKIDATA.Q902638])

slots.manifestation_of = Slot(uri=BIOLINK.manifestation_of, name="manifestation of", curie=BIOLINK.curie('manifestation_of'),
                   model_uri=BIOLINK.manifestation_of, domain=NamedThing, range=Optional[Union[Union[str, DiseaseId], List[Union[str, DiseaseId]]]])

slots.produces = Slot(uri=BIOLINK.produces, name="produces", curie=BIOLINK.curie('produces'),
                   model_uri=BIOLINK.produces, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.produced_by = Slot(uri=BIOLINK.produced_by, name="produced by", curie=BIOLINK.curie('produced_by'),
                   model_uri=BIOLINK.produced_by, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.temporally_related_to = Slot(uri=BIOLINK.temporally_related_to, name="temporally related to", curie=BIOLINK.curie('temporally_related_to'),
                   model_uri=BIOLINK.temporally_related_to, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.precedes = Slot(uri=BIOLINK.precedes, name="precedes", curie=BIOLINK.curie('precedes'),
                   model_uri=BIOLINK.precedes, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.preceded_by = Slot(uri=BIOLINK.preceded_by, name="preceded by", curie=BIOLINK.curie('preceded_by'),
                   model_uri=BIOLINK.preceded_by, domain=None, range=Optional[Union[Union[dict, "Occurrent"], List[Union[dict, "Occurrent"]]]])

slots.directly_interacts_with = Slot(uri=BIOLINK.directly_interacts_with, name="directly interacts with", curie=BIOLINK.curie('directly_interacts_with'),
                   model_uri=BIOLINK.directly_interacts_with, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.affects_expression_in = Slot(uri=BIOLINK.affects_expression_in, name="affects expression in", curie=BIOLINK.curie('affects_expression_in'),
                   model_uri=BIOLINK.affects_expression_in, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_variant_part = Slot(uri=BIOLINK.has_variant_part, name="has variant part", curie=BIOLINK.curie('has_variant_part'),
                   model_uri=BIOLINK.has_variant_part, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.related_condition = Slot(uri=BIOLINK.related_condition, name="related condition", curie=BIOLINK.curie('related_condition'),
                   model_uri=BIOLINK.related_condition, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.is_sequence_variant_of = Slot(uri=BIOLINK.is_sequence_variant_of, name="is sequence variant of", curie=BIOLINK.curie('is_sequence_variant_of'),
                   model_uri=BIOLINK.is_sequence_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GenomicEntityId], List[Union[str, GenomicEntityId]]]])

slots.is_missense_variant_of = Slot(uri=BIOLINK.is_missense_variant_of, name="is missense variant of", curie=BIOLINK.curie('is_missense_variant_of'),
                   model_uri=BIOLINK.is_missense_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.is_synonymous_variant_of = Slot(uri=BIOLINK.is_synonymous_variant_of, name="is synonymous variant of", curie=BIOLINK.curie('is_synonymous_variant_of'),
                   model_uri=BIOLINK.is_synonymous_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.is_nonsense_variant_of = Slot(uri=BIOLINK.is_nonsense_variant_of, name="is nonsense variant of", curie=BIOLINK.curie('is_nonsense_variant_of'),
                   model_uri=BIOLINK.is_nonsense_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.is_frameshift_variant_of = Slot(uri=BIOLINK.is_frameshift_variant_of, name="is frameshift variant of", curie=BIOLINK.curie('is_frameshift_variant_of'),
                   model_uri=BIOLINK.is_frameshift_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.is_splice_site_variant_of = Slot(uri=BIOLINK.is_splice_site_variant_of, name="is splice site variant of", curie=BIOLINK.curie('is_splice_site_variant_of'),
                   model_uri=BIOLINK.is_splice_site_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.is_nearby_variant_of = Slot(uri=BIOLINK.is_nearby_variant_of, name="is nearby variant of", curie=BIOLINK.curie('is_nearby_variant_of'),
                   model_uri=BIOLINK.is_nearby_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.is_non_coding_variant_of = Slot(uri=BIOLINK.is_non_coding_variant_of, name="is non coding variant of", curie=BIOLINK.curie('is_non_coding_variant_of'),
                   model_uri=BIOLINK.is_non_coding_variant_of, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.disease_has_basis_in = Slot(uri=BIOLINK.disease_has_basis_in, name="disease has basis in", curie=BIOLINK.curie('disease_has_basis_in'),
                   model_uri=BIOLINK.disease_has_basis_in, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.causes_adverse_event = Slot(uri=BIOLINK.causes_adverse_event, name="causes adverse event", curie=BIOLINK.curie('causes_adverse_event'),
                   model_uri=BIOLINK.causes_adverse_event, domain=Drug, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.contraindicated_for = Slot(uri=BIOLINK.contraindicated_for, name="contraindicated for", curie=BIOLINK.curie('contraindicated_for'),
                   model_uri=BIOLINK.contraindicated_for, domain=Drug, range=Optional[Union[Union[str, DiseaseOrPhenotypicFeatureId], List[Union[str, DiseaseOrPhenotypicFeatureId]]]])

slots.has_not_completed = Slot(uri=BIOLINK.has_not_completed, name="has not completed", curie=BIOLINK.curie('has_not_completed'),
                   model_uri=BIOLINK.has_not_completed, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_completed = Slot(uri=BIOLINK.has_completed, name="has completed", curie=BIOLINK.curie('has_completed'),
                   model_uri=BIOLINK.has_completed, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.decreases_molecular_interaction = Slot(uri=BIOLINK.decreases_molecular_interaction, name="decreases molecular interaction", curie=BIOLINK.curie('decreases_molecular_interaction'),
                   model_uri=BIOLINK.decreases_molecular_interaction, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.increases_molecular_interaction = Slot(uri=BIOLINK.increases_molecular_interaction, name="increases molecular interaction", curie=BIOLINK.curie('increases_molecular_interaction'),
                   model_uri=BIOLINK.increases_molecular_interaction, domain=MolecularEntity, range=Optional[Union[Union[str, MolecularEntityId], List[Union[str, MolecularEntityId]]]])

slots.in_linkage_disequilibrium_with = Slot(uri=BIOLINK.in_linkage_disequilibrium_with, name="in linkage disequilibrium with", curie=BIOLINK.curie('in_linkage_disequilibrium_with'),
                   model_uri=BIOLINK.in_linkage_disequilibrium_with, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_increased_amount = Slot(uri=BIOLINK.has_increased_amount, name="has increased amount", curie=BIOLINK.curie('has_increased_amount'),
                   model_uri=BIOLINK.has_increased_amount, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.has_decreased_amount = Slot(uri=BIOLINK.has_decreased_amount, name="has decreased amount", curie=BIOLINK.curie('has_decreased_amount'),
                   model_uri=BIOLINK.has_decreased_amount, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.lacks_part = Slot(uri=BIOLINK.lacks_part, name="lacks part", curie=BIOLINK.curie('lacks_part'),
                   model_uri=BIOLINK.lacks_part, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.develops_from = Slot(uri=BIOLINK.develops_from, name="develops from", curie=BIOLINK.curie('develops_from'),
                   model_uri=BIOLINK.develops_from, domain=NamedThing, range=Optional[Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]]])

slots.in_taxon = Slot(uri=BIOLINK.in_taxon, name="in taxon", curie=BIOLINK.curie('in_taxon'),
                   model_uri=BIOLINK.in_taxon, domain=None, range=Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]])

slots.has_molecular_consequence = Slot(uri=BIOLINK.has_molecular_consequence, name="has molecular consequence", curie=BIOLINK.curie('has_molecular_consequence'),
                   model_uri=BIOLINK.has_molecular_consequence, domain=NamedThing, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.association_slot = Slot(uri=BIOLINK.association_slot, name="association slot", curie=BIOLINK.curie('association_slot'),
                   model_uri=BIOLINK.association_slot, domain=Association, range=Optional[str])

slots.association_id = Slot(uri=BIOLINK.id, name="association_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.association_id, domain=Association, range=Union[str, AssociationId])

slots.subject = Slot(uri=RDF.subject, name="subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.subject, domain=Association, range=Union[str, NamedThingId])

slots.object = Slot(uri=RDF.object, name="object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.object, domain=Association, range=Union[str, NamedThingId])

slots.predicate = Slot(uri=RDF.predicate, name="predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.predicate, domain=Association, range=Union[str, PredicateType])

slots.edge_label = Slot(uri=RDF.predicate, name="edge label", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.edge_label, domain=Association, range=Union[str, PredicateType])

slots.logical_interpretation = Slot(uri=BIOLINK.logical_interpretation, name="logical interpretation", curie=BIOLINK.curie('logical_interpretation'),
                   model_uri=BIOLINK.logical_interpretation, domain=Association, range=Optional[Union[str, "LogicalInterpretationEnum"]])

slots.relation = Slot(uri=BIOLINK.relation, name="relation", curie=BIOLINK.curie('relation'),
                   model_uri=BIOLINK.relation, domain=Association, range=Union[str, URIorCURIE])

slots.negated = Slot(uri=BIOLINK.negated, name="negated", curie=BIOLINK.curie('negated'),
                   model_uri=BIOLINK.negated, domain=Association, range=Optional[Union[bool, Bool]])

slots.has_confidence_level = Slot(uri=BIOLINK.has_confidence_level, name="has confidence level", curie=BIOLINK.curie('has_confidence_level'),
                   model_uri=BIOLINK.has_confidence_level, domain=Association, range=Optional[Union[str, ConfidenceLevelId]])

slots.has_evidence = Slot(uri=BIOLINK.has_evidence, name="has evidence", curie=BIOLINK.curie('has_evidence'),
                   model_uri=BIOLINK.has_evidence, domain=Association, range=Optional[Union[str, EvidenceTypeId]])

slots.provided_by = Slot(uri=BIOLINK.provided_by, name="provided by", curie=BIOLINK.curie('provided_by'),
                   model_uri=BIOLINK.provided_by, domain=Association, range=Optional[Union[Union[str, AgentId], List[Union[str, AgentId]]]])

slots.association_type = Slot(uri=BIOLINK.association_type, name="association type", curie=BIOLINK.curie('association_type'),
                   model_uri=BIOLINK.association_type, domain=Association, range=Optional[Union[str, CategoryType]])

slots.chi_squared_statistic = Slot(uri=BIOLINK.chi_squared_statistic, name="chi squared statistic", curie=BIOLINK.curie('chi_squared_statistic'),
                   model_uri=BIOLINK.chi_squared_statistic, domain=Association, range=Optional[float])

slots.p_value = Slot(uri=BIOLINK.p_value, name="p value", curie=BIOLINK.curie('p_value'),
                   model_uri=BIOLINK.p_value, domain=Association, range=Optional[float])

slots.interacting_molecules_category = Slot(uri=BIOLINK.interacting_molecules_category, name="interacting molecules category", curie=BIOLINK.curie('interacting_molecules_category'),
                   model_uri=BIOLINK.interacting_molecules_category, domain=Association, range=Optional[Union[dict, OntologyClass]])

slots.quantifier_qualifier = Slot(uri=BIOLINK.quantifier_qualifier, name="quantifier qualifier", curie=BIOLINK.curie('quantifier_qualifier'),
                   model_uri=BIOLINK.quantifier_qualifier, domain=Association, range=Optional[Union[dict, OntologyClass]])

slots.catalyst_qualifier = Slot(uri=BIOLINK.catalyst_qualifier, name="catalyst qualifier", curie=BIOLINK.curie('catalyst_qualifier'),
                   model_uri=BIOLINK.catalyst_qualifier, domain=Association, range=Optional[Union[Union[dict, MacromolecularMachineMixin], List[Union[dict, MacromolecularMachineMixin]]]])

slots.expression_site = Slot(uri=BIOLINK.expression_site, name="expression site", curie=BIOLINK.curie('expression_site'),
                   model_uri=BIOLINK.expression_site, domain=Association, range=Optional[Union[str, AnatomicalEntityId]])

slots.stage_qualifier = Slot(uri=BIOLINK.stage_qualifier, name="stage qualifier", curie=BIOLINK.curie('stage_qualifier'),
                   model_uri=BIOLINK.stage_qualifier, domain=Association, range=Optional[Union[str, LifeStageId]])

slots.phenotypic_state = Slot(uri=BIOLINK.phenotypic_state, name="phenotypic state", curie=BIOLINK.curie('phenotypic_state'),
                   model_uri=BIOLINK.phenotypic_state, domain=Association, range=Optional[Union[str, DiseaseOrPhenotypicFeatureId]])

slots.qualifiers = Slot(uri=BIOLINK.qualifiers, name="qualifiers", curie=BIOLINK.curie('qualifiers'),
                   model_uri=BIOLINK.qualifiers, domain=Association, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.frequency_qualifier = Slot(uri=BIOLINK.frequency_qualifier, name="frequency qualifier", curie=BIOLINK.curie('frequency_qualifier'),
                   model_uri=BIOLINK.frequency_qualifier, domain=Association, range=Optional[Union[str, FrequencyValue]])

slots.severity_qualifier = Slot(uri=BIOLINK.severity_qualifier, name="severity qualifier", curie=BIOLINK.curie('severity_qualifier'),
                   model_uri=BIOLINK.severity_qualifier, domain=Association, range=Optional[Union[dict, SeverityValue]])

slots.sex_qualifier = Slot(uri=BIOLINK.sex_qualifier, name="sex qualifier", curie=BIOLINK.curie('sex_qualifier'),
                   model_uri=BIOLINK.sex_qualifier, domain=Association, range=Optional[Union[dict, BiologicalSex]])

slots.onset_qualifier = Slot(uri=BIOLINK.onset_qualifier, name="onset qualifier", curie=BIOLINK.curie('onset_qualifier'),
                   model_uri=BIOLINK.onset_qualifier, domain=Association, range=Optional[Union[dict, Onset]])

slots.clinical_modifier_qualifier = Slot(uri=BIOLINK.clinical_modifier_qualifier, name="clinical modifier qualifier", curie=BIOLINK.curie('clinical_modifier_qualifier'),
                   model_uri=BIOLINK.clinical_modifier_qualifier, domain=Association, range=Optional[Union[dict, ClinicalModifier]])

slots.sequence_variant_qualifier = Slot(uri=BIOLINK.sequence_variant_qualifier, name="sequence variant qualifier", curie=BIOLINK.curie('sequence_variant_qualifier'),
                   model_uri=BIOLINK.sequence_variant_qualifier, domain=Association, range=Optional[Union[str, SequenceVariantId]])

slots.publications = Slot(uri=BIOLINK.publications, name="publications", curie=BIOLINK.curie('publications'),
                   model_uri=BIOLINK.publications, domain=Association, range=Optional[Union[Union[str, PublicationId], List[Union[str, PublicationId]]]])

slots.associated_environmental_context = Slot(uri=BIOLINK.associated_environmental_context, name="associated environmental context", curie=BIOLINK.curie('associated_environmental_context'),
                   model_uri=BIOLINK.associated_environmental_context, domain=Association, range=Optional[str])

slots.sequence_localization_attribute = Slot(uri=BIOLINK.sequence_localization_attribute, name="sequence localization attribute", curie=BIOLINK.curie('sequence_localization_attribute'),
                   model_uri=BIOLINK.sequence_localization_attribute, domain=GenomicSequenceLocalization, range=Optional[str])

slots.interbase_coordinate = Slot(uri=BIOLINK.interbase_coordinate, name="interbase coordinate", curie=BIOLINK.curie('interbase_coordinate'),
                   model_uri=BIOLINK.interbase_coordinate, domain=GenomicSequenceLocalization, range=Optional[int])

slots.start_interbase_coordinate = Slot(uri=BIOLINK.start_interbase_coordinate, name="start interbase coordinate", curie=BIOLINK.curie('start_interbase_coordinate'),
                   model_uri=BIOLINK.start_interbase_coordinate, domain=GenomicSequenceLocalization, range=Optional[int])

slots.end_interbase_coordinate = Slot(uri=BIOLINK.end_interbase_coordinate, name="end interbase coordinate", curie=BIOLINK.curie('end_interbase_coordinate'),
                   model_uri=BIOLINK.end_interbase_coordinate, domain=GenomicSequenceLocalization, range=Optional[int])

slots.genome_build = Slot(uri=BIOLINK.genome_build, name="genome build", curie=BIOLINK.curie('genome_build'),
                   model_uri=BIOLINK.genome_build, domain=GenomicSequenceLocalization, range=Optional[str])

slots.strand = Slot(uri=BIOLINK.strand, name="strand", curie=BIOLINK.curie('strand'),
                   model_uri=BIOLINK.strand, domain=GenomicSequenceLocalization, range=Optional[str])

slots.phase = Slot(uri=BIOLINK.phase, name="phase", curie=BIOLINK.curie('phase'),
                   model_uri=BIOLINK.phase, domain=CodingSequence, range=Optional[str])

slots.has_taxonomic_rank = Slot(uri=BIOLINK.has_taxonomic_rank, name="has taxonomic rank", curie=BIOLINK.curie('has_taxonomic_rank'),
                   model_uri=BIOLINK.has_taxonomic_rank, domain=None, range=Optional[Union[dict, TaxonomicRank]], mappings = [WIKIDATA.P105])

slots.attribute_name = Slot(uri=RDFS.label, name="attribute_name", curie=RDFS.curie('label'),
                   model_uri=BIOLINK.attribute_name, domain=Attribute, range=Optional[Union[str, LabelType]])

slots.named_thing_category = Slot(uri=BIOLINK.category, name="named thing_category", curie=BIOLINK.curie('category'),
                   model_uri=BIOLINK.named_thing_category, domain=NamedThing, range=Union[Union[str, NamedThingId], List[Union[str, NamedThingId]]])

slots.organism_taxon_has_taxonomic_rank = Slot(uri=BIOLINK.has_taxonomic_rank, name="organism taxon_has taxonomic rank", curie=BIOLINK.curie('has_taxonomic_rank'),
                   model_uri=BIOLINK.organism_taxon_has_taxonomic_rank, domain=OrganismTaxon, range=Optional[Union[dict, TaxonomicRank]], mappings = [WIKIDATA.P105])

slots.organism_taxon_subclass_of = Slot(uri=BIOLINK.subclass_of, name="organism taxon_subclass of", curie=BIOLINK.curie('subclass_of'),
                   model_uri=BIOLINK.organism_taxon_subclass_of, domain=OrganismTaxon, range=Optional[Union[Union[str, OrganismTaxonId], List[Union[str, OrganismTaxonId]]]])

slots.agent_id = Slot(uri=BIOLINK.id, name="agent_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.agent_id, domain=Agent, range=Union[str, AgentId])

slots.agent_name = Slot(uri=RDFS.label, name="agent_name", curie=RDFS.curie('label'),
                   model_uri=BIOLINK.agent_name, domain=Agent, range=Optional[Union[str, LabelType]])

slots.publication_id = Slot(uri=BIOLINK.id, name="publication_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.publication_id, domain=Publication, range=Union[str, PublicationId])

slots.publication_name = Slot(uri=RDFS.label, name="publication_name", curie=RDFS.curie('label'),
                   model_uri=BIOLINK.publication_name, domain=Publication, range=Optional[Union[str, LabelType]])

slots.publication_type = Slot(uri=DCT.type, name="publication_type", curie=DCT.curie('type'),
                   model_uri=BIOLINK.publication_type, domain=Publication, range=str)

slots.publication_pages = Slot(uri=BIOLINK.pages, name="publication_pages", curie=BIOLINK.curie('pages'),
                   model_uri=BIOLINK.publication_pages, domain=Publication, range=Optional[Union[str, List[str]]])

slots.book_id = Slot(uri=BIOLINK.id, name="book_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.book_id, domain=Book, range=Union[str, BookId])

slots.book_type = Slot(uri=RDF.type, name="book_type", curie=RDF.curie('type'),
                   model_uri=BIOLINK.book_type, domain=Book, range=str)

slots.book_chapter_published_in = Slot(uri=BIOLINK.published_in, name="book chapter_published in", curie=BIOLINK.curie('published_in'),
                   model_uri=BIOLINK.book_chapter_published_in, domain=BookChapter, range=Union[str, URIorCURIE])

slots.serial_id = Slot(uri=BIOLINK.id, name="serial_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.serial_id, domain=Serial, range=Union[str, SerialId])

slots.serial_type = Slot(uri=RDF.type, name="serial_type", curie=RDF.curie('type'),
                   model_uri=BIOLINK.serial_type, domain=Serial, range=str)

slots.article_published_in = Slot(uri=BIOLINK.published_in, name="article_published in", curie=BIOLINK.curie('published_in'),
                   model_uri=BIOLINK.article_published_in, domain=Article, range=Union[str, URIorCURIE])

slots.article_iso_abbreviation = Slot(uri=BIOLINK.iso_abbreviation, name="article_iso abbreviation", curie=BIOLINK.curie('iso_abbreviation'),
                   model_uri=BIOLINK.article_iso_abbreviation, domain=Article, range=Optional[str])

slots.molecular_activity_has_input = Slot(uri=BIOLINK.has_input, name="molecular activity_has input", curie=BIOLINK.curie('has_input'),
                   model_uri=BIOLINK.molecular_activity_has_input, domain=MolecularActivity, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.molecular_activity_has_output = Slot(uri=BIOLINK.has_output, name="molecular activity_has output", curie=BIOLINK.curie('has_output'),
                   model_uri=BIOLINK.molecular_activity_has_output, domain=MolecularActivity, range=Optional[Union[Union[str, ChemicalSubstanceId], List[Union[str, ChemicalSubstanceId]]]])

slots.molecular_activity_enabled_by = Slot(uri=BIOLINK.enabled_by, name="molecular activity_enabled by", curie=BIOLINK.curie('enabled_by'),
                   model_uri=BIOLINK.molecular_activity_enabled_by, domain=MolecularActivity, range=Optional[Union[Union[dict, "MacromolecularMachineMixin"], List[Union[dict, "MacromolecularMachineMixin"]]]])

slots.organismal_entity_has_attribute = Slot(uri=BIOLINK.has_attribute, name="organismal entity_has attribute", curie=BIOLINK.curie('has_attribute'),
                   model_uri=BIOLINK.organismal_entity_has_attribute, domain=OrganismalEntity, range=Optional[Union[Union[dict, Attribute], List[Union[dict, Attribute]]]])

slots.macromolecular_machine_mixin_name = Slot(uri=RDFS.label, name="macromolecular machine mixin_name", curie=RDFS.curie('label'),
                   model_uri=BIOLINK.macromolecular_machine_mixin_name, domain=None, range=Optional[Union[str, SymbolType]])

slots.sequence_variant_has_gene = Slot(uri=BIOLINK.has_gene, name="sequence variant_has gene", curie=BIOLINK.curie('has_gene'),
                   model_uri=BIOLINK.sequence_variant_has_gene, domain=SequenceVariant, range=Optional[Union[Union[str, GeneId], List[Union[str, GeneId]]]])

slots.sequence_variant_has_biological_sequence = Slot(uri=BIOLINK.has_biological_sequence, name="sequence variant_has biological sequence", curie=BIOLINK.curie('has_biological_sequence'),
                   model_uri=BIOLINK.sequence_variant_has_biological_sequence, domain=SequenceVariant, range=Optional[Union[str, BiologicalSequence]])

slots.sequence_variant_id = Slot(uri=BIOLINK.id, name="sequence variant_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.sequence_variant_id, domain=SequenceVariant, range=Union[str, SequenceVariantId])

slots.clinical_measurement_has_attribute_type = Slot(uri=BIOLINK.has_attribute_type, name="clinical measurement_has attribute type", curie=BIOLINK.curie('has_attribute_type'),
                   model_uri=BIOLINK.clinical_measurement_has_attribute_type, domain=ClinicalMeasurement, range=Union[dict, OntologyClass])

slots.clinical_finding_has_attribute = Slot(uri=BIOLINK.has_attribute, name="clinical finding_has attribute", curie=BIOLINK.curie('has_attribute'),
                   model_uri=BIOLINK.clinical_finding_has_attribute, domain=ClinicalFinding, range=Optional[Union[Union[dict, ClinicalAttribute], List[Union[dict, ClinicalAttribute]]]])

slots.socioeconomic_exposure_has_attribute = Slot(uri=BIOLINK.has_attribute, name="socioeconomic exposure_has attribute", curie=BIOLINK.curie('has_attribute'),
                   model_uri=BIOLINK.socioeconomic_exposure_has_attribute, domain=SocioeconomicExposure, range=Union[Union[dict, SocioeconomicAttribute], List[Union[dict, SocioeconomicAttribute]]])

slots.association_type = Slot(uri=RDF.type, name="association_type", curie=RDF.curie('type'),
                   model_uri=BIOLINK.association_type, domain=Association, range=Optional[str])

slots.association_category = Slot(uri=BIOLINK.category, name="association_category", curie=BIOLINK.curie('category'),
                   model_uri=BIOLINK.association_category, domain=Association, range=Optional[Union[Union[str, CategoryType], List[Union[str, CategoryType]]]])

slots.contributor_association_subject = Slot(uri=RDF.subject, name="contributor association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.contributor_association_subject, domain=ContributorAssociation, range=Union[str, InformationContentEntityId])

slots.contributor_association_predicate = Slot(uri=RDF.predicate, name="contributor association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.contributor_association_predicate, domain=ContributorAssociation, range=Union[str, PredicateType])

slots.contributor_association_object = Slot(uri=RDF.object, name="contributor association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.contributor_association_object, domain=ContributorAssociation, range=Union[str, AgentId])

slots.contributor_association_qualifiers = Slot(uri=BIOLINK.qualifiers, name="contributor association_qualifiers", curie=BIOLINK.curie('qualifiers'),
                   model_uri=BIOLINK.contributor_association_qualifiers, domain=ContributorAssociation, range=Optional[Union[Union[dict, OntologyClass], List[Union[dict, OntologyClass]]]])

slots.genotype_to_genotype_part_association_predicate = Slot(uri=RDF.predicate, name="genotype to genotype part association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.genotype_to_genotype_part_association_predicate, domain=GenotypeToGenotypePartAssociation, range=Union[str, PredicateType])

slots.genotype_to_genotype_part_association_subject = Slot(uri=RDF.subject, name="genotype to genotype part association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_to_genotype_part_association_subject, domain=GenotypeToGenotypePartAssociation, range=Union[str, GenotypeId])

slots.genotype_to_genotype_part_association_object = Slot(uri=RDF.object, name="genotype to genotype part association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.genotype_to_genotype_part_association_object, domain=GenotypeToGenotypePartAssociation, range=Union[str, GenotypeId])

slots.genotype_to_gene_association_predicate = Slot(uri=RDF.predicate, name="genotype to gene association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.genotype_to_gene_association_predicate, domain=GenotypeToGeneAssociation, range=Union[str, PredicateType])

slots.genotype_to_gene_association_subject = Slot(uri=RDF.subject, name="genotype to gene association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_to_gene_association_subject, domain=GenotypeToGeneAssociation, range=Union[str, GenotypeId])

slots.genotype_to_gene_association_object = Slot(uri=RDF.object, name="genotype to gene association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.genotype_to_gene_association_object, domain=GenotypeToGeneAssociation, range=Union[str, GeneId])

slots.genotype_to_variant_association_predicate = Slot(uri=RDF.predicate, name="genotype to variant association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.genotype_to_variant_association_predicate, domain=GenotypeToVariantAssociation, range=Union[str, PredicateType])

slots.genotype_to_variant_association_subject = Slot(uri=RDF.subject, name="genotype to variant association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_to_variant_association_subject, domain=GenotypeToVariantAssociation, range=Union[str, GenotypeId])

slots.genotype_to_variant_association_object = Slot(uri=RDF.object, name="genotype to variant association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.genotype_to_variant_association_object, domain=GenotypeToVariantAssociation, range=Union[str, SequenceVariantId])

slots.gene_to_gene_association_subject = Slot(uri=RDF.subject, name="gene to gene association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_gene_association_subject, domain=GeneToGeneAssociation, range=Union[dict, GeneOrGeneProduct])

slots.gene_to_gene_association_object = Slot(uri=RDF.object, name="gene to gene association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.gene_to_gene_association_object, domain=GeneToGeneAssociation, range=Union[dict, GeneOrGeneProduct])

slots.gene_to_gene_homology_association_predicate = Slot(uri=RDF.predicate, name="gene to gene homology association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.gene_to_gene_homology_association_predicate, domain=GeneToGeneHomologyAssociation, range=Union[str, PredicateType])

slots.gene_expression_mixin_quantifier_qualifier = Slot(uri=BIOLINK.quantifier_qualifier, name="gene expression mixin_quantifier qualifier", curie=BIOLINK.curie('quantifier_qualifier'),
                   model_uri=BIOLINK.gene_expression_mixin_quantifier_qualifier, domain=None, range=Optional[Union[dict, OntologyClass]])

slots.gene_to_gene_coexpression_association_predicate = Slot(uri=RDF.predicate, name="gene to gene coexpression association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.gene_to_gene_coexpression_association_predicate, domain=GeneToGeneCoexpressionAssociation, range=Union[str, PredicateType])

slots.pairwise_gene_to_gene_interaction_predicate = Slot(uri=RDF.predicate, name="pairwise gene to gene interaction_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.pairwise_gene_to_gene_interaction_predicate, domain=PairwiseGeneToGeneInteraction, range=Union[str, PredicateType])

slots.pairwise_gene_to_gene_interaction_relation = Slot(uri=BIOLINK.relation, name="pairwise gene to gene interaction_relation", curie=BIOLINK.curie('relation'),
                   model_uri=BIOLINK.pairwise_gene_to_gene_interaction_relation, domain=PairwiseGeneToGeneInteraction, range=Union[str, URIorCURIE])

slots.pairwise_molecular_interaction_subject = Slot(uri=RDF.subject, name="pairwise molecular interaction_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.pairwise_molecular_interaction_subject, domain=PairwiseMolecularInteraction, range=Union[str, MolecularEntityId])

slots.pairwise_molecular_interaction_id = Slot(uri=BIOLINK.id, name="pairwise molecular interaction_id", curie=BIOLINK.curie('id'),
                   model_uri=BIOLINK.pairwise_molecular_interaction_id, domain=PairwiseMolecularInteraction, range=Union[str, PairwiseMolecularInteractionId])

slots.pairwise_molecular_interaction_predicate = Slot(uri=RDF.predicate, name="pairwise molecular interaction_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.pairwise_molecular_interaction_predicate, domain=PairwiseMolecularInteraction, range=Union[str, PredicateType])

slots.pairwise_molecular_interaction_relation = Slot(uri=BIOLINK.relation, name="pairwise molecular interaction_relation", curie=BIOLINK.curie('relation'),
                   model_uri=BIOLINK.pairwise_molecular_interaction_relation, domain=PairwiseMolecularInteraction, range=Union[str, URIorCURIE])

slots.pairwise_molecular_interaction_object = Slot(uri=RDF.object, name="pairwise molecular interaction_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.pairwise_molecular_interaction_object, domain=PairwiseMolecularInteraction, range=Union[str, MolecularEntityId])

slots.cell_line_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="cell line to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.cell_line_to_entity_association_mixin_subject, domain=None, range=Union[str, CellLineId])

slots.cell_line_to_disease_or_phenotypic_feature_association_subject = Slot(uri=RDF.subject, name="cell line to disease or phenotypic feature association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.cell_line_to_disease_or_phenotypic_feature_association_subject, domain=CellLineToDiseaseOrPhenotypicFeatureAssociation, range=Union[str, DiseaseOrPhenotypicFeatureId])

slots.molecular_entity_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="molecular entity to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.molecular_entity_to_entity_association_mixin_subject, domain=None, range=Union[str, MolecularEntityId])

slots.drug_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="drug to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.drug_to_entity_association_mixin_subject, domain=None, range=Union[str, DrugId])

slots.chemical_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="chemical to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.chemical_to_entity_association_mixin_subject, domain=None, range=Union[str, ChemicalSubstanceId])

slots.case_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="case to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.case_to_entity_association_mixin_subject, domain=None, range=Union[str, CaseId])

slots.chemical_to_chemical_association_object = Slot(uri=RDF.object, name="chemical to chemical association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.chemical_to_chemical_association_object, domain=ChemicalToChemicalAssociation, range=Union[str, ChemicalSubstanceId])

slots.chemical_to_chemical_derivation_association_subject = Slot(uri=RDF.subject, name="chemical to chemical derivation association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.chemical_to_chemical_derivation_association_subject, domain=ChemicalToChemicalDerivationAssociation, range=Union[str, ChemicalSubstanceId])

slots.chemical_to_chemical_derivation_association_object = Slot(uri=RDF.object, name="chemical to chemical derivation association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.chemical_to_chemical_derivation_association_object, domain=ChemicalToChemicalDerivationAssociation, range=Union[str, ChemicalSubstanceId])

slots.chemical_to_chemical_derivation_association_predicate = Slot(uri=RDF.predicate, name="chemical to chemical derivation association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.chemical_to_chemical_derivation_association_predicate, domain=ChemicalToChemicalDerivationAssociation, range=Union[str, PredicateType])

slots.chemical_to_chemical_derivation_association_catalyst_qualifier = Slot(uri=BIOLINK.catalyst_qualifier, name="chemical to chemical derivation association_catalyst qualifier", curie=BIOLINK.curie('catalyst_qualifier'),
                   model_uri=BIOLINK.chemical_to_chemical_derivation_association_catalyst_qualifier, domain=ChemicalToChemicalDerivationAssociation, range=Optional[Union[Union[dict, MacromolecularMachineMixin], List[Union[dict, MacromolecularMachineMixin]]]])

slots.chemical_to_disease_or_phenotypic_feature_association_object = Slot(uri=RDF.object, name="chemical to disease or phenotypic feature association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.chemical_to_disease_or_phenotypic_feature_association_object, domain=ChemicalToDiseaseOrPhenotypicFeatureAssociation, range=Union[str, DiseaseOrPhenotypicFeatureId])

slots.chemical_to_pathway_association_object = Slot(uri=RDF.object, name="chemical to pathway association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.chemical_to_pathway_association_object, domain=ChemicalToPathwayAssociation, range=Union[str, PathwayId])

slots.chemical_to_gene_association_object = Slot(uri=RDF.object, name="chemical to gene association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.chemical_to_gene_association_object, domain=ChemicalToGeneAssociation, range=Union[dict, GeneOrGeneProduct])

slots.drug_to_gene_association_object = Slot(uri=RDF.object, name="drug to gene association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.drug_to_gene_association_object, domain=DrugToGeneAssociation, range=Union[dict, GeneOrGeneProduct])

slots.material_sample_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="material sample to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.material_sample_to_entity_association_mixin_subject, domain=None, range=Union[str, MaterialSampleId])

slots.material_sample_derivation_association_subject = Slot(uri=RDF.subject, name="material sample derivation association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.material_sample_derivation_association_subject, domain=MaterialSampleDerivationAssociation, range=Union[str, MaterialSampleId])

slots.material_sample_derivation_association_object = Slot(uri=RDF.object, name="material sample derivation association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.material_sample_derivation_association_object, domain=MaterialSampleDerivationAssociation, range=Union[str, NamedThingId])

slots.material_sample_derivation_association_predicate = Slot(uri=RDF.predicate, name="material sample derivation association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.material_sample_derivation_association_predicate, domain=MaterialSampleDerivationAssociation, range=Union[str, PredicateType])

slots.disease_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="disease to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.disease_to_entity_association_mixin_subject, domain=None, range=Union[str, DiseaseId])

slots.entity_to_exposure_event_association_mixin_object = Slot(uri=RDF.object, name="entity to exposure event association mixin_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.entity_to_exposure_event_association_mixin_object, domain=None, range=Union[dict, ExposureEvent])

slots.exposure_event_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="exposure event to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.exposure_event_to_entity_association_mixin_subject, domain=None, range=Union[dict, ExposureEvent])

slots.entity_to_outcome_association_mixin_object = Slot(uri=RDF.object, name="entity to outcome association mixin_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.entity_to_outcome_association_mixin_object, domain=None, range=Union[dict, Outcome])

slots.entity_to_phenotypic_feature_association_mixin_description = Slot(uri=DCT.description, name="entity to phenotypic feature association mixin_description", curie=DCT.curie('description'),
                   model_uri=BIOLINK.entity_to_phenotypic_feature_association_mixin_description, domain=None, range=Optional[Union[str, NarrativeText]])

slots.entity_to_phenotypic_feature_association_mixin_object = Slot(uri=RDF.object, name="entity to phenotypic feature association mixin_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.entity_to_phenotypic_feature_association_mixin_object, domain=None, range=Union[str, PhenotypicFeatureId])

slots.entity_to_disease_association_mixin_object = Slot(uri=RDF.object, name="entity to disease association mixin_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.entity_to_disease_association_mixin_object, domain=None, range=Union[str, DiseaseId])

slots.disease_or_phenotypic_feature_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="disease or phenotypic feature to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.disease_or_phenotypic_feature_to_entity_association_mixin_subject, domain=None, range=Union[str, DiseaseOrPhenotypicFeatureId])

slots.disease_or_phenotypic_feature_association_to_location_association_object = Slot(uri=RDF.object, name="disease or phenotypic feature association to location association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.disease_or_phenotypic_feature_association_to_location_association_object, domain=DiseaseOrPhenotypicFeatureAssociationToLocationAssociation, range=Union[str, AnatomicalEntityId])

slots.disease_or_phenotypic_feature_to_location_association_object = Slot(uri=RDF.object, name="disease or phenotypic feature to location association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.disease_or_phenotypic_feature_to_location_association_object, domain=DiseaseOrPhenotypicFeatureToLocationAssociation, range=Union[str, AnatomicalEntityId])

slots.entity_to_disease_or_phenotypic_feature_association_mixin_object = Slot(uri=RDF.object, name="entity to disease or phenotypic feature association mixin_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.entity_to_disease_or_phenotypic_feature_association_mixin_object, domain=None, range=Union[str, DiseaseOrPhenotypicFeatureId])

slots.genotype_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="genotype to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_to_entity_association_mixin_subject, domain=None, range=Union[str, GenotypeId])

slots.genotype_to_phenotypic_feature_association_predicate = Slot(uri=RDF.predicate, name="genotype to phenotypic feature association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.genotype_to_phenotypic_feature_association_predicate, domain=GenotypeToPhenotypicFeatureAssociation, range=Union[str, PredicateType])

slots.genotype_to_phenotypic_feature_association_subject = Slot(uri=RDF.subject, name="genotype to phenotypic feature association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_to_phenotypic_feature_association_subject, domain=GenotypeToPhenotypicFeatureAssociation, range=Union[str, GenotypeId])

slots.exposure_event_to_phenotypic_feature_association_subject = Slot(uri=RDF.subject, name="exposure event to phenotypic feature association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.exposure_event_to_phenotypic_feature_association_subject, domain=ExposureEventToPhenotypicFeatureAssociation, range=Union[dict, ExposureEvent])

slots.behavior_to_behavioral_feature_association_subject = Slot(uri=RDF.subject, name="behavior to behavioral feature association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.behavior_to_behavioral_feature_association_subject, domain=BehaviorToBehavioralFeatureAssociation, range=Union[str, BehaviorId])

slots.behavior_to_behavioral_feature_association_object = Slot(uri=RDF.object, name="behavior to behavioral feature association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.behavior_to_behavioral_feature_association_object, domain=BehaviorToBehavioralFeatureAssociation, range=Union[str, BehavioralFeatureId])

slots.gene_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="gene to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_entity_association_mixin_subject, domain=None, range=Union[dict, GeneOrGeneProduct])

slots.variant_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="variant to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.variant_to_entity_association_mixin_subject, domain=None, range=Union[str, SequenceVariantId])

slots.gene_to_phenotypic_feature_association_subject = Slot(uri=RDF.subject, name="gene to phenotypic feature association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_phenotypic_feature_association_subject, domain=GeneToPhenotypicFeatureAssociation, range=Union[dict, GeneOrGeneProduct])

slots.gene_to_disease_association_subject = Slot(uri=RDF.subject, name="gene to disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_disease_association_subject, domain=GeneToDiseaseAssociation, range=Union[dict, GeneOrGeneProduct])

slots.variant_to_gene_association_object = Slot(uri=RDF.object, name="variant to gene association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.variant_to_gene_association_object, domain=VariantToGeneAssociation, range=Union[str, GeneId])

slots.variant_to_gene_association_predicate = Slot(uri=RDF.predicate, name="variant to gene association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.variant_to_gene_association_predicate, domain=VariantToGeneAssociation, range=Union[str, PredicateType])

slots.variant_to_gene_expression_association_predicate = Slot(uri=RDF.predicate, name="variant to gene expression association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.variant_to_gene_expression_association_predicate, domain=VariantToGeneExpressionAssociation, range=Union[str, PredicateType])

slots.variant_to_population_association_subject = Slot(uri=RDF.subject, name="variant to population association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.variant_to_population_association_subject, domain=VariantToPopulationAssociation, range=Union[str, SequenceVariantId])

slots.variant_to_population_association_object = Slot(uri=RDF.object, name="variant to population association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.variant_to_population_association_object, domain=VariantToPopulationAssociation, range=Union[str, PopulationOfIndividualOrganismsId])

slots.variant_to_population_association_has_quotient = Slot(uri=BIOLINK.has_quotient, name="variant to population association_has quotient", curie=BIOLINK.curie('has_quotient'),
                   model_uri=BIOLINK.variant_to_population_association_has_quotient, domain=VariantToPopulationAssociation, range=Optional[float])

slots.variant_to_population_association_has_count = Slot(uri=BIOLINK.has_count, name="variant to population association_has count", curie=BIOLINK.curie('has_count'),
                   model_uri=BIOLINK.variant_to_population_association_has_count, domain=VariantToPopulationAssociation, range=Optional[int])

slots.variant_to_population_association_has_total = Slot(uri=BIOLINK.has_total, name="variant to population association_has total", curie=BIOLINK.curie('has_total'),
                   model_uri=BIOLINK.variant_to_population_association_has_total, domain=VariantToPopulationAssociation, range=Optional[int])

slots.population_to_population_association_subject = Slot(uri=RDF.subject, name="population to population association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.population_to_population_association_subject, domain=PopulationToPopulationAssociation, range=Union[str, PopulationOfIndividualOrganismsId])

slots.population_to_population_association_object = Slot(uri=RDF.object, name="population to population association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.population_to_population_association_object, domain=PopulationToPopulationAssociation, range=Union[str, PopulationOfIndividualOrganismsId])

slots.population_to_population_association_predicate = Slot(uri=RDF.predicate, name="population to population association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.population_to_population_association_predicate, domain=PopulationToPopulationAssociation, range=Union[str, PredicateType])

slots.variant_to_phenotypic_feature_association_subject = Slot(uri=RDF.subject, name="variant to phenotypic feature association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.variant_to_phenotypic_feature_association_subject, domain=VariantToPhenotypicFeatureAssociation, range=Union[str, SequenceVariantId])

slots.variant_to_disease_association_subject = Slot(uri=RDF.subject, name="variant to disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.variant_to_disease_association_subject, domain=VariantToDiseaseAssociation, range=Union[str, NamedThingId])

slots.variant_to_disease_association_predicate = Slot(uri=RDF.predicate, name="variant to disease association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.variant_to_disease_association_predicate, domain=VariantToDiseaseAssociation, range=Union[str, PredicateType])

slots.variant_to_disease_association_object = Slot(uri=RDF.object, name="variant to disease association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.variant_to_disease_association_object, domain=VariantToDiseaseAssociation, range=Union[str, NamedThingId])

slots.genotype_to_disease_association_subject = Slot(uri=RDF.subject, name="genotype to disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_to_disease_association_subject, domain=GenotypeToDiseaseAssociation, range=Union[str, NamedThingId])

slots.genotype_to_disease_association_predicate = Slot(uri=RDF.predicate, name="genotype to disease association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.genotype_to_disease_association_predicate, domain=GenotypeToDiseaseAssociation, range=Union[str, PredicateType])

slots.genotype_to_disease_association_object = Slot(uri=RDF.object, name="genotype to disease association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.genotype_to_disease_association_object, domain=GenotypeToDiseaseAssociation, range=Union[str, NamedThingId])

slots.model_to_disease_association_mixin_subject = Slot(uri=RDF.subject, name="model to disease association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.model_to_disease_association_mixin_subject, domain=None, range=Union[str, NamedThingId])

slots.model_to_disease_association_mixin_predicate = Slot(uri=RDF.predicate, name="model to disease association mixin_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.model_to_disease_association_mixin_predicate, domain=None, range=Union[str, PredicateType])

slots.gene_as_a_model_of_disease_association_subject = Slot(uri=RDF.subject, name="gene as a model of disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_as_a_model_of_disease_association_subject, domain=GeneAsAModelOfDiseaseAssociation, range=Union[dict, GeneOrGeneProduct])

slots.variant_as_a_model_of_disease_association_subject = Slot(uri=RDF.subject, name="variant as a model of disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.variant_as_a_model_of_disease_association_subject, domain=VariantAsAModelOfDiseaseAssociation, range=Union[str, SequenceVariantId])

slots.genotype_as_a_model_of_disease_association_subject = Slot(uri=RDF.subject, name="genotype as a model of disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genotype_as_a_model_of_disease_association_subject, domain=GenotypeAsAModelOfDiseaseAssociation, range=Union[str, GenotypeId])

slots.cell_line_as_a_model_of_disease_association_subject = Slot(uri=RDF.subject, name="cell line as a model of disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.cell_line_as_a_model_of_disease_association_subject, domain=CellLineAsAModelOfDiseaseAssociation, range=Union[str, CellLineId])

slots.organismal_entity_as_a_model_of_disease_association_subject = Slot(uri=RDF.subject, name="organismal entity as a model of disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.organismal_entity_as_a_model_of_disease_association_subject, domain=OrganismalEntityAsAModelOfDiseaseAssociation, range=Union[str, OrganismalEntityId])

slots.gene_has_variant_that_contributes_to_disease_association_subject = Slot(uri=RDF.subject, name="gene has variant that contributes to disease association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_has_variant_that_contributes_to_disease_association_subject, domain=GeneHasVariantThatContributesToDiseaseAssociation, range=Union[dict, GeneOrGeneProduct])

slots.gene_to_expression_site_association_subject = Slot(uri=RDF.subject, name="gene to expression site association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_expression_site_association_subject, domain=GeneToExpressionSiteAssociation, range=Union[dict, GeneOrGeneProduct])

slots.gene_to_expression_site_association_object = Slot(uri=RDF.object, name="gene to expression site association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.gene_to_expression_site_association_object, domain=GeneToExpressionSiteAssociation, range=Union[str, AnatomicalEntityId])

slots.gene_to_expression_site_association_predicate = Slot(uri=RDF.predicate, name="gene to expression site association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.gene_to_expression_site_association_predicate, domain=GeneToExpressionSiteAssociation, range=Union[str, PredicateType])

slots.gene_to_expression_site_association_stage_qualifier = Slot(uri=BIOLINK.stage_qualifier, name="gene to expression site association_stage qualifier", curie=BIOLINK.curie('stage_qualifier'),
                   model_uri=BIOLINK.gene_to_expression_site_association_stage_qualifier, domain=GeneToExpressionSiteAssociation, range=Optional[Union[str, LifeStageId]])

slots.gene_to_expression_site_association_quantifier_qualifier = Slot(uri=BIOLINK.quantifier_qualifier, name="gene to expression site association_quantifier qualifier", curie=BIOLINK.curie('quantifier_qualifier'),
                   model_uri=BIOLINK.gene_to_expression_site_association_quantifier_qualifier, domain=GeneToExpressionSiteAssociation, range=Optional[Union[dict, OntologyClass]])

slots.sequence_variant_modulates_treatment_association_subject = Slot(uri=RDF.subject, name="sequence variant modulates treatment association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.sequence_variant_modulates_treatment_association_subject, domain=SequenceVariantModulatesTreatmentAssociation, range=Union[str, SequenceVariantId])

slots.sequence_variant_modulates_treatment_association_object = Slot(uri=RDF.object, name="sequence variant modulates treatment association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.sequence_variant_modulates_treatment_association_object, domain=SequenceVariantModulatesTreatmentAssociation, range=Union[str, TreatmentId])

slots.functional_association_subject = Slot(uri=RDF.subject, name="functional association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.functional_association_subject, domain=FunctionalAssociation, range=Union[dict, MacromolecularMachineMixin])

slots.functional_association_object = Slot(uri=RDF.object, name="functional association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.functional_association_object, domain=FunctionalAssociation, range=Union[dict, GeneOntologyClass])

slots.macromolecular_machine_to_entity_association_mixin_subject = Slot(uri=RDF.subject, name="macromolecular machine to entity association mixin_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.macromolecular_machine_to_entity_association_mixin_subject, domain=None, range=Union[str, NamedThingId])

slots.macromolecular_machine_to_molecular_activity_association_object = Slot(uri=RDF.object, name="macromolecular machine to molecular activity association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.macromolecular_machine_to_molecular_activity_association_object, domain=MacromolecularMachineToMolecularActivityAssociation, range=Union[str, MolecularActivityId])

slots.macromolecular_machine_to_biological_process_association_object = Slot(uri=RDF.object, name="macromolecular machine to biological process association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.macromolecular_machine_to_biological_process_association_object, domain=MacromolecularMachineToBiologicalProcessAssociation, range=Union[str, BiologicalProcessId])

slots.macromolecular_machine_to_cellular_component_association_object = Slot(uri=RDF.object, name="macromolecular machine to cellular component association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.macromolecular_machine_to_cellular_component_association_object, domain=MacromolecularMachineToCellularComponentAssociation, range=Union[str, CellularComponentId])

slots.gene_to_go_term_association_subject = Slot(uri=RDF.subject, name="gene to go term association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_go_term_association_subject, domain=GeneToGoTermAssociation, range=Union[str, MolecularEntityId])

slots.gene_to_go_term_association_object = Slot(uri=RDF.object, name="gene to go term association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.gene_to_go_term_association_object, domain=GeneToGoTermAssociation, range=Union[dict, GeneOntologyClass])

slots.genomic_sequence_localization_subject = Slot(uri=RDF.subject, name="genomic sequence localization_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.genomic_sequence_localization_subject, domain=GenomicSequenceLocalization, range=Union[str, GenomicEntityId])

slots.genomic_sequence_localization_object = Slot(uri=RDF.object, name="genomic sequence localization_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.genomic_sequence_localization_object, domain=GenomicSequenceLocalization, range=Union[str, GenomicEntityId])

slots.genomic_sequence_localization_predicate = Slot(uri=RDF.predicate, name="genomic sequence localization_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.genomic_sequence_localization_predicate, domain=GenomicSequenceLocalization, range=Union[str, PredicateType])

slots.sequence_feature_relationship_subject = Slot(uri=RDF.subject, name="sequence feature relationship_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.sequence_feature_relationship_subject, domain=SequenceFeatureRelationship, range=Union[str, GenomicEntityId])

slots.sequence_feature_relationship_object = Slot(uri=RDF.object, name="sequence feature relationship_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.sequence_feature_relationship_object, domain=SequenceFeatureRelationship, range=Union[str, GenomicEntityId])

slots.transcript_to_gene_relationship_subject = Slot(uri=RDF.subject, name="transcript to gene relationship_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.transcript_to_gene_relationship_subject, domain=TranscriptToGeneRelationship, range=Union[str, TranscriptId])

slots.transcript_to_gene_relationship_object = Slot(uri=RDF.object, name="transcript to gene relationship_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.transcript_to_gene_relationship_object, domain=TranscriptToGeneRelationship, range=Union[str, GeneId])

slots.gene_to_gene_product_relationship_subject = Slot(uri=RDF.subject, name="gene to gene product relationship_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_to_gene_product_relationship_subject, domain=GeneToGeneProductRelationship, range=Union[str, GeneId])

slots.gene_to_gene_product_relationship_object = Slot(uri=RDF.object, name="gene to gene product relationship_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.gene_to_gene_product_relationship_object, domain=GeneToGeneProductRelationship, range=Union[dict, GeneProductMixin])

slots.gene_to_gene_product_relationship_predicate = Slot(uri=RDF.predicate, name="gene to gene product relationship_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.gene_to_gene_product_relationship_predicate, domain=GeneToGeneProductRelationship, range=Union[str, PredicateType])

slots.exon_to_transcript_relationship_subject = Slot(uri=RDF.subject, name="exon to transcript relationship_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.exon_to_transcript_relationship_subject, domain=ExonToTranscriptRelationship, range=Union[str, ExonId])

slots.exon_to_transcript_relationship_object = Slot(uri=RDF.object, name="exon to transcript relationship_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.exon_to_transcript_relationship_object, domain=ExonToTranscriptRelationship, range=Union[str, TranscriptId])

slots.gene_regulatory_relationship_predicate = Slot(uri=RDF.predicate, name="gene regulatory relationship_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.gene_regulatory_relationship_predicate, domain=GeneRegulatoryRelationship, range=Union[str, PredicateType])

slots.gene_regulatory_relationship_subject = Slot(uri=RDF.subject, name="gene regulatory relationship_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.gene_regulatory_relationship_subject, domain=GeneRegulatoryRelationship, range=Union[dict, GeneOrGeneProduct])

slots.gene_regulatory_relationship_object = Slot(uri=RDF.object, name="gene regulatory relationship_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.gene_regulatory_relationship_object, domain=GeneRegulatoryRelationship, range=Union[dict, GeneOrGeneProduct])

slots.anatomical_entity_to_anatomical_entity_association_subject = Slot(uri=RDF.subject, name="anatomical entity to anatomical entity association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_association_subject, domain=AnatomicalEntityToAnatomicalEntityAssociation, range=Union[str, AnatomicalEntityId])

slots.anatomical_entity_to_anatomical_entity_association_object = Slot(uri=RDF.object, name="anatomical entity to anatomical entity association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_association_object, domain=AnatomicalEntityToAnatomicalEntityAssociation, range=Union[str, AnatomicalEntityId])

slots.anatomical_entity_to_anatomical_entity_part_of_association_subject = Slot(uri=RDF.subject, name="anatomical entity to anatomical entity part of association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_part_of_association_subject, domain=AnatomicalEntityToAnatomicalEntityPartOfAssociation, range=Union[str, AnatomicalEntityId])

slots.anatomical_entity_to_anatomical_entity_part_of_association_object = Slot(uri=RDF.object, name="anatomical entity to anatomical entity part of association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_part_of_association_object, domain=AnatomicalEntityToAnatomicalEntityPartOfAssociation, range=Union[str, AnatomicalEntityId])

slots.anatomical_entity_to_anatomical_entity_part_of_association_predicate = Slot(uri=RDF.predicate, name="anatomical entity to anatomical entity part of association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_part_of_association_predicate, domain=AnatomicalEntityToAnatomicalEntityPartOfAssociation, range=Union[str, PredicateType])

slots.anatomical_entity_to_anatomical_entity_ontogenic_association_subject = Slot(uri=RDF.subject, name="anatomical entity to anatomical entity ontogenic association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_ontogenic_association_subject, domain=AnatomicalEntityToAnatomicalEntityOntogenicAssociation, range=Union[str, AnatomicalEntityId])

slots.anatomical_entity_to_anatomical_entity_ontogenic_association_object = Slot(uri=RDF.object, name="anatomical entity to anatomical entity ontogenic association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_ontogenic_association_object, domain=AnatomicalEntityToAnatomicalEntityOntogenicAssociation, range=Union[str, AnatomicalEntityId])

slots.anatomical_entity_to_anatomical_entity_ontogenic_association_predicate = Slot(uri=RDF.predicate, name="anatomical entity to anatomical entity ontogenic association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.anatomical_entity_to_anatomical_entity_ontogenic_association_predicate, domain=AnatomicalEntityToAnatomicalEntityOntogenicAssociation, range=Union[str, PredicateType])

slots.organism_taxon_to_entity_association_subject = Slot(uri=RDF.subject, name="organism taxon to entity association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.organism_taxon_to_entity_association_subject, domain=None, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_association_subject = Slot(uri=RDF.subject, name="organism taxon to organism taxon association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_association_subject, domain=OrganismTaxonToOrganismTaxonAssociation, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_association_object = Slot(uri=RDF.object, name="organism taxon to organism taxon association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_association_object, domain=OrganismTaxonToOrganismTaxonAssociation, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_specialization_subject = Slot(uri=RDF.subject, name="organism taxon to organism taxon specialization_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_specialization_subject, domain=OrganismTaxonToOrganismTaxonSpecialization, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_specialization_object = Slot(uri=RDF.object, name="organism taxon to organism taxon specialization_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_specialization_object, domain=OrganismTaxonToOrganismTaxonSpecialization, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_specialization_predicate = Slot(uri=RDF.predicate, name="organism taxon to organism taxon specialization_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_specialization_predicate, domain=OrganismTaxonToOrganismTaxonSpecialization, range=Union[str, PredicateType])

slots.organism_taxon_to_organism_taxon_interaction_subject = Slot(uri=RDF.subject, name="organism taxon to organism taxon interaction_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_interaction_subject, domain=OrganismTaxonToOrganismTaxonInteraction, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_interaction_object = Slot(uri=RDF.object, name="organism taxon to organism taxon interaction_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_interaction_object, domain=OrganismTaxonToOrganismTaxonInteraction, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_organism_taxon_interaction_predicate = Slot(uri=RDF.predicate, name="organism taxon to organism taxon interaction_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_interaction_predicate, domain=OrganismTaxonToOrganismTaxonInteraction, range=Union[str, PredicateType])

slots.organism_taxon_to_organism_taxon_interaction_associated_environmental_context = Slot(uri=BIOLINK.associated_environmental_context, name="organism taxon to organism taxon interaction_associated environmental context", curie=BIOLINK.curie('associated_environmental_context'),
                   model_uri=BIOLINK.organism_taxon_to_organism_taxon_interaction_associated_environmental_context, domain=OrganismTaxonToOrganismTaxonInteraction, range=Optional[str])

slots.organism_taxon_to_environment_association_subject = Slot(uri=RDF.subject, name="organism taxon to environment association_subject", curie=RDF.curie('subject'),
                   model_uri=BIOLINK.organism_taxon_to_environment_association_subject, domain=OrganismTaxonToEnvironmentAssociation, range=Union[str, OrganismTaxonId])

slots.organism_taxon_to_environment_association_object = Slot(uri=RDF.object, name="organism taxon to environment association_object", curie=RDF.curie('object'),
                   model_uri=BIOLINK.organism_taxon_to_environment_association_object, domain=OrganismTaxonToEnvironmentAssociation, range=Union[str, NamedThingId])

slots.organism_taxon_to_environment_association_predicate = Slot(uri=RDF.predicate, name="organism taxon to environment association_predicate", curie=RDF.curie('predicate'),
                   model_uri=BIOLINK.organism_taxon_to_environment_association_predicate, domain=OrganismTaxonToEnvironmentAssociation, range=Union[str, PredicateType])