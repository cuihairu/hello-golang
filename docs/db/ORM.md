###  ORM Frameworks

#### 7.1 What Is ORM

Object-Relational Mapping (ORM) maps database tables to objects, so you work with a database through an object-oriented approach without writing complex SQL by hand. The framework handles the conversion between objects and relational tables automatically.

#### 7.2 Popular Go ORM Frameworks

Among Go ORM frameworks, the three most common are these:

##### 7.2.1 GORM
GORM supports multiple databases, including MySQL, PostgreSQL, and SQLite. The examples here use GORM.

##### 7.2.2 Ent
Ent is a Graph-based ORM framework that provides rich query builders and code generation tools, well suited to building complex data models.

##### 7.2.3 XORM
XORM is also a Go ORM that supports multiple databases and provides the usual database operations: insert, delete, update, and query.

#### 7.3 Database Operations with GORM

##### 7.3.1 Installing GORM
Install GORM with the `go get` command:
```bash
go get -u gorm.io/gorm
go get -u gorm.io/driver/mysql
```

##### 7.3.2 Initializing the Database Connection
```go
import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "log"
)

func main() {
    dsn := "user:password@tcp(127.0.0.1:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
    // SkipInitializeWithVersion skips the SELECT VERSION() at connection setup; DisableAutomaticPing defers the connection until first use
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

##### 7.3.3 Defining a Model
```go
type User struct {
    ID    uint   `gorm:"primaryKey"`
    Name  string
    Age   int
    Email string
}
```

##### 7.3.4 CRUD Operations
```go
// create
user := User{Name: "Alice", Age: 25, Email: "alice@example.com"}
db.Create(&user)

// read
var user User
db.First(&user, 1) // query by primary key
db.First(&user, "email = ?", "alice@example.com") // query by condition

// update
db.Model(&user).Update("Age", 26)
db.Model(&user).Updates(User{Age: 26, Email: "alice_new@example.com"})

// delete
db.Delete(&user, 1)
```

#### 7.4 Database Operations with Ent

##### 7.4.1 Installing Ent
Install Ent with the `go get` command:
```bash
go get -u entgo.io/ent/cmd/ent
```

##### 7.4.2 Defining a Model
Use Ent's code generation tool to define the model:
```bash
ent init User
```

Define the User model in the `ent/schema/user.go` file:
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

##### 7.4.3 Generating Code
```bash
go generate ./ent
```

##### 7.4.4 Initializing the Database Connection
```go
import (
    "context"
    "log"

    "entproject/ent"

    _ "github.com/go-sql-driver/mysql" // register the MySQL driver
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

##### 7.4.5 CRUD Operations
```go
// create
user, err := client.User.Create().
    SetName("Alice").
    SetAge(25).
    SetEmail("alice@example.com").
    Save(ctx)
if err != nil {
    log.Fatal(err)
}

// read
user, err := client.User.Get(ctx, 1)
if err != nil {
    log.Fatal(err)
}

// update
user, err = user.Update().
    SetAge(26).
    SetEmail("alice_new@example.com").
    Save(ctx)
if err != nil {
    log.Fatal(err)
}

// delete
err = client.User.DeleteOneID(1).Exec(ctx)
if err != nil {
    log.Fatal(err)
}
```

#### 7.5 Database Operations with XORM

##### 7.5.1 Installing XORM
Install XORM with the `go get` command:
```bash
go get -u xorm.io/xorm
```

##### 7.5.2 Initializing the Database Connection
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

##### 7.5.3 Defining a Model
```go
type User struct {
    ID    int64  `xorm:"pk autoincr"`
    Name  string `xorm:"varchar(255)"`
    Age   int
    Email string `xorm:"varchar(255)"`
}
```

##### 7.5.4 CRUD Operations
```go
// create
user := User{Name: "Alice", Age: 25, Email: "alice@example.com"}
_, err := engine.Insert(&user)
if err != nil {
    log.Fatal(err)
}

// read
var got User
has, err := engine.ID(1).Get(&got)
if err != nil {
    log.Fatal(err)
}
if has {
    log.Println(got)
}

// update
got.Age = 26
_, err = engine.ID(got.ID).Update(&got)
if err != nil {
    log.Fatal(err)
}

// delete
_, err = engine.ID(got.ID).Delete(&User{})
if err != nil {
    log.Fatal(err)
}
```

The three frameworks split the work differently: GORM writes inserts, deletes, updates, and queries with chained methods; Ent defines a schema first and then generates query code; XORM describes the mapping through struct tags.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)
- [GORM Official Documentation](https://gorm.io/docs/)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Normalization](/db/Normalization.md)
- [Performance](/db/Performance.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Normalization](/db/Normalization.md)
- [Performance](/db/Performance.md)
