
# Class: phenotypic sex


An attribute corresponding to the phenotypic sex of the individual, based upon the reproductive organs present.

URI: [biolink:PhenotypicSex](https://w3id.org/biolink/vocab/PhenotypicSex)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[QuantityValue],[BiologicalSex]^-[PhenotypicSex&#124;name(i):label_type%20%3F;iri(i):iri_type%20%3F;source(i):label_type%20%3F],[OntologyClass],[NamedThing],[BiologicalSex])](https://yuml.me/diagram/nofunky;dir:TB/class/[QuantityValue],[BiologicalSex]^-[PhenotypicSex&#124;name(i):label_type%20%3F;iri(i):iri_type%20%3F;source(i):label_type%20%3F],[OntologyClass],[NamedThing],[BiologicalSex])

## Parents

 *  is_a: [BiologicalSex](BiologicalSex.md)

## Attributes


### Inherited from biological sex:

 * [attribute➞name](attribute_name.md)  <sub>0..1</sub>
     * Description: The human-readable 'attribute name' can be set to a string which reflects its context of interpretation, e.g. SEPIO evidence/provenance/confidence annotation or it can default to the name associated with the 'has attribute type' slot ontology term.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal,samples)
 * [has attribute type](has_attribute_type.md)  <sub>1..1</sub>
     * Description: connects an attribute to a class that describes it
     * Range: [OntologyClass](OntologyClass.md)
     * in subsets: (samples)
 * [has quantitative value](has_quantitative_value.md)  <sub>0..\*</sub>
     * Description: connects an attribute to a value
     * Range: [QuantityValue](QuantityValue.md)
     * in subsets: (samples)
 * [has qualitative value](has_qualitative_value.md)  <sub>0..1</sub>
     * Description: connects an attribute to a value
     * Range: [NamedThing](NamedThing.md)
     * in subsets: (samples)
 * [iri](iri.md)  <sub>0..1</sub>
     * Description: An IRI for an entity. This is determined by the id using expansion rules.
     * Range: [IriType](types/IriType.md)
     * in subsets: (translator_minimal,samples)
 * [source](source.md)  <sub>0..1</sub>
     * Description: a lightweight analog to the association class 'has provider' slot, which is the string name, or the authoritative (i.e. database) namespace, designating the origin of the entity to which the slot belongs.
     * Range: [LabelType](types/LabelType.md)
     * in subsets: (translator_minimal)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Exact Mappings:** | | PATO:0001894 |

