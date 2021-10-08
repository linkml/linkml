package org.sink.kitchen;

import java.util.List;
import lombok.*;

/**
  None
**/
@Data
@EqualsAndHashCode(callSuper=false)
public  class MarriageEvent extend Event {

  private Person marriedTo;
  private Place inLocation;

}