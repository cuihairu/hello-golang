# 跳转语句

跳转语句用于改变程序的执行顺序。Go 提供了 `break`、`continue` 和 `goto` 三种跳转语句，它们可以配合标签（label）实现更精细的控制。

## `break`

`break` 用于立即终止所在的 `for` 循环、`switch` 或 `select` 语句。注意：在嵌套于 `for` 的 `switch`/`select` 中，不带标签的 `break` 只跳出 `switch`/`select` 本身。

```go
package main

import "fmt"

func main() {
    for i := 0; i < 10; i++ {
        if i == 5 {
            break
        }
        fmt.Println(i)
    }
}
```

配合标签可以一次跳出多层循环：

```go
package main

import "fmt"

func main() {
outer:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                break outer
            }
            fmt.Println(i, j)
        }
    }
    fmt.Println("结束")
}
```

详见 [break](Break.md)。

## `continue`

`continue` 用于跳过本轮循环中剩余的语句，直接进入下一轮迭代。它同样支持标签：

```go
package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ {
        if i%2 == 0 {
            continue
        }
        fmt.Println(i)
    }
}
```

详见 [continue](Continue.md)。

## `goto`

`goto` 无条件跳转到同一函数内的标签处。Go 对 `goto` 有两条硬性限制：

- 不能跳转到其他函数，也不能跨函数跳转。
- 不能跳过标签之前的变量声明，否则编译报错 "jumps over declaration"。

```go
package main

import "fmt"

func main() {
    i := 0
loop:
    if i < 3 {
        fmt.Println(i)
        i++
        goto loop
    }
    fmt.Println("结束")
}
```

`goto` 会让控制流难以追踪，日常代码中应优先使用 `break`、`continue` 或 `return`，仅在少数需要集中错误清理逻辑的场景下考虑使用。

详见 [goto](Goto.md)。

## 标签

标签是一个紧跟冒号的标识符，用于标记语句的位置，可以被 `break`、`continue` 和 `goto` 引用。标签只在定义它的函数内有效，未被引用的标签会被编译器忽略（`go vet` 会给出提示）。

```go
package main

import "fmt"

func main() {
done:
    for i := 0; i < 3; i++ {
        fmt.Println(i)
        if i == 1 {
            break done
        }
    }
}
```
