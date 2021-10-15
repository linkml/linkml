package org.sink.kitchen;

import java.util.List;
import lombok.*;


@Data
@EqualsAndHashCode(callSuper=false)
public class BirthEvent extends Event {

  private Place inLocation;

}