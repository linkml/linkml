package org.sink.kitchen;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class Concept  {

  private string id;
  private string name;
  private CodeSystem inCodeSystem;

}