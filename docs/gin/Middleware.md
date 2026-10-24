# Middleware Mechanism
### Chapter 5: Middleware Mechanism

#### 5.1 Defining and Using Middleware

Middleware is a mechanism in the Gin framework: it runs extra operations before or after a request is handled.

##### 5.1.1 Defining Middleware

Middleware is a function with the signature `func(*gin.Context)`. During request handling it can call the next handler function or middleware through `Next()`.

Example:

```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        t := time.Now()
        
        // handle the request
        c.Next()
        
        latency := time.Since(t)
        log.Print(latency)
    }
}
```

##### 5.1.2 Using Middleware

Middleware can be used globally through the `Use` method, or inside a route group.

Global usage:

```go
r := gin.New()
r.Use(Logger())
```

Usage inside a route group:

```go
authorized := r.Group("/", AuthRequired())
{
    authorized.POST("/login", loginHandler)
    authorized.POST("/submit", submitHandler)
}
```

#### 5.2 Built-in Middleware Explained

Gin provides several built-in middleware for common functionality.

##### 5.2.1 Logger Middleware

The Logger middleware logs HTTP requests.

```go
r := gin.New()
r.Use(gin.Logger())
```

##### 5.2.2 Recovery Middleware

The Recovery middleware handles uncaught panics and prevents the server from crashing.

```go
r := gin.New()
r.Use(gin.Recovery())
```

##### 5.2.3 Cors Middleware

The Cors middleware handles cross-origin resource sharing (CORS).

Example:

```go
import (
    "github.com/gin-contrib/cors"
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.New()
    r.Use(cors.Default())
}
```

#### 5.3 Custom Middleware

Custom middleware can implement specific functionality such as authentication, logging, and rate limiting.

Example: a simple authentication middleware

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

Using custom middleware in a route group:

```go
authorized := r.Group("/")
authorized.Use(AuthRequired())
{
    authorized.GET("/secure", secureEndpoint)
}
```

#### 5.4 Middleware Execution Order

The order in which middleware executes is determined by the order they are registered in. Gin runs middleware one by one in registration order.

##### 5.4.1 Execution Order of Global Middleware

Global middleware executes in registration order:

```go
r := gin.New()
r.Use(Middleware1())
r.Use(Middleware2())
```

##### 5.4.2 Execution Order of Route Group Middleware

Middleware in a route group executes after global middleware:

```go
r := gin.New()
r.Use(GlobalMiddleware())

group := r.Group("/")
group.Use(GroupMiddleware())
{
    group.GET("/endpoint", endpointHandler)
}
```

Execution order: `GlobalMiddleware` -> `GroupMiddleware` -> `endpointHandler`

##### 5.4.3 Control Flow in Middleware

Inside middleware, you can use `c.Next()` to control the middleware execution order and the request-handling flow. After `c.Next()` is called, Gin continues with the remaining middleware or the handler function.

Example:

```go
package main

import (
    "fmt"
    "net/http/httptest"

    "github.com/gin-gonic/gin"
)

func Middleware1() gin.HandlerFunc {
    return func(c *gin.Context) {
        fmt.Println("Middleware1 before")
        c.Next()
        fmt.Println("Middleware1 after")
    }
}

func Middleware2() gin.HandlerFunc {
    return func(c *gin.Context) {
        fmt.Println("Middleware2 before")
        c.Next()
        fmt.Println("Middleware2 after")
    }
}

func main() {
    r := gin.New()
    r.Use(Middleware1(), Middleware2())
    r.GET("/", func(c *gin.Context) {
        fmt.Println("Handler execution")
        c.String(200, "ok")
    })

    // issue a request to observe the execution order of middleware and the handler
    w := httptest.NewRecorder()
    req := httptest.NewRequest("GET", "/", nil)
    r.ServeHTTP(w, req)
}
```

Output order:

```
Middleware1 before
Middleware2 before
Handler execution
Middleware2 after
Middleware1 after
```

### Summary

Middleware itself is a `func(*gin.Context)`: attach it globally or to a route group with `Use`, it executes in registration order, code before `c.Next()` runs before the business handling and code after it runs after, and `AbortWithStatusJSON` cuts the request off right there. Gin's `gin.Logger()`, `gin.Recovery()`, and third-party `cors` are all the same shell.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Gin](/gin/Gin.md)
- [Optimize](/gin/Optimize.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Gin](/gin/Gin.md)
- [Optimize](/gin/Optimize.md)
