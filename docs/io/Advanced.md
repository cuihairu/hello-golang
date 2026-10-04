### 进阶主题

这一章讲四件事：文件系统编程、分布式文件系统、大数据文件处理和实时数据流处理，每节配一段可运行的 Go 代码。

#### 10.1 文件系统编程

文件系统编程涉及对文件系统本身的操作和管理，如文件创建、删除、权限设置等。

**Go 示例代码**（获取文件信息并设置权限）：

```go
package main

import (
    "fmt"
    "os"
)

func getFileInfo(filePath string) {
    fileInfo, err := os.Stat(filePath)
    if err != nil {
        fmt.Println("Error getting file info:", err)
        return
    }

    fmt.Printf("File Name: %s\n", fileInfo.Name())
    fmt.Printf("Size: %d bytes\n", fileInfo.Size())
    fmt.Printf("Permissions: %s\n", fileInfo.Mode().String())
    fmt.Printf("Last Modified: %s\n", fileInfo.ModTime().String())
}

func setFilePermissions(filePath string, mode os.FileMode) {
    err := os.Chmod(filePath, mode)
    if err != nil {
        fmt.Println("Error setting file permissions:", err)
    }
}

func main() {
    filePath := "example.txt"
    getFileInfo(filePath)
    setFilePermissions(filePath, 0644)
    getFileInfo(filePath)
}
```

#### 10.2 分布式文件系统

分布式文件系统（DFS）用于在多台机器上共享文件和存储数据。

**Go 示例代码**（使用 Apache Hadoop 分布式文件系统 HDFS，先安装客户端库）：

```bash
go get github.com/colinmarc/hdfs/v2
```

```go
package main

import (
    "fmt"
    "github.com/colinmarc/hdfs/v2"
)

func main() {
    client, err := hdfs.New("namenode:9000")
    if err != nil {
        fmt.Println("Error connecting to HDFS:", err)
        return
    }

    filePath := "/user/hadoop/example.txt"
    writer, err := client.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file on HDFS:", err)
        return
    }
    if _, err := writer.Write([]byte("Hello, HDFS!\n")); err != nil {
        fmt.Println("Error writing to HDFS:", err)
        return
    }
    if err := writer.Close(); err != nil {
        fmt.Println("Error closing file on HDFS:", err)
        return
    }

    data, err := client.ReadFile(filePath)
    if err != nil {
        fmt.Println("Error reading from HDFS:", err)
        return
    }

    fmt.Printf("Data read from HDFS: %s\n", string(data))
}
```

#### 10.3 大数据文件处理

大数据文件处理要读写大规模数据集，常见方法是分布式计算和批处理。Go 没有官方的 Apache Spark 客户端，处理单个大文件时通常使用流式读取，逐块处理而不把整个文件加载进内存。

**Go 示例代码**（流式统计大文件的词频）：

```go
package main

import (
    "bufio"
    "fmt"
    "os"
    "sort"
    "strings"
)

func main() {
    filePath := "data.txt"
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    counts := make(map[string]int)
    scanner := bufio.NewScanner(file)
    scanner.Buffer(make([]byte, 1024*1024), 1024*1024) // 支持超长行
    for scanner.Scan() {
        for _, word := range strings.Fields(scanner.Text()) {
            counts[strings.ToLower(word)]++
        }
    }
    if err := scanner.Err(); err != nil {
        fmt.Println("Error scanning file:", err)
        return
    }

    words := make([]string, 0, len(counts))
    for word := range counts {
        words = append(words, word)
    }
    sort.Slice(words, func(i, j int) bool { return counts[words[i]] > counts[words[j]] })

    for i, word := range words {
        if i >= 10 {
            break
        }
        fmt.Printf("%s: %d\n", word, counts[word])
    }
}
```

#### 10.4 实时数据流处理

实时数据流处理用于处理连续不断的数据流，常用于监控系统、实时分析和在线计算。

**Go 示例代码**（使用 Apache Kafka 进行实时数据流处理，先安装客户端库；该库基于 CGO，需要本机安装 librdkafka）：

```bash
go get github.com/confluentinc/confluent-kafka-go/kafka
```

```go
package main

import (
    "fmt"
    "log"
    "github.com/confluentinc/confluent-kafka-go/kafka"
)

func main() {
    producer, err := kafka.NewProducer(&kafka.ConfigMap{"bootstrap.servers": "localhost:9092"})
    if err != nil {
        log.Fatalf("Failed to create producer: %s", err)
    }

    topic := "example-topic"
    for _, word := range []string{"Hello", "world", "Kafka", "stream"} {
        producer.Produce(&kafka.Message{
            TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
            Value:          []byte(word),
        }, nil)
    }
    producer.Flush(15 * 1000)

    consumer, err := kafka.NewConsumer(&kafka.ConfigMap{
        "bootstrap.servers": "localhost:9092",
        "group.id":          "example-group",
        "auto.offset.reset": "earliest",
    })
    if err != nil {
        log.Fatalf("Failed to create consumer: %s", err)
    }

    consumer.SubscribeTopics([]string{topic}, nil)
    for {
        msg, err := consumer.ReadMessage(-1)
        if err == nil {
            fmt.Printf("Received message: %s\n", string(msg.Value))
        } else {
            fmt.Printf("Consumer error: %v (%v)\n", err, msg)
        }
    }
}
```

四段代码对应四个方向：`os` 管本地文件信息和权限，`hdfs` 客户端读写分布式存储，`bufio.Scanner` 流式统计大文件，`confluent-kafka-go` 收发消息流。