package org.sink.kitchen;

import java.util.List;
import lombok.*;

/**
  None
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class BirthEvent extends Event {

  private Place inLocation;

}