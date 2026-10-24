### Benchmark tests

A benchmark test (Benchmark Testing) measures how fast a piece of code runs. Go ships with a built-in benchmarking framework; the syntax is much like a normal test, only the function signature and the way you run it differ.

#### 3.1 The concept of benchmark testing

A benchmark test measures the execution time of a block of code and expresses performance as numbers. Unlike a normal test, it cares about speed rather than functional correctness, and the measured times are used to find performance bottlenecks.

#### 3.2 Writing a benchmark function

The signature of a benchmark function should be `func BenchmarkXxx(b *testing.B)`, where `Xxx` is the test name and `b` is a parameter of type `*testing.B`, used to manage benchmark state and record results.

**Example**:
```go
// math.go
package math

// Add returns the sum of two integers
func Add(a, b int) int {
    return a + b
}

// math_test.go
package math

import "testing"

// BenchmarkAdd tests the performance of the Add function
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

In the code above:
- `BenchmarkAdd` is the benchmark function, used to measure the performance of `Add`.
- `b.N` is a loop count that the benchmarking framework adjusts dynamically, ensuring the test runs with enough iterations.

#### 3.3 Running benchmark tests

Use the `go test -bench` command to run benchmark tests. This compiles the benchmark code and the code under test, and executes every benchmark function.

**Basic command**:
```sh
go test -bench .
```

- The `-bench` flag specifies benchmark mode. `.` means run all benchmark functions.

**Verbose benchmark output**:
```sh
go test -bench . -v
```

- The `-v` flag enables verbose mode, showing the detailed result of every benchmark.

**Run a specific benchmark**:
```sh
go test -bench BenchmarkAdd
```

- The `-bench` flag can also name a specific benchmark function to run.

#### 3.4 Analyzing benchmark results

Benchmark output includes the average time per iteration, operations per second, and so on. From these numbers you can assess the performance and efficiency of the code.

**Example output**:
```sh
go test -bench . -v
```
```
BenchmarkAdd-8    1000000000               1.00 ns/op
```

- `BenchmarkAdd-8` is the benchmark name together with the concurrency level.
- `1000000000` is the number of iterations executed.
- `1.00 ns/op` is the average time per operation.

#### 3.5 Benchmarking tips

1. **Avoid excessive logging**: in a benchmark, avoid lots of log output, which drags down the measured performance.
2. **Avoid unnecessary computation**: keep only the code you actually want to measure in the benchmark function, reducing noise.
3. **Use realistic test data**: benchmark with a representative data set so the numbers reflect real conditions.

#### 3.6 Benchmark testing and profiling

Benchmarks and Go's profiling tools chain together nicely: `-bench` finds the slow function, then `pprof` shows exactly which line the time is spent on.

**Generate a CPU profile**:
```sh
go test -bench . -cpuprofile cpu.out
go tool pprof cpu.out
```

- The `-cpuprofile` flag generates a CPU profiling file.

**Generate a memory profile**:
```sh
go test -bench . -memprofile mem.out
go tool pprof mem.out
```

- The `-memprofile` flag generates a memory profiling file.

### Summary

What a benchmark gives you is the average time per operation (such as `1.00 ns/op`), and a number is more reliable than a gut feeling. Three things in the syntax: the function name starts with `Benchmark`, the loop runs `b.N` times, and you execute it with `go test -bench`. To keep digging into hot spots, add `-cpuprofile` or `-memprofile` to produce a pprof report.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)
- [Go Blog · testing.B.Loop](https://go.dev/blog/testing-b-loop)


## Sibling pages

- [Fuzz](/zh/test/Fuzz.md)
- [Test](/test/Test.md)
- [Advanced](/test/Advanced.md)
- [BaseTest](/test/BaseTest.md)
- [Cover](/test/Cover.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Cover](/test/Cover.md)
