在 Go 语言中，算术运算符执行基本的数学操作，作用于整数、浮点数等基本类型：

### 1. 算术运算符列表

1. **加法运算符 (`+`)**
   - **用途**：计算两个数的和。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         sum := a + b
         fmt.Println("Sum:", sum) // 输出: Sum: 8
     }
     ```

2. **减法运算符 (`-`)**
   - **用途**：计算两个数的差。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         difference := a - b
         fmt.Println("Difference:", difference) // 输出: Difference: 2
     }
     ```

3. **乘法运算符 (`*`)**
   - **用途**：计算两个数的乘积。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         product := a * b
         fmt.Println("Product:", product) // 输出: Product: 15
     }
     ```

4. **除法运算符 (`/`)**
   - **用途**：计算两个数的商。对于整数除法，结果会向零取整（舍去小数部分，例如 `-10 / 3` 的结果是 `-3`）；对于浮点数除法，会得到精确的结果。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 10
         b := 3
         quotient := a / b
         fmt.Println("Quotient:", quotient) // 输出: Quotient: 3

         x := 10.0
         y := 3.0
         floatQuotient := x / y
         fmt.Println("Float Quotient:", floatQuotient) // 输出: Float Quotient: 3.3333333333333335
     }
     ```

5. **取余运算符 (`%`)**
   - **用途**：计算两个数相除后的余数。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 10
         b := 3
         remainder := a % b
         fmt.Println("Remainder:", remainder) // 输出: Remainder: 1
     }
     ```

6. **自增运算符 (`++`)**
   - **用途**：将变量的值增加1。只能用于变量，不能用于常量。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         x := 5
         x++
         fmt.Println("x after increment:", x) // 输出: x after increment: 6
     }
     ```

7. **自减运算符 (`--`)**
   - **用途**：将变量的值减少1。只能用于变量，不能用于常量。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         y := 5
         y--
         fmt.Println("y after decrement:", y) // 输出: y after decrement: 4
     }
     ```

### 2. 运算符优先级

在 Go 中，运算符的优先级决定了表达式中运算符的执行顺序。算术运算符的优先级相对较高，但低于括号和一些其他运算符（如逻辑运算符）。常见的顺序从高到低：

1. 括号 `()`
2. 乘法 `*`、除法 `/` 和取余 `%`
3. 加法 `+` 和减法 `-`

注意：自增 `++` 和自减 `--` 在 Go 中是**语句**而不是运算符，不能出现在表达式里，因此不参与优先级的比较。

### 3. 示例

**示例 1：优先级的影响**

```go
package main

import "fmt"

func main() {
    a := 5
    b := 3
    c := 2
    result := a + b * c // 先计算 b * c，然后加上 a
    fmt.Println("Result:", result) // 输出: Result: 11
}
```

在这个示例中，`b * c` 会先被计算，然后将结果加上 `a`，即 `5 + (3 * 2) = 11`。

**示例 2：自增和自减运算**

在 Go 中，`++` 和 `--` 是语句，不能像 C/Java 那样作为表达式的一部分使用（`y := x++` 或 `w := --z` 都是非法代码）。如果需要“先取值、再自增（或自减）”的语义，可以写成两条语句：

```go
package main

import "fmt"

func main() {
    x := 10
    y := x // 先取 x 的值
    x++    // 再自增
    fmt.Println("x:", x) // 输出: x: 11
    fmt.Println("y:", y) // 输出: y: 10

    z := 10
    w := z // 先取 z 的值
    z--    // 再自减
    fmt.Println("z:", z) // 输出: z: 9
    fmt.Println("w:", w) // 输出: w: 10
}
```

在这个示例中，`y` 保存的是 `x` 自增之前的值 10，`w` 保存的是 `z` 自减之前的值 10。

### 4. 总结

- **算术运算符** 是用于执行基本数学操作的工具，包括加法、减法、乘法、除法、取余、自增和自减。
- **优先级** 决定了在复杂表达式中运算符的执行顺序。
- **自增和自减** 运算符用于将变量的值增加或减少1。

记两条容易踩的：整数除法向零取整，`++` 和 `--` 是语句，不是运算符。