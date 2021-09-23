
# Class: MedicalEvent




URI: [ks:MedicalEvent](https://w3id.org/linkml/tests/kitchen_sink/MedicalEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ProcedureConcept],[Place],[ProcedureConcept]<procedure%200..1-++[MedicalEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[DiagnosisConcept]<diagnosis%200..1-++[MedicalEvent],[Place]<in%20location%200..1-%20[MedicalEvent],[Person]++-%20has%20medical%20history%200..*>[MedicalEvent],[Event]^-[MedicalEvent],[Person],[Event],[DiagnosisConcept])](https://yuml.me/diagram/nofunky;dir:TB/class/[ProcedureConcept],[Place],[ProcedureConcept]<procedure%200..1-++[MedicalEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;is_current(i):boolean%20%3F],[DiagnosisConcept]<diagnosis%200..1-++[MedicalEvent],[Place]<in%20location%200..1-%20[MedicalEvent],[Person]++-%20has%20medical%20history%200..*>[MedicalEvent],[Event]^-[MedicalEvent],[Person],[Event],[DiagnosisConcept])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Class

 *  **None** *[has medical history](has_medical_history.md)*  <sub>0..\*</sub>  **[MedicalEvent](MedicalEvent.md)**

## Attributes


### Own

 * [in location](in_location.md)  <sub>0..1</sub>
     * Range: [Place](Place.md)
 * [diagnosis](diagnosis.md)  <sub>0..1</sub>
     * Range: [DiagnosisConcept](DiagnosisConcept.md)
 * [procedure](procedure.md)  <sub>0..1</sub>
     * Range: [ProcedureConcept](ProcedureConcept.md)

### Inherited from Event:

 * [started at time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended at time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [is current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
