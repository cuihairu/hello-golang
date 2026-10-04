# 函数的定义和调用
在 Go 语言中，函数可以按标准的 `func` 方式定义，也可以用类型定义（type definition）创建函数类型。函数一旦成为类型，就能当值一样传递和操作。

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

函数类型可以作为参数传给其他函数：`compute` 不关心是加还是乘，具体算什么由调用方传进来的函数决定。

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

函数类型也可以作为返回值，调用方按条件拿到不同的函数，拿到之后照常调用。

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
- 函数类型可以用作函数参数或返回值。

函数当参数、当返回值传来传去，回调和策略选择就不必另起一套接口。示例里的 `IntOperation` 同时用在参数和返回值两处，写法是一样的。