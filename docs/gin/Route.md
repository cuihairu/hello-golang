# 路由机制
### 路由机制

#### 4.1 路由注册

在 Gin 中，路由注册是通过关联 HTTP 方法和路径到特定处理函数来实现的。以下是如何注册不同 HTTP 方法的路由：

```go
r.GET("/path", handler)
r.POST("/path", handler)
r.PUT("/path", handler)
r.DELETE("/path", handler)
r.PATCH("/path", handler)
r.OPTIONS("/path", handler)
r.HEAD("/path", handler)
```

每个方法接受一个路径和一个处理函数 `func(*gin.Context)`。

示例：

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    r.GET("/hello", func(c *gin.Context) {
        c.String(200, "Hello, World!")
    })

    r.POST("/submit", func(c *gin.Context) {
        c.String(200, "Submission received")
    })

    r.Run(":8080")
}
```

#### 4.2 路由匹配

Gin 使用基于树的路由匹配算法，以保证高效的路由查找。

##### 4.2.1 精确匹配

Gin 首先尝试进行精确路径匹配。

```go
r.GET("/hello", func(c *gin.Context) {
    c.String(200, "Hello, World!")
})
```

##### 4.2.2 参数匹配

Gin 支持路径参数和通配符匹配。

路径参数：

```go
r.GET("/user/:name", func(c *gin.Context) {
    name := c.Param("name")
    c.String(200, "Hello %s", name)
})
```

通配符匹配：

```go
r.GET("/files/*filepath", func(c *gin.Context) {
    filepath := c.Param("filepath")
    c.String(200, "Requested file: %s", filepath)
})
```

#### 4.3 路由分组

路由分组用于将多个路由组织在一起，便于管理和应用中间件。

```go
v1 := r.Group("/v1")
{
    v1.GET("/login", loginHandler)
    v1.GET("/submit", submitHandler)
}

v2 := r.Group("/v2")
{
    v2.GET("/login", loginHandlerV2)
    v2.GET("/submit", submitHandlerV2)
}
```

分组中的路由可以共享中间件：

```go
authorized := r.Group("/", AuthRequired())
{
    authorized.POST("/login", loginHandler)
    authorized.POST("/submit", submitHandler)
}
```

#### 4.4 动态路由和静态路由

动态路由和静态路由是路由匹配的两种方式。

##### 4.4.1 静态路由

静态路由是指路径固定的路由：

```go
r.GET("/home", homeHandler)
r.POST("/login", loginHandler)
```

##### 4.4.2 动态路由

动态路由包括路径参数和通配符：

路径参数：

```go
r.GET("/user/:id", func(c *gin.Context) {
    id := c.Param("id")
    c.String(200, "User ID: %s", id)
})
```

通配符：

```go
r.GET("/static/*filepath", func(c *gin.Context) {
    filepath := c.Param("filepath")
    c.String(200, "Filepath: %s", filepath)
})
```

动态路由使得路径具有灵活性，可以处理多种情况。

### 总结

本章详细介绍了 Gin 的路由机制，包括路由注册、路由匹配、路由分组以及动态路由和静态路由。理解这些概念是掌握 Gin 框架的基础，有助于高效地组织和管理 Web 应用的路由。