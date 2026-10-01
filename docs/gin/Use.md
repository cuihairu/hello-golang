### Gin 的基本使用

#### 1 路由与请求处理

Gin 的路由机制是其核心功能之一，允许开发者定义和处理 HTTP 请求。

##### 1.1 路由注册

Gin 使用类似 HTTP 方法的函数来注册路由：
```go
r.GET("/path", handler)
r.POST("/path", handler)
r.PUT("/path", handler)
r.DELETE("/path", handler)
```
每个方法接受一个路径和一个处理函数。

##### 1.2 处理函数

处理函数签名为 `func(*gin.Context)`，示例：
```go
r.GET("/ping", func(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "pong",
    })
})
```

##### 1.3 动态路由

支持路径参数：
```go
r.GET("/user/:name", func(c *gin.Context) {
    name := c.Param("name")
    c.String(200, "Hello %s", name)
})
```

##### 1.4 查询参数

通过 `c.Query` 获取查询参数：
```go
r.GET("/welcome", func(c *gin.Context) {
    firstname := c.DefaultQuery("firstname", "Guest")
    lastname := c.Query("lastname")
    c.String(200, "Hello %s %s", firstname, lastname)
})
```

#### 2 中间件

中间件是 Gin 强大的扩展机制，用于在请求处理前后执行额外的操作。

##### 2.1 使用中间件

内置中间件：
```go
r := gin.Default() // 包含 Logger 和 Recovery 中间件
```

自定义中间件：
```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        // 在请求处理前
        t := time.Now()

        // 处理请求
        c.Next()

        // 在请求处理后
        latency := time.Since(t)
        log.Print(latency)
    }
}
r.Use(Logger())
```

##### 2.2 中间件应用

中间件可以应用于路由组：
```go
authorized := r.Group("/", AuthRequired())
{
    authorized.POST("/login", loginEndpoint)
    authorized.POST("/submit", submitEndpoint)
}
```

#### 3 参数解析

Gin 提供了多种方式解析请求参数，包括路径参数、查询参数、表单参数和 JSON 参数。

##### 3.1 表单参数

通过 `c.PostForm` 获取表单参数：
```go
r.POST("/form", func(c *gin.Context) {
    name := c.PostForm("name")
    message := c.PostForm("message")
    c.JSON(200, gin.H{
        "status":  "posted",
        "name":    name,
        "message": message,
    })
})
```

##### 3.2 JSON 参数

通过 `c.BindJSON` 解析 JSON 参数：
```go
type Login struct {
    User     string `json:"user"`
    Password string `json:"password"`
}

r.POST("/login", func(c *gin.Context) {
    var json Login
    if err := c.ShouldBindJSON(&json); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    if json.User == "admin" && json.Password == "admin" {
        c.JSON(200, gin.H{"status": "you are logged in"})
    } else {
        c.JSON(401, gin.H{"status": "unauthorized"})
    }
})
```

#### 4 返回响应

Gin 提供了多种方式返回响应，包括字符串、JSON、XML等格式。

##### 4.1 返回字符串

通过 `c.String` 返回字符串：
```go
r.GET("/string", func(c *gin.Context) {
    c.String(200, "Hello, %s", "Gin")
})
```

##### 4.2 返回 JSON

通过 `c.JSON` 返回 JSON：
```go
r.GET("/json", func(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "hello world",
        "status":  "success",
    })
})
```

##### 4.3 返回 XML

通过 `c.XML` 返回 XML：
```go
r.GET("/xml", func(c *gin.Context) {
    c.XML(200, gin.H{
        "message": "hello world",
        "status":  "success",
    })
})
```

#### 5 错误处理

Gin 提供了灵活的错误处理机制，可以通过自定义错误处理函数和中间件实现。

##### 5.1 内置错误处理

通过 `c.AbortWithStatus` 或 `c.AbortWithStatusJSON` 返回错误状态码：
```go
r.GET("/abort", func(c *gin.Context) {
    c.AbortWithStatusJSON(401, gin.H{"status": "unauthorized"})
})
```

##### 5.2 自定义错误处理

通过自定义中间件实现错误处理：
```go
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        if len(c.Errors) > 0 {
            c.JSON(-1, gin.H{"errors": c.Errors})
        }
    }
}
r.Use(ErrorHandler())
```

#### 6 日志和恢复中间件

Gin 提供了 `Logger` 和 `Recovery` 中间件，用于日志记录和异常恢复。

##### 6.1 日志中间件

默认启用日志中间件：
```go
r := gin.Default() // 包含 Logger 中间件
```

##### 6.2 恢复中间件

默认启用恢复中间件，处理未捕获的异常：
```go
r := gin.Default() // 包含 Recovery 中间件
```

也可以单独使用：
```go
r.Use(gin.Recovery())
```

### 总结
本章介绍了 Gin 框架的基本使用，包括路由与请求处理、中间件、参数解析、返回响应、错误处理和日志与恢复中间件的基本用法。这些内容帮助读者快速上手 Gin 框架，为后续深入解析其内部实现和高级应用打下基础。