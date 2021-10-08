
# Class: behavior




URI: [biolink:Behavior](https://w3id.org/biolink/vocab/Behavior)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[SocioeconomicOutcome],[SocioeconomicExposure],[PhysicalEntity],[OntologyClass],[NamedThing],[BiologicalProcess],[BehavioralOutcome],[BehavioralExposure],[BehaviorToBehavioralFeatureAssociation],[BehaviorToBehavioralFeatureAssociation]-%20subject%201..1>[Behavior&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Behavior]uses%20-.->[OntologyClass],[Behavior]^-[SocioeconomicOutcome],[Behavior]^-[SocioeconomicExposure],[Behavior]^-[BehavioralOutcome],[Behavior]^-[BehavioralExposure],[BiologicalProcess]^-[Behavior],[Attribute],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[SocioeconomicOutcome],[SocioeconomicExposure],[PhysicalEntity],[OntologyClass],[NamedThing],[BiologicalProcess],[BehavioralOutcome],[BehavioralExposure],[BehaviorToBehavioralFeatureAssociation],[BehaviorToBehavioralFeatureAssociation]-%20subject%201..1>[Behavior&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F],[Behavior]uses%20-.->[OntologyClass],[Behavior]^-[SocioeconomicOutcome],[Behavior]^-[SocioeconomicExposure],[Behavior]^-[BehavioralOutcome],[Behavior]^-[BehavioralExposure],[BiologicalProcess]^-[Behavior],[Attribute],[Agent])

## Parents

 *  is_a: [BiologicalProcess](BiologicalProcess.md) - One or more causally connected executions of molecular functions

## Uses Mixin

 *  mixin: [OntologyClass](OntologyClass.md) - a concept or class in an ontology, vocabulary or thesaurus. Note that nodes in a biolink compatible KG can be considered both instances of biolink classes, and OWL classes in their own right. In general you should not need to use this class directly. Instead, use the appropriate biolink class. For example, for the GO concept of endocytosis (GO:0006897), use bl:BiologicalProcess as the type.

## Children

 * [BehavioralExposure](BehavioralExposure.md) - A behavioral exposure is a factor relating to behavior impacting an individual.
 * [BehavioralOutcome](BehavioralOutcome.md) - An outcome resulting from an exposure event which is the manifestation of human behavior.
 * [SocioeconomicExposure](SocioeconomicExposure.md) - A socioeconomic exposure is a factor relating to social and financial status of an affected individual (e.g. poverty).
 * [SocioeconomicOutcome](SocioeconomicOutcome.md) - An general social or economic outcome, such as healthcare costs, utilization, etc., resulting from an exposure event

## Referenced by Class

 *  **[BehaviorToBehavioralFeatureAssociation](BehaviorToBehavioralFeatureAssociation.md)** *[behavior to behavioral feature association➞subject](behavior_to_behavioral_feature_association_subject.md)*  <sub>1..1</sub>  **[Behavior](Behavior.md)**

## Attributes


### Inherited from biological process:

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
 * [has input](has_input.md)  <sub>0..\*</sub>
     * Description: holds between a process and a continuant, where the continuant is an input into the process
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
 * [has output](has_output.md)  <sub>0..\*</sub>
     * Description: holds between a process and a continuant, where the continuant is an output of the process
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (translator_minimal)
 * [enabled by](enabled_by.md)  <sub>0..\*</sub>
     * Description: holds between a process and a physical entity, where the physical entity executes the process
     * Range: [PhysicalEntity](PhysicalEntity.md)
     * in subsets: (translator_minimal)

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

