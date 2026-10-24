### Advanced topics

Four directions are covered here: file system programming, distributed file systems, big data file processing, and real-time data stream processing, each with a runnable Go snippet.

#### 10.1 File system programming

File system programming involves operating and managing the file system itself — creating and deleting files, setting permissions, and so on.

**Go example code** (get file info and set permissions):

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

#### 10.2 Distributed file systems

A distributed file system (DFS) shares files and stores data across multiple machines.

**Go example code** (using the Apache Hadoop Distributed File System, HDFS — install the client library first):

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

#### 10.3 Big data file processing

Big data file processing reads and writes large datasets; the common approaches are distributed computing and batch processing. Go has no official Apache Spark client, so when handling a single large file you typically stream it, processing it in chunks rather than loading the whole file into memory.

**Go example code** (stream word frequency in a large file):

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
    scanner.Buffer(make([]byte, 1024*1024), 1024*1024) // supports very long lines
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

#### 10.4 Real-time data stream processing

Real-time data stream processing handles continuously arriving data streams, commonly used in monitoring systems, real-time analysis, and online computing.

**Go example code** (using Apache Kafka for real-time data stream processing — install the client library first; the library is based on CGO and requires librdkafka installed on the machine):

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

The four snippets map to the four directions: `os` handles local file info and permissions, the `hdfs` client reads and writes distributed storage, `bufio.Scanner` streams word counts over a large file, and `confluent-kafka-go` sends and receives message streams.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)
- [bufio standard library](https://pkg.go.dev/bufio)

## Sibling pages

- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [Example](/io/Example.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [Example](/io/Example.md)
- [File](/io/File.md)
- [FileAdvanced](/io/FileAdvanced.md)
- [FileOperation](/io/FileOperation.md)
- [IO](/io/IO.md)
- [InputOutput](/io/InputOutput.md)
- [ModIO](/io/ModIO.md)
- [ModOS](/io/ModOS.md)
- [ModPath](/io/ModPath.md)
- [Security](/io/Security.md)
- [Utils](/io/Utils.md)
