### Redis Streams

Redis Streams is a data structure introduced in Redis 5.0 that combines a message queue with an append-only log: messages are ordered by ID, can be persisted, and can be distributed through consumer groups. It fits real-time data processing.

#### Scenario examples

1. **Real-time log collection**
   - Example: push application logs into a Redis stream in real time, then analyse and monitor them.
     ```bash
     XADD logs * level "info" message "Application started"
     XADD logs * level "error" message "Something went wrong"
     ```
   - Note: `XADD` adds log entries to the `logs` stream.

2. **Message queue**
   - Example: use a Redis stream as a message queue. Producers push messages into the stream, and consumers read them for processing.
     ```bash
     XADD message_queue * sender "user1" content "Hello, World!"
     ```
   - Note: `XADD` adds the message to the `message_queue` stream; consumers can read messages with `XREAD` or `XREADGROUP`.

3. **Task scheduling**
   - Example: add scheduled tasks to a Redis stream, and have worker processes read and execute them.
     ```bash
     XADD tasks * task_id "1" action "process_data" timestamp "2024-07-29T10:00:00Z"
     ```
   - Note: `XADD` adds the task entry to the `tasks` stream; workers can poll the stream for tasks on a regular interval.

4. **Real-time data processing**
   - Example: process a stream of sensor data in real time, then analyse and store it.
     ```bash
     XADD sensor_data * sensor_id "123" temperature "22.5" humidity "55"
     ```
   - Note: `XADD` adds the sensor data to the `sensor_data` stream; downstream analysis tools can process it in real time.

#### Underlying implementation

The underlying implementation of Redis Streams is a mix of a linked-list structure and a hash structure, to make writes and reads efficient. The main characteristics are:

1. **Data structure**
   - **Message entries**: each entry has a unique ID and a hash containing multiple fields. The ID is generated from a timestamp and a sequence number, which guarantees uniqueness and ordering.
   - **Internal storage**: Redis stores message entries in a linked-list structure, and each entry is represented by a hash data structure. The linked list preserves message order, while the hash provides efficient data storage.

2. **Main commands**
   - **XADD**: add a new message to the stream.
     ```bash
     XADD key ID field value [field value ...]
     ```
   - **XRANGE**: read messages from the stream.
     ```bash
     XRANGE key start end [COUNT count]
     ```
   - **XREVRANGE**: read messages from the stream in reverse order.
     ```bash
     XREVRANGE key end start [COUNT count]
     ```
   - **XREAD**: read messages from a stream; a blocking mode can be set.
     ```bash
     XREAD [BLOCK timeout] [COUNT count] STREAMS key [key ...] ID [ID ...]
     ```
   - **XREADGROUP**: read messages from a stream using a consumer group.
     ```bash
     XREADGROUP GROUP group consumer [BLOCK timeout] [COUNT count] STREAMS key [key ...] ID [ID ...]
     ```
   - **XGROUP**: create and manage consumer groups.
     ```bash
     XGROUP CREATE key group name ID [MKSTREAM]
     XGROUP DELCONSUMER key group name consumer
     XGROUP SETID key group name ID
     ```

3. **Message IDs**
   - A message ID is made up of a timestamp and a sequence number, for example `"1627574400000-0"`, where `"1627574400000"` is the timestamp (in milliseconds) and `"-0"` is the sequence number. This structure guarantees that messages are unique and ordered.

4. **Consumer groups**
   - Consumer groups let multiple consumers pull messages from the same stream. Once a message is assigned to one consumer, the others will not receive the same message again, so several machines can process the same stream in parallel.

#### Using Redis Streams in Go

In Go, you can use the `go-redis` library to work with Redis streams. Here are some basic operations.

1. **Connect to Redis**
   ```go
   package main

   import (
       "context"
       "fmt"

       "github.com/go-redis/redis/v8"
   )

   var ctx = context.Background()

   func main() {
       rdb := redis.NewClient(&redis.Options{
           Addr:     "localhost:6379",
           Password: "", // no password set
           DB:       0,  // use default DB
       })

       // call the example code
       example(rdb)
   }

   func example(rdb *redis.Client) {
       // example operations
   }
   ```

2. **Add a message to the stream**
   ```go
   func example(rdb *redis.Client) {
       _, err := rdb.XAdd(ctx, &redis.XAddArgs{
           Stream: "messages",
           Values: map[string]interface{}{
               "sender":  "user1",
               "content": "Hello, World!",
           },
       }).Result()
       if err != nil {
           panic(err)
       }
   }
   ```

3. **Read messages from the stream**
   ```go
   func example(rdb *redis.Client) {
       messages, err := rdb.XRange(ctx, "messages", "-", "+").Result()
       if err != nil {
           panic(err)
       }
       for _, message := range messages {
           fmt.Println("Message ID:", message.ID)
           fmt.Println("Fields:", message.Values)
       }
   }
   ```

4. **Read messages using a consumer group**
   ```go
   func example(rdb *redis.Client) {
       // "0" consumes existing messages from the start of the stream; "$" consumes only messages written after the group was created
       _, err := rdb.XGroupCreateMkStream(ctx, "messages", "group1", "0").Result()
       if err != nil {
           panic(err)
       }
       
       messages, err := rdb.XReadGroup(ctx, &redis.XReadGroupArgs{
           Group:    "group1",
           Consumer: "consumer1",
           Block:    0,
           Count:    10,
           Streams:  []string{"messages", ">"}, // ">" indicates read new messages only
       }).Result()
       if err != nil {
           panic(err)
       }
       for _, stream := range messages {
           for _, message := range stream.Messages {
               fmt.Println("Message ID:", message.ID)
               fmt.Println("Fields:", message.Values)
           }
       }
   }
   ```

`go-redis` wraps all of the commands above as `XAdd`, `XRange` and `XReadGroup` methods, so a producer sending messages and a consumer group receiving them each takes just a few lines of code.

## References

- [Redis Official Command Manual](https://redis.io/commands/)
- [go-redis Official Client](https://github.com/redis/go-redis)
- [go-redis · pkg.go.dev](https://pkg.go.dev/github.com/redis/go-redis/v9)
- [Redis Official Documentation · Streams (external link)](https://redis.io/docs/latest/develop/data-types/streams/)


## Sibling pages

- [Bitmap](/redis/Bitmap.md)
- [Geospatial](/redis/Geospatial.md)
- [Hash](/redis/Hash.md)
- [SortedSet](/redis/SortedSet.md)
- [String](/redis/String.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [SortedSet](/redis/SortedSet.md)
- [String](/redis/String.md)
