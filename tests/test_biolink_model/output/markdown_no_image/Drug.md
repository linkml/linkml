
# Class: Drug


A substance intended for use in the diagnosis, cure, mitigation, treatment, or prevention of disease

URI: [biolink:Drug](https://w3id.org/biolink/vocab/Drug)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[OrganismTaxon],[OntologyClass],[NamedThing],[MolecularEntity],[Mixture],[DrugToEntityAssociationMixin],[DrugExposure],[DrugToEntityAssociationMixin]-%20subject%201..1>[Drug&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Treatment]-%20has%20drug%200..*>[Drug],[Drug]uses%20-.->[Mixture],[Drug]uses%20-.->[OntologyClass],[Drug]^-[DrugExposure],[MolecularEntity]^-[Drug],[Treatment],[ChemicalSubstance],[Attribute],[Agent])

## Identifier prefixes

 * RXCUI
 * NDC
 * PHARMGKB.DRUG

## Parents

 *  is_a: [MolecularEntity](MolecularEntity.md) - A gene, gene product, small molecule or macromolecule (including protein complex)"

## Uses Mixins

 *  mixin: [Mixture](Mixture.md) - The physical combination of two or more molecular entities in which the identities are retained and are mixed in the form of solutions, suspensions and colloids.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [DrugExposure](DrugExposure.md) - A drug exposure is an intake of a particular drug.

## Referenced by class

 *  **[DrugToEntityAssociationMixin](DrugToEntityAssociationMixin.md)** *[drug to entity association mixin➞subject](drug_to_entity_association_mixin_subject.md)*  <sub>REQ</sub>  **[Drug](Drug.md)**
 *  **[NamedThing](NamedThing.md)** *[has drug](has_drug.md)*  <sub>0..*</sub>  **[Drug](Drug.md)**
 *  **[ChemicalSubstance](ChemicalSubstance.md)** *[is active ingredient of](is_active_ingredient_of.md)*  <sub>0..*</sub>  **[Drug](Drug.md)**
 *  **[ChemicalSubstance](ChemicalSubstance.md)** *[is excipient of](is_excipient_of.md)*  <sub>0..*</sub>  **[Drug](Drug.md)**

## Attributes


### Inherited from molecular entity:

 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..*</sub>
     * Description: connects any entity to an attribute
     * range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [id](id.md)  <sub>REQ</sub>
     * Description: A unique identifier for an entity. Must be either a CURIE shorthand for a URI or a complete URI
     * range: [String](types/String.md)
     * in subsets: (translator_minimal)
 * [iri](iri.md)  <sub>OPT</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [name](name.md)  <sub>OPT</sub>
     * Description: A human-readable name for an attribute or entity.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [named thing➞category](named_thing_category.md)  <sub>1..*</sub>
     * range: [NamedThing](NamedThing.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
 * [type](type.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Mixed in from mixture:

 * [has constituent](has_constituent.md)  <sub>0..*</sub>
     * Description: one or more chemical substances within a mixture
     * range: [ChemicalSubstance](ChemicalSubstance.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Comments:** | | The CHEBI ID represents a role rather than a substance |
| **Exact Mappings:** | | WIKIDATA:Q12140 |
|  | | CHEBI:23888 |
|  | | UMLSSC:T200 |
|  | | UMLSST:clnd |
| **Narrow Mappings:** | | UMLSSC:T195 |
|  | | UMLSST:antb |
| **Broad Mappings:** | | UMLSSC:T121 |
|  | | UMLSST:phsu |

