
# Class: attribute


A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.

URI: [biolink:Attribute](https://w3id.org/biolink/vocab/Attribute)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Zygosity],[SocioeconomicAttribute],[SeverityValue],[QuantityValue],[OrganismalEntity],[OrganismAttribute],[OntologyClass],[NamedThing],[Entity],[ClinicalAttribute],[BiologicalSex],[NamedThing]<has%20qualitative%20value%200..1-%20[Attribute&#124;name:label_type%20%3F;iri:iri_type%20%3F;source:label_type%20%3F],[QuantityValue]<has%20quantitative%20value%200..*-++[Attribute],[OntologyClass]<has%20attribute%20type%201..1-++[Attribute],[Entity]++-%20has%20attribute%200..*>[Attribute],[OrganismalEntity]++-%20has%20attribute%200..*>[Attribute],[Attribute]uses%20-.->[OntologyClass],[Attribute]^-[Zygosity],[Attribute]^-[SocioeconomicAttribute],[Attribute]^-[SeverityValue],[Attribute]^-[OrganismAttribute],[Attribute]^-[ClinicalAttribute],[Attribute]^-[BiologicalSex],[Annotation]^-[Attribute],[Annotation])](https://yuml.me/diagram/nofunky;dir:TB/class/[Zygosity],[SocioeconomicAttribute],[SeverityValue],[QuantityValue],[OrganismalEntity],[OrganismAttribute],[OntologyClass],[NamedThing],[Entity],[ClinicalAttribute],[BiologicalSex],[NamedThing]<has%20qualitative%20value%200..1-%20[Attribute&#124;name:label_type%20%3F;iri:iri_type%20%3F;source:label_type%20%3F],[QuantityValue]<has%20quantitative%20value%200..*-++[Attribute],[OntologyClass]<has%20attribute%20type%201..1-++[Attribute],[Entity]++-%20has%20attribute%200..*>[Attribute],[OrganismalEntity]++-%20has%20attribute%200..*>[Attribute],[Attribute]uses%20-.->[OntologyClass],[Attribute]^-[Zygosity],[Attribute]^-[SocioeconomicAttribute],[Attribute]^-[SeverityValue],[Attribute]^-[OrganismAttribute],[Attribute]^-[ClinicalAttribute],[Attribute]^-[BiologicalSex],[Annotation]^-[Attribute],[Annotation])

## Identifier prefixes

 * EDAM-DATA
 * EDAM-FORMAT
 * EDAM-OPERATION
 * EDAM-TOPIC

## Parents

 *  is_a: [Annotation](Annotation.md) - Biolink Model root class for entity annotations.

## Uses Mixin

 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [BiologicalSex](BiologicalSex.md)
 * [ClinicalAttribute](ClinicalAttribute.md) - Attributes relating to a clinical manifestation
 * [OrganismAttribute](OrganismAttribute.md) - describes a characteristic of an organismal entity.
 * [SeverityValue](SeverityValue.md) - describes the severity of a phenotypic feature or disease
 * [SocioeconomicAttribute](SocioeconomicAttribute.md) - Attributes relating to a socioeconomic manifestation
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
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | samples |
| **Exact Mappings:** | | SIO:000614 |

