### Debugging Go programs with GDB

GDB (GNU Debugger) is mainly used for debugging C and C++ programs, and it can debug Go programs too, though its Go support is limited.

#### 1. Installation and preparation

**1.1 Installing GDB**

On Linux, you can install GDB through a package manager:

- **On Debian/Ubuntu**:
  ```bash
  sudo apt-get update
  sudo apt-get install gdb
  ```

- **On Fedora**:
  ```bash
  sudo dnf install gdb
  ```

- **On macOS**:
  ```bash
  brew install gdb
  ```

- **On Windows**:
  ```ps1
  scoop install gdb
  ```


**1.2 Compiling the Go program**

To debug a Go program with GDB, compile it in debug mode. By default the Go compiler includes debug information, but you can use the `-gcflags` option to make sure the debug information is complete.

```bash
go build -gcflags "all=-N -l" -o myprogram main.go
```

- `-N`: disables optimization, which helps make debugging more accurate.
- `-l`: disables inlining, which makes debugging easier.

#### 2. Starting GDB

Run the compiled program with GDB:

```bash
gdb ./myprogram
```

This starts GDB and loads the `myprogram` binary.

#### 3. Common GDB commands

**3.1 Running the program**

Start executing the program:

```gdb
(gdb) run
```

**3.2 Setting breakpoints**

You can set breakpoints on a specific line, function, or address in a Go program:

- **Breakpoint on a line**:
  ```gdb
  (gdb) break main.go:10
  ```

- **Breakpoint on a function**:
  ```gdb
  (gdb) break main.main
  ```

- **Breakpoint on a specific address**:
  ```gdb
  (gdb) break *0x123456
  ```

**3.3 Viewing breakpoints**

List all breakpoints and their state:

```gdb
(gdb) info breakpoints
```

**3.4 Continuing**

Continue execution until the next breakpoint:

```gdb
(gdb) continue
```

**3.5 Stepping**

- **Step over the current line**:
  ```gdb
  (gdb) next
  ```

- **Step into a function call**:
  ```gdb
  (gdb) step
  ```

- **Run out of the current function**:
  ```gdb
  (gdb) finish
  ```

**3.6 Inspecting variables**

View the values of variables in the current scope:

```gdb
(gdb) print variableName
```

If you need to inspect a complex struct or array, use the more detailed command:

```gdb
(gdb) ptype variableName
```

**3.7 Viewing the call stack**

Show the current call stack information:

```gdb
(gdb) backtrace
```

**3.8 Modifying variables**

While debugging, you can change the value of a variable:

```gdb
(gdb) set variable variableName = newValue
```

**3.9 Listing source code**

Show the source code at the current breakpoint:

```gdb
(gdb) list
```

**3.10 Quitting GDB**

Exit GDB once debugging is done:

```gdb
(gdb) quit
```

#### 4. Debugging notes

**4.1 Go debug information**

The debug information produced by the Go compiler is limited for GDB. In some cases GDB cannot display Go-specific structs and goroutine information correctly.

**4.2 Compatibility of GDB and Go**

GDB was designed mainly for C and C++, and its Go support is weak. Debugging a fairly complex Go program runs into trouble, for example with concurrency (goroutine) related parts.

#### 5. Summary

Before debugging a Go program, turn off optimization and inlining with `go build -gcflags "all=-N -l"`, then use `break` to set breakpoints, `next`/`step` to step, and `print` to inspect variables. GDB's Go support is limited; structs and goroutine information may not display in full, and this is especially noticeable when debugging concurrent programs.

## References

- [Official · Diagnostics](https://go.dev/doc/diagnostics)
- [runtime/pprof standard library](https://pkg.go.dev/runtime/pprof)
- [Official · Debugging Go Code with GDB](https://go.dev/doc/gdb)


## Sibling pages

- [PGO](/debug/PGO.md)
- [Pprof](/debug/Pprof.md)
- [Debug](/debug/Debug.md)
- [Expvar](/debug/Expvar.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Expvar](/debug/Expvar.md)
