A package's import path determines how code references it, and an identifier's first letter determines whether it is visible to the outside. Together they control the dependency relationships between packages.

### 1. Package import paths

#### Concept

- **Import path**: An import path is the unique identifier used to reference and access a Go package; it points at the package's directory.
- **Standard library packages**: Packages in the Go standard library are referenced through predefined import paths, such as `fmt`, `os`, and `net/http`.
- **Third-party packages**: Third-party packages are typically referenced through their module path, such as `github.com/some/package`.
- **Local packages**: Local packages in a project are imported via the module path. For example, if this project's `go.mod` declares the module name `myapp`, then the import path for the `utils` package is `myapp/utils` (note: Go module mode does not support relative import paths such as `./mypackage`).

#### Example

Suppose your project directory looks like this:

```
myapp/
├── go.mod
├── main.go
└── utils/
    └── helper.go
```

**`main.go` file**:

```go
package main

import (
    "fmt"
    "myapp/utils" // import a local package
)

func main() {
    fmt.Println(utils.Greet())
}
```

**`utils/helper.go` file**:

```go
package utils

func Greet() string {
    return "Hello from utils!"
}
```

In this example, `main.go` imports the `utils` package with `import "myapp/utils"`, and the `Greet` function in the `utils` package is called from the `main` package.

### 2. Package visibility

#### Concept

- **Visibility**: A package's visibility refers to whether the identifiers (variables, functions, types, and so on) in it can be accessed from outside the package. Go uses an identifier's first letter to decide its visibility.
- **Public identifier**: An identifier that starts with an uppercase letter is visible to outside packages. For example, the `Greet` function is public.
- **Private identifier**: An identifier that starts with a lowercase letter is not visible to outside packages. For example, the `greetHelper` function is private.

#### Example

Consider these two packages:

**`utils/helper.go` file**:

```go
package utils

// Public function
func Greet() string {
    return "Hello from utils!"
}

// Private function
func greetHelper() string {
    return "This is a helper function."
}
```

**`main.go` file**:

```go
package main

import (
    "fmt"
    "myapp/utils"
)

func main() {
    fmt.Println(utils.Greet()) // accessible
    // fmt.Println(utils.greetHelper()) // compile error: not accessible
}
```

In this example:

- The `utils.Greet` function is accessible from the `main` package because its first letter is uppercase, meaning it is public.
- The `utils.greetHelper` function is not accessible from the `main` package because its first letter is lowercase, meaning it is private.

### 3. Managing import paths and visibility

#### Package import paths

- **Module path**: It is recommended to import packages using the module path, such as `github.com/user/project/package`. The module path is defined in the `go.mod` file.
- **Relative path**: Go module mode does **not** support relative import paths such as `./` or `../`. Using them directly produces the error `relative import paths are not supported in module mode`, and you must use the module path instead.

#### Package visibility control

Put the related identifiers in the same package, expose only the uppercase ones to the outside, keep the lowercase ones as internal implementation. The package's external interface is controlled by the exported names.

### 4. Package management in `go.mod`

The `go.mod` file defines the module's path and its dependencies. For example:

**`go.mod` file**:

```go
module myapp

go 1.20

require (
    github.com/some/dependency v1.2.3
)
```

`go.mod` records the dependencies a project needs along with their versions.

### Summary

- **Package import paths**: write the package name directly for the standard library; use the module path declared in `go.mod` followed by the directory for third-party and local packages. Relative paths are not supported.
- **Package visibility**: identifiers that start with an uppercase letter are exported to outside the package; identifiers that start with a lowercase letter stay inside.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)


## Sibling pages

- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Get](/mod/Get.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Get](/mod/Get.md)
