在 Go 语言中，`true` 和 `false` 是布尔类型的预定义常量，用于表示逻辑真和逻辑假。

### 布尔类型

布尔类型只有两个预定义的值：`true` 和 `false`。在 Go 中，布尔类型用于条件判断、逻辑运算和控制流程。

#### 声明和初始化

```go
var b1 bool = true
var b2 = false // 自动推断类型为 bool
```

#### 逻辑运算

布尔类型可以进行逻辑运算，包括逻辑与 (`&&`)、逻辑或 (`||`)、逻辑非 (`!`) 等。

```go
fmt.Println(true && false) // 输出: false
fmt.Println(true || false) // 输出: true
fmt.Println(!true)         // 输出: false
```

#### 条件判断

布尔类型常用于 `if`、`for`、`switch` 等语句的条件判断中。

```go
if true {
    fmt.Println("This condition is true")
}

for i := 0; i < 3; i++ {
    fmt.Println(i)
}

switch true {
case true:
    fmt.Println("This case is true")
default:
    fmt.Println("This case is false")
}
```

### 使用场景

- **条件判断**：在控制流程中根据条件执行不同的逻辑。
- **逻辑运算**：对布尔值进行逻辑操作，例如组合多个条件进行复杂的逻辑判断。
- **函数返回值**：函数可以返回布尔值，表示某些条件是否满足。

### 示例代码

以下是一个简单示例，展示了布尔类型的使用：

```go
package main

import "fmt"

func main() {
    var isOpen bool = true
    var isFound = false // 自动推断类型为 bool

    if isOpen {
        fmt.Println("The door is open")
    }

    if !isFound {
        fmt.Println("Item not found")
    }

    fmt.Println(true && false) // 输出: false
    fmt.Println(true || false) // 输出: true
}
```

### 总结

布尔类型 `true` 和 `false` 是 Go 语言中的预定义常量，用于表示逻辑上的真和假。它们在条件判断、逻辑运算和控制流程中都有重要的作用，是编写条件逻辑和控制程序流程的基础。