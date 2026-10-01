# 函数值
在 Go 语言中，函数是第一类对象，这意味着函数可以被赋值给变量、传递作为参数以及作为返回值返回。这种特性使得函数非常灵活，可以用于实现高阶函数、回调以及策略模式等。下面我们详细介绍 Go 中的函数值及其用法。

### 函数值

函数值是指函数的引用。Go 允许你将函数赋值给变量，传递函数作为参数，以及从函数中返回函数。这样可以实现很多有趣的编程模式和技术。

#### 定义和使用函数值

1. **定义函数值**：
   - 定义函数并将其赋值给变量。
   - 调用函数变量就像调用普通函数一样。

2. **函数值作为参数**：
   - 将函数值作为参数传递给其他函数。

3. **函数值作为返回值**：
   - 从函数中返回另一个函数值。

### 示例：基本用法

#### 定义函数值

```go
package main

import "fmt"

// 定义一个函数
func add(a int, b int) int {
    return a + b
}

func main() {
    // 将函数赋值给变量
    var addFunc func(int, int) int
    addFunc = add

    // 调用函数值
    result := addFunc(3, 4)
    fmt.Println("Result:", result) // 输出：Result: 7
}
```

#### 函数值作为参数

```go
package main

import "fmt"

// 定义函数类型
type IntOperation func(int, int) int

// 函数接收函数值作为参数
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

#### 函数值作为返回值

```go
package main

import "fmt"

// 返回一个函数值
func getOperation(op string) func(int, int) int {
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

### 高阶函数

函数值允许我们实现高阶函数，这些函数可以接受其他函数作为参数，或返回其他函数。高阶函数可以用于实现更加灵活和可扩展的代码。

#### 示例：高阶函数

```go
package main

import "fmt"

// 定义高阶函数
func createMultiplier(factor int) func(int) int {
    return func(value int) int {
        return value * factor
    }
}

func main() {
    // 创建一个乘以 2 的函数
    double := createMultiplier(2)
    // 创建一个乘以 10 的函数
    tenTimes := createMultiplier(10)

    fmt.Println("Double 3:", double(3))     // 输出：Double 3: 6
    fmt.Println("Ten times 3:", tenTimes(3)) // 输出：Ten times 3: 30
}
```

### 总结

- **函数值**：在 Go 中，函数可以赋值给变量、作为参数传递以及作为返回值返回，这使得函数值非常灵活。
- **函数作为参数**：可以将函数值作为参数传递给其他函数，以实现更多功能。
- **函数作为返回值**：可以从函数中返回另一个函数值，从而创建更加动态的功能。
- **高阶函数**：利用函数值，可以实现高阶函数，创建更加灵活和可扩展的代码。

这些特性使得 Go 中的函数值非常强大，能够支持许多编程模式和技术。