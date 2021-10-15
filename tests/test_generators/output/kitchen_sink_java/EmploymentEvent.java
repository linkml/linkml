package org.sink.kitchen;

import java.util.List;
import lombok.*;


@Data
@EqualsAndHashCode(callSuper=false)
public class EmploymentEvent extends Event {

  private Company employedAt;

}