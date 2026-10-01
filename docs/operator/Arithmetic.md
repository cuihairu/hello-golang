在 Go 语言中，算术运算符用于执行基本的数学操作。这些运算符可以作用于整数、浮点数等基本数据类型。以下是 Go 语言中的算术运算符及其用法：

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
   - **用途**：计算两个数的商。对于整数除法，会向下取整；对于浮点数除法，会得到精确的结果。
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

在 Go 中，运算符的优先级决定了表达式中运算符的执行顺序。算术运算符的优先级相对较高，但低于括号和一些其他运算符（如逻辑运算符）。以下是常见的算术运算符的优先级从高到低的顺序：

1. 括号 `()`
2. 自增 `++` 和自减 `--`
3. 乘法 `*`、除法 `/` 和取余 `%`
4. 加法 `+` 和减法 `-`

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

```go
package main

import "fmt"

func main() {
    x := 10
    y := x++
    fmt.Println("x:", x) // 输出: x: 11
    fmt.Println("y:", y) // 输出: y: 10

    z := 10
    w := --z
    fmt.Println("z:", z) // 输出: z: 9
    fmt.Println("w:", w) // 输出: w: 9
}
```

在这个示例中，`x++` 表示先使用 `x` 的值然后再自增，而 `--z` 表示先自减 `z` 的值然后再使用。

### 4. 总结

- **算术运算符** 是用于执行基本数学操作的工具，包括加法、减法、乘法、除法、取余、自增和自减。
- **优先级** 决定了在复杂表达式中运算符的执行顺序。
- **自增和自减** 运算符用于将变量的值增加或减少1。

理解 Go 语言中的算术运算符及其优先级有助于编写准确、高效的代码。通过掌握这些基本运算符，你可以更好地处理各种数学计算和数据操作。