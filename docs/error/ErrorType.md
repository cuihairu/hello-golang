### The concept of errors

In Go, the basic unit of error handling is the `error` type. `error` is a built-in interface that defines the basic behaviour of an error message. A function reports success or failure by returning a value of type `error`. On success it usually returns `nil`; on failure it returns a concrete implementation of `error`.

### The `error` type

The `error` type is an interface, defined in the `errors` package. Its definition looks like this:

```go
type error interface {
    Error() string
}
```

- The `error` interface has only one method: `Error()`, which returns a string describing the error.

### Creating and using errors

#### 1. Using `errors.New`

`errors.New` creates a new error. It takes a string argument as the error message and returns an error value that implements the `error` interface.

**Example:**

```go
package main

import (
    "errors"
    "fmt"
)

func doSomething() error {
    return errors.New("something went wrong")
}

func main() {
    err := doSomething()
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

#### 2. Using `fmt.Errorf`

`fmt.Errorf` creates a formatted error message. It lets you use a format string and variadic arguments to build a complex error message.

**Example:**

```go
package main

import (
    "fmt"
)

func doSomething(value int) error {
    if value < 0 {
        return fmt.Errorf("invalid value: %d is less than 0", value)
    }
    return nil
}

func main() {
    err := doSomething(-1)
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

### Custom error types

In Go you can define a custom error type by declaring a struct and implementing the `error` interface. The struct's fields (such as an error code) travel along with the error.

**Example:**

```go
package main

import (
    "fmt"
)

// MyError defines a custom error type
type MyError struct {
    Code    int
    Message string
}

// Error implements the error interface
func (e *MyError) Error() string {
    return fmt.Sprintf("Code: %d, Message: %s", e.Code, e.Message)
}

func doSomething() error {
    return &MyError{Code: 404, Message: "Resource not found"}
}

func main() {
    err := doSomething()
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

### Error-handling patterns

In Go, error handling usually follows this pattern:

1. **Check the error**: after calling a function that may return an error, inspect the `error` return value. If it is not `nil`, handle it.

2. **Return the error**: when an error occurs, a function returns a non-`nil` `error` value.

3. **Handle the error**: handle the error at the call site, taking whatever action the situation calls for, such as logging it or retrying the operation.

**Example:**

```go
package main

import (
    "fmt"
    "os"
)

func readFile(fileName string) ([]byte, error) {
    data, err := os.ReadFile(fileName)
    if err != nil {
        return nil, fmt.Errorf("failed to read file %s: %w", fileName, err)
    }
    return data, nil
}

func main() {
    data, err := readFile("nonexistent_file.txt")
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("File content:", string(data))
}
```

In the example above, `readFile` attempts to read a file; if it fails, it returns an error carrying detailed error information. `main` checks and handles those errors.

### Summary

- **The `error` type**: a built-in interface in Go used to represent errors. The `error` interface contains only an `Error()` method, used to return a description of the error.
- **Creating errors**:
  - Use `errors.New` to create simple errors.
  - Use `fmt.Errorf` to create formatted error messages.
- **Custom error types**: create a custom error type by defining a struct and implementing the `error` interface.
- **Error-handling patterns**: manage errors by checking the error value (whether it is `nil`), returning errors, and handling errors.

An error is simply a value that implements `Error() string`, passed around like any other return value; each layer in the call chain can either handle it or wrap it with `fmt.Errorf` and `%w` and keep passing it up.

## References

- [Official blog · Error handling and Go](https://go.dev/blog/error-handling-and-go)
- [Official blog · Errors are values](https://go.dev/blog/errors-are-values)
- [errors standard library](https://pkg.go.dev/errors)
- [Effective Go · Errors](https://go.dev/doc/effective_go#errors)

## Sibling pages

- [Error](/error/Error.md)
- [Errors](/error/Errors.md)
- [PanicAndRecover](/error/PanicAndRecover.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Error](/error/Error.md)
