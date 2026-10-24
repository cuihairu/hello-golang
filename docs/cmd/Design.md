### 6. Designing and Implementing Command-line Tools

A command-line tool is more than its code: design, user experience, extensibility, and maintainability all matter. I organized this approach in the order of requirements analysis, design, and implementation.

#### 6.1 Requirements Analysis

Before designing, nail down the tool's goals and requirements:

- **User goals**: Understand who the tool's main users are and what they need.
- **Functional requirements**: Pin down the list of features the tool must implement.
- **Non-functional requirements**: Performance requirements, extensibility, maintainability, security, and so on.

Example: suppose we want to design a database management command-line tool. Its requirements might include:

- Support connecting to different types of databases (MySQL, PostgreSQL, etc.).
- Provide database query, backup, and restore features.
- Provide friendly help and documentation.

#### 6.2 User Experience Design

User experience design for a command-line tool mainly covers these aspects:

- **Command and argument design**: Command and argument names should be short and guessable, matching user habits.
- **Help information**: Every command lists what its arguments mean plus examples, so a new user can run it by following along.
- **Error handling**: When something fails, say which step failed and how to fix it.

Example: command design for the database management tool

```shell
dbtool connect --type=mysql --host=localhost --user=root --password=123456
dbtool query --sql="SELECT * FROM users"
dbtool backup --output=/path/to/backup
dbtool restore --input=/path/to/backup
```

#### 6.3 Architecture Design

The architecture of a command-line tool should account for extensibility and maintainability; common architecture patterns include modular design and plugin-based design.

- **Modular design**: Break the features into modules, which makes them easier to maintain and extend.
- **Plugin-based design**: Support feature extension through a plugin mechanism, suitable for large tools.

Example: modular design

```shell
cmd/
    connect.go
    query.go
    backup.go
    restore.go
internal/
    db/
        mysql.go
        postgresql.go
    utils/
        config.go
        logger.go
```

#### 6.4 Implementation Example

The following example shows how to use the `cobra` library to implement a simple database management command-line tool.

##### 6.4.1 Project Structure

```shell
dbtool/
    cmd/
        root.go
        connect.go
        query.go
        backup.go
        restore.go
    internal/
        db/
            mysql.go
            postgresql.go
        utils/
            config.go
            logger.go
    main.go
```

##### 6.4.2 Root Command Implementation

`cmd/root.go`

```go
package cmd

import (
    "fmt"
    "os"

    "github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
    Use:   "dbtool",
    Short: "A database management tool",
    Long:  `dbtool is a CLI tool for managing databases like MySQL and PostgreSQL.`,
}

func Execute() {
    if err := rootCmd.Execute(); err != nil {
        fmt.Println(err)
        os.Exit(1)
    }
}
```

##### 6.4.3 Connect Command Implementation

`cmd/connect.go`

```go
package cmd

import (
    "fmt"
    "github.com/spf13/cobra"
    "dbtool/internal/db"
)

var connectCmd = &cobra.Command{
    Use:   "connect",
    Short: "Connect to a database",
    Run: func(cmd *cobra.Command, args []string) {
        dbType, _ := cmd.Flags().GetString("type")
        host, _ := cmd.Flags().GetString("host")
        user, _ := cmd.Flags().GetString("user")
        password, _ := cmd.Flags().GetString("password")
        
        err := db.Connect(dbType, host, user, password)
        if err != nil {
            fmt.Println("Error connecting to database:", err)
        } else {
            fmt.Println("Connected to database successfully")
        }
    },
}

func init() {
    rootCmd.AddCommand(connectCmd)
    connectCmd.Flags().String("type", "", "Type of the database (mysql, postgresql)")
    connectCmd.Flags().String("host", "", "Database host")
    connectCmd.Flags().String("user", "", "Database user")
    connectCmd.Flags().String("password", "", "Database password")
}
```

##### 6.4.4 Database Connection Implementation

`internal/db/db.go`

```go
package db

import (
    "fmt"
)

func Connect(dbType, host, user, password string) error {
    switch dbType {
    case "mysql":
        return connectMySQL(host, user, password)
    case "postgresql":
        return connectPostgreSQL(host, user, password)
    default:
        return fmt.Errorf("unsupported database type: %s", dbType)
    }
}

func connectMySQL(host, user, password string) error {
    // implement the MySQL connection logic
    fmt.Println("Connecting to MySQL...")
    return nil
}

func connectPostgreSQL(host, user, password string) error {
    // implement the PostgreSQL connection logic
    fmt.Println("Connecting to PostgreSQL...")
    return nil
}
```

##### 6.4.5 Other Command Implementations

The implementations of `cmd/query.go`, `cmd/backup.go`, and `cmd/restore.go` follow the same pattern as `connect.go`; write the actual code as your needs require.

#### 6.5 Testing and Continuous Integration

Tests plus continuous integration are how a command-line tool stays stable: run `go test` locally, and let CI run the whole thing automatically on every commit.

##### 6.5.1 Writing Tests

Use Go's testing framework to write unit tests and integration tests, making sure each module and command behaves correctly.

Example: testing the `db` package

```go
package db

import "testing"

func TestConnectMySQL(t *testing.T) {
    err := connectMySQL("localhost", "root", "123456")
    if err != nil {
        t.Errorf("Failed to connect to MySQL: %v", err)
    }
}

func TestConnectPostgreSQL(t *testing.T) {
    err := connectPostgreSQL("localhost", "root", "123456")
    if err != nil {
        t.Errorf("Failed to connect to PostgreSQL: %v", err)
    }
}
```

##### 6.5.2 Configuring Continuous Integration

Set up a continuous integration tool (such as GitHub Actions, Travis CI, etc.) to run tests automatically and generate reports.

Example: a GitHub Actions configuration file

```yaml
name: Go CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Go
      uses: actions/setup-go@v2
      with:
        go-version: 1.16

    - name: Install dependencies
      run: go mod tidy

    - name: Run tests
      run: go test -v ./...
```

### Summary

This page is organized as follows: list the requirements first, then fix the shape of commands, help, and errors, organize the code by module, wire the commands together with cobra, and finally let tests and CI catch regressions. Later chapters discuss optimization and performance improvements for command-line tools.

## References

- [flag standard library](https://pkg.go.dev/flag)
- [os/exec standard library](https://pkg.go.dev/os/exec)

## Sibling pages

- [Flag](/cmd/Flag.md)
- [Lib](/cmd/Lib.md)
- [Parse](/cmd/Parse.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Flag](/cmd/Flag.md)
- [Lib](/cmd/Lib.md)
- [Parse](/cmd/Parse.md)
- [Readme](/cmd/Readme.md)
- [Syntax](/cmd/Syntax.md)
