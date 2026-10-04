**包**（Package）和**模块**（Module）是组织代码的两个单位：包把相关代码分组封装，模块管包的集合和版本。不同语言的叫法和用法不一，做的都是组织、封装、复用这几件事。

### 1. 包（Package）

#### 概念

包是代码的一个组织单元，用于将相关的功能和数据封装在一起。包的主要作用是：

- **封装**：将相关功能和数据封装在一起，隐藏内部实现细节。
- **复用**：使得其他代码可以重用包中的功能。
- **命名空间**：防止命名冲突，确保不同包中的标识符（如函数、变量、类型）不会互相干扰。

#### Go 中的包

在 Go 语言中，包是代码的基本组织单位。每个 Go 源文件都属于某个包，并且每个包都有一个唯一的名称。

- **包的定义**：一个包由一个或多个 Go 源文件组成，这些文件位于同一个目录下，并且文件顶部的 `package` 语句指定了包的名称。
- **导入包**：使用 `import` 语句导入其他包，从而使用其定义的函数、变量和类型。
- **包的使用**：包的公共成员（以大写字母开头的标识符）可以被其他包访问，而包的私有成员（以小写字母开头的标识符）只能在包内部访问。

示例代码：
```go
// 文件: mathutils.go
package mathutils

// Add adds two integers.
func Add(a, b int) int {
    return a + b
}

// Subtract subtracts two integers.
func Subtract(a, b int) int {
    return a - b
}
```

```go
// 文件: main.go
package main

import (
    "fmt"
    "path/to/your/project/mathutils"
)

func main() {
    sum := mathutils.Add(10, 5)
    diff := mathutils.Subtract(10, 5)
    fmt.Println("Sum:", sum)
    fmt.Println("Difference:", diff)
}
```

### 2. 模块（Module）

#### 概念

模块是更高层次的代码组织单位，用于管理包的集合。模块的主要作用是：

- **依赖管理**：帮助管理代码的依赖关系和版本控制。
- **版本化**：为代码库提供版本控制，使得不同版本的模块可以被管理和使用。
- **封装**：提供对包的逻辑分组，便于模块的分发和重用。

#### Go 中的模块

Go 的模块（module）从 Go 1.11 开始引入：它是包的集合，带版本信息，依赖和版本从此都记在 `go.mod` 里。

- **模块的定义**：一个模块由一个 `go.mod` 文件定义，该文件位于模块的根目录下。`go.mod` 文件包含了模块的名称、依赖关系和其他版本信息。
- **模块的使用**：可以通过 `go mod` 命令来管理模块的依赖和版本。

示例代码：

**创建模块**
```bash
go mod init example.com/myapp
```

**`go.mod` 文件**
```go
module example.com/myapp

go 1.20
```

**添加依赖**
```bash
go get github.com/some/dependency@v1.2.3
```

**使用依赖**
```go
package main

import (
    "fmt"
    "github.com/some/dependency"
)

func main() {
    result := dependency.SomeFunction()
    fmt.Println(result)
}
```

**管理依赖**
- `go mod tidy`：清理 `go.mod` 和 `go.sum` 文件，删除不再需要的依赖。
- `go mod vendor`：将所有依赖复制到 `vendor` 目录中，以便进行离线构建。

### 总结

- **包（Package）**：把相关功能封装在一起，大写标识符对外可见，小写只在包内能用。
- **模块（Module）**：包的集合，`go.mod` 记模块名、依赖和版本。

两者各管一段：目录内的组织和导出归包，依赖版本归模块。`go mod init` 建模块，`go get` 加依赖，`go mod tidy` 清理多余的。