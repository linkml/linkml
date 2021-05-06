
# Class: SocioeconomicAttribute


Attributes relating to a socioeconomic manifestation

URI: [biolink:SocioeconomicAttribute](https://w3id.org/biolink/vocab/SocioeconomicAttribute)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[SocioeconomicExposure],[SocioeconomicExposure]++-%20has%20attribute%201..*>[SocioeconomicAttribute&#124;name(i):label_type%20%3F;iri(i):iri_type%20%3F;source(i):label_type%20%3F],[Attribute]^-[SocioeconomicAttribute],[QuantityValue],[OntologyClass],[NamedThing],[Attribute])

## Parents

 *  is_a: [Attribute](Attribute.md) - A property or characteristic of an entity. For example, an apple may have properties such as color, shape, age, crispiness. An environmental sample may have attributes such as depth, lat, long, material.

## Referenced by class

 *  **[SocioeconomicExposure](SocioeconomicExposure.md)** *[socioeconomic exposure➞has attribute](socioeconomic_exposure_has_attribute.md)*  <sub>1..*</sub>  **[SocioeconomicAttribute](SocioeconomicAttribute.md)**

## Attributes


### Inherited from attribute:

 * [attribute➞name](attribute_name.md)  <sub>OPT</sub>
     * Description: The human-readable 'attribute name' can be set to a string which reflects its context of interpretation, e.g. SEPIO evidence/provenance/confidence annotation or it can default to the name associated with the 'has attribute type' slot ontology term.
     * range: [LabelType](types/LabelType.md)
 * [has attribute type](has_attribute_type.md)  <sub>REQ</sub>
     * Description: connects an attribute to a class that describes it
     * range: [OntologyClass](OntologyClass.md)
     * in subsets: (samples)
 * [has qualitative value](has_qualitative_value.md)  <sub>OPT</sub>
     * Description: connects an attribute to a value
     * range: [NamedThing](NamedThing.md)
     * in subsets: (samples)
 * [has quantitative value](has_quantitative_value.md)  <sub>0..*</sub>
     * Description: connects an attribute to a value
     * range: [QuantityValue](QuantityValue.md)
     * in subsets: (samples)
 * [iri](iri.md)  <sub>OPT</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [source](source.md)  <sub>OPT</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)
