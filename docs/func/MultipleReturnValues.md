In Go, a function can return multiple values, often used to deliver a computed result and related state information at the same time (for example, an error).

### Defining and calling a function that returns multiple values

#### Example: a simple multi-return function

```go
package main

import "fmt"

// define a function that returns the sum and difference of two integers
func sumAndDiff(a int, b int) (int, int) {
    sum := a + b
    diff := a - b
    return sum, diff
}

func main() {
    sum, diff := sumAndDiff(10, 5)
    fmt.Println("Sum:", sum)   // prints: Sum: 15
    fmt.Println("Diff:", diff) // prints: Diff: 5
}
```

In the example above:
- the `sumAndDiff` function returns two integers, `sum` and `diff`.
- when calling the function, the multi-assignment syntax is used to receive the return values.

### Using named return values

Go also supports named return values. In the function definition, the return values are named; these named return values are used as local variables inside the function, and the function can return them directly with a `return` statement.

#### Example: using named return values

```go
package main

import "fmt"

// use named return values
func sumAndDiff(a int, b int) (sum int, diff int) {
    sum = a + b
    diff = a - b
    return // return the named return values directly with return
}

func main() {
    sum, diff := sumAndDiff(10, 5)
    fmt.Println("Sum:", sum)   // prints: Sum: 15
    fmt.Println("Diff:", diff) // prints: Diff: 5
}
```

In the example above:
- the `sumAndDiff` function uses the named return values `sum` and `diff`.
- inside the function, values are assigned directly to `sum` and `diff`, and they are returned with a `return` statement.

### Common multi-return patterns

Multiple return values are widely used in Go, especially for error handling. Typically a function returns a result value and an error value.

#### Example: the error-handling pattern

```go
package main

import (
    "errors"
    "fmt"
)

// define a function that returns a result and an error
func divide(a int, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(10, 0)
    if err != nil {
        fmt.Println("Error:", err) // prints: Error: division by zero
    } else {
        fmt.Println("Result:", result)
    }
}
```

In the example above:
- the `divide` function returns two values: the computed result and a possible error.
- after calling the function, the error value `err` is checked; if there is an error, it is handled, otherwise the result value is used.

### Ignoring return values

In some cases, return values you do not need can be ignored. The blank identifier `_` can be used to discard them.

#### Example: ignoring return values

```go
package main

import "fmt"

func sumAndDiff(a int, b int) (int, int) {
    sum := a + b
    diff := a - b
    return sum, diff
}

func main() {
    sum, _ := sumAndDiff(10, 5)
    fmt.Println("Sum:", sum) // prints: Sum: 15
}
```

In the example above:
- when calling the `sumAndDiff` function, the difference `diff` is ignored and only the sum `sum` is received.

### Summary

Multiple return values mean a function does not have to define a separate struct just to bring back an error; `(value, error)` is the most common combination. Named return values write the meaning into the function signature, so reading the signature tells you what each return value is; values you do not need are discarded with `_`.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Effective Go · multiple returns](https://go.dev/doc/effective_go#multiple-returns)


## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [InnerFunc](/func/InnerFunc.md)
- [RecursiveFunction](/func/RecursiveFunction.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [InnerFunc](/func/InnerFunc.md)
- [RecursiveFunction](/func/RecursiveFunction.md)
