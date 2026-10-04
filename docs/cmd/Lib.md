### 4. 使用第三方库解析命令行参数

标准库 `flag` 之外，常用的命令行参数解析库有 `cobra` 和 `urfave/cli`。它们支持子命令、别名、自动生成的帮助信息等 `flag` 没有的功能。

#### 4.1 使用 `cobra` 库

`cobra` 由 `spf13` 开发，支持子命令、命令别名、自动生成帮助信息等，常用于构建有多个子命令的应用程序。

##### 4.1.1 安装 `cobra`

```shell
go get github.com/spf13/cobra
```

##### 4.1.2 基本用法

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

运行示例：

```shell
$ go run main.go
Hello, Cobra!
```

##### 4.1.3 添加选项参数

可以使用 `Flags()` 方法为命令添加选项参数：

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

运行示例：

```shell
$ go run main.go --name=Go
Hello, Go!

$ go run main.go
Hello, World!
```

##### 4.1.4 添加子命令

可以通过 `AddCommand()` 方法为应用添加子命令：

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

运行示例：

```shell
$ go run main.go greet
Hello, World!
```

##### 4.1.5 复杂示例

子命令和选项参数组合起来用：

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

运行示例：

```shell
$ go run main.go greet --name=Go
Hello, Go!

$ go run main.go greet
Hello, World!
```

#### 4.2 使用 `urfave/cli` 库

`urfave/cli` 是另一个常用选择，支持子命令、命令别名和多种选项类型。

##### 4.2.1 安装 `urfave/cli`

```shell
go get -u github.com/urfave/cli/v2
```

##### 4.2.2 基本用法

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

运行示例：

```shell
$ go run main.go
Hello, CLI!
```

##### 4.2.3 添加选项参数

可以使用 `Flags` 字段为命令添加选项参数：

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

运行示例：

```shell
$ go run main.go --name=Go
Hello, Go!

$ go run main.go
Hello, World!
```

##### 4.2.4 添加子命令

可以通过 `Commands` 字段为应用添加子命令：

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

运行示例：

```shell
$ go run main.go greet
Hello, World!
```

##### 4.2.5 复杂示例

子命令和选项参数组合起来用：

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

运行示例：

```shell
$ go run main.go greet --name=Go
Hello, Go!

$ go run main.go greet
Hello, World!
```

### 总结

`cobra` 和 `urfave/cli` 都能搭出带子命令、选项参数和自动帮助的命令行程序，两者能力相当。`urfave/cli` 用一个 `App` 结构体配齐字段，小程序写起来更省事；`cobra` 的命令树组织在子命令层级多时更清楚，按自己的场景选一个即可。