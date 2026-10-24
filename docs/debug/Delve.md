`delve` is a debugger written specifically for Go. Here I note installation, how to start it, and the commands I use most.

### Installing `delve`

1. **Install `delve`**

   First make sure the machine has a Go environment, then run:

   ```sh
   go install github.com/go-delve/delve/cmd/dlv@latest
   ```

   After installing, the `delve` binary lands in `$GOPATH/bin`. If `$GOPATH/bin` is not in your `PATH`, add it manually, or run `delve` by its full path.

2. **Verify the install**

   If it prints a version number, it is installed:

   ```sh
   dlv version
   ```

### Starting `delve`

`delve` supports several startup modes, including debugging a program directly, debugging a compiled program, and attaching to a running process.

1. **Debug a program directly**

   The `dlv debug` command compiles and debugs the Go package in the current directory (just run it in the directory containing `main.go`; you can also pass a package path, such as `dlv debug ./cmd/app`):

   ```sh
   dlv debug
   ```

   This compiles and starts the program, then enters debug mode. Note that `dlv debug` takes a package path, not a source file name.

2. **Debug a compiled program**

   If the program is already compiled, debug it with the `dlv exec` command:

   ```sh
   dlv exec <your_program>
   ```

3. **Attach to a running process**

   Use `dlv attach` to attach to an already-running Go process:

   ```sh
   dlv attach <pid>
   ```

### Basic debugging commands

The debugging commands I use most:

1. **Set a breakpoint**

   ```sh
   break <location>
   ```

   - `<location>` can be a file name and line number (for example `main.go:10`) or a function name (for example `main.main`).
   - Example: `break main.go:15` or `break main.main`

2. **Continue**

   ```sh
   continue
   ```

   Resume execution until the next breakpoint or until the program ends.

3. **Step into**

   ```sh
   step
   ```

   Enter a function and execute the next line of code.

4. **Step over**

   ```sh
   next
   ```

   Execute the current line without entering a function.

5. **Step out**

   ```sh
   stepout
   ```

   Run until the current function returns.

6. **Print a variable value**

   ```sh
   print <variable>
   ```

   Print the current value of the specified variable. It can be a local variable, a global variable, or a struct field.

7. **View the call stack**

   ```sh
   stack
   ```

   Show the current call stack, including the order of function calls.

8. **View the local variables of the current scope**

   ```sh
   locals
   ```

   Show the local variables of the current function.

9. **View the parameters of the current function**

   ```sh
   args
   ```

   Show the parameters of the current function.

10. **List the source code**

    ```sh
    list
    ```

    Show the source code near the current breakpoint. You can specify a line number or function name to look at a specific area.

### Advanced debugging tips

1. **Conditional breakpoints**

   Break only when the condition holds:

   ```sh
   break <location> if <condition>
   ```

   For example: `break main.go:10 if x > 5`

2. **View Goroutines**

   Use the `goroutines` command to see the state of all goroutines:

   ```sh
   goroutines
   ```

   You can then attach to a specific goroutine to debug it.

3. **Watch an expression**

   Use the `watch` command to set a watchpoint and observe changes to a given expression:

   ```sh
   watch <expression>
   ```

   For example: `watch x > 5`

4. **Manage breakpoints**

   - List all breakpoints: `breakpoints`
   - Delete a breakpoint: `clear <location>`

5. **Custom debugging configuration**

   When debugging from an IDE (such as VSCode), `delve` is driven by the IDE's debug configuration file (such as `.vscode/launch.json`), and the breakpoint and variable panels work directly.

### Example debugging session

Suppose there is a simple Go program, `main.go`:

```go
package main

import "fmt"

func main() {
    x := 10
    y := 20
    result := add(x, y)
    fmt.Println(result)
}

func add(a, b int) int {
    return a + b
}
```

Debug this program with `delve`:

1. **Start the debug session**

   Run from the directory containing `main.go`:

   ```sh
   dlv debug
   ```

2. **At the `delve` prompt**

   ```sh
   (dlv) break main.go:9
   (dlv) continue
   (dlv) print x
   (dlv) print result
   (dlv) step
   ```

   These commands set a breakpoint at `fmt.Println(result)` (by which point `result` has already been assigned 30), then continue the program and inspect the variable values.

### Summary

Breakpoints, stepping, variable inspection, conditional breakpoints, and the goroutine list — `delve`'s commands cover the main actions of debugging a Go program. Once it is installed, run `dlv debug` and the rest is command-line interaction.

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)
- [Delve debugger (official repository)](https://github.com/go-delve/delve)

## Sibling pages

- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Debug](/debug/Debug.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Debug](/debug/Debug.md)
- [Expvar](/debug/Expvar.md)
