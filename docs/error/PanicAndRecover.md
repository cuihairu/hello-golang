`panic` and `recover` are two built-in mechanisms in Go for handling runtime errors: `panic` immediately breaks the current flow of execution, and `recover` can catch it inside a `defer`.

### `panic`

`panic` triggers a runtime error that immediately interrupts the control flow. `panic` breaks the current execution and begins unwinding up through the call stack, executing `defer` statements one level at a time, until the program terminates.

#### Using `panic`

`panic` is typically used when the program hits an unrecoverable error, such as an error state that should never occur, or a programming mistake.

**Example:**

```go
package main

import "fmt"

func causePanic() {
    panic("something went wrong")
}

func main() {
    causePanic()
    fmt.Println("This will not be executed")
}
```

**Output:**

```
panic: something went wrong

goroutine 1 [running]:
main.causePanic()
        /path/to/file.go:6 +0x39
main.main()
        /path/to/file.go:10 +0x20
exit status 2
```

### `recover`

`recover` pulls the flow back out of a `panic`. It can only be called from inside a `defer` statement, and it catches the `panic` occurring on the current goroutine, so the program does not crash.

#### Using `recover`

1. Call `recover` from within a `defer` statement.
2. If a `panic` has occurred, `recover` returns the argument passed to `panic` (usually an error message) and restores normal execution.
3. If no `panic` occurred, `recover` returns `nil`.

**Example:**

```go
package main

import "fmt"

func recoverFromPanic() {
    if r := recover(); r != nil {
        fmt.Println("Recovered from panic:", r)
    }
}

func causePanic() {
    defer recoverFromPanic()
    panic("something went wrong")
}

func main() {
    causePanic()
    fmt.Println("Recovered and continuing execution")
}
```

**Output:**

```
Recovered from panic: something went wrong
Recovered and continuing execution
```

### The relationship between `panic` and `recover`

- **`panic`**: triggers a runtime error, terminates normal execution, and begins executing `defer` statements level by level.
- **`recover`**: catches a `panic`; it is called from a `defer` statement and can restore normal execution.

### Use cases

- **`panic`**: typically used for serious errors that should not be recovered from (such as an unrecoverable state) and where you want to terminate the program.
- **`recover`**: used to catch and handle a `panic` in a specific part of the program, so the program can recover from the exception and keep going.

### Limitations and caveats

