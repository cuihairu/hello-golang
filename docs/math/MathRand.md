### 3. 随机数生成与概率计算

在编程中，随机数生成和概率计算是处理模拟、统计分析和算法设计等任务的核心技术。Go语言提供了丰富的工具和库来处理随机数和概率计算。以下是对随机数生成与概率计算的详细介绍。

---

#### 3.1 随机数生成

**3.1.1 伪随机数生成（`math/rand` 包）**

Go语言的 `math/rand` 包用于生成伪随机数。伪随机数是通过算法生成的看似随机的数字序列。初始化随机数生成器的种子是产生不同随机数序列的关键。

- **初始化种子**：
  使用当前时间的纳秒数作为种子可以确保每次运行程序时生成的随机数序列不同。

  ```go
  import (
      "fmt"
      "math/rand"
      "time"
  )

  func main() {
      rand.Seed(time.Now().UnixNano())  // 初始化随机数种子
      fmt.Println("随机整数:", rand.Intn(100))  // 生成 0 到 99 之间的随机整数
      fmt.Println("随机浮点数:", rand.Float64())  // 生成 0.0 到 1.0 之间的随机浮点数
  }
  ```

**3.1.2 随机数生成的函数**

- **`rand.Intn(n int) int`**：返回一个 [0, n) 范围内的随机整数。
- **`rand.Float64() float64`**：返回一个 [0.0, 1.0) 范围内的随机浮点数。
- **`rand.Perm(n int) []int`**：返回一个长度为 `n` 的随机排列的整数切片。
- **`rand.Int() *big.Int`**：返回一个随机的大整数。

**3.1.3 自定义随机数生成**

你可以自定义生成的随机数类型，例如生成在特定范围内的随机浮点数或整数。

- **示例**：
  ```go
  import (
      "fmt"
      "math/rand"
      "time"
  )

  func randomInRange(min, max int) int {
      return rand.Intn(max-min+1) + min
  }

  func main() {
      rand.Seed(time.Now().UnixNano())
      fmt.Println("自定义随机整数:", randomInRange(10, 50))  // 生成 10 到 50 之间的随机整数
  }
  ```

#### 3.2 概率基础

**3.2.1 事件和样本空间**

- **事件**：一个事件是样本空间中的一个子集。比如，抛掷一枚硬币的事件可以是“正面朝上”。
- **样本空间**：样本空间是所有可能事件的集合。在抛掷硬币的例子中，样本空间是 `{正面, 反面}`。

**3.2.2 概率计算**

概率是事件发生的可能性。概率的计算公式是：
\[ P(A) = \frac{\text{事件 A 的成功数}}{\text{样本空间的总数}} \]

- **示例**：
  ```go
  import "fmt"

  func probability(successes, total int) float64 {
      return float64(successes) / float64(total)
  }

  func main() {
      fmt.Println("事件 A 的概率:", probability(3, 10))  // 输出: 0.3
  }
  ```

**3.2.3 条件概率和联合概率**

- **条件概率**：事件 B 在事件 A 已经发生的情况下发生的概率。计算公式是：
  \[ P(B|A) = \frac{P(A \cap B)}{P(A)} \]
- **联合概率**：两个事件 A 和 B 同时发生的概率。计算公式是：
  \[ P(A \cap B) = P(A) \times P(B) \]

- **示例**：
  ```go
  import "fmt"

  func conditionalProbability(pAB, pA float64) float64 {
      return pAB / pA
  }

  func main() {
      fmt.Println("条件概率:", conditionalProbability(0.2, 0.5))  // 输出: 0.4
  }
  ```

#### 3.3 常见概率分布

**3.3.1 正态分布**

正态分布是一种对称的钟形曲线，表示大多数数据集中在均值附近，远离均值的数据点较少。Go语言中的 `math/rand` 包并没有直接提供正态分布函数，但可以通过算法进行实现。

- **示例**（通过 Box-Muller 变换）：
  ```go
  import (
      "fmt"
      "math"
      "math/rand"
      "time"
  )

  func normalRandom(mu, sigma float64) float64 {
      u1 := rand.Float64()
      u2 := rand.Float64()
      z0 := math.Sqrt(-2.0 * math.Log(u1)) * math.Cos(2.0 * math.Pi * u2)
      return mu + z0*sigma
  }

  func main() {
      rand.Seed(time.Now().UnixNano())
      fmt.Println("正态分布随机数:", normalRandom(0, 1))  // 均值为 0，标准差为 1
  }
  ```

**3.3.2 伯努利分布**

伯努利分布是一种离散概率分布，只有两个可能的结果：成功（通常表示为 1）和失败（通常表示为 0）。它用于模拟两种可能结果的事件。

- **示例**：
  ```go
  import (
      "fmt"
      "math/rand"
      "time"
  )

  func bernoulli(p float64) int {
      if rand.Float64() < p {
          return 1
      }
      return 0
  }

  func main() {
      rand.Seed(time.Now().UnixNano())
      fmt.Println("伯努利分布随机结果:", bernoulli(0.7))  // 成功概率为 70%
  }
  ```

**3.3.3 泊松分布**

泊松分布用于模拟单位时间内事件发生的次数。适用于稀有事件的统计，如每小时到达的顾客数量。

- **示例**：
  ```go
  import (
      "fmt"
      "math"
      "math/rand"
      "time"
  )

  func poisson(lambda float64) int {
      L := math.Exp(-lambda)
      k := 0
      p := 1.0
      for p > L {
          k++
          p *= rand.Float64()
      }
      return k - 1
  }

  func main() {
      rand.Seed(time.Now().UnixNano())
      fmt.Println("泊松分布随机结果:", poisson(3.0))  // 参数 lambda 为 3.0
  }
  ```

### 总结

本节介绍了随机数生成和概率计算的基本概念和方法。Go语言提供了强大的 `math/rand` 包用于生成伪随机数，并且可以利用数学公式和算法实现各种概率分布。掌握这些技术将有助于处理模拟、统计分析和随机算法等任务。在实际应用中，理解随机数生成和概率计算的基础知识是进行数据科学、算法设计和系统建模的重要基础。