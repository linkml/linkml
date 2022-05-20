package org.sink.kitchen;

import java.util.List;
import lombok.*;






/**
  A person, living or dead
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class Person  {

  private string id;
  private string name;
  private List<EmploymentEvent> hasEmploymentHistory;
  private List<FamilialRelationship> hasFamilialRelationships;
  private List<MedicalEvent> hasMedicalHistory;
  private integer ageInYears;
  private List<Address> addresses;
  private BirthEvent hasBirthEvent;
  private List<string> aliases;

}