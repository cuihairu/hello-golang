# Testing

Go tests don't need a framework; the standard library `testing` package alone is enough: unit tests check that a feature works, benchmarks measure elapsed time, and example tests show how the code is used. This page records how to write each of those three kinds of test and how to read coverage.

#### 1.1 The role of tests

Tests answer two questions: before changing code, confirm it is currently correct; after changing it, confirm nothing broke. Concretely:

- **Verify functionality**: the code's output matches what is expected.
- **Find defects**: errors surface in tests instead of waiting to blow up in production.
- **Support refactoring**: there is a safety net of checks when restructuring.
- **Documentation value**: an example test is itself a runnable usage guide.

#### 1.2 Overview of Go's test framework

All of Go's testing capability lives in the standard library `testing` package, and a single `go test` command runs it. The main features are:

- **Basic tests**: verify whether the code's functionality is correct.
- **Benchmark tests**: measure the code's performance, i.e. how long an operation takes.
- **Example tests**: demonstrate how the code is used and verify the examples are correct.
- **Test coverage**: assess how much of the code the tests reach.

## References

- [testing standard library](https://pkg.go.dev/testing)
- [Go Official Documentation · Add a test (external link)](https://go.dev/doc/tutorial/add-a-test)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Advanced](/test/Advanced.md)
- [BaseTest](/test/BaseTest.md)
- [Benchmark](/test/Benchmark.md)
- [Cover](/test/Cover.md)
- [Example](/test/Example.md)
- [Lib](/zh/test/Lib.md)
- [Practice](/zh/test/Practice.md)
