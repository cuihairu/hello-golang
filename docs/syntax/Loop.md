# 循环语句

循环语句用于重复执行一段代码。Go 只有一种循环语句——`for`，但通过省略其中的组成部分，它可以覆盖 `while`、`do-while`、无限循环等所有场景。

## 三段式 `for`

最常见的写法由初始化语句、条件表达式和后置语句三部分组成，用分号分隔：

```go
package main

import "fmt"

func main() {
    sum := 0
    for i := 1; i <= 100; i++ {
        sum += i
    }
    fmt.Println("1 到 100 的和:", sum)
}
```

初始化语句和后置语句都可以省略，省略后分号也可以不写，此时与 `while` 等价：

```go
package main

import "fmt"

func main() {
    n := 1
    for n < 100 {
        n *= 2
    }
    fmt.Println(n)
}
```

三个部分全部省略就是无限循环，需要配合 `break`、`return` 或 `panic` 退出：

```go
package main

import "fmt"

func main() {
    count := 0
    for {
        count++
        if count%2 == 0 {
            continue
        }
        if count > 5 {
            break
        }
        fmt.Println(count)
    }
}
```

## `for range` 遍历

`range` 用于遍历数组、切片、字符串、map 和通道。不同集合返回的迭代变量不同：

| 集合类型 | 第一个值 | 第二个值 |
| --- | --- | --- |
| 数组、切片、字符串 | 索引 | 元素副本 |
| map | 键 | 值 |
| 通道 | 元素 | - |
| 整数（Go 1.22+） | 0..n-1 | - |

```go
package main

import "fmt"

func main() {
    nums := []int{10, 20, 30}
    for i, v := range nums {
        fmt.Println(i, v)
    }

    // 只需要索引或键
    for i := range nums {
        fmt.Println(i)
    }

    // 只需要值，用空白标识符忽略索引
    sum := 0
    for _, v := range nums {
        sum += v
    }
    fmt.Println(sum)

    m := map[string]int{"a": 1, "b": 2}
    for k, v := range m {
        fmt.Println(k, v)
    }

    // 遍历字符串时按 UTF-8 码点迭代
    for i, r := range "Go语言" {
        fmt.Printf("%d %q\n", i, r)
    }
}
```

## 循环变量的作用域

在 Go 1.22 之前，循环变量在整个循环中共享同一个实例，闭包和协程中直接引用会得到意外结果；Go 1.22 起每次迭代都会创建新的变量实例。跨版本兼容的写法是在循环体内显式复制：

```go
package main

import (
    "fmt"
    "sync"
)

func main() {
    var wg sync.WaitGroup
    for i := 0; i < 3; i++ {
        wg.Add(1)
        i := i // 复制一份循环变量，兼容所有版本
        go func() {
            defer wg.Done()
            fmt.Println(i)
        }()
    }
    wg.Wait()
}
```

## 循环与 `break`、`continue`

`break` 立即终止所在循环，`continue` 跳过本次迭代剩余语句、直接进入下一轮。两者都可以带标签，从而作用于外层循环：

```go
package main

import "fmt"

func main() {
outer:
    for i := 1; i <= 3; i++ {
        for j := 1; j <= 3; j++ {
            if j > i {
                continue outer // 直接开始外层下一轮
            }
            if i*j == 6 {
                break outer // 直接结束外层循环
            }
            fmt.Printf("%d*%d=%d ", i, j, i*j)
        }
        fmt.Println()
    }
}
```

详细说明见 [for](For.md)、[break](Break.md) 和 [continue](Continue.md)。
