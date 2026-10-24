### Using Database/SQL Libraries

#### 5.1 The Database/SQL Package in the Go Standard Library (`database/sql`)

The `database/sql` package in Go provides a general-purpose interface for interacting with SQL databases. It does not include any database drivers itself, but it can be used together with a variety of database drivers.

##### 5.1.1 Importing the `database/sql` Package
To use the `database/sql` package you first need to import it:
```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"  // import the MySQL driver
)

var db *sql.DB // once imported, you can declare a *sql.DB connection handle
```

#### 5.2 SQL Drivers (MySQL, PostgreSQL, SQLite, etc.)

To connect to a specific database you need the corresponding driver. Here are some commonly used database drivers:

##### 5.2.1 MySQL Driver
The MySQL driver can be imported via `github.com/go-sql-driver/mysql`.
```go
import _ "github.com/go-sql-driver/mysql"
```

##### 5.2.2 PostgreSQL Driver
The PostgreSQL driver can be imported via `github.com/lib/pq`.
```go
import _ "github.com/lib/pq"
```

##### 5.2.3 SQLite Driver
The SQLite driver can be imported via `github.com/mattn/go-sqlite3`.
```go
import _ "github.com/mattn/go-sqlite3"
```

#### 5.3 Opening and Closing Database Connections

You need to open a connection before working with the database, and close it afterwards:

##### 5.3.1 Establishing a Connection
Use the `sql.Open` function to establish a database connection. The driver has to be registered with a blank import, otherwise you get `unknown driver "mysql"` at runtime; `sql.Open` only validates the DSN format and does not actually connect, so a placeholder DSN still constructs successfully:
```go
package main

import (
    "database/sql"
    "log"

    _ "github.com/go-sql-driver/mysql" // register the mysql driver; must be a blank import
)

func main() {
    db, err := sql.Open("mysql", "user:password@/dbname")
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()
}
```

`user:password@/dbname` is a placeholder. Replace it with real credentials and a database name, and the `db.Ping` step that follows will pass.

##### 5.3.2 Testing the Connection
You can use the `db.Ping` method to test whether the connection succeeded:
```go
err = db.Ping()
if err != nil {
    log.Fatal(err)
}
```

#### 5.4 Executing Basic SQL Operations (Query, Insert, Update, Delete)

Through the `database/sql` package you can perform the basic SQL operations: query, insert, update and delete. The snippets below reuse the `db` connection established in 5.3.1.

##### 5.4.1 Querying Data
Use the `db.Query` method to run a query:
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

##### 5.4.2 Inserting Data
Use the `db.Exec` method to insert data:
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

##### 5.4.3 Updating Data
Use the `db.Exec` method to update data:
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

##### 5.4.4 Deleting Data
Use the `db.Exec` method to delete data:
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

#### 5.5 Handling SQL Errors

Every operation in `database/sql` returns an `error`. Miss one and you may well get an empty result without ever realizing it.

##### 5.5.1 An Error-Handling Example
After each database operation, check for and handle any possible error:
```go
_, err := db.Exec("INVALID SQL STATEMENT")
if err != nil {
    log.Printf("Error executing statement: %v", err)
}
```

##### 5.5.2 Common SQL Errors
- **sql.ErrNoRows**: means the query returned no results.
- **sql.ErrConnDone**: means the database connection has already been closed.

To handle these errors you can use the `errors.Is` method:
```go
if errors.Is(err, sql.ErrNoRows) {
    log.Println("No rows were found")
} else {
    log.Printf("Error executing query: %v", err)
}
```

`database/sql` only supplies the interface; you install a separate driver for each database. Queries and writes go through `Query`/`Exec`, and errors are matched with `errors.Is` against sentinel values like `sql.ErrNoRows`. When you swap databases, the business code usually only needs the DSN and the driver import line changed.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Install](/db/Install.md)
- [Migrate](/db/Migrate.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Install](/db/Install.md)
- [Migrate](/db/Migrate.md)
