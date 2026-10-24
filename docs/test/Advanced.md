# Advanced testing techniques

Alongside unit tests I've put together six more testing techniques: concurrent testing, mocking, coverage analysis, memory-leak detection, performance testing, and A/B comparison. Each section gives the Go approach.

#### 5.1 Concurrent testing

Concurrent testing verifies how code behaves and performs under concurrency. In Go, concurrent testing mainly uses features from the `testing` package together with goroutines and channels.

**Example**:
```go
// concurrent_test.go
package main

import (
    "testing"
    "time"
)

// Suppose we have a function that must handle data correctly under concurrency
func ProcessData(data int) int {
    // simulate data processing
    time.Sleep(100 * time.Millisecond)
    return data * 2
}

// TestConcurrentProcessing tests concurrent data processing
func TestConcurrentProcessing(t *testing.T) {
    // the channel carries input and output together, avoiding dependence on receive order
    type result struct {
        input  int
        output int
    }
    results := make(chan result, 10)

    for i := 0; i < 10; i++ {
        go func(i int) {
            results <- result{input: i, output: ProcessData(i)}
        }(i)
    }

    for i := 0; i < 10; i++ {
        r := <-results
        if r.output != r.input*2 {
            t.Errorf("Expected %d, got %d", r.input*2, r.output)
        }
    }
}
```

In the code above:
- The `TestConcurrentProcessing` function runs `ProcessData` concurrently via goroutines.
- Results are collected through a channel and compared against the expected values.

#### 5.2 Mocking

Mocking creates and controls the dependencies in a test so that the behavior of the code can be exercised. In Go you can use libraries such as `gomock` and `testify` for mocking.

**Using `gomock`**:
```go
// example_test.go
package example

import (
    "testing"
    "github.com/golang/mock/gomock"
)

// define the interface
type Service interface {
    DoSomething() string
}

// use gomock to generate a mock object
func TestService(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockService := NewMockService(ctrl)
    mockService.EXPECT().DoSomething().Return("Mocked Response")

    result := mockService.DoSomething()
    if result != "Mocked Response" {
        t.Errorf("Expected 'Mocked Response', got '%s'", result)
    }
}
```

In the code above:
- `gomock` is used to create a mock object for the `Service` interface.
- The expected call and return value are set, and the actual call is checked against them.

#### 5.3 Coverage analysis

Coverage analysis measures which parts of the code are exercised by tests. Go provides built-in coverage tooling that can produce a coverage report.

**Generate a coverage report**:
```sh
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

- The `-coverprofile` flag generates the coverage data file.
- The `cover` tool generates an HTML coverage report showing which code is covered.

#### 5.4 Memory-leak detection

Memory-leak detection finds and fixes memory leaks in the code. Go provides the `pprof` tool to analyze memory usage.

**Generate a memory analysis report**:
```sh
go test -memprofile mem.out
go tool pprof mem.out
```

- The `-memprofile` flag generates a memory profiling file.
- The `pprof` tool is used to analyze and visualize memory usage.

#### 5.5 Performance testing

Performance testing measures how code executes and how much resource it consumes. Go's `testing` package provides benchmarking for this.

**Write a benchmark**:
```go
// performance_test.go
package main

import (
    "sort"
    "testing"
)

// BenchmarkSort tests the performance of the sorting algorithm
func BenchmarkSort(b *testing.B) {
    data := []int{5, 3, 8, 1, 2, 7, 6, 4}
    for i := 0; i < b.N; i++ {
        sort.Ints(data)
    }
}
```

- The `BenchmarkSort` function measures the sorting algorithm's performance and records the average time per operation.

#### 5.6 A/B testing

A/B testing compares two or more versions of the code to determine which one performs better. Go has no built-in A/B testing tool, but you can implement it by writing test code and recording performance data.

**Example**:
```go
// ab_test.go
package main

import (
    "testing"
)

// implement A and B
func runImplementationA() int {
    return 1
}

func runImplementationB() int {
    return 2
}

// TestABComparison tests the performance of the two implementations
func TestABComparison(t *testing.T) {
    resultA := runImplementationA()
    resultB := runImplementationB()

    if resultA < resultB {
        t.Logf("Implementation A is better")
    } else {
        t.Logf("Implementation B is better")
    }
}
```

In the code above:
- `runImplementationA` and `runImplementationB` are the different implementations being compared.
- The test result decides which implementation is better.

### Summary

The six techniques each cover one angle: concurrent testing exposes data races, mocking isolates dependencies, a coverage report shows code your tests never touched, memory analysis finds the heavy allocators, and benchmarks give the time per operation. Coverage, memory, and benchmarks are all supported directly by `go test` flags.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)
- [Go Blog · Subtests and Sub-benchmarks](https://go.dev/blog/subtests)

## Sibling pages

- [Fuzz](/zh/test/Fuzz.md)
- [Test](/test/Test.md)
- [BaseTest](/test/BaseTest.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [BaseTest](/test/BaseTest.md)
- [Benchmark](/test/Benchmark.md)
- [Cover](/test/Cover.md)
- [Example](/test/Example.md)
- [Lib](/zh/test/Lib.md)
- [Practice](/zh/test/Practice.md)
