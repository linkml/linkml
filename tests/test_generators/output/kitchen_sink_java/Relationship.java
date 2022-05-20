package org.sink.kitchen;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class Relationship  {

  private date startedAtTime;
  private date endedAtTime;
  private string relatedTo;
  private string type;

}