
# Class: EmploymentEvent




URI: [personinfo:EmploymentEvent](https://w3id.org/linkml/examples/personinfo/EmploymentEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization],[Event],[Organization]<employed_at%200..1-%20[EmploymentEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;duration(i):float%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has_employment_history%200..*>[EmploymentEvent],[Event]^-[EmploymentEvent],[Person])](https://yuml.me/diagram/nofunky;dir:TB/class/[Organization],[Event],[Organization]<employed_at%200..1-%20[EmploymentEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;duration(i):float%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has_employment_history%200..*>[EmploymentEvent],[Event]^-[EmploymentEvent],[Person])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Class

 *  **None** *[has_employment_history](has_employment_history.md)*  <sub>0..\*</sub>  **[EmploymentEvent](EmploymentEvent.md)**

## Attributes


### Own

 * [employed_at](employed_at.md)  <sub>0..1</sub>
     * Range: [Organization](Organization.md)

### Inherited from Event:

 * [started_at_time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended_at_time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [duration](duration.md)  <sub>0..1</sub>
     * Range: [Float](types/Float.md)
 * [is_current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
