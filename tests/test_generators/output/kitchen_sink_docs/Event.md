
# Class: Event




URI: [ks:Event](https://w3id.org/linkml/tests/kitchen_sink/Event)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MedicalEvent],[MarriageEvent],[AnyObject]<metadata%200..1-++[Event&#124;started_at_time:date%20%3F;ended_at_time:date%20%3F;is_current:boolean%20%3F],[Event]^-[MedicalEvent],[Event]^-[MarriageEvent],[Event]^-[EmploymentEvent],[Event]^-[BirthEvent],[EmploymentEvent],[BirthEvent],[AnyObject])](https://yuml.me/diagram/nofunky;dir:TB/class/[MedicalEvent],[MarriageEvent],[AnyObject]<metadata%200..1-++[Event&#124;started_at_time:date%20%3F;ended_at_time:date%20%3F;is_current:boolean%20%3F],[Event]^-[MedicalEvent],[Event]^-[MarriageEvent],[Event]^-[EmploymentEvent],[Event]^-[BirthEvent],[EmploymentEvent],[BirthEvent],[AnyObject])

## Children

 * [BirthEvent](BirthEvent.md)
 * [EmploymentEvent](EmploymentEvent.md)
 * [MarriageEvent](MarriageEvent.md)
 * [MedicalEvent](MedicalEvent.md)

## Referenced by Record


## Attributes


### Own

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](Boolean.md)
 * [metadata](metadata.md)  <sub>0..1</sub>
     * Description: Example of a slot that has an unconstrained range
     * Range: [AnyObject](AnyObject.md)
