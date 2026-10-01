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

在与数据库交互之前，首先需要建立数据库连接，并在操作完成后关闭连接。

##### 5.3.1 建立连接
使用 `sql.Open` 函数建立数据库连接：
```go
db, err := sql.Open("mysql", "user:password@/dbname")
if err != nil {
    log.Fatal(err)
}
defer db.Close()
```

##### 5.3.2 测试连接
可以使用 `db.Ping` 方法测试连接是否成功：
```go
err = db.Ping()
if err != nil {
    log.Fatal(err)
}
```

#### 5.4 执行基本的SQL操作（查询、插入、更新、删除）

通过 `database/sql` 包，可以执行基本的 SQL 操作，如查询、插入、更新和删除。

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

在处理数据库操作时，正确处理错误是非常重要的。

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

通过学习和掌握这些数据库操作和错误处理方法，读者可以在 Go 语言中高效地与各种数据库进行交互。