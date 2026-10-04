在 Go 语言中，逻辑运算符用于进行布尔值的逻辑运算。它们主要用于控制流判断和条件测试。以下是 Go 语言中的逻辑运算符及其用法：

### 1. 逻辑运算符列表

1. **逻辑与 (`&&`)**
   - **用途**：当且仅当两个操作数都为 `true` 时，结果为 `true`。如果第一个操作数为 `false`，则不会再计算第二个操作数（短路行为）。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := true
         b := false
         result := a && b
         fmt.Println("a && b:", result) // 输出: a && b: false
     }
     ```

2. **逻辑或 (`||`)**
   - **用途**：当两个操作数中至少有一个为 `true` 时，结果为 `true`。如果第一个操作数为 `true`，则不会再计算第二个操作数（短路行为）。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := true
         b := false
         result := a || b
         fmt.Println("a || b:", result) // 输出: a || b: true
     }
     ```

3. **逻辑非 (`!`)**
   - **用途**：将布尔值取反，即如果操作数为 `true`，则结果为 `false`，反之亦然。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := true
         result := !a
         fmt.Println("!a:", result) // 输出: !a: false
     }
     ```

### 2. 示例

**示例 1：组合使用逻辑运算符**

```go
package main

import "fmt"

func main() {
    x := 10
    y := 20
    z := 30

    // 逻辑与和逻辑或的组合
    result1 := (x < y) && (y < z)  // true && true = true
    result2 := (x > y) || (y < z)  // false || true = true

    fmt.Println("result1:", result1) // 输出: result1: true
    fmt.Println("result2:", result2) // 输出: result2: true
}
```

**示例 2：短路行为**

注意：`1/0` 是常量表达式，Go 在编译阶段就会报 `division by zero` 错误，根本无法通过编译；下面用一个函数来演示运行时的短路行为：

```go
package main

import "fmt"

func checkDiv(n int) bool {
    // 演示短路行为：使用安全的条件避免除以零
    // 当 n 不为 0 时，返回 true；否则返回 false
    // 这样可以演示 && 和 || 的短路行为，而不会触发 panic
    return n != 0
}

func main() {
    a := false
    b := true

    // 短路行为：&& 左侧为 false 时，右侧的 checkDiv 不会被调用，
    // 因此避免了除以零的 panic
    result1 := a && checkDiv(1)
    // || 左侧为 true 时同理，右侧的 checkDiv 不会被调用
    result2 := b || checkDiv(1)

    fmt.Println("result1:", result1) // 输出: result1: false
    fmt.Println("result2:", result2) // 输出: result2: true
}
```

### 3. 总结

- **逻辑运算符** 用于布尔值的逻辑操作，主要有：
  - 逻辑与 (`&&`): 仅当两个操作数都为 `true` 时，结果为 `true`。
  - 逻辑或 (`||`): 只要有一个操作数为 `true`，结果为 `true`。
  - 逻辑非 (`!`): 将布尔值取反。
- 逻辑运算符具有短路行为，即在某些情况下避免计算第二个操作数，从而提高效率或避免错误。

`&&` 和 `||` 的短路行为是有语言保证的：右侧表达式只有需要时才会求值，依赖这一点写的保护判断是安全的。
