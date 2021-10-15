package org.sink.kitchen;

import java.util.List;
import lombok.*;


@Data
@EqualsAndHashCode(callSuper=false)
public class Event  {

  private String startedAtTime;
  private String endedAtTime;
  private Boolean isCurrent;

}