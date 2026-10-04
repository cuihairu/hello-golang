### 数据库连接池

#### 6.1 连接池的概念

数据库连接池预先建好一组数据库连接，应用程序要用时直接取用，省掉频繁创建和销毁连接的开销。

##### 6.1.1 连接池的优点
- **提高性能**：通过重用现有连接，减少连接创建和销毁的开销。
- **控制资源使用**：限制同时打开的连接数量，防止资源耗尽。
- **管理连接生命周期**：自动管理连接的创建、使用和销毁，简化代码逻辑。

#### 6.2 配置连接池

在 Go 的 `database/sql` 包中，可以通过配置数据库连接池的参数来优化连接池的性能。

##### 6.2.1 设置最大打开连接数
可以使用 `SetMaxOpenConns` 方法设置数据库的最大打开连接数：
```go
db.SetMaxOpenConns(10)
```
此参数限制了同时打开的数据库连接数，防止资源耗尽。

##### 6.2.2 设置最大空闲连接数
可以使用 `SetMaxIdleConns` 方法设置数据库的最大空闲连接数：
```go
db.SetMaxIdleConns(5)
```
此参数限制了连接池中空闲连接的数量，避免连接过多导致资源浪费。

##### 6.2.3 设置连接的最大生存时间
可以使用 `SetConnMaxLifetime` 方法设置连接的最大生存时间：
```go
db.SetConnMaxLifetime(time.Hour)
```
此参数设置了连接的最大生存时间，超过此时间的连接将被关闭并重新创建，防止连接长期占用资源。

#### 6.3 使用`database/sql`实现连接池

`database/sql` 包本身就带连接池，配上参数就能用。

##### 6.3.1 创建数据库连接池
用 `sql.Open` 创建连接池：
```go
import (
    "database/sql"
    "log"
    "time"
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // 创建数据库连接池
    db, err := sql.Open("mysql", "user:password@tcp(127.0.0.1:3306)/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // 配置连接池
    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(time.Hour)

    // 测试数据库连接
    err = db.Ping()
    if err != nil {
        log.Fatal(err)
    }

    // 执行数据库操作
    // ...
}
```

##### 6.3.2 使用连接池执行数据库操作
使用连接池执行数据库操作与普通的数据库操作没有区别，可以直接使用 `db.Query`、`db.Exec` 等方法：
```go
// 查询数据
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
    log.Println(id, name)
}

// 插入数据
result, err := db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Bob", 29)
if err != nil {
    log.Fatal(err)
}
lastInsertID, err := result.LastInsertId()
if err != nil {
    log.Fatal(err)
}
log.Println("Last Insert ID:", lastInsertID)

// 更新数据
result, err = db.Exec("UPDATE users SET age = ? WHERE name = ?", 30, "Bob")
if err != nil {
    log.Fatal(err)
}
rowsAffected, err := result.RowsAffected()
if err != nil {
    log.Fatal(err)
}
log.Println("Rows Affected:", rowsAffected)

// 删除数据
result, err = db.Exec("DELETE FROM users WHERE name = ?", "Bob")
if err != nil {
    log.Fatal(err)
}
rowsAffected, err = result.RowsAffected()
if err != nil {
    log.Fatal(err)
}
log.Println("Rows Affected:", rowsAffected)
```

三个参数配好，连接的复用和上限就都有了：`SetMaxOpenConns` 卡住同时打开的总量，`SetMaxIdleConns` 留住热连接，`SetConnMaxLifetime` 防止连接被长期占用。之后的增删改查照常写，连接池在下面自动换进换出。