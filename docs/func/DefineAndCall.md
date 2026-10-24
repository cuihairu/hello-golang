# Defining and calling functions
In Go, a function can be defined in the standard `func` way, and you can also create a function type via a type definition. Once a function becomes a type, it can be passed and manipulated like any value.

### Defining functions

#### Basic syntax

The basic form of a function definition looks like this:

```go
func functionName(parameterList) (returnType) {
    // function body
}
```

#### Example: a simple function

```go
package main

import "fmt"

// define a function
func add(a int, b int) int {
    return a + b
}

func main() {
    result := add(3, 4)
    fmt.Println("Result:", result) // prints: Result: 7
}
```

### Defining function types

Go allows defining function types with the `type` keyword. Such a type definition can be used to declare function-typed variables, or as a function parameter or return value.

#### Basic syntax

```go
type FunctionNameType func(parameterList) (returnType)
```

#### Example: defining and using a function type

```go
package main

import "fmt"

// define a function type
type IntOperation func(int, int) int

// define two functions matching the IntOperation type
func add(a int, b int) int {
    return a + b
}

func multiply(a int, b int) int {
    return a * b
}

func main() {
    // use a variable defined with the function type
    var op IntOperation

    // assign the add function to op
    op = add
    fmt.Println("Add:", op(3, 4)) // prints: Add: 7

    // assign the multiply function to op
    op = multiply
    fmt.Println("Multiply:", op(3, 4)) // prints: Multiply: 12
}
```

### Using a function type as a parameter

A function type can be passed as a parameter to another function: `compute` does not care whether it is adding or multiplying — what actually gets computed is decided by the function the caller passes in.

#### Example: a function as a parameter

```go
package main

import "fmt"

// define a function type
type IntOperation func(int, int) int

// define a function that accepts an IntOperation argument
func compute(a int, b int, op IntOperation) int {
    return op(a, b)
}

func add(a int, b int) int {
    return a + b
}

func multiply(a int, b int) int {
    return a * b
}

func main() {
    fmt.Println("Add:", compute(3, 4, add))        // prints: Add: 7
    fmt.Println("Multiply:", compute(3, 4, multiply)) // prints: Multiply: 12
}
```

### Using a function type as a return value

A function type can also be used as a return value; the caller gets a different function depending on the condition, and calls it as usual once it has it.

#### Example: a function as a return value

```go
package main

import "fmt"

// define a function type
type IntOperation func(int, int) int

// return a function, selecting the function based on the operation type
func getOperation(op string) IntOperation {
    switch op {
    case "add":
        return func(a int, b int) int { return a + b }
    case "multiply":
        return func(a int, b int) int { return a * b }
    default:
        return nil
    }
}

func main() {
    addOp := getOperation("add")
    multiplyOp := getOperation("multiply")

    if addOp != nil {
        fmt.Println("Add:", addOp(3, 4)) // prints: Add: 7
    }
    if multiplyOp != nil {
        fmt.Println("Multiply:", multiplyOp(3, 4)) // prints: Multiply: 12
    }
}
```

### Summary

In Go, defining and calling functions is very flexible:
- functions can be defined and called with the standard `func` keyword.
- functions can be used as types, with function types defined via the `type` keyword.
- function types can be used as function parameters or return values.

Once functions go back and forth as parameters and return values, callbacks and strategy selection do not need a separate set of interfaces. In the examples, `IntOperation` is used in both a parameter and a return value, and the syntax is the same.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)


## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [FuncValue](/func/FuncValue.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [FuncValue](/func/FuncValue.md)
