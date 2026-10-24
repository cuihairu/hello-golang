# Go Project Startup Notes
I've written down the directory, module, build, and dependency commands for a minimal Go project here, handy for looking up when starting a new repo.

### 1. Setting up GOPATH and the project directory

`GOPATH` is the root directory of the Go workspace. Add the following to your shell config file (such as `.bashrc` or `.zshrc`):

```sh
export GOPATH=$HOME/go
export PATH=$PATH:$GOPATH/bin
```

Then create the project directory. Assume you want to create a project named `myproject`:

```sh
mkdir -p $GOPATH/src/github.com/yourusername/myproject
cd $GOPATH/src/github.com/yourusername/myproject
```

### 2. Initializing a Go module

Go modules are the dependency management system introduced in Go 1.11, with dependencies recorded in `go.mod`. Initialize a new Go module in the project directory:

```sh
go mod init github.com/yourusername/myproject
```

This creates a `go.mod` file recording the project's module path and dependencies.

### 3. Creating the project structure

A typical Go project structure might look like this:

```
myproject/
├── go.mod
├── go.sum
├── cmd/
│   └── myproject/
│       └── main.go
├── pkg/
│   └── ...
└── internal/
    └── ...
```

- `cmd/`: holds the project's main application entry points.
- `pkg/`: holds library code that other projects can use.
- `internal/`: holds packages that only this project can use.

Create these directories and files:

```sh
mkdir -p cmd/myproject
touch cmd/myproject/main.go
mkdir -p pkg
mkdir -p internal
```

### 4. Writing the code

Write your Go code in `cmd/myproject/main.go`, for example a simple "Hello, World!" program:

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

### 5. Building and running the project

You can use the following commands to build and run your project:

```sh
go build -o bin/myproject ./cmd/myproject
./bin/myproject
```

Or run it directly:

```sh
go run ./cmd/myproject
```

### 6. Adding dependencies

If your project needs external packages, you can use the `go get` command. For example, to use the `gin` framework, you can run:

```sh
go get -u github.com/gin-gonic/gin
```

This automatically updates your `go.mod` and `go.sum` files to include the new dependency.

### 7. Managing dependencies

When you add or update dependencies, the `go mod tidy` command helps you clean up and tidy the `go.mod` and `go.sum` files:

```sh
go mod tidy
```

### Full example

```sh
# set up the project directory
mkdir -p $GOPATH/src/github.com/yourusername/myproject
cd $GOPATH/src/github.com/yourusername/myproject

# initialize the Go module
go mod init github.com/yourusername/myproject

# create the project structure
mkdir -p cmd/myproject
touch cmd/myproject/main.go
mkdir -p pkg
mkdir -p internal

# write the code
echo 'package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}' > cmd/myproject/main.go

# build and run the project
go build -o bin/myproject ./cmd/myproject
./bin/myproject

# or run it directly
go run ./cmd/myproject

# add dependencies
go get -u github.com/gin-gonic/gin

# manage dependencies
go mod tidy
```

After running this set of commands, `bin/myproject` prints `Hello, World!`. Use `go get` to add dependencies later, and `go mod tidy` to clean up.

## References

- [Go official docs · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go official docs · Create a module (external link)](https://go.dev/doc/tutorial/create-module)


## Sibling pages

- [BuildConstraint](/start/BuildConstraint.md)
- [Build](/start/Build.md)
- [Embed](/start/Embed.md)
- [Run](/start/Run.md)
- [Structure](/start/Structure.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Run](/start/Run.md)
- [Structure](/start/Structure.md)
