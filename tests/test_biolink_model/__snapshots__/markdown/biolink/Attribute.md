
# Class: attribute


A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.

URI: [biolink:Attribute](https://w3id.org/biolink/vocab/Attribute)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Zygosity],[SocioeconomicExposure],[SocioeconomicAttribute],[SeverityValue],[QuantityValue],[PathologicalProcessExposure],[PathologicalAnatomicalExposure],[OrganismalEntity],[OrganismAttribute],[OntologyClass],[NamedThing],[GenomicBackgroundExposure],[EnvironmentalExposure],[Entity],[DiseaseOrPhenotypicFeatureExposure],[ComplexChemicalExposure],[ClinicalAttribute],[ChemicalRole],[ChemicalExposure],[BioticExposure],[BiologicalSex],[BehavioralExposure],[NamedThing]<has%20qualitative%20value%200..1-%20[Attribute&#124;name:label_type%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;description(i):narrative_text%20%3F],[QuantityValue]<has%20quantitative%20value%200..*-++[Attribute],[OntologyClass]<has%20attribute%20type%201..1-%20[Attribute],[Entity]-%20has%20attribute%200..*>[Attribute],[OrganismalEntity]-%20has%20attribute%200..*>[Attribute],[Attribute]uses%20-.->[OntologyClass],[Attribute]^-[Zygosity],[Attribute]^-[SocioeconomicExposure],[Attribute]^-[SocioeconomicAttribute],[Attribute]^-[SeverityValue],[Attribute]^-[PathologicalProcessExposure],[Attribute]^-[PathologicalAnatomicalExposure],[Attribute]^-[OrganismAttribute],[Attribute]^-[GenomicBackgroundExposure],[Attribute]^-[EnvironmentalExposure],[Attribute]^-[DiseaseOrPhenotypicFeatureExposure],[Attribute]^-[ComplexChemicalExposure],[Attribute]^-[ClinicalAttribute],[Attribute]^-[ChemicalRole],[Attribute]^-[ChemicalExposure],[Attribute]^-[BioticExposure],[Attribute]^-[BiologicalSex],[Attribute]^-[BehavioralExposure],[NamedThing]^-[Attribute])](https://yuml.me/diagram/nofunky;dir:TB/class/[Zygosity],[SocioeconomicExposure],[SocioeconomicAttribute],[SeverityValue],[QuantityValue],[PathologicalProcessExposure],[PathologicalAnatomicalExposure],[OrganismalEntity],[OrganismAttribute],[OntologyClass],[NamedThing],[GenomicBackgroundExposure],[EnvironmentalExposure],[Entity],[DiseaseOrPhenotypicFeatureExposure],[ComplexChemicalExposure],[ClinicalAttribute],[ChemicalRole],[ChemicalExposure],[BioticExposure],[BiologicalSex],[BehavioralExposure],[NamedThing]<has%20qualitative%20value%200..1-%20[Attribute&#124;name:label_type%20%3F;provided_by(i):string%20*;xref(i):uriorcurie%20*;category(i):category_type%20%2B;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;description(i):narrative_text%20%3F],[QuantityValue]<has%20quantitative%20value%200..*-++[Attribute],[OntologyClass]<has%20attribute%20type%201..1-%20[Attribute],[Entity]-%20has%20attribute%200..*>[Attribute],[OrganismalEntity]-%20has%20attribute%200..*>[Attribute],[Attribute]uses%20-.->[OntologyClass],[Attribute]^-[Zygosity],[Attribute]^-[SocioeconomicExposure],[Attribute]^-[SocioeconomicAttribute],[Attribute]^-[SeverityValue],[Attribute]^-[PathologicalProcessExposure],[Attribute]^-[PathologicalAnatomicalExposure],[Attribute]^-[OrganismAttribute],[Attribute]^-[GenomicBackgroundExposure],[Attribute]^-[EnvironmentalExposure],[Attribute]^-[DiseaseOrPhenotypicFeatureExposure],[Attribute]^-[ComplexChemicalExposure],[Attribute]^-[ClinicalAttribute],[Attribute]^-[ChemicalRole],[Attribute]^-[ChemicalExposure],[Attribute]^-[BioticExposure],[Attribute]^-[BiologicalSex],[Attribute]^-[BehavioralExposure],[NamedThing]^-[Attribute])

## Identifier prefixes

 * EDAM-DATA
 * EDAM-FORMAT
 * EDAM-OPERATION
 * EDAM-TOPIC

## Parents

 *  is_a: [NamedThing](NamedThing.md) - a databased entity or concept/class

## Uses Mixin

 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [BehavioralExposure](BehavioralExposure.md) - A behavioral exposure is a factor relating to behavior impacting an individual.
 * [BiologicalSex](BiologicalSex.md)
 * [BioticExposure](BioticExposure.md) - An external biotic exposure is an intake of (sometimes pathological) biological organisms (including viruses).
 * [ChemicalExposure](ChemicalExposure.md) - A chemical exposure is an intake of a particular chemical entity.
 * [ChemicalRole](ChemicalRole.md) - A role played by the molecular entity or part thereof within a chemical context.
 * [ClinicalAttribute](ClinicalAttribute.md) - Attributes relating to a clinical manifestation
 * [ComplexChemicalExposure](ComplexChemicalExposure.md) - A complex chemical exposure is an intake of a chemical mixture (e.g. gasoline), other than a drug.
 * [DiseaseOrPhenotypicFeatureExposure](DiseaseOrPhenotypicFeatureExposure.md) - A disease or phenotypic feature state, when viewed as an exposure, represents an precondition, leading to or influencing an outcome, e.g. HIV predisposing an individual to infections; a relative deficiency of skin pigmentation predisposing an individual to skin cancer.
 * [EnvironmentalExposure](EnvironmentalExposure.md) - A environmental exposure is a factor relating to abiotic processes in the environment including sunlight (UV-B), atmospheric (heat, cold, general pollution) and water-born contaminants.
 * [GenomicBackgroundExposure](GenomicBackgroundExposure.md) - A genomic background exposure is where an individual's specific genomic background of genes, sequence variants or other pre-existing genomic conditions constitute a kind of 'exposure' to the organism, leading to or influencing an outcome.
 * [OrganismAttribute](OrganismAttribute.md) - describes a characteristic of an organismal entity.
 * [PathologicalAnatomicalExposure](PathologicalAnatomicalExposure.md) - An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
 * [PathologicalProcessExposure](PathologicalProcessExposure.md) - A pathological process, when viewed as an exposure, representing a precondition, leading to or influencing an outcome, e.g. autoimmunity leading to disease.
 * [SeverityValue](SeverityValue.md) - describes the severity of a phenotypic feature or disease
 * [SocioeconomicAttribute](SocioeconomicAttribute.md) - Attributes relating to a socioeconomic manifestation
 * [SocioeconomicExposure](SocioeconomicExposure.md) - A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g. poverty).
 * [Zygosity](Zygosity.md)

