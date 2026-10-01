在 Go 语言中，函数可以返回多个值，这是一个非常有用的特性，可以用于返回函数的计算结果及其相关的状态信息（例如错误信息）。

### 定义和调用返回多个值的函数

#### 示例：简单的多返回值函数

```go
package main

import "fmt"

// 定义一个返回两个整数之和及差的函数
func sumAndDiff(a int, b int) (int, int) {
    sum := a + b
    diff := a - b
    return sum, diff
}

func main() {
    sum, diff := sumAndDiff(10, 5)
    fmt.Println("Sum:", sum)   // 输出：Sum: 15
    fmt.Println("Diff:", diff) // 输出：Diff: 5
}
```

在上述示例中：
- `sumAndDiff` 函数返回两个整数，分别是 `sum` 和 `diff`。
- 调用函数时，使用多重赋值语法来接收返回值。

### 使用命名返回值

Go 语言还支持命名返回值。在函数定义中为返回值命名，这些命名返回值在函数内部作为局部变量使用，函数可以直接通过 `return` 语句返回它们。

#### 示例：使用命名返回值

```go
package main

import "fmt"

// 使用命名返回值
func sumAndDiff(a int, b int) (sum int, diff int) {
    sum = a + b
    diff = a - b
    return // 直接使用 return 返回命名返回值
}

func main() {
    sum, diff := sumAndDiff(10, 5)
    fmt.Println("Sum:", sum)   // 输出：Sum: 15
    fmt.Println("Diff:", diff) // 输出：Diff: 5
}
```

在上述示例中：
- `sumAndDiff` 函数使用命名返回值 `sum` 和 `diff`。
- 在函数内部，直接给 `sum` 和 `diff` 赋值，并使用 `return` 语句返回它们。

### 常见的多返回值模式

多返回值在 Go 语言中广泛应用，特别是在错误处理方面。通常函数返回一个结果值和一个错误值。

#### 示例：错误处理模式

```go
package main

import (
    "errors"
    "fmt"
)

// 定义一个返回结果和错误的函数
func divide(a int, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err) // 输出：Error: division by zero
    } else {
        fmt.Println("Result:", result)
    }
}
```

在上述示例中：
- `divide` 函数返回两个值：计算结果和可能的错误。
- 调用函数后，检查错误值 `err`，如果存在错误则处理错误，否则使用结果值。

### 忽略返回值

在某些情况下，可以忽略不需要的返回值。使用空标识符 `_` 可以丢弃这些返回值。

#### 示例：忽略返回值

```go
package main

import "fmt"

func sumAndDiff(a int, b int) (int, int) {
    sum := a + b
    diff := a - b
    return sum, diff
}

func main() {
    sum, _ := sumAndDiff(10, 5)
    fmt.Println("Sum:", sum) // 输出：Sum: 15
}
```

在上述示例中：
- 调用 `sumAndDiff` 函数时，忽略了差值 `diff`，只接收了和 `sum`。

### 总结

Go 语言的多返回值特性使得函数可以返回多个相关的信息，而不需要使用复杂的数据结构。这在处理错误、返回状态信息和计算多个结果时非常有用。通过命名返回值，可以使代码更加清晰和自解释。忽略不需要的返回值也使得代码更加简洁。