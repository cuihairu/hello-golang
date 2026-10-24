### Input and Output Streams

IO streams are the channels through which data moves between a program and external devices (files, the network); file reads/writes and network communication all go through them. By data type and processing style they come in three contrasting pairs: character streams vs byte streams, buffered vs unbuffered streams, and data streams vs object streams.

#### 5.1 Basic Concepts of IO Streams

An IO stream is a channel through which data moves between a program and external devices (such as files or the network). By data type and processing style, IO streams divide into character streams and byte streams.

##### 5.1.1 Character Streams and Byte Streams
**Character streams**: process text data, suited to handling characters and strings.
**Byte streams**: process binary data, suited to handling images, audio, video, and the like.

##### 5.1.2 Buffered and Unbuffered Streams
**Buffered streams**: use a buffer to cut the number of direct reads/writes and improve performance.
**Unbuffered streams**: read and write directly, suited to scenarios with strict real-time requirements.

##### 5.1.3 Data Streams and Object Streams
**Data streams**: work with primitive data types.
**Object streams**: handle object serialization and deserialization.

#### 5.2 Character Streams and Byte Streams

Character streams and byte streams are the most fundamental IO streams, suited respectively to text and binary data.

##### 5.2.1 Character Streams

**Go example code**:
```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

func readFileByLine(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        fmt.Println("Error reading file:", err)
    }
}

func writeFileByLine(filePath, content string) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    writer := bufio.NewWriter(file)
    _, err = writer.WriteString(content)
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }

    writer.Flush()
}

func main() {
    writeFileByLine("example.txt", "Hello, World!\nThis is a test.")
    readFileByLine("example.txt")
}
```

##### 5.2.2 Byte Streams

**Go example code**:
```go
package main

import (
    "fmt"
    "io"
    "os"
)

func readBinaryFile(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    buffer := make([]byte, 1024)
    for {
        bytesRead, err := file.Read(buffer)
        if err != nil && err != io.EOF {
            fmt.Println("Error reading file:", err)
            return
        }
        if bytesRead == 0 {
            break
        }
        fmt.Printf("Read %d bytes: %v\n", bytesRead, buffer[:bytesRead])
    }
}

func writeBinaryFile(filePath string, data []byte) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    _, err = file.Write(data)
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }
}

func main() {
    data := []byte{0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x2C, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x21}
    writeBinaryFile("example.bin", data)
    readBinaryFile("example.bin")
}
```

#### 5.3 Buffered and Unbuffered Streams

Buffered streams use a buffer to reduce the number of reads and writes, improving IO performance.

##### 5.3.1 Buffered Streams

**Go example code**:
```go
package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
)

func bufferedWrite(filePath string, content string) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    writer := bufio.NewWriter(file)
    _, err = writer.WriteString(content)
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }
    writer.Flush()
}

func bufferedRead(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    reader := bufio.NewReader(file)
    for {
        line, err := reader.ReadString('\n')
        if err != nil {
            if err != io.EOF {
                fmt.Println("Error reading file:", err)
            }
            break
        }
        fmt.Print(line)
    }
}

func main() {
    bufferedWrite("example.txt", "Hello, buffered world!\nThis is a test.")
    bufferedRead("example.txt")
}
```

##### 5.3.2 Unbuffered Streams

**Go example code**:
```go
package main

import (
    "fmt"
    "io"
    "os"
)

func nonBufferedWrite(filePath string, content string) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    _, err = file.Write([]byte(content))
    if err != nil {
        fmt.Println("Error writing to file:", err)
        return
    }
}

func nonBufferedRead(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    buffer := make([]byte, 1024)
    for {
        bytesRead, err := file.Read(buffer)
        if err != nil && err != io.EOF {
            fmt.Println("Error reading file:", err)
            return
        }
        if bytesRead == 0 {
            break
        }
        fmt.Print(string(buffer[:bytesRead]))
    }
}

func main() {
    nonBufferedWrite("example.txt", "Hello, non-buffered world!\nThis is a test.")
    nonBufferedRead("example.txt")
}
```

#### 5.4 Data Streams and Object Streams

Data streams work with primitive data types, while object streams handle object serialization and deserialization.

##### 5.4.1 Data Streams

**Go example code**:
```go
package main

import (
    "encoding/binary"
    "fmt"
    "io"
    "os"
)

func writeData(filePath string, data []int32) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    for _, value := range data {
        err := binary.Write(file, binary.LittleEndian, value)
        if err != nil {
            fmt.Println("Error writing data:", err)
            return
        }
    }
}

func readData(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    var value int32
    for {
        err := binary.Read(file, binary.LittleEndian, &value)
        if err != nil {
            if err != io.EOF {
                fmt.Println("Error reading data:", err)
            }
            break
        }
        fmt.Println("Read value:", value)
    }
}

func main() {
    data := []int32{1, 2, 3, 4, 5}
    writeData("data.bin", data)
    readData("data.bin")
}
```

##### 5.4.2 Object Streams

Go has no direct object-stream support, but we can implement object serialization and deserialization through encoding and decoding.

**Go example code**:
```go
package main

import (
    "encoding/gob"
    "fmt"
    "os"
)

type Person struct {
    Name string
    Age  int
}

func writeObject(filePath string, obj interface{}) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    encoder := gob.NewEncoder(file)
    err = encoder.Encode(obj)
    if err != nil {
        fmt.Println("Error encoding object:", err)
    }
}

func readObject(filePath string, obj interface{}) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return


    }
    defer file.Close()

    decoder := gob.NewDecoder(file)
    err = decoder.Decode(obj)
    if err != nil {
        fmt.Println("Error decoding object:", err)
    }
}

func main() {
    person := Person{Name: "Alice", Age: 30}
    writeObject("person.gob", person)

    var readPerson Person
    readObject("person.gob", &readPerson)
    fmt.Printf("Read object: %+v\n", readPerson)
}
```

Which one to pick depends on the shape of the data: for text read line by line with `bufio.Scanner`, for binary read in chunks with `file.Read`; if read/write calls are too frequent, wrap things in a layer of `bufio`; for fixed-size numeric values use `binary.Read` / `binary.Write`, and for storing Go structs as-is use `gob`.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)


## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [IO](/io/IO.md)
- [ModIO](/io/ModIO.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [IO](/io/IO.md)
- [ModIO](/io/ModIO.md)
