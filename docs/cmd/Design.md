### 6. 命令行工具的设计与实现

命令行工具除了代码本身，还要考虑设计、用户体验、扩展性和维护性。本章从需求分析走到具体实现，按顺序过一遍。

#### 6.1 需求分析

设计之前先明确工具的目标和需求：

- **用户目标**：了解工具的主要用户群体是谁，他们的需求是什么。
- **功能需求**：明确工具需要实现的功能列表。
- **非功能需求**：包括性能要求、可扩展性、可维护性、安全性等。

示例：假设我们要设计一个数据库管理命令行工具，其需求可能包括：

- 支持连接到不同类型的数据库（MySQL、PostgreSQL 等）。
- 提供数据库查询、备份、恢复等功能。
- 提供友好的帮助和文档。

#### 6.2 用户体验设计

命令行工具的用户体验设计主要涉及以下几个方面：

- **命令和参数的设计**：命令名和参数名要短、能猜，符合用户习惯。
- **帮助信息**：每个命令列出参数含义和示例，新用户照着就能跑。
- **错误处理**：报错时说清哪一步失败、怎么改。

示例：数据库管理工具的命令设计

```shell
dbtool connect --type=mysql --host=localhost --user=root --password=123456
dbtool query --sql="SELECT * FROM users"
dbtool backup --output=/path/to/backup
dbtool restore --input=/path/to/backup
```

#### 6.3 架构设计

命令行工具的架构设计应考虑到可扩展性和可维护性，常见的架构模式包括模块化设计、插件式设计等。

- **模块化设计**：将不同的功能模块化，便于维护和扩展。
- **插件式设计**：通过插件机制支持功能扩展，适用于大型工具。

示例：模块化设计

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

#### 6.4 实现示例

以下示例展示了如何使用 `cobra` 库实现一个简单的数据库管理命令行工具。

##### 6.4.1 项目结构

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

##### 6.4.2 根命令实现

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

##### 6.4.3 连接命令实现

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

##### 6.4.4 数据库连接实现

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
    // 实现 MySQL 连接逻辑
    fmt.Println("Connecting to MySQL...")
    return nil
}

func connectPostgreSQL(host, user, password string) error {
    // 实现 PostgreSQL 连接逻辑
    fmt.Println("Connecting to PostgreSQL...")
    return nil
}
```

##### 6.4.5 其他命令实现

`cmd/query.go`、`cmd/backup.go` 和 `cmd/restore.go` 的实现类似于 `connect.go`，具体代码可根据需求自行编写。

#### 6.5 测试和持续集成

测试加持续集成是命令行工具保持稳定的做法：本地跑 `go test`，CI 在每次提交时自动跑一遍。

##### 6.5.1 编写测试

使用 Go 的测试框架编写单元测试和集成测试，确保各个模块和命令的正确性。

示例：测试 `db` 包

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

##### 6.5.2 配置持续集成

配置持续集成工具（如 GitHub Actions、Travis CI 等），自动运行测试并生成报告。

示例：GitHub Actions 配置文件

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

### 总结

这一章的顺序是：先列需求，再定命令、帮助和报错的形态，按模块组织代码，用 cobra 把命令接起来，最后交给测试和 CI 兜住回归。后续章节讨论命令行工具的优化和性能提升。