### Test coverage

Test coverage is an important measure of test quality: it expresses what fraction of code lines or code paths in the tested code were actually executed by the tests. High coverage usually means most code paths are exercised, which catches potential defects more reliably. Go provides built-in coverage tooling that helps developers see how far their tests reach and where to add more cases.

#### 7.1 Types of test coverage

There are usually several kinds of coverage:

1. **Line coverage**: measures the fraction of code lines executed by the tests. This is the most common coverage metric.

2. **Statement coverage**: computes the fraction of statements executed by the tests. Like line coverage, but it focuses more on whether each statement runs.

3. **Branch coverage**: measures whether each branch path was executed by a test. It ensures every possible conditional branch is covered.

4. **Path coverage**: measures the fraction of all paths executed by the tests. Path coverage can catch more subtle logic errors, but is usually harder to achieve.

5. **Function coverage**: checks whether every function is called. Function coverage cares whether a function runs, not about the lines inside it.

#### 7.2 Analyzing coverage with Go's built-in tools

Go provides built-in tools to collect and analyze test coverage. Use the `go test` command with the coverage flags to produce a coverage report.

**Collect coverage data**:
```sh
go test -coverprofile=coverage.out
```

**Generate an HTML report**:
```sh
go tool cover -html=coverage.out -o coverage.html
```

**Generate a coverage summary report**:
```sh
go tool cover -func=coverage.out
```

**Generate a detailed coverage report**:
```sh
go test -coverprofile=coverage.out -covermode=atomic
```

**Example**:
```go
// example_test.go
package example

import (
    "testing"
    "math"
)

// function example
func Sqrt(x float64) float64 {
    return math.Sqrt(x)
}

// test example
func TestSqrt(t *testing.T) {
    result := Sqrt(16)
    if result != 4 {
        t.Errorf("Expected 4, got %f", result)
    }
}
```

**Generate a coverage report**:
```sh
go test -coverprofile=coverage.out
go tool cover -html=coverage.out -o coverage.html
```

#### 7.3 Reading a coverage report

- **HTML report**: the `coverage.html` file is a visual report. Open it in a browser to see which lines were covered by tests and which were not.

- **Function coverage report**: the `go tool cover -func=coverage.out` command shows the coverage percentage of every function plus how many lines are uncovered.

**Example report output**:
```
filename      line   stmt   cover   delta
example.go    1      1      100.0%  +100.0%
example.go    5      5      80.0%   +60.0%
example.go    9      9      60.0%   +30.0%
total:        15     15     75.0%   +40.0%
```

#### 7.4 Improving test coverage

To raise coverage you can take these steps:

1. **Add test cases**: write more tests to cover the lines and branches that are not yet tested.

2. **Use boundary-value analysis**: make sure your tests include various boundary values and special cases.

3. **Look for coverage blind spots**: use the coverage report to identify untested parts of the code and write cases targeted at them.

4. **Automate tests**: run tests and generate coverage reports on a schedule, so new code and changed code stay covered.

#### 7.5 Coverage and what it means

High coverage can raise code quality, but it is not the only measure of test quality. Use coverage reports together with other test measures (functional tests, integration tests, user acceptance tests) to get thorough coverage and high-quality software.

### Summary

Go coverage is three commands: `go test -coverprofile` produces the data, `go tool cover -html` shows which lines never ran, and `go tool cover -func` shows each function's percentage. A high coverage number does not mean good tests; boundary values and branches still need their own cases.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)
- [Official · Coverage (build-cover)](https://go.dev/doc/build-cover)
- [Go Blog · The cover story](https://go.dev/blog/cover)


## Sibling pages

- [Fuzz](/zh/test/Fuzz.md)
- [Test](/test/Test.md)
- [Advanced](/test/Advanced.md)
- [Benchmark](/test/Benchmark.md)
- [Example](/test/Example.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Benchmark](/test/Benchmark.md)
- [Example](/test/Example.md)
