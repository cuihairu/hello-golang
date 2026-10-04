标签（Labels）在 Go 语言中用于标记代码的位置，供 `break`、`continue` 和 `goto` 跳转。它主要用在多层嵌套的循环里，让内层能直接跳出或跳过外层。

### 标签的基本语法

标签的语法是在标签名后加上冒号（`:`），然后是代码块。标签通常放置在 `for` 循环、`switch` 语句或 `select` 语句的前面。标签名可以是任何合法的标识符，通常以小写字母开头。

#### 标签的语法示例

```go
LabelName:
    // 代码块
```

### 标签与 `break`

标签与 `break` 语句结合使用时，可以跳出多层嵌套的循环或 `switch` 语句。`break` 语句跳出的是最近的循环或 `switch` 语句，标签可以用来指定具体要跳出的循环或 `switch`。

#### 示例：使用标签跳出多层循环

```go
package main

import "fmt"

func main() {
    OuterLoop:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                break OuterLoop
            }
            fmt.Println(i, j)
        }
    }
}
```

**输出：**

```
0 0
0 1
0 2
1 0
```

在这个示例中，`break OuterLoop` 语句跳出标记为 `OuterLoop` 的外层 `for` 循环。当 `i` 等于 1 且 `j` 等于 1 时，`break` 语句触发，外层循环立即终止。

### 标签与 `continue`

`continue` 语句用于跳过当前循环的剩余部分并开始下一次循环迭代。`continue` 可以与标签结合使用，以跳过外层循环的当前迭代。

#### 示例：使用标签跳过外层循环的当前迭代

```go
package main

import "fmt"

func main() {
    OuterLoop:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                continue OuterLoop
            }
            fmt.Println(i, j)
        }
    }
}
```

**输出：**

```
0 0
0 1
0 2
1 0
2 0
2 1
2 2
```

在这个示例中，`continue OuterLoop` 语句跳过外层 `for` 循环的当前迭代。当 `i` 等于 1 且 `j` 等于 1 时，`continue` 语句使程序跳过当前的 `OuterLoop` 迭代，继续执行下一个 `OuterLoop` 迭代。

### 标签与 `goto`

`goto` 语句用于无条件跳转到程序中指定的标签。`goto` 可以跳转到同一函数中的任何标签，但应谨慎使用，以避免代码混乱和维护困难。

#### 示例：使用 `goto` 跳转到标签

```go
package main

import "fmt"

func main() {
    i := 0
    Start:
    fmt.Println(i)
    i++
    if i < 5 {
        goto Start
    }
}
```

**输出：**

```
0
1
2
3
4
```

在这个示例中，`goto Start` 语句使程序跳回到 `Start` 标签，从而实现了一个简单的循环。

### 标签的使用注意事项

1. **代码可读性**：标签和 `goto` 用多了，读代码的人要来回翻才能找到跳转目标。标签留给多层 `for` 嵌套这类场景就够了。

2. **避免复杂控制流**：几个标签交叉跳转的控制流很难跟踪，能靠提前返回、函数拆分解决的就不要上标签。

### 总结

- **标签（Labels）**：标记程序中的位置，配合 `break`、`continue` 和 `goto` 使用。
- **`break`**：带标签时直接跳出多层嵌套的循环或 `switch`。
- **`continue`**：带标签时跳过外层循环的当前迭代。
- **`goto`**：无条件跳到指定标签，同一个函数内有效。