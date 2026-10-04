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

- **条件判断**：`if`、`for`、`switch` 的条件位置。
- **逻辑运算**：`&&`、`||`、`!` 把多个条件组合成一个。
- **函数返回值**：返回布尔值表示条件是否满足，调用方拿到就能判断。

### 示例代码

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

`true` 和 `false` 是布尔类型的预定义常量，`&&`、`||`、`!` 都在它们之上运算，`if`、`for`、`switch` 的条件用的也是布尔值。