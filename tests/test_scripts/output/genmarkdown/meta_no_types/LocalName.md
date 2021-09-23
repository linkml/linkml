
# Class: local_name


an attributed label

URI: [linkml:LocalName](https://w3id.org/linkml/LocalName)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Element]++-%20local_names%200..*>[LocalName&#124;local_name_source(pk):ncname;local_name_value:string],[Element])](https://yuml.me/diagram/nofunky;dir:TB/class/[Element]++-%20local_names%200..*>[LocalName&#124;local_name_source(pk):ncname;local_name_value:string],[Element])

## Referenced by Class

 *  **[Element](Element.md)** *[local_names](local_names.md)*  <sub>0..\*</sub>  **[LocalName](LocalName.md)**

## Attributes


### Own

 * [local_name_source](local_name_source.md)  <sub>1..1</sub>
     * Description: the ncname of the source of the name
     * Range: [Ncname](Ncname.md)
 * [local_name_value](local_name_value.md)  <sub>1..1</sub>
     * Description: a name assigned to an element in a given ontology
     * Range: [String](String.md)
