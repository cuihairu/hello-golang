# Hello Go
Here I record a minimal program made up of two modules: the main module `hello-go` calls the library module `greeting`'s `Hello()`, printing "Hello, Go!".

### Creating the project structure

First, create the project structure:

```
hello-go/
├── go.mod
├── main.go
└── greeting/
    ├── go.mod
    └── greeting.go
```

### 1. Initializing the main module

Initialize the main module in the `hello-go` directory:

```sh
mkdir -p hello-go
cd hello-go
go mod init hello-go
```

### 2. Creating the main module files

Create the `main.go` file in the `hello-go` directory:

```go
// main.go

package main

// import the greeting module
import (
    "fmt"
    "hello-go/greeting"
)

func main() {
    // call the Hello function in the greeting module
    message := greeting.Hello()
    fmt.Println(message)
}
```

### 3. Initializing the library module

Initialize the library module in the `hello-go/greeting` directory:

```sh
mkdir -p greeting
cd greeting
go mod init hello-go/greeting
```

### 4. Creating the library module files

Create the `greeting.go` file in the `hello-go/greeting` directory:

```go
// greeting.go

package greeting

// the Hello function returns a greeting message
func Hello() string {
    return "Hello, Go!"
}
```

### 5. Setting up the module dependency

Return to the main module directory:

```sh
cd ..
```

Then run the following command to add the `greeting` module dependency:

```sh
go mod edit -replace hello-go/greeting=./greeting
go mod tidy
```

### 6. Running the program

In the main module directory, run the following command to compile and run the program:

```sh
go run main.go
```

You should see the following output:

```
Hello, Go!
```

### Code explanation

#### Main module (`main.go`)

```go
// main.go

package main

// import the standard library fmt for output, and the custom greeting module
import (
    "fmt"
    "hello-go/greeting"
)

func main() {
    // call the Hello function in the greeting module, receiving the returned string
    message := greeting.Hello()
    // print the returned greeting message
    fmt.Println(message)
}
```

1. `package main`: defines the main package, which is the entry-point package of the program.
2. `import ("fmt" "hello-go/greeting")`: imports the standard library `fmt` and the custom module `greeting`.
3. `func main() { ... }`: defines the `main` function, which is the entry point of the Go program.
4. `message := greeting.Hello()`: calls the `Hello` function in the `greeting` module and assigns the returned string to the `message` variable.
5. `fmt.Println(message)`: prints the content of `message` using the `fmt.Println` function.

#### Library module (`greeting.go`)

```go
// greeting.go

package greeting

// the Hello function returns a greeting message
func Hello() string {
    return "Hello, Go!"
}
```

1. `package greeting`: defines the `greeting` package, which provides a public `Hello` function.
2. `func Hello() string { ... }`: defines the `Hello` function, which returns a greeting message of type `string`.
3. `return "Hello, Go!"`: returns the "Hello, Go!" string as the greeting message.

## References

- [Go Official Documentation · Getting started (external link)](https://go.dev/doc/tutorial/getting-started)
- [Go Official Documentation · Create a module (external link)](https://go.dev/doc/tutorial/create-module)

## Sibling pages

- [BuildConstraint](/start/BuildConstraint.md)
- [Build](/start/Build.md)
- [Embed](/start/Embed.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Build](/start/Build.md)
- [Embed](/start/Embed.md)
- [Run](/start/Run.md)
