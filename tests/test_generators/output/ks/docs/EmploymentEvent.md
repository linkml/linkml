
# Class: EmploymentEvent




URI: [ks:EmploymentEvent](https://w3id.org/linkml/tests/kitchen_sink/EmploymentEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Event],[Company]<employed%20at%200..1-%20[EmploymentEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has%20employment%20history%200..*>[EmploymentEvent],[Event]^-[EmploymentEvent],[Person],[Company])](https://yuml.me/diagram/nofunky;dir:TB/class/[Event],[Company]<employed%20at%200..1-%20[EmploymentEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has%20employment%20history%200..*>[EmploymentEvent],[Event]^-[EmploymentEvent],[Person],[Company])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Class

 *  **None** *[has employment history](has_employment_history.md)*  <sub>0..\*</sub>  **[EmploymentEvent](EmploymentEvent.md)**

## Attributes


### Own

 * [employed at](employed_at.md)  <sub>0..1</sub>
     * Range: [Company](Company.md)
     * in subsets: (subset A)

### Inherited from Event:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
