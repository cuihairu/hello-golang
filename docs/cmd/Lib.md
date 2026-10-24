### 4. Parsing Command-line Arguments with Third-party Libraries

Beyond the standard library `flag` package, the commonly used command-line argument parsing libraries are `cobra` and `urfave/cli`. They support subcommands, aliases, auto-generated help information, and other features `flag` does not have.

#### 4.1 Using the `cobra` Library

`cobra` is developed by `spf13` and supports subcommands, command aliases, auto-generated help information, and more; it is commonly used to build applications with multiple subcommands.

##### 4.1.1 Installing `cobra`

```shell
go get github.com/spf13/cobra
```

##### 4.1.2 Basic Usage

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{
        Use:   "app",
        Short: "A simple command-line application",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println("Hello, Cobra!")
        },
    }

    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go
Hello, Cobra!
```

##### 4.1.3 Adding Option Arguments

You can use the `Flags()` method to add option arguments to a command:

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var name string

    var rootCmd = &cobra.Command{
        Use:   "app",
        Short: "A simple command-line application",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Printf("Hello, %s!\n", name)
        },
    }

    rootCmd.Flags().StringVarP(&name, "name", "n", "World", "Name to greet")

    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go --name=Go
Hello, Go!

$ go run main.go
Hello, World!
```

##### 4.1.4 Adding Subcommands

You can use the `AddCommand()` method to add subcommands to an application:

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{Use: "app"}

    var greetCmd = &cobra.Command{
        Use:   "greet",
        Short: "Greet someone",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println("Hello, World!")
        },
    }

    rootCmd.AddCommand(greetCmd)
    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go greet
Hello, World!
```

##### 4.1.5 A More Complex Example

Combining subcommands with option arguments:

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{Use: "app"}

    var greetCmd = &cobra.Command{
        Use:   "greet",
        Short: "Greet someone",
        Run: func(cmd *cobra.Command, args []string) {
            name, _ := cmd.Flags().GetString("name")
            fmt.Printf("Hello, %s!\n", name)
        },
    }

    greetCmd.Flags().StringP("name", "n", "World", "Name to greet")

    rootCmd.AddCommand(greetCmd)
    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go greet --name=Go
Hello, Go!

$ go run main.go greet
Hello, World!
```

#### 4.2 Using the `urfave/cli` Library

`urfave/cli` is another common choice, supporting subcommands, command aliases, and multiple option types.

##### 4.2.1 Installing `urfave/cli`

```shell
go get -u github.com/urfave/cli/v2
```

##### 4.2.2 Basic Usage

```go
package main

import (
    "fmt"
    "os"
    "github.com/urfave/cli/v2"
)

func main() {
    app := &cli.App{
        Name:  "app",
        Usage: "A simple command-line application",
        Action: func(c *cli.Context) error {
            fmt.Println("Hello, CLI!")
            return nil
        },
    }

    app.Run(os.Args)
}
```

Run example:

```shell
$ go run main.go
Hello, CLI!
```

##### 4.2.3 Adding Option Arguments

You can use the `Flags` field to add option arguments to a command:

```go
package main

import (
    "fmt"
    "os"
    "github.com/urfave/cli/v2"
)

func main() {
    app := &cli.App{
        Name:  "app",
        Usage: "A simple command-line application",
        Flags: []cli.Flag{
            &cli.StringFlag{
                Name:  "name",
                Value: "World",
                Usage: "Name to greet",
            },
        },
        Action: func(c *cli.Context) error {
            name := c.String("name")
            fmt.Printf("Hello, %s!\n", name)
            return nil
        },
    }

    app.Run(os.Args)
}
```

Run example:

```shell
$ go run main.go --name=Go
Hello, Go!

$ go run main.go
Hello, World!
```

##### 4.2.4 Adding Subcommands

You can use the `Commands` field to add subcommands to an application:

```go
package main

import (
    "fmt"
    "os"
    "github.com/urfave/cli/v2"
)

func main() {
    app := &cli.App{
        Name:  "app",
        Usage: "A simple command-line application",
        Commands: []*cli.Command{
            {
                Name:    "greet",
                Aliases: []string{"g"},
                Usage:   "Greet someone",
                Action: func(c *cli.Context) error {
                    fmt.Println("Hello, World!")
                    return nil
                },
            },
        },
    }

    app.Run(os.Args)
}
```

Run example:

```shell
$ go run main.go greet
Hello, World!
```

##### 4.2.5 A More Complex Example

Combining subcommands with option arguments:

```go
package main

import (
    "fmt"
    "os"
    "github.com/urfave/cli/v2"
)

func main() {
    app := &cli.App{
        Name:  "app",
        Usage: "A simple command-line application",
        Commands: []*cli.Command{
            {
                Name:    "greet",
                Aliases: []string{"g"},
                Usage:   "Greet someone",
                Flags: []cli.Flag{
                    &cli.StringFlag{
                        Name:  "name",
                        Value: "World",
                        Usage: "Name to greet",
                    },
                },
                Action: func(c *cli.Context) error {
                    name := c.String("name")
                    fmt.Printf("Hello, %s!\n", name)
                    return nil
                },
            },
        },
    }

    app.Run(os.Args)
}
```

Run example:

```shell
$ go run main.go greet --name=Go
Hello, Go!

$ go run main.go greet
Hello, World!
```

### Summary

Both `cobra` and `urfave/cli` can build command-line programs with subcommands, option arguments, and automatic help; the two are comparable in capability. `urfave/cli` configures everything through fields on a single `App` struct, which is less work for small programs; `cobra`'s command tree stays clearer as subcommand levels multiply. Pick whichever fits your scenario.

## References

- [flag standard library](https://pkg.go.dev/flag)
- [os/exec standard library](https://pkg.go.dev/os/exec)

## Sibling pages

- [Design](/cmd/Design.md)
- [Flag](/cmd/Flag.md)
- [Parse](/cmd/Parse.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Design](/cmd/Design.md)
- [Flag](/cmd/Flag.md)
- [Parse](/cmd/Parse.md)
- [Readme](/cmd/Readme.md)
- [Syntax](/cmd/Syntax.md)
