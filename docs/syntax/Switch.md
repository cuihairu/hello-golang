
> Perspective: this page records expression `switch`, `fallthrough`, and other control-flow usage; for type switches that branch on the dynamic type of an interface, see the [type assertion and type switch notes](/type/Switch.md).

# The `switch` statement in Go

Go's `switch` exits by default once a match is found; if you want fall-through, you must write `fallthrough` explicitly. There is also the type `switch` form. Below, from basic usage up to how it differs from `select`.

## Basic usage

The simplest `switch` statement looks like this:

```go
package main

import "fmt"

func main() {
    day := "Tuesday"
    switch day {
    case "Monday":
        fmt.Println("Today is Monday.")
    case "Tuesday":
        fmt.Println("Today is Tuesday.")
    case "Wednesday":
        fmt.Println("Today is Wednesday.")
    default:
        fmt.Println("Another day.")
    }
}
```

In this example, the variable `day` has the value `"Tuesday"`, so it matches `case "Tuesday"` and prints `"Today is Tuesday."`.

## The `fallthrough` keyword

By default, Go's `switch` statement exits automatically after matching a `case`. If you want execution to continue with the next `case`, use the `fallthrough` keyword:

```go
package main

import "fmt"

func main() {
    num := 2
    switch num {
    case 1:
        fmt.Println("One")
    case 2:
        fmt.Println("Two")
        fallthrough
    case 3:
        fmt.Println("Three")
    default:
        fmt.Println("Other")
    }
}
```

When `num` is `2`, `case 2` matches and prints `"Two"`; then, because of the `fallthrough`, the code block of `case 3` runs as well, printing `"Three"`.

### Notes

1. `fallthrough` can only appear on the last line of a `case` block.
2. You cannot skip multiple `case`s; it only falls into the immediately following `case`.
3. You cannot use `fallthrough` in the last `case`, because there is no next `case` to fall into.

## A `switch` without a condition

Go allows omitting the condition expression in a `switch` statement; it then defaults to `true`, giving functionality similar to an `if-else` chain:

```go
package main

import "fmt"

func main() {
    num := 10
    switch {
    case num < 0:
        fmt.Println("Negative number")
    case num == 0:
        fmt.Println("Zero")
    case num > 0:
        fmt.Println("Positive number")
    }
}
```

## Multiple conditions matching one `case`

A `case` can contain multiple matching conditions, separated by commas:

```go
package main

import "fmt"

func main() {
    day := "Saturday"
    switch day {
    case "Saturday", "Sunday":
        fmt.Println("Weekend")
    default:
        fmt.Println("Weekday")
    }
}
```

## Type `switch`

Go supports the type `switch`, used to determine the actual type of an interface variable:

```go
package main

import "fmt"

func typeSwitch(i interface{}) {
    switch v := i.(type) {
    case int:
        fmt.Printf("Integer: %d\n", v)
    case string:
        fmt.Printf("String: %s\n", v)
    default:
        fmt.Printf("Unknown type\n")
    }
}

func main() {
    typeSwitch(42)
    typeSwitch("hello")
    typeSwitch(3.14)
}
```

In this example, the `typeSwitch` function executes a different code block depending on the actual type of the argument passed in.

## The difference between `switch` and `select`

Although `switch` and `select` are both branching control structures in Go, they are used in different scenarios and have different functions.

### The `select` statement

The `select` statement is used to handle multiple channel operations. It picks a `case` that can execute immediately; if no `case` can execute, it blocks until one can. Only one `case` is executed each time.

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    go func() {
        time.Sleep(1 * time.Second)
        ch1 <- "one"
    }()

    go func() {
        time.Sleep(2 * time.Second)
        ch2 <- "two"
    }()

    select {
    case msg1 := <-ch1:
        fmt.Println("Received", msg1)
    case msg2 := <-ch2:
        fmt.Println("Received", msg2)
    case <-time.After(3 * time.Second):
        fmt.Println("Timeout")
    }
}
```

In this example, `select` waits until one of its `case`s can execute. Depending on the situation, it may print `"Received one"` or `"Received two"`, or it may print `"Timeout"` after the timeout.

### Summary

- **Different purposes**: `switch` is for general multi-way branching, while `select` is specifically for channel communication.
- **Different execution**: `switch` can use `fallthrough` to continue into the next branch after a match, whereas `select` executes only one branch each time and does not support `fallthrough`.
- **Blocking behavior**: `switch` does not block, while `select` blocks when no `case` can execute.

## Conclusion

One sentence on the division of labor: use `switch` for comparing ordinary values when you want explicit fall-through, and `select` for waiting on channel messages.

## References

- [Language Specification · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Specification · Switch statements](https://go.dev/ref/spec#Switch_statements)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Conditional](/syntax/Conditional.md)
- [Loop](/syntax/Loop.md)
