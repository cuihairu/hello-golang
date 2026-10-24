# Function Values
In Go, functions are first-class objects: they can be assigned to variables, passed as arguments, and returned as return values. Higher-order functions and callbacks are all built on this.

### Function Values

A function value is just the value of a function itself; once assigned to a variable, it is called the same way as any other function.

#### Defining and using a function value

A function value has three destinations: assigned to a variable and called directly; passed as an argument to another function so the caller decides what to do; or returned from a function so the caller gets a piece of executable logic. The examples below cover these three in order.

### Example: basic usage

#### Defining a function value

```go
package main

import "fmt"

// define a function
func add(a int, b int) int {
    return a + b
}

func main() {
    // assign the function to a variable
    var addFunc func(int, int) int
    addFunc = add

    // call the function value
    result := addFunc(3, 4)
    fmt.Println("Result:", result) // prints: Result: 7
}
```

#### A function value as an argument

```go
package main

import "fmt"

// define a function type
type IntOperation func(int, int) int

// a function that takes a function value as an argument
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

#### A function value as a return value

```go
package main

import "fmt"

// return a function value
func getOperation(op string) func(int, int) int {
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

### Higher-Order Functions

A function that takes function arguments, or returns functions, is called a higher-order function. `createMultiplier` is one: call it once and you get back a new function bound to `factor`.

#### Example: a higher-order function

```go
package main

import "fmt"

// define a higher-order function
func createMultiplier(factor int) func(int) int {
    return func(value int) int {
        return value * factor
    }
}

func main() {
    // create a function that multiplies by 2
    double := createMultiplier(2)
    // create a function that multiplies by 10
    tenTimes := createMultiplier(10)

    fmt.Println("Double 3:", double(3))     // prints: Double 3: 6
    fmt.Println("Ten times 3:", tenTimes(3)) // prints: Ten times 3: 30
}
```

### Summary

A function value has three destinations, and each of the three examples takes one: `addFunc = add` assigns it to a variable, `compute(3, 4, add)` passes it as an argument, and `getOperation("add")` returns it. Function types can be declared on your own; `IntOperation` is just an alias for `func(int, int) int`, used specifically as a parameter type.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Language Spec · Function literals](https://go.dev/ref/spec#Function_literals)


## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [DefineAndCall](/func/DefineAndCall.md)
- [History](/func/History.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [DefineAndCall](/func/DefineAndCall.md)
- [History](/func/History.md)
