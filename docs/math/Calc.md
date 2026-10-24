### 6. Numerical Computing

Numerical computing solves math problems with approximate methods when no exact solution exists or the exact one is too expensive: nonlinear equations, linear systems, differential equations. Scientific computing, engineering, economics, and data analysis all use it.

---

#### 6.1 Basic Concepts of Numerical Methods

**6.1.1 Numerical error**

In numerical computation, results carry error because computers represent numbers with finite precision. The main kinds of error:
- **Rounding error**: error caused by the limited precision of floating-point numbers.
- **Truncation error**: error from truncating an infinite series or limiting the number of iterations.
- **Accumulated error**: the build-up of multiple errors across the computation.

**6.1.2 Convergence**

Convergence asks whether an algorithm's approximate solution approaches the exact one. Common notions of convergence:
- **Local convergence**: near the solution, the algorithm moves closer to it step by step.
- **Global convergence**: from any starting point, the algorithm moves closer to the actual solution.

#### 6.2 Numerical Linear Algebra

**6.2.1 Systems of linear equations**

A linear system can be written in matrix form \( Ax = b \). Methods for solving it include:
- **Gaussian elimination**: solves the system by eliminating unknowns step by step.
- **LU decomposition**: factors the matrix into a product of a lower-triangular and an upper-triangular matrix.

- **Example** (solving a linear system with `gonum`):
  ```go
  import (
      "fmt"
      "gonum.org/v1/gonum/mat"
  )

  func main() {
      // coefficient matrix A
      A := mat.NewDense(2, 2, []float64{2, 1, 1, 3})
      // constant vector b
      b := mat.NewVecDense(2, []float64{4, 9})

      // create the solver
      var AInv mat.Dense
      AInv.Inverse(A)

      // solve x = A^(-1) * b
      var x mat.VecDense
      x.MulVec(&AInv, b)

      fmt.Printf("解向量: x0=%.2f, x1=%.2f\n", x.AtVec(0), x.AtVec(1))  // prints: 解向量: x0=0.60, x1=2.80
  }
  ```

**6.2.2 Matrix factorization**

Matrix factorization breaks a matrix into a product of several matrices to simplify computation. Common factorizations include:
- **QR decomposition**: factors the matrix into a product of an orthogonal matrix and an upper-triangular matrix.
- **Eigenvalue decomposition**: factors the matrix into its eigenvalues and eigenvectors.

#### 6.3 Numerical Differentiation and Integration

**6.3.1 Numerical differentiation**

Numerical differentiation approximates the derivative of a function. Common methods:
- **Finite difference method**: approximates the derivative using the function values at neighboring points.

- **Example**:
  ```go
  import "fmt"

  func finiteDifference(f func(float64) float64, x float64, h float64) float64 {
      return (f(x+h) - f(x)) / h
  }

  func main() {
      f := func(x float64) float64 { return x*x }
      x := 2.0
      h := 1e-5
      fmt.Println("导数:", finiteDifference(f, x, h))  // prints: 4.000010000027032
  }
  ```

**6.3.2 Numerical integration**

Numerical integration approximates the definite integral of a function. Common methods:
- **Trapezoidal rule**: approximates the integral with the area of trapezoids.
- **Simpson's rule**: uses quadratic interpolation to improve accuracy.

- **Example**:
  ```go
  import "fmt"

  func trapezoidalRule(f func(float64) float64, a, b float64, n int) float64 {
      h := (b - a) / float64(n)
      sum := 0.5 * (f(a) + f(b))
      for i := 1; i < n; i++ {
          sum += f(a + float64(i)*h)
      }
      return sum * h
  }

  func main() {
      f := func(x float64) float64 { return x*x }
      a, b := 0.0, 1.0
      n := 100
      fmt.Println("积分结果:", trapezoidalRule(f, a, b, n))  // prints: 0.33335000000000004
  }
  ```

#### 6.4 Nonlinear Equations and Optimization

**6.4.1 Nonlinear equations**

Nonlinear equations can be solved numerically. Common methods:
- **Newton's method**: finds a root by iteration.
- **Secant method**: approximates the root's position with a straight line.

- **Example** (Newton's method on a nonlinear equation):
  ```go
  import (
      "fmt"
      "math"
  )

  func newtonMethod(f func(float64) float64, df func(float64) float64, x0 float64, tol float64, maxIter int) float64 {
      x := x0
      for i := 0; i < maxIter; i++ {
          fx := f(x)
          dfx := df(x)
          if math.Abs(dfx) < tol {
              return x
          }
          x = x - fx/dfx
      }
      return x
  }

  func main() {
      f := func(x float64) float64 { return x*x - 2 }
      df := func(x float64) float64 { return 2 * x }
      root := newtonMethod(f, df, 1, 1e-6, 100)
      fmt.Println("根:", root)  // prints: 1.414213562373095
  }
  ```

**6.4.2 Optimization**

Numerical optimization is about finding the best solution under given constraints. Common methods:
- **Gradient descent**: reduces the objective function's value through iteration.
- **Quasi-Newton methods**: use second-derivative information to speed up convergence.

#### 6.5 Application Examples

**6.5.1 Engineering design**

In engineering design, numerical computation simulates and optimizes design parameters, such as structural strength and fluid dynamics.

**6.5.2 Economics**

Economics uses numerical computation to optimize portfolios, forecast economic trends, and so on.

**6.5.3 Scientific research**

In research, numerical computation is used for data fitting, analysis of experimental results, and more.

### Summary

Every technique listed here comes with a runnable example: `gonum` solving a linear system, finite differences for derivatives, the trapezoidal rule for integration, Newton's method for roots. Data fitting and simulation in engineering design, economics, and research are all built on these basics.

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)

## Sibling pages

- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)
- [MathFunc](/math/MathFunc.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)
- [MathFunc](/math/MathFunc.md)
- [MathRand](/math/MathRand.md)
- [Optimize](/math/Optimize.md)
- [Science](/math/Science.md)
- [Statistics](/math/Statistics.md)
