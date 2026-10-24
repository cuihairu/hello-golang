### Example tests

Example tests are a special form of Go test: write a function with an expected output, and it both demonstrates how the function is used and verifies that the output is what was expected. Unlike a normal test or a benchmark, it contains no assertions — it only compares standard output.

#### 4.1 What an example test is

An example test is a function named `ExampleXxx`, where `Xxx` is the example's name and `Example` is the prefix. An example test has the signature `func ExampleXxx()`, with no parameters and no return values. Example tests usually print the expected result to standard output (with `fmt.Println`).

**Example**:
```go
// math.go
package math

import "fmt"

// Add returns the sum of two integers
func Add(a, b int) int {
    return a + b
}

// math_test.go
package math

import "fmt"

// ExampleAdd shows how to use the Add function
func ExampleAdd() {
    result := Add(2, 3)
    fmt.Println(result)
    // Output: 5
}
```

In the code above:
- `ExampleAdd` is the example test function, showing how to use `Add`.
- `fmt.Println(result)` prints the function's result.
- The comment `// Output: 5` specifies the expected output.

#### 4.2 Running example tests

Example tests can be run with the `go test` command. When tests run, the Go test framework executes every example test and checks whether its output matches the expected result in the comment.

**Basic command**:
```sh
go test
```

- `go test` runs all example tests automatically and checks whether the actual output matches the expected output.

#### 4.3 Example test output

The output of an example test is used to verify the example code. During execution, the Go test framework compares the actual output with the expected output. If they do not match, the test fails and prints an error message.

**Example output**:
```sh
go test
```
```
--- FAIL: ExampleAdd (0.00s)
    math_test.go:12: example output does not match expectation:
        got: 6
        want: 5
```

- `--- FAIL` means the test failed.
- The error message shows that the actual output does not match the expected output.

#### 4.4 What example tests are for

1. **Documentation**: an example test serves as documentation for the code, showing how to use a function and what it is expected to do.
2. **Verifying examples**: ensure the code samples in the documentation are correct and do not rot as the code changes.
3. **Teaching**: help newcomers learn how to use a particular function or method, with a real example showing its behavior.

#### 4.5 Best practices for writing example tests

1. **State the expected output clearly**: make sure the example test's comment contains an explicit expected output so results are verified correctly.
2. **Keep the code short**: the example code should show only the basic usage and expected behavior of the function.
3. **Cover boundary conditions**: consider adding example tests that show how the function behaves with different kinds of input.

**Example**:
```go
// ExampleAddNegative shows how to use Add with negative numbers
func ExampleAddNegative() {
    result := Add(-2, -3)
    fmt.Println(result)
    // Output: -5
}

// ExampleAddZero shows how to use Add with zero
func ExampleAddZero() {
    result := Add(0, 5)
    fmt.Println(result)
    // Output: 5
}
```

### Summary

An example test does double duty: it is a test, because `go test` compares the actual output against the `// Output:` comment and fails on a mismatch; and it is documentation, because the example next to a function tells callers directly how to use it. If the code changes and the documentation example is not updated, the test goes red first.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)


## Sibling pages

- [Fuzz](/zh/test/Fuzz.md)
- [Test](/test/Test.md)
- [Advanced](/test/Advanced.md)
- [Cover](/test/Cover.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Cover](/test/Cover.md)
