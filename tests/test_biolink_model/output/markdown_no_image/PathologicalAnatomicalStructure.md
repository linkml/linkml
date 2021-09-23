
# Class: pathological anatomical structure


An anatomical structure with the potential of have an abnormal or deleterious effect at the subcellular, cellular, multicellular, or organismal level.

URI: [biolink:PathologicalAnatomicalStructure](https://w3id.org/biolink/vocab/PathologicalAnatomicalStructure)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[PathologicalEntityMixin],[PathologicalAnatomicalStructure&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[PathologicalEntityMixin],[PathologicalAnatomicalStructure]^-[PathologicalAnatomicalOutcome],[PathologicalAnatomicalStructure]^-[PathologicalAnatomicalExposure],[AnatomicalEntity]^-[PathologicalAnatomicalStructure],[PathologicalAnatomicalOutcome],[PathologicalAnatomicalExposure],[OrganismTaxon],[NamedThing],[Attribute],[AnatomicalEntity],[Agent])](https://yuml.me/diagram/nofunky;dir:TB/class/[PathologicalEntityMixin],[PathologicalAnatomicalStructure&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[PathologicalEntityMixin],[PathologicalAnatomicalStructure]^-[PathologicalAnatomicalOutcome],[PathologicalAnatomicalStructure]^-[PathologicalAnatomicalExposure],[AnatomicalEntity]^-[PathologicalAnatomicalStructure],[PathologicalAnatomicalOutcome],[PathologicalAnatomicalExposure],[OrganismTaxon],[NamedThing],[Attribute],[AnatomicalEntity],[Agent])

## Parents

 *  is_a: [AnatomicalEntity](AnatomicalEntity.md) - A subcellular location, cell type or gross anatomical part

## Uses Mixin

 *  mixin: [PathologicalEntityMixin](PathologicalEntityMixin.md) - A pathological (abnormal) structure or process.

## Children

 * [PathologicalAnatomicalExposure](PathologicalAnatomicalExposure.md) - An abnormal anatomical structure, when viewed as an exposure, representing an precondition, leading to or influencing an outcome, e.g. thrombosis leading to an ischemic disease outcome.
 * [PathologicalAnatomicalOutcome](PathologicalAnatomicalOutcome.md) - An outcome resulting from an exposure event which is the manifestation of an abnormal anatomical structure.

## Referenced by Class


## Attributes


### Inherited from anatomical entity:

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
 * [named thing➞category](named_thing_category.md)  <sub>1..\*</sub>
     * Range: [NamedThing](NamedThing.md)
 * [organismal entity➞has attribute](organismal_entity_has_attribute.md)  <sub>0..\*</sub>
     * Description: may often be an organism attribute
     * Range: [Attribute](Attribute.md)
