## Performance analysis with pprof and flame graphs

Guessing where a program is slow is useless. Go's `pprof` collects runtime data for CPU, memory, goroutines, and so on, and a flame graph draws that data as a call-stack picture, so you can see at a glance which function eats the most time. Here I record the process of using these tools to track down deadlocks and CPU hot spots.

### 1. Introduction to the `pprof` tool

`pprof` is the performance analysis tool built into Go. It supports analysis of CPU, memory allocation, goroutines, blocking operations, and more, and the reports it produces are used to locate bottlenecks.

#### 1.1 Installing `pprof`

`pprof` is already in the standard library, and `go tool pprof` runs as is. To install the visualization tool, use the command below:

```bash
go install github.com/google/pprof@latest
```

### 2. Generating performance analysis data

To use `pprof` for performance analysis, you need to import the `net/http/pprof` package in your code and start an HTTP server that exposes the profiling data.

#### 2.1 Example code

An example of an HTTP server with `pprof`:

```go
package main

import (
    "net/http"
    _ "net/http/pprof"
)

func main() {
    // start the HTTP server
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("Hello, Go!"))
    })

    http.ListenAndServe(":8080", nil)
}
```

In the code above, importing the `pprof` package via `_ "net/http/pprof"` enables `pprof` analysis in the default HTTP server.

### 3. Collecting and analyzing performance data

#### 3.1 Collecting CPU profile data

While the program is running, use the following command to collect CPU profile data:

```bash
go tool pprof http://localhost:8080/debug/pprof/profile?seconds=30
```

The command above collects 30 seconds of CPU performance data and produces a `pprof` report file ready for analysis.

#### 3.2 Collecting memory profile data

Similarly, you can collect memory profile data:

```bash
go tool pprof http://localhost:8080/debug/pprof/heap
```

#### 3.3 Finding deadlocks

Go's `pprof` tool can also help you find deadlocks and other blocking operations. Use the following command to get the stack information of all current goroutines:

```bash
go tool pprof http://localhost:8080/debug/pprof/goroutine
```

Analyzing the goroutine stack information helps you identify and locate deadlocks or other blocking problems.

#### 3.4 Analyzing performance data

Use the `pprof` tool to analyze the generated performance data file:

```bash
go tool pprof [profile_file]
```

Once you enter the `pprof` interactive interface, use the following commands to analyze the data:

- `top`: show the functions consuming the most CPU
- `list [function_name]`: view detailed information for a given function
- `web`: generate and open a visualization of the performance data

### 4. Flame graphs

A flame graph is a tool for visualizing performance analysis results. By showing the function call stack and the time consumed, it helps you locate performance bottlenecks quickly. Each rectangle in a flame graph represents a function, and its width represents that function's CPU time or memory usage.

#### 4.1 Installing the flame graph tool

Use the `FlameGraph` tool provided by Brendan Gregg to generate flame graphs:

```bash
git clone https://github.com/brendangregg/FlameGraph.git
```

#### 4.2 Generating a flame graph

Use `pprof` to produce the folded file that a flame graph needs:

```bash
go tool pprof -raw -output=cpu.pprof http://localhost:8080/debug/pprof/profile?seconds=30
```

Convert the `pprof` output into the folded file format the flame graph tool recognizes:

```bash
go tool pprof -raw -output=cpu.raw cpu.pprof
```

Use the `FlameGraph` tool to generate the flame graph:

```bash
./FlameGraph/stackcollapse-go.pl cpu.raw > out.folded
./FlameGraph/flamegraph.pl out.folded > cpu_flamegraph.svg
```

### 5. Example: analyzing and optimizing code

#### 5.1 Example code

A simple example that runs a computation in a loop:

```go
package main

import (
    "net/http"
    _ "net/http/pprof"
    "time"
)

func main() {
    go func() {
        for {
            work()
        }
    }()

    http.ListenAndServe(":8080", nil)
}

func work() {
    time.Sleep(1 * time.Second)
}
```

#### 5.2 Performance analysis

Run the example code and collect CPU profile data:

```bash
go tool pprof http://localhost:8080/debug/pprof/profile?seconds=30
```

Analyze the collected performance data and generate a flame graph:

```bash
go tool pprof -raw -output=cpu.pprof http://localhost:8080/debug/pprof/profile?seconds=30
go tool pprof -raw -output=cpu.raw cpu.pprof
./FlameGraph/stackcollapse-go.pl cpu.raw > out.folded
./FlameGraph/flamegraph.pl out.folded > cpu_flamegraph.svg
```

Open the generated flame graph `cpu_flamegraph.svg` and locate the performance bottleneck in the program.

### 6. Finding deadlocks and the most CPU-heavy logic with `pprof`

In performance analysis, beyond the usual CPU and memory usage analysis, you also need to watch for deadlocks and the logic that consumes the most CPU in the program.

#### 6.1 Finding deadlocks

Run the following command to view the stack information of all current goroutines, which helps identify and locate deadlocks:

```bash
go tool pprof http://localhost:8080/debug/pprof/goroutine
```

In the `pprof` interactive interface, use the `goroutine` command to view detailed goroutine stack information and analyze possible deadlocks.

#### 6.2 Finding the most CPU-heavy logic

In the `pprof` interactive interface, use the `top` command to view the functions consuming the most CPU:

```bash
go tool pprof [profile_file]
top
```

Use the `list [function_name]` command to view detailed information for a given function, which helps locate the most CPU-heavy logic:

```bash
list work
```

For deadlocks, look at goroutine stacks; for hot spots, look at `top` and `list`; both start from the `pprof` interactive interface.

### Summary

`pprof`'s workflow is three steps: import `net/http/pprof` to expose the endpoints, collect data with `go tool pprof`, then look at the results in the interactive interface with `top`, `list`, and `web`. A flame graph draws the same data as a picture, where rectangle width is the share of time. Check goroutine stacks for deadlocks and `top` for CPU hot spots.

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)
- [Official blog · Profiling Go Programs](https://go.dev/blog/pprof)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Debug](/debug/Debug.md)
- [Delve](/debug/Delve.md)
- [Expvar](/debug/Expvar.md)
- [GDB](/debug/GDB.md)
- [Utils](/debug/Utils.md)
- [glossary](/glossary.md)
