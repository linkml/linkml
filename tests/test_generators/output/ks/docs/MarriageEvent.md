
# Class: MarriageEvent




URI: [ks:MarriageEvent](https://w3id.org/linkml/tests/kitchen_sink/MarriageEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[WithLocation],[Place],[Person],[Person]<married%20to%200..1-%20[MarriageEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[MarriageEvent]uses%20-.->[WithLocation],[Event]^-[MarriageEvent],[Event])](https://yuml.me/diagram/nofunky;dir:TB/class/[WithLocation],[Place],[Person],[Person]<married%20to%200..1-%20[MarriageEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[MarriageEvent]uses%20-.->[WithLocation],[Event]^-[MarriageEvent],[Event])

## Parents

 *  is_a: [Event](Event.md)

## Uses Mixin

 *  mixin: [WithLocation](WithLocation.md)

## Referenced by Class

 *  **None** *[has marriage history](has_marriage_history.md)*  <sub>0..\*</sub>  **[MarriageEvent](MarriageEvent.md)**

## Attributes


### Own

 * [married to](married_to.md)  <sub>0..1</sub>
     * Range: [Person](Person.md)

### Inherited from Event:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)

### Mixed in from WithLocation:

 * [in location](in_location.md)  <sub>0..1</sub>
     * Range: [Place](Place.md)
