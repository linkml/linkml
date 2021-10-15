package org.sink.kitchen;

import java.util.List;
import lombok.*;


@Data
@EqualsAndHashCode(callSuper=false)
public class Dataset  {

  private List<Person> persons;
  private List<Company> companies;
  private List<Activity> activities;

}