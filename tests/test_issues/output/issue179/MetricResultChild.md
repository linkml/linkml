
# Class: //example.org/sample/example1/MetricResultChild




URI: [http://example.org/sample/example1/MetricResultChild](http://example.org/sample/example1/MetricResultChild)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[MetricResultChild&#124;result_child_slot:string%20%3F;has_child_messages:string%20%3F;evaluated_using(i):string%20%3F;has_source(i):string%20%3F;has_status(i):string%20%3F;description(i):string%20%3F;has_messages(i):string%20%3F]uses%20-.->[HasMessagesChild],[MetricResult]^-[MetricResultChild],[MetricResult],[HasMessagesChild])

## Parents

 *  is_a: [MetricResult](MetricResult.md) - Result of executing a metric on a KS

## Uses Mixins

 *  mixin: [HasMessagesChild](HasMessagesChild.md)

## Attributes


### Own

 * [result child slot](result_child_slot.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Inherited from metric result:

 * [description](description.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [evaluated using](evaluated_using.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [has source](has_source.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [has status](has_status.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Mixed in from has messages child:

 * [has child messages](has_child_messages.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Mixed in from has messages class:

 * [has messages](has_messages.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
