### 使用数据库/SQL库

#### 5.1 Go标准库中的数据库/SQL包（`database/sql`）

Go 语言的 `database/sql` 包提供了与 SQL 数据库交互的通用接口。它不包含任何数据库驱动程序，但可以与各种数据库驱动程序一起使用。

##### 5.1.1 导入 `database/sql` 包
要使用 `database/sql` 包，需要首先导入它：
```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"  // 导入 MySQL 驱动程序
)

var db *sql.DB // 导入后即可声明 *sql.DB 连接句柄
```

#### 5.2 SQL驱动程序（MySQL、PostgreSQL、SQLite等）

为了连接特定的数据库，您需要相应的驱动程序。以下是一些常用的数据库驱动程序：

##### 5.2.1 MySQL 驱动程序
MySQL 驱动程序可以通过 `github.com/go-sql-driver/mysql` 导入。
```go
import _ "github.com/go-sql-driver/mysql"
```

##### 5.2.2 PostgreSQL 驱动程序
PostgreSQL 驱动程序可以通过 `github.com/lib/pq` 导入。
```go
import _ "github.com/lib/pq"
```

##### 5.2.3 SQLite 驱动程序
SQLite 驱动程序可以通过 `github.com/mattn/go-sqlite3` 导入。
```go
import _ "github.com/mattn/go-sqlite3"
```

#### 5.3 数据库连接与关闭

和数据库交互前要先建立连接，操作完再关闭：

##### 5.3.1 建立连接
使用 `sql.Open` 函数建立数据库连接。驱动要用空白导入注册，否则运行时报 `unknown driver "mysql"`；`sql.Open` 只校验 DSN 格式，不真正连接，所以占位 DSN 也能构造成功：
```go
package main

import (
    "database/sql"
    "log"

    _ "github.com/go-sql-driver/mysql" // 注册 mysql 驱动，必须空白导入
)

func main() {
    db, err := sql.Open("mysql", "user:password@/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
}
```

`user:password@/dbname` 是占位写法，换成真实的账号、密码和库名之后，下一步的 `db.Ping` 才能通过。

##### 5.3.2 测试连接
可以使用 `db.Ping` 方法测试连接是否成功：
```go
err = db.Ping()
if err != nil {
    log.Fatal(err)
}
```

#### 5.4 执行基本的SQL操作（查询、插入、更新、删除）

通过 `database/sql` 包，可以执行基本的 SQL 操作，如查询、插入、更新和删除。以下片段沿用 5.3.1 建立的 `db` 连接。

##### 5.4.1 查询数据
使用 `db.Query` 方法执行查询操作：
```go
rows, err := db.Query("SELECT id, name FROM users WHERE age > ?", 30)
if err != nil {
    log.Fatal(err)
}
defer rows.Close()

for rows.Next() {
    var id int
    var name string
    err = rows.Scan(&id, &name)
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(id, name)
}

err = rows.Err()
if err != nil {
    log.Fatal(err)
}
```

##### 5.4.2 插入数据
使用 `db.Exec` 方法插入数据：
```go
result, err := db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Alice", 25)
if err != nil {
    log.Fatal(err)
}

lastInsertID, err := result.LastInsertId()
if err != nil {
    log.Fatal(err)
}
fmt.Println("Last Insert ID:", lastInsertID)
```

##### 5.4.3 更新数据
使用 `db.Exec` 方法更新数据：
```go
result, err := db.Exec("UPDATE users SET age = ? WHERE name = ?", 26, "Alice")
if err != nil {
    log.Fatal(err)
}

rowsAffected, err := result.RowsAffected()
if err != nil {
    log.Fatal(err)
}
fmt.Println("Rows Affected:", rowsAffected)
```

##### 5.4.4 删除数据
使用 `db.Exec` 方法删除数据：
```go
result, err := db.Exec("DELETE FROM users WHERE name = ?", "Alice")
if err != nil {
    log.Fatal(err)
}

rowsAffected, err := result.RowsAffected()
if err != nil {
    log.Fatal(err)
}
fmt.Println("Rows Affected:", rowsAffected)
```

#### 5.5 处理SQL错误

`database/sql` 的每个操作都返回 `error`，漏掉一个查询就可能拿到空结果还不自知。

##### 5.5.1 错误处理示例
每个数据库操作后，检查并处理可能的错误：
```go
_, err := db.Exec("INVALID SQL STATEMENT")
if err != nil {
    log.Printf("Error executing statement: %v", err)
}
```

##### 5.5.2 常见的SQL错误
- **sql.ErrNoRows**：表示查询没有返回任何结果。
- **sql.ErrConnDone**：表示数据库连接已经关闭。

处理这些错误可以使用 `errors.Is` 方法：
```go
if errors.Is(err, sql.ErrNoRows) {
    log.Println("No rows were found")
} else {
    log.Printf("Error executing query: %v", err)
}
```

`database/sql` 只提供接口，驱动按数据库各装各的；查询、写入走 `Query`/`Exec`，错误用 `errors.Is` 对着 `sql.ErrNoRows` 这类哨兵值判断。换数据库时，业务代码通常只需要改 DSN 和驱动导入那一行。