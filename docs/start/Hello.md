# 你好Go
好的，下面是一个简单的多模块Go程序示例。这个程序将分为两个模块，一个主模块和一个库模块。主模块将调用库模块中的函数来打印"Hello, Go!"。

### 创建项目结构

首先，创建项目结构：

```
hello-go/
├── go.mod
├── main.go
└── greeting/
    ├── go.mod
    └── greeting.go
```

### 1. 初始化主模块

在`hello-go`目录下初始化主模块：

```sh
mkdir -p hello-go
cd hello-go
go mod init hello-go
```

### 2. 创建主模块文件

在`hello-go`目录下创建`main.go`文件：

```go
// main.go

package main

// 导入greeting模块
import (
    "fmt"
    "hello-go/greeting"
)

func main() {
    // 调用greeting模块中的Hello函数
    message := greeting.Hello()
    fmt.Println(message)
}
```

### 3. 初始化库模块

在`hello-go/greeting`目录下初始化库模块：

```sh
mkdir -p greeting
cd greeting
go mod init hello-go/greeting
```

### 4. 创建库模块文件

在`hello-go/greeting`目录下创建`greeting.go`文件：

```go
// greeting.go

package greeting

// Hello 函数返回一个问候消息
func Hello() string {
    return "Hello, Go!"
}
```

### 5. 设置模块依赖

返回主模块目录：

```sh
cd ..
```

然后运行以下命令来添加`greeting`模块的依赖：

```sh
go mod edit -replace hello-go/greeting=./greeting
go mod tidy
```

### 6. 运行程序

在主模块目录下，运行以下命令来编译和运行程序：

```sh
go run main.go
```

你应该会看到输出：

```
Hello, Go!
```

### 代码解释

#### 主模块 (`main.go`)

```go
// main.go

package main

// 导入标准库fmt用于输出，导入自定义模块greeting
import (
    "fmt"
    "hello-go/greeting"
)

func main() {
    // 调用greeting模块中的Hello函数，接收返回的字符串
    message := greeting.Hello()
    // 打印返回的问候消息
    fmt.Println(message)
}
```

1. `package main`: 定义主包，这是程序的入口包。
2. `import ("fmt" "hello-go/greeting")`: 导入标准库`fmt`和自定义模块`greeting`。
3. `func main() { ... }`: 定义`main`函数，这是Go程序的入口点。
4. `message := greeting.Hello()`: 调用`greeting`模块中的`Hello`函数，并将返回的字符串赋值给`message`变量。
5. `fmt.Println(message)`: 使用`fmt.Println`函数打印`message`的内容。

#### 库模块 (`greeting.go`)

```go
// greeting.go

package greeting

// Hello 函数返回一个问候消息
func Hello() string {
    return "Hello, Go!"
}
```

1. `package greeting`: 定义`greeting`包，这个包提供了一个公共的`Hello`函数。
2. `func Hello() string { ... }`: 定义`Hello`函数，它返回一个`string`类型的问候消息。
3. `return "Hello, Go!"`: 返回"Hello, Go!"字符串作为问候消息。
