# 函数值
在 Go 里，函数是第一类对象：能赋给变量、能当参数传、能当返回值返回，高阶函数、回调都建立在这上面。

### 函数值

函数值就是函数本身的值，赋给变量之后和普通函数一样调用。

#### 定义和使用函数值

函数值有三种去向：赋给变量后直接调用；当参数传进另一个函数，让调用方决定做什么；当返回值从函数里抛出来，调用方拿到一段可执行的逻辑。下面的示例依次对应这三种。

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

接受函数参数、或返回函数的函数叫高阶函数。`createMultiplier` 就是：调一次，拿到一个绑定了 `factor` 的新函数。

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

函数值的三种去向，三个例子各占一个：`addFunc = add` 赋给变量，`compute(3, 4, add)` 当参数传，`getOperation("add")` 当返回值抛。函数类型可以自己声明，`IntOperation` 就是 `func(int, int) int` 起的别名，专用来当参数类型。