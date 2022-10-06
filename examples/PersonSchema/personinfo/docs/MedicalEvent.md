
# Class: MedicalEvent




URI: [personinfo:MedicalEvent](https://w3id.org/linkml/examples/personinfo/MedicalEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[ProcedureConcept],[Place],[ProcedureConcept]<procedure%200..1-++[MedicalEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;duration(i):float%20%3F;is_current(i):boolean%20%3F],[DiagnosisConcept]<diagnosis%200..1-++[MedicalEvent],[Place]<in_location%200..1-%20[MedicalEvent],[Person]++-%20has_medical_history%200..*>[MedicalEvent],[Event]^-[MedicalEvent],[Person],[Event],[DiagnosisConcept])](https://yuml.me/diagram/nofunky;dir:TB/class/[ProcedureConcept],[Place],[ProcedureConcept]<procedure%200..1-++[MedicalEvent&#124;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;duration(i):float%20%3F;is_current(i):boolean%20%3F],[DiagnosisConcept]<diagnosis%200..1-++[MedicalEvent],[Place]<in_location%200..1-%20[MedicalEvent],[Person]++-%20has_medical_history%200..*>[MedicalEvent],[Event]^-[MedicalEvent],[Person],[Event],[DiagnosisConcept])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Class

 *  **None** *[has_medical_history](has_medical_history.md)*  <sub>0..\*</sub>  **[MedicalEvent](MedicalEvent.md)**

## Attributes


### Own

 * [in_location](in_location.md)  <sub>0..1</sub>
     * Range: [Place](Place.md)
 * [diagnosis](diagnosis.md)  <sub>0..1</sub>
     * Range: [DiagnosisConcept](DiagnosisConcept.md)
 * [procedure](procedure.md)  <sub>0..1</sub>
     * Range: [ProcedureConcept](ProcedureConcept.md)

### Inherited from Event:

 * [started_at_time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended_at_time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [duration](duration.md)  <sub>0..1</sub>
     * Range: [Float](types/Float.md)
 * [is_current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
