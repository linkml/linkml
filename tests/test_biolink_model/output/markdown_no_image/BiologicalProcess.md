
# Class: BiologicalProcess


One or more causally connected executions of molecular functions

URI: [biolink:BiologicalProcess](https://w3id.org/biolink/vocab/BiologicalProcess)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[PhysiologicalProcess],[PhysicalEntity],[Pathway],[PathologicalProcess],[OntologyClass],[Occurrent],[NamedThing],[MacromolecularMachineToBiologicalProcessAssociation],[Death],[BiologicalProcessOrActivity],[MacromolecularMachineToBiologicalProcessAssociation]-%20object%201..1>[BiologicalProcess&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[BiologicalProcess]uses%20-.->[Occurrent],[BiologicalProcess]uses%20-.->[OntologyClass],[BiologicalProcess]^-[PhysiologicalProcess],[BiologicalProcess]^-[Pathway],[BiologicalProcess]^-[PathologicalProcess],[BiologicalProcess]^-[Death],[BiologicalProcess]^-[Behavior],[BiologicalProcessOrActivity]^-[BiologicalProcess],[Behavior],[Attribute],[Agent])

## Identifier prefixes

 * GO
 * REACT
 * MetaCyc
 * KEGG.MODULE

## Parents

 *  is_a: [BiologicalProcessOrActivity](BiologicalProcessOrActivity.md) - Either an individual molecular activity, or a collection of causally connected molecular activities in a biological system.

## Uses Mixins

 *  mixin: [Occurrent](Occurrent.md) - A processual entity.
 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [Behavior](Behavior.md)
 * [Death](Death.md)
 * [PathologicalProcess](PathologicalProcess.md) - A biologic function or a process having an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.
 * [Pathway](Pathway.md)
 * [PhysiologicalProcess](PhysiologicalProcess.md)

## Referenced by class

 *  **[MacromolecularMachineToBiologicalProcessAssociation](MacromolecularMachineToBiologicalProcessAssociation.md)** *[macromolecular machine to biological process association➞object](macromolecular_machine_to_biological_process_association_object.md)*  <sub>REQ</sub>  **[BiologicalProcess](BiologicalProcess.md)**

## Attributes


### Inherited from biological process or activity:

 * [description](description.md)  <sub>OPT</sub>
     * Description: a human-readable description of an entity
     * range: [NarrativeText](types/NarrativeText.md)
     * in subsets: (translator_minimal)
 * [enabled by](enabled_by.md)  <sub>0..*</sub>
     * Description: holds between a process and a physical entity, where the physical entity executes the process
     * range: [PhysicalEntity](PhysicalEntity.md)
     * in subsets: (translator_minimal)
 * [has attribute](has_attribute.md)  <sub>0..*</sub>
     * Description: connects any entity to an attribute
     * range: [Attribute](Attribute.md)
     * in subsets: (samples)
 * [has input](has_input.md)  <sub>0..*</sub>
     * Description: holds between a process and a continuant, where the continuant is an input into the process
     * range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
 * [has output](has_output.md)  <sub>0..*</sub>
     * Description: holds between a process and a continuant, where the continuant is an output of the process
     * range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
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

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | GO:0008150 |
|  | | SIO:000006 |
|  | | WIKIDATA:Q2996394 |

