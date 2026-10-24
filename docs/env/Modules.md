# Package manager
Go uses `go mod` to manage dependencies, and the `go.mod` file records the module path and dependency versions. Here are the commonly used commands organized by purpose:

### Basic concepts of `go mod`

1. **Module**: a module is a directory tree of Go source files whose root directory contains a `go.mod` file. A module contains one or more packages.
2. **Package**: a package is a collection of Go source files that are all in the same directory and declare the same package.
3. **Dependency**: refers to the other modules a project depends on.

### `go mod` commands in detail

#### Initializing and creating a module

- `go mod init <module-path>`: initializes a new module and creates a `go.mod` file. `<module-path>` is the module's path, usually the project's repository URL.

```sh
go mod init github.com/user/project
```

#### Managing dependencies

- `go get <package>`: adds or updates a dependency package. You can specify a particular version, such as `@v1.2.3`.

```sh
go get github.com/sirupsen/logrus@v1.8.1
```

- `go mod tidy`: cleans up module dependencies. It removes unused dependencies from the `go.mod` file and downloads missing ones.

```sh
go mod tidy
```

- `go mod vendor`: copies dependency packages into the `vendor` directory. You can then read dependencies from the `vendor` directory when using `go build` and `go test`.

```sh
go mod vendor
```

#### Viewing dependencies

- `go list -m all`: lists all module dependencies.

```sh
go list -m all
```

- `go mod graph`: prints the module dependency graph.

```sh
go mod graph
```

- `go mod why <package>`: explains why a given dependency package is needed.

```sh
go mod why github.com/sirupsen/logrus
```

#### Version management

- `go mod edit`: a tool for manually editing the `go.mod` file; you can change the module path, versions, and so on.

```sh
go mod edit -require=github.com/sirupsen/logrus@v1.8.1
```

#### Upgrading and downgrading dependencies

- `go get -u`: upgrades all dependency packages to the latest version.

```sh
go get -u
```

- `go get <package>@latest`: upgrades a specific package to the latest version.

```sh
go get github.com/sirupsen/logrus@latest
```

- `go get <package>@<version>`: downgrades or upgrades a specific package to a particular version.

```sh
go get github.com/sirupsen/logrus@v1.7.0
```

### Summary

`go mod` is Go's entry point for dependency management: `go mod init` creates a module, `go get` adds or removes dependencies, `go mod tidy` cleans up unused entries, and `go mod vendor` copies dependencies into the `vendor` directory. These commands, together with the versions recorded in `go.mod`, let the same code pull in the same set of dependencies when building on different machines.

## References

- [Official · Installing and managing the Go toolchain](https://go.dev/doc/manage-install)
- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Official · Go Modules usage guide](https://go.dev/doc/modules/)


## Sibling pages

- [Env](/env/Env.md)
- [Install](/env/Install.md)
- [GOPROXY](/env/GOPROXY.md)
- [Tools](/env/Tools.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Tools](/env/Tools.md)
