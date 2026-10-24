A package is Go's unit for organizing code: one directory holds a set of `.go` files, and the `package` declaration at the top of a file names the package. This page covers three things: concept, scope, and imports.

### 1. The concept of a package

#### Definition

A package is a directory containing one or more `.go` files. Every Go source file starts with a `package` declaration that specifies which package the file belongs to. A package's name is usually the same as its directory name.

#### Purpose

- **Encapsulation**: group related functionality and data together, hiding internal implementation details.
- **Organization**: organize code into modules to make it easier to manage and maintain.
- **Reuse**: enable code reuse through package imports and calls.

### 2. Package scope

#### Scope rules

- **Within a package**: inside the same package, all identifiers (functions, variables, constants, types) have package-level scope. Private identifiers inside a package (starting with a lowercase letter) can only be accessed from within the package.
- **Outside a package**: code outside the package cannot access private identifiers inside the package (those starting with a lowercase letter). Only identifiers that start with an uppercase letter are public and can be accessed from outside the package.

Example code:
```go
// file: mathutils.go
package mathutils

// Public function (exported)
func Add(a, b int) int {
    return a + b
}

// Private function (not exported)
func subtract(a, b int) int {
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
    sum := mathutils.Add(10, 5)    // accessible
    // diff := mathutils.subtract(10, 5) // compile error: not accessible
    fmt.Println("Sum:", sum)
}
```

### 3. Importing packages

#### Importing packages

Use `import` to import other packages, and give the package an alias if you need one.

- **Basic import**: import the package directly and access its exported identifiers using the package name as a prefix.
- **Aliased import**: give the imported package an alias to simplify the code or avoid name conflicts.

#### Example code

**Basic import**
```go
package main

import (
    "fmt"
    "math"
)

func main() {
    fmt.Println("Square root of 16 is", math.Sqrt(16)) // using the Sqrt function from the math package
}
```

**Aliased import**
```go
package main

import (
    fmt "fmt" // give the fmt package an alias
    math "math" // give the math package an alias
)

func main() {
    fmt.Println("Square root of 16 is", math.Sqrt(16)) // access the function in the package via the alias
}
```

**Importing multiple packages**
```go
package main

import (
    "fmt"
    "math"
    "time"
)

func main() {
    fmt.Println("Square root of 16 is", math.Sqrt(16))
    fmt.Println("Current time:", time.Now())
}
```

**Importing and ignoring a package**
If you import a package but do not use it, you can import it with `_` (the blank identifier) so that its init functions run, while avoiding a compiler warning about an unused package.

Example code:
```go
package main

import (
    _ "path/to/some/package" // import the package without using it
)

func main() {
    // you can run code here, but the imported package is not used directly
}
```

### Summary

- **Package**: the unit of code organization, used to group related functionality and data together. Each package has its own scope, and the accessibility of an identifier inside a package depends on whether its first letter is uppercase or lowercase.
- **Scope**: identifiers inside a package have package-level scope; only identifiers that start with an uppercase letter can be accessed from outside.
- **Import**: use the `import` statement to import packages, supporting both basic and aliased imports. You can import multiple packages, and use `_` to import a package so its init functions run without using it directly.

To decide whether an identifier is visible to the outside, look only at its first letter: uppercase is exported, lowercase is private to the package. A `_` import only runs the package's initialization and does not occupy a name.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)


## Sibling pages

- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [New](/mod/New.md)
- [Pkg](/mod/Pkg.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [New](/mod/New.md)
- [Pkg](/mod/Pkg.md)
