### Basic Usage of Gin

#### 1 Routes and Request Handling

To handle HTTP requests with Gin, start with routes.

##### 1.1 Route Registration

Gin uses HTTP-method-like functions to register routes:
```go
r := gin.Default()
handler := func(c *gin.Context) {}
r.GET("/path", handler)
r.POST("/path", handler)
r.PUT("/path", handler)
r.DELETE("/path", handler)
```
Each method takes a path and a handler function.

##### 1.2 Handler Functions

The handler function signature is `func(*gin.Context)`; for example:
```go
r := gin.Default()
r.GET("/ping", func(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "pong",
    })
})
```

##### 1.3 Dynamic Routes

Path parameters are supported:
```go
r := gin.Default()
r.GET("/user/:name", func(c *gin.Context) {
    name := c.Param("name")
    c.String(200, "Hello %s", name)
})
```

##### 1.4 Query Parameters

Read query parameters through `c.Query`:
```go
r := gin.Default()
r.GET("/welcome", func(c *gin.Context) {
    firstname := c.DefaultQuery("firstname", "Guest")
    lastname := c.Query("lastname")
    c.String(200, "Hello %s %s", firstname, lastname)
})
```

#### 2 Middleware

Middleware runs extra operations before or after request handling; logging, authentication, and panic recovery all go through this layer.

##### 2.1 Using Middleware

Built-in middleware:
```go
r := gin.Default() // includes the Logger and Recovery middleware
r.GET("/ping", func(c *gin.Context) {})
```

Custom middleware:
```go
func Logger() gin.HandlerFunc {
    return func(c *gin.Context) {
        // before handling the request
        t := time.Now()

        // handle the request
        c.Next()

        // after handling the request
        latency := time.Since(t)
        log.Print(latency)
    }
}

func main() {
    r := gin.New()
    r.Use(Logger())
}
```

##### 2.2 Applying Middleware

Middleware can be applied to route groups:
```go
func AuthRequired() gin.HandlerFunc {
    return func(c *gin.Context) {}
}

func main() {
    r := gin.New()
    loginEndpoint := func(c *gin.Context) {}
    submitEndpoint := func(c *gin.Context) {}
    authorized := r.Group("/", AuthRequired())
    {
        authorized.POST("/login", loginEndpoint)
        authorized.POST("/submit", submitEndpoint)
    }
}
```

#### 3 Parameter Parsing

Gin provides several ways to parse request parameters, including path parameters, query parameters, form parameters, and JSON parameters.

##### 3.1 Form Parameters

Read form parameters through `c.PostForm`:
```go
r := gin.Default()
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

##### 3.2 JSON Parameters

Parse JSON parameters through `c.ShouldBindJSON`:
```go
package main

import "github.com/gin-gonic/gin"

type Login struct {
    User     string `json:"user"`
    Password string `json:"password"`
}

func main() {
    r := gin.Default()
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
}
```

#### 4 Returning Responses

Gin provides several ways to return responses, including string, JSON, XML, and other formats.

##### 4.1 Returning a String

Return a string through `c.String`:
```go
r := gin.Default()
r.GET("/string", func(c *gin.Context) {
    c.String(200, "Hello, %s", "Gin")
})
```

##### 4.2 Returning JSON

Return JSON through `c.JSON`:
```go
r := gin.Default()
r.GET("/json", func(c *gin.Context) {
    c.JSON(200, gin.H{
        "message": "hello world",
        "status":  "success",
    })
})
```

##### 4.3 Returning XML

Return XML through `c.XML`:
```go
r := gin.Default()
r.GET("/xml", func(c *gin.Context) {
    c.XML(200, gin.H{
        "message": "hello world",
        "status":  "success",
    })
})
```

#### 5 Error Handling

Error handling has two paths: the built-in abort functions return a status code directly, or middleware catches errors in one place.

##### 5.1 Built-in Error Handling

Return an error status code through `c.AbortWithStatus` or `c.AbortWithStatusJSON`:
```go
r := gin.Default()
r.GET("/abort", func(c *gin.Context) {
    c.AbortWithStatusJSON(401, gin.H{"status": "unauthorized"})
})
```

##### 5.2 Custom Error Handling

Implement error handling through custom middleware:
```go
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        if len(c.Errors) > 0 {
            c.JSON(-1, gin.H{"errors": c.Errors})
        }
    }
}

func main() {
    r := gin.New()
    r.Use(ErrorHandler())
}
```

#### 6 Logger and Recovery Middleware

Gin provides the `Logger` and `Recovery` middleware for logging and panic recovery.

##### 6.1 Logger Middleware

The Logger middleware is enabled by default:
```go
r := gin.Default() // includes the Logger middleware
r.GET("/ping", func(c *gin.Context) {})
```

##### 6.2 Recovery Middleware

The Recovery middleware is enabled by default and handles uncaught panics:
```go
r := gin.Default() // includes the Recovery middleware
r.GET("/ping", func(c *gin.Context) {})
```

It can also be used on its own:
```go
r := gin.New()
r.Use(gin.Recovery())
```

### Summary
This page collects Gin's six commonly used areas: routes and request handling, middleware, parameter parsing, returning responses, error handling, and the built-in Logger and Recovery middleware. For everyday API development, these are enough.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Source](/gin/Source.md)
- [advanced](/gin/advanced.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Source](/gin/Source.md)
- [advanced](/gin/advanced.md)
