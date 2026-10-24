# Anonymous Functions and Closures
Anonymous functions and closures often show up together, but they aren't the same thing: the former are functions without names, the latter are function values that carry variables from an outer scope. Below I look at each syntax on its own, then show how they combine.

### Anonymous Functions

**Anonymous functions** are functions without a name, usually used in one-off situations: passed as an argument, or defined inline as a callback.

#### Syntax

```go
func(parameter_list) return_type {
    // function body
}
```

#### Example: basic usage

```go
package main

import "fmt"

func main() {
    // define an anonymous function and call it immediately
    func(message string) {
        fmt.Println(message)
    }("Hello, World!")
}
```

In this example the anonymous function is defined and called immediately. It takes one argument, `message`, and prints it.

### Closures

A **closure** is a function value that references variables from an outer scope. Even after the function that defined it has returned, the closure can still read and write the variables it captured.

#### Characteristics

- A closure can capture and modify variables from the scope where it was created; those variables stay alive after the original function returns.

#### Example: basic usage

```go
package main

import "fmt"

// return a closure
func createCounter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

func main() {
    // create a closure
    counter := createCounter()
    
    // call the closure
    fmt.Println(counter()) // prints: 1
    fmt.Println(counter()) // prints: 2
    fmt.Println(counter()) // prints: 3
}
```

In this example, `createCounter` returns a closure that captures the `count` variable. Each time the closure is called it increments and returns `count`.

### Combining Anonymous Functions and Closures

Anonymous functions can be used to create closures, which is one of their common uses.

#### Example: combining an anonymous function and a closure

```go
package main

import "fmt"

func main() {
    // define a closure using an anonymous function
    multiplier := func(factor int) func(int) int {
        return func(value int) int {
            return value * factor
        }
    }

    // create a closure that multiplies by 2
    double := multiplier(2)
    // create a closure that multiplies by 10
    tenTimes := multiplier(10)

    fmt.Println("Double 3:", double(3))     // prints: Double 3: 6
    fmt.Println("Ten times 3:", tenTimes(3)) // prints: Ten times 3: 30
}
```

In this example, `multiplier` is an anonymous function that returns a closure. The closure captures the `factor` variable, which lets `double` and `tenTimes` compute with different multipliers.

### Summary

- **Anonymous function**: a function without a name, typically used for one-off tasks or as a callback.
- **Closure**: a function value that captures and can modify variables from its outer scope. The closure can still access those captured variables after the function returns.

The `createCounter` example is a textbook closure: the function returns, `count` is still alive, and each call to `counter()` adds one on top of the last call's value.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Language Spec · Function literals](https://go.dev/ref/spec#Function_literals)

## Sibling pages

- [Arguments](/func/Arguments.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Arguments](/func/Arguments.md)
- [DefineAndCall](/func/DefineAndCall.md)
- [FuncValue](/func/FuncValue.md)
- [History](/func/History.md)
- [InnerFunc](/func/InnerFunc.md)
- [MultipleReturnValues](/func/MultipleReturnValues.md)
- [RecursiveFunction](/func/RecursiveFunction.md)
- [glossary](/glossary.md)
