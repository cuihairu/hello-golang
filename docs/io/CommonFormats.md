### Common file formats

A file format is how file data is organized and represented, and which format you pick depends on where the data is going. This page notes how to handle text files, binary files, XML, JSON, CSV, and TSV separately.

#### 8.1 Text files

A text file stores data in plain-text form, commonly used for configuration files, log files, and simple data files.

**Go example code** (read and write a text file):

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

#### 8.2 Binary files

A binary file stores data in binary form, commonly used for structured data and files that need efficient reads.

**Go example code** (read and write a binary file):

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

#### 8.3 XML and JSON files

XML and JSON are common file formats for data exchange and configuration.

**Go example code** (handle a JSON file):

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

**Go example code** (handle an XML file):

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

#### 8.4 CSV and TSV files

CSV (Comma-Separated Values) and TSV (Tab-Separated Values) files are common formats for storing tabular data.

**Go example code** (handle a CSV file):

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

Text files use `bufio`, binary uses `encoding/binary`, and JSON, XML, and CSV each have a corresponding `encoding/` package, with reading and writing always paired as an Encoder/Decoder.

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)

## Sibling pages

- [Advanced](/io/Advanced.md)
- [EfficientIO](/io/EfficientIO.md)
- [Example](/io/Example.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/io/Advanced.md)
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
