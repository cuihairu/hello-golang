In Go, package management is a key part of development. Go's package management system includes modules (`go mod`) and the older GOPATH mode. This page focuses on the Go Modules (`go mod`) approach, since it is the recommended way for Go and the current mainstream.

### Overview of Go package management

#### 1. Go Modules (`go mod`)

**Go Modules** is the officially recommended way to manage packages in Go. It was introduced in Go 1.11 and became the default in Go 1.13. Dependencies and versions are recorded in the module's own files, with no reliance on a global workspace.

##### Core concepts

- **`go.mod` file**: records the module's basic information and its dependencies.
- **`go.sum` file**: records a checksum for each dependency to ensure the dependency's integrity.
- **Module path**: the unique name that identifies a module, usually the repository URL or a unique identifier.
- **Module version**: each dependency has a version number, and versions can be managed with semantic versioning (SemVer).

##### Common commands

- **Initialize a module**: create a `go.mod` file and initialize the module.
  ```bash
  go mod init example.com/myapp
  ```

- **Add a dependency**: add a new dependency or update an existing one.
  ```bash
  go get github.com/some/dependency@v1.2.3
  ```

- **Update dependencies**: update all dependencies to the latest minor or patch version.
  ```bash
  go get -u
  ```

- **Tidy dependencies**: remove dependencies that are no longer needed, and update the `go.mod` and `go.sum` files.
  ```bash
  go mod tidy
  ```

- **Create the `vendor` directory**: save copies of all dependencies in the `vendor` directory.
  ```bash
  go mod vendor
  ```

- **View module information**: display detailed information about the modules.
  ```bash
  go list -m all
  ```

#### 2. GOPATH mode (historical)

Before Go Modules existed, Go used the GOPATH mode for package management. GOPATH mode is based on the concept of a workspace, which stores all packages and dependencies under a single designated directory. This approach is fairly simple, but it has some limitations, such as:

- **Global dependencies**: all projects share the same set of dependencies, which can cause version conflicts.
- **Package path problems**: package paths must follow a specific directory structure.
- **Difficult version management**: it is not easy to manage different versions of the same dependency.

**Basic GOPATH mode concepts:**

- **GOPATH environment variable**: specifies the workspace directory, which contains the `src` (source code), `pkg` (compiled packages), and `bin` (executables) directories.
- **Package path**: the package path relates to the GOPATH directory structure, for example `GOPATH/src/github.com/user/project`.

### Examples

**Example 1: managing a project with `go mod`**

1. **Initialize the module**

   Run the following in the project root:
   ```bash
   go mod init example.com/myapp
   ```

2. **Add a dependency**

   Add a third-party dependency:
   ```bash
   go get github.com/some/dependency@v1.2.3
   ```

3. **View the `go.mod` file**

   ```go
   module example.com/myapp

   go 1.20

   require (
       github.com/some/dependency v1.2.3
   )
   ```

4. **Tidy dependencies**

   Clean up unused dependencies:
   ```bash
   go mod tidy
   ```

5. **Create the `vendor` directory**

   ```bash
   go mod vendor
   ```

6. **Build using the `vendor` directory**

   ```bash
   go build
   ```

**Example 2: GOPATH mode**

1. **Set GOPATH**

   Set the GOPATH environment variable, for example:
   ```bash
   export GOPATH=$HOME/go
   ```

2. **Directory structure**

   ```
   $GOPATH/
   ├── src/
   │   └── github.com/
   │       └── user/
   │           └── project/
   │               ├── main.go
   │               └── go.mod
   ├── bin/
   └── pkg/
   ```

3. **Download and manage packages**

   Use `go get` to download and manage packages:
   ```bash
   go get github.com/some/dependency
   ```

### Summary

- **Go Modules** is the currently recommended way to manage packages, providing concise dependency management, version control, and a build process.
- **`go.mod` and `go.sum`** files are used to manage a module and its dependencies, ensuring stability and consistency across dependencies.
- **GOPATH mode** was the package management approach before Go Modules; it is simple but has some limitations.

Commit `go.mod` and `go.sum` to the repository, and anyone who clones it will build against the same set of dependencies.

## References

- [Official · Go Modules user guide](https://go.dev/doc/modules/)
- [Go Modules Reference](https://go.dev/ref/mod)
- [Official blog · Using Go Modules](https://go.dev/blog/using-go-modules)

## Sibling pages

- [Readme](/distribution/Readme.md)

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
