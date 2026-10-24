Debugging is finding and fixing errors in a program. Here I organize the common practice into four areas: tools, techniques, tips, and performance profiling:

### 1. **Debugging tools**

- **Debugger**: A debugger is a tool for inspecting and controlling program execution. It lets a developer step through the code, inspect variable values, set breakpoints, and so on. Common debuggers include `gdb` (for C/C++), `delve` (for Go), and `pdb` (for Python).
- **Logging**: Insert log statements in the code to record the state of the program and error messages as it runs, answering "what was the program doing at that moment."

### 2. **Debugging techniques**

- **Breakpoints**: A breakpoint is a marker placed on a line of code. When the program reaches that line it pauses, letting the developer inspect the current state.
- **Step execution**: Running the program line by line to observe the effect of each line. Common operations are "Step Into", "Step Over", and "Step Out".
- **Watching variables**: Viewing variable values in real time to track how data changes in the program.
- **Call stack**: The call stack shows the program's current execution path, including the order and nesting of function calls. Pinning an error to a specific call chain relies on it.
- **Conditional breakpoints**: A conditional breakpoint only interrupts execution when a given condition is met, useful for debugging problems that appear in specific situations.
- **Core dumps**: A core dump is a snapshot of memory produced when a program crashes, and can be used to analyze why it crashed.

### 3. **Debugging tips**

- **Bisection debugging**: Narrow the problem down step by step to locate it quickly. Commenting out portions of the code or using logs lets you identify where the problem occurs fast.
- **Boundary testing**: Check how the program behaves on boundary conditions (maximum, minimum, empty values, etc.) to make sure it is robust.
- **Unit testing**: Writing unit tests catches errors early in development and keeps code correct after changes.

### 4. **Performance debugging**

- **Profiling**: Profiling tools (`perf`, `gprof`, `pprof`, and so on) analyze performance metrics such as runtime and memory usage, helping you find bottlenecks.
- **Flame graphs**: A flame graph is a visualization that shows how time is distributed across function calls, helping you spot hot spots.

### 5. **Debugging best practices**

- **Investigate as soon as a problem shows up**: Put it off and there will be more code changes and more variables to compare against.
- **Keep it simple**: Keep the code clean while debugging, and record the key debugging observations in comments.
- **Record and analyze**: Write down the observations from each step so you have a traceable write-up of the process to look back at later.

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)

## Sibling pages

- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Delve](/debug/Delve.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Delve](/debug/Delve.md)
- [Expvar](/debug/Expvar.md)
- [GDB](/debug/GDB.md)
- [Utils](/debug/Utils.md)
