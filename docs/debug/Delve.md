`delve` 是 Go 语言专用的调试器。下面从安装、启动方式到常用命令过一遍。

### 安装 `delve`

1. **安装 `delve`**

   先确认机器上有 Go 环境，然后执行：

   ```sh
   go install github.com/go-delve/delve/cmd/dlv@latest
   ```

   安装后，`delve` 的二进制文件会放在 `$GOPATH/bin` 目录下。如果 `$GOPATH/bin` 不在你的 `PATH` 中，需要手动添加，或者使用完整路径运行 `delve`。

2. **验证安装**

   打出版本号说明装好了：

   ```sh
   dlv version
   ```

### 启动 `delve`

`delve` 支持几种启动模式，包括直接调试程序、调试已编译程序、附加到运行中的进程等。

1. **直接调试程序**

   使用 `dlv debug` 命令可以编译并调试当前目录下的 Go 包（在 `main.go` 所在目录直接运行即可；也可传入包路径，如 `dlv debug ./cmd/app`）：

   ```sh
   dlv debug
   ```

   这会编译并启动程序，并进入调试模式。注意 `dlv debug` 接收的是包路径，不能直接传源文件名。

2. **调试已编译程序**

   如果程序已经编译，可以使用 `dlv exec` 命令调试：

   ```sh
   dlv exec <your_program>
   ```

3. **附加到运行中的进程**

   可以使用 `dlv attach` 附加到已经运行的 Go 程序进程：

   ```sh
   dlv attach <pid>
   ```

### 基本调试命令

常用的调试命令：

1. **设置断点**

   ```sh
   break <location>
   ```

   - `<location>` 可以是文件名和行号（例如 `main.go:10`）或函数名（例如 `main.main`）。
   - 示例：`break main.go:15` 或 `break main.main`

2. **继续执行**

   ```sh
   continue
   ```

   继续程序的执行，直到下一个断点或程序结束。

3. **单步执行**

   ```sh
   step
   ```

   进入函数内部并执行下一行代码。

4. **跳过当前行**

   ```sh
   next
   ```

   执行当前行代码，但不进入函数内部。

5. **跳出当前函数**

   ```sh
   stepout
   ```

   执行到当前函数返回为止。

6. **打印变量值**

   ```sh
   print <variable>
   ```

   打印指定变量的当前值。可以是局部变量、全局变量或结构体字段。

7. **查看调用栈**

   ```sh
   stack
   ```

   显示当前的调用栈，包括函数调用的顺序。

8. **查看当前作用域的局部变量**

   ```sh
   locals
   ```

   显示当前函数的局部变量。

9. **查看当前函数的参数**

   ```sh
   args
   ```

   显示当前函数的参数。

10. **列出源码**

    ```sh
    list
    ```

    显示当前断点附近的源代码。可以指定行号或函数名来查看特定区域。

### 高级调试技巧

1. **条件断点**

   条件成立时才中断：

   ```sh
   break <location> if <condition>
   ```

   例如：`break main.go:10 if x > 5`

2. **查看 Goroutines**

   使用 `goroutines` 命令查看所有 Goroutine 的状态：

   ```sh
   goroutines
   ```

   可以选择附加到特定 Goroutine 进行调试。

3. **观察表达式**

   使用 `watch` 命令设置观察点，观察特定表达式的变化：

   ```sh
   watch <expression>
   ```

   例如：`watch x > 5`

4. **管理断点**

   - 列出所有断点：`breakpoints`
   - 删除断点：`clear <location>`

5. **自定义调试配置**

   在 IDE（如 VSCode）里调试时，`delve` 由 IDE 的调试配置文件（如 `.vscode/launch.json`）驱动，断点和变量面板直接可用。

### 示例调试会话

假设有一个简单的 Go 程序 `main.go`：

```go
package main

import "fmt"

func main() {
    x := 10
    y := 20
    result := add(x, y)
    fmt.Println(result)
}

func add(a, b int) int {
    return a + b
}
```

用 `delve` 调这个程序：

1. **启动调试**

   在 `main.go` 所在目录运行：

   ```sh
   dlv debug
   ```

2. **在 `delve` 提示符下**

   ```sh
   (dlv) break main.go:9
   (dlv) continue
   (dlv) print x
   (dlv) print result
   (dlv) step
   ```

   这些命令在 `fmt.Println(result)` 处设置断点（此时 `result` 已被赋值为 30），继续执行程序并查看变量值。

### 总结

断点、单步、变量查看、条件断点、goroutine 列表，`delve` 的命令覆盖了调试 Go 程序的主要动作。装好以后 `dlv debug` 进去，剩下的就是命令行交互。