### Go 和环境变量

Go 用几个环境变量定位安装目录、工作区和可执行文件的位置，常用的就这几个：

#### 1. GOROOT

`GOROOT` 是 Go 安装目录的路径。这个变量指向 Go 工具链和标准库所在的位置。通常在安装 Go 时，`GOROOT` 会被自动设置，不需要手动配置。

**示例**：
```bash
export GOROOT=/usr/local/go
```

#### 2. GOPATH

`GOPATH` 是工作空间的路径，用于存放 Go 源代码、包和可执行文件。`GOPATH` 工作空间包含三个目录：`src`（源代码）、`pkg`（编译后的包）和 `bin`（编译后的可执行文件）。

**示例**：
```bash
export GOPATH=$HOME/go
```

#### 3. GOBIN

`GOBIN` 是安装 Go 可执行文件的目录。默认情况下，它是 `$GOPATH/bin`，但可以自定义为其他路径。

**示例**：
```bash
export GOBIN=$HOME/go/bin
```

#### 4. GO111MODULE

`GO111MODULE` 是用于启用或禁用 Go 模块支持的变量。它有三个值：
- `off`: 关闭模块支持，使用传统的 `GOPATH` 模式。
- `on`: 启用模块支持，不考虑当前目录。
- `auto`: 在包含 `go.mod` 文件的目录或其子目录中启用模块支持。

**示例**：
```bash
export GO111MODULE=on
```

### Go 的相对路径问题

Go 的路径问题集中在两处：导入包时走的是模块路径，读写文件时走的是运行时工作目录。分清这两条，多数“找不到文件”的问题就能对上号。

#### 相对路径和绝对路径

- **绝对路径**：从根目录开始的完整路径。
- **相对路径**：相对于当前工作目录的路径。

在 Go 项目中，通常使用模块路径来导入包，而不是文件系统中的相对路径。这是因为 Go 语言在设计上要求包的导入路径基于 `go.mod` 中声明的模块路径（例如 `myproject/utils`），这样可以避免路径依赖的混乱。

#### 执行时的相对路径

当执行 Go 程序时，相对路径是相对于程序的当前工作目录（working directory）的路径，而不是相对于源文件的路径。执行路径是指执行程序时所在的目录。

#### 例子

假设有一个项目结构如下：

```
myproject/
├── go.mod
├── main.go
└── data/
    └── file.txt
```

`main.go` 读取 `data/file.txt` 文件的示例：

```go
package main

import (
    "fmt"
    "log"
    "os"
    "path/filepath"
)

func main() {
    // 使用相对路径读取文件
    path := filepath.Join("data", "file.txt")
    content, err := os.ReadFile(path)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(content))
}
```

在这个例子中，文件路径 `data/file.txt` 是相对于程序的当前工作目录的路径。如果在 `myproject` 目录下执行程序，文件路径将是正确的。如果在其他目录下执行程序，需要提供正确的相对路径。

### Go 模块化项目

使用 Go 模块化项目，可以在项目根目录下创建一个 `go.mod` 文件，指定模块路径。这使得包的导入变得更加简单和可靠。

创建 `go.mod` 文件：

```bash
go mod init myproject
```

`go.mod` 文件的内容：

```
module myproject

go 1.16
```

### 处理相对路径问题

避开相对路径坑的两条做法：

1. **使用 Go 模块**：确保在项目根目录下有一个 `go.mod` 文件，并使用模块路径导入包。
2. **正确设置工作目录**：在运行程序前，确保当前工作目录是程序所期望的目录。

### 代码示例

下面的程序先打印当前工作目录，再按相对路径读文件：

```go
package main

import (
    "fmt"
    "log"
    "os"
    "path/filepath"
)

func main() {
    // 获取当前工作目录
    cwd, err := os.Getwd()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Current working directory:", cwd)

    // 使用相对路径读取文件
    path := filepath.Join("data", "file.txt")
    content, err := os.ReadFile(path)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("File content:", string(content))
}
```

创建 `go.mod` 文件：

```bash
go mod init myproject
```

设置环境变量：

```bash
export GOPATH=$HOME/go
export GOBIN=$HOME/go/bin
export GO111MODULE=on
```

确保正确的工作目录：

```bash
cd myproject
go run main.go
```

### 总结

`GOROOT` 指向安装目录，`GOPATH` 管工作区，`GOBIN` 管可执行文件的落点，`GO111MODULE` 决定模块模式开不开。导入包只认 `go.mod` 里的模块路径，读文件只认运行时的工作目录——程序启动前先 `cd` 到预期的目录，再跑 `go run`。