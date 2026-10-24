### 7. Statistical Analysis

Statistical analysis is the process of drawing conclusions from data: describing it, making inferences, testing hypotheses, modeling, and forecasting.

---

#### 7.1 Basic Concepts of Statistical Analysis

**7.1.1 Data types**

- **Quantitative data**: data that can be measured, such as age and income, further split into discrete and continuous data.
- **Qualitative data**: data describing properties, such as gender and color, further split into categorical and ordinal data.

**7.1.2 Descriptive statistics**

Descriptive statistics summarizes and describes the basic characteristics of a dataset. Common descriptive measures:
- **Mean**: the arithmetic average of the data.
- **Median**: the middle value of the data, splitting it into two halves.
- **Mode**: the value that appears most frequently in the data.
- **Variance and standard deviation**: measure the spread of the data.

- **Example**:
  ```go
  import (
      "fmt"
      "math"
  )

  func mean(data []float64) float64 {
      sum := 0.0
      for _, v := range data {
          sum += v
      }
      return sum / float64(len(data))
  }

  func stdDev(data []float64) float64 {
      m := mean(data)
      sum := 0.0
      for _, v := range data {
          sum += (v - m) * (v - m)
      }
      return math.Sqrt(sum / float64(len(data)))
  }

  func main() {
      data := []float64{1, 2, 3, 4, 5}
      fmt.Println("均值:", mean(data))
      fmt.Println("标准差:", stdDev(data))
  }
  ```

#### 7.2 Probability Distributions

**7.2.1 Normal distribution**

The normal distribution (Gaussian distribution) is the most common continuous probability distribution, characterized by a bell-shaped curve. Its parameters are the mean and the standard deviation.

- **Example** (using Go's `gonum` library):
  ```go
  import (
      "fmt"
      "gonum.org/v1/gonum/stat/distuv"
  )

  func main() {
      normal := distuv.Normal{
          Mu:    0,   // mean
          Sigma: 1,   // standard deviation
      }
      x := 1.0
      fmt.Println("正态分布概率密度:", normal.Prob(x))  // prints: 正态分布概率密度: 0.24197072451914337
  }
  ```

**7.2.2 Other distributions**

- **Poisson distribution**: describes the number of events occurring in a fixed interval of time or space.
- **Exponential distribution**: describes the time interval between events.
- **Uniform distribution**: every value has an equal probability of occurring.

#### 7.3 Hypothesis Testing

**7.3.1 One-sample t-test**

Tests whether a sample mean differs from a known population mean. Commonly used to compare means of an experimental group and a control group.

- **Example**:
  ```go
  import (
      "fmt"
      "gonum.org/v1/gonum/stat"
  )

  func main() {
      data := []float64{5.1, 5.2, 5.3, 5.4, 5.5}
      mean := stat.Mean(data, nil)
      sd := stat.StdDev(data, nil)
      fmt.Println("样本均值:", mean)
      fmt.Println("样本标准差:", sd)
  }
  ```

**7.3.2 Chi-squared test**

Tests whether the distribution of categorical data matches an expected distribution. Commonly used for tests of independence and tests of goodness of fit.

- **Example** (the chi-squared test needs a statistics library; the Go library may need extra support):
  ```go
  // requires a third-party library
  ```

**7.3.3 ANOVA (analysis of variance)**

Tests whether there is a significant difference among the means of multiple samples. Commonly used for analyzing experimental data.

- **Example**:
  ```go
  // the ANOVA test requires a third-party library
  ```

#### 7.4 Regression Analysis

**7.4.1 Linear regression**

Linear regression models the linear relationship between a dependent variable and one or more independent variables. The regression equation is \( y = \beta_0 + \beta_1 x \).

- **Example** (linear regression model):
  ```go
  import (
      "fmt"
      "gonum.org/v1/gonum/stat"
  )

  func main() {
      x := []float64{1, 2, 3, 4, 5}
      y := []float64{2, 4, 6, 8, 10}
      // LinearRegression returns the intercept alpha and the slope beta
      alpha, beta := stat.LinearRegression(x, y, nil, false)
      fmt.Printf("回归方程: y = %.2fx + %.2f\n", beta, alpha)  // prints: 回归方程: y = 2.00x + 0.00
  }
  ```

**7.4.2 Multiple regression**

Multiple regression models the relationship between a dependent variable and several independent variables. The regression equation is \( y = \beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n \).

- **Example**:
  ```go
  // multiple regression requires a more complex library
  ```

#### 7.5 Time Series Analysis

**7.5.1 Autoregressive model (AR)**

An autoregressive model predicts time series data from its own past values.

- **Example**:
  ```go
  // the AR model requires a more complex library
  ```

**7.5.2 Moving average model (MA)**

A moving average model smooths time series data and reduces the effect of noise.

- **Example**:
  ```go
  // the MA model requires a more complex library
  ```

**7.5.3 ARIMA model**

ARIMA (autoregressive integrated moving average) is used for time series forecasting. It combines autoregressive and moving average models and includes differencing.

- **Example**:
  ```go
  // the ARIMA model requires a more complex library
  ```

#### 7.6 Application Examples

Business analysis uses it for market research, customer behavior analysis, and sales forecasting; medical research uses it for clinical trials and drug efficacy evaluation; social science research uses it for surveys and policy evaluation. It's the same recipe each time: describe the data first, then test the hypothesis.

### Summary

The Go tooling here is concentrated in `gonum`: the `stat` package computes means, standard deviations, and linear regression, while the `distuv` package computes the probability density of the normal distribution. Chi-squared tests, ANOVA, multiple regression, and time series are left as comments only in the examples — they need a third-party library.

## References

- [math standard library](https://pkg.go.dev/math)
- [math/rand standard library](https://pkg.go.dev/math/rand)


## Sibling pages

- [Calc](/math/Calc.md)
- [LinearAlgebra](/math/LinearAlgebra.md)
- [Math](/math/Math.md)
- [Science](/math/Science.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Science](/math/Science.md)
