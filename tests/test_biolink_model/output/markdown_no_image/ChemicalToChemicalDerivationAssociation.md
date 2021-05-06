
# Class: ChemicalToChemicalDerivationAssociation


A causal relationship between two chemical entities, where the subject represents the upstream entity and the object represents the downstream. For any such association there is an implicit reaction:
  IF
  R has-input C1 AND
  R has-output C2 AND
  R enabled-by P AND
  R type Reaction
  THEN
  C1 derives-into C2 <<catalyst qualifier P>>

URI: [biolink:ChemicalToChemicalDerivationAssociation](https://w3id.org/biolink/vocab/ChemicalToChemicalDerivationAssociation)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Publication],[OntologyClass],[MacromolecularMachineMixin],[ChemicalSubstance]<object%201..1-%20[ChemicalToChemicalDerivationAssociation&#124;predicate:predicate_type;relation(i):uriorcurie;negated(i):boolean%20%3F;type(i):string%20%3F;category(i):category_type%20*;id(i):string;iri(i):iri_type%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[ChemicalSubstance]<subject%201..1-%20[ChemicalToChemicalDerivationAssociation],[MacromolecularMachineMixin]<catalyst%20qualifier%200..*-++[ChemicalToChemicalDerivationAssociation],[ChemicalToChemicalAssociation]^-[ChemicalToChemicalDerivationAssociation],[ChemicalToChemicalAssociation],[ChemicalSubstance],[Attribute],[Agent])

## Parents

 *  is_a: [ChemicalToChemicalAssociation](ChemicalToChemicalAssociation.md) - A relationship between two chemical entities. This can encompass actual interactions as well as temporal causal edges, e.g. one chemical converted to another.

## Referenced by class


## Attributes


### Own

 * [chemical to chemical derivation association➞catalyst qualifier](chemical_to_chemical_derivation_association_catalyst_qualifier.md)  <sub>0..*</sub>
     * Description: this connects the derivation edge to the molecular entity that catalyzes the reaction that causes the subject chemical to transform into the object chemical.
     * range: [MacromolecularMachineMixin](MacromolecularMachineMixin.md)
 * [chemical to chemical derivation association➞object](chemical_to_chemical_derivation_association_object.md)  <sub>REQ</sub>
     * Description: the downstream chemical entity
     * range: [ChemicalSubstance](ChemicalSubstance.md)
 * [chemical to chemical derivation association➞predicate](chemical_to_chemical_derivation_association_predicate.md)  <sub>REQ</sub>
     * range: [PredicateType](types/PredicateType.md)
 * [chemical to chemical derivation association➞subject](chemical_to_chemical_derivation_association_subject.md)  <sub>REQ</sub>
     * Description: the upstream chemical entity
     * range: [ChemicalSubstance](ChemicalSubstance.md)

### Inherited from chemical to chemical association:

 * [association➞category](association_category.md)  <sub>0..*</sub>
     * range: [CategoryType](types/CategoryType.md)
 * [association➞type](association_type.md)  <sub>OPT</sub>
     * Description: rdf:type of biolink:Association should be fixed at rdf:Statement
     * range: [String](types/String.md)
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
 * [negated](negated.md)  <sub>OPT</sub>
     * Description: if set to true, then the association is negated i.e. is not true
     * range: [Boolean](types/Boolean.md)
 * [provided by](provided_by.md)  <sub>0..*</sub>
     * Description: connects an association to the agent (person, organization or group) that provided it
     * range: [Agent](Agent.md)
 * [publications](publications.md)  <sub>0..*</sub>
     * Description: connects an association to publications supporting the association
     * range: [Publication](Publication.md)
 * [qualifiers](qualifiers.md)  <sub>0..*</sub>
     * Description: connects an association to qualifiers that modify or qualify the meaning of that association
     * range: [OntologyClass](OntologyClass.md)
 * [relation](relation.md)  <sub>REQ</sub>
     * Description: The relation which describes an association between a subject and an object in a more granular manner. Usually this is a term from Relation Ontology, but it can be any edge CURIE.
     * range: [Uriorcurie](types/Uriorcurie.md)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
