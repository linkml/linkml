package org.sink.kitchen;

import java.util.List;
import lombok.*;

/**
  None
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class Address  {

  private String street;
  private String city;

}