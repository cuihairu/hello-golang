Go's debugging tools fall into two groups: `log`, `testing`, `pprof`, and `runtime` in the standard library, and the `delve` debugger outside it.

### 1. **The `log` package**

The `log` package handles basic log output and comes in handy when tracking down problems (the standard library `log` itself has no log levels; if you need leveled logging, use `log/slog`, introduced in Go 1.21). For example:

```go
import "log"

func main() {
    log.Println("This is a log message.")
}
```

### 2. **The `testing` package**

Besides unit testing, the `testing` package also supports benchmark tests and example tests. Adding debugging code inside a test function lets you check program behavior. For example:

```go
import (
    "testing"
    "log"
)

func TestExample(t *testing.T) {
    log.Println("Debugging information")
    // Your test code here
}
```

### 3. **The `pprof` package**

The `pprof` package is used for performance analysis and debugging. It can produce CPU and memory profiles of a program, which help identify performance bottlenecks and memory leak problems. Here is how to use it:

- **Start pprof**:

```go
import (
    "log"
    "net/http"
    _ "net/http/pprof"
)

func main() {
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()
    // Your application code here
}
```

- **View the profiles**: after running the application, visit `http://localhost:6060/debug/pprof/` to get different kinds of profile information.

### 4. **The `delve` debugger**

`delve` is not in the standard library, but it is Go's mainstream debugger, and it supports breakpoints, step execution, variable inspection, and the call stack. Basic usage:

- **Install delve**:

```sh
go install github.com/go-delve/delve/cmd/dlv@latest
```

- **Start debugging**:

```sh
# compile the current package and start debugging (most common)
dlv debug

# debug an already compiled binary
dlv exec ./your_program
```

- **Common commands**:

  - `break <location>`: set a breakpoint
  - `next`: step over
  - `step`: step into a function
  - `continue`: run until the next breakpoint
  - `print <variable>`: inspect a variable's value
  - `stack`: view the call stack

### 5. **The `runtime` package**

The `runtime` package provides functionality related to the Go runtime, which helps debug some low-level problems. For example, you can use `runtime.Stack` to print the current stack information:

```go
import (
    "fmt"
    "runtime"
)

func main() {
    buf := make([]byte, 1<<16)
    runtime.Stack(buf, true)
    fmt.Printf("%s", buf)
}
```

Logging, testing, profiling, and breakpoints each cover a slice: add logs to narrow the problem, follow a failing test with `delve` breakpoints, and hand performance problems over to `pprof` profile data.

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)

## Sibling pages

- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Debug](/debug/Debug.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [PGO](/debug/PGO.md)
