### Testing best practices

Tests make sure a change did not break something else. Go tests are written in `_test.go` files and run with `go test`; here I organize practices across five areas: maintainability, coverage, strategy, exception handling, and CI.

#### 8.1 Writing maintainable test code

1. **Keep tests concise**:
   - Test code should not pile up complex logic.
   - Each test function should focus on one specific feature or behavior.

2. **Use table-driven tests**:
   - Organize test cases with table-driven tests, which are easy to maintain and extend.
   - Define an array of structs describing the various inputs and expected outputs, then loop over them.

   **Example**:
   ```go
   // example_test.go
   package example

   import "testing"

   func TestAdd(t *testing.T) {
       tests := []struct {
           a, b, expected int
       }{
           {1, 1, 2},
           {2, 2, 4},
           {2, 3, 5},
       }

       for _, test := range tests {
           result := Add(test.a, test.b)
           if result != test.expected {
               t.Errorf("Add(%d, %d) = %d; want %d", test.a, test.b, result, test.expected)
           }
       }
   }
   ```

3. **Make tests descriptive**:
   - Test function names should clearly describe the purpose and expected behavior of the test.
   - Use `t.Error` or `t.Errorf` to print clear error messages that help locate the problem quickly.

4. **Organize test files**:
   - Put test code in the same package as the code under test, in `_test.go` files.
   - Organize test files by functional module so the code structure stays clear.

#### 8.2 Test coverage

1. **Monitor test coverage**:
   - Use Go's built-in coverage tooling to check test coverage and make sure important code paths are covered.
   - Review coverage reports regularly to identify untested parts of the code.

2. **Do not over-chase high coverage**:
   - High coverage does not mean high-quality tests. Make sure your test cases cover the real business logic and the critical paths.

3. **Combine with other test types**:
   - Beyond unit tests, include integration tests, end-to-end tests, and so on, to ensure comprehensive coverage.

#### 8.3 An efficient testing strategy

1. **Avoid test side effects**:
   - Tests should be independent and free of side effects; each test should start from the same initial state.
   - Use `setup` and `teardown` functions to initialize and clean up the test environment.

2. **Use mocks and stubs**:
   - Use mock objects and stubs to isolate tests, avoiding dependence on external systems such as databases or network services.
   - The commonly used libraries are `gomock` and `testify`.

3. **Write performance tests**:
   - Use benchmarking to assess the code's performance and make sure it meets performance requirements.
   - Run performance tests regularly to watch for performance shifts and optimize the code.

   **Example**:
   ```go
   // example_benchmark_test.go
   package example

   import "testing"

   func BenchmarkAdd(b *testing.B) {
       for i := 0; i < b.N; i++ {
           Add(1, 2)
       }
   }
   ```

4. **Parallel tests**:
   - Take advantage of Go's concurrency by calling `t.Parallel()` to run tests in parallel and shorten total test time.
   - Make sure the test code is thread-safe and does not introduce data races.

   **Example**:
   ```go
   func TestParallel(t *testing.T) {
       t.Parallel()
       // test logic
   }
   ```

#### 8.4 Exception handling and error handling

1. **Test exceptional cases**:
   - Write test cases that verify how a function behaves with abnormal input or under error conditions.
   - Use `t.Errorf` to print clear error messages that help locate the problem.

2. **Verify error return values**:
   - Make sure a function returns the correct error information when handling a failure, and that the error is handled appropriately.
   - Use assertion methods such as `assert.Error` to check errors.

   **Example**:
   ```go
   func TestErrorHandling(t *testing.T) {
       _, err := Divide(1, 0)
       if err == nil {
           t.Errorf("Expected error, got nil")
       }
   }
   ```

#### 8.5 Automating tests and continuous integration

1. **Automate test runs**:
   - Integrate tests into the CI pipeline so tests run automatically on every code change.
   - Use CI tools (such as GitHub Actions, GitLab CI, and Jenkins) to run tests automatically and generate reports.

2. **Test reports and feedback**:
   - Configure the CI tool to generate test reports and check results after every build.
   - Set up alerts and notifications so failures are responded to and fixed promptly.

#### 8.6 A practical example

```go
// example_test.go
package example

import (
    "testing"
)

// the function under test
func Add(a, b int) int {
    return a + b
}

// unit test
func TestAdd(t *testing.T) {
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// parallel test
func TestAddParallel(t *testing.T) {
    t.Parallel()
    result := Add(2, 3)
    if result != 5 {
        t.Errorf("Add(2, 3) = %d; want 5", result)
    }
}

// benchmark test
func BenchmarkAdd(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Add(2, 3)
    }
}
```

### Summary

Table-driven tests, benchmarks, and `t.Parallel()` all come from the standard library `testing` package; coverage comes from the built-in tools, and mocking and assertions from `gomock` and `testify`. Hook all of this into CI and it runs on every commit.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)


## Sibling pages

- [Fuzz](/test/Fuzz.md)
- [Test](/test/Test.md)
- [Advanced](/test/Advanced.md)
- [Lib](/test/Lib.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Lib](/test/Lib.md)
