### 第三方日志库

除了 Go 标准库的 `log` 和 `slog`，还有许多功能强大且灵活的第三方日志库。这些库通常提供更丰富的功能，如结构化日志、日志级别、钩子机制等，适合复杂的日志需求。

#### 1. `logrus`

##### 1.1 安装与基本使用

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

##### 1.2 日志级别和钩子

```go
logger.SetLevel(logrus.WarnLevel)

logger.Info("This will not be logged")
logger.Warn("This will be logged")

logger.AddHook(&CustomHook{})
```

##### 1.3 自定义格式化器和输出

```go
logger.SetFormatter(&logrus.JSONFormatter{})

file, err := os.OpenFile("app.log", os.O_CREATE|os.O_WRONLY, 0666)
if err == nil {
	logger.SetOutput(file)
} else {
	logger.Info("Failed to log to file, using default stderr")
}
```

##### 1.4 实践案例

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

##### 2.1 安装与基本使用

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

##### 2.2 性能优化

```go
logger, _ := zap.NewProduction(zap.WithCaller(false))
```

##### 2.3 结构化日志

```go
logger.Info("This is a structured log message",
	zap.String("key1", "value1"),
	zap.Int("key2", 123))
```

##### 2.4 配置与示例

```go
config := zap.NewProductionConfig()
config.OutputPaths = []string{"stdout", "app.log"}
logger, _ := config.Build()

logger.Info("This is an info message with custom configuration")
```

##### 2.5 实践案例

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

##### 3.1 安装与基本使用

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

##### 3.2 最小开销和高效日志

```go
log.Info().Str("key1", "value1").Int("key2", 123).Msg("This is a structured log message")
```

##### 3.3 使用 JSON 格式记录日志

```go
log.Logger = log.Output(os.Stdout)
log.Info().Msg("This is a log message in JSON format")
```

##### 3.4 实践案例

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

#### 4. 比较与选择

##### 4.1 不同日志库的比较

- **`logrus`**：功能全面，支持钩子、自定义格式化器和输出，但性能相对较低。
- **`zap`**：高性能，支持结构化日志，适合需要高效日志记录的应用。
- **`zerolog`**：最小开销，高效日志，采用 JSON 格式，适合需要高性能和低开销的场景。

##### 4.2 选择合适的日志库

- 根据应用的性能要求和功能需求选择合适的日志库。
- 考虑日志库的易用性和可扩展性。
- 在高并发和高性能场景下，优先选择 `zap` 或 `zerolog`。

