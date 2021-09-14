package org.sink.kitchen;

import java.util.List;
import lombok.*;

/**
  None
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class Relationship  {

  private String startedAtTime;
  private String endedAtTime;
  private String relatedTo;
  private String type;

}