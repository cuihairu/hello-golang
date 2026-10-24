### 2. Math Functions

Go's `math` package provides the common math functions: absolute value, powers, trigonometry, logarithms, and so on. Listed here by use, with output.

---

#### 2.1 Common Math Functions

**2.1.1 Absolute value (`math.Abs`)**

`math.Abs` returns the absolute value of a number — its non-negative value with the sign removed. Used a lot for distance and error calculations.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("绝对值:", math.Abs(-3.14))  // prints: 3.14
  }
  ```

**2.1.2 Power (`math.Pow`)**

`math.Pow` computes a specified power of a number. It returns `x` raised to the power `y`.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("幂运算:", math.Pow(2, 3))  // prints: 8
  }
  ```

**2.1.3 Square root (`math.Sqrt`)**

`math.Sqrt` computes the square root of a number. Square roots come up in square-related math problems, like geometry and solving equations.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("平方根:", math.Sqrt(16))  // prints: 4
  }
  ```

**2.1.4 Trigonometric functions (`math.Sin`, `math.Cos`, `math.Tan`)**

- **`math.Sin`**: computes the sine of an angle.
- **`math.Cos`**: computes the cosine of an angle.
- **`math.Tan`**: computes the tangent of an angle.

These trigonometric functions handle periodic phenomena and angle-related calculations.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      angle := math.Pi / 4  // 45 degrees
      fmt.Println("正弦:", math.Sin(angle))  // prints: 0.7071067811865475
      fmt.Println("余弦:", math.Cos(angle))  // prints: 0.7071067811865476
      fmt.Println("正切:", math.Tan(angle))  // prints: 1
  }
  ```

**2.1.5 Exponential function (`math.Exp`)**

`math.Exp` computes `e` (the base of the natural logarithm) raised to the power `x`. Used for exponential-growth models and similar.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("指数函数:", math.Exp(2))  // prints: 7.38905609893065
  }
  ```

**2.1.6 Logarithm functions (`math.Log`, `math.Log10`)**

- **`math.Log`**: computes the natural logarithm (base `e`).
- **`math.Log10`**: computes the logarithm base 10.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("自然对数:", math.Log(10))    // prints: 2.302585092994046
      fmt.Println("常用对数:", math.Log10(100))  // prints: 2
  }
  ```

**2.1.7 Hyperbolic functions (`math.Sinh`, `math.Cosh`, `math.Tanh`)**

- **`math.Sinh`**: computes the hyperbolic sine.
- **`math.Cosh`**: computes the hyperbolic cosine.
- **`math.Tanh`**: computes the hyperbolic tangent.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      x := 1.0
      fmt.Println("双曲正弦:", math.Sinh(x))  // prints: 1.1752011936438014
      fmt.Println("双曲余弦:", math.Cosh(x))  // prints: 1.5430806348152437
      fmt.Println("双曲正切:", math.Tanh(x))  // prints: 0.7615941559557649
  }
  ```

#### 2.2 Advanced Math Functions

**2.2.1 Pseudo-random number generation (`math/rand` package)**

The `math/rand` package generates pseudo-random numbers, used for simulations, games, and randomization.

- **Usage**:
  ```go
  package main

  import (
      "fmt"
      "math/rand"
      "time"
  )

  func main() {
      r := rand.New(rand.NewSource(time.Now().UnixNano()))  // create a seeded random generator (recommended style in Go 1.20+)
      fmt.Println("随机整数:", r.Intn(100))   // random integer from 0 to 99
      fmt.Println("随机浮点数:", r.Float64())  // random float from 0.0 to 1.0
  }
  ```

**2.2.2 Special functions (`math` package)**

The standard library `math` package includes a few special functions: `Gamma`, `Lgamma`, `Erf`, `Erfc`, and so on. Statistically common ones like the beta function are not included — use a third-party library such as `gonum` or implement them yourself.

#### 2.3 Common Math Formulas

**2.3.1 Fibonacci sequence**

The Fibonacci sequence is a series of numbers in which each number is the sum of the two preceding ones.

- **Usage**:
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

**2.3.2 Prime number test**

A prime number is a positive integer divisible only by 1 and itself.

- **Usage**:
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

### Summary

This gathers the `math` package's absolute value, power, square root, trigonometry, exponential, logarithm, and hyperbolic functions, plus `math/rand` pseudo-random numbers. Every example is annotated with its output value, so you can check them off one by one.

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)

## Sibling pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)
- [MathRand](/math/MathRand.md)
