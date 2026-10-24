In Go, the `vendor` directory is used to manage a project's dependencies: copies of third-party libraries are placed inside the project, so builds no longer depend on external repositories.

### Overview of the `vendor` directory

#### Purpose

- **Package isolation**: the `vendor` directory lets you store copies of the third-party libraries your project depends on inside the project itself, so that updates or changes to those dependencies do not affect the project.
- **Stability**: ensures the project has consistent dependency versions across development environments, unaffected by updates to the external dependency libraries.
- **Build process**: when building the project, the Go toolchain prefers the packages in the `vendor` directory, making sure the versions specified by the project are used.

### Using the `vendor` directory

#### Creating and using a `vendor` directory

1. **Create the `vendor` directory**

   Create a `vendor` directory in the project's root directory and copy the dependency libraries you need into it. You can download and copy them manually, or let Go tools manage it automatically.

2. **Use the `go mod vendor` command**

   The `go mod vendor` command automatically downloads all the dependencies listed in the `go.mod` file into the `vendor` directory.

   ```bash
   go mod vendor
   ```

   This creates the `vendor` directory based on the dependencies specified in the `go.mod` file and places copies of all the dependencies in it.

3. **Build and test**

   When you build or test the project, the Go toolchain automatically prefers the packages in the `vendor` directory. This way you can be sure the project is using pinned dependency versions.

#### Example

A walkthrough of the `vendor` flow, starting from module initialization:

1. **Initialize the module**

   First, make sure you have initialized a Go module:

   ```bash
   go mod init example.com/myapp
   ```

2. **Add dependencies**

   Use the `go get` command to add the dependencies you need:

   ```bash
   go get github.com/some/dependency@v1.2.3
   ```

3. **Generate the `vendor` directory**

   Run the `go mod vendor` command to create the `vendor` directory:

   ```bash
   go mod vendor
   ```

4. **Inspect the `vendor` directory**

   The `vendor` directory will contain all the dependencies you specified in the `go.mod` file. For example, the directory structure might look like this:

   ```
   myapp/
   ├── go.mod
   ├── go.sum
   ├── main.go
   └── vendor/
       └── github.com/
           └── some/
               └── dependency/
                   └── dependency.go
   ```

5. **Build the project**

   When you run `go build` or `go test`, the Go toolchain prefers the packages in the `vendor` directory:

   ```bash
   go build
   ```

   ```bash
   go test
   ```

### Things to watch when using the `vendor` directory

- **Version management**: make sure the dependency versions in the `vendor` directory match the versions specified in your `go.mod` file. You can use `go mod tidy` to tidy and update the `go.mod` file.
- **Storage and synchronization**: putting the `vendor` directory under version control (such as Git) ensures that other developers get the same dependencies when they clone the project.

### Summary

- **`vendor` directory**: stores copies of third-party dependencies, which are preferred during builds; versions are locked by `go.mod`.
- **Creating and managing**: `go mod vendor` generates the directory, and `go mod tidy` tidies `go.mod`.
- **Building and testing**: the Go toolchain prefers the packages in `vendor`, so updates to external dependencies cannot affect this project.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)


## Sibling pages

- [Init](/mod/Init.md)
- [Mod](/mod/Mod.md)
- [Work](/mod/Work.md)
- [Pkg](/mod/Pkg.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Pkg](/mod/Pkg.md)
