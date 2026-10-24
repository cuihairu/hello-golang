# goto
### A Detailed Explanation of `goto` in Go

In Go, the `goto` statement is used to unconditionally jump to a labeled position within the same function. Although it provides a direct jump mechanism, it should generally be used with caution because it can make code hard to understand and maintain.

### 1. Basic Usage

The basic use of `goto` is to jump program control directly to a labeled position within the same function. A label is a name consisting of an identifier and a colon (`:`).

**Example: Basic usage**

```go
package main

import "fmt"

func main() {
    fmt.Println("Start")
    goto skip
    fmt.Println("This will be skipped")

skip:
    fmt.Println("This will be executed")
}
```

**Output:**

```
Start
This will be executed
```

In this example, the `goto skip` statement jumps program control directly to the `skip:` label, skipping the `fmt.Println("This will be skipped")` statement.

### 2. Use Cases for `goto`

The `goto` statement can be used in the following scenarios:

- **Error handling**: In some complex error handling scenarios, `goto` can be used to jump to a common cleanup location.
- **Loop exit**: It can be used to exit a loop early or skip certain logic, though this is generally not recommended.

**Example: Error handling**

```go
package main

import "fmt"

func process() (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("error occurred: %v", r)
        }
    }()

    fmt.Println("Processing...")
    goto errorHandler

errorHandler:
    fmt.Println("Handling error")
    return
}

func main() {
    if err := process(); err != nil {
        fmt.Println(err)
    }
}
```

In this example, `goto errorHandler` is used to jump to the error handling section, and after executing the error handling logic, it returns.

### 3. Limitations and Caveats of `goto`

- **Readability**: Overusing `goto` can lead to poor code readability, making it difficult to follow the program flow.
- **Maintainability**: Using `goto` extensively can make code harder to maintain, as it breaks the basic principles of structured programming.
- **Best practice**: Structured control flow (such as `for`, `if`, `switch`) is generally recommended over `goto`, unless there is a specific case that truly requires it.

### 4. `goto` and Loops

The `goto` statement can be used to skip certain logic within a loop, but this usage is rare because it can lead to maintainability issues.

**Example: Skipping certain logic in a loop**

```go
package main

import "fmt"

func main() {
    for i := 0; i < 5; i++ {
        if i == 2 {
            goto endLoop
        }
        fmt.Println(i)
    }

endLoop:
    fmt.Println("Loop ended early")
}
```

**Output:**

```
0
1
Loop ended early
```

### 5. Low-Level Implementation of `goto`

The low-level implementation of `goto` involves a direct jump and does not typically involve complex low-level mechanisms. It simply sets the program counter (PC) to jump to the labeled position.

**Simplified assembly code example**

The following is a simplified assembly code example (for the `amd64` architecture) that shows the low-level implementation of `goto`:

```assembly
TEXT main(SB), NOSPLIT, $0
    MOVQ    $0, i(SP)       // initialize the loop variable
loop:
    CMPQ    $2, i(SP)       // check the condition
    JGE     endLoop         // if the condition is met, jump to endLoop
    MOVQ    i(SP), AX       // read the loop variable
    CALL    fmt.Println(SB) // print the variable value
    ADDQ    $1, i(SP)       // update the loop variable
    JMP     loop            // jump back to loop
endLoop:
    CALL    fmt.Println(SB) // print "Loop ended early"
    RET
```

### Summary

After compilation, `goto` is just a jump instruction with no extra runtime cost. Its uses are concentrated in a few places: breaking out of deeply nested structures, or jumping to a common cleanup or error handling location. In everyday code, `break`/`continue` with labels and `defer` already cover most of these needs. When you feel the need to write `goto`, first ask yourself whether the loop structure is designed well.

## References

- [Language Spec · Statements](https://go.dev/ref/spec#Statements)
- [Effective Go · Control Structures](https://go.dev/doc/effective_go#control-structures)
- [Language Spec · Goto statements](https://go.dev/ref/spec#Goto_statements)
- [Language Spec · Label scopes](https://go.dev/ref/spec#Label_scopes)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Jump](/syntax/Jump.md)
