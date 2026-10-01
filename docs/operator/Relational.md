在 Go 语言中，关系运算符用于比较值并确定它们之间的关系。这些运算符返回布尔值 (`true` 或 `false`)，表示比较的结果。以下是 Go 语言中的关系运算符及其用法：

### 1. 关系运算符列表

1. **等于 (`==`)**
   - **用途**：检查两个值是否相等。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 5
         result := (a == b)
         fmt.Println("a == b:", result) // 输出: a == b: true
     }
     ```

2. **不等于 (`!=`)**
   - **用途**：检查两个值是否不相等。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         result := (a != b)
         fmt.Println("a != b:", result) // 输出: a != b: true
     }
     ```

3. **大于 (`>`)**
   - **用途**：检查左边的值是否大于右边的值。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 3
         result := (a > b)
         fmt.Println("a > b:", result) // 输出: a > b: true
     }
     ```

4. **小于 (`<`)**
   - **用途**：检查左边的值是否小于右边的值。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 3
         b := 5
         result := (a < b)
         fmt.Println("a < b:", result) // 输出: a < b: true
     }
     ```

5. **大于等于 (`>=`)**
   - **用途**：检查左边的值是否大于或等于右边的值。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 5
         b := 5
         result := (a >= b)
         fmt.Println("a >= b:", result) // 输出: a >= b: true
     }
     ```

6. **小于等于 (`<=`)**
   - **用途**：检查左边的值是否小于或等于右边的值。
   - **示例**：
     ```go
     package main

     import "fmt"

     func main() {
         a := 3
         b := 5
         result := (a <= b)
         fmt.Println("a <= b:", result) // 输出: a <= b: true
     }
     ```

### 2. 示例

**示例 1：比较整数**

```go
package main

import "fmt"

func main() {
    x := 10
    y := 20

    fmt.Println("x == y:", x == y)  // 输出: x == y: false
    fmt.Println("x != y:", x != y)  // 输出: x != y: true
    fmt.Println("x > y:", x > y)    // 输出: x > y: false
    fmt.Println("x < y:", x < y)    // 输出: x < y: true
    fmt.Println("x >= y:", x >= y)  // 输出: x >= y: false
    fmt.Println("x <= y:", x <= y)  // 输出: x <= y: true
}
```

**示例 2：比较字符串**

```go
package main

import "fmt"

func main() {
    str1 := "hello"
    str2 := "world"

    fmt.Println("str1 == str2:", str1 == str2)  // 输出: str1 == str2: false
    fmt.Println("str1 != str2:", str1 != str2)  // 输出: str1 != str2: true
    fmt.Println("str1 > str2:", str1 > str2)    // 输出: str1 > str2: false
    fmt.Println("str1 < str2:", str1 < str2)    // 输出: str1 < str2: true
}
```

### 3. 总结

- **关系运算符** 用于比较值之间的关系。
- 包括：
  - 等于 (`==`)
  - 不等于 (`!=`)
  - 大于 (`>`)
  - 小于 (`<`)
  - 大于等于 (`>=`)
  - 小于等于 (`<=`)
- 关系运算符返回布尔值 (`true` 或 `false`)，表示比较的结果。

理解这些关系运算符有助于在 Go 程序中进行条件判断和控制流。