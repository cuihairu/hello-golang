### 2. 数学函数

Go 语言的 `math` 包提供了常用的数学函数，覆盖绝对值、幂运算、三角函数、对数等。本节按用途分组，列出每个函数的用法和输出。

---

#### 2.1 常用数学函数

**2.1.1 绝对值（`math.Abs`）**

`math.Abs` 函数返回一个数值的绝对值，即去掉负号后的非负值。距离、误差这类计算里经常用到。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("绝对值:", math.Abs(-3.14))  // 输出: 3.14
  }
  ```

**2.1.2 幂运算（`math.Pow`）**

`math.Pow` 函数用于计算一个数的指定幂。它返回 `x` 的 `y` 次幂。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("幂运算:", math.Pow(2, 3))  // 输出: 8
  }
  ```

**2.1.3 平方根（`math.Sqrt`）**

`math.Sqrt` 函数计算一个数的平方根。平方根用于解决平方相关的数学问题，如几何计算和方程求解。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("平方根:", math.Sqrt(16))  // 输出: 4
  }
  ```

**2.1.4 三角函数（`math.Sin`, `math.Cos`, `math.Tan`）**

- **`math.Sin`**：计算角度的正弦值。
- **`math.Cos`**：计算角度的余弦值。
- **`math.Tan`**：计算角度的正切值。

这些三角函数用于处理周期性现象和角度相关的计算。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      angle := math.Pi / 4  // 45 度
      fmt.Println("正弦:", math.Sin(angle))  // 输出: 0.7071067811865475
      fmt.Println("余弦:", math.Cos(angle))  // 输出: 0.7071067811865476
      fmt.Println("正切:", math.Tan(angle))  // 输出: 1
  }
  ```

**2.1.5 指数函数（`math.Exp`）**

`math.Exp` 函数计算自然对数的底 `e` 的 `x` 次幂。它用于处理指数增长等数学模型。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("指数函数:", math.Exp(2))  // 输出: 7.38905609893065
  }
  ```

**2.1.6 对数函数（`math.Log`, `math.Log10`）**

- **`math.Log`**：计算自然对数（底为 `e`）的对数。
- **`math.Log10`**：计算以 10 为底的对数。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("自然对数:", math.Log(10))    // 输出: 2.302585092994046
      fmt.Println("常用对数:", math.Log10(100))  // 输出: 2
  }
  ```

**2.1.7 双曲函数（`math.Sinh`, `math.Cosh`, `math.Tanh`）**

- **`math.Sinh`**：计算双曲正弦值。
- **`math.Cosh`**：计算双曲余弦值。
- **`math.Tanh`**：计算双曲正切值。

- **用法**：
  ```go
  import (
      "fmt"
      "math"
  )

  func main() {
      x := 1.0
      fmt.Println("双曲正弦:", math.Sinh(x))  // 输出: 1.1752011936438014
      fmt.Println("双曲余弦:", math.Cosh(x))  // 输出: 1.5430806348152437
      fmt.Println("双曲正切:", math.Tanh(x))  // 输出: 0.7615941559557649
  }
  ```

#### 2.2 高级数学函数

**2.2.1 伪随机数生成（`math/rand` 包）**

`math/rand` 包用于生成伪随机数，常用于模拟、游戏和随机化操作。

- **用法**：
  ```go
  import (
      "fmt"
      "math/rand"
      "time"
  )

  func main() {
      r := rand.New(rand.NewSource(time.Now().UnixNano()))  // 创建带种子的随机数生成器（Go 1.20+ 推荐写法）
      fmt.Println("随机整数:", r.Intn(100))   // 生成 0 到 99 之间的随机整数
      fmt.Println("随机浮点数:", r.Float64())  // 生成 0.0 到 1.0 之间的随机浮点数
  }
  ```

**2.2.2 统计函数（`math/gamma` 包）**

Go 标准库中并没有直接提供统计函数，如 Gamma 函数、贝塔函数等。这些函数通常需要使用第三方库，如 `gonum`，或自己实现。

#### 2.3 常用数学公式

**2.3.1 斐波那契数列**

斐波那契数列是一种数值序列，其中每个数字都是前两个数字的和。

- **用法**：
  ```go
  package main

  import "fmt"

  func fibonacci(n int) int {
      if n <= 1 {
          return n
      }
      return fibonacci(n-1) + fibonacci(n-2)
  }

  func main() {
      for i := 0; i < 10; i++ {
          fmt.Print(fibonacci(i), " ")
      }
  }
  ```

**2.3.2 质数判断**

质数是只能被 1 和自身整除的正整数。

- **用法**：
  ```go
  package main

  import "fmt"

  func isPrime(n int) bool {
      if n <= 1 {
          return false
      }
      for i := 2; i*i <= n; i++ {
          if n%i == 0 {
              return false
          }
      }
      return true
  }

  func main() {
      for i := 2; i <= 50; i++ {
          if isPrime(i) {
              fmt.Print(i, " ")
          }
      }
  }
  ```

### 总结

本节列出了 `math` 包的绝对值、幂、平方根、三角、指数、对数、双曲函数，以及 `math/rand` 的伪随机数。每个示例都标注了输出值，可以逐条对照验证。