### 实践项目

#### 15.1 构建一个简单的Go数据库应用

本节将带领读者构建一个简单的Go数据库应用，从安装依赖到运行完整的应用。

##### 安装依赖
首先，安装所需的Go依赖库，包括数据库驱动和Web框架（如Gin）。
```bash
go get -u github.com/gin-gonic/gin
go get -u github.com/go-sql-driver/mysql
```

##### 创建项目结构
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

#### 15.2 实现一个CRUD操作示例

##### 模型层（model/model.go）
定义数据库模型和操作。
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

##### 数据库连接层（db/db.go）
管理数据库连接。
```go
package db

import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"
    "log"
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

##### 处理器层（handler/handler.go）
实现HTTP处理器函数。
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

##### 主程序（main.go）
配置路由和启动服务器。
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

#### 15.3 数据库与Web框架集成（Gin、Echo等）

除了Gin，还可以使用Echo等Web框架进行数据库操作。

##### 使用Echo框架
安装Echo框架：
```bash
go get -u github.com/labstack/echo/v4
```

替换`main.go`中的Gin代码为Echo代码：
```go
package main

import (
    "your_project/db"
    "your_project/handler"
    "github.com/labstack/echo/v4"
    "log"
)

func main() {
    database, err := db.InitDB("user:password@tcp(127.0.0.1:3306)/your_database_name")
    if err != nil {
        log.Fatal(err)
    }

    e := echo.New()
    e.GET("/users", func(c echo.Context) error {
        return handler.GetUsers(c, database)
    })
    e.POST("/users", func(c echo.Context) error {
        return handler.CreateUser(c, database)
    })
    e.PUT("/users/:id", func(c echo.Context) error {
        return handler.UpdateUser(c, database)
    })
    e.DELETE("/users/:id", func(c echo.Context) error {
        return handler.DeleteUser(c, database)
    })

    e.Start(":8080")
}
```

#### 15.4 完整的项目示例

最后，本节将通过一个完整的项目示例，整合前述内容，展示如何构建一个包含数据库操作的完整Go应用。

##### 项目结构
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

通过本章内容，读者将全面掌握如何在Go语言中进行数据库操作，并将其应用到实际项目中，实现一个完整的数据库驱动的Web应用。