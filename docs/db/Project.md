### 实践项目

#### 15.1 构建一个简单的Go数据库应用

这一节从装依赖开始，到跑起一个能增删改查的 Go 数据库应用为止。

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

替换`main.go`中的Gin代码为Echo代码。注意：Echo 的处理器接收 `echo.Context` 并返回 `error`，与上面 Gin 版的 `handler` 签名不兼容，因此这里直接使用 `model` 层实现处理器：
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

#### 15.4 完整的项目示例

完整的项目把前面几层合到一起：连接、模型、处理器、路由。

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

四个包各管一段：`db` 建连接，`model` 写 SQL，`handler` 收发 HTTP，`main` 挂路由。CRUD 读写全在 `model`，换成 Echo 时改的是 `main` 里的路由和处理器，`model` 一行不动。