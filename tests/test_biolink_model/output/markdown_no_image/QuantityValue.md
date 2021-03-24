
# Class: QuantityValue


A value of an attribute that is quantitative and measurable, expressed as a combination of a unit and a numeric value

URI: [biolink:QuantityValue](https://w3id.org/biolink/vocab/QuantityValue)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[Attribute]++-%20has%20quantitative%20value%200..*>[QuantityValue&#124;has_unit:unit%20%3F;has_numeric_value:double%20%3F],[Annotation]^-[QuantityValue],[Attribute],[Annotation])

## Parents

 *  is_a: [Annotation](Annotation.md) - Biolink Model root class for entity annotations.

## Referenced by class

 *  **[Attribute](Attribute.md)** *[has quantitative value](has_quantitative_value.md)*  <sub>0..*</sub>  **[QuantityValue](QuantityValue.md)**

## Attributes


### Own

 * [has numeric value](has_numeric_value.md)  <sub>OPT</sub>
     * Description: connects a quantity value to a number
     * range: [Double](types/Double.md)
     * in subsets: (samples)
 * [has unit](has_unit.md)  <sub>OPT</sub>
     * Description: connects a quantity value to a unit
     * range: [Unit](types/Unit.md)
     * in subsets: (samples)
