### Gin Framework Overview

#### 1 What is Gin
Gin is a lightweight web framework written in Go. Its API is concise and its routing is fast, so it is commonly used for RESTful APIs and the HTTP layer of microservices.

#### 2 Features of Gin
- **Fast routing**: routing is built on an HTTP route tree that matches path segments one at a time.
- **Concise API**: registering routes, reading parameters, and returning a response all live on `*gin.Context`, so the code stays small.
- **Middleware**: custom middleware can be inserted into the request-handling chain.
- **Built-in middleware**: logging and recovery come standard (after a panic it returns 500 instead of crashing the process).
- **Error responses**: methods like `c.JSON`/`c.String` directly control the status code and response body.

#### 3 Use Cases for Gin
- RESTful API services: routing plus middleware already covers most needs.
- Microservice architecture: every service's HTTP layer uses the same Gin style.
- Rapid prototyping: a few routes get an API up and running, which suits MVP validation.

#### 4 Installing Gin and a Minimal Example

##### 4.1 Installing Gin
In your Go environment, you can install Gin with the following command:
```sh
go get -u github.com/gin-gonic/gin
```

##### 4.2 Minimal Route Example
A minimal HTTP server:

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    // create a default Gin router
    r := gin.Default()

    // define a simple GET route
    r.GET("/ping", func(c *gin.Context) {
        c.JSON(200, gin.H{
            "message": "pong",
        })
    })

    // start the HTTP server, listening on port 8080
    r.Run(":8080")
}
```

After running it, visit `http://localhost:8080/ping`; the response is:
```json
{
    "message": "pong"
}
```

##### 4.3 Routing and Request Handling
Route matching goes through the HTTP route tree; add a few more routes to see parameter extraction:

```go
package main

import (
    "github.com/gin-gonic/gin"
)

func main() {
    r := gin.Default()

    // define a simple GET route
    r.GET("/hello", func(c *gin.Context) {
        name := c.Query("name")
        if name == "" {
            name = "World"
        }
        c.JSON(200, gin.H{
            "message": "Hello " + name,
        })
    })

    // define a GET route with a path parameter
    r.GET("/user/:name", func(c *gin.Context) {
        name := c.Param("name")
        c.JSON(200, gin.H{
            "message": "Hello " + name,
        })
    })

    // start the HTTP server
    r.Run(":8080")
}
```

In this example, the `/hello` route returns a JSON response with the `name` query parameter, while the `/user/:name` route returns a JSON response with the URL parameter `name`.

### Summary
This page records how to install Gin, plus two kinds of routes: `/ping` and the parameterized `/user/:name`. Middleware, parameter binding, and grouped routing are each expanded in the later chapters.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Extend](/gin/Extend.md)
- [Middleware](/gin/Middleware.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Middleware](/gin/Middleware.md)