- **`recover` can only be called from `defer`**: `recover` only takes effect in the execution context of a `defer` statement. If you use `recover` in an ordinary function call, it will not work.
- **Avoid overusing `panic` and `recover`**: while `panic` and `recover` provide a mechanism for handling exceptions, they should not be used for routine error handling. Typically you use error return values (such as Go's `error` type) for anticipated errors; `panic` and `recover` are mainly for catching unexpected and serious errors.

### Assembly example

A simplified assembly sketch, just to make the relationship among the three clear; real assembly is far more complex:

```assembly
TEXT main.main(SB), NOSPLIT, $0
	// function entry
	// call causePanic
	CALL main.causePanic(SB)
	// handle panic recovery
	// ...
	// continue execution
	// ...
	RET

TEXT main.causePanic(SB), NOSPLIT, $0
	// set up the deferred function, calling recoverFromPanic
	// ...
	// trigger the panic
	// ...
	// ...
	RET

TEXT main.recoverFromPanic(SB), NOSPLIT, $0
	// catch the panic
	// ...
	// resume normal execution
	// ...
	RET
```


### The return value of `recover`

In Go 1.18 and later, `recover` returns a value of type `any`, not `error`. That is because the return value of `recover` can be of any type: it is usually a value describing the error or `nil`, depending on the argument passed to `panic`.

#### The return type of `recover`

`recover` returns a value of type `any`, which lets it catch and recover from `panic` values of different types. `any` is a new type introduced in Go 1.18; it is an alias for `interface{}` and can represent a value of any type.

#### Example

Change the argument to `panic` to an integer, and `recover` gets that integer:

```go
package main

import (
    "fmt"
)

func recoverFromPanic() {
    if r := recover(); r != nil {
        fmt.Printf("Recovered from panic with value: %v\n", r)
    }
}

func causePanic() {
    defer recoverFromPanic()
    panic(123)  // an integer panic
    // panic("something went wrong")  // a string panic
}

func main() {
    causePanic()
    fmt.Println("Recovered and continuing execution")
}
```

**Output:**

```
Recovered from panic with value: 123
Recovered and continuing execution
```

#### The implementation of `recover` in the Go source

The details of `recover`'s implementation can be found in the Go runtime source. The following is a snippet of the relevant code from the Go runtime library (pseudocode):

```go
// runtime/recover.go
func recover() any {
    if r := getPanicValue(); r != nil {
        return r
    }
    return nil
}

// getPanicValue retrieves the value from the current goroutine's panic state
func getPanicValue() any {
    // the real implementation involves more low-level detail
    // this is just a sketch
}
```

In the real Go runtime, `recover`'s implementation checks and handles the current goroutine's panic state. The actual source contains more low-level detail to support goroutine stack management and the exception-recovery mechanism.

#### Summary

- **The return type of `recover`**: `recover` returns a value of type `any`, which can represent a value of any type; this was introduced in Go 1.18 and later.
- **The purpose of `recover`**: catch and handle a `panic` to prevent the program from crashing.
- **Source implementation**: `recover`'s actual implementation involves low-level handling in the runtime library to support exception recovery for goroutines.


### `panic` with other types

What `recover` gets is not necessarily an `error`; `panic` returns whatever it was passed. Three examples:

#### Example 1: `panic` with an integer

```go
package main

import "fmt"

func recoverFromPanic() {
    if r := recover(); r != nil {
        fmt.Printf("Recovered from panic with value: %v (type: %T)\n", r, r)
    }
}

func causePanic() {
    defer recoverFromPanic()
    panic(123)  // panic with an integer
}

func main() {
    causePanic()
    fmt.Println("Recovered and continuing execution")
}
```

**Output:**

```
Recovered from panic with value: 123 (type: int)
Recovered and continuing execution
```

In this example `panic` is called with the integer `123`; the value `recover` catches is that integer, of type `int`.

#### Example 2: `panic` with a string

```go
package main

import "fmt"

func recoverFromPanic() {
    if r := recover(); r != nil {
        fmt.Printf("Recovered from panic with value: %v (type: %T)\n", r, r)
    }
}

func causePanic() {
    defer recoverFromPanic()
    panic("something went wrong")  // panic with a string
}

func main() {
    causePanic()
    fmt.Println("Recovered and continuing execution")
}
```

**Output:**

```
Recovered from panic with value: something went wrong (type: string)
Recovered and continuing execution
```

In this example `panic` is called with the string `"something went wrong"`; the value `recover` catches is that string, of type `string`.

#### Example 3: `panic` with a custom struct

```go
package main

import "fmt"

// CustomError is a custom error type
type CustomError struct {
    Code    int
    Message string
}

func (e *CustomError) Error() string {
    return fmt.Sprintf("Code: %d, Message: %s", e.Code, e.Message)
}

func recoverFromPanic() {
    if r := recover(); r != nil {
        fmt.Printf("Recovered from panic with value: %v (type: %T)\n", r, r)
    }
}

func causePanic() {
    defer recoverFromPanic()
    panic(&CustomError{Code: 404, Message: "Not Found"})  // panic with a custom error
}

func main() {
    causePanic()
    fmt.Println("Recovered and continuing execution")
}
```

**Output:**

```
Recovered from panic with value: &{404 Not Found} (type: *main.CustomError)
Recovered and continuing execution
```

In this example `panic` is called with an instance of the custom struct `CustomError`; the value `recover` catches is that struct instance, of type `*main.CustomError`.

#### Summary

- **The type of `recover`'s return value**: `recover` can catch and return a value of any type, which means the value passed to `panic` can be an `int`, a `string`, a custom struct, and so on.
- **Error type is not the only option**: `error` is a common choice, but `panic` can carry other types too — `recover` returns whatever it catches.


### Summary

- **`panic`**: triggers a runtime error and terminates normal execution.
- **`recover`**: catches a `panic` and restores normal execution; it must be called from `defer`.
- **Use cases**: `panic` for serious errors, `recover` for catching and handling exceptions so the program does not crash.

Anticipated errors are handled with `error` return values; `panic`/`recover` is reserved for states that should not happen. Keeping those two lanes separate is what keeps the program from being both slow and hard to debug.

## References

- [Official blog · Error handling and Go](https://go.dev/blog/error-handling-and-go)
- [Official blog · Errors are values](https://go.dev/blog/errors-are-values)
- [errors standard library](https://pkg.go.dev/errors)
- [Effective Go · Errors](https://go.dev/doc/effective_go#errors)
- [Official blog · Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
- [Language spec · Defer statement (including panic/recover handling)](https://go.dev/ref/spec#Handling_panics)
- [Effective Go · Panic/Recover](https://go.dev/doc/effective_go#panic)

<!-- BACKLINKS-AUTO -->
## Related pages

- [ErrorType](/error/ErrorType.md)
- [glossary](/glossary.md)
