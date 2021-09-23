
# Class: molecular activity


An execution of a molecular function carried out by a gene product or macromolecular complex.

URI: [biolink:MolecularActivity](https://w3id.org/biolink/vocab/MolecularActivity)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[Occurrent],[NamedThing],[MacromolecularMachineMixin]<enabled%20by%200..*-++[MolecularActivity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[ChemicalSubstance]<has%20output%200..*-%20[MolecularActivity],[ChemicalSubstance]<has%20input%200..*-%20[MolecularActivity],[MacromolecularMachineToMolecularActivityAssociation]-%20object%201..1>[MolecularActivity],[MolecularActivity]uses%20-.->[Occurrent],[MolecularActivity]uses%20-.->[OntologyClass],[BiologicalProcessOrActivity]^-[MolecularActivity],[MacromolecularMachineToMolecularActivityAssociation],[MacromolecularMachineMixin],[ChemicalSubstance],[BiologicalProcessOrActivity],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[OntologyClass],[Occurrent],[NamedThing],[MacromolecularMachineMixin]<enabled%20by%200..*-++[MolecularActivity&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[ChemicalSubstance]<has%20output%200..*-%20[MolecularActivity],[ChemicalSubstance]<has%20input%200..*-%20[MolecularActivity],[MacromolecularMachineToMolecularActivityAssociation]-%20object%201..1>[MolecularActivity],[MolecularActivity]uses%20-.->[Occurrent],[MolecularActivity]uses%20-.->[OntologyClass],[BiologicalProcessOrActivity]^-[MolecularActivity],[MacromolecularMachineToMolecularActivityAssociation],[MacromolecularMachineMixin],[ChemicalSubstance],[BiologicalProcessOrActivity],[Attribute],[Agent])

## Identifier prefixes

 * GO
 * REACT
 * RHEA
 * MetaCyc
 * EC
 * TCDB
 * KEGG.REACTION
 * KEGG.RCLASS
 * KEGG.ENZYME

## Parents

 *  is_a: [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md) - Either an individual molecular activity, or a collection of causally connected molecular activities in a biological system.

## Uses Mixin

 *  mixin: [Occurrent](Occurrent.md) - A processual entity.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Referenced by Class

 *  **[MacromolecularMachineToMolecularActivityAssociation](MacromolecularMachineToMolecularActivityAssociation.md)** *[macromolecular machine to molecular activity association➞object](macromolecular_machine_to_molecular_activity_association_object.md)*  <sub>1..1</sub>  **[MolecularActivity](MolecularActivity.md)**

## Attributes


### Own

 * [molecular activity➞has input](molecular_activity_has_input.md)  <sub>0..\*</sub>
     * Description: A chemical entity that is the input for the reaction
     * Range: [ChemicalSubstance](ChemicalSubstance.md)
 * [molecular activity➞has output](molecular_activity_has_output.md)  <sub>0..\*</sub>
     * Description: A chemical entity that is the output for the reaction
     * Range: [ChemicalSubstance](ChemicalSubstance.md)
 * [molecular activity➞enabled by](molecular_activity_enabled_by.md)  <sub>0..\*</sub>
     * Description: The gene product, gene, or complex that catalyzes the reaction
     * Range: [MacromolecularMachineMixin](MacromolecularMachineMixin.md)

### Inherited from biological process or activity:

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
     * Range: [NamedThing](NamedThing.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Aliases:** | | molecular function |
|  | | molecular event |
|  | | reaction |
| **Exact Mappings:** | | GO:0003674 |
|  | | UMLSSC:T044 |
|  | | UMLSST:moft |

