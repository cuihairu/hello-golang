### Go's `init` function

In Go, an `init` function is a special function that runs automatically when a package is initialized, without being called explicitly.

#### The purpose of `init` functions

`init` functions are mainly used for package-level initialization. They run when a package is first imported, before any other code executes. Typical uses include:

1. **Initializing package-level variables**: you can perform complex initialization inside an `init` function.
2. **Running runtime configuration**: for example, reading a configuration file or setting up logging.
3. **Registering dependencies**: for example, registering a type or plugin into a global registry.

#### Characteristics of `init` functions

1. **Executed automatically**: an `init` function does not need to be called explicitly; the Go runtime executes it when the package is initialized.
2. **No parameters or return values**: an `init` function cannot have parameters or return values.
3. **Multiple definitions allowed**: a package can contain several `init` functions, and they run in the order they appear in the source files.
4. **Order of execution**: packages are initialized in import order — imported packages are initialized first, then the importing package.
5. **Every file can have an `init` function**: the several source files in a package can each define an `init` function, and all of them are executed.

#### Example

```go
package main

import (
    "fmt"
)

var globalVar int

func init() {
    globalVar = 42
    fmt.Println("init function executed, globalVar set to:", globalVar)
}

func main() {
    fmt.Println("main function executed, globalVar is:", globalVar)
}
```

#### `init` versus `main`

Both `init` and `main` are special functions; they differ in when they are called and what they are for.

1. **When they are called**:
   - An `init` function runs automatically when the package is initialized.
   - The `main` function is the program's entry point and runs after all package initialization is complete.

2. **Scope of purpose**:
   - An `init` function is used for package-level initialization, and each package can have its own `init` function.
   - The `main` function is used for the program's overall logic, and a program can have only one `main` function.

3. **Definition and use**:
   - An `init` function cannot have parameters or return values, and several can be defined in a single package.
   - The `main` function cannot have parameters or return values, and only one can be defined, in the `main` package.

#### Comparison example

```go
package main

import (
    "fmt"
)

func init() {
    fmt.Println("This is the init function")
}

func main() {
    fmt.Println("This is the main function")
}
```

Output:

```
This is the init function
This is the main function
```

### Summary

- An `init` function is a special function used for package initialization; it does not need to be called explicitly and runs automatically when the package is imported.
- The `main` function is the program's entry point and runs after all `init` functions have finished.
- `init` functions are used for package-level initialization; the `main` function is used for the program's overall logic.

Remember the order: first initialize each package's `init` according to the import relationships, and only after all of them have run does execution enter `main`.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)

<!-- BACKLINKS-AUTO -->
## Related pages

- [glossary](/glossary.md)
- [Get](/mod/Get.md)
- [Import](/mod/Import.md)
- [New](/mod/New.md)
- [Package](/mod/Package.md)
- [Pkg](/mod/Pkg.md)
- [Vendor](/mod/Vendor.md)
