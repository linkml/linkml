
# Class: //example.org/sample/example1/MetricResult


Result of executing a metric on a KS

URI: [http://example.org/sample/example1/MetricResult](http://example.org/sample/example1/MetricResult)


![img](http://yuml.me/diagram/nofunky;dir:TB/class/[MetricResultChild],[MetricResult&#124;evaluated_using:string%20%3F;has_source:string%20%3F;has_status:string%20%3F;description:string%20%3F;has_messages:string%20%3F]uses%20-.->[HasMessagesClass],[MetricResult]^-[MetricResultChild],[HasMessagesClass])

## Uses Mixins

 *  mixin: [HasMessagesClass](HasMessagesClass.md)

## Children

 * [MetricResultChild](MetricResultChild.md)

## Referenced by class


## Attributes


### Own

 * [description](description.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [evaluated using](evaluated_using.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [has source](has_source.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
 * [has status](has_status.md)  <sub>OPT</sub>
     * range: [String](types/String.md)

### Mixed in from has messages class:

 * [has messages](has_messages.md)  <sub>OPT</sub>
     * range: [String](types/String.md)
