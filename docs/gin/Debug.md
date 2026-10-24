# Testing and debugging
### Testing and debugging

#### 11.1 Testing Gin

Most Gin tests never actually spin up an HTTP server: you build the routes, use `httptest.NewRecorder()` to capture the response, then compare the status code and body.

##### 11.1.1 Unit tests

Unit tests check a single component or function in your app and make sure it works as expected.

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/gin-gonic/gin"
)

func TestHelloWorld(t *testing.T) {
    // create a new Gin router
    r := gin.Default()
    r.GET("/hello", func(c *gin.Context) {
        c.String(http.StatusOK, "Hello, World!")
    })

    // create an HTTP request
    req, err := http.NewRequest(http.MethodGet, "/hello", nil)
    if err != nil {
        t.Fatalf("Failed to create request: %v", err)
    }

    // record the response
    resp := httptest.NewRecorder()
    r.ServeHTTP(resp, req)

    // verify the response status code
    if resp.Code != http.StatusOK {
        t.Errorf("Expected status code %d but got %d", http.StatusOK, resp.Code)
    }

    // verify the response body
    expectedBody := "Hello, World!"
    if resp.Body.String() != expectedBody {
        t.Errorf("Expected body %q but got %q", expectedBody, resp.Body.String())
    }
}
```

##### 11.1.2 Integration tests

Integration tests check how several parts of the app interact, and usually involve a full application environment and real requests and responses.

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
    "github.com/gin-gonic/gin"
)

func TestIntegration(t *testing.T) {
    r := gin.Default()
    r.GET("/greet/:name", func(c *gin.Context) {
        name := c.Param("name")
        c.JSON(http.StatusOK, gin.H{"greeting": "Hello, " + name})
    })

    req, err := http.NewRequest(http.MethodGet, "/greet/John", nil)
    if err != nil {
        t.Fatalf("Failed to create request: %v", err)
    }

    resp := httptest.NewRecorder()
    r.ServeHTTP(resp, req)

    if resp.Code != http.StatusOK {
        t.Errorf("Expected status code %d but got %d", http.StatusOK, resp.Code)
    }

    expectedBody := `{"greeting":"Hello, John"}`
    if resp.Body.String() != expectedBody {
        t.Errorf("Expected body %q but got %q", expectedBody, resp.Body.String())
    }
}
```

##### 11.1.3 Performance tests

Performance tests use `testing.B` to measure how long a single request takes to handle.

```go
import (
    "testing"
    "github.com/gin-gonic/gin"
    "net/http"
    "net/http/httptest"
)

func BenchmarkHelloWorld(b *testing.B) {
    r := gin.Default()
    r.GET("/hello", func(c *gin.Context) {
        c.String(http.StatusOK, "Hello, World!")
    })

    req, _ := http.NewRequest(http.MethodGet, "/hello", nil)
    resp := httptest.NewRecorder()

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        r.ServeHTTP(resp, req)
    }
}
```

#### 11.2 Unit tests and integration tests

##### 11.2.1 Unit tests

A unit test tests a single function or method in your code. They are usually automated and should run fast, with the focus on whether the code behaves as expected.

- **Test functions**: write a dedicated test function to check the logic of each handler.
- **Mock data**: use mocks or fake data to test how a function behaves with different inputs.

##### 11.2.2 Integration tests

Integration tests check how the parts of a system work together, and usually include interactions with a database, a cache, or other services.

- **Test the whole route**: integration tests that cover multiple handlers and middleware.
- **Mock services**: use a mock service in place of the real one and run end-to-end tests.

#### 11.3 Debugging common problems

When tracking down a problem, the most direct tool is to record the request and response.

##### 11.3.1 Debugging requests and responses

Use Gin's built-in logging, or a custom logging middleware, to record requests and responses so you can track things down.

```go
func debugLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        log.Printf("Request: %s %s", c.Request.Method, c.Request.URL.Path)
        c.Next()
        log.Printf("Response: %d", c.Writer.Status())
    }
}
```

Note: `c.Writer` is the `gin.ResponseWriter` interface. It only exposes methods like `Status()`, `Size()`, `Written()`, and `Header()`, and has no `Body` field, so you can't read the response body directly. If you really need to log the response body, define a type that wraps `http.ResponseWriter`, buffer the content in `Write`, and then emit it from your middleware.

func main() {
    r := gin.Default()
    r.Use(debugLogger())
    r.GET("/debug", func(c *gin.Context) {
        c.String(http.StatusOK, "Debug Info")
    })
    r.Run()
}
```

##### 11.3.2 Handling error messages

Include detailed error information when handling errors, so it's easy to find where the problem came from.

```go
func errorHandling() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        if len(c.Errors) > 0 {
            for _, e := range c.Errors {
                log.Printf("Error: %v", e.Err)
            }
            c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal Server Error"})
        }
    }
}
```

##### 11.3.3 Using debugging tools

Use Go's debugging tools (such as `delve`) to dig deeper: set breakpoints, inspect variable values, and look at the call stack.

```bash
dlv debug main.go
```

### Summary

Testing Gin is just `httptest`: unit tests, integration tests, and benchmarks all run without opening a real port. To debug, start with the request method, path, and response status code from your logging middleware; if that's not enough, use `dlv` to set breakpoints and inspect variables and the call stack.

## References

- [Gin Official Documentation](https://gin-gonic.com/en/docs/)
- [Gin · pkg.go.dev](https://pkg.go.dev/github.com/gin-gonic/gin)

## Sibling pages

- [Config](/zh/gin/Config.md)
- [Error](/zh/gin/Error.md)
- [Extend](/zh/gin/Extend.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Config](Config.md)
- [Error](Error.md)
- [Extend](Extend.md)
- [Gin](Gin.md)
- [Middleware](Middleware.md)
- [Optimize](Optimize.md)
- [Request](Request.md)
- [Response](Response.md)
- [Route](Route.md)
- [Source](Source.md)
- [Use](Use.md)
- [advanced](advanced.md)
