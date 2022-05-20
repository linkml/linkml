
# Class: material sample


A sample is a limited quantity of something (e.g. an individual or set of individuals from a population, or a portion of a substance) to be used for testing, analysis, inspection, investigation, demonstration, or trial use. [SIO]

URI: [biolink:MaterialSample](https://w3id.org/biolink/vocab/MaterialSample)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SubjectOfInvestigation],[PhysicalEntity],[NamedThing],[MaterialSampleToEntityAssociationMixin],[MaterialSampleDerivationAssociation],[MaterialSampleDerivationAssociation]-%20subject%201..1>[MaterialSample&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MaterialSampleToEntityAssociationMixin]-%20subject%201..1>[MaterialSample],[MaterialSample]uses%20-.->[SubjectOfInvestigation],[PhysicalEntity]^-[MaterialSample],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[SubjectOfInvestigation],[PhysicalEntity],[NamedThing],[MaterialSampleToEntityAssociationMixin],[MaterialSampleDerivationAssociation],[MaterialSampleDerivationAssociation]-%20subject%201..1>[MaterialSample&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[MaterialSampleToEntityAssociationMixin]-%20subject%201..1>[MaterialSample],[MaterialSample]uses%20-.->[SubjectOfInvestigation],[PhysicalEntity]^-[MaterialSample],[Attribute],[Agent])

## Identifier prefixes

 * BIOSAMPLE
 * GOLD.META

## Parents

 *  is_a: [PhysicalEntity](PhysicalEntity.md) - An entity that has material reality (a.k.a. physical essence).

## Uses Mixin

 *  mixin: [SubjectOfInvestigation](SubjectOfInvestigation.md) - An entity that has the role of being studied in an investigation, study, or experiment

## Referenced by Class

 *  **[MaterialSampleDerivationAssociation](MaterialSampleDerivationAssociation.md)** *[material sample derivation association➞subject](material_sample_derivation_association_subject.md)*  <sub>1..1</sub>  **[MaterialSample](MaterialSample.md)**
 *  **[MaterialSampleToEntityAssociationMixin](MaterialSampleToEntityAssociationMixin.md)** *[material sample to entity association mixin➞subject](material_sample_to_entity_association_mixin_subject.md)*  <sub>1..1</sub>  **[MaterialSample](MaterialSample.md)**

## Attributes


### Inherited from physical entity:

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
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [provided by](provided_by.md)  <sub>0..\*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * Range: [Agent](Agent.md)
 * [has attribute](has_attribute.md)  <sub>0..\*</sub>
     * Description: connects any entity to an attribute
     * Range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Description: Name of the high level ontology class in which this entity is categorized. Corresponds to the label for the biolink entity type class.
 * In a neo4j database this MAY correspond to the neo4j label tag.
 * In an RDF database it should be a biolink model class URI.
This field is multi-valued. It should include values for ancestors of the biolink class; for example, a protein such as Shh would have category values `biolink:Protein`, `biolink:GeneProduct`, `biolink:MolecularEntity`, ...
In an RDF database, nodes will typically have an rdf:type triples. This can be to the most specific biolink class, or potentially to a class more specific than something in biolink. For example, a sequence feature `f` may have a rdf:type assertion to a SO class such as TF_binding_site, which is more specific than anything in biolink. Here we would have categories {biolink:GenomicEntity, biolink:MolecularEntity, biolink:NamedThing}
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | biospecimen |
|  | | sample |
|  | | biosample |
|  | | physical sample |
| **Exact Mappings:** | | OBI:0000747 |
|  | | SIO:001050 |

