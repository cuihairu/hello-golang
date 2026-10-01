### Go 标准库 `log`

#### 1. 概述

Go 标准库提供了两个主要的日志包：`log` 和 `slog`。`log` 包提供了基础的日志记录功能，而 `slog` 包是最近引入的，旨在提供更高级和灵活的日志记录能力。本章将详细介绍这两个包的使用方法和最佳实践。

#### 2. 基本使用

##### 2.1 初始化和基本配置

###### `log` 包

```go
package main

import (
	"log"
	"os"
)

func main() {
	log.Println("This is a log message")
	
	// 自定义配置
	log.SetPrefix("INFO: ")
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
	log.Println("This is a customized log message")
}
```

###### `slog` 包

```go
package main

import (
	"log/slog"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout))
	logger.Info("This is a log message")
}
```

##### 2.2 记录日志

###### `log` 包

```go
log.Println("This is a log message")
log.Printf("This is a formatted log message: %d", 42)
log.Fatal("This is a fatal log message") // 会调用 os.Exit(1)
log.Panic("This is a panic log message") // 会调用 panic()
```

###### `slog` 包

```go
logger.Info("This is an info message")
logger.Warn("This is a warning message")
logger.Error("This is an error message", slog.Error(err))
```

##### 2.3 日志输出格式

###### `log` 包

```go
log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds | log.Llongfile)
log.Println("This is a log message with custom format")
```

###### `slog` 包

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout))
logger.Info("This is a log message in JSON format")
```

#### 3. 日志级别

###### `log` 包的局限性

`log` 包没有内置的日志级别机制，可以通过自定义实现日志级别。

```go
package main

import (
	"fmt"
	"log"
	"os"
)

type Level int

const (
	DEBUG Level = iota
	INFO
	WARN
	ERROR
)

var logLevel = INFO

func logMessage(level Level, msg string) {
	if level >= logLevel {
		log.Println(msg)
	}
}

func main() {
	logMessage(INFO, "This is an info message")
	logMessage(DEBUG, "This is a debug message")
}
```

###### `slog` 包

`slog` 包支持内置的日志级别。

```go
logger.Info("This is an info message")
logger.Warn("This is a warning message")
logger.Error("This is an error message")
```

#### 4. 输出重定向

###### `log` 包

```go
logFile, err := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
if err != nil {
	log.Fatal(err)
}
defer logFile.Close()

log.SetOutput(logFile)
log.Println("This message is written to the log file")
```

###### `slog` 包

```go
logFile, err := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
if err != nil {
	log.Fatal(err)
}
defer logFile.Close()

logger := slog.New(slog.NewJSONHandler(logFile))
logger.Info("This message is written to the log file")
```

#### 5. 日志前缀和标志

###### `log` 包

```go
log.SetPrefix("INFO: ")
log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
log.Println("This is a log message with prefix and flags")
```

###### `slog` 包

`slog` 包没有前缀的概念，但可以通过添加字段实现类似功能。

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout))
logger.Info("This is a log message", slog.String("prefix", "INFO"))
```

#### 6. 日志轮转

###### `log` 包

使用第三方库（如 `lumberjack`）来实现日志轮转。

```go
package main

import (
	"log"
	"gopkg.in/natefinch/lumberjack.v2"
)

func main() {
	log.SetOutput(&lumberjack.Logger{
		Filename:   "app.log",
		MaxSize:    10, // megabytes
		MaxBackups: 3,
		MaxAge:     28, //days
	})
	log.Println("This is a log message with log rotation")
}
```

###### `slog` 包

同样可以使用 `lumberjack` 实现日志轮转。

```go
package main

import (
	"gopkg.in/natefinch/lumberjack.v2"
	"log/slog"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(&lumberjack.Logger{
		Filename:   "app.log",
		MaxSize:    10, // megabytes
		MaxBackups: 3,
		MaxAge:     28, //days
	}))
	logger.Info("This is a log message with log rotation")
}
```

#### 7. 并发与安全

###### `log` 包

`log` 包是并发安全的，但在高并发场景下可能需要优化。

```go
package main

import (
	"log"
	"sync"
)

func main() {
	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			log.Printf("Logging from goroutine %d", i)
		}(i)
	}
	wg.Wait()
}
```

###### `slog` 包

`slog` 包也是并发安全的。

```go
package main

import (
	"log/slog"
	"sync"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout))

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			logger.Info("Logging from goroutine", slog.Int("goroutine", i))
		}(i)
	}
	wg.Wait()
}
```

#### 8. 实践案例

##### 8.1 构建一个简单的日志工具包

```go
package logutil

import (
	"log"
	"os"
	"gopkg.in/natefinch/lumberjack.v2"
)

func NewLogger(filename string) *log.Logger {
	logger := log.New(&lumberjack.Logger{
		Filename:   filename,
		MaxSize:    10, // megabytes
		MaxBackups: 3,
		MaxAge:     28, //days
	}, "", log.Ldate|log.Ltime|log.Lshortfile)
	return logger
}
```

##### 8.2 集成到一个实际项目中

```go
package main

import (
	"logutil"
)

func main() {
	logger := logutil.NewLogger("app.log")
	logger.Println("This is a log message from the main package")
}
```

#### 9. 总结与最佳实践

- **日志记录的最佳实践**：
  - 始终记录足够的上下文信息，便于调试和分析。
  - 合理设置日志级别，避免过多无用日志。
  - 使用日志轮转，防止日志文件过大。
  - 在高并发场景下，确保日志记录的性能和安全。

- **避免常见错误**：
  - 不要在日志中记录敏感信息。
  - 注意日志文件的权限设置，防止未授权访问。

- **提高日志记录的效率与可读性**：
  - 使用结构化日志，提高日志的可解析性。
  - 选择合适的日志格式（如 JSON）以便于日志聚合和分析。
