### Overview of the Gin Framework

#### 1 What Gin is
Gin is a lightweight web framework written in Go. It has a short API and fast routing, and it is commonly used to write RESTful APIs and the HTTP layer of microservices.

#### 2 Features of Gin
- **Fast routing**: routing is built on an HTTP route tree, matching the path segment by segment.
- **Short API**: registering routes, reading parameters, and writing responses all hang off `*gin.Context`, so there isn't much code to write.
- **Middleware**: custom middleware can be inserted into the request handling chain.
- **Built-in middleware**: logging and recovery come included (a panic returns 500 instead of crashing the process).
- **Error responses**: methods like `c.JSON`/`c.String` control the status code and response body directly.

#### 3 Where Gin fits
- RESTful API services: routing plus middleware already covers most needs.
- Microservice architectures: every service's HTTP layer uses the same Gin approach.
- Rapid prototyping: a few routes get the endpoints running, which suits MVP validation.

#### 4 Installing Gin and a minimal example

##### 4.1 Installing Gin
In your Go environment, you can install Gin with:
```sh
go get -u github.com/gin-gonic/gin
```

##### 4.2 Minimal routing example
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

After it runs, visit `http://localhost:8080/ping`; the response is:
```json
{
    "message": "pong"
}
```

##### 4.3 Routing and request handling
Route matching goes through the HTTP route tree. Add a few more routes to see how parameters are read:

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

    // define a GET route with a parameter
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

In this example, the `/hello` route returns a JSON response that takes a `name` parameter, while the `/user/:name` route returns a JSON response that takes a URL parameter `name`.

### Summary
This page covers installing Gin, plus two kinds of routes: `/ping` and the parameterized `/user/:name`. Middleware, parameter binding, and grouped routes are each unpacked in later sections.

## References

- [Gin official documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/zh/gin/Config.md)
- [Debug](/zh/gin/Debug.md)
- [Error](/zh/gin/Error.md)
- [Extend](/zh/gin/Extend.md)
- [Middleware](/zh/gin/Middleware.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Middleware](/zh/gin/Middleware.md)
