# defer
### `defer` in Go, in detail

In Go, `defer` is used to run a deferred operation just before a function returns; its typical use is releasing resources and cleanup.

#### Basic usage

A `defer` statement registers a function call that runs after the function containing the `defer` statement has finished executing. The syntax of `defer` is as follows:

```go
func functionName() {
    defer deferredFunction()
    // function body
}
```

#### Example: basic usage

```go
package main

import "fmt"

func deferExample() (result int) {
    result = 1
    defer func() {
        fmt.Println("Deferred function called")
        result = 2
    }()
    return
}

func multipleDefers() {
    defer fmt.Println("First deferred")
    defer fmt.Println("Second deferred")
    fmt.Println("Function body")
}

func main() {
    fmt.Println("Starting deferExample:")
    fmt.Println("Return value:", deferExample())

    fmt.Println("\nStarting multipleDefers:")
    multipleDefers()
}
```

**Output:**

```
Starting deferExample:
Deferred function called
Return value: 2

Starting multipleDefers:
Function body
Second deferred
First deferred
```

### Execution order of multiple `defer`s

Multiple `defer` statements execute in last-in, first-out (LIFO) order. This means the last-registered `defer` statement runs first.

#### Example: multiple `defer` statements

```go
package main

import "fmt"

func multipleDefers() {
    defer fmt.Println("First deferred")
    defer fmt.Println("Second deferred")
    fmt.Println("Function body")
}

func main() {
    multipleDefers()
}
```

**Output:**

```
Function body
Second deferred
First deferred
```

### The relationship between `defer` and `return`

- `defer` statements run after `return` is executed but before the function actually returns.
- `defer` statements can access a function's return values and modify them.

#### Example: the relationship between `defer` and `return`

```go
package main

import "fmt"

func modifyReturnValue() (result int) {
    result = 1
    defer func() {
        fmt.Println("Deferred function modifies result")
        result = 2
    }()
    return
}

func main() {
    fmt.Println("Return value:", modifyReturnValue())
}
```

**Output:**

```
Deferred function modifies result
Return value: 2
```

### `defer` and `for`

When using `defer` inside a `for` loop, the two things to watch are how many times it gets registered and the order it runs in; since Go 1.14, the overhead of `defer` itself has also dropped considerably.

### Things to note when using `defer` in a `for` loop

#### 1. Each loop iteration registers a new `defer`

Each iteration registers a new `defer`, and those calls don't run until the function returns; with many loop iterations, the registered data structures keep piling up, and execution gets held back to the very last moment.

#### 2. Execution order of `defer` statements

Later-registered ones run first. When allocating several resources together, check the release order against this rule.

#### Example: using `defer` in a `for` loop

```go
package main

import "fmt"

func main() {
    for i := 0; i < 3; i++ {
        defer fmt.Printf("Deferred: %d\n", i)
    }
}
```

**Output:**

```
Deferred: 2
Deferred: 1
Deferred: 0
```

In this example, although the `defer` statement is registered on every iteration of the loop, the order of execution is reversed, which illustrates the LIFO nature of `defer` statements.

### Improvements in Go

Go's `defer` mechanism has been improved several times across versions, mostly on the performance side.

#### 1. Performance optimizations in Go 1.14 and later

Starting with Go 1.14, both registering and executing `defer` became cheaper, and stack management became leaner; code that calls `defer` at high frequency benefited first.

#### 2. Stack allocation optimizations

Before Go 1.14, the overhead of `defer` was relatively large, because each `defer` statement allocated a new data structure on the stack. Go 1.14 introduced a more efficient stack allocation strategy to reduce the overhead of `defer`, especially in loops and high-concurrency scenarios.

#### Example: performance improvement

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    start := time.Now()
    for i := 0; i < 1000000; i++ {
        defer fmt.Println("Deferred:", i)
    }
    fmt.Println("Time taken:", time.Since(start))
}
```

In Go 1.14 and later, the execution time of the example above is noticeably lower than in earlier versions, which reflects the effect of the `defer` performance optimizations.

#### Summary

- **Basic usage**: `defer` runs before a function returns and is used for resource cleanup.
- **Use in a `for` loop**: each loop iteration registers a new `defer`, and execution follows LIFO order.
- **Improvements in Go**: Go 1.14 and later optimized the performance of `defer`, reduced overhead, and improved stack management.

### The underlying implementation of `defer`

Under the hood, `defer` is implemented with a stack. Whenever a `defer` statement is encountered, Go pushes the pending function call and its arguments onto the stack. Before a function returns, Go pops the calls off the stack in LIFO order and executes them one by one.

#### Assembly example

To understand the underlying implementation, you can look at Go's assembly code. The following is a simplified assembly snippet showing how `defer` is handled:

```assembly
TEXT main.deferredExample(SB), NOSPLIT, $0
	MOVQ	$1, result(SP)
	// set up the deferred function
	MOVQ	$deferFunction(SB), R8
	MOVQ	R8, deferCall(SP)
	RET

TEXT main.multipleDefers(SB), NOSPLIT, $0
	// set up the first deferred function
	MOVQ	$firstDeferred(SB), R8
	MOVQ	R8, deferCall1(SP)
	// set up the second deferred function
	MOVQ	$secondDeferred(SB), R8
	MOVQ	R8, deferCall2(SP)
	RET

TEXT deferFunction(SB), NOSPLIT, $0
	// execute the deferred function
	RET

TEXT firstDeferred(SB), NOSPLIT, $0
	// execute the first deferred function
	RET

TEXT secondDeferred(SB), NOSPLIT, $0
	// execute the second deferred function
	RET
```

### Summary

- **Basic usage**: `defer` is used to run cleanup operations before a function returns.
- **Multiple `defer` statements**: they execute in last-in, first-out (LIFO) order.
- **Relationship with `return`**: `defer` statements run after `return` is executed but before the function actually returns, and they can modify return values.
- **Underlying implementation**: `defer` uses a stack to manage function calls, ensuring they execute in LIFO order.

## References

- [Language Spec · Function declarations](https://go.dev/ref/spec#Function_declarations)
- [Language Spec · Calls](https://go.dev/ref/spec#Calls)
- [Effective Go · Functions](https://go.dev/doc/effective_go#functions)
- [Language Spec · Defer statements](https://go.dev/ref/spec#Defer_statements)
- [Official Blog · Defer, Panic, and Recover](https://go.dev/blog/defer-panic-and-recover)
- [Effective Go · Defer](https://go.dev/doc/effective_go#defer)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Arguments](/func/Arguments.md)
- [DefineAndCall](/func/DefineAndCall.md)
- [FuncValue](/func/FuncValue.md)
- [History](/func/History.md)
- [InnerFunc](/func/InnerFunc.md)
- [MultipleReturnValues](/func/MultipleReturnValues.md)
- [RecursiveFunction](/func/RecursiveFunction.md)
- [glossary](/zh/glossary.md)
