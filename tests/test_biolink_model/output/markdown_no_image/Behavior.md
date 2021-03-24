
# Class: Behavior




URI: [biolink:Behavior](https://w3id.org/biolink/vocab/Behavior)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SocioeconomicOutcome],[SocioeconomicExposure],[PhysicalEntity],[OntologyClass],[NamedThing],[BiologicalProcess],[BehavioralOutcome],[BehavioralExposure],[BehaviorToBehavioralFeatureAssociation],[BehaviorToBehavioralFeatureAssociation]-%20subject%201..1>[Behavior&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Behavior]uses%20-.->[OntologyClass],[Behavior]^-[SocioeconomicOutcome],[Behavior]^-[SocioeconomicExposure],[Behavior]^-[BehavioralOutcome],[Behavior]^-[BehavioralExposure],[BiologicalProcess]^-[Behavior],[Attribute],[Agent])

## Parents

 *  is_a: [BiologicalProcess](BiologicalProcess.md) - One or more causally connected executions of molecular functions

## Uses Mixins

 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [BehavioralExposure](BehavioralExposure.md) - A behavioral exposure is a factor relating to behavior impacting an individual.
 * [BehavioralOutcome](BehavioralOutcome.md) - An outcome resulting from an exposure event which is the manifestation of human behavior.
 * [SocioeconomicExposure](SocioeconomicExposure.md) - A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g. poverty).
 * [SocioeconomicOutcome](SocioeconomicOutcome.md) - An general social or economic outcome, such as healthcare costs, utilization, etc., resulting from an exposure event

## Referenced by class

 *  **[BehaviorToBehavioralFeatureAssociation](BehaviorToBehavioralFeatureAssociation.md)** *[behavior to behavioral feature association➞subject](behavior_to_behavioral_feature_association_subject.md)*  <sub>REQ</sub>  **[Behavior](Behavior.md)**

## Attributes


### Inherited from biological process:

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
| **Exact Mappings:** | | GO:0007610 |
|  | | UMLSSC:T053 |
|  | | UMLSST:bhvr |
| **Narrow Mappings:** | | UMLSSC:T041 |
|  | | UMLSST:menp |
|  | | UMLSSC:T054 |
|  | | UMLSST:socb |
|  | | UMLSSC:T055 |
|  | | UMLSST:inbe |

