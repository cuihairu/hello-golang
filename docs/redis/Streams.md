### Redis 流（Streams）

Redis 流（Streams）是 Redis 5.0 引入的数据结构，把消息队列和追加日志（append-only log）两种特性合在一起：消息按 ID 排序、可持久化，还能按消费者组分发，适合实时数据处理。

#### 场景示例

1. **实时日志收集**
   - 示例：将应用程序日志实时推送到 Redis 流中，然后进行分析和监控。
     ```bash
     XADD logs * level "info" message "Application started"
     XADD logs * level "error" message "Something went wrong"
     ```
   - 说明：`XADD` 将日志条目添加到 `logs` 流中。

2. **消息队列**
   - 示例：使用 Redis 流作为消息队列，生产者将消息推送到流中，消费者从流中读取消息进行处理。
     ```bash
     XADD message_queue * sender "user1" content "Hello, World!"
     ```
   - 说明：`XADD` 将消息添加到 `message_queue` 流中，消费者可以使用 `XREAD` 或 `XREADGROUP` 命令来读取消息。

3. **任务调度**
   - 示例：将定时任务加入 Redis 流，工作进程从流中读取任务并执行。
     ```bash
     XADD tasks * task_id "1" action "process_data" timestamp "2024-07-29T10:00:00Z"
     ```
   - 说明：`XADD` 将任务条目添加到 `tasks` 流中，工作进程可以定期检查流中的任务。

4. **实时数据处理**
   - 示例：实时处理传感器数据流，进行分析和存储。
     ```bash
     XADD sensor_data * sensor_id "123" temperature "22.5" humidity "55"
     ```
   - 说明：`XADD` 将传感器数据添加到 `sensor_data` 流中，后续的分析工具可以实时处理这些数据。

#### 底层实现

Redis 流（Streams）的底层实现是基于一个链表结构和散列结构的混合体，以实现高效的写入和读取操作。主要特性包括：

1. **数据结构**
   - **消息条目**：每个消息条目包含一个唯一的 ID 和一个包含多个字段的散列。ID 是基于时间戳和序列号生成的，确保了条目的唯一性和顺序性。
   - **内部存储**：Redis 流使用链表结构来存储消息条目，每个条目由一个散列数据结构表示。链表确保了消息的顺序，而散列提供了高效的数据存储。

2. **主要命令**
   - **XADD**：向流中添加新消息。
     ```bash
     XADD key ID field value [field value ...]
     ```
   - **XRANGE**：读取流中的消息。
     ```bash
     XRANGE key start end [COUNT count]
     ```
   - **XREVRANGE**：反向读取流中的消息。
     ```bash
     XREVRANGE key end start [COUNT count]
     ```
   - **XREAD**：从流中读取消息，可以设置阻塞模式。
     ```bash
     XREAD [BLOCK timeout] [COUNT count] STREAMS key [key ...] ID [ID ...]
     ```
   - **XREADGROUP**：使用消费者组从流中读取消息。
     ```bash
     XREADGROUP GROUP group consumer [BLOCK timeout] [COUNT count] STREAMS key [key ...] ID [ID ...]
     ```
   - **XGROUP**：创建和管理消费者组。
     ```bash
     XGROUP CREATE key group name ID [MKSTREAM]
     XGROUP DELCONSUMER key group name consumer
     XGROUP SETID key group name ID
     ```

3. **消息 ID**
   - 消息 ID 是由时间戳和序列号组成的，例如 `"1627574400000-0"`，其中 `"1627574400000"` 是时间戳（毫秒级别），`"-0"` 是序列号。这种结构确保了消息的唯一性和顺序。

4. **消费者组**
   - 消费者组让多个消费者从同一个流里取消息，消息分配给其中一个消费者后别的消费者不会重复拿到，多台机器可以并行处理同一个流。

#### Go 中使用 Redis 流

在 Go 语言中，可以使用 `go-redis` 库来操作 Redis 流。以下是一些基本操作示例。

1. **连接 Redis**
   ```go
   package main

   import (
       "context"

       "github.com/go-redis/redis/v8"
   )

   var ctx = context.Background()

   func main() {
       rdb := redis.NewClient(&redis.Options{
           Addr:     "localhost:6379",
           Password: "", // no password set
           DB:       0,  // use default DB
       })

       // 示例代码调用
       example(rdb)
   }

   func example(rdb *redis.Client) {
       // 示例操作
   }
   ```

2. **添加消息到流**
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

3. **读取流中的消息**
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

4. **使用消费者组读取消息**
   ```go
   func example(rdb *redis.Client) {
       // "0" 表示从流的开头开始消费已有消息；若使用 "$" 则只消费创建组之后新写入的消息
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

`go-redis` 把上面几个命令都封成了 `XAdd`、`XRange`、`XReadGroup` 方法，生产者发消息、消费者组收消息各几行代码就能跑通。