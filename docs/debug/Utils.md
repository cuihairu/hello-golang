Go 标准库中提供了一些调试工具和功能，帮助开发者进行代码调试。以下是一些与调试相关的工具和功能：

### 1. **`log` 包**

`log` 包提供了基本的日志记录功能，能够帮助开发者在程序中输出调试信息。可以通过 `log` 包记录不同级别的日志信息，帮助排查问题。例如：

```go
import "log"

func main() {
    log.Println("This is a log message.")
}
```

### 2. **`testing` 包**

`testing` 包不仅用于编写单元测试，还支持基准测试和示例测试。通过在测试函数中添加调试代码，可以帮助检查程序的正确性。示例：

```go
import (
    "testing"
    "log"
)

func TestExample(t *testing.T) {
    log.Println("Debugging information")
    // Your test code here
}
```

### 3. **`pprof` 包**

`pprof` 包用于性能分析和调试。它可以生成程序的 CPU 和内存剖析信息，帮助识别性能瓶颈和内存泄漏问题。使用方法如下：

- **启动 pprof**：

```go
import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()
    // Your application code here
}
```

- **查看性能剖析**：运行应用程序后，可以通过访问 `http://localhost:6060/debug/pprof/` 来获取不同类型的剖析信息。

### 4. **`delve` 调试器**

虽然 `delve` 不是 Go 标准库的一部分，但它是 Go 语言的主要调试工具。`delve` 提供了丰富的调试功能，包括设置断点、单步执行、查看变量值、调用栈等。使用 `delve` 进行调试的基本步骤：

- **安装 delve**：

```sh
go install github.com/go-delve/delve/cmd/dlv@latest
```

- **启动调试**：

```sh
dlv debug <your_program>
```

- **常用命令**：

  - `break <location>`：设置断点
  - `next`：单步执行
  - `step`：进入函数
  - `continue`：继续运行直到下一个断点
  - `print <variable>`：查看变量值
  - `stack`：查看调用栈

### 5. **`runtime` 包**

`runtime` 包提供了与 Go 运行时相关的功能，帮助调试一些底层问题。例如，可以使用 `runtime.Stack` 来打印当前的堆栈信息：

```go
import (
    "fmt"
    "runtime"
)

func main() {
    buf := make([]byte, 1<<16)
    runtime.Stack(buf, true)
    fmt.Printf("%s", buf)
}
```

这些工具和功能可以帮助你在 Go 程序中进行有效的调试和性能分析。
