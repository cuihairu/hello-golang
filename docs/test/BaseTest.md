### Basic tests

Go tests are written in `_test.go` files, with function names starting with `Test` and a `*testing.T` parameter; one `go test` runs them all. I've organized this page around four steps: writing, running, reading output, and handling errors.

#### 2.1 Test files and test functions

##### Test files

In Go, test files end with `_test.go`. For example, if you are testing code in the file `math.go`, the corresponding test file should be named `math_test.go`. This is how the Go toolchain recognizes and runs those test files.

##### Test functions

The signature of a test function should be `func TestXxx(t *testing.T)`, where `Xxx` is the name of the test and `t` is a parameter of type `*testing.T`, used to manage test state and record results.

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

// TestAdd tests the Add function
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5

    if result != expected {
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}
```

In the code above:
- `Add` is the function under test.
- `TestAdd` is the test function, used to verify that `Add` returns the expected result.
- `t.Errorf` records the details of a test failure.

#### 2.2 Running tests

Use the `go test` command to run tests. By default, Go finds every `_test.go` file in the current directory and its subdirectories and runs the tests inside.

**Basic command**:
```sh
go test
```

- `go test` compiles the test code and the code under test, then executes all the test functions.
- Test results are shown in the terminal.

**Verbose output**:
```sh
go test -v
```

- The `-v` flag enables verbose mode, which shows the output and result of every test.

**Run a specific test**:
```sh
go test -run TestAdd
```

- The `-run` flag runs only the test functions matching the given pattern. The command above runs only the `TestAdd` test.

**Run tests with a coverage report**:
```sh
go test -cover
```

- The `-cover` flag shows test coverage, i.e. what percentage of the source code the tests execute.

**Generate a coverage report**:
```sh
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

- The `-coverprofile` flag names the output file for coverage data.
- `go tool cover` turns that data into a coverage report you can view as HTML.

#### 2.3 Test output

Test functions can use the `t.Log` and `t.Logf` methods to record debug information, which is only shown when tests are run with the `-v` flag.

**Example**:
```go
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    expected := 5

    if result != expected {
        t.Logf("Testing Add(2, 3)")
        t.Errorf("Add(2, 3) = %d; want %d", result, expected)
    }
}
```

- `t.Logf` records debug information, which helps diagnose problems in a test.

#### 2.4 Handling test failures

A failed assertion is recorded with `t.Errorf` and the test keeps running; a fatal error stops the test on the spot with `t.Fatalf`.

**Example**:
```go
func TestDivide(t *testing.T) {
    result, err := Divide(4, 2)
    if err != nil {
        t.Fatalf("Divide(4, 2) failed: %v", err)
    }
    expected := 2
    if result != expected {
        t.Errorf("Divide(4, 2) = %d; want %d", result, expected)
    }
}
```

- `t.Fatalf` is used to stop a test and record the error when it hits a fatal failure.

### Summary

Put test functions in `_test.go`, run them with `go test`, use `-v` to see `t.Log` output, use `-cover` for coverage, and on failure `t.Errorf` prints the expected and actual values side by side.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)

## Sibling pages

- [Fuzz](/zh/test/Fuzz.md)
- [Test](/test/Test.md)
- [Advanced](/test/Advanced.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Advanced](/test/Advanced.md)
- [Benchmark](/test/Benchmark.md)
