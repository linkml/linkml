package org.sink.kitchen;

import java.util.List;
import lombok.*;


@Data
@EqualsAndHashCode(callSuper=false)
public class Place  {

  private String id;
  private String name;
  private List<String> aliases;

}