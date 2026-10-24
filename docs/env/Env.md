### Go and environment variables

Go uses a few environment variables to locate the installation directory, the workspace, and where executables land. The common ones:

#### 1. GOROOT

`GOROOT` is the path to the Go installation directory. This variable points to where the Go toolchain and standard library live. Usually `GOROOT` is set automatically when you install Go and does not need to be configured manually.

**Example**:
```bash
export GOROOT=/usr/local/go
```

#### 2. GOPATH

`GOPATH` is the path to the workspace, used to store Go source code, packages, and executables. The `GOPATH` workspace contains three directories: `src` (source code), `pkg` (compiled packages), and `bin` (compiled executables).

**Example**:
```bash
export GOPATH=$HOME/go
```

#### 3. GOBIN

`GOBIN` is the directory where Go executables are installed. By default it is `$GOPATH/bin`, but it can be customized to any other path.

**Example**:
```bash
export GOBIN=$HOME/go/bin
```

#### 4. GO111MODULE

`GO111MODULE` is the variable used to enable or disable Go module support. It has three values:
- `off`: module support is disabled, using the traditional `GOPATH` mode.
- `on`: module support is enabled, regardless of the current directory.
- `auto`: module support is enabled in a directory containing a `go.mod` file or in its subdirectories.

**Example**:
```bash
export GO111MODULE=on
```

### Go and the relative path problem

Go path issues come down to two places: when importing packages, Go uses the module path; when reading and writing files, it uses the runtime working directory. Distinguish these two and most "file not found" problems will line up.

#### Relative and absolute paths

- **Absolute path**: a full path starting from the root directory.
- **Relative path**: a path relative to the current working directory.

In Go projects, packages are usually imported using the module path rather than a relative path on the file system. This is because Go by design requires package import paths to be based on the module path declared in `go.mod` (for example `myproject/utils`), which avoids the confusion of path dependencies.

#### Relative paths at runtime

When executing a Go program, a relative path is relative to the program's current working directory, not relative to the source file. The execution path refers to the directory the program is running from.

#### Example

Suppose there is a project structure like this:

```
myproject/
├── go.mod
├── main.go
└── data/
    └── file.txt
```

An example of `main.go` reading `data/file.txt`:

```go
package main

import (
    "fmt"
    "log"
    "os"
    "path/filepath"
)

func main() {
    // read the file using a relative path
    path := filepath.Join("data", "file.txt")
    content, err := os.ReadFile(path)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(string(content))
}
```

In this example, the file path `data/file.txt` is relative to the program's current working directory. If you run the program from the `myproject` directory, the file path will be correct. If you run it from some other directory, you need to provide the correct relative path.

### Go modularized projects

Using Go modules, you can create a `go.mod` file at the project root to specify the module path. This makes importing packages simpler and more reliable.

Create the `go.mod` file:

```bash
go mod init myproject
```

Contents of the `go.mod` file:

```
module myproject

go 1.16
```

### Handling relative path problems

Two ways to avoid the relative path pitfalls:

1. **Use Go modules**: make sure there is a `go.mod` file at the project root, and import packages using the module path.
2. **Set the working directory correctly**: before running the program, make sure the current working directory is the directory the program expects.

### Code example

The program below first prints the current working directory, then reads a file using a relative path:

```go
package main

import (
    "fmt"
    "log"
    "os"
    "path/filepath"
)

func main() {
    // get the current working directory
    cwd, err := os.Getwd()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("Current working directory:", cwd)

    // read the file using a relative path
    path := filepath.Join("data", "file.txt")
    content, err := os.ReadFile(path)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println("File content:", string(content))
}
```

Create the `go.mod` file:

```bash
go mod init myproject
```

Set the environment variables:

```bash
export GOPATH=$HOME/go
export GOBIN=$HOME/go/bin
export GO111MODULE=on
```

Make sure the working directory is correct:

```bash
cd myproject
go run main.go
```

### Summary

`GOROOT` points to the installation directory, `GOPATH` manages the workspace, `GOBIN` manages where executables land, and `GO111MODULE` decides whether module mode is on. Package imports only recognize the module path in `go.mod`; file reads only recognize the runtime working directory — `cd` to the expected directory before starting the program, then run `go run`.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules usage guide](https://go.dev/doc/modules/)

<!-- BACKLINKS-AUTO -->
## Related pages

- [GOPROXY](/env/GOPROXY.md)
- [Goland](/env/Goland.md)
- [Modules](/env/Modules.md)
- [Tools](/env/Tools.md)
- [Vim](/env/Vim.md)
- [ide](/env/ide.md)
- [vscode](/env/vscode.md)
- [glossary](/glossary.md)
