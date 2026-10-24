### Database Connection Pool

#### 6.1 The Concept of Connection Pooling

A database connection pool pre-creates a set of database connections. When the application needs one, it takes one straight away, avoiding the overhead of constantly creating and destroying connections.

##### 6.1.1 Benefits of a Connection Pool
- **Improved performance**: By reusing existing connections, it cuts the cost of creating and destroying connections.
- **Controlled resource usage**: It caps the number of simultaneously open connections, preventing resource exhaustion.
- **Connection lifecycle management**: It handles connection creation, use, and destruction automatically, simplifying the code.

#### 6.2 Configuring a Connection Pool

In Go's `database/sql` package, you can tune connection pool performance by setting the pool's parameters.

##### 6.2.1 Setting the Maximum Number of Open Connections
You can use the `SetMaxOpenConns` method to set the maximum number of open connections in a database:
```go
db.SetMaxOpenConns(10)
```
This parameter limits the number of simultaneously open database connections, preventing resource exhaustion.

##### 6.2.2 Setting the Maximum Number of Idle Connections
You can use the `SetMaxIdleConns` method to set the maximum number of idle connections in a database:
```go
db.SetMaxIdleConns(5)
```
This parameter limits the number of idle connections held in the pool, avoiding wasted resources from keeping too many around.

##### 6.2.3 Setting the Maximum Connection Lifetime
You can use the `SetConnMaxLifetime` method to set the maximum lifetime of a connection:
```go
db.SetConnMaxLifetime(time.Hour)
```
This parameter sets how long a connection may live. Connections that exceed it are closed and recreated, so no connection holds onto resources for too long.

#### 6.3 Implementing a Connection Pool with `database/sql`

The `database/sql` package ships with a connection pool. Set the parameters and it works.

##### 6.3.1 Creating a Database Connection Pool
Use `sql.Open` to create the pool:
```go
import (
    "database/sql"
    "log"
    "time"
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // create a database connection pool
    db, err := sql.Open("mysql", "user:password@tcp(127.0.0.1:3306)/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // configure the connection pool
    db.SetMaxOpenConns(10)
    db.SetMaxIdleConns(5)
    db.SetConnMaxLifetime(time.Hour)

    // test the database connection
    err = db.Ping()
    if err != nil {
        log.Fatal(err)
    }

    // perform database operations
    // ...
}
```

##### 6.3.2 Performing Database Operations Through the Pool
Using the pool for database operations is no different from ordinary database operations. You can use `db.Query`, `db.Exec`, and so on directly:
```go
import (
    "database/sql"
    "log"
)

func usePool(db *sql.DB) {
    // query data
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

    // insert data
    result, err := db.Exec("INSERT INTO users (name, age) VALUES (?, ?)", "Bob", 29)
    if err != nil {
        log.Fatal(err)
    }
    lastInsertID, err := result.LastInsertId()
    if err != nil {
        log.Fatal(err)
    }
    log.Println("Last Insert ID:", lastInsertID)

    // update data
    result, err = db.Exec("UPDATE users SET age = ? WHERE name = ?", 30, "Bob")
    if err != nil {
        log.Fatal(err)
    }
    rowsAffected, err := result.RowsAffected()
    if err != nil {
        log.Fatal(err)
    }
    log.Println("Rows Affected:", rowsAffected)

    // delete data
    result, err = db.Exec("DELETE FROM users WHERE name = ?", "Bob")
    if err != nil {
        log.Fatal(err)
    }
    rowsAffected, err = result.RowsAffected()
    if err != nil {
        log.Fatal(err)
    }
    log.Println("Rows Affected:", rowsAffected)
}
```

With those three parameters set, you have both connection reuse and limits in place: `SetMaxOpenConns` caps the total open at once, `SetMaxIdleConns` keeps the warm connections around, and `SetConnMaxLifetime` stops a connection from being held indefinitely. After that, write your inserts, deletes, updates, and selects as usual, and the pool swaps connections in and out underneath.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)

## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [GraphQL](/db/GraphQL.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [GraphQL](/db/GraphQL.md)
- [Install](/db/Install.md)
- [Lib](/db/Lib.md)
- [Migrate](/db/Migrate.md)
- [Mock](/db/Mock.md)
- [Monitor](/db/Monitor.md)
- [NoSQL](/db/NoSQL.md)
- [Normalization](/db/Normalization.md)
- [ORM](/db/ORM.md)
- [Performance](/db/Performance.md)
- [Project](/db/Project.md)
- [Readme](/db/Readme.md)
- [SQL](/db/SQL.md)
- [Security](/db/Security.md)
- [Sharding](/db/Sharding.md)
- [Tx](/db/Tx.md)
