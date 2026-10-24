# Middleware

Once data volume grows, pushing everything straight into the database over a single path breaks down. You need a layer in between to move and transform the data. Distributed message systems and stream processing platforms are that layer: the former guarantees data gets delivered reliably, the latter processes and analyzes data the moment it arrives.

#### 1.1 The Evolution of Data Architecture

In the early days everything ran on centralized databases. As data volume grew you hit performance bottlenecks, and scaling was capped by a single machine. Distributed message systems and stream processing platforms grew out of that need: concurrent data streams are spread across multiple nodes, so one point of failure does not take down the whole system.

#### 1.2 What Message Systems and Stream Processing Do

**Message systems** (such as Apache Kafka, RabbitMQ) handle asynchronous data transfer; system components communicate with each other in the form of messages. They provide message persistence, routing and consumption, but more importantly they decouple the two ends: the producer just throws into the queue, the consumer pulls at its own pace, and adding or removing machines for scaling never requires changing the other side's code.

**Stream processing platforms** (such as Apache Flink, Apache Storm) handle continuous data streams; data can be processed as soon as it arrives, which differs from batch processing that waits to accumulate a batch before computing. Event-driven applications and real-time dashboards are all built on this process-as-you-go capability.

## References

- [Apache Kafka official documentation](https://kafka.apache.org/documentation/)

## Sibling pages

- [ApacheKafka](/middleware/ApacheKafka.md)
- [MessageQueue](/middleware/MessageQueue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ApacheKafka](/middleware/ApacheKafka.md)
- [MessageQueue](/middleware/MessageQueue.md)
