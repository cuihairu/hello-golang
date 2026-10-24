### Hands-on project

#### 15.1 Building a simple Go database application

This section goes from installing the dependencies all the way to running a Go database app that can do create, read, update, and delete.

##### Installing dependencies
First, install the Go dependencies you need, including the database driver and a web framework (such as Gin).
```bash
go get -u github.com/gin-gonic/gin
go get -u github.com/go-sql-driver/mysql
```

##### Creating the project structure
```plaintext
go-database-app/
├── main.go
├── handler/
│   └── handler.go
├── model/
│   └── model.go
└── db/
    └── db.go
```

#### 15.2 Implementing a CRUD example

##### Model layer (model/model.go)
Define the database models and their operations.
```go
package model

import (
    "database/sql"
)

type User struct {
    ID    int    `json:"id"`
    Name  string `json:"name"`
    Email string `json:"email"`
}

func GetUsers(db *sql.DB) ([]User, error) {
    rows, err := db.Query("SELECT id, name, email FROM users")
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    users := []User{}
    for rows.Next() {
        var user User
        if err := rows.Scan(&user.ID, &user.Name, &user.Email); err != nil {
            return nil, err
        }
        users = append(users, user)
    }
    return users, nil
}

func CreateUser(db *sql.DB, user User) error {
    _, err := db.Exec("INSERT INTO users (name, email) VALUES (?, ?)", user.Name, user.Email)
    return err
}

func UpdateUser(db *sql.DB, user User) error {
    _, err := db.Exec("UPDATE users SET name=?, email=? WHERE id=?", user.Name, user.Email, user.ID)
    return err
}

func DeleteUser(db *sql.DB, id int) error {
    _, err := db.Exec("DELETE FROM users WHERE id=?", id)
    return err
}
```

##### Database connection layer (db/db.go)
Manage the database connection.
```go
package db

import (
    "database/sql"

    _ "github.com/go-sql-driver/mysql"
)

func InitDB(dataSourceName string) (*sql.DB, error) {
    db, err := sql.Open("mysql", dataSourceName)
    if err != nil {
        return nil, err
    }

    if err := db.Ping(); err != nil {
        return nil, err
    }

    return db, nil
}
```

##### Handler layer (handler/handler.go)
Implement the HTTP handler functions.
```go
package handler

import (
    "database/sql"
    "github.com/gin-gonic/gin"
    "net/http"
    "strconv"
    "your_project/model"
)

func GetUsers(c *gin.Context, db *sql.DB) {
    users, err := model.GetUsers(db)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusOK, users)
}

func CreateUser(c *gin.Context, db *sql.DB) {
    var user model.User
    if err := c.BindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    if err := model.CreateUser(db, user); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusCreated, user)
}

func UpdateUser(c *gin.Context, db *sql.DB) {
    var user model.User
    if err := c.BindJSON(&user); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    id, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
        return
    }
    user.ID = id

    if err := model.UpdateUser(db, user); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, user)
}

func DeleteUser(c *gin.Context, db *sql.DB) {
    id, err := strconv.Atoi(c.Param("id"))
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
        return
    }

    if err := model.DeleteUser(db, id); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
        return
    }

    c.JSON(http.StatusOK, gin.H{"message": "User deleted"})
}
```

##### Main program (main.go)
Set up the routes and start the server.
```go
package main

import (
    "your_project/db"
    "your_project/handler"
    "github.com/gin-gonic/gin"
    "log"
)

func main() {
    database, err := db.InitDB("user:password@tcp(127.0.0.1:3306)/your_database_name")
    if err != nil {
        log.Fatal(err)
    }

    router := gin.Default()
    router.GET("/users", func(c *gin.Context) {
        handler.GetUsers(c, database)
    })
    router.POST("/users", func(c *gin.Context) {
        handler.CreateUser(c, database)
    })
    router.PUT("/users/:id", func(c *gin.Context) {
        handler.UpdateUser(c, database)
    })
    router.DELETE("/users/:id", func(c *gin.Context) {
        handler.DeleteUser(c, database)
    })

    router.Run(":8080")
}
```

#### 15.3 Integrating a database with web frameworks (Gin, Echo, and others)

Besides Gin, you can also use web frameworks such as Echo to work with a database.

##### Using the Echo framework
Install the Echo framework:
```bash
go get -u github.com/labstack/echo/v4
```

Replace the Gin code in `main.go` with Echo code. Note: Echo handlers take an `echo.Context` and return an `error`, which is not compatible with the `handler` signatures in the Gin version above, so here we implement the handlers directly against the `model` layer:
```go
package main

import (
    "log"
    "net/http"
    "strconv"

    "github.com/labstack/echo/v4"

    "your_project/db"
    "your_project/model"
)

func main() {
    database, err := db.InitDB("user:password@tcp(127.0.0.1:3306)/your_database_name")
    if err != nil {
        log.Fatal(err)
    }

    e := echo.New()

    e.GET("/users", func(c echo.Context) error {
        users, err := model.GetUsers(database)
        if err != nil {
            return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
        }
        return c.JSON(http.StatusOK, users)
    })

    e.POST("/users", func(c echo.Context) error {
        var user model.User
        if err := c.Bind(&user); err != nil {
            return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
        }
        if err := model.CreateUser(database, user); err != nil {
            return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
        }
        return c.JSON(http.StatusCreated, user)
    })

    e.PUT("/users/:id", func(c echo.Context) error {
        id, err := strconv.Atoi(c.Param("id"))
        if err != nil {
            return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid ID"})
        }
        var user model.User
        if err := c.Bind(&user); err != nil {
            return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
        }
        user.ID = id
        if err := model.UpdateUser(database, user); err != nil {
            return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
        }
        return c.JSON(http.StatusOK, user)
    })

    e.DELETE("/users/:id", func(c echo.Context) error {
        id, err := strconv.Atoi(c.Param("id"))
        if err != nil {
            return c.JSON(http.StatusBadRequest, map[string]string{"error": "Invalid ID"})
        }
        if err := model.DeleteUser(database, id); err != nil {
            return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
        }
        return c.JSON(http.StatusOK, map[string]string{"message": "User deleted"})
    })

    log.Fatal(e.Start(":8080"))
}
```

#### 15.4 A complete project example

The complete project pulls the layers above together: connection, model, handlers, and routing.

##### Project structure
```plaintext
go-web-app/
├── main.go
├── handler/
│   └── handler.go
├── model/
│   └── model.go
├── db/
│   └── db.go
├── config/
│   └── config.go
└── README.md
```

Each of the four packages owns one piece: `db` opens the connection, `model` writes the SQL, `handler` sends and receives HTTP, and `main` wires up the routes. All CRUD reads and writes live in `model`; when switching to Echo you change the routes and handlers in `main`, and not a single line of `model` moves.

## References

- [Official · Database Access Guide](https://go.dev/doc/database/)
- [Go Official Documentation · Accessing a relational database (external link)](https://go.dev/doc/tutorial/database-access)
- [database/sql standard library](https://pkg.go.dev/database/sql)


## Sibling pages

- [Availability](/db/Availability.md)
- [Base](/db/Base.md)
- [ConnectPool](/db/ConnectPool.md)
- [Performance](/db/Performance.md)
- [Readme](/db/Readme.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Performance](/db/Performance.md)
- [Readme](/db/Readme.md)
