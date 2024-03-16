
# Class: organismal entity


A named entity that is either a part of an organism, a whole organism, population or clade of organisms, excluding chemical entities

URI: [biolink:OrganismalEntity](https://w3id.org/biolink/vocab/OrganismalEntity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Virus],[SubjectOfInvestigation],[PopulationOfIndividualOrganisms],[OrganismalEntityAsAModelOfDiseaseAssociation],[Attribute]<has%20attribute%200..*-%20[OrganismalEntity&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[OrganismalEntityAsAModelOfDiseaseAssociation]-%20subject%201..1>[OrganismalEntity],[OrganismalEntity]uses%20-.->[SubjectOfInvestigation],[OrganismalEntity]^-[Virus],[OrganismalEntity]^-[PopulationOfIndividualOrganisms],[OrganismalEntity]^-[LifeStage],[OrganismalEntity]^-[IndividualOrganism],[OrganismalEntity]^-[CellularOrganism],[OrganismalEntity]^-[CellLine],[OrganismalEntity]^-[AnatomicalEntity],[BiologicalEntity]^-[OrganismalEntity],[OrganismTaxon],[LifeStage],[IndividualOrganism],[ExposureEvent],[CellularOrganism],[CellLine],[BiologicalEntity],[Attribute],[AnatomicalEntity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Virus],[SubjectOfInvestigation],[PopulationOfIndividualOrganisms],[OrganismalEntityAsAModelOfDiseaseAssociation],[Attribute]<has%20attribute%200..*-%20[OrganismalEntity&#124;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F],[OrganismalEntityAsAModelOfDiseaseAssociation]-%20subject%201..1>[OrganismalEntity],[OrganismalEntity]uses%20-.->[SubjectOfInvestigation],[OrganismalEntity]^-[Virus],[OrganismalEntity]^-[PopulationOfIndividualOrganisms],[OrganismalEntity]^-[LifeStage],[OrganismalEntity]^-[IndividualOrganism],[OrganismalEntity]^-[CellularOrganism],[OrganismalEntity]^-[CellLine],[OrganismalEntity]^-[AnatomicalEntity],[BiologicalEntity]^-[OrganismalEntity],[OrganismTaxon],[LifeStage],[IndividualOrganism],[ExposureEvent],[CellularOrganism],[CellLine],[BiologicalEntity],[Attribute],[AnatomicalEntity])

## Parents

 *  is_a: [BiologicalEntity](BiologicalEntity.md)

## Uses Mixin

 *  mixin: [SubjectOfInvestigation](SubjectOfInvestigation.md) - An entity that has the role of being studied in an investigation, study, or experiment

## Children

 * [AnatomicalEntity](AnatomicalEntity.md) - A subcellular location, cell type or gross anatomical part
 * [CellLine](CellLine.md)
 * [CellularOrganism](CellularOrganism.md)
 * [IndividualOrganism](IndividualOrganism.md) - An instance of an organism. For example, Richard Nixon, Charles Darwin, my pet cat. Example ID: ORCID:0000-0002-5355-2576
 * [LifeStage](LifeStage.md) - A stage of development or growth of an organism, including post-natal adult stages
 * [PopulationOfIndividualOrganisms](PopulationOfIndividualOrganisms.md) - A collection of individuals from the same taxonomic class distinguished by one or more characteristics.  Characteristics can include, but are not limited to, shared geographic location, genetics, phenotypes.
 * [Virus](Virus.md) - A virus is a microorganism that replicates itself as a microRNA and infects the host cell.

## Referenced by Class

 *  **[ExposureEvent](ExposureEvent.md)** *[has receptor](has_receptor.md)*  <sub>0..1</sub>  **[OrganismalEntity](OrganismalEntity.md)**
 *  **[OrganismalEntityAsAModelOfDiseaseAssociation](OrganismalEntityAsAModelOfDiseaseAssociation.md)** *[organismal entity as a model of disease association➞subject](organismal_entity_as_a_model_of_disease_association_subject.md)*  <sub>1..1</sub>  **[OrganismalEntity](OrganismalEntity.md)**

## Attributes


### Own

 * [organismal entity➞has attribute](organismal_entity_has_attribute.md)  <sub>0..\*</sub>
     * Description: may often be an organism attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)

### Inherited from biological entity:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [name](name.md)  <sub>0..1</sub>
     * Description: A human-readable name for an attribute or entity.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: The value in this node property represents the knowledge provider that created or assembled the node and all of its attributes.  Used internally to represent how a particular node made its way into a knowledge provider or graph.
     * Range: [String](types/String.md)
 * [xref](xref.md)  <sub>0..\*</sub>
     * Description: Alternate CURIEs for a thing
     * Range: [Uriorcurie](types/Uriorcurie.md)
     * in subsets: (translator_minimal)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [CategoryType](types/CategoryType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | WIKIDATA:Q7239 |
|  | | UMLSSG:LIVB |
|  | | CARO:0001010 |

