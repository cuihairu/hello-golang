Labels in Go mark positions in the code, used by `break`, `continue`, and `goto` for jumps. They mainly serve multiply nested loops, letting an inner loop jump directly out of, or skip, an outer one.

### Basic label syntax

The syntax is a label name followed by a colon (`:`), then the code block. Labels are usually placed before a `for` loop, a `switch` statement, or a `select` statement. A label name can be any legal identifier and usually starts with a lowercase letter.

#### Label syntax example

```go
LabelName:
    // code block
```

### Labels with `break`

Used together with a `break` statement, a label lets you break out of a multiply nested loop or `switch` statement. A plain `break` exits only the nearest loop or `switch`; a label specifies exactly which one to exit.

#### Example: breaking out of nested loops with a label

```go
package main

import "fmt"

func main() {
    OuterLoop:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                break OuterLoop
            }
            fmt.Println(i, j)
        }
    }
}
```

**Output:**

```
0 0
0 1
0 2
1 0
```

In this example, `break OuterLoop` exits the outer `for` loop labelled `OuterLoop`. When `i` equals 1 and `j` equals 1, the `break` fires and the outer loop terminates immediately.

### Labels with `continue`

A `continue` statement skips the rest of the current loop iteration and starts the next one. Combined with a label, `continue` can skip the current iteration of an outer loop.

#### Example: skipping the current iteration of an outer loop with a label

```go
package main

import "fmt"

func main() {
    OuterLoop:
    for i := 0; i < 3; i++ {
        for j := 0; j < 3; j++ {
            if i == 1 && j == 1 {
                continue OuterLoop
            }
            fmt.Println(i, j)
        }
    }
}
```

**Output:**

```
0 0
0 1
0 2
1 0
2 0
2 1
2 2
```

In this example, `continue OuterLoop` skips the current iteration of the outer `for` loop. When `i` equals 1 and `j` equals 1, the `continue` makes the program skip the current `OuterLoop` iteration and proceed to the next one.

### Labels with `goto`

A `goto` statement jumps unconditionally to a specified label in the program. `goto` can jump to any label in the same function, but it should be used cautiously to avoid tangled code that is hard to maintain.

#### Example: jumping to a label with `goto`

```go
package main

import "fmt"

func main() {
    i := 0
    Start:
    fmt.Println(i)
    i++
    if i < 5 {
        goto Start
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

In this example, `goto Start` sends the program back to the `Start` label, which produces a simple loop.

### Things to watch out for when using labels

1. **Readability**: use too many labels and `goto`, and readers have to keep flipping back and forth to find where a jump lands. Labels are plenty for cases like deeply nested `for` loops.

2. **Avoid complex control flow**: control flow where several labels jump across each other is hard to follow. If early returns or splitting a function can solve it, don't reach for labels.

### Summary

- **Labels**: mark positions in the program, used together with `break`, `continue`, and `goto`.
- **`break`**: with a label, jumps directly out of a multiply nested loop or `switch`.
- **`continue`**: with a label, skips the current iteration of an outer loop.
- **`goto`**: jumps unconditionally to a specified label, valid within the same function.

## References

- [Effective Go (official)](https://go.dev/doc/effective_go)
- [Language spec · Labeled statements](https://go.dev/ref/spec#Labeled_statements)
- [Language spec · Label scopes](https://go.dev/ref/spec#Label_scopes)


## Sibling pages

- [EffectiveGo](/idioms/EffectiveGo.md)
- [StructTags](/idioms/StructTags.md)
- [BlankIdentifier](/idioms/BlankIdentifier.md)
- [Idioms](/idioms/Idioms.md)
- [Range](/idioms/Range.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Idioms](/idioms/Idioms.md)
- [Range](/idioms/Range.md)
