### 5. Advanced Command-line Argument Parsing

This page covers four topics: multi-level subcommands, dynamically generated commands, and autocompletion, plus a few practices around environment variables, error handling, internationalization, and testing.

#### 5.1 Handling Complex Subcommand Structures

In real applications, command-line tools often need to support multi-level subcommands. We use `cobra` and `urfave/cli` as examples to show how to handle complex subcommand structures.

##### 5.1.1 Handling Complex Subcommands with `cobra`

The following example shows how to use `cobra` to handle multi-level subcommands:

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{Use: "app"}

    var userCmd = &cobra.Command{
        Use:   "user",
        Short: "User management commands",
    }

    var addUserCmd = &cobra.Command{
        Use:   "add",
        Short: "Add a new user",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println("User added")
        },
    }

    var deleteUserCmd = &cobra.Command{
        Use:   "delete",
        Short: "Delete an existing user",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println("User deleted")
        },
    }

    userCmd.AddCommand(addUserCmd)
    userCmd.AddCommand(deleteUserCmd)
    rootCmd.AddCommand(userCmd)

    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go user add
User added

$ go run main.go user delete
User deleted
```

##### 5.1.2 Handling Complex Subcommands with `urfave/cli`

The following example shows how to use `urfave/cli` to handle multi-level subcommands:

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
                Name:    "user",
                Aliases: []string{"u"},
                Usage:   "User management commands",
                Subcommands: []*cli.Command{
                    {
                        Name:  "add",
                        Usage: "Add a new user",
                        Action: func(c *cli.Context) error {
                            fmt.Println("User added")
                            return nil
                        },
                    },
                    {
                        Name:  "delete",
                        Usage: "Delete an existing user",
                        Action: func(c *cli.Context) error {
                            fmt.Println("User deleted")
                            return nil
                        },
                    },
                },
            },
        },
    }

    app.Run(os.Args)
}
```

Run example:

```shell
$ go run main.go user add
User added

$ go run main.go user delete
User deleted
```

#### 5.2 Dynamically Generating Commands

In some cases a command-line tool needs to generate commands from dynamic data — for example, reading the list of available commands from a configuration file or a database. We use `cobra` as an example to show how to generate commands dynamically.

##### 5.2.1 Dynamically Generating `cobra` Commands

The following example shows how to generate `cobra` commands from dynamic data:

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{Use: "app"}

    commands := []string{"start", "stop", "restart"}

    for _, cmd := range commands {
        command := &cobra.Command{
            Use:   cmd,
            Short: fmt.Sprintf("%s the service", cmd),
            Run: func(c *cobra.Command, args []string) {
                fmt.Printf("%s command executed\n", c.Use)
            },
        }
        rootCmd.AddCommand(command)
    }

    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go start
start command executed

$ go run main.go stop
stop command executed
```

#### 5.3 Implementing Autocompletion

`cobra` ships with autocompletion support; here is how:

##### 5.3.1 Adding Autocompletion to `cobra`

First, install `bash-completion`:

```shell
brew install bash-completion
```

Then add autocompletion support in your `cobra` project:

```go
package main

import (
    "fmt"
    "github.com/spf13/cobra"
)

func main() {
    var rootCmd = &cobra.Command{Use: "app"}

    var completionCmd = &cobra.Command{
        Use:   "completion",
        Short: "Generate bash completion script",
        Run: func(cmd *cobra.Command, args []string) {
            rootCmd.GenBashCompletionFile("app_completion.sh")
            fmt.Println("Bash completion script generated: app_completion.sh")
        },
    }

    rootCmd.AddCommand(completionCmd)
    rootCmd.Execute()
}
```

Run example:

```shell
$ go run main.go completion
Bash completion script generated: app_completion.sh

$ source ./app_completion.sh
$ app [TAB]
completion  start        stop         restart
```

#### 5.4 Advanced Features and Best Practices

The four items below are common practices; each gets a direction only, no expanded code:

##### 5.4.1 Supporting Environment Variables

A command-line tool's behavior can be configured with environment variables instead of being written into a configuration file. Both `cobra` and `urfave/cli` support reading environment variables.

##### 5.4.2 Unified Error Handling

Route error messages and logs through the same handling; do not let every subcommand roll its own.

##### 5.4.3 Internationalization and Localization

Switch prompt messages to the user's language. `cobra` provides some basic internationalization support.

##### 5.4.4 Testing and Continuous Integration

Write tests for the command-line tool and run them automatically with tools like GitHub Actions or Travis CI.

### Summary

This page records the implementations of multi-level subcommands, dynamically generated commands, and autocompletion, plus four practices: environment variables, error handling, internationalization, and testing. The first three have complete code; the latter four only give a direction.

## References

- [flag standard library](https://pkg.go.dev/flag)
- [os/exec standard library](https://pkg.go.dev/os/exec)

## Sibling pages

- [Design](/cmd/Design.md)
- [Flag](/cmd/Flag.md)
- [Lib](/cmd/Lib.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Design](/cmd/Design.md)
- [Flag](/cmd/Flag.md)
- [Lib](/cmd/Lib.md)
- [Readme](/cmd/Readme.md)
