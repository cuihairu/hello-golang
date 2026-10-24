# Message Queue Systems

#### 2. Overview of Message Queue Systems

Message Queue Systems are middleware used for asynchronous message delivery. They pass messages between different applications or system components, and are common in scenarios that need to decouple components, scale horizontally, or handle high-throughput messaging.

##### 2.1 Basic Concepts of Message Queues

- **Message queue**: a data structure used to store and pass messages. Messages are sent into the queue, then retrieved from the queue by a consumer system. The message queue ensures message ordering and reliability, allowing loose coupling between producers and consumers.

- **Producers and consumers**:
  - **Producer**: an application or service that sends messages to the queue.
  - **Consumer**: an application or service that receives and processes messages from the queue.

- **Message delivery models**:
  - **Point-to-Point**: messages are sent to a specific queue, and a single consumer receives messages from that queue.
  - **Publish/Subscribe**: messages are published to a topic, and multiple subscribers can receive the messages published to that topic.

- **Message persistence**: messages can be stored persistently, ensuring they are not lost even when the system fails. This usually involves writing messages to disk or a database.

- **Message acknowledgement**: after a consumer processes a message, it typically sends an acknowledgement back to the system to indicate the message was handled successfully. This helps ensure messages are neither lost nor processed twice.

##### 2.2 Application Scenarios for Message Queue Systems

- **Asynchronous processing**: message queues allow different components of a system to process tasks asynchronously, improving response time and throughput. Common uses include sending email, processing payments, and handling images.

- **Decoupling**: message queues decouple producers from consumers, so system components can be developed, deployed and scaled independently. This improves the system's flexibility and maintainability.

- **Load balancing**: message queues can distribute messages across multiple consumers, achieving load balancing and thus raising the system's processing capacity.

- **Reliability and fault tolerance**: through message persistence and message acknowledgement, message queue systems provide high reliability and fault tolerance. Even after a system failure, messages can still be recovered and processed.

- **Data stream processing**: message queue systems can be used for real-time data stream processing, passing data from producers to consumers to support real-time analysis and decision making.

- **Task scheduling**: message queues can be used for task scheduling, passing tasks from task generators to task executors, enabling delayed and timed task execution.

## References

- [Apache Kafka official documentation](https://kafka.apache.org/documentation/)

## Sibling pages

- [ApacheKafka](/middleware/ApacheKafka.md)
- [Readme](/middleware/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ApacheKafka](/middleware/ApacheKafka.md)
- [Readme](/middleware/Readme.md)
