# Routing Mechanism

#### 4.1 Route Registration

In Gin, route registration is done by associating an HTTP method and a path with a specific handler function. Here is how to register routes for the different HTTP methods:

```go
r.GET("/path", handler)
r.POST("/path", handler)
r.PUT("/path", handler)
r.DELETE("/path", handler)
r.PATCH("/path", handler)
r.OPTIONS("/path", handler)
r.HEAD("/path", handler)
```

Each method takes a path and a handler function `func(*gin.Context)`.

Example:

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

#### 4.2 Route Matching

Gin uses a tree-based route matching algorithm to ensure efficient route lookup.

##### 4.2.1 Exact Matching

Gin first attempts an exact path match.

```go
r.GET("/hello", func(c *gin.Context) {
    c.String(200, "Hello, World!")
})
```

##### 4.2.2 Parameter Matching

Gin supports path parameter and wildcard matching.

Path parameters:

```go
r.GET("/user/:name", func(c *gin.Context) {
    name := c.Param("name")
    c.String(200, "Hello %s", name)
})
```

Wildcard matching:

```go
r.GET("/files/*filepath", func(c *gin.Context) {
    filepath := c.Param("filepath")
    c.String(200, "Requested file: %s", filepath)
})
```

#### 4.3 Route Groups

Route groups are used to organize multiple routes together, making them easier to manage and to apply middleware to.

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

Routes within a group can share middleware:

```go
authorized := r.Group("/", AuthRequired())
{
    authorized.POST("/login", loginHandler)
    authorized.POST("/submit", submitHandler)
}
```

#### 4.4 Dynamic and Static Routes

Dynamic routes and static routes are two ways route matching works.

##### 4.4.1 Static Routes

Static routes are those with a fixed path:

```go
r.GET("/home", homeHandler)
r.POST("/login", loginHandler)
```

##### 4.4.2 Dynamic Routes

Dynamic routes include path parameters and wildcards:

Path parameters:

```go
r.GET("/user/:id", func(c *gin.Context) {
    id := c.Param("id")
    c.String(200, "User ID: %s", id)
})
```

Wildcards:

```go
r.GET("/static/*filepath", func(c *gin.Context) {
    filepath := c.Param("filepath")
    c.String(200, "Filepath: %s", filepath)
})
```

A single `/user/:id` or `/static/*filepath` route covers a whole class of paths, so there is no need to register a separate route for every value.

### Summary

Gin's routing comes in four parts: registration (HTTP method + path + handler), matching (exact, `:param` parameters, `*wildcard` wildcards), grouping (shared prefix and middleware), and static vs. dynamic paths. Organizing routes along these four parts keeps things orderly even as the route count grows.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Response](/gin/Response.md)
- [Source](/gin/Source.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Response](/gin/Response.md)
- [Source](/gin/Source.md)
