
# Class: MedicalEvent




URI: [ks:MedicalEvent](https://w3id.org/linkml/tests/kitchen_sink/MedicalEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Person]++-%20has%20medical%20history%200..*>[MedicalEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Event]^-[MedicalEvent],[Person],[Event])](https://yuml.me/diagram/nofunky;dir:TB/class/[Person]++-%20has%20medical%20history%200..*>[MedicalEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Event]^-[MedicalEvent],[Person],[Event])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by class

 *  **None** *[has medical history](has_medical_history.md)*  <sub>0..\*</sub>  **[MedicalEvent](MedicalEvent.md)**

## Attributes


### Inherited from Event:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](Boolean.md)
