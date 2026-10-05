###  ORM框架

#### 7.1 什么是ORM

对象关系映射（Object-Relational Mapping，ORM）把数据库表映射成对象，用面向对象的方式操作数据库，不用手写复杂的 SQL。框架自动处理对象和关系表之间的转换。

#### 7.2 流行的Go ORM框架

Go 语言的 ORM 框架里，常用的是下面三个：

##### 7.2.1 GORM
GORM 支持多种数据库，包括 MySQL、PostgreSQL、SQLite 等，本节的示例就用它。

##### 7.2.2 Ent
Ent 是一个基于 Graph 的 ORM 框架，提供了丰富的查询生成器和代码生成工具，适合构建复杂的数据模型。

##### 7.2.3 XORM
XORM 也是支持多种数据库的 Go ORM，提供增删改查等数据库操作。

#### 7.3 使用GORM进行数据库操作

##### 7.3.1 安装GORM
使用 `go get` 命令安装 GORM：
```bash
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

##### 7.3.2 初始化数据库连接
```go
import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "log"
)

func main() {
    dsn := "user:password@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
    // SkipInitializeWithVersion 跳过建连时的 SELECT VERSION()，DisableAutomaticPing 让连接推迟到首次使用
    db, err := gorm.Open(mysql.New(mysql.Config{
        DSN:                       dsn,
        SkipInitializeWithVersion: true,
    }), &gorm.Config{DisableAutomaticPing: true})
    if err != nil {
        log.Fatal(err)
    }
    _ = db
}
```

##### 7.3.3 定义模型
```go
type User struct {
    ID    uint   `gorm:"primaryKey"`
    Name  string
    Age   int
    Email string
}
```

##### 7.3.4 CRUD 操作
```go
// 创建
user := User{Name: "Alice", Age: 25, Email: "alice@example.com"}
db.Create(&user)

// 读取
var user User
db.First(&user, 1) // 根据主键查询
db.First(&user, "email = ?", "alice@example.com") // 根据条件查询

// 更新
db.Model(&user).Update("Age", 26)
db.Model(&user).Updates(User{Age: 26, Email: "alice_new@example.com"})

// 删除
db.Delete(&user, 1)
```

#### 7.4 使用Ent进行数据库操作

##### 7.4.1 安装Ent
使用 `go get` 命令安装 Ent：
```bash
go get -u entgo.io/ent/cmd/ent
```

##### 7.4.2 定义模型
使用 Ent 的代码生成工具定义模型：
```bash
ent init User
```

在 `ent/schema/user.go` 文件中定义 User 模型：
```go
package schema

import (
    "entgo.io/ent"
    "entgo.io/ent/schema/field"
)

// User holds the schema definition for the User entity.
type User struct {
    ent.Schema
}

// Fields of the User.
func (User) Fields() []ent.Field {
    return []ent.Field{
        field.String("name"),
        field.Int("age"),
        field.String("email"),
    }
}
```

##### 7.4.3 生成代码
```bash
go generate ./ent
```

##### 7.4.4 初始化数据库连接
```go
import (
    "context"
    "log"

    "entproject/ent"

    _ "github.com/go-sql-driver/mysql" // 注册 MySQL 驱动
)

func main() {
    client, err := ent.Open("mysql", "user:password@tcp(127.0.0.1:3306)/dbname?parseTime=true")
    if err != nil {
        log.Fatal(err)
    }
    defer client.Close()
    ctx := context.Background()
    if err := client.Schema.Create(ctx); err != nil {
        log.Fatal(err)
    }
}
```

##### 7.4.5 CRUD 操作
```go
// 创建
user, err := client.User.Create().
    SetName("Alice").
    SetAge(25).
    SetEmail("alice@example.com").
    Save(ctx)
if err != nil {
    log.Fatal(err)
}

// 读取
user, err := client.User.Get(ctx, 1)
if err != nil {
    log.Fatal(err)
}

// 更新
user, err = user.Update().
    SetAge(26).
    SetEmail("alice_new@example.com").
    Save(ctx)
if err != nil {
    log.Fatal(err)
}

// 删除
err = client.User.DeleteOneID(1).Exec(ctx)
if err != nil {
    log.Fatal(err)
}
```

#### 7.5 使用XORM进行数据库操作

##### 7.5.1 安装XORM
使用 `go get` 命令安装 XORM：
```bash
go get -u xorm.io/xorm
```

##### 7.5.2 初始化数据库连接
```go
import (
    "xorm.io/xorm"
    _ "github.com/go-sql-driver/mysql"
    "log"
)

func main() {
    engine, err := xorm.NewEngine("mysql", "user:password@tcp(127.0.0.1:3306)/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer engine.Close()
}
```

##### 7.5.3 定义模型
```go
type User struct {
    ID    int64  `xorm:"pk autoincr"`
    Name  string `xorm:"varchar(255)"`
    Age   int
    Email string `xorm:"varchar(255)"`
}
```

##### 7.5.4 CRUD 操作
```go
// 创建
user := User{Name: "Alice", Age: 25, Email: "alice@example.com"}
_, err := engine.Insert(&user)
if err != nil {
    log.Fatal(err)
}

// 读取
var got User
has, err := engine.ID(1).Get(&got)
if err != nil {
    log.Fatal(err)
}
if has {
    log.Println(got)
}

// 更新
got.Age = 26
_, err = engine.ID(got.ID).Update(&got)
if err != nil {
    log.Fatal(err)
}

// 删除
_, err = engine.ID(got.ID).Delete(&User{})
if err != nil {
    log.Fatal(err)
}
```

三个框架的分工不同：GORM 用链式方法写增删改查，Ent 先定义 schema 再生成查询代码，XORM 靠 struct 标签描述映射。