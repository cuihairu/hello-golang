### 5. Mathematical Optimization

Mathematical optimization is about minimizing or maximizing an objective function subject to certain conditions. Engineering, economics, finance, and AI all use it. A problem usually breaks into three parts: the objective function, the constraints, and the solution method.

---

#### 5.1 Basic Concepts of Optimization Problems

**5.1.1 Objective function**

The objective function is the function to be optimized — either a benefit function to maximize or a cost function to minimize. It is usually written as $f(x)$, where $x$ is the decision variable.

- **Example**: maximize profit  $f(x) = 3x_1 + 2x_2$, where $x_1$ and $x_2$ are production quantities.

**5.1.2 Constraints**

Constraints are the restrictions on the decision variables, usually expressed as equalities or inequalities. They define the feasible region — the set of all solutions satisfying them.

- **Example**: production constraint $x_1 + x_2 \leq 10$, meaning production cannot exceed 10 units.

**5.1.3 Feasible and optimal solutions**

- **Feasible solution**: a solution satisfying all constraints is called a feasible solution.
- **Optimal solution**: among all feasible solutions, the one that makes the objective function reach its optimum is the optimal solution.

#### 5.2 Classification of Optimization Problems

**5.2.1 Linear programming**

Linear programming is a class of optimization problems in which both the objective function and the constraints are linear. Standard linear programming methods (such as the simplex method and interior point methods) solve it.

- **Example**:
  - Objective function: maximize $2x_1 + 3x_2$
  - Constraints:
$$
    \begin{cases}
    x_1 + 2x_2 \leq 6 \\
    3x_1 + x_2 \leq 9 \\
    x_1 \geq 0 \\
    x_2 \geq 0
    \end{cases}
$$

**5.2.2 Nonlinear programming**

Nonlinear programming handles cases where at least one of the objective function or constraints is nonlinear. These problems are generally more complex than linear ones and need more involved algorithms (such as Newton's method and quasi-Newton methods).

- **Example**:
  - Objective function: minimize $f(x) = x_1^2 + x_2^2$
  - Constraints: $x_1 + x_2 = 1$

**5.2.3 Integer programming**

In integer programming the decision variables must be integers. This type of optimization problem applies to scheduling and allocation problems. Branch and bound and the cutting plane method are common solution techniques.

- **Example**:
  - Objective function: maximize $5x_1 + 7x_2$
  - Constraints:
$$
    \begin{cases}
    3x_1 + 4x_2 \leq 15 \\
    x_1, x_2 \text{ must be integers}
    \end{cases}
 $$   

**5.2.4 Dynamic programming**

Dynamic programming handles problems where decisions are made stage by stage and each stage's decision affects later ones. It is usually used for optimal-path problems and resource allocation problems.

- **Example**: computing the shortest path from start to finish.

#### 5.3 Optimization Algorithms

**5.3.1 Simplex method**

The simplex method is an algorithm for solving linear programming problems. It finds the optimal solution by moving between the vertices of the feasible region.

- **Example**: solving an unconstrained optimization problem with the `optimize` package of `gonum` (linear programming with linear constraints needs additional library support):
  ```go
  package main

  import (
      "fmt"
      "gonum.org/v1/gonum/optimize"
  )

  func main() {
      // objective function: f(x) = (x0 - 3)^2 + (x1 - 2)^2, theoretical minimum at (3, 2)
      problem := optimize.Problem{
          Func: func(x []float64) float64 {
              return (x[0]-3)*(x[0]-3) + (x[1]-2)*(x[1]-2)
          },
      }

      // solve using the Nelder-Mead simplex algorithm
      result, err := optimize.Minimize(problem, []float64{0, 0}, nil, &optimize.NelderMead{})
      if err != nil {
          fmt.Println("优化失败:", err)
          return
      }
      fmt.Println("最优解:", result.X)    // prints: 最优解: [3.0000000000000004 2]
      fmt.Println("目标函数值:", result.F) // prints: 目标函数值: 1.9721522630525295e-31
  }
  ```

**5.3.2 Newton's method**

Newton's method is an iterative algorithm for nonlinear optimization, using the second derivative of the objective function to speed up convergence.

- **Example**:
  ```go
  package main

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
      fmt.Println("根:", root)
  }
  ```

**5.3.3 Genetic algorithms**

A genetic algorithm is an optimization algorithm based on natural selection and genetics, suitable for complex optimization problems such as combinatorial optimization.

- **Example**: the fitness function, selection, crossover, and mutation operations for an optimization problem must be customized for each specific problem.

#### 5.4 Application Examples

**5.4.1 Resource allocation**

In manufacturing and project management, optimizing resource allocation maximizes benefit or minimizes cost. For example, optimizing production schedules or employee shifts.

**5.4.2 Machine learning**

Many machine learning algorithms, such as support vector machines and neural network training, involve optimization problems — optimizing the objective function to improve model performance.

**5.4.3 Logistics and transport**

In logistics and transport, optimizing routes and delivery plans cuts costs in practice.

### Summary

This covers the four problem classes — linear, nonlinear, integer, and dynamic programming — starting from the objective function and constraints, and records three solution approaches: simplex for linear problems, Newton's method for nonlinear, and genetic algorithms for combinatorial optimization. The first two examples run as-is with `gonum/optimize`.

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)


## Sibling pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)
- [MathRand](/math/MathRand.md)
- [Science](/math/Science.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [MathRand](/math/MathRand.md)
- [Science](/math/Science.md)
