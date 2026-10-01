# 函数的定义和调用
在 Go 语言中，函数不仅可以使用标准的定义方式，还可以使用类型定义（type definition）来创建函数类型。这使得函数能够作为类型进行传递和操作。下面我们详细介绍函数的定义、调用以及如何使用类型定义函数。

### 函数定义

#### 基本语法

函数的基本定义形式如下：

```go
func functionName(parameterList) (returnType) {
    // 函数体
}
```

#### 示例：简单函数

```go
package main

import "fmt"

// 定义一个函数
func add(a int, b int) int {
    return a + b
}

func main() {
    result := add(3, 4)
    fmt.Println("Result:", result) // 输出：Result: 7
}
```

### 类型定义函数

Go 允许使用 `type` 关键字定义函数类型。这种类型定义可以用于声明函数类型变量、作为函数参数或返回值。

#### 基本语法

```go
type FunctionNameType func(parameterList) (returnType)
```

#### 示例：定义和使用函数类型

```go
package main

import "fmt"

// 定义函数类型
type IntOperation func(int, int) int

// 定义两个函数，符合 IntOperation 类型
func add(a int, b int) int {
    return a + b
}

func multiply(a int, b int) int {
    return a * b
}

func main() {
    // 使用函数类型定义的变量
    var op IntOperation

    // 将 add 函数赋值给 op
    op = add
    fmt.Println("Add:", op(3, 4)) // 输出：Add: 7

    // 将 multiply 函数赋值给 op
    op = multiply
    fmt.Println("Multiply:", op(3, 4)) // 输出：Multiply: 12
}
```

### 使用函数类型作为参数

函数类型可以作为参数传递给其他函数，这使得函数可以更加灵活和可重用。

#### 示例：函数作为参数

```go
package main

import "fmt"

// 定义函数类型
type IntOperation func(int, int) int

// 定义一个函数，接受 IntOperation 类型的参数
func compute(a int, b int, op IntOperation) int {
    return op(a, b)
}

func add(a int, b int) int {
    return a + b
}

func multiply(a int, b int) int {
    return a * b
}

func main() {
    fmt.Println("Add:", compute(3, 4, add))        // 输出：Add: 7
    fmt.Println("Multiply:", compute(3, 4, multiply)) // 输出：Multiply: 12
}
```

### 使用函数类型作为返回值

函数类型也可以作为函数的返回值，这允许我们动态选择返回的函数。

#### 示例：函数作为返回值

```go
package main

import "fmt"

// 定义函数类型
type IntOperation func(int, int) int

// 返回一个函数，根据操作类型选择函数
func getOperation(op string) IntOperation {
    switch op {
    case "add":
        return func(a int, b int) int { return a + b }
    case "multiply":
        return func(a int, b int) int { return a * b }
    default:
        return nil
    }
}

func main() {
    addOp := getOperation("add")
    multiplyOp := getOperation("multiply")

    if addOp != nil {
        fmt.Println("Add:", addOp(3, 4)) // 输出：Add: 7
    }
    if multiplyOp != nil {
        fmt.Println("Multiply:", multiplyOp(3, 4)) // 输出：Multiply: 12
    }
}
```

### 总结

在 Go 语言中，函数的定义和调用非常灵活：
- 函数可以通过标准的 `func` 关键字进行定义和调用。
- 函数可以作为类型使用，通过 `type` 关键字定义函数类型。
- 函数类型可以用作函数参数或返回值，这使得函数更加灵活和可重用。

通过这些特性，Go 语言提供了强大的函数编程能力，支持函数的高效传递和组合。