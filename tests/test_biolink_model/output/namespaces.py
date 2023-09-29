# Auto generated from biolink-model.yaml by namespacegen.py version: 0.0.1
# Generation date: 2023-09-22T11:47:50
# Schema: Biolink-Model
#
# id: https://w3id.org/biolink/biolink-model
# description: Entity and association taxonomy and datamodel for life-sciences data
# license: https://creativecommons.org/publicdomain/zero/1.0/

from collections import defaultdict
from typing import Iterable, Dict, Tuple

from linkml_runtime.utils.curienamespace import CurieNamespace

GENE = 'gene'
DISEASE = 'disease'
CHEMICAL_SUBSTANCE = 'chemical substance'

SYMBOL = 'Approved_Symbol'


class IdentifierResolverException(RuntimeError):
    pass


class BiolinkNameSpace:
    """
    Map of BioLink Model registered URI Namespaces
    """

    _namespaces = [
        CurieNamespace('AGRKB', 'https://www.alliancegenome.org/'),
        CurieNamespace('APO', 'http://purl.obolibrary.org/obo/APO_'),
        CurieNamespace('AspGD', 'http://www.aspergillusgenome.org/cgi-bin/locus.pl?dbid='),
        CurieNamespace('BFO', 'http://purl.obolibrary.org/obo/BFO_'),
        CurieNamespace('BIGG_METABOLITE', 'http://identifiers.org/bigg.metabolite/'),
        CurieNamespace('BIGG_REACTION', 'http://identifiers.org/bigg.reaction/'),
        CurieNamespace('BIOGRID', 'http://identifiers.org/biogrid/'),
        CurieNamespace('BIOSAMPLE', 'http://identifiers.org/biosample/'),
        CurieNamespace('BSPO', 'http://purl.obolibrary.org/obo/BSPO_'),
        CurieNamespace('BTO', 'http://purl.obolibrary.org/obo/BTO_'),
        CurieNamespace('CAID', 'http://reg.clinicalgenome.org/redmine/projects/registry/genboree_registry/by_caid?caid='),
        CurieNamespace('CARO', 'http://purl.obolibrary.org/obo/CARO_'),
        CurieNamespace('CAS', 'http://identifiers.org/cas/'),
        CurieNamespace('CATH', 'http://identifiers.org/cath/'),
        CurieNamespace('CATH_SUPERFAMILY', 'http://identifiers.org/cath.superfamily/'),
        CurieNamespace('CDD', 'http://identifiers.org/cdd/'),
        CurieNamespace('CHADO', 'http://gmod.org/wiki/Chado/'),
        CurieNamespace('CHEBI', 'http://purl.obolibrary.org/obo/CHEBI_'),
        CurieNamespace('CHEMBL_COMPOUND', 'http://identifiers.org/chembl.compound/'),
        CurieNamespace('CHEMBL_MECHANISM', 'https://www.ebi.ac.uk/chembl/mechanism/inspect/'),
        CurieNamespace('CHEMBL_TARGET', 'http://identifiers.org/chembl.target/'),
        CurieNamespace('CID', 'http://pubchem.ncbi.nlm.nih.gov/compound/'),
        CurieNamespace('CIO', 'http://purl.obolibrary.org/obo/CIO_'),
        CurieNamespace('CL', 'http://purl.obolibrary.org/obo/CL_'),
        CurieNamespace('CLINVAR', 'http://identifiers.org/clinvar'),
        CurieNamespace('CLO', 'http://purl.obolibrary.org/obo/CLO_'),
        CurieNamespace('COAR_RESOURCE', 'http://purl.org/coar/resource_type/'),
        CurieNamespace('COG', 'https://www.ncbi.nlm.nih.gov/research/cog-project/'),
        CurieNamespace('CPT', 'https://www.ama-assn.org/practice-management/cpt/'),
        CurieNamespace('CTD', 'http://ctdbase.org/'),
        CurieNamespace('CTD_CHEMICAL', 'http://ctdbase.org/detail.go?type=chem&acc='),
        CurieNamespace('CTD_DISEASE', 'http://ctdbase.org/detail.go?type=disease&db=MESH&acc='),
        CurieNamespace('CTD_GENE', 'http://ctdbase.org/detail.go?type=gene&acc='),
        CurieNamespace('ChemBank', 'http://chembank.broadinstitute.org/chemistry/viewMolecule.htm?cbid='),
        CurieNamespace('ComplexPortal', 'https://www.ebi.ac.uk/complexportal/complex/'),
        CurieNamespace('DBSNP', 'http://identifiers.org/dbsnp/'),
        CurieNamespace('DDANAT', 'http://purl.obolibrary.org/obo/DDANAT_'),
        CurieNamespace('DGIdb', 'https://www.dgidb.org/interaction_types'),
        CurieNamespace('DOID', 'http://purl.obolibrary.org/obo/DOID_'),
        CurieNamespace('DOID-PROPERTY', 'http://purl.obolibrary.org/obo/doid#'),
        CurieNamespace('DRUGBANK', 'http://identifiers.org/drugbank/'),
        CurieNamespace('DrugCentral', 'http://drugcentral.org/drugcard/'),
        CurieNamespace('EC', 'http://www.enzyme-database.org/query.php?ec='),
        CurieNamespace('ECO', 'http://purl.obolibrary.org/obo/ECO_'),
        CurieNamespace('ECTO', 'http://purl.obolibrary.org/obo/ECTO_'),
        CurieNamespace('EDAM-DATA', 'http://edamontology.org/data_'),
        CurieNamespace('EDAM-FORMAT', 'http://edamontology.org/format_'),
        CurieNamespace('EDAM-OPERATION', 'http://edamontology.org/operation_'),
        CurieNamespace('EDAM-TOPIC', 'http://edamontology.org/topic_'),
        CurieNamespace('EFO', 'http://www.ebi.ac.uk/efo/EFO_'),
        CurieNamespace('EGGNOG', 'http://identifiers.org/eggnog/'),
        CurieNamespace('EMAPA', 'http://purl.obolibrary.org/obo/EMAPA_'),
        CurieNamespace('ENSEMBL', 'http://identifiers.org/ensembl/'),
        CurieNamespace('ENVO', 'http://purl.obolibrary.org/obo/ENVO_'),
        CurieNamespace('ExO', 'http://purl.obolibrary.org/obo/ExO_'),
        CurieNamespace('FAO', 'http://purl.obolibrary.org/obo/FAO_'),
        CurieNamespace('FB', 'http://identifiers.org/fb/'),
        CurieNamespace('FBbt', 'http://purl.obolibrary.org/obo/FBbt_'),
        CurieNamespace('FBcv', 'http://purl.obolibrary.org/obo/FBcv_'),
        CurieNamespace('FBdv', 'http://purl.obolibrary.org/obo/FBdv_'),
        CurieNamespace('FMA', 'http://purl.obolibrary.org/obo/FMA_'),
        CurieNamespace('FOODON', 'http://purl.obolibrary.org/obo/FOODON_'),
        CurieNamespace('FYECO', 'https://www.pombase.org/term/'),
        CurieNamespace('FYPO', 'http://purl.obolibrary.org/obo/FYPO_'),
        CurieNamespace('GENEPIO', 'http://purl.obolibrary.org/obo/GENEPIO_'),
        CurieNamespace('GENO', 'http://purl.obolibrary.org/obo/GENO_'),
        CurieNamespace('GO', 'http://purl.obolibrary.org/obo/GO_'),
        CurieNamespace('GOLD_META', 'http://identifiers.org/gold.meta/'),
        CurieNamespace('GOP', 'http://purl.obolibrary.org/obo/go#'),
        CurieNamespace('GOREL', 'http://purl.obolibrary.org/obo/GOREL_'),
        CurieNamespace('GSID', 'https://scholar.google.com/citations?user='),
        CurieNamespace('GTEx', 'https://www.gtexportal.org/home/gene/'),
        CurieNamespace('GTOPDB', 'https://www.guidetopharmacology.org/GRAC/LigandDisplayForward?ligandId='),
        CurieNamespace('HAMAP', 'http://identifiers.org/hamap/'),
        CurieNamespace('HANCESTRO', 'http://www.ebi.ac.uk/ancestro/ancestro_'),
        CurieNamespace('HCPCS', 'http://purl.bioontology.org/ontology/HCPCS/'),
        CurieNamespace('HGNC', 'http://identifiers.org/hgnc/'),
        CurieNamespace('HGNC_FAMILY', 'http://identifiers.org/hgnc.family/'),
        CurieNamespace('HMDB', 'http://identifiers.org/hmdb/'),
        CurieNamespace('HP', 'http://purl.obolibrary.org/obo/HP_'),
        CurieNamespace('HsapDv', 'http://purl.obolibrary.org/obo/HsapDv_'),
        CurieNamespace('IAO', 'http://purl.obolibrary.org/obo/IAO_'),
        CurieNamespace('ICD10', 'https://icd.codes/icd9cm/'),
        CurieNamespace('ICD9', 'http://translator.ncats.nih.gov/ICD9_'),
        CurieNamespace('IDO', 'http://purl.obolibrary.org/obo/IDO_'),
        CurieNamespace('INCHI', 'http://identifiers.org/inchi/'),
        CurieNamespace('INCHIKEY', 'http://identifiers.org/inchikey/'),
        CurieNamespace('INO', 'http://purl.obolibrary.org/obo/INO_'),
        CurieNamespace('INTACT', 'http://identifiers.org/intact/'),
        CurieNamespace('IUPHAR_FAMILY', 'http://identifiers.org/iuphar.family/'),
        CurieNamespace('KEGG', 'http://identifiers.org/kegg/'),
        CurieNamespace('KEGG_BRITE', 'http://www.kegg.jp/entry/'),
        CurieNamespace('KEGG_COMPOUND', 'http://identifiers.org/kegg.compound/'),
        CurieNamespace('KEGG_DGROUP', 'http://www.kegg.jp/entry/'),
        CurieNamespace('KEGG_DISEASE', 'http://identifiers.org/kegg.disease/'),
        CurieNamespace('KEGG_DRUG', 'http://identifiers.org/kegg.drug/'),
        CurieNamespace('KEGG_ENVIRON', 'http://identifiers.org/kegg.environ/'),
        CurieNamespace('KEGG_ENZYME', 'http://www.kegg.jp/entry/'),
        CurieNamespace('KEGG_GENE', 'http://www.kegg.jp/entry/'),
        CurieNamespace('KEGG_GLYCAN', 'http://identifiers.org/kegg.glycan/'),
        CurieNamespace('KEGG_MODULE', 'http://identifiers.org/kegg.module/'),
        CurieNamespace('KEGG_ORTHOLOGY', 'http://identifiers.org/kegg.orthology/'),
        CurieNamespace('KEGG_PATHWAY', 'https://www.kegg.jp/entry/'),
        CurieNamespace('KEGG_RCLASS', 'http://www.kegg.jp/entry/'),
        CurieNamespace('KEGG_REACTION', 'http://identifiers.org/kegg.reaction/'),
        CurieNamespace('LOINC', 'http://loinc.org/rdf/'),
        CurieNamespace('MA', 'http://purl.obolibrary.org/obo/MA_'),
        CurieNamespace('MAXO', 'http://purl.obolibrary.org/obo/MAXO_'),
        CurieNamespace('MEDDRA', 'http://identifiers.org/meddra/'),
        CurieNamespace('MESH', 'http://id.nlm.nih.gov/mesh/'),
        CurieNamespace('METANETX_REACTION', 'https://www.metanetx.org/equa_info/'),
        CurieNamespace('MGI', 'http://identifiers.org/mgi/'),
        CurieNamespace('MI', 'http://purl.obolibrary.org/obo/MI_'),
        CurieNamespace('MIR', 'http://identifiers.org/mir/'),
        CurieNamespace('MONDO', 'http://purl.obolibrary.org/obo/MONDO_'),
        CurieNamespace('MP', 'http://purl.obolibrary.org/obo/MP_'),
        CurieNamespace('MPATH', 'http://purl.obolibrary.org/obo/MPATH_'),
        CurieNamespace('MSigDB', 'https://www.gsea-msigdb.org/gsea/msigdb/'),
        CurieNamespace('MmusDv', 'http://purl.obolibrary.org/obo/MMUSDV_'),
        CurieNamespace('NBO', 'http://purl.obolibrary.org/obo/NBO_'),
        CurieNamespace('NBO-PROPERTY', 'http://purl.obolibrary.org/obo/nbo#'),
        CurieNamespace('NCBIGene', 'http://identifiers.org/ncbigene/'),
        CurieNamespace('NCBITaxon', 'http://purl.obolibrary.org/obo/NCBITaxon_'),
        CurieNamespace('NCIT', 'http://purl.obolibrary.org/obo/NCIT_'),
        CurieNamespace('NCIT-OBO', 'http://purl.obolibrary.org/obo/ncit#'),
        CurieNamespace('NDC', 'http://identifiers.org/ndc/'),
        CurieNamespace('NDDF', 'http://purl.bioontology.org/ontology/NDDF/'),
        CurieNamespace('NLMID', 'https://www.ncbi.nlm.nih.gov/nlmcatalog/?term='),
        CurieNamespace('OBAN', 'http://purl.org/oban/'),
        CurieNamespace('OBI', 'http://purl.obolibrary.org/obo/OBI_'),
        CurieNamespace('OGMS', 'http://purl.obolibrary.org/obo/OGMS_'),
        CurieNamespace('OIO', 'http://www.geneontology.org/formats/oboInOwl#'),
        CurieNamespace('OMIM', 'http://purl.obolibrary.org/obo/OMIM_'),
        CurieNamespace('OMIM_PS', 'https://www.omim.org/phenotypicSeries/'),
        CurieNamespace('ORCID', 'https://orcid.org/'),
        CurieNamespace('PANTHER_FAMILY', 'http://www.pantherdb.org/panther/family.do?clsAccession='),
        CurieNamespace('PANTHER_PATHWAY', 'http://identifiers.org/panther.pathway/'),
        CurieNamespace('PATO', 'http://purl.obolibrary.org/obo/PATO_'),
        CurieNamespace('PCO', 'http://purl.obolibrary.org/obo/PCO_'),
        CurieNamespace('PFAM', 'http://identifiers.org/pfam/'),
        CurieNamespace('PHARMGKB_PATHWAYS', 'http://identifiers.org/pharmgkb.pathways/'),
        CurieNamespace('PHAROS', 'http://pharos.nih.gov'),
        CurieNamespace('PIRSF', 'http://identifiers.org/pirsf/'),
        CurieNamespace('PMID', 'http://www.ncbi.nlm.nih.gov/pubmed/'),
        CurieNamespace('PO', 'http://purl.obolibrary.org/obo/PO_'),
        CurieNamespace('PR', 'http://purl.obolibrary.org/obo/PR_'),
        CurieNamespace('PRINTS', 'http://identifiers.org/prints/'),
        CurieNamespace('PRODOM', 'http://identifiers.org/prodom/'),
        CurieNamespace('PROSITE', 'http://identifiers.org/prosite/'),
        CurieNamespace('PUBCHEM_COMPOUND', 'http://identifiers.org/pubchem.compound/'),
        CurieNamespace('PUBCHEM_SUBSTANCE', 'http://identifiers.org/pubchem.substance/'),
        CurieNamespace('PW', 'http://purl.obolibrary.org/obo/PW_'),
        CurieNamespace('PathWhiz', 'http://smpdb.ca/pathways/#'),
        CurieNamespace('PomBase', 'https://www.pombase.org/gene/'),
        CurieNamespace('REACT', 'http://www.reactome.org/PathwayBrowser/#/'),
        CurieNamespace('REPODB', 'http://apps.chiragjpgroup.org/repoDB/'),
        CurieNamespace('RFAM', 'http://identifiers.org/rfam/'),
        CurieNamespace('RGD', 'http://identifiers.org/rgd/'),
        CurieNamespace('RHEA', 'http://identifiers.org/rhea/'),
        CurieNamespace('RNACENTRAL', 'http://identifiers.org/rnacentral/'),
        CurieNamespace('RO', 'http://purl.obolibrary.org/obo/RO_'),
        CurieNamespace('RXCUI', 'https://mor.nlm.nih.gov/RxNav/search?searchBy=RXCUI&searchTerm='),
        CurieNamespace('RXNORM', 'http://purl.bioontology.org/ontology/RXNORM/'),
        CurieNamespace('ResearchID', 'https://publons.com/researcher/'),
        CurieNamespace('SEED_REACTION', 'https://modelseed.org/biochem/reactions/'),
        CurieNamespace('SEMMEDDB', 'https://skr3.nlm.nih.gov/SemMedDB'),
        CurieNamespace('SEPIO', 'http://purl.obolibrary.org/obo/SEPIO_'),
        CurieNamespace('SGD', 'http://identifiers.org/sgd/'),
        CurieNamespace('SIDER_DRUG', 'http://identifiers.org/sider.drug/'),
        CurieNamespace('SIO', 'http://semanticscience.org/resource/SIO_'),
        CurieNamespace('SMART', 'http://identifiers.org/smart/'),
        CurieNamespace('SMPDB', 'http://identifiers.org/smpdb/'),
        CurieNamespace('SNOMED', 'http://purl.obolibrary.org/obo/SNOMED_'),
        CurieNamespace('SNOMEDCT', 'http://snomed.info/id/'),
        CurieNamespace('SO', 'http://purl.obolibrary.org/obo/SO_'),
        CurieNamespace('SPDI', 'https://api.ncbi.nlm.nih.gov/variation/v0/spdi/'),
        CurieNamespace('STATO', 'http://purl.obolibrary.org/obo/STATO_'),
        CurieNamespace('STY', 'http://purl.bioontology.org/ontology/STY/'),
        CurieNamespace('SUPFAM', 'http://identifiers.org/supfam/'),
        CurieNamespace('ScopusID', 'https://www.scopus.com/authid/detail.uri?authorId='),
        CurieNamespace('TAXRANK', 'http://purl.obolibrary.org/obo/TAXRANK_'),
        CurieNamespace('TCDB', 'http://identifiers.org/tcdb/'),
        CurieNamespace('TIGRFAM', 'http://identifiers.org/tigrfam/'),
        CurieNamespace('TO', 'http://purl.obolibrary.org/obo/TO_'),
        CurieNamespace('UBERGRAPH', 'http://translator.renci.org/ubergraph-axioms.ofn#'),
        CurieNamespace('UBERON', 'http://purl.obolibrary.org/obo/UBERON_'),
        CurieNamespace('UBERON_CORE', 'http://purl.obolibrary.org/obo/uberon/core#'),
        CurieNamespace('UBERON_NONAMESPACE', 'http://purl.obolibrary.org/obo/core#'),
        CurieNamespace('UMLS', 'http://identifiers.org/umls/'),
        CurieNamespace('UMLSSG', 'https://lhncbc.nlm.nih.gov/semanticnetwork/download/sg_archive/SemGroups-v04.txt'),
        CurieNamespace('UNII', 'http://identifiers.org/unii/'),
        CurieNamespace('UNIPROT_ISOFORM', 'http://identifiers.org/uniprot.isoform/'),
        CurieNamespace('UO', 'http://purl.obolibrary.org/obo/UO_'),
        CurieNamespace('UO-PROPERTY', 'http://purl.obolibrary.org/obo/uo#'),
        CurieNamespace('UPHENO', 'http://purl.obolibrary.org/obo/UPHENO_'),
        CurieNamespace('UniProtKB', 'http://identifiers.org/uniprot/'),
        CurieNamespace('VANDF', 'https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/VANDF/'),
        CurieNamespace('VMC', 'https://github.com/ga4gh/vr-spec/'),
        CurieNamespace('WB', 'http://identifiers.org/wb/'),
        CurieNamespace('WBPhenotype', 'http://purl.obolibrary.org/obo/WBPhenotype_'),
        CurieNamespace('WBVocab', 'http://bio2rdf.org/wormbase_vocabulary'),
        CurieNamespace('WBbt', 'http://purl.obolibrary.org/obo/WBBT_'),
        CurieNamespace('WBls', 'http://purl.obolibrary.org/obo/WBBL_'),
        CurieNamespace('WIKIDATA', 'https://www.wikidata.org/wiki/'),
        CurieNamespace('WIKIDATA_PROPERTY', 'https://www.wikidata.org/wiki/Property:'),
        CurieNamespace('WIKIPATHWAYS', 'http://identifiers.org/wikipathways/'),
        CurieNamespace('WormBase', 'https://www.wormbase.org/get?name='),
        CurieNamespace('XAO', 'http://purl.obolibrary.org/obo/XAO_'),
        CurieNamespace('XCO', 'http://purl.obolibrary.org/obo/XCO_'),
        CurieNamespace('XPO', 'http://purl.obolibrary.org/obo/XPO_'),
        CurieNamespace('Xenbase', 'http://www.xenbase.org/gene/showgene.do?method=display&geneId='),
        CurieNamespace('ZFA', 'http://purl.obolibrary.org/obo/ZFA_'),
        CurieNamespace('ZFIN', 'http://identifiers.org/zfin/'),
        CurieNamespace('ZFS', 'http://purl.obolibrary.org/obo/ZFS_'),
        CurieNamespace('ZP', 'http://purl.obolibrary.org/obo/ZP_'),
        CurieNamespace('apollo', 'https://github.com/GMOD/Apollo'),
        CurieNamespace('biolink', 'https://w3id.org/biolink/vocab/'),
        CurieNamespace('bioschemas', 'https://bioschemas.org/'),
        CurieNamespace('dcat', 'http://www.w3.org/ns/dcat#'),
        CurieNamespace('dcid', 'https://datacommons.org/browser/'),
        CurieNamespace('dct', 'http://purl.org/dc/terms/'),
        CurieNamespace('dctypes', 'http://purl.org/dc/dcmitype/'),
        CurieNamespace('dictyBase', 'http://dictybase.org/gene/'),
        CurieNamespace('doi', 'https://doi.org/'),
        CurieNamespace('fabio', 'http://purl.org/spar/fabio/'),
        CurieNamespace('faldo', 'http://biohackathon.org/resource/faldo#'),
        CurieNamespace('foaf', 'http://xmlns.com/foaf/0.1/'),
        CurieNamespace('foodb_compound', 'http://foodb.ca/foods/'),
        CurieNamespace('foodb_food', 'http://foodb.ca/compounds/'),
        CurieNamespace('gff3', 'https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md#'),
        CurieNamespace('gpi', 'https://github.com/geneontology/go-annotation/blob/master/specs/gpad-gpi-2-0.md#'),
        CurieNamespace('gtpo', 'https://rdf.guidetopharmacology.org/ns/gtpo#'),
        CurieNamespace('interpro', 'https://www.ebi.ac.uk/interpro/entry/'),
        CurieNamespace('isbn', 'https://www.isbn-international.org/identifier/'),
        CurieNamespace('isni', 'https://isni.org/isni/'),
        CurieNamespace('issn', 'https://portal.issn.org/resource/ISSN/'),
        CurieNamespace('linkml', 'https://w3id.org/linkml/'),
        CurieNamespace('medgen', 'https://www.ncbi.nlm.nih.gov/medgen/'),
        CurieNamespace('metacyc_reaction', 'http://identifiers.org/metacyc.reaction:'),
        CurieNamespace('mirbase', 'http://identifiers.org/mirbase'),
        CurieNamespace('mmmp_biomaps', 'https://bioregistry.io/mmmp.biomaps:'),
        CurieNamespace('ncats_bioplanet', 'https://tripod.nih.gov/bioplanet/detail.jsp?pid='),
        CurieNamespace('ncats_drug', 'https://drugs.ncats.io/drug/'),
        CurieNamespace('oboInOwl', 'http://www.geneontology.org/formats/oboInOwl#'),
        CurieNamespace('oboformat', 'http://www.geneontology.org/formats/oboInOwl#'),
        CurieNamespace('orphanet', 'http://www.orpha.net/ORDO/Orphanet_'),
        CurieNamespace('os', 'https://github.com/cmungall/owlstar/blob/master/owlstar.ttl'),
        CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#'),
        CurieNamespace('pav', 'http://purl.org/pav/'),
        CurieNamespace('prov', 'http://www.w3.org/ns/prov#'),
        CurieNamespace('qud', 'http://qudt.org/1.1/schema/qudt#'),
        CurieNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'),
        CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#'),
        CurieNamespace('schema', 'http://schema.org/'),
        CurieNamespace('skos', 'http://www.w3.org/2004/02/skos/core#'),
        CurieNamespace('wgs', 'http://www.w3.org/2003/01/geo/wgs84_pos'),
        CurieNamespace('xsd', 'http://www.w3.org/2001/XMLSchema#'),
    ]

    # class level dictionaries

    _prefix_map: Dict[str, CurieNamespace] = {}

    @classmethod
    def _get_prefix_map(cls):
        if not cls._prefix_map:
            for ns in cls._namespaces:
                # index by upper case for uniformity of search
                cls._prefix_map[ns.prefix.upper()] = ns
        return cls._prefix_map

    @classmethod
    def parse_curie(cls, curie: str) -> Tuple[CurieNamespace, str]:
        """
        Parse a candidate CURIE
        :param curie: candidate curie string
        :return: CURIE namespace and object_id
        """
        found = CurieNamespace("", ""), curie  # default value if not a CURIE or unknown XMLNS prefix
        if ':' in curie:
            part = curie.split(":")
            # Normalize retrieval with upper case of prefix for lookup
            prefix = part[0].upper()
            if prefix in cls._get_prefix_map():
                found = cls._prefix_map[prefix], part[1]
        return found

    @classmethod
    def parse_uri(cls, uri: str) -> Tuple[CurieNamespace,  str]:
        """
        Parse a candidate URI
        :param uri: candidate URI string
        :return: namespace and object_id
        """
        found = CurieNamespace("", ""), uri   # default value returned if unknown URI namespace

        # TODO: is there a more efficient lookup scheme here than a linear search of namespaces?
        for ns in cls._namespaces:
            base_uri = str(ns)
            if uri.startswith(base_uri):
                # simple minded deletion of base_uri to give the object_id
                object_id = uri.replace(base_uri, "")
                found = ns, object_id
                break
        return found

    @classmethod
    def parse_identifier(cls,  identifier: str) -> Tuple[CurieNamespace,  str]:

        # trivial case of a null identifier?
        if not identifier:
            return CurieNamespace("", ""), ""

        # check if this is a candidate URI...
        if identifier.lower().startswith("http"):
            # guess that perhaps it is, so try to parse it
            return cls.parse_uri(identifier)

        else:  # attempt to parse as a CURIE
            return cls.parse_curie(identifier)


