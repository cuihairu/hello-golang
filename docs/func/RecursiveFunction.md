In Go, a **recursive function** is a function that calls itself in its own definition. Recursion is a programming technique typically used to solve problems that can be decomposed into smaller subproblems of the same kind. A recursive function generally includes two main parts:

1. **Base case**: the termination condition of the recursion, preventing infinite recursion.
2. **Recursive step**: breaks the problem into one or more subproblems and calls itself recursively.

### Basic usage

The key to a recursive function is ensuring that each recursive call moves closer to the base case, thereby avoiding an infinite loop. Typically, each recursive call solves a smaller subproblem until the base case is reached.

#### Example: computing the factorial

The factorial is a classic recursion problem, defined as \( n! = n \times (n-1) \times (n-2) \times \ldots \times 1 \), with \( 0! = 1 \).

**Example of a recursive factorial function in Go:**

```go
package main

import "fmt"

// a recursive function to compute the factorial
func factorial(n int) int {
    // base case
    if n <= 1 {
        return 1
    }
    // recursive step
    return n * factorial(n-1)
}

func main() {
    fmt.Println(factorial(5)) // prints: 120
}
```

In this example, the `factorial` function calls itself to compute the factorial. The base case is `n <= 1`, where the function returns 1. The recursive step is multiplying `n` by `factorial(n-1)`.

#### Example: the Fibonacci sequence

The Fibonacci sequence is another classic recursion problem, where each number is the sum of the two preceding ones. Defined as: \( F(n) = F(n-1) + F(n-2) \), with \( F(0) = 0 \) and \( F(1) = 1 \).

**Example of a recursive Fibonacci function in Go:**

```go
package main

import "fmt"

// a recursive function to compute the Fibonacci sequence
func fibonacci(n int) int {
    // base case
    if n <= 1 {
        return n
    }
    // recursive step
    return fibonacci(n-1) + fibonacci(n-2)
}

func main() {
    fmt.Println(fibonacci(6)) // prints: 8
}
```

In this example, the `fibonacci` function computes the nth Fibonacci number by calling itself recursively. The base case is `n <= 1`, where the function returns `n`.

### Characteristics of recursive functions

- **Base case**: every recursive function must have a base case to terminate the recursion.
- **Recursive step**: a recursive function needs to call itself to solve the problem step by step.
- **Stack usage**: each recursive call pushes a new stack frame, so a deep enough recursion overflows the stack.

### Summary

- **Recursive function**: a function that calls itself in its own definition.
- Recursion consists of a **base case** and a **recursive step**.
- It is well suited to problems that decompose into simpler subproblems, such as the factorial and the Fibonacci sequence.

When writing recursion, define the base case first, then the recursive step; the function can only stop when both are in place. Leave out the base case and you get an infinite loop at best, a stack overflow at worst.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)


## Sibling pages

- [AnonymousFunc](/func/AnonymousFunc.md)
- [Defer](/func/Defer.md)
- [VariadicParameters](/func/VariadicParameters.md)
- [MultipleReturnValues](/func/MultipleReturnValues.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [MultipleReturnValues](/func/MultipleReturnValues.md)
