### 使用 GDB 调试 Go 程序

GDB（GNU Debugger）主要用于调试 C 和 C++ 程序，也能调试 Go 程序，只是对 Go 的支持有限。

#### 1. 安装和准备

**1.1 安装 GDB**

在 Linux 系统上，你可以通过包管理器安装 GDB：

- **在 Debian/Ubuntu 上**：
  ```bash
  sudo apt-get update
  sudo apt-get install gdb
  ```

- **在 Fedora 上**：
  ```bash
  sudo dnf install gdb
  ```

- **在 macOS 上**：
  ```bash
  brew install gdb
  ```

- **在 Windows上**：
  ```ps1
  scoop install gdb
  ```


**1.2 编译 Go 程序**

为了使用 GDB 调试 Go 程序，需要以调试模式编译 Go 程序。默认情况下，Go 编译器会包含调试信息，但你可以使用 `-gcflags` 选项来确保调试信息的完整性。

```bash
go build -gcflags "all=-N -l" -o myprogram main.go
```

- `-N`：禁用优化，这有助于提高调试的准确性。
- `-l`：禁用内联函数，以便能够更好地调试。

#### 2. 启动 GDB

使用 GDB 运行编译后的程序：

```bash
gdb ./myprogram
```

这将启动 GDB 并加载 `myprogram` 二进制文件。

#### 3. 常用 GDB 命令

**3.1 运行程序**

启动程序的执行：

```gdb
(gdb) run
```

**3.2 设置断点**

可以在 Go 程序的指定行、函数或地址上设置断点：

- **在某一行设置断点**：
  ```gdb
  (gdb) break main.go:10
  ```

- **在某个函数上设置断点**：
  ```gdb
  (gdb) break main.main
  ```

- **在特定地址设置断点**：
  ```gdb
  (gdb) break *0x123456
  ```

**3.3 查看断点**

列出所有断点及其状态：

```gdb
(gdb) info breakpoints
```

**3.4 继续执行**

继续执行程序直到下一个断点：

```gdb
(gdb) continue
```

**3.5 单步调试**

- **单步执行当前行**：
  ```gdb
  (gdb) next
  ```

- **进入函数调用**：
  ```gdb
  (gdb) step
  ```

- **跳过函数调用**：
  ```gdb
  (gdb) finish
  ```

**3.6 查看变量**

查看当前作用域中的变量值：

```gdb
(gdb) print variableName
```

如果需要查看复杂的结构体或数组，可以使用更详细的命令：

```gdb
(gdb) ptype variableName
```

**3.7 查看调用栈**

查看当前的调用栈信息：

```gdb
(gdb) backtrace
```

**3.8 修改变量**

在调试过程中，可以修改变量的值：

```gdb
(gdb) set variable variableName = newValue
```

**3.9 列出源代码**

查看当前断点位置的源代码：

```gdb
(gdb) list
```

**3.10 退出 GDB**

调试完成后退出 GDB：

```gdb
(gdb) quit
```

#### 4. 调试注意事项

**4.1 Go 的调试信息**

Go 编译器生成的调试信息对 GDB 来说是有限的，某些情况下 GDB 无法正确显示 Go 特有的结构体和 goroutine 信息。

**4.2 GDB 和 Go 语言的兼容性**

GDB 主要为 C 和 C++ 设计，对 Go 的支持不足。调试较复杂的 Go 程序时会遇到困难，比如调试并发（goroutine）相关的部分。

#### 5. 小结

调试 Go 程序前，先用 `go build -gcflags "all=-N -l"` 关闭优化和内联，再用 `break` 设断点、`next`/`step` 单步、`print` 看变量。GDB 对 Go 的支持有限，结构体和 goroutine 信息可能显示不全，调试并发程序时尤其明显。