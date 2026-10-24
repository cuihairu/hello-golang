### 1. Basic Math Concepts

Math in programming starts with number types and the four arithmetic operations. This section covers how integers, floats, and complex numbers are represented, then the operations and two constants.

#### 1.1 Number Types and Representation

**1.1.1 Integer**

An integer is a number with no fractional part. In programming, integers are usually used for counting, indexing, and other scenarios that need exact values. Integers can be positive, negative, or zero.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      var x int = 42
      var y int = -7
      fmt.Println("整数 x:", x)
      fmt.Println("整数 y:", y)
  }
  ```

**1.1.2 Floating-point**

Floating-point numbers are used to represent numbers that have a fractional part. In programming, they are commonly used in scientific computing, financial applications, and other scenarios that need imprecise values. The floating-point representation includes single precision (float32) and double precision (float64).

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      var a float32 = 3.14
      var b float64 = -2.71828
      fmt.Println("浮点数 a:", a)
      fmt.Println("浮点数 b:", b)
  }
  ```

**1.1.3 Complex Numbers**

A complex number consists of a real part and an imaginary part, and is used to represent a point on a two-dimensional plane. In Go, the complex types are `complex64` and `complex128`.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      var c complex64 = 1 + 2i
      var d complex128 = 3 - 4i
      fmt.Println("复数 c:", c)
      fmt.Println("复数 d:", d)
  }
  ```

#### 1.2 Basic Arithmetic Operations

**1.2.1 Addition**

Addition is the operation of adding two or more numbers together. The result is the sum of those numbers.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a, b := 5, 7
      fmt.Println("加法:", a + b)
  }
  ```

**1.2.2 Subtraction**

Subtraction is the operation of subtracting one number from another. The result is the difference between the two numbers.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a, b := 10, 4
      fmt.Println("减法:", a - b)
  }
  ```

**1.2.3 Multiplication**

Multiplication is the operation of multiplying one number by another. The result is the product of those numbers.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a, b := 6, 9
      fmt.Println("乘法:", a * b)
  }
  ```

**1.2.4 Division**

Division is the operation of dividing one number by another. The result is the quotient of the two numbers. Note that a division can produce a fraction.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a, b := 15, 4
      fmt.Println("除法:", float64(a) / float64(b))
  }
  ```

**1.2.5 Modulus**

Modulus computes the remainder when one number is divided by another. The result is the leftover part.

- **Example**:
  ```go
  package main

  import "fmt"

  func main() {
      a, b := 15, 4
      fmt.Println("取模:", a % b)
  }
  ```

#### 1.3 Mathematical Constants

**1.3.1 Pi (π, Pi)**

Pi is a mathematical constant that represents the ratio of a circle's circumference to its diameter, roughly 3.14159. You need it to compute both the area and the circumference of a circle.

- **Example**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("圆周率:", math.Pi)
  }
  ```

**1.3.2 E (base of the natural logarithm, e)**

E is a mathematical constant that is the base of the natural logarithm, roughly 2.71828. It shows up in many natural phenomena and mathematical formulas.

- **Example**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  func main() {
      fmt.Println("自然对数的底:", math.E)
  }
  ```

### Summary

In Go every one of these has a direct counterpart: the types are `int`, `float32`/`float64`, `complex64`/`complex128`, the operators are just `+`, `-`, `*`, `/`, `%`, and the constants come from the `math` package (`math.Pi`, `math.E`).

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)

## Sibling pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [MathFunc](/math/MathFunc.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [MathFunc](/math/MathFunc.md)
- [MathRand](/math/MathRand.md)
- [Optimize](/math/Optimize.md)
- [Science](/math/Science.md)
- [Statistics](/math/Statistics.md)
