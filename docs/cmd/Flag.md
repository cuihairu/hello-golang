### 3. Parsing Command-line Arguments with the Standard Library `flag` Package

The standard library `flag` package parses command-line arguments and supports options of types such as boolean, integer, and string. Here I record its common usage with 7 small examples.

#### 3.1 Overview of the `flag` Package

The core of the `flag` package is two steps: "define options + parse". Declare options with functions like `flag.Bool` and `flag.String`; after `flag.Parse`, the variables hold the values passed in from the command line.

#### 3.2 Defining and Parsing Boolean Options

Boolean options represent switch-style parameters, for example enabling or disabling a feature. Use the `flag.Bool` function to define a boolean option:

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    verbose := flag.Bool("verbose", false, "Enable verbose output")

    flag.Parse()

    if *verbose {
        fmt.Println("Verbose output enabled")
    } else {
        fmt.Println("Verbose output disabled")
    }
}
```

Run example:

```shell
$ go run main.go --verbose
Verbose output enabled

$ go run main.go
Verbose output disabled
```

#### 3.3 Defining and Parsing String Options

String options pass string-type parameters, for example a file path or a username. Use the `flag.String` function to define a string option:

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    name := flag.String("name", "World", "Name to greet")

    flag.Parse()

    fmt.Printf("Hello, %s!\n", *name)
}
```

Run example:

```shell
$ go run main.go --name=Go
Hello, Go!

$ go run main.go
Hello, World!
```

#### 3.4 Defining and Parsing Integer Options

Integer options pass integer-type parameters, for example a port number or a retry count. Use the `flag.Int` function to define an integer option:

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    port := flag.Int("port", 8080, "Port number")

    flag.Parse()

    fmt.Printf("Server running on port %d\n", *port)
}
```

Run example:

```shell
$ go run main.go --port=9090
Server running on port 9090

$ go run main.go
Server running on port 8080
```

#### 3.5 Defining and Parsing Other Types of Options

The `flag` package also supports other option types, such as floating point numbers and time values. Use the corresponding functions `flag.Float64` and `flag.Duration` to define these options. For example:

```go
package main

import (
    "flag"
    "fmt"
    "time"
)

func main() {
    timeout := flag.Duration("timeout", 30*time.Second, "Timeout duration")

    flag.Parse()

    fmt.Printf("Timeout: %v\n", *timeout)
}
```

Run example:

```shell
$ go run main.go --timeout=1m
Timeout: 1m0s

$ go run main.go
Timeout: 30s
```

#### 3.6 Custom Option Parsing

Beyond the standard types, the `flag` package also supports custom option parsing. You can implement the `flag.Value` interface to define a custom option type. The `flag.Value` interface defines the `Set` and `String` methods:

```go
package main

import (
    "flag"
    "fmt"
)

type myFlag string

func (f *myFlag) Set(value string) error {
    *f = myFlag(value)
    return nil
}

func (f *myFlag) String() string {
    return string(*f)
}

func main() {
    var customFlag myFlag
    flag.Var(&customFlag, "custom", "Custom flag example")

    flag.Parse()

    fmt.Printf("Custom flag: %s\n", customFlag)
}
```

Run example:

```shell
$ go run main.go --custom=example
Custom flag: example
```

#### 3.7 Handling Undefined Options and Help Information

The `flag` package automatically generates help information so users can see the available options. When a user passes an undefined option, the `flag` package automatically prints an error message and displays the help information:

```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    help := flag.Bool("help", false, "Display help")

    flag.Parse()

    if *help {
        flag.Usage()
        os.Exit(0)
    }

    fmt.Println("Running the program")
}
```

Run example:

```shell
$ go run main.go --help
Usage of /tmp/go-build123456/b001/exe/main:
  -help
        Display help

$ go run main.go --undefined
flag provided but not defined: -undefined
Usage of /tmp/go-build123456/b001/exe/main:
  -help
        Display help
exit status 2
```

#### 3.8 Parsing Positional Arguments

Positional arguments are the arguments passed to the program in order. When using the `flag` package to parse positional arguments, you handle them manually after calling `flag.Parse`:

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    flag.Parse()
    args := flag.Args()

    if len(args) < 2 {
        fmt.Println("Usage: main.go <input> <output>")
        return
    }

    input := args[0]
    output := args[1]

    fmt.Printf("Input: %s\n", input)
    fmt.Printf("Output: %s\n", output)
}
```

Run example:

```shell
$ go run main.go input.txt output.txt
Input: input.txt
Output: output.txt

$ go run main.go
Usage: main.go <input> <output>
```

### Summary

The usage of the `flag` package boils down to a few steps: declare options with functions like `flag.Bool`/`flag.String`/`flag.Int`, parse with `flag.Parse`, and read the value through the pointer variable; use `flag.Float64` and `flag.Duration` for floats and durations, implement the `flag.Value` interface for special types, leave positional arguments in `flag.Args()`, and undefined options trigger an error plus the printed help.

## References

- [flag standard library](https://pkg.go.dev/flag)
- [os/exec standard library](https://pkg.go.dev/os/exec)

## Sibling pages

- [Design](/cmd/Design.md)
- [Lib](/cmd/Lib.md)
- [Parse](/cmd/Parse.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Design](/cmd/Design.md)
- [Lib](/cmd/Lib.md)
- [Parse](/cmd/Parse.md)
- [Readme](/cmd/Readme.md)
- [Syntax](/cmd/Syntax.md)
