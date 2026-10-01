### 实战案例

通过实际案例，读者可以将所学的文件与 IO 知识应用到实际项目中。本章将介绍几个常见的实战案例，包括日志文件管理、配置文件处理、数据导入导出以及大文件处理等。

#### 9.1 日志文件管理

日志文件是记录系统运行状态和错误信息的重要文件。日志管理包括日志的创建、写入、滚动等操作。

**Go 示例代码**（日志文件写入和滚动）：

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

#### 9.2 配置文件处理

配置文件用于存储应用程序的配置参数，常见的格式有 JSON、YAML 和 TOML。本例介绍如何读取和写入 JSON 格式的配置文件。

**Go 示例代码**（读取和写入 JSON 配置文件）：

```go
package main

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
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

    err = ioutil.WriteFile(filePath, data, 0644)
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

#### 9.3 数据导入导出

数据导入导出是将数据从一个系统迁移到另一个系统的常见操作。本例介绍如何导入和导出 CSV 格式的数据。

**Go 示例代码**（导入和导出 CSV 文件）：

```go
package main

import (
    "encoding/csv"
    "fmt"
    "os"
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

#### 9.4 大文件处理

大文件处理需要特别注意内存和性能问题，常见的方法包括分块读取和多线程处理。

**Go 示例代码**（分块读取大文件）：

```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

const chunkSize = 1024 * 1024 // 1 MB

func processChunk(chunk []byte) {
    // 处理分块数据
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

通过学习本章内容，读者将能够掌握日志文件管理、配置文件处理、数据导入导出以及大文件处理等实战案例，从而在实际项目中灵活应用这些技术。