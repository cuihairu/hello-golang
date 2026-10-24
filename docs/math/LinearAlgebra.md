### 4. Linear Algebra

Linear algebra studies systems of linear equations, linear transformations, and vector spaces. Image processing, data analysis, and graphics all need it. Organized here into four parts: vectors, matrices, equation systems, and eigenvalues.

---

#### 4.1 Vectors

**4.1.1 Definition of a vector**

A vector is a quantity with both magnitude and direction. It can be written as an ordered set of numbers, such as `(x, y)` in two dimensions or `(x, y, z)` in three. Vectors are widely used in computation to represent points, directions, and displacements.

- **Example** (2D vector addition and dot product):
  ```go
  package main

  import "fmt"

  type Vector2D struct {
      X, Y float64
  }

  func (v1 Vector2D) Add(v2 Vector2D) Vector2D {
      return Vector2D{v1.X + v2.X, v1.Y + v2.Y}
  }

  func (v1 Vector2D) Dot(v2 Vector2D) float64 {
      return v1.X*v2.X + v1.Y*v2.Y
  }

  func main() {
      v1 := Vector2D{1, 2}
      v2 := Vector2D{3, 4}
      fmt.Println("向量加法:", v1.Add(v2))       // prints: {4 6}
      fmt.Println("向量点积:", v1.Dot(v2))       // prints: 11
  }
  ```

**4.1.2 Length of a vector**

The length (or norm) of a vector is its magnitude, computed from the square root of the sum of squares.

- **Example**:
  ```go
  package main

  import (
      "fmt"
      "math"
  )

  type Vector2D struct {
      X, Y float64
  }

  func (v Vector2D) Length() float64 {
      return math.Sqrt(v.X*v.X + v.Y*v.Y)
  }

  func main() {
      v := Vector2D{3, 4}
      fmt.Println("向量长度:", v.Length())  // prints: 5
  }
  ```

#### 4.2 Matrices

**4.2.1 Definition of a matrix**

A matrix is a rectangular array of numbers, used to represent linear transformations, systems of equations, and so on. Matrices support addition, multiplication, and other operations.

- **Example** (matrix addition and multiplication):
  ```go
  package main

  import "fmt"

  type Matrix2x2 struct {
      A, B, C, D float64
  }

  func (m1 Matrix2x2) Add(m2 Matrix2x2) Matrix2x2 {
      return Matrix2x2{
          A: m1.A + m2.A, B: m1.B + m2.B,
          C: m1.C + m2.C, D: m1.D + m2.D,
      }
  }

  func (m1 Matrix2x2) Multiply(m2 Matrix2x2) Matrix2x2 {
      return Matrix2x2{
          A: m1.A*m2.A + m1.B*m2.C,
          B: m1.A*m2.B + m1.B*m2.D,
          C: m1.C*m2.A + m1.D*m2.C,
          D: m1.C*m2.B + m1.D*m2.D,
      }
  }

  func main() {
      m1 := Matrix2x2{1, 2, 3, 4}
      m2 := Matrix2x2{5, 6, 7, 8}
      fmt.Println("矩阵加法:", m1.Add(m2))  // prints: {6 8 10 12}
      fmt.Println("矩阵乘法:", m1.Multiply(m2)) // prints: {19 22 43 50}
  }
  ```

**4.2.2 Transpose of a matrix**

The transpose of a matrix is the new matrix formed by swapping rows and columns.

- **Example**:
  ```go
  package main

  import "fmt"

  type Matrix2x2 struct {
      A, B, C, D float64
  }

  func (m Matrix2x2) Transpose() Matrix2x2 {
      return Matrix2x2{
          A: m.A, B: m.C,
          C: m.B, D: m.D,
      }
  }

  func main() {
      m := Matrix2x2{1, 2, 3, 4}
      fmt.Println("矩阵转置:", m.Transpose())  // prints: {1 3 2 4}
  }
  ```

#### 4.3 Systems of Linear Equations

**4.3.1 Solving a linear system**

A linear system can be written in matrix form \( Ax = b \), where `A` is the coefficient matrix, `x` is the vector of unknowns, and `b` is the constant vector. Algorithms such as Gaussian elimination and LU decomposition can solve it.

- **Example** (solving a linear system with the third-party library `gonum`):
  ```go
  package main

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

#### 4.4 Eigenvalues and Eigenvectors

**4.4.1 Definition of eigenvalues and eigenvectors**

Eigenvalues and eigenvectors are central to matrix analysis. For a matrix \( A \), if an eigenvalue \( \lambda \) and an eigenvector \( v \) satisfy \( Av = \lambda v \), then \( \lambda \) is the eigenvalue and \( v \) is the eigenvector.

- **Example** (finding eigenvalues and eigenvectors with `gonum`):
  ```go
  package main

  import (
      "fmt"
      "gonum.org/v1/gonum/mat"
  )

  func main() {
      // matrix A
      A := mat.NewSymDense(2, []float64{4, 1, 1, 3})

      // eigenvalues and eigenvectors
      var eig mat.EigenSym
      eig.Factorize(A, true)

      // get the eigenvalues
      vals := eig.Values(nil)
      fmt.Println("特征值:", vals)  // prints: 特征值: [2.381966011250105 4.618033988749895]

      // get the eigenvectors
      var vectors mat.Dense
      eig.VectorsTo(&vectors)
      fmt.Println("特征向量:\n", mat.Formatted(&vectors))
  }
  ```

#### 4.5 Application Examples

**4.5.1 Image processing**

Linear algebra is important in image processing. For example, transformations such as image rotation and scaling can be implemented with matrix multiplication.

**4.5.2 Data analysis**

In data analysis methods such as linear regression and principal component analysis (PCA), linear algebra is used to process and transform data.

**4.5.3 Computer graphics**

In computer graphics, 3D transformations, lighting models, and more all involve matrix and vector operations.

### Summary

Basic vector and matrix arithmetic is covered by the standard library `math`; solving systems and computing eigenvalues means reaching for `gonum`.

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)

## Sibling pages

- [Calc](/math/Calc.md)
- [Math](/math/Math.md)
- [MathFunc](/math/MathFunc.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Calc](/math/Calc.md)
- [Math](/math/Math.md)
- [MathFunc](/math/MathFunc.md)
- [MathRand](/math/MathRand.md)
- [Optimize](/math/Optimize.md)
- [Science](/math/Science.md)
- [Statistics](/math/Statistics.md)
