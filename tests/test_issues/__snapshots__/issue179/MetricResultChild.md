
# Class: metric result child




URI: [http://example.org/sample/example1/MetricResultChild](http://example.org/sample/example1/MetricResultChild)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MetricResultChild&#124;result_child_slot:string%20%3F;has_child_messages:string%20%3F;evaluated_using(i):string%20%3F;has_source(i):string%20%3F;has_status(i):string%20%3F;description(i):string%20%3F;has_messages(i):string%20%3F]uses%20-.->[HasMessagesChild],[MetricResult]^-[MetricResultChild],[MetricResult],[HasMessagesChild])](https://yuml.me/diagram/nofunky;dir:TB/class/[MetricResultChild&#124;result_child_slot:string%20%3F;has_child_messages:string%20%3F;evaluated_using(i):string%20%3F;has_source(i):string%20%3F;has_status(i):string%20%3F;description(i):string%20%3F;has_messages(i):string%20%3F]uses%20-.->[HasMessagesChild],[MetricResult]^-[MetricResultChild],[MetricResult],[HasMessagesChild])

## Parents

 *  is_a: [MetricResult](MetricResult.md) - Result of executing a metric on a KS

## Uses Mixin

 *  mixin: [HasMessagesChild](HasMessagesChild.md)

## Attributes


### Own

 * [result child slot](result_child_slot.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Inherited from metric result:

 * [evaluated using](evaluated_using.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [has source](has_source.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [has status](has_status.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
 * [description](description.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Mixed in from has messages class:

 * [has messages](has_messages.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Mixed in from has messages child:

 * [has child messages](has_child_messages.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)
