### Third-Party Logging Libraries

Besides the Go standard library's `log` and `slog`, the common third-party logging libraries are `logrus`, `zap` and `zerolog`. All of them support structured fields, log levels and hooks.

#### 1. `logrus`

##### 1.1 Installation and Basic Usage

```sh
go get github.com/sirupsen/logrus
```

```go
package main

import (
	"github.com/sirupsen/logrus"
)

func main() {
	logger := logrus.New()
	logger.Info("This is an info message")
	logger.Warn("This is a warning message")
	logger.Error("This is an error message")
}
```

##### 1.2 Log Levels and Hooks

```go
logger.SetLevel(logrus.WarnLevel)

logger.Info("This will not be logged")
logger.Warn("This will be logged")

logger.AddHook(&CustomHook{})
```

##### 1.3 Custom Formatters and Output

```go
logger.SetFormatter(&logrus.JSONFormatter{})

file, err := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY, 0666)
if err == nil {
	logger.SetOutput(file)
} else {
	logger.Info("Failed to log to file, using default stderr")
}
```

##### 1.4 Practical Example

```go
package main

import (
	"github.com/sirupsen/logrus"
	"os"
)

func main() {
	logger := logrus.New()

	logger.SetFormatter(&logrus.JSONFormatter{})
	file, err := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY, 0666)
	if err == nil {
		logger.SetOutput(file)
	} else {
		logger.Info("Failed to log to file, using default stderr")
	}

	logger.WithFields(logrus.Fields{
		"event": "event",
		"topic": "topic",
		"key":   "value",
	}).Info("This is a structured log message")
}
```

#### 2. `zap`

##### 2.1 Installation and Basic Usage

```sh
go get go.uber.org/zap
```

```go
package main

import (
	"go.uber.org/zap"
)

func main() {
	logger, _ := zap.NewProduction()
	defer logger.Sync()

	logger.Info("This is an info message")
	logger.Warn("This is a warning message")
	logger.Error("This is an error message")
}
```

##### 2.2 Performance Optimization

```go
package main

import "go.uber.org/zap"

func main() {
	logger, _ := zap.NewProduction(zap.WithCaller(false))
	defer logger.Sync()
	logger.Info("This is an info message")
}
```

##### 2.3 Structured Logging

```go
logger.Info("This is a structured log message",
	zap.String("key1", "value1"),
	zap.Int("key2", 123))
```

##### 2.4 Configuration and Example

```go
package main

import "go.uber.org/zap"

func main() {
	config := zap.NewProductionConfig()
	config.OutputPaths = []string{"stdout", "app.log"}
	logger, _ := config.Build()

	logger.Info("This is an info message with custom configuration")
}
```

##### 2.5 Practical Example

```go
package main

import (
	"go.uber.org/zap"
)

func main() {
	logger, _ := zap.NewProduction()
	defer logger.Sync()

	sugar := logger.Sugar()
	sugar.Infow("This is a structured log message",
		"key1", "value1",
		"key2", 123)
}
```

#### 3. `zerolog`

##### 3.1 Installation and Basic Usage

```sh
go get github.com/rs/zerolog/log
```

```go
package main

import (
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"os"
)

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

	log.Info().Msg("This is an info message")
	log.Warn().Msg("This is a warning message")
	log.Error().Msg("This is an error message")
}
```

##### 3.2 Minimal Overhead and Efficient Logging

```go
package main

import "github.com/rs/zerolog/log"

func main() {
	log.Info().Str("key1", "value1").Int("key2", 123).Msg("This is a structured log message")
}
```

##### 3.3 Logging in JSON Format

```go
package main

import (
	"os"

	"github.com/rs/zerolog/log"
)

func main() {
	log.Logger = log.Output(os.Stdout)
	log.Info().Msg("This is a log message in JSON format")
}
```

##### 3.4 Practical Example

```go
package main

import (
	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"
	"os"
)

func main() {
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr})

	log.Info().Str("key1", "value1").Int("key2", 123).Msg("This is a structured log message")
}
```

#### 4. Comparison and Choosing

##### 4.1 Comparing the Logging Libraries

- **`logrus`**: full-featured, supports hooks, custom formatters and output, but performance is comparatively low.
- **`zap`**: high performance, supports structured logging, fits applications that need efficient logging.
- **`zerolog`**: minimal overhead, efficient logging, JSON format, fits cases that need high performance and low overhead.

##### 4.2 Picking the Right Logging Library

- For high-concurrency, performance-sensitive cases, prefer `zap` or `zerolog`.
- When you need hooks and custom formatters, pick `logrus`; it has the most complete feature set, at the cost of comparatively lower performance.

## References

- [log standard library](https://pkg.go.dev/log)
- [Official blog · Structured Logging with slog](https://go.dev/blog/slog)

## Sibling pages

- [Aggregation](/log/Aggregation.md)
- [Log](/log/Log.md)
- [ModLog](/log/ModLog.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Aggregation](/log/Aggregation.md)
- [Log](/log/Log.md)
- [ModLog](/log/ModLog.md)
