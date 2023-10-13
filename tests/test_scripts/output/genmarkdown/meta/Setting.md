
# Class: setting


assignment of a key to a value

URI: [linkml:Setting](https://w3id.org/linkml/Setting)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ImportExpression]++-%20import_map%200..*>[Setting&#124;setting_key(pk):ncname;setting_value:string],[SchemaDefinition]++-%20settings%200..*>[Setting],[SchemaDefinition],[ImportExpression])](https://yuml.me/diagram/nofunky;dir:TB/class/[ImportExpression]++-%20import_map%200..*>[Setting&#124;setting_key(pk):ncname;setting_value:string],[SchemaDefinition]++-%20settings%200..*>[Setting],[SchemaDefinition],[ImportExpression])

## Referenced by Class

 *  **[ImportExpression](ImportExpression.md)** *[import_map](import_map.md)*  <sub>0..\*</sub>  **[Setting](Setting.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[settings](settings.md)*  <sub>0..\*</sub>  **[Setting](Setting.md)**

## Attributes


### Own

 * [setting_key](setting_key.md)  <sub>1..1</sub>
     * Description: the variable name for a setting
     * Range: [Ncname](types/Ncname.md)
     * in subsets: (SpecificationSubset)
 * [setting_value](setting_value.md)  <sub>1..1</sub>
     * Description: The value assigned for a setting
     * Range: [String](types/String.md)
     * in subsets: (SpecificationSubset)

## Other properties

|  |  |  |
| --- | --- | --- |
| **In Subsets:** | | SpecificationSubset |

