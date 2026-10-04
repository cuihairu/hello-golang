简短声明（short variable declaration）用 `:=` 在函数内部声明并初始化变量，一次可以声明一个或多个。

### 基本语法

```go
variableName := expression
```

### 详细示例

#### 1. 简短声明单个变量

```go
package main

import "fmt"

func main() {
    a := 1 // 声明并初始化一个整数变量 a
    fmt.Println(a) // 输出：1
}
```

#### 2. 简短声明多个变量

```go
package main

import "fmt"

func main() {
    a, b, c := 1, 2, 3 // 同时声明并初始化三个变量
    fmt.Println(a, b, c) // 输出：1 2 3
}
```

#### 3. 与函数返回值结合使用

```go
package main

import "fmt"

func add(a, b int) int {
    return a + b
}

func main() {
    result := add(3, 4) // 使用简短声明接收函数的返回值
    fmt.Println(result) // 输出：7
}
```

#### 4. 在循环中使用简短声明

```go
package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ { // 在 for 循环中使用简短声明
        fmt.Println(i)
    }
}
```

#### 5. 与 `if` 语句结合使用

```go
package main

import "fmt"

func main() {
    if a := 10; a > 5 { // 在 if 语句中使用简短声明
        fmt.Println(a) // 输出：10
    }
}
```

这里 `a` 声明在 `if` 的条件部分，只在 `if` 语句内可用。

### 注意事项

1. **只能在函数内部使用**：包级别（全局作用域）用不了。
2. **至少有一个新变量**：如果在一个已经存在的变量上使用简短声明，必须至少有一个新变量。例如：
    ```go
    package main

    import "fmt"

    func main() {
        a, b := 1, 2
        a, c := 3, 4 // 这里 a 是已存在的变量，而 c 是新变量
        fmt.Println(a, b, c) // 输出：3 2 4
    }
    ```
3. **类型推断**：Go 会根据右侧表达式的类型自动推断变量的类型。

### 总结

`:=` 把声明和初始化并成一步。两条限制要记住：只能写在函数内部；对已有变量重新声明时，左边至少要有一个新变量。