def object_id(identifier, keep_version=False) -> str:
    """
    Returns the core object_id of a CURIE, with or without the version suffix.
    Note:  not designed to be used with a URI (will give an invalid outcome)
    :param identifier: candidate CURIE identifier for processing
    :param keep_version: True if the version string suffix is to be retained in the identifier
    :return:
    """
    # trivial case: null input value?
    if not identifier:
        return identifier

    if ':' in identifier:
        identifier = identifier.split(":")[1]

    if not keep_version and '.' in identifier:
        identifier = identifier.split(".")[0]

    return identifier


def fix_curies(identifiers, prefix=''):
    """
    Applies the specified XMLNS prefix to (an) identifier(s) known
    to be "raw" IDs as keys in a dictionary or elements in a list (or a simple string)
    :param identifiers:
    :param prefix:
    :return:
    """
    if not prefix:
        # return identifiers without modification
        # Caller may already consider them in curie format
        return identifiers

    if isinstance(identifiers, dict):
        curie_dict = defaultdict(dict)
        for key in identifiers.keys():
            curie_dict[prefix + ':' + object_id(key, keep_version=True)] = identifiers[key]
        return curie_dict

    # identifiers assumed to be just a single object identifier
    elif isinstance(identifiers, str):
        # single string to convert
        return prefix + ':' + object_id(identifiers, keep_version=True)

    elif isinstance(identifiers, Iterable):
        return [prefix + ':' + object_id(x, keep_version=True) for x in identifiers]

    else:
        raise RuntimeError("fix_curie() is not sure how to fix an instance of data type '", type(identifiers))


def curie(identifier) -> str:
    # Ignore enpty strings
    if not identifier:
        return ""
    else:
        namespace: CurieNamespace
        identifier_object_id: str
        namespace, identifier_object_id = BiolinkNameSpace.parse_identifier(identifier)
        return namespace.curie(identifier_object_id)