## Referenced by Class

 *  **[Entity](Entity.md)** *[has attribute](has_attribute.md)*  <sub>0..\*</sub>  **[Attribute](Attribute.md)**
 *  **[OrganismalEntity](OrganismalEntity.md)** *[organismal entity➞has attribute](organismal_entity_has_attribute.md)*  <sub>0..\*</sub>  **[Attribute](Attribute.md)**

## Attributes


### Own

 * [attribute➞name](attribute_name.md)  <sub>0..1</sub>
     * Description: The human-readable 'attribute name' can be set to a string which reflects its context of interpretation, e.g. SEPIO evidence/provenance/confidence annotation or it can default to the name associated with the 'has attribute type' slot ontology term.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [has attribute type](has_attribute_type.md)  <sub>1..1</sub>
     * Description: connects an attribute to a class that describes it
     * Range: [OntologyClass](OntologyClass.md)
     * in subsets: (samples)
 * [has quantitative value](has_quantitative_value.md)  <sub>0..\*</sub>
     * Description: connects an attribute to a value
     * Range: [QuantityValue](QuantityValue.md)
     * in subsets: (samples)
 * [has qualitative value](has_qualitative_value.md)  <sub>0..1</sub>
     * Description: connects an attribute to a value
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (samples)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)

### Inherited from named thing:

 * [id](id.md)  <sub>1..1</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * Range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [type](type.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Description: a human-readable description of an entity
     * Range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
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
| **In Subsets:** | | samples |
| **Exact Mappings:** | | SIO:000614 |

