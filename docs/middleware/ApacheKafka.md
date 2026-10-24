### Message Queue Systems

#### 3. Apache Kafka

Apache Kafka is an open-source distributed stream processing platform, designed for high-throughput, low-latency data stream processing. It was originally developed by LinkedIn and is now part of the Apache Software Foundation. Kafka can handle large volumes of messages and deliver high reliability and scalability, making it a commonly used message middleware in modern data architectures.

##### 3.1 Kafka Overview

- **Features**: Kafka provides high-throughput messaging and stream processing, and supports large-scale data stream processing and log aggregation.
- **Characteristics**: distributed, scalable, supports persistence and fault tolerance, suitable for both real-time data streams and batch processing.

##### 3.2 Kafka Architecture and Components

- **Broker**: the core component of Kafka, responsible for storing and forwarding messages. A Kafka cluster consists of multiple brokers, and each broker manages a portion of the messages.
- **Topic**: the logical classification unit for messages. Producers publish messages to a topic, and consumers read messages from a topic.
- **Partition**: each topic can be split into multiple partitions to achieve load balancing and parallel processing. Each partition is an ordered message log.
- **Producer**: an application or service that sends messages to Kafka.
- **Consumer**: an application or service that reads messages from Kafka.
- **Zookeeper**: Kafka uses Zookeeper for cluster management and coordination. Zookeeper handles broker metadata management, leader election, and configuration management.

##### 3.3 Kafka Persistence and Fault Tolerance

- **Persistence**: Kafka persists messages to disk, ensuring message reliability. Messages in each partition are stored as a log, and a retention policy (by time or by size) can be configured to manage storage.
- **Replication**: Kafka improves fault tolerance through replication. Each partition can have multiple replicas, ensuring that even if some brokers fail, the data can still be recovered from other replicas.
- **Leader-Follower model**: each partition has one leader and multiple followers. All read and write operations are handled by the leader, and followers sync data from the leader.

##### 3.4 Stream Processing with Kafka

- **Kafka Streams**: Kafka provides a stream processing library, Kafka Streams, that lets you do real-time stream processing inside Kafka itself. It supports state management, windowing, and complex event processing.
- **KSQL**: KSQL is the stream query engine that comes with Kafka, allowing you to query and analyze Kafka data streams using SQL syntax.

##### 3.5 Common Kafka Use Cases and Best Practices

- **Log aggregation**: Kafka can serve as a centralized log aggregation system, gathering log messages from different services into one central location for analysis.
- **Event sourcing**: Kafka supports event-driven architecture and can process and store application event streams.
- **Data pipelines**: Kafka is used to build real-time data pipelines, moving data from producer systems into data lakes, data warehouses, or other data stores.
- **Best practices**:
  - **Partition and replica settings**: set the partition and replica counts of a topic sensibly to optimize performance and fault tolerance.
  - **Message compression**: use message compression (such as Snappy, LZ4) to reduce storage footprint and network bandwidth.
  - **Monitoring and management**: use the monitoring tools Kafka provides (such as JMX) to watch cluster health and performance metrics.

##### **Using Kafka in Go**

- **Kafka Go client libraries**
  - **`confluent-kafka-go`**: the official Kafka Go client library from Confluent. It supports Kafka's core features such as producing and consuming messages, and managing topics and partitions.
  - **`sarama`**: an open-source Kafka Go client library with a rich API for interacting with Kafka. The repository has moved from `github.com/Shopify/sarama` to `github.com/IBM/sarama` (the old address is archived), so use the new address in the import path.

- **Basic operation examples**
  - **Producer example**:
    ```go
    package main

    import (
        "github.com/IBM/sarama"
        "log"
    )

    func main() {
        config := sarama.NewConfig()
        config.Producer.RequiredAcks = sarama.WaitForAll
        config.Producer.Retry.Max = 5
        config.Producer.Return.Successes = true

        producer, err := sarama.NewSyncProducer([]string{"localhost:9092"}, config)
        if err != nil {
            log.Fatal(err)
        }
        defer producer.Close()

        msg := &sarama.ProducerMessage{
            Topic: "example-topic",
            Value: sarama.StringEncoder("Hello, Kafka!"),
        }

        partition, offset, err := producer.SendMessage(msg)
        if err != nil {
            log.Fatal(err)
        }
        log.Printf("Message sent to partition %d at offset %d\n", partition, offset)
    }
    ```

  - **Consumer example**:
    ```go
    package main

    import (
        "github.com/IBM/sarama"
        "log"
    )

    func main() {
        config := sarama.NewConfig()
        config.Consumer.Return.Errors = true

        consumer, err := sarama.NewConsumer([]string{"localhost:9092"}, config)
        if err != nil {
            log.Fatal(err)
        }
        defer consumer.Close()

        partitionConsumer, err := consumer.ConsumePartition("example-topic", 0, sarama.OffsetNewest)
        if err != nil {
            log.Fatal(err)
        }
        defer partitionConsumer.Close()

        for msg := range partitionConsumer.Messages() {
            log.Printf("Received message: %s\n", string(msg.Value))
        }
    }
    ```

### Summary

The two code blocks above line up with the architecture concepts from earlier: the producer's `RequiredAcks` corresponds to the replication and leader read/write mechanism in section 3.3, and `Retry.Max` is one more layer of reliability on top of persistence. The consumer specifies a partition and `OffsetNewest`, which matches the design that "each partition is an ordered message log". Pick either of the two client libraries as needed, and remember to use `github.com/IBM/sarama` as the import path.

## References

- [Apache Kafka official documentation](https://kafka.apache.org/documentation/)

## Sibling pages

- [MessageQueue](/middleware/MessageQueue.md)
- [Readme](/middleware/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [MessageQueue](/middleware/MessageQueue.md)
- [Readme](/middleware/Readme.md)
