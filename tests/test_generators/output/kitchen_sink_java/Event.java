package org.sink.kitchen;

import java.util.List;
import lombok.*;







@Data
@EqualsAndHashCode(callSuper=false)
public class Event  {

  private date startedAtTime;
  private date endedAtTime;
  private boolean isCurrent;
  private AnyObject metadata;

}