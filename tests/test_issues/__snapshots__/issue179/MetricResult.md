
# Class: metric result


Result of executing a metric on a KS

URI: [http://example.org/sample/example1/MetricResult](http://example.org/sample/example1/MetricResult)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[MetricResultChild],[MetricResult&#124;evaluated_using:string%20%3F;has_source:string%20%3F;has_status:string%20%3F;description:string%20%3F;has_messages:string%20%3F]uses%20-.->[HasMessagesClass],[MetricResult]^-[MetricResultChild],[HasMessagesClass])](https://yuml.me/diagram/nofunky;dir:TB/class/[MetricResultChild],[MetricResult&#124;evaluated_using:string%20%3F;has_source:string%20%3F;has_status:string%20%3F;description:string%20%3F;has_messages:string%20%3F]uses%20-.->[HasMessagesClass],[MetricResult]^-[MetricResultChild],[HasMessagesClass])

## Uses Mixin

 *  mixin: [HasMessagesClass](HasMessagesClass.md)

## Children

 * [MetricResultChild](MetricResultChild.md)

## Referenced by Class


## Attributes


### Own

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
