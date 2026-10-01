### 3. 使用标准库 `flag` 包解析命令行参数

Go 语言的标准库 `flag` 包提供了简单而强大的命令行参数解析功能。它支持基本的选项参数解析，包括布尔值、整数、字符串等类型。在这一章，我们将详细介绍如何使用 `flag` 包解析命令行参数。

#### 3.1 `flag` 包概述

`flag` 包提供了一组函数和方法，用于定义和解析命令行选项参数。通过 `flag` 包，可以轻松地定义各种类型的选项参数，并将它们解析为对应的变量。

#### 3.2 定义和解析布尔选项

布尔选项用于表示开关类型的参数，例如启用或禁用某个功能。使用 `flag.Bool` 函数可以定义布尔选项：

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    verbose := flag.Bool("verbose", false, "Enable verbose output")

    flag.Parse()

    if *verbose {
        fmt.Println("Verbose output enabled")
    } else {
        fmt.Println("Verbose output disabled")
    }
}
```

运行示例：

```shell
$ go run main.go --verbose
Verbose output enabled

$ go run main.go
Verbose output disabled
```

#### 3.3 定义和解析字符串选项

字符串选项用于传递字符串类型的参数，例如文件路径或用户名。使用 `flag.String` 函数可以定义字符串选项：

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    name := flag.String("name", "World", "Name to greet")

    flag.Parse()

    fmt.Printf("Hello, %s!\n", *name)
}
```

运行示例：

```shell
$ go run main.go --name=Go
Hello, Go!

$ go run main.go
Hello, World!
```

#### 3.4 定义和解析整数选项

整数选项用于传递整数类型的参数，例如端口号或重试次数。使用 `flag.Int` 函数可以定义整数选项：

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    port := flag.Int("port", 8080, "Port number")

    flag.Parse()

    fmt.Printf("Server running on port %d\n", *port)
}
```

运行示例：

```shell
$ go run main.go --port=9090
Server running on port 9090

$ go run main.go
Server running on port 8080
```

#### 3.5 定义和解析其他类型选项

`flag` 包还支持其他类型的选项，例如浮点数和时间值。可以使用对应的函数 `flag.Float64` 和 `flag.Duration` 来定义这些选项。例如：

```go
package main

import (
    "flag"
    "fmt"
    "time"
)

func main() {
    timeout := flag.Duration("timeout", 30*time.Second, "Timeout duration")

    flag.Parse()

    fmt.Printf("Timeout: %v\n", *timeout)
}
```

运行示例：

```shell
$ go run main.go --timeout=1m
Timeout: 1m0s

$ go run main.go
Timeout: 30s
```

#### 3.6 自定义选项解析

除了标准类型，`flag` 包还支持自定义选项解析。可以实现 `flag.Value` 接口来自定义选项类型。`flag.Value` 接口定义了 `Set` 和 `String` 方法：

```go
package main

import (
    "flag"
    "fmt"
)

type myFlag string

func (f *myFlag) Set(value string) error {
    *f = myFlag(value)
    return nil
}

func (f *myFlag) String() string {
    return string(*f)
}

func main() {
    var customFlag myFlag
    flag.Var(&customFlag, "custom", "Custom flag example")

    flag.Parse()

    fmt.Printf("Custom flag: %s\n", customFlag)
}
```

运行示例：

```shell
$ go run main.go --custom=example
Custom flag: example
```

#### 3.7 处理未定义选项和帮助信息

`flag` 包自动生成帮助信息，帮助用户了解可用的选项。当用户传递未定义的选项时，`flag` 包会自动提示错误信息并显示帮助信息：

```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    help := flag.Bool("help", false, "Display help")

    flag.Parse()

    if *help {
        flag.Usage()
        os.Exit(0)
    }

    fmt.Println("Running the program")
}
```

运行示例：

```shell
$ go run main.go --help
Usage of /tmp/go-build123456/b001/exe/main:
  -help
        Display help

$ go run main.go --undefined
flag provided but not defined: -undefined
Usage of /tmp/go-build123456/b001/exe/main:
  -help
        Display help
exit status 2
```

#### 3.8 解析位置参数

位置参数是按顺序传递给程序的参数。使用 `flag` 包解析位置参数时，需要在调用 `flag.Parse` 后手动处理位置参数：

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    flag.Parse()
    args := flag.Args()

    if len(args) < 2 {
        fmt.Println("Usage: main.go <input> <output>")
        return
    }

    input := args[0]
    output := args[1]

    fmt.Printf("Input: %s\n", input)
    fmt.Printf("Output: %s\n", output)
}
```

运行示例：

```shell
$ go run main.go input.txt output.txt
Input: input.txt
Output: output.txt

$ go run main.go
Usage: main.go <input> <output>
```

### 总结

本章介绍了如何使用 Go 语言的标准库 `flag` 包解析命令行参数，包括布尔选项、字符串选项、整数选项、其他类型选项、自定义选项解析、处理未定义选项和帮助信息以及解析位置参数。通过 `flag` 包，开发者可以轻松实现各种命令行工具的参数解析需求。在接下来的章节中，我们将进一步探讨如何使用第三方库解析命令行参数，以实现更复杂和高级的命令行工具功能。