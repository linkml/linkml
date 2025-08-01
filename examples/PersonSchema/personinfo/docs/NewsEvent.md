
# Class: NewsEvent



URI: [personinfo:NewsEvent](https://w3id.org/linkml/examples/personinfo/NewsEvent)


[![img](https://yuml.me/diagram/nofunky;dir:TB/class/[HasNewsEvents]++-%20has_news_events%200..*>[NewsEvent&#124;headline:string%20%3F;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;duration(i):float%20%3F;is_current(i):boolean%20%3F],[Event]^-[NewsEvent],[HasNewsEvents],[Event])](https://yuml.me/diagram/nofunky;dir:TB/class/[HasNewsEvents]++-%20has_news_events%200..*>[NewsEvent&#124;headline:string%20%3F;started_at_time(i):date%20%3F;ended_at_time(i):date%20%3F;duration(i):float%20%3F;is_current(i):boolean%20%3F],[Event]^-[NewsEvent],[HasNewsEvents],[Event])

## Parents

 *  is_a: [Event](Event.md)

## Referenced by Class

 *  **None** *[➞has_news_events](hasNewsEvents__has_news_events.md)*  <sub>0..\*</sub>  **[NewsEvent](NewsEvent.md)**

## Attributes


### Own

 * [➞headline](newsEvent__headline.md)  <sub>0..1</sub>
     * Range: [String](types/String.md)

### Inherited from Event:

 * [started_at_time](started_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [ended_at_time](ended_at_time.md)  <sub>0..1</sub>
     * Range: [Date](types/Date.md)
 * [duration](duration.md)  <sub>0..1</sub>
     * Range: [Float](types/Float.md)
 * [is_current](is_current.md)  <sub>0..1</sub>
     * Range: [Boolean](types/Boolean.md)
