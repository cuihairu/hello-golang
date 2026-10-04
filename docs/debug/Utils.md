Go 的调试工具分两类：标准库里的 `log`、`testing`、`pprof`、`runtime`，以及标准库之外的 `delve` 调试器。

### 1. **`log` 包**

`log` 包负责基本的日志输出，排查问题时用得上（标准库 `log` 本身不区分日志级别，若需要分级日志可使用 Go 1.21 引入的 `log/slog`）。例如：

```go
import "log"

func main() {
    log.Println("This is a log message.")
}
```

### 2. **`testing` 包**

`testing` 包除了单元测试，还支持基准测试和示例测试。在测试函数里加调试代码，可以检查程序行为。示例：

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

`delve` 不在标准库里，但是 Go 的主流调试器，断点、单步执行、查看变量、调用栈都支持。基本用法：

- **安装 delve**：

```sh
go install github.com/go-delve/delve/cmd/dlv@latest
```

- **启动调试**：

```sh
# 编译当前包并启动调试（最常用）
dlv debug

# 调试已编译好的二进制
dlv exec ./your_program
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

日志、测试、剖析、断点各管一段：加日志缩小问题范围，测试不过用 `delve` 断点跟进，性能问题交给 `pprof` 的剖析数据。
