# 控制流语句

控制流语句决定了程序语句的执行顺序。与很多语言不同，Go 移除了 `while`、`do-while` 等循环语法，只保留 `for` 作为唯一的循环语句，同时提供了完整的条件判断、跳转语句，让控制流保持简单统一。

## Go 控制流的三大类

Go 的控制流语句可以分为三类：

| 类别 | 语句 | 说明 |
| --- | --- | --- |
| 条件语句 | `if`、`switch` | 根据条件选择执行的分支 |
| 循环语句 | `for`（含 `range`） | 重复执行一段代码 |
| 跳转语句 | `break`、`continue`、`goto` | 改变循环或分支的跳转方向 |

## 条件语句

`if` 语句根据布尔表达式的值选择执行路径，支持在条件前携带初始化语句；`switch` 语句是多路分支的简化写法，还可以进行类型判断。

```go
package main

import "fmt"

func classify(n int) string {
    if n < 0 {
        return "negative"
    } else if n == 0 {
        return "zero"
    }
    return "positive"
}

func main() {
    x := -5
    fmt.Println(x, classify(x))

    switch day := x % 3; {
    case day == 0:
        fmt.Println("余数为 0")
    case day < 0:
        fmt.Println("余数为负数")
    }
}
```

## 循环语句

`for` 循环是 Go 中唯一的循环结构，它可以省略初始化、条件或后置语句中的任意部分，甚至三个全部省略形成无限循环。配合 `range` 关键字，可以遍历切片、数组、字符串、map 和通道。

```go
package main

import "fmt"

func main() {
    // 三段式
    for i := 0; i < 3; i++ {
        fmt.Println("i =", i)
    }

    // range 遍历切片
    nums := []int{10, 20, 30}
    for idx, v := range nums {
        fmt.Println(idx, v)
    }

    // 无限循环配合 break
    n := 0
    for {
        n++
        if n >= 3 {
            break
        }
    }
    fmt.Println("n =", n)
}
```

## 跳转语句

`break` 跳出循环或 `switch`，`continue` 跳过本次迭代进入下一次，`goto` 跳转到同一函数内的标签处。`break` 和 `continue` 还可以配合标签使用，从而控制多层嵌套的循环。

```go
package main

import "fmt"

func main() {
outer:
    for i := 0; i < 4; i++ {
        for j := 0; j < 4; j++ {
            if i*j >= 6 {
                break outer // 直接跳出最外层循环
            }
            if j == 2 {
                continue // 只跳过内层本次迭代
            }
            fmt.Println(i, j)
        }
    }
}
```

## 建议

- 优先使用 `if`、`for`、`switch` 这些结构化语句，`goto` 只在需要统一跳转到函数内清理逻辑等少数场景下使用。
- Go 不强制在条件表达式外加括号，`gofmt` 会自动省略多余的括号。
- 分支语句不使用 `fallthrough` 时会自动跳出，需要显式贯穿时再用 `fallthrough`。

本章后续小节将分别展开讲解条件语句、循环语句和跳转语句的具体用法。
