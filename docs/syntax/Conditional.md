# 条件语句

条件语句根据布尔表达式的值来选择要执行的代码分支。Go 提供了两种条件语句：`if` 和 `switch`，两者都属于条件语句的范畴。

## `if` 语句

`if` 语句是最基本的条件判断结构，条件表达式不需要使用括号包裹，分支必须使用花括号。

```go
package main

import "fmt"

func main() {
    age := 20

    if age >= 18 {
        fmt.Println("成年")
    }

    if age >= 18 {
        fmt.Println("成年")
    } else if age >= 12 {
        fmt.Println("少年")
    } else {
        fmt.Println("儿童")
    }
}
```

`if` 还支持在条件前写一条初始化语句，用分号隔开。初始化语句中声明的变量作用域覆盖整个 `if`/`else` 块，这是 Go 中处理错误最惯用的写法：

```go
package main

import (
    "errors"
    "fmt"
)

func find() (int, error) {
    return 0, errors.New("not found")
}

func main() {
    if v, err := find(); err != nil {
        fmt.Println("出错:", err)
    } else {
        fmt.Println("结果:", v)
    }
}
```

`if` 语句的详细用法见 [if](If.md)。

## `switch` 语句

`switch` 是多路分支语句，它把对同一个表达式的多次比较集中到一个块中，避免深层嵌套的 `if-else if`。Go 的 `switch` 有三个重要特性：

- 命中一个 `case` 后自动跳出，不会贯穿到下一个 `case`（需要贯穿时显式使用 `fallthrough`）。
- `case` 中可以列出多个匹配值，用逗号分隔。
- 可以省略 `switch` 的表达式，等价于 `switch true`，此时 `case` 写条件表达式。

```go
package main

import "fmt"

func main() {
    score := 85

    switch {
    case score >= 90:
        fmt.Println("A")
    case score >= 80:
        fmt.Println("B")
    default:
        fmt.Println("C 及以下")
    }

    switch day := 3; day {
    case 1, 2, 3, 4, 5:
        fmt.Println("工作日")
    case 6, 7:
        fmt.Println("周末")
    }

    // 类型 switch：判断接口值的实际类型
    var i interface{} = "hello"
    switch v := i.(type) {
    case int:
        fmt.Println("int:", v)
    case string:
        fmt.Println("string:", v)
    }
}
```

`switch` 的详细用法见 [switch](Switch.md)。

## 与 `select` 的区别

`switch` 用于一般条件的多路分支，`select` 则专门用于通道通信的多路选择，语法上与 `switch` 相似，但 `case` 中只能出现通道操作，且由运行时选择就绪的分支。两者的详细对比见 [switch](Switch.md)。
