# Control Flow Statements

Control flow statements determine the execution order of statements in a program. Unlike many languages, Go removes `while`, `do-while`, and other loop syntax, keeping only `for` as the sole loop statement, while providing a full set of conditional and jump statements so control flow stays simple and uniform.

## The Three Categories of Go Control Flow

Go's control flow statements fall into three categories:

| Category | Statement | Description |
| --- | --- | --- |
| Conditional | `if`, `switch` | Choose which branch to execute based on a condition |
| Loop | `for` (including `range`) | Repeatedly execute a block of code |
| Jump | `break`, `continue`, `goto` | Change the direction of jumps in loops or branches |

## Conditional Statements

The `if` statement chooses an execution path based on the value of a boolean expression and supports an initialization statement before the condition; the `switch` statement is a simplified form of multi-way branching and can also perform type checks.

```go
package main

import "fmt"

func classify(n int) string {
    if n < 0 {
        return "negative"
    } else if n == 0 {
        return "zero"
    }
    return "positive"
}

func main() {
    x := -5
    fmt.Println(x, classify(x))

    switch day := x % 3; {
    case day == 0:
        fmt.Println("remainder is 0")
    case day < 0:
        fmt.Println("remainder is negative")
    }
}
```

## Loop Statements

The `for` loop is the only loop structure in Go. It can omit any part of the initialization, condition, or post statement, or even omit all three to form an infinite loop. With the `range` keyword, it can iterate over slices, arrays, strings, maps, and channels.

```go
package main

import "fmt"

func main() {
    // three-part form
    for i := 0; i < 3; i++ {
        fmt.Println("i =", i)
    }

    // iterate over a slice with range
    nums := []int{10, 20, 30}
    for idx, v := range nums {
        fmt.Println(idx, v)
    }

    // infinite loop with break
    n := 0
    for {
        n++
        if n >= 3 {
            break
        }
    }
    fmt.Println("n =", n)
}
```

## Jump Statements

`break` exits a loop or `switch`, `continue` skips the rest of the current iteration and proceeds to the next, and `goto` jumps to a label within the same function. `break` and `continue` can also be used with labels to control multi-level nested loops.

```go
package main

import "fmt"

func main() {
outer:
    for i := 0; i < 4; i++ {
        for j := 0; j < 4; j++ {
            if i*j >= 6 {
                break outer // break out of the outermost loop directly
            }
            if j == 2 {
                continue // only skip the current iteration of the inner loop
            }
            fmt.Println(i, j)
        }
    }
}
```

## Recommendations

- Prefer the structured statements `if`, `for`, and `switch`; use `goto` only in the few cases where you need to jump to a common cleanup location within a function.
- Go does not require parentheses around condition expressions; `gofmt` will automatically remove unnecessary parentheses.
- Branch statements break out automatically unless `fallthrough` is used; only use `fallthrough` when you explicitly need to fall through.

The following sections cover the specific usage of conditional statements, loop statements, and jump statements.

## References

- [Language Spec · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)

## Sibling pages

- [Break](/syntax/Break.md)
- [Continue](/syntax/Continue.md)
- [For](/syntax/For.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Break](/syntax/Break.md)
