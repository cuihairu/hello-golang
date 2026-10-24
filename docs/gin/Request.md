# Request handling
### Request handling

#### 6.1 The request context (Context)

Gin uses the `gin.Context` struct to manage the lifetime of a request. `Context` gives you access to the request and the response, and carries the shared data between middleware.

##### 6.1.1 The basic structure of Context

The `gin.Context` struct holds the request and response information:

```go
type Context struct {
    Request  *http.Request
    Writer   http.ResponseWriter
    Params   Params
    Keys     map[string]interface{}
    Errors   errorMsgs
    // other fields...
}
```

##### 6.1.2 Using Context

Inside a handler, use `Context` to read the request data and set the response data:

```go
func handler(c *gin.Context) {
    // get request parameters
    name := c.Query("name")
    
    // set the response status code and response data
    c.JSON(200, gin.H{"message": "Hello " + name})
}
```

#### 6.2 Parsing request data

Gin gives you several ways to parse the data in an HTTP request: query parameters, form parameters, a JSON body, and more.

##### 6.2.1 Parsing query parameters

Use the `c.Query` method to parse the query parameters in the URL:

```go
func handler(c *gin.Context) {
    name := c.Query("name")
    c.String(200, "Hello %s", name)
}
```

##### 6.2.2 Parsing form parameters

Use the `c.PostForm` method to parse form parameters:

```go
func handler(c *gin.Context) {
    name := c.PostForm("name")
    c.String(200, "Hello %s", name)
}
```

##### 6.2.3 Parsing a JSON request body

Use the `c.ShouldBindJSON` method to parse a JSON request body:

```go
type Login struct {
    User     string `json:"user" binding:"required"`
    Password string `json:"password" binding:"required"`
}

func handler(c *gin.Context) {
    var json Login
    if err := c.ShouldBindJSON(&json); err != nil {
        c.JSON(400, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, gin.H{"message": "Login successful"})
}
```

##### 6.2.4 Parsing path parameters

Use the `c.Param` method to parse path parameters:

```go
func handler(c *gin.Context) {
    id := c.Param("id")
    c.String(200, "ID: %s", id)
}
```

#### 6.3 The request lifecycle

A request, from coming in to going back out, goes through these stages in Gin:

1. **Receive the request**: Gin receives the HTTP request and creates a new `gin.Context` instance.
2. **Middleware processing**: global middleware and route-group middleware run in registration order.
3. **Route matching**: the request path and method are matched against the routes to find the handler.
4. **Request handling**: the handler runs, parsing the request data and producing the response data.
5. **Post-middleware processing**: once the handler returns, middleware can keep going with their follow-up work.
6. **Send the response**: Gin sends the response data to the client, finishing the request.

#### 6.4 Streaming

Streaming is for scenarios like large file uploads, downloads, and real-time data transfer.

##### 6.4.1 File upload

Gin supports uploading multiple files:

```go
func uploadHandler(c *gin.Context) {
    file, err := c.FormFile("file")
    if err != nil {
        c.String(400, "get form file failed: %v", err)
        return
    }
    if err := c.SaveUploadedFile(file, "/path/to/save/"+file.Filename); err != nil {
        c.String(500, "save file failed: %v", err)
        return
    }
    c.String(200, "File uploaded successfully")
}
```

##### 6.4.2 File download

Use the `c.File` method to send a file to the client:

```go
func downloadHandler(c *gin.Context) {
    c.File("/path/to/file")
}
```

##### 6.4.3 SSE (Server-Sent Events)

Gin supports SSE for pushing real-time data:

```go
func sseHandler(c *gin.Context) {
    c.Stream(func(w io.Writer) bool {
        c.SSEvent("message", "Hello world")
        return true
    })
}
```

### Summary

Gin's request flow is: receive the request, run middleware, match the route, execute the handler, send the response, and `gin.Context` runs through all of it. Pick the parsing method by where the data comes from: `c.Query` for query parameters, `c.PostForm` for forms, `c.ShouldBindJSON` for JSON, and `c.Param` for path parameters.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)


## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Error](/gin/Error.md)
- [Optimize](/gin/Optimize.md)
- [Response](/gin/Response.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Optimize](/gin/Optimize.md)
- [Response](/gin/Response.md)
