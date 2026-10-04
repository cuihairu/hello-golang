# 匿名函数和闭包
匿名函数和闭包经常一起出现，但不是一回事：前者是没有名字的函数，后者是带着外部变量的函数值。下面分开看写法，再看怎么配合。

### 匿名函数

**匿名函数**（Anonymous Functions）是没有名字的函数，通常用在一次性场景：作为参数传递，或就地定义回调。

#### 语法

```go
func(parameter_list) return_type {
    // function body
}
```

#### 示例：基本用法

```go
package main

import "fmt"

func main() {
    // 定义一个匿名函数并立即调用它
    func(message string) {
        fmt.Println(message)
    }("Hello, World!")
}
```

在这个例子中，匿名函数被定义并立即调用。它接收一个参数 `message` 并打印它。

### 闭包

**闭包**（Closure）是一个函数值，它引用了外部作用域的变量。即使定义它的函数已经返回，闭包仍然能读写当初捕获的变量。

#### 特性

- 闭包能捕获并修改创建时所在作用域的变量，原函数返回后这些变量依然存活。

#### 示例：基本用法

```go
package main

import "fmt"

// 返回一个闭包
func createCounter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

func main() {
    // 创建一个闭包
    counter := createCounter()
    
    // 调用闭包
    fmt.Println(counter()) // 输出：1
    fmt.Println(counter()) // 输出：2
    fmt.Println(counter()) // 输出：3
}
```

在这个例子中，`createCounter` 函数返回一个闭包，这个闭包捕获了 `count` 变量。每次调用闭包时，它会修改并返回 `count` 的值。

### 匿名函数和闭包的结合

匿名函数可以用来创建闭包，这是它们的一个常见用法。

#### 示例：结合使用匿名函数和闭包

```go
package main

import "fmt"

func main() {
    // 定义一个闭包，使用匿名函数
    multiplier := func(factor int) func(int) int {
        return func(value int) int {
            return value * factor
        }
    }

    // 创建一个闭包，乘以 2
    double := multiplier(2)
    // 创建一个闭包，乘以 10
    tenTimes := multiplier(10)

    fmt.Println("Double 3:", double(3))     // 输出：Double 3: 6
    fmt.Println("Ten times 3:", tenTimes(3)) // 输出：Ten times 3: 30
}
```

在这个例子中，`multiplier` 是一个匿名函数，它返回一个闭包。闭包捕获了 `factor` 变量，从而允许 `double` 和 `tenTimes` 使用不同的乘数进行计算。

### 总结

- **匿名函数**：没有名字的函数，通常用于一次性任务或作为回调函数。
- **闭包**：函数值能够捕获和修改其外部作用域的变量。闭包在函数返回后仍能访问这些捕获的变量。

`createCounter` 那个例子就是闭包的典型用法：函数返回了，`count` 还活着，每次调用 `counter()` 都在上一次的基础上加一。