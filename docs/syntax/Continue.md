# continue
### Go 中的 `continue` 详解

在 Go 语言中，`continue` 语句用于跳过当前循环迭代中剩余的语句，直接进入下一次循环迭代。它可以在 `for` 循环、`switch` 语句中的 `case` 语句块中使用，且常用于跳过某些条件下的处理逻辑。

### 1. 基本用法

`continue` 语句的基本用法是在循环体中使用，它会跳过循环体中 `continue` 之后的代码，直接进入下一次迭代。

**示例：基本用法**

```go
package main

import "fmt"

func main() {
    for i := 1; i <= 5; i++ {
        if i == 3 {
            continue // 跳过当前迭代
        }
        fmt.Println(i)
    }
}
```

**输出：**

```
1
2
4
5
```

在这个示例中，当 `i` 等于 3 时，`continue` 语句被触发，当前迭代被跳过，因此数字 3 没有被打印出来。

### 2. 在嵌套循环中的使用

`continue` 语句会影响当前循环层级，不会跳过外层的循环。

**示例：嵌套循环中的 `continue`**

```go
package main

import "fmt"

func main() {
    for i := 1; i <= 3; i++ {
        for j := 1; j <= 3; j++ {
            if j == 2 {
                continue // 跳过当前内层循环的当前迭代
            }
            fmt.Printf("i = %d, j = %d\n", i, j)
        }
    }
}
```

**输出：**

```
i = 1, j = 1
i = 1, j = 3
i = 2, j = 1
i = 2, j = 3
i = 3, j = 1
i = 3, j = 3
```

在这个示例中，当 `j` 等于 2 时，`continue` 跳过了内层循环的当前迭代，`j = 2` 的情况没有被打印。

### 3. `continue` 与标签（Label）的配合使用

`continue` 语句可以与标签（Label）一起使用，以跳过外层循环的当前迭代。

**示例：使用标签**

```go
package main

import "fmt"

func main() {
    OuterLoop:
    for i := 1; i <= 3; i++ {
        for j := 1; j <= 3; j++ {
            if j == 2 {
                continue OuterLoop // 跳过外层循环的当前迭代
            }
            fmt.Printf("i = %d, j = %d\n", i, j)
        }
    }
}
```

**输出：**

```
i = 1, j = 1
i = 2, j = 1
i = 3, j = 1
```

在这个示例中，`continue OuterLoop` 语句会跳过外层循环的当前迭代。当 `j` 等于 2 时，整个外层循环（包括当前 `i` 的值）会跳过，直接进入下一次外层循环的迭代。

### 4. `continue` 与 `break` 的比较

- **`continue`**：跳过当前循环的剩余部分，继续执行下一次循环迭代。
- **`break`**：终止整个循环，不再进行任何迭代。

**示例：`continue` 和 `break` 的比较**

```go
package main

import "fmt"

func main() {
    fmt.Println("Using continue:")
    for i := 1; i <= 3; i++ {
        if i == 2 {
            continue
        }
        fmt.Println(i)
    }

    fmt.Println("\nUsing break:")
    for i := 1; i <= 3; i++ {
        if i == 2 {
            break
        }
        fmt.Println(i)
    }
}
```

**输出：**

```
Using continue:
1
3

Using break:
1
```

### 5. `continue` 的底层实现

Go 的 `continue` 语句在底层实现中，通常涉及到以下步骤：
- **跳转到循环的条件检查**：`continue` 语句会使程序跳转到循环体的起始部分，重新进行条件检查。
- **更新循环变量**：在跳过当前迭代后，程序会根据循环变量的更新规则进行下一次迭代。

**汇编代码示例**

在 Go 的汇编代码中，`continue` 的实现通常涉及到将程序计数器（PC）跳转到循环条件检查的位置。以下是一个简化的汇编代码示例（以 `amd64` 架构为例）：

```assembly
TEXT main.loop(SB), NOSPLIT, $0
    MOVQ    8(SP), CX         // 获取循环变量
    CMPQ    $2, CX            // 检查循环条件
    JGE     endLoop           // 如果条件满足，跳转到循环结束
    JMP     continueLoop      // 跳转到循环条件检查

continueLoop:
    // 继续下次循环
    RET

endLoop:
    // 循环结束
    RET
```

### 总结

- **`continue` 语句**：用于跳过当前循环的剩余部分，直接进入下一次循环迭代。
- **使用场景**：适用于需要跳过某些条件下的处理逻辑的情况。
- **标签**：可以与标签结合使用，跳过外层循环的当前迭代。
- **`continue` 与 `break`**：`continue` 跳过当前迭代，`break` 终止整个循环。
- **底层实现**：通过跳转到循环条件检查位置来实现，涉及到程序计数器的跳转。

通过了解 `continue` 的使用和底层实现，你可以更灵活地控制循环的执行流程，编写高效和可读性强的代码。