Go 1.18 introduced the `go.work` file for managing workspaces: it places multiple Go modules in one directory tree so they can reference each other directly during local development, without publishing and fetching in between.

### 1. Overview of the `go.work` file

#### Purpose

The `go.work` file defines a workspace that can contain multiple Go modules. This approach is mainly used in the following situations:

- **Developing multiple related modules**: when you are developing several modules that depend on each other, the `go.work` file helps you manage them in one unified workspace.
- **Local development and testing**: when developing and testing multiple modules locally, you can use the `go.work` file to specify local module paths so that dependencies between modules are resolved correctly.

#### Structure

The `go.work` file is similar to a `go.mod` file, but its purpose is to define configuration for the multiple modules in a workspace. Its basic structure is:

```go
go 1.20

use (
    ./module1
    ./module2
)
```

Here the `use` keyword specifies which modules the workspace contains.

### 2. Using the `go.work` file

#### Initializing a workspace

1. **Create the `go.work` file**

   Create a `go.work` file in the project's root directory and define the modules to include. For example:

   ```go
   go 1.20

   use (
       ./module1
       ./module2
   )
   ```

   Here `./module1` and `./module2` are paths relative to the directory containing the `go.work` file.

2. **Using it inside modules**

   Modules specified in the `go.work` file can reference each other within the workspace. For example, you can reference `module2` from `module1` without downloading it through an external version control system.

3. **Running and building**

   When using the `go` command, the Go toolchain prefers the modules defined in the `go.work` file. Inside each module directory, you can build or test with the `./...` pattern as usual:

   ```bash
   cd module1
   go build ./...
   go test ./...
   ```

   Note: using `./...` directly at the workspace root produces the error `pattern ./...: directory prefix . does not contain modules listed in go.work`, in which case you need to use the module path pattern instead, for example:

   ```bash
   go build example.com/module1/...
   go test example.com/module2/...
   ```

#### Example

Suppose you have a workspace with two modules:

- `module1`: contains a `main` package.
- `module2`: contains a library package.

The project directory structure looks like this:

```
project/
├── go.work
├── module1/
│   └── main.go
└── module2/
    └── library.go
```

**`go.work` file**:

```go
go 1.20

use (
    ./module1
    ./module2
)
```

**`module1/main.go`**:

```go
package main

import (
    "fmt"
    "example.com/module2" // assuming module2's path is example.com/module2
)

func main() {
    fmt.Println(module2.Greet())
}
```

**`module2/library.go`**:

```go
package module2

func Greet() string {
    return "Hello from module2!"
}
```

In this example, you can reference `module2` from `module1` without declaring `module2` as a dependency in `go.mod`. You only need the `go.work` file to manage the whole workspace.

### 3. Related commands

Here are a few commands related to the `go.work` file:

- **`go work init`**: initialize the `go.work` file.

  ```bash
  go work init ./module1 ./module2
  ```

  This creates a new `go.work` file and adds the specified modules to the workspace.

- **`go work edit`**: edit an existing `go.work` file.

  ```bash
  go work edit -use ./module3
  ```

  This adds `module3` to the existing `go.work` file.

### 4. Notes

- **Workspace management**: the `go.work` file exists to make managing multiple modules convenient during development, but it does not affect production builds. Production environments still use each module's `go.mod` file to manage dependencies.
- **Module version control**: when using a `go.work` file, module versions are still managed by each module's `go.mod` file. `go.work` is mainly for local development and testing.

### Summary

`go.work` groups several local modules into one workspace, and the toolchain prefers the modules listed in the workspace when building and testing; production dependencies are still managed by each module's own `go.mod`. Generate the file with `go work init`, and add or remove modules afterwards with `go work edit`.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)
- [Go Official Documentation · Workspaces (external link)](https://go.dev/doc/tutorial/workspaces)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Readme](/distribution/Readme.md)
- [glossary](/glossary.md)
- [Get](/mod/Get.md)
- [Import](/mod/Import.md)
- [New](/mod/New.md)
- [Package](/mod/Package.md)
- [Pkg](/mod/Pkg.md)
- [Vendor](/mod/Vendor.md)
