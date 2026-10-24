### CSV (Comma-Separated Values)

CSV (Comma-Separated Values) is a simple text file format for storing tabular data. CSV files represent data as plain text, where each line is one record and the fields within a record are separated by commas. Because it is simple and easy to read, CSV is widely used for data exchange, storage, and analysis.

#### 1. CSV file format

The basic format of a CSV file is as follows:

1. **One record per line, fields separated by commas (`,`)**:
     ```
     name,age,city
     John,30,New York
     Jane,25,Los Angeles
     ```

2. The first line is usually the field names (header row), but this is not mandatory. For example:
     ```
     name,age,city
     John,30,New York
     Jane,25,Los Angeles
     ```

3. When a field's content contains a comma, newline, or quote, the whole field is wrapped in double quotes. For example:
     ```
     name,age,city
     "John, Doe",30,"New York"
     ```

4. When a field itself contains a quote, add another quote to escape it. For example:
     ```
     name,age,city
     "John ""Johnny"" Doe",30,"New York"
     ```

5. Each line ends with a newline character (`\n`); different operating systems may use `\r\n` or `\n`.

#### 2. Pros and cons of CSV files

**Pros**:

- Simple format, and most programming languages and tools have ready-made support.
- Spreadsheet software such as Excel and Google Sheets can open it directly, and plain text is easy to transmit and edit.

**Cons**:

- No unified standard; different implementations handle quotes and newlines inconsistently, which easily causes compatibility issues.
- All content is strings, so type information has to be agreed on by the upper layer, and nested structures cannot be expressed.
- When a field contains commas, quotes, or newlines, parsing needs extra quote handling.

#### 3. Applications of CSV

1. **Data exchange**: Exporting data between systems, or importing/exporting for databases and spreadsheets.
2. **Logging**: Writing structured data as text logs so it can be processed later with text tools.
3. **Data analysis**: Often used as a data source for analysis tools.

#### 4. CSV processing example (Go)

In Go, use the `encoding/csv` package to read and write CSV files. Here are examples of CSV file processing:

**Reading a CSV file**:

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)

func main() {
    // open the CSV file
    file, err := os.Open("data.csv")
    if err != nil {
        fmt.Println("打开文件失败:", err)
        return
    }
    defer file.Close()

    // create a CSV reader
    reader := csv.NewReader(file)
    
    // read all records
    records, err := reader.ReadAll()
    if err != nil {
        fmt.Println("读取文件失败:", err)
        return
    }

    // print the records
    for _, record := range records {
        fmt.Println(record)
    }
}
```

**Writing a CSV file**:

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)

func main() {
    // create or open the CSV file
    file, err := os.Create("output.csv")
    if err != nil {
        fmt.Println("创建文件失败:", err)
        return
    }
    defer file.Close()

    // create a CSV writer
    writer := csv.NewWriter(file)
    
    // write the records
    records := [][]string{
        {"name", "age", "city"},
        {"John", "30", "New York"},
        {"Jane", "25", "Los Angeles"},
    }
    
    err = writer.WriteAll(records)
    if err != nil {
        fmt.Println("写入文件失败:", err)
        return
    }

    fmt.Println("CSV 文件写入成功")
}
```

#### 5. Common issues in CSV file handling

1. **Special characters in field content**:

   - When handling commas, quotes, and newlines inside field content, you need to correctly wrap them in quotes and escape them.

2. **Data type conversion**:

   - All data in a CSV file is stored as strings, so you may need to convert to the appropriate data type (such as integer or float) when processing.

3. **Handling large CSV files**:

   - For very large CSV files, use streaming reads to avoid loading the entire file into memory at once.

#### Summary

Go handles CSV with the `encoding/csv` package: reading goes through `Reader`'s `ReadAll`, writing through `Writer`'s `WriteAll`; switch to streaming reads for large files so the whole file does not end up in memory.

## References

- [encoding series standard library (json as an example)](https://pkg.go.dev/encoding/json)
- [encoding/csv standard library](https://pkg.go.dev/encoding/csv)

## Sibling pages

- [JsonV2](/encoding/JsonV2.md)
- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Base64](/encoding/Base64.md)
- [Binary](/encoding/Binary.md)
- [Encoding](/encoding/Encoding.md)
