# 中间件机制
### 第5章：中间件机制

#### 5.1 中间件的定义和使用

中间件是 Gin 框架中的一个强大特性，用于在请求被处理前或处理后执行一些额外的操作。

##### 5.1.1 中间件的定义

中间件是一个签名为 `func(*gin.Context)` 的函数。它可以在请求处理过程中通过 `Next()` 调用下一个处理函数或中间件。

示例：

```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        t := time.Now()
        
        // 处理请求
        c.Next()
        
        latency := time.Since(t)
        log.Print(latency)
    }
}
```

##### 5.1.2 中间件的使用

中间件可以通过 `Use` 方法全局使用，或在路由组中使用。

全局使用：

```go
r := gin.New()
r.Use(Logger())
```

路由组中使用：

```go
authorized := r.Group("/", AuthRequired())
{
    authorized.POST("/login", loginHandler)
    authorized.POST("/submit", submitHandler)
}
```

#### 5.2 内置中间件解析

Gin 提供了一些内置中间件，用于常见的功能。

##### 5.2.1 Logger 中间件

Logger 中间件用于记录 HTTP 请求日志。

```go
r := gin.New()
r.Use(gin.Logger())
```

##### 5.2.2 Recovery 中间件

Recovery 中间件用于处理未捕获的异常，防止服务器崩溃。

```go
r := gin.New()
r.Use(gin.Recovery())
```

##### 5.2.3 Cors 中间件

Cors 中间件用于处理跨域资源共享（CORS）。

示例：

```go
import "github.com/gin-contrib/cors"

r := gin.New()
r.Use(cors.Default())
```

#### 5.3 自定义中间件

自定义中间件可以实现特定的功能，如认证、日志记录、速率限制等。

示例：简单的认证中间件

```go
func AuthRequired() gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token != "valid-token" {
            c.AbortWithStatusJSON(401, gin.H{"error": "unauthorized"})
            return
        }
        c.Next()
    }
}
```

在路由组中使用自定义中间件：

```go
authorized := r.Group("/")
authorized.Use(AuthRequired())
{
    authorized.GET("/secure", secureEndpoint)
}
```

#### 5.4 中间件的执行顺序

中间件的执行顺序由它们注册的顺序决定。Gin 按照注册顺序依次执行中间件。

##### 5.4.1 全局中间件的执行顺序

全局中间件按注册顺序执行：

```go
r := gin.New()
r.Use(Middleware1())
r.Use(Middleware2())
```

##### 5.4.2 路由组中间件的执行顺序

路由组中的中间件在全局中间件之后执行：

```go
r := gin.New()
r.Use(GlobalMiddleware())

group := r.Group("/")
group.Use(GroupMiddleware())
{
    group.GET("/endpoint", endpointHandler)
}
```

执行顺序：`GlobalMiddleware` -> `GroupMiddleware` -> `endpointHandler`

##### 5.4.3 中间件中的控制流

在中间件中，可以通过 `c.Next()` 控制中间件的执行顺序和请求处理流程。调用 `c.Next()` 后，Gin 会继续执行后续的中间件或处理函数。

示例：

```go
func Middleware1() gin.HandlerFunc {
    return func(c *gin.Context) {
        log.Println("Middleware1 before")
        c.Next()
        log.Println("Middleware1 after")
    }
}

func Middleware2() gin.HandlerFunc {
    return func(c *gin.Context) {
        log.Println("Middleware2 before")
        c.Next()
        log.Println("Middleware2 after")
    }
}

r := gin.New()
r.Use(Middleware1(), Middleware2())
```

输出顺序：

```
Middleware1 before
Middleware2 before
Handler execution
Middleware2 after
Middleware1 after
```

### 总结

本章详细介绍了 Gin 框架中的中间件机制，包括中间件的定义和使用、内置中间件解析、自定义中间件和中间件的执行顺序。理解中间件的工作原理和使用方式，可以帮助开发者更灵活地处理 HTTP 请求，增加应用的扩展性和可维护性。