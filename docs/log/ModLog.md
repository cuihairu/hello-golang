### The Go Standard Library `log`

#### 1. Overview

The Go standard library has two logging packages: `log` is the basic one, outputting a line of text with a prefix; `slog` was added later and brings log levels and structured fields. The two are worth looking at side by side.

#### 2. Basic Usage

##### 2.1 Initialization and Basic Configuration

###### `log` package

```go
package main

import (
	"log"
)

func main() {
	log.Println("This is a log message")

	// custom configuration
	log.SetPrefix("INFO: ")
	log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
	log.Println("This is a customized log message")
}
```

###### `slog` package

```go
package main

import (
	"log/slog"
	"os"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	logger.Info("This is a log message")
}
```

##### 2.2 Recording Logs

###### `log` package

```go
package main

import "log"

func main() {
	log.Println("This is a log message")
	log.Printf("This is a formatted log message: %d", 42)

	// log.Fatal / log.Panic call os.Exit(1) / panic() to terminate the program;
	// they are commented out here so the example does not exit mid-run.
	// log.Fatal("This is a fatal log message")
	// log.Panic("This is a panic log message")
}
```

###### `slog` package

```go
package main

import (
	"errors"
	"log/slog"
	"os"
)

func main() {
	err := errors.New("example failure")
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

	logger.Info("This is an info message")
	logger.Warn("This is a warning message")
	logger.Error("This is an error message", slog.Any("error", err))
}
```

##### 2.3 Log Output Format

###### `log` package

```go
log.SetFlags(log.Ldate | log.Ltime | log.Lmicroseconds | log.Llongfile)
log.Println("This is a log message with custom format")
```

###### `slog` package

```go
package main

import (
	"log/slog"
	"os"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	logger.Info("This is a log message in JSON format")
}
```

#### 3. Log Levels

###### The limitations of the `log` package

The `log` package has no built-in log level mechanism, so you can implement levels yourself.

```go
package main

import (
	"log"
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

###### `slog` package

The `slog` package has built-in log levels.

```go
package main

import (
	"log/slog"
	"os"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

	logger.Info("This is an info message")
	logger.Warn("This is a warning message")
	logger.Error("This is an error message")
}
```

#### 4. Output Redirection

###### `log` package

```go
logFile, err := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
if err != nil {
	log.Fatal(err)
}
defer logFile.Close()

log.SetOutput(logFile)
log.Println("This message is written to the log file")
```

###### `slog` package

```go
package main

import (
	"log"
	"log/slog"
	"os"
)

func main() {
	logFile, err := os.OpenFile("app.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
	}
	defer logFile.Close()

	logger := slog.New(slog.NewJSONHandler(logFile, nil))
	logger.Info("This message is written to the log file")
}
```

#### 5. Log Prefixes and Flags

###### `log` package

```go
log.SetPrefix("INFO: ")
log.SetFlags(log.Ldate | log.Ltime | log.Lshortfile)
log.Println("This is a log message with prefix and flags")
```

###### `slog` package

The `slog` package has no notion of a prefix, but you can achieve something similar by adding fields.

```go
package main

import (
	"log/slog"
	"os"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
	logger.Info("This is a log message", slog.String("prefix", "INFO"))
}
```

#### 6. Log Rotation

###### `log` package

Use a third-party library (such as `lumberjack`) to implement log rotation.

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

###### `slog` package

`lumberjack` can be used the same way to implement log rotation.

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
	}, nil))
	logger.Info("This is a log message with log rotation")
}
```

#### 7. Concurrency and Safety

###### `log` package

The `log` package is concurrency-safe, though it may need optimization under high concurrency.

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

###### `slog` package

The `slog` package is also concurrency-safe.

```go
package main

import (
	"log/slog"
	"os"
	"sync"
)

func main() {
	logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

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

#### 8. Practical Examples

##### 8.1 Building a Simple Logging Utility Package

```go
package logutil

import (
	"log"
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

##### 8.2 Integrating Into a Real Project

Assume the `logutil` package above lives in a `logutil` subdirectory of the current module (the module is named `example.com/myapp`); then reference it from the main package like this:

```go
package main

import (
	"example.com/myapp/logutil"
)

func main() {
	logger := logutil.NewLogger("app.log")
	logger.Println("This is a log message from the main package")
}
```

#### 9. Summary and Best Practices

- **Best practices for logging**:
  - Always record enough context to make debugging and analysis easier.
  - Set log levels sensibly to avoid producing too much useless logging.
  - Use log rotation to stop log files from growing unbounded.
  - Under high concurrency, make sure logging stays fast and safe.

- **Avoiding common mistakes**:
  - Do not record sensitive information in logs.
  - Mind the permissions on log files to prevent unauthorized access.

- **Improving logging efficiency and readability**:
  - Use structured logging to make logs easier to parse.
  - Pick a format suited to your needs (such as JSON) to ease log aggregation and analysis.

## References

- [log standard library](https://pkg.go.dev/log)
- [Official blog · Structured Logging with slog](https://go.dev/blog/slog)
- [log/slog standard library](https://pkg.go.dev/log/slog)

## Sibling pages

- [Aggregation](/log/Aggregation.md)
- [LibLog](/log/LibLog.md)
- [Log](/log/Log.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Aggregation](/log/Aggregation.md)
- [LibLog](/log/LibLog.md)
- [Log](/log/Log.md)
