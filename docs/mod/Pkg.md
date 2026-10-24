A **package** and a **module** are two units for organizing code: a package groups and encapsulates related code, while a module manages a collection of packages and their versions. Different languages call them different things and use them differently, but they all do the same few jobs: organize, encapsulate, reuse.

### 1. Packages

#### Concept

A package is a unit of code organization, used to group related functionality and data together. The main purposes of a package are:

- **Encapsulation**: group related functionality and data together, hiding internal implementation details.
- **Reuse**: let other code reuse the functionality inside the package.
- **Namespace**: prevent naming conflicts and ensure that identifiers in different packages (functions, variables, types) do not interfere with each other.

#### Packages in Go

In Go, a package is the basic unit of code organization. Every Go source file belongs to some package, and every package has a unique name.

- **Defining a package**: a package consists of one or more Go source files located in the same directory, and the `package` statement at the top of each file specifies the package name.
- **Importing a package**: use the `import` statement to import other packages and use the functions, variables, and types they define.
- **Using a package**: a package's public members (identifiers starting with an uppercase letter) can be accessed by other packages, while its private members (identifiers starting with a lowercase letter) can only be accessed from inside the package.

Example code:
```go
// file: mathutils.go
package mathutils

// Add adds two integers.
func Add(a, b int) int {
    return a + b
}

// Subtract subtracts two integers.
func Subtract(a, b int) int {
    return a - b
}
```

```go
// file: main.go
package main

import (
    "fmt"
    "path/to/your/project/mathutils"
)

func main() {
    sum := mathutils.Add(10, 5)
    diff := mathutils.Subtract(10, 5)
    fmt.Println("Sum:", sum)
    fmt.Println("Difference:", diff)
}
```

### 2. Modules

#### Concept

A module is a higher-level unit of code organization, used to manage a collection of packages. The main purposes of a module are:

- **Dependency management**: help manage code dependencies and version control.
- **Versioning**: provide version control for a code repository so that different versions of a module can be managed and used.
- **Encapsulation**: provide a logical grouping of packages, making it easier to distribute and reuse a module.

#### Modules in Go

Go modules were introduced in Go 1.11: a module is a collection of packages carrying version information, from which dependencies and versions are recorded in `go.mod`.

- **Defining a module**: a module is defined by a `go.mod` file located at the module's root directory. The `go.mod` file contains the module's name, its dependencies, and other version information.
- **Using a module**: the `go mod` command can be used to manage a module's dependencies and versions.

Example code:

**Creating a module**
```bash
go mod init example.com/myapp
```

**`go.mod` file**
```go
module example.com/myapp

go 1.20
```

**Adding a dependency**
```bash
go get github.com/some/dependency@v1.2.3
```

**Using a dependency**
```go
package main

import (
    "fmt"
    "github.com/some/dependency"
)

func main() {
    result := dependency.SomeFunction()
    fmt.Println(result)
}
```

**Managing dependencies**
- `go mod tidy`: clean up the `go.mod` and `go.sum` files, removing dependencies that are no longer needed.
- `go mod vendor`: copy all dependencies into the `vendor` directory so you can build offline.

### Summary

- **Package**: groups related functionality together; uppercase identifiers are visible from outside, lowercase ones work only inside the package.
- **Module**: a collection of packages; `go.mod` records the module name, dependencies, and versions.

Each handles a different part: organizing and exporting within a directory belongs to the package, dependency versions belong to the module. `go mod init` creates a module, `go get` adds a dependency, and `go mod tidy` cleans up anything extra.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)


## Sibling pages

- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Package](/mod/Package.md)
- [Vendor](/mod/Vendor.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Package](/mod/Package.md)
- [Vendor](/mod/Vendor.md)
