### 输入输出流

在本章中，我们将探讨输入输出流（IO流）的基本概念。IO流是进行数据传输的基础，广泛应用于文件读写、网络通信等场景。我们将介绍字符流与字节流、缓冲流与非缓冲流、数据流与对象流的区别和用法。

#### 5.1 IO 流的基本概念

IO流是数据在程序与外部设备（如文件、网络）之间传输的通道。根据数据类型和处理方式，IO流可以分为字符流和字节流。

##### 5.1.1 字符流与字节流
**字符流**：处理文本数据，适用于处理字符、字符串。
**字节流**：处理二进制数据，适用于处理图片、音频、视频等。

##### 5.1.2 缓冲流与非缓冲流
**缓冲流**：通过缓冲区减少直接读写次数，提高性能。
**非缓冲流**：直接进行读写操作，适用于实时性要求高的场景。

##### 5.1.3 数据流与对象流
**数据流**：处理基本数据类型的数据。
**对象流**：处理对象序列化和反序列化。

#### 5.2 字符流与字节流

字符流和字节流是最基础的IO流，分别适用于处理文本和二进制数据。

##### 5.2.1 字符流

**Go 示例代码**：
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

##### 5.2.2 字节流

**Go 示例代码**：
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

#### 5.3 缓冲流与非缓冲流

缓冲流通过使用缓冲区来减少读写次数，提高IO操作的性能。

##### 5.3.1 缓冲流

**Go 示例代码**：
```go
package main

import (
    "bufio"
    "fmt"
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

##### 5.3.2 非缓冲流

**Go 示例代码**：
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

#### 5.4 数据流与对象流

数据流处理基本数据类型的数据，而对象流处理对象的序列化和反序列化。

##### 5.4.1 数据流

**Go 示例代码**：
```go
package main

import (
    "encoding/binary"
    "fmt"
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

##### 5.4.2 对象流

Go 中没有直接的对象流支持，但我们可以通过编码和解码来实现对象的序列化和反序列化。

**Go 示例代码**：
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

通过学习本章内容，读者将能够掌握IO流的基本概念和应用，理解字符流、字节流、缓冲流、非缓冲流、数据流和对象流的区别和用法，从而在实际开发中灵活应用这些知识。