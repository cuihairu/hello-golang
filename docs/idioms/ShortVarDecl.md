在 Go 语言中，简短声明（short variable declaration）是一种简洁的方式，用于在函数内部声明并初始化变量。它使用 `:=` 操作符，可以同时声明并赋值一个或多个变量。简短声明的语法使代码更加简洁明了，提高了可读性。

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

在这个例子中，`a` 被声明为一个整数，并被初始化为 `1`。

#### 2. 简短声明多个变量

```go
package main

import "fmt"

func main() {
    a, b, c := 1, 2, 3 // 同时声明并初始化三个变量
    fmt.Println(a, b, c) // 输出：1 2 3
}
```

在这个例子中，`a`、`b` 和 `c` 被同时声明并初始化。

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

在这个例子中，`result` 被声明并初始化为 `add` 函数的返回值。

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

在这个例子中，`i` 被声明并初始化为循环计数器。

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

在这个例子中，`a` 被声明并初始化在 `if` 语句的条件部分。

### 注意事项

1. **只能在函数内部使用**：简短声明不能在包级别（全局作用域）使用，只能在函数内部使用。
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

简短声明（short variable declaration）通过 `:=` 操作符在 Go 语言中提供了一种简洁的方式来声明和初始化变量。它使代码更为简洁和易读，但也有一些限制条件需要注意，例如只能在函数内部使用，并且在重新声明变量时必须包含至少一个新变量。