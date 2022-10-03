
# Class: setting


assignment of a key to a value

URI: [linkml:Setting](https://w3id.org/linkml/Setting)


[![img](images/Setting.svg)](images/Setting.svg)

## Referenced by Class

 *  **[ImportExpression](ImportExpression.md)** *[import_map](import_map.md)*  <sub>0..\*</sub>  **[Setting](Setting.md)**
 *  **[SchemaDefinition](SchemaDefinition.md)** *[settings](settings.md)*  <sub>0..\*</sub>  **[Setting](Setting.md)**

## Attributes


### Own

 * [setting_key](setting_key.md)  <sub>1..1</sub>
     * Description: the variable name for a setting
     * Range: [Ncname](types/Ncname.md)
 * [setting_value](setting_value.md)  <sub>1..1</sub>
     * Description: The value assigned for a setting
     * Range: [String](types/String.md)
