
# Class: PathologicalProcess


A biologic function or a process having an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.

URI: [biolink:PathologicalProcess](https://w3id.org/biolink/vocab/PathologicalProcess)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[PhysicalEntity],[PathologicalProcessOutcome],[PathologicalProcessExposure],[PathologicalProcess&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[PathologicalEntityMixin],[PathologicalProcess]^-[PathologicalProcessOutcome],[PathologicalProcess]^-[PathologicalProcessExposure],[BiologicalProcess]^-[PathologicalProcess],[PathologicalEntityMixin],[NamedThing],[BiologicalProcess],[Attribute],[Agent])

## Parents

 *  is_a: [BiologicalProcess](BiologicalProcess.md) - One or more causally connected executions of molecular functions

## Uses Mixins

 *  mixin: [PathologicalEntityMixin](PathologicalEntityMixin.md) - A pathological (abnormal) structure or process.

## Children

 * [PathologicalProcessExposure](PathologicalProcessExposure.md) - A pathological process, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. autoimmunity leading to disease.
 * [PathologicalProcessOutcome](PathologicalProcessOutcome.md) - An outcome resulting from an exposure event which is the manifestation of a pathological process.

## Referenced by class


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
| **Exact Mappings:** | | OBI:1110122 |
|  | | NCIT:C16956 |
| **Narrow Mappings:** | | NCIT:C19151 |
|  | | EFO:0009708 |

