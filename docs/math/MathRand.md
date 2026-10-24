### 3. Random Number Generation and Probability

`math/rand` produces the pseudo-random numbers, and probability models are a few formulas layered on top of it. This section first looks at how random numbers are generated, then at events, conditional probability, and the normal, Bernoulli, and Poisson distributions.

---

#### 3.1 Random Number Generation

**3.1.1 Pseudo-random number generation (`math/rand` package)**

Go's `math/rand` package generates pseudo-random numbers. Pseudo-random numbers are sequences that look random but are produced by an algorithm. Seeding the generator is what makes different runs produce different sequences.

- **Seeding**:
  Using the current time in nanoseconds as the seed ensures each run of the program produces a different sequence.

  ```go
  package main

  import (
      "fmt"
      "math/rand"
      "time"
  )

  func main() {
      rand.Seed(time.Now().UnixNano())  // seed the random number generator
      fmt.Println("随机整数:", rand.Intn(100))  // random integer from 0 to 99
      fmt.Println("随机浮点数:", rand.Float64())  // random float from 0.0 to 1.0
  }
  ```

> Note: since Go 1.20 the global random number generator is seeded automatically, and `rand.Seed` is deprecated. If you need explicit control over the seed (for example to reproduce results), create a standalone generator with `r := rand.New(rand.NewSource(seed))`.

**3.1.2 Functions for generating random numbers**

- **`rand.Intn(n int) int`**: returns a random integer in [0, n).
- **`rand.Float64() float64`**: returns a random float in [0.0, 1.0).
- **`rand.Perm(n int) []int`**: returns a random permutation of integers as a slice of length `n`.
- **`rand.Int() int`**: returns a non-negative random integer (for large random integers use the `Int.Rand` method of the `math/big` package).

**3.1.3 Custom random number generation**

You can customize the kind of random number you generate, for example a random float or integer within a specific range.

- **Example**:
  ```go
  package main

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
      fmt.Println("自定义随机整数:", randomInRange(10, 50))  // random integer from 10 to 50
  }
  ```

#### 3.2 Probability Basics

**3.2.1 Events and the sample space**

- **Event**: an event is a subset of the sample space. For example, in a coin toss an event could be "heads comes up".
- **Sample space**: the sample space is the set of all possible outcomes. In the coin toss example, the sample space is `{heads, tails}`.

**3.2.2 Computing probability**

Probability is the likelihood that an event occurs. The formula is:

`P(A) = number of successful outcomes for event A / total number of outcomes in the sample space`

- **Example**:
  ```go
  package main

  import "fmt"

  func probability(successes, total int) float64 {
      return float64(successes) / float64(total)
  }

  func main() {
      fmt.Println("事件 A 的概率:", probability(3, 10))  // prints: 0.3
  }
  ```

**3.2.3 Conditional probability and joint probability**

- **Conditional probability**: the probability that event B occurs given that event A has already occurred. The formula is:

  `P(B|A) = P(A ∩ B) / P(A)`
- **Joint probability**: the probability that events A and B both occur. When A and B are **mutually independent**, the formula is:

  `P(A ∩ B) = P(A) × P(B)`

- **Example**:
  ```go
  package main

  import "fmt"

  func conditionalProbability(pAB, pA float64) float64 {
      return pAB / pA
  }

  func main() {
      fmt.Println("条件概率:", conditionalProbability(0.2, 0.5))  // prints: 0.4
  }
  ```

#### 3.3 Common Probability Distributions

**3.3.1 Normal distribution**

The normal distribution is a symmetric bell-shaped curve: most of the data clusters near the mean, and fewer points sit far from it. Go's `math/rand` package does not provide a normal distribution function directly, but you can implement one yourself.

- **Example** (via the Box-Muller transform):
  ```go
  package main

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
      fmt.Println("正态分布随机数:", normalRandom(0, 1))  // mean 0, standard deviation 1
  }
  ```

**3.3.2 Bernoulli distribution**

The Bernoulli distribution is a discrete distribution with only two possible outcomes: success (usually 1) and failure (usually 0). It models events with exactly two possible results.

- **Example**:
  ```go
  package main

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
      fmt.Println("伯努利分布随机结果:", bernoulli(0.7))  // success probability 70%
  }
  ```

**3.3.3 Poisson distribution**

The Poisson distribution models the number of events occurring per unit of time. It suits rare-event counts, such as the number of customers arriving per hour.

- **Example**:
  ```go
  package main

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
      fmt.Println("泊松分布随机结果:", poisson(3.0))  // lambda parameter 3.0
  }
  ```

### Summary

`math/rand` gives you the random numbers: `Intn` for integers, `Float64` for decimals in [0, 1), `Perm` for random permutations; the Box-Muller transform turns two uniform random numbers into a normal distribution, Bernoulli is one `Float64` compared against p, and Poisson multiplies uniforms until the product drops below `exp(-lambda)`.

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)
- [Official Blog · math/rand/v2](https://go.dev/blog/randv2)


## Sibling pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)
- [MathFunc](/math/MathFunc.md)
- [Optimize](/math/Optimize.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Optimize](/math/Optimize.md)
