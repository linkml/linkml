
# Class: HospitalizationOutcome


An outcome resulting from an exposure event which is the increased manifestation of acute (e.g. emergency room visit) or chronic (inpatient) hospitalization.

URI: [biolink:HospitalizationOutcome](https://w3id.org/biolink/vocab/HospitalizationOutcome)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Outcome],[NamedThing],[HospitalizationOutcome&#124;id(i):string;iri(i):iri_type%20%3F;type(i):string%20%3F;name(i):label_type%20%3F;description(i):narrative_text%20%3F;source(i):label_type%20%3F]uses%20-.->[Outcome],[Hospitalization]^-[HospitalizationOutcome],[Hospitalization],[Attribute],[Agent])

## Parents

 *  is_a: [Hospitalization](Hospitalization.md)

## Uses Mixins

 *  mixin: [Outcome](Outcome.md) - An entity that has the role of being the consequence of an exposure event. This is an abstract mixin grouping of various categories of possible biological or non-biological (e.g. clinical) outcomes.

## Attributes


### Inherited from hospitalization:

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
