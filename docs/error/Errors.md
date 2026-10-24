Go's error handling is built around the `error` return value; `panic`/`recover` is reserved for genuinely unrecoverable situations, and the standard library `errors` adds comparison, unwrapping, and root-cause extraction. The common practices follow:

### 1. Returning an `error` type

Go's standard error-handling approach is for a function to return a value of type `error` through its return values. `error` is a built-in interface type used to represent error information.

#### Example

```go
package main

import (
    "fmt"
    "errors"
)

// the function returns an error
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err)
        return
    }
    fmt.Println("Result:", result)
}
```

In this example the `divide` function returns two values: the result and an `error`. If something goes wrong (such as dividing by zero), the function returns a non-`nil` `error` value, and the caller can inspect that error value and handle it accordingly.

### 2. Custom error types

Beyond creating simple errors with `errors.New`, you can create custom error types that carry more context. Custom error types usually implement the `error` interface.

#### Example

```go
package main

import (
    "fmt"
)

// CustomError is a custom error type
type CustomError struct {
    Code    int
    Message string
}

func (e *CustomError) Error() string {
    return fmt.Sprintf("Code %d: %s", e.Code, e.Message)
}

// the function returns a custom error
func doSomething() error {
    return &CustomError{Code: 404, Message: "Not Found"}
}

func main() {
    err := doSomething()
    if err != nil {
        fmt.Println("Error:", err)
    }
}
```

In this example the custom error type `CustomError` carries an error code and message, and implements the `Error` method.

### 3. The `errors` package

Go's `errors` package provides several utility functions for creating and handling errors. Functions in the package include:

- `errors.New`: creates a basic error.
- `errors.Is`: reports whether any error in the chain equals the target error (usually used together with sentinel error variables).
- `errors.As`: converts the error to a specific error type.
- `errors.Unwrap`: retrieves the wrapped underlying error.

#### Example

Note: `errors.Is` decides by comparing error values (pointer equality), so the target must be a sentinel error variable, not a freshly constructed `&CustomError{}` each time.

```go
package main

import (
    "errors"
    "fmt"
)

// CustomError is a custom error type
type CustomError struct {
    Code    int
    Message string
}

func (e *CustomError) Error() string {
    return fmt.Sprintf("Code %d: %s", e.Code, e.Message)
}

// ErrNotFound is a sentinel error
var ErrNotFound = &CustomError{Code: 404, Message: "Not Found"}

func doSomething() error {
    return ErrNotFound
}

func main() {
    err := doSomething()

    if errors.Is(err, ErrNotFound) {
        fmt.Println("CustomError detected")
    }

    var customErr *CustomError
    if errors.As(err, &customErr) {
        fmt.Printf("CustomError with code %d\n", customErr.Code)
    }
}
```

### 4. Error wrapping

Error wrapping means attaching more context to an error as you return it. Go 1.13 introduced error wrapping, done through `fmt.Errorf` with the `%w` verb.

#### Example

```go
package main

import (
    "fmt"
    "errors"
)

// errOriginal is a sentinel error, for comparison with errors.Is
var errOriginal = errors.New("original error")

func doSomething() error {
    return fmt.Errorf("failed to do something: %w", errOriginal)
}

func main() {
    err := doSomething()
    if err != nil {
        fmt.Println("Error:", err)
        if errors.Is(err, errOriginal) {
            fmt.Println("The error is the original error")
        }
    }
}
```

### 5. Best practices for error handling

- **Early return**: for error handling, early returns are the usual way to keep the code simple.
  
  ```go
  func process() error {
      if err := doSomething(); err != nil {
          return err
      }
      // keep processing
      return nil
  }
  ```

- **Wrap errors**: wrap the error at a higher-level function and add extra context, to help with debugging and understanding why the error happened.

  ```go
  func main() {
      if err := process(); err != nil {
          fmt.Printf("Error occurred: %v\n", err)
      }
  }
  ```

### Summary

- **Returning an `error` type**: Go's standard error-handling approach — handle errors inside a function by returning an `error` value.
- **Custom error types**: create custom error types to carry more context.
- **The `errors` package**: provides practical functions for creating and handling errors.
- **Error wrapping**: use `fmt.Errorf` with the `%w` verb to wrap errors and attach more context.
- **Best practices**: use early returns and error wrapping to simplify error handling and improve maintainability.

Which one to pick depends on whether the caller needs the error's details: equality checks go with `errors.Is`, extracting fields goes with `errors.As`, and adding clues for debugging goes with `%w` wrapping.

## References

- [Official blog · Error handling and Go](https://go.dev/blog/error-handling-and-go)
- [Official blog · Errors are values](https://go.dev/blog/errors-are-values)
- [errors standard library](https://pkg.go.dev/errors)
- [Effective Go · Errors](https://go.dev/doc/effective_go#errors)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ErrorType](/error/ErrorType.md)
- [glossary](/glossary.md)
