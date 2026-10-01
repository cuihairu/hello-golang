### 常见文件格式处理

文件格式是文件数据组织和表示的方式，不同的文件格式适用于不同的应用场景。本章将介绍常见的文件格式及其处理方法，包括文本文件、二进制文件、XML、JSON、CSV 和 TSV 文件等。

#### 8.1 文本文件格式

文本文件是以纯文本形式存储数据的文件，常用于存储配置文件、日志文件和简单的数据文件。

**Go 示例代码**（读取和写入文本文件）：

```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

func writeTextFile(filePath string, content string) {
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

func readTextFile(filePath string) {
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

func main() {
    filePath := "example.txt"
    content := "Hello, world!\nThis is a text file."
    writeTextFile(filePath, content)
    readTextFile(filePath)
}
```

#### 8.2 二进制文件格式

二进制文件是以二进制形式存储数据的文件，常用于存储结构化数据和需要高效读取的文件。

**Go 示例代码**（读取和写入二进制文件）：

```go
package main

import (
    "encoding/binary"
    "fmt"
    "os"
)

func writeBinaryFile(filePath string, data []int32) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    for _, value := range data {
        err = binary.Write(file, binary.LittleEndian, value)
        if err != nil {
            fmt.Println("Error writing to file:", err)
            return
        }
    }
}

func readBinaryFile(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    var value int32
    for {
        err = binary.Read(file, binary.LittleEndian, &value)
        if err != nil {
            break
        }
        fmt.Println(value)
    }

    if err != nil && err.Error() != "EOF" {
        fmt.Println("Error reading file:", err)
    }
}

func main() {
    filePath := "example.bin"
    data := []int32{1, 2, 3, 4, 5}
    writeBinaryFile(filePath, data)
    readBinaryFile(filePath)
}
```

#### 8.3 XML 与 JSON 文件

XML 和 JSON 是常见的用于数据交换和配置的文件格式。

**Go 示例代码**（处理 JSON 文件）：

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func writeJSONFile(filePath string, person Person) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    encoder := json.NewEncoder(file)
    err = encoder.Encode(person)
    if err != nil {
        fmt.Println("Error encoding JSON to file:", err)
    }
}

func readJSONFile(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    var person Person
    decoder := json.NewDecoder(file)
    err = decoder.Decode(&person)
    if err != nil {
        fmt.Println("Error decoding JSON from file:", err)
        return
    }

    fmt.Printf("Name: %s, Age: %d\n", person.Name, person.Age)
}

func main() {
    filePath := "person.json"
    person := Person{Name: "Alice", Age: 30}
    writeJSONFile(filePath, person)
    readJSONFile(filePath)
}
```

**Go 示例代码**（处理 XML 文件）：

```go
package main

import (
    "encoding/xml"
    "fmt"
    "os"
)

type Person struct {
    XMLName xml.Name `xml:"person"`
    Name    string   `xml:"name"`
    Age     int      `xml:"age"`
}

func writeXMLFile(filePath string, person Person) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    encoder := xml.NewEncoder(file)
    encoder.Indent("", "  ")
    err = encoder.Encode(person)
    if err != nil {
        fmt.Println("Error encoding XML to file:", err)
    }
}

func readXMLFile(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    var person Person
    decoder := xml.NewDecoder(file)
    err = decoder.Decode(&person)
    if err != nil {
        fmt.Println("Error decoding XML from file:", err)
        return
    }

    fmt.Printf("Name: %s, Age: %d\n", person.Name, person.Age)
}

func main() {
    filePath := "person.xml"
    person := Person{Name: "Alice", Age: 30}
    writeXMLFile(filePath, person)
    readXMLFile(filePath)
}
```

#### 8.4 CSV 与 TSV 文件

CSV（Comma-Separated Values）和 TSV（Tab-Separated Values）文件是常用于存储表格数据的文件格式。

**Go 示例代码**（处理 CSV 文件）：

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)

func writeCSVFile(filePath string, records [][]string) {
    file, err := os.Create(filePath)
    if err != nil {
        fmt.Println("Error creating file:", err)
        return
    }
    defer file.Close()

    writer := csv.NewWriter(file)
    err = writer.WriteAll(records)
    if err != nil {
        fmt.Println("Error writing to CSV file:", err)
    }
}

func readCSVFile(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    reader := csv.NewReader(file)
    records, err := reader.ReadAll()
    if err != nil {
        fmt.Println("Error reading from CSV file:", err)
        return
    }

    for _, record := range records {
        fmt.Println(record)
    }
}

func main() {
    filePath := "example.csv"
    records := [][]string{
        {"Name", "Age"},
        {"Alice", "30"},
        {"Bob", "25"},
    }
    writeCSVFile(filePath, records)
    readCSVFile(filePath)
}
```

通过学习本章内容，读者将能够掌握常见文件格式的处理方法，包括文本文件、二进制文件、XML、JSON、CSV 和 TSV 文件的读写操作，从而在实际开发中灵活应用这些知识。