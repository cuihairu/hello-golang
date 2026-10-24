# Conditional statements

Conditional statements choose which branch of code to execute based on the value of a boolean expression. Go provides two conditional statements: `if` and `switch`; both fall under the category of conditional statements.

## The `if` statement

The `if` statement is the most basic conditional structure. The condition expression does not need to be wrapped in parentheses, and the branches must use braces.

```go
package main

import "fmt"

func main() {
    age := 20

    if age >= 18 {
        fmt.Println("adult")
    }

    if age >= 18 {
        fmt.Println("adult")
    } else if age >= 12 {
        fmt.Println("teenager")
    } else {
        fmt.Println("child")
    }
}
```

`if` also supports writing an initialization statement before the condition, separated by a semicolon. Variables declared in the initialization statement are in scope across the whole `if`/`else` block — this is the most idiomatic way to handle errors in Go:

```go
package main

import (
    "errors"
    "fmt"
)

func find() (int, error) {
    return 0, errors.New("not found")
}

func main() {
    if v, err := find(); err != nil {
        fmt.Println("error:", err)
    } else {
        fmt.Println("result:", v)
    }
}
```

For detailed usage of the `if` statement, see [if](/syntax/If.md).

## The `switch` statement

`switch` is a multi-way branch statement: it gathers multiple comparisons of the same expression into one block, avoiding deeply nested `if-else if`. Go's `switch` has three important properties:

- It jumps out automatically once a `case` matches; it does not fall through to the next `case` (when you do want fall-through, use `fallthrough` explicitly).
- A `case` can list multiple match values, separated by commas.
- The `switch` expression can be omitted, which is equivalent to `switch true`; the `case`s then take condition expressions.

```go
package main

import "fmt"

func main() {
    score := 85

    switch {
    case score >= 90:
        fmt.Println("A")
    case score >= 80:
        fmt.Println("B")
    default:
        fmt.Println("C or below")
    }

    switch day := 3; day {
    case 1, 2, 3, 4, 5:
        fmt.Println("weekday")
    case 6, 7:
        fmt.Println("weekend")
    }

    // type switch: determine the actual type of an interface value
    var i interface{} = "hello"
    switch v := i.(type) {
    case int:
        fmt.Println("int:", v)
    case string:
        fmt.Println("string:", v)
    }
}
```

For detailed usage of `switch`, see [switch](/syntax/Switch.md).

## The difference from `select`

`switch` is for multi-way branching on general conditions, while `select` is dedicated to multi-way selection over channel communication. Its syntax looks like `switch`, but its `case`s can only contain channel operations, and the runtime picks the branch that is ready. For a detailed comparison of the two, see [switch](/syntax/Switch.md).

## References

- [Language Specification · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Specification · If statements](https://go.dev/ref/spec#If_statements)
- [Language Specification · Switch statements](https://go.dev/ref/spec#Switch_statements)

## Sibling pages

- [Break](/syntax/Break.md)
- [Continue](/syntax/Continue.md)
- [For](/syntax/For.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Break](/syntax/Break.md)
