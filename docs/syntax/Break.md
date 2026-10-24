# break
In Go, the `break` statement immediately terminates the execution of a `for` loop, `switch`, or `select` statement.

### Basic usage

#### `break` in `for` loops

In a `for` loop, `break` is used to jump out of the loop body, regardless of whether the loop condition is still met.

**Example:**

```go
package main

import "fmt"

func main() {
    for i := 0; i < 10; i++ {
        if i == 5 {
            break
        }
        fmt.Println(i)
    }
}
```

**Output:**

```
0
1
2
3
4
```

In this example, when the value of `i` reaches 5, the `break` statement terminates the `for` loop, causing it to stop after printing up to 4.

#### `break` in `switch` statements

In a `switch` statement, `break` is usually not needed, because each `case` block automatically jumps out of the `switch` statement after execution. However, if a `switch` is nested inside a `for` or another `switch`, `break` can be used to jump out of those structures.

**Example:**

```go
package main

import "fmt"

func main() {
    switch day := 2; day {
    case 1:
        fmt.Println("Monday")
    case 2:
        fmt.Println("Tuesday")
        // suppose there were other structures here
        break // this break is redundant
    case 3:
        fmt.Println("Wednesday")
    }
}
```

In this example, the `break` statement is actually redundant, because each `case` automatically jumps out of the `switch` statement.

#### `break` in `select` statements

In a `select` statement, `break` is used to jump out of the `select` statement's execution. Note: when a `select` is inside a `for` loop, an unlabeled `break` only jumps out of the `select` itself, not out of the outer `for` loop. To exit the loop, you must use a labeled `break`.

**Example: an unlabeled `break` only jumps out of `select`**

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 3)
    ch <- 1
    ch <- 2
    close(ch)

    for {
        select {
        case msg, ok := <-ch:
            if !ok {
                fmt.Println("channel closed")
                break // only jumps out of select, the for loop will continue to the next iteration
            }
            fmt.Println("Received:", msg)
        }
        if len(ch) == 0 {
            // no more data can be read in select, end the loop through other conditions
            fmt.Println("done")
            return
        }
    }
}
```

**Example: using a label to jump out of the `for` loop**

```go
package main

import "fmt"

func main() {
    ch := make(chan int, 3)
    ch <- 1
    ch <- 2
    close(ch)

loop:
    for {
        select {
        case msg, ok := <-ch:
            if !ok {
                fmt.Println("channel closed")
                break loop // jumps out of the outer for loop
            }
            fmt.Println("Received:", msg)
        }
    }
}
```

In this example, the `break loop` statement terminates the `for` loop; if it were written as an unlabeled `break`, it would only end the current `select`, and the loop would run forever.

### Notes

1. **`break` and labels**: `break` can be used together with labels to jump out of multiple levels of nested loops. A label identifies an outer loop, and `break` can specify the label to jump out of a specific loop.

**Example:**

```go
package main

import "fmt"

func main() {
OuterLoop:
    for i := 0; i < 5; i++ {
        for j := 0; j < 5; j++ {
            if i == 2 && j == 2 {
                break OuterLoop
            }
            fmt.Println(i, j)
        }
    }
}
```

In this example, the `break OuterLoop` statement jumps out of the outer `for` loop labeled `OuterLoop`.

2. **`break` can only be used in loops and `switch` statements**: the `break` statement cannot be used in functions or other code blocks; it can only be used to jump out of loop structures and `switch` statements.

3. **`break` does not affect other control flow**: `break` only terminates the current loop or `switch` statement and does not affect the execution of other control-flow structures.

### Summary

- **`for` loops**: `break` is used to terminate the loop body's execution early.
- **`switch` statements**: `break` is usually not needed, because `case` blocks automatically jump out of the `switch`, but it can be used for more complex control flow.
- **`select` statements**: `break` is used to exit the current `select`; to exit the enclosing `for` loop, you must use a labeled `break`.
- **Labels**: used together with `break`, labels allow you to jump out of multiple levels of nested loops.

The most common pitfall is a `select` written inside a loop: an unlabeled `break` only jumps out of the `select`, and the `for` is still spinning.

## References

- [Language Specification · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Specification · Break statements](https://go.dev/ref/spec#Break_statements)

## Sibling pages

- [Conditional](/syntax/Conditional.md)
- [ControlFlow](/syntax/ControlFlow.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Conditional](/syntax/Conditional.md)
- [ControlFlow](/syntax/ControlFlow.md)
- [Jump](/syntax/Jump.md)
- [Loop](/syntax/Loop.md)
