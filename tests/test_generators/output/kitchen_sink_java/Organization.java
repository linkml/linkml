package org.sink.kitchen;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class Organization  {

  private string id;
  private string name;
  private List<string> aliases;

}