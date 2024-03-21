
# Class: UnitOfMeasure


A unit of measure, or unit, is a particular quantity value that has been chosen as a scale for  measuring other quantities the same kind (more generally of equivalent dimension).

URI: [linkml:UnitOfMeasure](https://w3id.org/linkml/UnitOfMeasure)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression]++-%20unit%200..1>[UnitOfMeasure&#124;symbol:string%20%3F;abbreviation:string%20%3F;descriptive_name:string%20%3F;exact_mappings:uriorcurie%20*;ucum_code:string%20%3F;derivation:string%20%3F;has_quantity_kind:uriorcurie%20%3F;iec61360code:string%20%3F],[SlotExpression]++-%20unit%200..1>[UnitOfMeasure],[PermissibleValue]++-%20unit%200..1>[UnitOfMeasure],[TypeExpression],[SlotExpression],[PermissibleValue])](https://yuml.me/diagram/nofunky;dir:TB/class/[TypeExpression]++-%20unit%200..1>[UnitOfMeasure&#124;symbol:string%20%3F;abbreviation:string%20%3F;descriptive_name:string%20%3F;exact_mappings:uriorcurie%20*;ucum_code:string%20%3F;derivation:string%20%3F;has_quantity_kind:uriorcurie%20%3F;iec61360code:string%20%3F],[SlotExpression]++-%20unit%200..1>[UnitOfMeasure],[PermissibleValue]++-%20unit%200..1>[UnitOfMeasure],[TypeExpression],[SlotExpression],[PermissibleValue])

## Referenced by Class

 *  **None** *[unit](unit.md)*  <sub>0..1</sub>  **[UnitOfMeasure](UnitOfMeasure.md)**

## Attributes


### Own

 * [symbol](symbol.md)  <sub>0..1</sub>
     * Description: name of the unit encoded as a symbol
     * Range: [String](types/String.md)
 * [abbreviation](abbreviation.md)  <sub>0..1</sub>
     * Description: An abbreviation for a unit is a short ASCII string that is used in place of the full name for the unit in  contexts where non-ASCII characters would be problematic, or where using the abbreviation will enhance  readability. When a power of a base unit needs to be expressed, such as squares this can be done using  abbreviations rather than symbols (source: qudt)
     * Range: [String](types/String.md)
 * [descriptive_name](descriptive_name.md)  <sub>0..1</sub>
     * Description: the spelled out name of the unit, for example, meter
     * Range: [String](types/String.md)
 * [UnitOfMeasure➞exact mappings](UnitOfMeasure_exact_mappings.md)  <sub>0..\*</sub>
     * Description: Used to link a unit to equivalent concepts in ontologies such as UO, SNOMED, OEM, OBOE, NCIT
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [ucum_code](ucum_code.md)  <sub>0..1</sub>
     * Description: associates a QUDT unit with its UCUM code (case-sensitive).
     * Range: [String](types/String.md)
 * [derivation](derivation.md)  <sub>0..1</sub>
     * Description: Expression for deriving this unit from other units
     * Range: [String](types/String.md)
 * [has_quantity_kind](has_quantity_kind.md)  <sub>0..1</sub>
     * Description: Concept in a vocabulary or ontology that denotes the kind of quantity being measured, e.g. length
     * Range: [Uriorcurie](types/Uriorcurie.md)
 * [iec61360code](iec61360code.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | qudt:Unit |

