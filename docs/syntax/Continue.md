# continue
### A Detailed Explanation of `continue` in Go

In Go, the `continue` statement is used to skip the remaining statements in the current loop iteration and go directly to the next iteration. It can only be used in `for` loops (even when written inside a `switch` or `select` block, it still acts on the enclosing `for` loop), and is commonly used to skip processing logic under certain conditions.

### 1. Basic Usage

Inside a `for` loop body, the statements after `continue` are skipped for the current iteration, and control returns to the loop condition:

**Example: Basic usage**

```go
package main

import "fmt"

func main() {
    for i := 1; i <= 5; i++ {
        if i == 3 {
            continue // skip the current iteration
        }
        fmt.Println(i)
    }
}
```

**Output:**

```
1
2
4
5
```

In this example, when `i` equals 3, the `continue` statement is triggered, the current iteration is skipped, and the number 3 is not printed.

### 2. Usage in Nested Loops

The `continue` statement affects only the current loop level and does not skip the outer loop.

**Example: `continue` in nested loops**

```go
package main

import "fmt"

func main() {
    for i := 1; i <= 3; i++ {
        for j := 1; j <= 3; j++ {
            if j == 2 {
                continue // skip the current iteration of the inner loop
            }
            fmt.Printf("i = %d, j = %d\n", i, j)
        }
    }
}
```

**Output:**

```
i = 1, j = 1
i = 1, j = 3
i = 2, j = 1
i = 2, j = 3
i = 3, j = 1
i = 3, j = 3
```

In this example, when `j` equals 2, `continue` skips the current iteration of the inner loop, and the case `j = 2` is not printed.

### 3. Using `continue` with Labels

The `continue` statement can be used together with a label to skip the current iteration of an outer loop.

**Example: Using a label**

```go
package main

import "fmt"

func main() {
    OuterLoop:
    for i := 1; i <= 3; i++ {
        for j := 1; j <= 3; j++ {
            if j == 2 {
                continue OuterLoop // skip the current iteration of the outer loop
            }
            fmt.Printf("i = %d, j = %d\n", i, j)
        }
    }
}
```

**Output:**

```
i = 1, j = 1
i = 2, j = 1
i = 3, j = 1
```

In this example, `continue OuterLoop` skips the current iteration of the outer loop. When `j` equals 2, the entire outer loop (including the current value of `i`) is skipped, going directly to the next outer loop iteration.

### 4. Comparing `continue` and `break`

- **`continue`**: Skips the rest of the current iteration and continues with the next loop iteration.
- **`break`**: Terminates the entire loop, with no further iterations.

**Example: Comparing `continue` and `break`**

```go
package main

import "fmt"

func main() {
    fmt.Println("Using continue:")
    for i := 1; i <= 3; i++ {
        if i == 2 {
            continue
        }
        fmt.Println(i)
    }

    fmt.Println("\nUsing break:")
    for i := 1; i <= 3; i++ {
        if i == 2 {
            break
        }
        fmt.Println(i)
    }
}
```

**Output:**

```
Using continue:
1
3

Using break:
1
```

### 5. Low-Level Implementation of `continue`

In Go's low-level implementation, the `continue` statement typically involves the following steps:
- **Jump to the loop condition check**: The `continue` statement causes the program to jump to the beginning of the loop body to re-evaluate the condition.
- **Update the loop variable**: After skipping the current iteration, the program updates the loop variable according to its update rule for the next iteration.

**Assembly code example**

In Go's assembly code, `continue` simply jumps the program counter (PC) back to the loop condition check. For `amd64`, the simplified assembly is:

```assembly
TEXT main.loop(SB), NOSPLIT, $0
    MOVQ    8(SP), CX         // get the loop variable
    CMPQ    $2, CX            // check the loop condition
    JGE     endLoop           // if the condition is met, jump to end of loop
    JMP     continueLoop      // jump to loop condition check

continueLoop:
    // continue to the next iteration
    RET

endLoop:
    // end of loop
    RET
```

### Summary

- `continue` skips the rest of the current iteration, while `break` ends the entire loop.
- A `continue` in an inner loop only affects the inner loop; to skip the outer iteration, write `continue OuterLoop`.
- At the low level, it simply moves the program counter (PC) back to the loop condition check.

## References

- [Language Spec · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Spec · Continue statements](https://go.dev/ref/spec#Continue_statements)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Conditional](/syntax/Conditional.md)
- [ControlFlow](/syntax/ControlFlow.md)
- [Jump](/syntax/Jump.md)
- [Loop](/syntax/Loop.md)
