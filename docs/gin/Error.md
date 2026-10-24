# Error handling
### Error handling

#### 8.1 Built-in error handling

Gin provides built-in error handling to make it easy to catch and deal with errors that happen during a request.

##### 8.1.1 The `c.Error` method

Use the `c.Error` method to record an error inside a handler:

```go
// someFunction represents any business call that can fail
func someFunction() error {
    return errors.New("something went wrong")
}

func handler(c *gin.Context) {
    err := someFunction()
    if err != nil {
        c.Error(err)  // record the error
        c.JSON(500, gin.H{"error": err.Error()})
        return
    }
    c.JSON(200, gin.H{"message": "Success"})
}
```

##### 8.1.2 Collecting and handling errors

Gin automatically collects every error recorded via `c.Error`, and you can handle them all in one place in a middleware or a handler:

```go
func errorHandlingMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()  // run the other handlers first

        // check whether any errors happened
        if len(c.Errors) > 0 {
            c.JSON(500, gin.H{"errors": c.Errors})
        }
    }
}
```

#### 8.2 Custom error handling

Where the built-in send-and-receive path doesn't cover a case, define your own error types and handling middleware.

##### 8.2.1 Custom error types

Bundle the status code and the message into a single type so you can send them together in the response:

```go
type AppError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
}

func (e AppError) Error() string {
    return e.Message
}
```

##### 8.2.2 Global error handling

Use middleware to implement global error handling:

```go
func customErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        // check whether any errors happened
        if len(c.Errors) > 0 {
            err := c.Errors[0].Err
            if appErr, ok := err.(AppError); ok {
                c.JSON(appErr.Code, appErr)
            } else {
                c.JSON(500, gin.H{"error": "Internal Server Error"})
            }
        }
    }
}
```

##### 8.2.3 Handling specific error types

Handle errors differently depending on their type:

```go
// ValidationError is a business-defined validation error type
type ValidationError struct {
    Field string
}

func (e ValidationError) Error() string {
    return "invalid field: " + e.Field
}

// someFunction returns a business error; here a validation error as an example
func someFunction() error {
    return ValidationError{Field: "age"}
}

func handler(c *gin.Context) {
    err := someFunction()
    if err != nil {
        if validationErr, ok := err.(ValidationError); ok {
            c.JSON(400, gin.H{"error": validationErr.Error()})
        } else {
            c.Error(err)
            c.JSON(500, gin.H{"error": "Internal Server Error"})
        }
        return
    }
    c.JSON(200, gin.H{"message": "Success"})
}
```

#### 8.3 Logging errors

Attaching an error to `c.Errors` only records it on the request. To be able to look it up later, you still need to get it into your logs.

##### 8.3.1 Using the built-in logger

Gin's built-in logger can record requests and error information:

```go
func main() {
    r := gin.Default()

    // use Gin's default logging middleware
    r.Use(gin.Logger())

    r.GET("/example", func(c *gin.Context) {
        c.String(200, "example")
    })

    r.Run()
}
```

##### 8.3.2 A custom logger

You can implement your own logging logic:

```go
func customLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        // record the request information
        log.Printf("Request: %s %s", c.Request.Method, c.Request.URL.Path)

        c.Next()

        // record the error information
        if len(c.Errors) > 0 {
            log.Printf("Errors: %v", c.Errors)
        }
    }
}

func main() {
    r := gin.New()

    // use the custom logging middleware
    r.Use(customLogger())

    r.GET("/example", func(c *gin.Context) {
        c.String(200, "example")
    })

    r.Run()
}
```

### Summary

Gin error handling comes in three steps: `c.Error(err)` attaches the error to the current request, a middleware reads `c.Errors` after `c.Next()` and dispatches a status code based on a type like `AppError`, and everything else falls back to a 500. For logging, start with the built-in `gin.Logger()` and swap in a custom middleware when you need extra fields.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)

## Sibling pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Extend](/gin/Extend.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Config](/gin/Config.md)
- [Debug](/gin/Debug.md)
- [Extend](/gin/Extend.md)
- [Gin](/gin/Gin.md)
- [Middleware](/gin/Middleware.md)
- [Optimize](/gin/Optimize.md)
- [Request](/gin/Request.md)
- [Response](/gin/Response.md)
- [Route](/gin/Route.md)
- [Source](/gin/Source.md)
- [Use](/gin/Use.md)
- [advanced](/gin/advanced.md)
