
# Class: BirthEvent




URI: [ks:BirthEvent](https://w3id.org/linkml/tests/kitchen_sink/BirthEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[Place],[Event],[Place]<in%20location%200..1-%20[BirthEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has%20birth%20event%200..1>[BirthEvent],[Event]^-[BirthEvent],[Person])](https://yuml.me/diagram/nofunky;dir:TB/class/[Place],[Event],[Place]<in%20location%200..1-%20[BirthEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[Person]++-%20has%20birth%20event%200..1>[BirthEvent],[Event]^-[BirthEvent],[Person])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Class

 *  **None** *[has birth event](has_birth_event.md)*  <sub>0..1</sub>  **[BirthEvent](BirthEvent.md)**

## Attributes


### Own

 * [in location](in_location.md)  <sub>0..1</sub>
     * Range: [Place](Place.md)

### Inherited from Event:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
