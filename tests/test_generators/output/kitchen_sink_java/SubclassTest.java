package org.sink.kitchen;

import java.util.List;
import lombok.*;


@Data
@EqualsAndHashCode(callSuper=false)
public class SubclassTest extends ClassWithSpaces {

  private ClassWithSpaces slotWithSpace2;

}