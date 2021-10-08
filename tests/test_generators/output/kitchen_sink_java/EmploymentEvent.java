package org.sink.kitchen;

import java.util.List;
import lombok.*;

/**
  None
**/
@Data
@EqualsAndHashCode(callSuper=false)
public  class EmploymentEvent extend Event {

  private Company employedAt;

}