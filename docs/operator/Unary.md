在 Go 语言中，一元运算符是作用于单个操作数的运算符。以下是 Go 语言中的一元运算符及其用法：

### 1. 正号（`+`）

- **用途**：表示操作数的正值。
- **示例**：
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      result := +a
      fmt.Println("+a:", result) // 输出: +a: 5
  }
  ```

### 2. 负号（`-`）

- **用途**：表示操作数的负值，即对操作数取相反数。
- **示例**：
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      result := -a
      fmt.Println("-a:", result) // 输出: -a: -5
  }
  ```

### 3. 取反（`^`）

- **用途**：对操作数进行按位取反（即所有位取反），仅对整数类型有效。
- **示例**：
  ```go
  package main

  import "fmt"

  func main() {
      a := 12 // 二进制: 1100
      result := ^a
      fmt.Println("^a:", result) // 输出: ^a: -13（按位取反后再取补码）
  }
  ```

### 4. 自增（`++`）

- **用途**：将操作数的值增加 1。自增运算符只能用于变量，并且不能用于表达式中。
- **示例**：
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      a++
      fmt.Println("a++:", a) // 输出: a++: 6
  }
  ```

### 5. 自减（`--`）

- **用途**：将操作数的值减少 1。自减运算符只能用于变量，并且不能用于表达式中。
- **示例**：
  ```go
  package main

  import "fmt"

  func main() {
      a := 5
      a--
      fmt.Println("a--:", a) // 输出: a--: 4
  }
  ```

### 6. 逻辑非（`!`）

- **用途**：对操作数进行逻辑非操作，将 `true` 转为 `false`，将 `false` 转为 `true`。
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

### 总结

这六个运算符都作用于单个操作数：`+`、`-`、`^`、`!` 可以出现在表达式里，`++` 和 `--` 只能单独成句，不能写在表达式中。
