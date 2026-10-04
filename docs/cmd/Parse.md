### 5. 高级命令行参数解析

本章讲四个话题：多层次子命令、动态生成命令、自动完成，以及环境变量、错误处理、国际化、测试几项实践。

#### 5.1 处理复杂的子命令结构

在实际应用中，命令行工具往往需要支持多层次的子命令。我们以 `cobra` 和 `urfave/cli` 为例，展示如何处理复杂的子命令结构。

##### 5.1.1 使用 `cobra` 处理复杂子命令

以下示例展示了如何使用 `cobra` 处理多层次子命令：

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

运行示例：

```shell
$ go run main.go user add
User added

$ go run main.go user delete
User deleted
```

##### 5.1.2 使用 `urfave/cli` 处理复杂子命令

以下示例展示了如何使用 `urfave/cli` 处理多层次子命令：

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

运行示例：

```shell
$ go run main.go user add
User added

$ go run main.go user delete
User deleted
```

#### 5.2 动态生成命令

在某些情况下，命令行工具需要根据动态数据生成命令。例如，从配置文件或数据库中读取可用的命令列表。我们以 `cobra` 为例，展示如何动态生成命令。

##### 5.2.1 动态生成 `cobra` 命令

以下示例展示了如何根据动态数据生成 `cobra` 命令：

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

运行示例：

```shell
$ go run main.go start
start command executed

$ go run main.go stop
stop command executed
```

#### 5.3 实现自动完成

`cobra` 自带自动完成支持，做法如下：

##### 5.3.1 为 `cobra` 添加自动完成

首先，安装 `bash-completion`：

```shell
brew install bash-completion
```

然后，在 `cobra` 项目中添加自动完成支持：

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

运行示例：

```shell
$ go run main.go completion
Bash completion script generated: app_completion.sh

$ source ./app_completion.sh
$ app [TAB]
completion  start        stop         restart
```

#### 5.4 高级特性和最佳实践

下面四项是常见实践，各给一个方向，不展开代码：

##### 5.4.1 支持环境变量

命令行工具的行为可以用环境变量配置，不必写进配置文件。`cobra` 和 `urfave/cli` 都支持读取环境变量。

##### 5.4.2 统一的错误处理

错误信息和日志走同一套处理，别让每个子命令各写各的。

##### 5.4.3 国际化和本地化

提示信息按用户语言切换。`cobra` 提供了一些基本的国际化支持。

##### 5.4.4 测试和持续集成

给命令行工具写测试，用 GitHub Actions、Travis CI 这类工具自动跑。

### 总结

本章写了多层次子命令、动态生成命令、自动完成三个功能，外加环境变量、错误处理、国际化、测试四项实践。前三个有完整代码，后四项只给了方向。