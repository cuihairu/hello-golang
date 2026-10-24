### Practice Notes

This page records four common file and IO practices: writing log files and rotating them by size, reading and writing JSON config files, CSV import and export, and reading large files in chunks.

#### 9.1 Log File Management

Log files record system state and error messages. This example implements log writing and rotation: once the file exceeds 1 MB, it is renamed as a backup and a new file is created to keep writing.

**Go example code** (log file writing and rotation):

```go
package main

import (
    "fmt"
    "os"
    "time"
)

const (
    logFilePath  = "application.log"
    maxFileSize  = 1 * 1024 * 1024 // 1 MB
    backupSuffix = ".bak"
)

func checkFileSize(filePath string) bool {
    fileInfo, err := os.Stat(filePath)
    if err != nil {
        return false
    }
    return fileInfo.Size() >= maxFileSize
}

func rotateLogFile(filePath string) error {
    backupPath := filePath + backupSuffix
    err := os.Rename(filePath, backupPath)
    if err != nil {
        return fmt.Errorf("error rotating log file: %v", err)
    }
    return nil
}

func logMessage(filePath, message string) error {
    if checkFileSize(filePath) {
        if err := rotateLogFile(filePath); err != nil {
            return err
        }
    }

    file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        return fmt.Errorf("error opening log file: %v", err)
    }
    defer file.Close()

    timestamp := time.Now().Format("2006-01-02 15:04:05")
    _, err = fmt.Fprintf(file, "[%s] %s\n", timestamp, message)
    if err != nil {
        return fmt.Errorf("error writing to log file: %v", err)
    }

    return nil
}

func main() {
    messages := []string{
        "Application started",
        "Processing request",
        "Request processed successfully",
        "Application stopped",
    }

    for _, msg := range messages {
        if err := logMessage(logFilePath, msg); err != nil {
            fmt.Println("Error logging message:", err)
        }
    }
}
```

#### 9.2 Config File Handling

Config files store an application's configuration parameters; common formats include JSON, YAML, and TOML. This example shows how to read and write a JSON config file.

**Go example code** (read and write a JSON config file):

```go
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

type Config struct {
    ServerPort int    `json:"server_port"`
    Database   string `json:"database"`
    Username   string `json:"username"`
    Password   string `json:"password"`
}

func loadConfig(filePath string) (*Config, error) {
    file, err := os.Open(filePath)
    if err != nil {
        return nil, fmt.Errorf("error opening config file: %v", err)
    }
    defer file.Close()

    var config Config
    decoder := json.NewDecoder(file)
    if err := decoder.Decode(&config); err != nil {
        return nil, fmt.Errorf("error decoding config file: %v", err)
    }

    return &config, nil
}

func saveConfig(filePath string, config *Config) error {
    data, err := json.MarshalIndent(config, "", "  ")
    if err != nil {
        return fmt.Errorf("error marshalling config: %v", err)
    }

    err = os.WriteFile(filePath, data, 0644)
    if err != nil {
        return fmt.Errorf("error writing config file: %v", err)
    }

    return nil
}

func main() {
    configFilePath := "config.json"

    // Sample configuration
    config := &Config{
        ServerPort: 8080,
        Database:   "mydatabase",
        Username:   "admin",
        Password:   "password",
    }

    // Save configuration
    if err := saveConfig(configFilePath, config); err != nil {
        fmt.Println("Error saving config:", err)
    }

    // Load configuration
    loadedConfig, err := loadConfig(configFilePath)
    if err != nil {
        fmt.Println("Error loading config:", err)
    } else {
        fmt.Printf("Loaded config: %+v\n", loadedConfig)
    }
}
```

#### 9.3 Data Import and Export

Data import and export is a common operation for moving data from one system to another. This example shows how to import and export CSV data.

**Go example code** (import and export CSV files):

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
    "strconv"
)

type Record struct {
    Name  string
    Age   int
    Email string
}

func exportCSV(filePath string, records []Record) error {
    file, err := os.Create(filePath)
    if err != nil {
        return fmt.Errorf("error creating file: %v", err)
    }
    defer file.Close()

    writer := csv.NewWriter(file)
    defer writer.Flush()

    for _, record := range records {
        row := []string{record.Name, fmt.Sprintf("%d", record.Age), record.Email}
        if err := writer.Write(row); err != nil {
            return fmt.Errorf("error writing to CSV file: %v", err)
        }
    }

    return nil
}

func importCSV(filePath string) ([]Record, error) {
    file, err := os.Open(filePath)
    if err != nil {
        return nil, fmt.Errorf("error opening file: %v", err)
    }
    defer file.Close()

    reader := csv.NewReader(file)
    rows, err := reader.ReadAll()
    if err != nil {
        return nil, fmt.Errorf("error reading CSV file: %v", err)
    }

    var records []Record
    for _, row := range rows {
        age, _ := strconv.Atoi(row[1])
        record := Record{Name: row[0], Age: age, Email: row[2]}
        records = append(records, record)
    }

    return records, nil
}

func main() {
    filePath := "data.csv"
    records := []Record{
        {"Alice", 30, "alice@example.com"},
        {"Bob", 25, "bob@example.com"},
    }

    // Export records to CSV
    if err := exportCSV(filePath, records); err != nil {
        fmt.Println("Error exporting CSV:", err)
    }

    // Import records from CSV
    importedRecords, err := importCSV(filePath)
    if err != nil {
        fmt.Println("Error importing CSV:", err)
    } else {
        fmt.Printf("Imported records: %+v\n", importedRecords)
    }
}
```

#### 9.4 Large File Handling

Large file handling needs special attention to memory and performance; common approaches include reading in chunks and multi-threaded processing.

**Go example code** (read a large file in chunks):

```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

const chunkSize = 1024 * 1024 // 1 MB

func processChunk(chunk []byte) {
    // process the chunk data
    fmt.Printf("Processing chunk of size %d\n", len(chunk))
}

func readLargeFile(filePath string) {
    file, err := os.Open(filePath)
    if err != nil {
        fmt.Println("Error opening file:", err)
        return
    }
    defer file.Close()

    reader := bufio.NewReader(file)
    buffer := make([]byte, chunkSize)

    for {
        bytesRead, err := reader.Read(buffer)
        if err != nil && err.Error() != "EOF" {
            fmt.Println("Error reading file:", err)
            break
        }
        if bytesRead == 0 {
            break
        }

        processChunk(buffer[:bytesRead])
    }
}

func main() {
    filePath := "largefile.dat"
    readLargeFile(filePath)
}
```

## References

- [io standard library](https://pkg.go.dev/io)
- [os standard library](https://pkg.go.dev/os)

## Sibling pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/io/Advanced.md)
- [CommonFormats](/io/CommonFormats.md)
- [EfficientIO](/io/EfficientIO.md)
- [File](/io/File.md)
