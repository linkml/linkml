
# Class: agent


a provence-generating agent

URI: [core:Agent](https://w3id.org/linkml/tests/core/Agent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Activity]<was%20informed%20by%200..1-%20[Agent&#124;id:string],[Agent]<acted%20on%20behalf%20of%200..1-%20[Agent],[Activity]-%20was%20associated%20with%200..1>[Agent],[Activity])](https://yuml.me/diagram/nofunky;dir:TB/class/[Activity]<was%20informed%20by%200..1-%20[Agent&#124;id:string],[Agent]<acted%20on%20behalf%20of%200..1-%20[Agent],[Activity]-%20was%20associated%20with%200..1>[Agent],[Activity])

## Referenced by Class

 *  **None** *[acted on behalf of](acted_on_behalf_of.md)*  <sub>0..1</sub>  **[Agent](Agent.md)**
 *  **None** *[agent set](agent_set.md)*  <sub>0..\*</sub>  **[Agent](Agent.md)**
 *  **None** *[was associated with](was_associated_with.md)*  <sub>0..1</sub>  **[Agent](Agent.md)**

## Attributes


### Own

 * [id](id.md)  <sub>1..1</sub>
     * Range: [String](types/String.md)
 * [acted on behalf of](acted_on_behalf_of.md)  <sub>0..1</sub>
     * Range: [Agent](Agent.md)
 * [was informed by](was_informed_by.md)  <sub>0..1</sub>
     * Range: [Activity](Activity.md)

## Other properties

|  |  |  |
| --- | --- | --- |
| **Mappings:** | | prov:Agent |

